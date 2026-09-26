#!/usr/bin/env python3
"""
Confident Agent Benchmark Runner
================================

Produces results; it does not evaluate them (that is evaluate_benchmark's job).

Runs every task of a dataset against a model served by LM Studio's
OpenAI-compatible API, in two configurations:

  baseline      The model gets instructions/Baseline/BASELINE_SYSTEM_PROMPT.md and
                the task. Its reply is logged and the code extracted. Nothing else.

  intervention  The Confidence Agent: the model gets the toolbox's
                CONFIDENCE_AGENT_PROMPT.md, the task, and the toolbox's
                verify_candidate tool through the API's function calling. The model
                decides when to call the tool and whether to correct (the prompt
                allows one correction after a verified_incorrect layer). This
                script executes each tool call with the toolbox itself
                (tool_bridge.cjs), feeds the result back, and records every turn,
                every verified candidate and whether a correction was attempted.

The benchmark never interprets the task for the model and never executes generated
code: the tool analyses candidates statically. Every file, folder and JSONL line is
written by this script, not by the model.

Usage
-----
    python run_benchmark.py --mode baseline     --model qwen/qwen3.5-9b --model-label "Qwen3.5-9B"
    python run_benchmark.py --mode intervention --model qwen/qwen3.5-9b --model-label "Qwen3.5-9B"
    python run_benchmark.py --mode both         --model qwen/qwen3.5-9b --model-label "Qwen3.5-9B"

Runs resume: a task whose folder already has result.json is skipped (use
--overwrite to redo it). See README.md and --help.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
TOOLBOX_DEFAULT = REPO / "confident-agent-toolbox"
DATASET_DEFAULT = ROOT / "dataset" / "rest_api_prompts_pilot.jsonl"
BASELINE_PROMPT_DEFAULT = ROOT / "instructions" / "Baseline" / "BASELINE_SYSTEM_PROMPT.md"
INTERVENTION_PROMPT_DEFAULT = TOOLBOX_DEFAULT / "instructions" / "CONFIDENCE_AGENT_PROMPT.md"
BRIDGE = ROOT / "tool_bridge.cjs"
MODE_DIRS = {"baseline": ROOT / "Baseline_Tests", "intervention": ROOT / "Intervention_Tests"}
MODE_JSONL = {"baseline": ROOT / "complete_test_baseline.jsonl", "intervention": ROOT / "complete_test_intervention.jsonl"}

CODE_FENCE_RE = re.compile(r"```(?:python|py)?[ \t]*\n(.*?)```", re.DOTALL)
THINK_RE = re.compile(r"^\s*<think>.*?</think>\s*", re.DOTALL)
LABEL_SAFE_RE = re.compile(r"[^A-Za-z0-9._-]+")
DELIVERED = ("deliver", "deliver_with_flag")


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------
def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(data: str | bytes) -> str:
    return hashlib.sha256(data.encode("utf-8") if isinstance(data, str) else data).hexdigest()


def sanitize_label(label: str) -> str:
    return LABEL_SAFE_RE.sub("_", label.strip()).strip("_") or "model"


def estimate_tokens(text: str) -> int:
    """~4 characters per token. Only used to keep requests under the context cap."""
    return max(1, len(text) // 4)


def message_tokens(messages: list) -> int:
    return sum(estimate_tokens(json.dumps(m, ensure_ascii=False)) for m in messages)


def strip_think(text: str) -> str:
    return THINK_RE.sub("", text or "").strip()


def extract_code(text: str) -> str | None:
    """First fenced Python block, or None when the reply contains no code block."""
    match = CODE_FENCE_RE.search(strip_think(text))
    return match.group(1).strip() if match else None


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def git_commit() -> str | None:
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(REPO), capture_output=True, text=True, timeout=10)
        return out.stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def load_dataset(path: Path) -> list:
    with path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load_intervention_prompt(path: Path) -> str:
    """The toolbox prompt opens with an operator note (blockquote lines) meant for
    people setting up LM Studio, not for the model. It is left out; the exact text
    sent is saved with the run."""
    lines = path.read_text(encoding="utf-8").splitlines()
    return "\n".join(l for l in lines if not l.startswith(">")).replace("\n\n\n", "\n\n").strip() + "\n"


# --------------------------------------------------------------------------
# LM Studio client
# --------------------------------------------------------------------------
class LMStudioError(RuntimeError):
    pass


def http_json(url: str, payload: dict | None, timeout: int) -> dict:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise LMStudioError(f"HTTP {e.code} from {url}: {e.read().decode('utf-8', 'replace')[:500]}") from e
    except urllib.error.URLError as e:
        raise LMStudioError(f"Cannot reach {url}: {e.reason}") from e


def chat(args, messages: list, max_tokens: int, tools: list | None = None) -> dict:
    payload = {"model": args.model, "messages": messages, "temperature": args.temperature,
               "max_tokens": max_tokens, "stream": False}
    if args.seed is not None:
        payload["seed"] = args.seed
    if args.thinking == "off":
        payload["reasoning_effort"] = "none"  # the switch LM Studio honours for Qwen3.5 thinking
    if tools:
        payload["tools"] = tools
    return http_json(args.api_base.rstrip("/") + "/chat/completions", payload, args.request_timeout)


def model_info(args) -> dict:
    """What LM Studio reports about the model (quantization, loaded context). Best effort."""
    base = re.sub(r"/v1/?$", "", args.api_base.rstrip("/"))
    try:
        models = http_json(base + "/api/v0/models", None, 15).get("data", [])
        return next((m for m in models if m.get("id") == args.model), {})
    except LMStudioError:
        return {}


def preflight(args) -> dict:
    listed = http_json(args.api_base.rstrip("/") + "/models", None, 15).get("data", [])
    if args.model not in {m.get("id") for m in listed}:
        sys.exit(f"Model {args.model!r} is not served by LM Studio at {args.api_base}. Available: "
                 + ", ".join(m.get("id", "?") for m in listed))
    info = model_info(args)
    loaded = info.get("loaded_context_length")
    if isinstance(loaded, int) and loaded < args.context_limit:
        print(f"[setup] The model is loaded with a {loaded}-token context; using that instead of "
              f"--context-limit {args.context_limit}.", flush=True)
        args.context_limit = loaded
    return info


def budget(messages: list, args) -> int:
    """max_tokens that keeps the estimated prompt plus reply under the context cap."""
    return min(args.max_tokens, args.context_limit - message_tokens(messages) - 256)


# --------------------------------------------------------------------------
# Toolbox (intervention)
# --------------------------------------------------------------------------
def toolbox_python(toolbox: Path) -> str:
    if os.environ.get("CONFIDENCE_PYTHON"):
        return os.environ["CONFIDENCE_PYTHON"]
    for candidate in (toolbox / ".venv" / "Scripts" / "python.exe", toolbox / ".venv" / "bin" / "python"):
        if candidate.exists():
            return str(candidate)
    return "python"


def ensure_toolbox_built(toolbox: Path) -> None:
    if (toolbox / "dist" / "confidenceAgentTools.js").exists():
        return
    npm = shutil.which("npm")  # resolves npm.cmd on Windows
    if not npm:
        sys.exit("The toolbox is not built and npm was not found. Run `npm ci && npm run build` in " + str(toolbox))
    print("[setup] Building the toolbox (npm ci && npm run build) ...", flush=True)
    if not (toolbox / "node_modules").exists():
        subprocess.run([npm, "ci", "--no-audit", "--no-fund"], cwd=str(toolbox), check=True)
    subprocess.run([npm, "run", "build"], cwd=str(toolbox), check=True)


def bridge(args, request: dict | None = None, describe: bool = False) -> dict:
    cmd = ["node", str(BRIDGE), str(args.toolbox)] + (["--describe"] if describe else [])
    env = {**os.environ, "CONFIDENCE_PYTHON": args.python}
    try:
        out = subprocess.run(cmd, input=json.dumps(request or {}), capture_output=True, text=True,
                             encoding="utf-8", timeout=args.tool_timeout, env=env)
    except subprocess.TimeoutExpired:
        return {"error": f"verify_candidate timed out after {args.tool_timeout} s."}
    try:
        return json.loads(out.stdout)
    except json.JSONDecodeError:
        return {"error": f"Tool bridge failed (exit {out.returncode}): {(out.stderr or out.stdout)[-500:]}"}


def verify_tool_schema(args) -> list:
    described = bridge(args, describe=True)
    if "error" in described:
        sys.exit(described["error"])
    return [{"type": "function", "function": {
        "name": "verify_candidate", "description": described["description"],
        "parameters": {"type": "object", "properties": {
            "code": {"type": "string", "description": "The complete Python candidate to verify."}},
            "required": ["code"]}}}]


# --------------------------------------------------------------------------
# Runs
# --------------------------------------------------------------------------
def settings_fingerprint(mode: str, args, prompt: str) -> dict:
    fp = {"mode": mode, "model": args.model, "system_prompt_sha256": sha256(prompt), "temperature": args.temperature,
          "max_tokens": args.max_tokens, "thinking": args.thinking, "seed": args.seed}
    if mode == "intervention":
        fp["max_turns"] = args.max_turns
    return fp


def open_run(mode: str, args, prompt: str, info: dict) -> Path:
    """Folder for this model label and mode, with the settings every result in it shares."""
    run_dir = MODE_DIRS[mode] / sanitize_label(args.model_label or args.model)
    run_dir.mkdir(parents=True, exist_ok=True)
    fingerprint = settings_fingerprint(mode, args, prompt)
    manifest_path = run_dir / "run_manifest.json"
    if manifest_path.exists() and not args.overwrite:
        previous = json.loads(manifest_path.read_text(encoding="utf-8")).get("settings")
        if previous != fingerprint:
            sys.exit(f"{run_dir} holds results produced with different settings:\n  before: {previous}\n  now:    "
                     f"{fingerprint}\nUse a new --model-label, or --overwrite to redo every task.")
    (run_dir / "system_prompt.md").write_text(prompt, encoding="utf-8")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {"invocations": []}
    manifest.update({"settings": fingerprint, "model_label": run_dir.name, "api_base": args.api_base,
                     "lmstudio_model_info": info, "context_limit": args.context_limit,
                     "request_timeout_seconds": args.request_timeout})
    if mode == "intervention":
        manifest.update({"toolbox": str(args.toolbox), "verification_python": args.python,
                         "toolbox_prompt_source": str(args.intervention_prompt)})
    manifest["invocations"].append({"started": now(), "git_commit": git_commit(), "dataset": str(args.dataset),
                                    "dataset_sha256": sha256(args.dataset.read_bytes()), "argv": sys.argv[1:]})
    write_json(manifest_path, manifest)
    return run_dir


def rebuild_jsonl(mode: str) -> None:
    """The JSONL file is an index of every result.json of this mode (all model labels),
    so an interrupted or resumed run never leaves duplicate or missing lines."""
    rows = []
    for result in sorted(MODE_DIRS[mode].glob("*/*/result.json")):
        rows.append(json.loads(result.read_text(encoding="utf-8"))["jsonl"])
    MODE_JSONL[mode].write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def run_mode(mode: str, tasks: list, args, info: dict) -> None:
    prompt = (args.baseline_prompt.read_text(encoding="utf-8") if mode == "baseline"
              else load_intervention_prompt(args.intervention_prompt))
    tools = verify_tool_schema(args) if mode == "intervention" else None
    run_dir = open_run(mode, args, prompt, info)
    for n, task in enumerate(tasks, 1):
        task_dir = run_dir / task["task_id"]
        if (task_dir / "result.json").exists() and not args.overwrite:
            print(f"[{mode}] {n}/{len(tasks)} {task['task_id']}: done earlier, skipped", flush=True)
            continue
        if task_dir.exists():
            shutil.rmtree(task_dir)  # a partial folder from an interrupted task
        task_dir.mkdir(parents=True)
        started = time.time()
        record = (run_baseline_task if mode == "baseline" else run_intervention_task)(task, prompt, tools, task_dir, args)
        record["meta"].update({"task_id": task["task_id"], "mode": mode, "model": args.model, "model_label": run_dir.name,
                               "instruction": task["natural_language_instruction"], "finished": now(),
                               "duration_seconds": round(time.time() - started, 3)})
        record["jsonl"] = {"prompt_id": task["task_id"], "model": args.model, "model_label": run_dir.name, **record["jsonl"]}
        write_json(task_dir / "result.json", record)
        rebuild_jsonl(mode)
        print(f"[{mode}] {n}/{len(tasks)} {task['task_id']}: {record['summary']} ({record['meta']['duration_seconds']} s)", flush=True)


def run_baseline_task(task: dict, prompt: str, tools, task_dir: Path, args) -> dict:
    messages = [{"role": "system", "content": prompt}, {"role": "user", "content": task["natural_language_instruction"]}]
    error, text, code, response = None, "", None, None
    max_tokens = budget(messages, args)
    if max_tokens <= 0:
        error = f"prompt exceeds the {args.context_limit}-token context"
    else:
        try:
            response = chat(args, messages, max_tokens)
            text = response["choices"][0]["message"].get("content") or ""
            code = extract_code(text)
            write_json(task_dir / "raw_response.json", response)
        except (LMStudioError, KeyError, IndexError, TypeError) as e:
            error = str(e)
    finish = response["choices"][0].get("finish_reason") if response else None
    (task_dir / "response.md").write_text(text, encoding="utf-8")
    (task_dir / "solution.py").write_text(code or "", encoding="utf-8")
    return {"meta": {"finish_reason": finish, "usage": response.get("usage") if response else None, "error": error},
            "jsonl": {"code": code, "has_code_block": code is not None, "finish_reason": finish, "error": error},
            "summary": error or ("code" if code is not None else "no code block") + (f", {finish}" if finish != "stop" else "")}


def run_intervention_task(task: dict, prompt: str, tools, task_dir: Path, args) -> dict:
    messages = [{"role": "system", "content": prompt}, {"role": "user", "content": task["natural_language_instruction"]}]
    turns, verifications, other_tools, error, reply, finish = [], [], [], None, None, None
    turns_dir = task_dir / "turns"
    turns_dir.mkdir()
    for turn in range(1, args.max_turns + 1):
        max_tokens = budget(messages, args)
        if max_tokens <= 0:
            error = f"conversation exceeds the {args.context_limit}-token context"
            break
        try:
            response = chat(args, messages, max_tokens, tools)
            message = response["choices"][0]["message"]
            finish = response["choices"][0].get("finish_reason")
        except (LMStudioError, KeyError, IndexError, TypeError) as e:
            error = f"model request failed: {e}"
            break
        write_json(turns_dir / f"turn_{turn:02d}_response.json", response)
        calls = message.get("tool_calls") or []
        messages.append({"role": "assistant", "content": message.get("content") or "", **({"tool_calls": calls} if calls else {})})
        turns.append({"turn": turn, "finish_reason": finish, "usage": response.get("usage"), "tool_calls": [c.get("function", {}).get("name") for c in calls]})
        if not calls:
            reply = strip_think(message.get("content") or "")
            break
        for call in calls:
            name = call.get("function", {}).get("name")
            try:
                arguments = json.loads(call.get("function", {}).get("arguments") or "{}")
            except json.JSONDecodeError:
                arguments = None
            if name != "verify_candidate":
                result = {"error": f"Tool {name} is not available in this benchmark; only verify_candidate is provided."}
                other_tools.append(name)
            elif not isinstance(arguments, dict) or not isinstance(arguments.get("code"), str):
                result = {"error": "verify_candidate needs a code string."}
            else:
                result = bridge(args, {"name": "verify_candidate", "arguments": arguments})
                index = len(verifications) + 1
                (task_dir / f"verified_candidate_{index}.py").write_text(arguments["code"], encoding="utf-8")
                write_json(task_dir / f"verification_{index}.json", result)
                layers = result.get("layers") or []
                verifications.append({
                    "index": index, "turn": turn, "code": arguments["code"], "code_sha256": sha256(arguments["code"]),
                    "decision": result.get("decision"), "ewcs": (result.get("ewcs_report") or {}).get("ewcs"),
                    "layers": {l.get("layer"): l.get("state") for l in layers},
                    "has_contradiction": any(l.get("state") == "verified_incorrect" for l in layers),
                    "evidence_selection": result.get("evidence_selection"), "report": result.get("report"),
                    "error": result.get("error"), "extra_arguments": sorted(k for k in arguments if k != "code")})
            messages.append({"role": "tool", "tool_call_id": call.get("id", ""), "content": json.dumps(result, ensure_ascii=False)})
    else:
        error = f"stopped after {args.max_turns} model turns without a final reply"
    write_json(task_dir / "conversation.json", messages)
    (task_dir / "response.md").write_text(reply or "", encoding="utf-8")
    return intervention_record(verifications, other_tools, turns, reply, finish, error)


def intervention_record(verifications, other_tools, turns, reply, finish, error) -> dict:
    """What the model did, and what the tool decided. Only the tool's decisions count as
    decisions; the model's compliance with the prompt is recorded, not enforced."""
    first = verifications[0] if verifications else None
    final = verifications[-1] if verifications else None
    # A correction is a resubmission of different code after the first verification.
    codes = [v["code_sha256"] for v in verifications]
    changes = sum(1 for a, b in zip(codes, codes[1:]) if a != b)
    attempted = changes > 0
    allowed = bool(first and first["has_contradiction"])
    decision = final["decision"] if final else None
    delivered = final["code"] if final and decision in DELIVERED else None
    reply_code = extract_code(reply) if reply else None
    notes = []
    if not verifications:
        notes.append("never called verify_candidate")
    if attempted and not allowed:
        notes.append("corrected without a verified_incorrect layer")
    if changes > 1:
        notes.append("more than one correction")
    if allowed and not attempted:
        notes.append("did not correct after a verified_incorrect layer")
    if len(codes) - 1 > changes:
        notes.append("verified the same code more than once")
    if other_tools:
        notes.append("called unavailable tool(s): " + ", ".join(sorted(set(filter(None, other_tools)))))
    if reply is not None and final and final.get("report") and reply.strip() != final["report"].strip():
        notes.append("reply differs from the final report")
    if reply_code is not None and decision not in DELIVERED:
        notes.append("reply shows code the tool did not approve")
    if any(v["extra_arguments"] for v in verifications):
        notes.append("passed arguments other than code")
    correction = {"attempted": attempted, "allowed": allowed, "count": changes,
                  "first_decision": first["decision"] if first else None,
                  "first_layers": first["layers"] if first else None,
                  "final_decision_after_correction": decision if attempted else None}
    summary = (error or f"{decision or 'no verification'}; {len(verifications)} verification(s)"
               + ("; correction attempted" if attempted else "") + (f"; {len(notes)} protocol note(s)" if notes else ""))
    return {
        "meta": {"turns": turns, "verifications": [{k: v for k, v in x.items() if k != "code"} for x in verifications],
                 "correction": correction, "protocol_notes": notes, "final_finish_reason": finish, "error": error},
        "jsonl": {"decision": decision, "ewcs": final["ewcs"] if final else None, "code_output": delivered,
                  "first_candidate": first["code"] if first else None, "final_candidate": final["code"] if final else None,
                  "reply_code": reply_code, "verification_calls": len(verifications),
                  "correction_attempted": attempted, "correction_allowed": allowed, "correction_count": changes,
                  "first_decision": correction["first_decision"], "first_has_contradiction": allowed,
                  "protocol_notes": notes, "error": error},
        "summary": summary}


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------
def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Confident Agent Benchmark Runner (produces results only)")
    p.add_argument("--mode", choices=["baseline", "intervention", "both"], required=True)
    p.add_argument("--model", required=True, help="Model identifier exactly as LM Studio serves it (lms ps)")
    p.add_argument("--model-label", default=None, help="Results folder name for this model/quantization, e.g. 'Qwen3.5-9B-Q4'")
    p.add_argument("--api-base", default="http://127.0.0.1:1234/v1")
    p.add_argument("--dataset", type=Path, default=DATASET_DEFAULT)
    p.add_argument("--tasks", default=None, help="Comma-separated task ids to run (default: all)")
    p.add_argument("--limit", type=int, default=None, help="Only the first N tasks (smoke test)")
    p.add_argument("--toolbox", type=Path, default=TOOLBOX_DEFAULT, help="confident-agent-toolbox folder (default: the repo's)")
    p.add_argument("--baseline-prompt", type=Path, default=BASELINE_PROMPT_DEFAULT)
    p.add_argument("--intervention-prompt", type=Path, default=INTERVENTION_PROMPT_DEFAULT)
    p.add_argument("--temperature", type=float, default=0.2)
    p.add_argument("--seed", type=int, default=None, help="Sampling seed sent to LM Studio (recorded)")
    p.add_argument("--thinking", choices=["off", "on"], default="off",
                   help="off sends reasoning_effort 'none' (much faster on CPU); recorded with the results")
    p.add_argument("--max-tokens", type=int, default=4096, help="Ceiling per reply; shrunk to fit the context")
    p.add_argument("--context-limit", type=int, default=32768,
                   help="Context length the model is loaded with; lowered automatically to what LM Studio reports")
    # The prompt's workflow needs at most 3 turns (verify, correct once, reply); one spare
    # turn lets a deviation show before a looping model is stopped.
    p.add_argument("--max-turns", type=int, default=4, help="Model turns per intervention task before it is stopped")
    p.add_argument("--request-timeout", type=int, default=900, help="Seconds per model request")
    p.add_argument("--tool-timeout", type=int, default=300, help="Seconds per verify_candidate call")
    p.add_argument("--overwrite", action="store_true", help="Redo tasks that already have results")
    return p


def main() -> None:
    # Windows consoles default to cp1252; a model reply or error text must not crash the run.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    args = build_arg_parser().parse_args()
    args.toolbox = args.toolbox.resolve()
    args.python = toolbox_python(args.toolbox)
    tasks = load_dataset(args.dataset)
    if args.tasks:
        wanted = [t.strip() for t in args.tasks.split(",") if t.strip()]
        known = {t["task_id"]: t for t in tasks}
        missing = [t for t in wanted if t not in known]
        if missing:
            sys.exit("Unknown task id(s): " + ", ".join(missing))
        tasks = [known[t] for t in wanted]
    if args.limit:
        tasks = tasks[: args.limit]
    info = preflight(args)
    modes = ["baseline", "intervention"] if args.mode == "both" else [args.mode]
    if "intervention" in modes:
        ensure_toolbox_built(args.toolbox)
        if args.context_limit < 16000:
            print(f"[setup] Warning: a {args.context_limit}-token context is tight for the intervention (system prompt "
                  "~2.6K tokens, each verify_candidate result ~2.5K). Load the model with 16K or more.", flush=True)
    for mode in modes:
        run_mode(mode, tasks, args, info)
    print("Done.")


if __name__ == "__main__":
    main()
