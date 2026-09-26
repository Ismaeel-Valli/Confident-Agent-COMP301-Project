#!/usr/bin/env python3
"""
Confident Agent Benchmark Runner
=================================

Runs a dataset of REST-API code-generation tasks against a model served by
LM Studio (OpenAI-compatible /v1/chat/completions endpoint), in one of two
configurable modes:

  baseline      - the model is given BASELINE_SYSTEM_PROMPT.md and asked to
                  write the candidate. Nothing else happens.

  intervention  - the model is given CONFIDENCE_AGENT_SYSTEM_PROMPT.md and
                  asked to write the candidate. The benchmark (never the
                  model) then runs the candidate through the
                  confident-agent-toolbox's external verification
                  controller (dist/verificationCli.js), which performs the
                  six-layer static verification, computes EWCS, makes the
                  deliver / deliver_with_flag / abstain decision, and
                  (optionally) requests one model-side correction of a
                  contradicted candidate.

All logging, folder creation, and JSONL bookkeeping is performed by this
script. The model only ever sees a task and returns code.

Usage
-----
    python run_benchmark.py --mode baseline --model qwen2.5-coder-7b-instruct
    python run_benchmark.py --mode intervention --model qwen2.5-coder-7b-instruct
    python run_benchmark.py --mode both --model qwen2.5-coder-7b-instruct

By default this looks for LM Studio at http://127.0.0.1:1234/v1 and reads
the pilot dataset at dataset/rest_api_prompts_pilot.jsonl. Override with
--api-base / --dataset. See --help for all options.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATASET_DEFAULT = ROOT / "dataset" / "rest_api_prompts_pilot.jsonl"
TOOLBOX_DEFAULT = ROOT / "toolbox" / "confident-agent-toolbox"
BASELINE_PROMPT_DEFAULT = ROOT / "instructions" / "Baseline" / "BASELINE_SYSTEM_PROMPT.md"
INTERVENTION_PROMPT_DEFAULT = ROOT / "instructions" / "Intervention" / "CONFIDENCE_AGENT_SYSTEM_PROMPT.md"
BASELINE_TESTS_DIR_DEFAULT = ROOT / "Baseline_Tests"
INTERVENTION_TESTS_DIR_DEFAULT = ROOT / "Intervention_Tests"
BASELINE_JSONL_DEFAULT = ROOT / "complete_test_baseline.jsonl"
INTERVENTION_JSONL_DEFAULT = ROOT / "complete_test_intervention.jsonl"

CODE_FENCE_RE = re.compile(r"```(?:python)?\s*\n(.*?)```", re.DOTALL)

_LABEL_SAFE_RE = re.compile(r"[^A-Za-z0-9._-]+")


def sanitize_label(label: str) -> str:
    """Turn a model id like 'qwen2.5-9b-instruct-q8_0' or a free-form label
    like 'Qwen 9B Q8' into a filesystem-safe folder name."""
    cleaned = _LABEL_SAFE_RE.sub("_", label.strip())
    return cleaned.strip("_") or "model"


def estimate_tokens(text: str) -> int:
    """Rough token estimate (~4 chars/token for English/code). This is a
    stdlib-only approximation, not the model's real tokenizer — it exists
    only so the benchmark can refuse to send a prompt that would clearly
    blow the context cap, and to leave enough room for the reply. The real
    enforcement of the context cap is the context length the model was
    loaded with in LM Studio (see README / --context-limit)."""
    return max(1, len(text) // 4)


def effective_max_tokens(system_prompt: str, user_prompt: str, requested_max_tokens: int,
                          context_limit: int, margin: int = 64) -> int:
    """Shrink max_tokens so estimated prompt + completion tokens stay under
    context_limit. Returns 0 if the prompt alone leaves no room."""
    prompt_tokens = estimate_tokens(system_prompt) + estimate_tokens(user_prompt)
    available = context_limit - prompt_tokens - margin
    if available <= 0:
        return 0
    return min(requested_max_tokens, available)


# --------------------------------------------------------------------------
# Dataset
# --------------------------------------------------------------------------
def load_dataset(path: Path):
    tasks = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            tasks.append(json.loads(line))
    return tasks


# --------------------------------------------------------------------------
# LM Studio client
# --------------------------------------------------------------------------
def chat_completion(api_base: str, model: str, system_prompt: str, user_prompt: str,
                     temperature: float = 0.2, max_tokens: int = 2048, timeout: int = 300) -> dict:
    """POST to {api_base}/chat/completions. Returns the parsed JSON response."""
    url = api_base.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def extract_message_text(response_json: dict) -> str:
    try:
        return response_json["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError, TypeError):
        return ""


def strip_think_tags(text: str) -> str:
    return re.sub(r"^\s*<think>.*?</think>\s*", "", text, flags=re.DOTALL).strip()


def extract_code(raw_text: str) -> str:
    """Pull the code out of a fenced ```python block. Falls back to the raw
    text (stripped) if no fence is found, so a non-conforming reply is still
    logged rather than silently dropped."""
    text = strip_think_tags(raw_text)
    match = CODE_FENCE_RE.search(text)
    if match:
        return match.group(1).strip()
    return text.strip()


# --------------------------------------------------------------------------
# Baseline mode
# --------------------------------------------------------------------------
def run_baseline(tasks, args):
    system_prompt = args.baseline_prompt.read_text(encoding="utf-8")
    model_label = sanitize_label(args.model_label or args.model)
    out_dir = args.baseline_dir / model_label
    out_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = args.baseline_jsonl

    for task in tasks:
        task_id = task["task_id"]
        instruction = task["natural_language_instruction"]
        print(f"[baseline] {model_label} / {task_id} ...", flush=True)

        task_dir = out_dir / task_id
        task_dir.mkdir(parents=True, exist_ok=True)

        started = time.time()
        error = None
        raw_text = ""
        code = ""
        gen_max_tokens = effective_max_tokens(system_prompt, instruction, args.max_tokens, args.context_limit)
        if gen_max_tokens <= 0:
            error = (f"prompt alone (~{estimate_tokens(system_prompt) + estimate_tokens(instruction)} "
                      f"estimated tokens) leaves no room under --context-limit {args.context_limit}")
            print(f"    ERROR: {error}", file=sys.stderr)
        else:
            try:
                response_json = chat_completion(args.api_base, args.model, system_prompt, instruction,
                                                 temperature=args.temperature, max_tokens=gen_max_tokens)
                raw_text = extract_message_text(response_json)
                code = extract_code(raw_text)
                (task_dir / "raw_response.json").write_text(json.dumps(response_json, indent=2), encoding="utf-8")
            except Exception as e:  # noqa: BLE001 - benchmark must keep going on a single failed task
                error = str(e)
                print(f"    ERROR: {error}", file=sys.stderr)

        (task_dir / "solution.py").write_text(code, encoding="utf-8")
        (task_dir / "response.md").write_text(raw_text, encoding="utf-8")
        meta = {
            "task_id": task_id,
            "mode": "baseline",
            "model": args.model,
            "model_label": model_label,
            "api_base": args.api_base,
            "context_limit": args.context_limit,
            "requested_max_tokens": args.max_tokens,
            "effective_max_tokens": gen_max_tokens,
            "instruction": instruction,
            "started": started,
            "duration_seconds": round(time.time() - started, 3),
            "error": error,
        }
        (task_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

        append_jsonl(jsonl_path, {
            "prompt_id": task_id,
            "model": args.model,
            "model_label": model_label,
            "code": code,
            "error": error,
        })


# --------------------------------------------------------------------------
# Intervention mode
# --------------------------------------------------------------------------
def ensure_toolbox_built(toolbox_dir: Path):
    cli = toolbox_dir / "dist" / "verificationCli.js"
    if cli.exists():
        return
    print("[intervention] dist/verificationCli.js not found - building toolbox (npm install && npm run build) ...")
    subprocess.run(["npm", "install", "--no-audit", "--no-fund"], cwd=str(toolbox_dir), check=True)
    subprocess.run(["npm", "run", "build"], cwd=str(toolbox_dir), check=True)
    if not cli.exists():
        raise RuntimeError(f"Toolbox build did not produce {cli}")


def run_verifier(toolbox_dir: Path, candidate_path: Path, task_text: str, out_dir: Path,
                  api_base: str, model: str, enable_correction: bool) -> dict:
    cli = toolbox_dir / "dist" / "verificationCli.js"
    cmd = [
        "node", str(cli),
        "--code", str(candidate_path),
        "--task", task_text,
        "--endpoint", api_base,
        "--out-dir", str(out_dir),
    ]
    if enable_correction:
        cmd += ["--model", model]
    result = subprocess.run(cmd, cwd=str(toolbox_dir), capture_output=True, text=True, timeout=600)
    stdout, stderr = result.stdout, result.stderr
    audit_path = out_dir / "audit.json"
    audit = json.loads(audit_path.read_text(encoding="utf-8")) if audit_path.exists() else None
    return {
        "returncode": result.returncode,
        "stdout": stdout,
        "stderr": stderr,
        "audit": audit,
    }


def run_intervention(tasks, args):
    system_prompt = args.intervention_prompt.read_text(encoding="utf-8")
    model_label = sanitize_label(args.model_label or args.model)
    out_dir = args.intervention_dir / model_label
    out_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = args.intervention_jsonl

    ensure_toolbox_built(args.toolbox)

    for task in tasks:
        task_id = task["task_id"]
        instruction = task["natural_language_instruction"]
        print(f"[intervention] {model_label} / {task_id} ...", flush=True)

        task_dir = out_dir / task_id
        task_dir.mkdir(parents=True, exist_ok=True)

        started = time.time()
        error = None
        raw_text = ""
        candidate_code = ""
        ewcs = None
        decision = None
        code_output = None

        gen_max_tokens = effective_max_tokens(system_prompt, instruction, args.max_tokens, args.context_limit)
        if gen_max_tokens <= 0:
            error = (f"prompt alone (~{estimate_tokens(system_prompt) + estimate_tokens(instruction)} "
                      f"estimated tokens) leaves no room under --context-limit {args.context_limit}")
            print(f"    ERROR: {error}", file=sys.stderr)
        else:
            try:
                response_json = chat_completion(args.api_base, args.model, system_prompt, instruction,
                                                 temperature=args.temperature, max_tokens=gen_max_tokens)
                raw_text = extract_message_text(response_json)
                candidate_code = extract_code(raw_text)
                (task_dir / "raw_response.json").write_text(json.dumps(response_json, indent=2), encoding="utf-8")
            except Exception as e:  # noqa: BLE001
                error = f"generation failed: {e}"
                print(f"    ERROR: {error}", file=sys.stderr)

        (task_dir / "candidate.py").write_text(candidate_code, encoding="utf-8")
        (task_dir / "response.md").write_text(raw_text, encoding="utf-8")

        if not error:
            candidate_path = task_dir / "candidate.py"
            verify_out = task_dir / "verification"
            try:
                verifier_result = run_verifier(
                    args.toolbox, candidate_path, instruction, verify_out,
                    args.api_base, args.model, enable_correction=not args.no_correction,
                )
                (task_dir / "verifier_stdout.txt").write_text(verifier_result["stdout"], encoding="utf-8")
                if verifier_result["stderr"]:
                    (task_dir / "verifier_stderr.txt").write_text(verifier_result["stderr"], encoding="utf-8")
                audit = verifier_result["audit"]
                if audit is None:
                    error = f"verifier produced no audit.json (exit code {verifier_result['returncode']})"
                else:
                    decision = audit.get("decision")
                    code_output = audit.get("delivered_code")
                    attempts = audit.get("attempts") or []
                    if attempts:
                        ewcs = attempts[-1].get("verification", {}).get("ewcs_report", {}).get("ewcs")
                    # Convenience copies alongside the raw verifier output.
                    if audit.get("report") is not None:
                        (task_dir / "report.md").write_text(audit["report"], encoding="utf-8")
                    if code_output:
                        (task_dir / "delivered.py").write_text(code_output, encoding="utf-8")
            except Exception as e:  # noqa: BLE001
                error = f"verification failed: {e}"
                print(f"    ERROR: {error}", file=sys.stderr)

        meta = {
            "task_id": task_id,
            "mode": "intervention",
            "model": args.model,
            "model_label": model_label,
            "api_base": args.api_base,
            "context_limit": args.context_limit,
            "requested_max_tokens": args.max_tokens,
            "effective_max_tokens": gen_max_tokens,
            "instruction": instruction,
            "started": started,
            "duration_seconds": round(time.time() - started, 3),
            "decision": decision,
            "ewcs": ewcs,
            "error": error,
        }
        (task_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

        append_jsonl(jsonl_path, {
            "prompt_id": task_id,
            "model": args.model,
            "model_label": model_label,
            "code_output": code_output,
            "ewcs": ewcs,
            "decision": decision,
            "error": error,
        })


# --------------------------------------------------------------------------
# Shared helpers
# --------------------------------------------------------------------------
def append_jsonl(path: Path, record: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Confident Agent Benchmark Runner")
    p.add_argument("--mode", choices=["baseline", "intervention", "both"], required=True)
    p.add_argument("--model", required=True, help="Exact model identifier as loaded in LM Studio")
    p.add_argument("--model-label", default=None,
                    help="Human-readable name/parameters for this run, e.g. 'Qwen2.5-9B-Q8'. "
                         "Used as the results subfolder name under Baseline_Tests/Intervention_Tests. "
                         "Defaults to --model, sanitized for the filesystem.")
    p.add_argument("--api-base", default="http://127.0.0.1:1234/v1", help="LM Studio OpenAI-compatible base URL")
    p.add_argument("--context-limit", type=int, default=30000,
                    help="Token budget the model was loaded with in LM Studio (context length). "
                         "The benchmark estimates prompt size and shrinks --max-tokens to fit under "
                         "this cap rather than risk overflow; it does not itself change the model's "
                         "loaded context length (see README for 'lms load --context-length').")
    p.add_argument("--dataset", type=Path, default=DATASET_DEFAULT)
    p.add_argument("--toolbox", type=Path, default=TOOLBOX_DEFAULT,
                    help="Path to the confident-agent-toolbox project (needs npm install once)")
    p.add_argument("--baseline-prompt", type=Path, default=BASELINE_PROMPT_DEFAULT)
    p.add_argument("--intervention-prompt", type=Path, default=INTERVENTION_PROMPT_DEFAULT)
    p.add_argument("--baseline-dir", type=Path, default=BASELINE_TESTS_DIR_DEFAULT)
    p.add_argument("--intervention-dir", type=Path, default=INTERVENTION_TESTS_DIR_DEFAULT)
    p.add_argument("--baseline-jsonl", type=Path, default=BASELINE_JSONL_DEFAULT)
    p.add_argument("--intervention-jsonl", type=Path, default=INTERVENTION_JSONL_DEFAULT)
    p.add_argument("--temperature", type=float, default=0.2)
    p.add_argument("--max-tokens", type=int, default=2048)
    p.add_argument("--no-correction", action="store_true",
                    help="Disable the verifier's one-shot model-side correction for contradicted candidates")
    p.add_argument("--limit", type=int, default=None, help="Only run the first N tasks (for smoke-testing)")
    return p


def main():
    args = build_arg_parser().parse_args()
    tasks = load_dataset(args.dataset)
    if args.limit:
        tasks = tasks[: args.limit]

    if args.mode in ("baseline", "both"):
        run_baseline(tasks, args)
    if args.mode in ("intervention", "both"):
        run_intervention(tasks, args)

    print("Done.")


if __name__ == "__main__":
    main()
