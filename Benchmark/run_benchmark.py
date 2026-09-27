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

Every task also records its timing (model time, tool time), token counts and, where
the machine allows it, the energy used (GPU; CPU with LibreHardwareMonitor; see
power_monitor.py). Each run folder gets a run_summary.json.

The benchmark never interprets the task for the model and never executes generated
code: the tool analyses candidates statically. Every file, folder and JSONL line is
written by this script, not by the model.

Usage
-----
    python run_benchmark.py --mode both --model qwen/qwen3.5-9b --model-label "Qwen3.5-9B-Q4_K_M"

Runs resume: a task whose folder already has result.json is skipped (use
--overwrite to redo it). See README.md and --help.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import re
import shutil
import statistics
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from power_monitor import LHM_URL_DEFAULT, PowerMonitor, power_check

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
TOOLBOX_DEFAULT = REPO / "confident-agent-toolbox"
DATASET_DEFAULT = ROOT / "dataset" / "rest_api_prompts_pilot.jsonl"
BASELINE_PROMPT_DEFAULT = ROOT / "instructions" / "Baseline" / "BASELINE_SYSTEM_PROMPT.md"
INTERVENTION_PROMPT_DEFAULT = TOOLBOX_DEFAULT / "instructions" / "CONFIDENCE_AGENT_PROMPT.md"
PACKAGE_EVIDENCE_DEFAULT = TOOLBOX_DEFAULT / "examples" / "evidence" / "requests-pypi-pilot.json"
BRIDGE = ROOT / "tool_bridge.cjs"
MODE_DIRS = {"baseline": ROOT / "Baseline_Tests", "intervention": ROOT / "Intervention_Tests"}
MODE_JSONL = {"baseline": ROOT / "complete_test_baseline.jsonl", "intervention": ROOT / "complete_test_intervention.jsonl"}

CODE_FENCE_RE = re.compile(r"```(?:python|py)?[ \t]*\n(.*?)```", re.DOTALL)
THINK_RE = re.compile(r"^\s*<think>.*?</think>\s*", re.DOTALL)
LABEL_SAFE_RE = re.compile(r"[^A-Za-z0-9._-]+")
DELIVERED = ("deliver", "deliver_with_flag")
# Part of every run's settings: results produced by a different harness behaviour are
# never mixed under one model label.
#   2026-09-26.2  run 1
#   2026-09-27.1  tool-bridge retries and failures kept apart from verifications, exact
#                 (LF) candidate files, frozen package evidence, timing, tokens, GPU energy
#   2026-09-27.2  energy via LibreHardwareMonitor (AMD GPUs, CPU package) as well as nvidia-smi
BENCHMARK_VERSION = "2026-09-27.2"
# Sent once, with tool calls disabled, when the model reaches --max-turns without replying.
FINAL_REPLY_REQUEST = ("Verification for this task is finished; no more tool calls are available. Reply now with "
                       "the report field of your last verify_candidate result, exactly as returned.")
FINAL_REPLY_REQUEST_UNVERIFIED = "No more tool calls are available for this task. Reply now with your final answer."


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------
def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(data: str | bytes) -> str:
    return hashlib.sha256(data.encode("utf-8") if isinstance(data, str) else data).hexdigest()


def content_sha256(path: Path) -> str:
    """Hash of a text file with line endings normalized, so the same dataset or evidence
    file gets the same fingerprint on a Windows (CRLF) and a Linux (LF) checkout."""
    return sha256(path.read_bytes().replace(b"\r\n", b"\n"))


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


def save_text(path: Path, text: str) -> None:
    """Written byte for byte (no newline translation), so a saved candidate hashes to the
    candidate_hash the tool reported."""
    with path.open("w", encoding="utf-8", newline="") as f:
        f.write(text)


def write_json(path: Path, data) -> None:
    save_text(path, json.dumps(data, indent=2, ensure_ascii=False))


def rounded(x, digits=3):
    return round(x, digits) if isinstance(x, (int, float)) else x


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


def usage_totals(usages: list) -> dict:
    """Token counts summed over the model requests of one task."""
    total = {"requests": 0, "prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "reasoning_tokens": 0}
    for u in usages:
        if not u:
            continue
        total["requests"] += 1
        for k in ("prompt_tokens", "completion_tokens", "total_tokens"):
            total[k] += u.get(k) or 0
        total["reasoning_tokens"] += (u.get("completion_tokens_details") or {}).get("reasoning_tokens") or 0
    return total


# --------------------------------------------------------------------------
# Machine description and GPU power
# --------------------------------------------------------------------------
def cpu_name() -> str:
    try:
        if sys.platform == "win32":
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") as key:
                return winreg.QueryValueEx(key, "ProcessorNameString")[0].strip()
        if Path("/proc/cpuinfo").exists():
            for line in Path("/proc/cpuinfo").read_text().splitlines():
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
        if sys.platform == "darwin":
            return subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return platform.processor() or "unknown"


def ram_gb() -> float | None:
    try:
        if sys.platform == "win32":
            import ctypes

            class MemoryStatus(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
            status = MemoryStatus()
            status.dwLength = ctypes.sizeof(MemoryStatus)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))
            return round(status.ullTotalPhys / 1024 ** 3, 1)
        if Path("/proc/meminfo").exists():
            kb = int(Path("/proc/meminfo").read_text().split("MemTotal:")[1].split()[0])
            return round(kb / 1024 ** 2, 1)
    except (OSError, ValueError, AttributeError, IndexError):
        pass
    return None


def tool_version(cmd: list) -> str | None:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=10).stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def environment(args, power: PowerMonitor) -> dict:
    return {"os": platform.platform(), "machine": platform.machine(), "cpu": cpu_name(), "logical_cpus": os.cpu_count(),
            "ram_gb": ram_gb(), "python": platform.python_version(), "node": tool_version(["node", "--version"]),
            "gpus": power.gpus}


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
    except TimeoutError as e:
        # A read timeout surfaces as TimeoutError, not URLError (it stopped a smoke test).
        raise LMStudioError(f"No response from {url} within {timeout} s") from e
    except (OSError, ValueError) as e:  # dropped connection, malformed JSON
        raise LMStudioError(f"Request to {url} failed: {e}") from e


def chat(args, messages: list, max_tokens: int, tools: list | None = None, tool_choice: str | None = None) -> tuple:
    """One model request. Returns the response and the wall-clock seconds it took."""
    payload = {"model": args.model, "messages": messages, "temperature": args.temperature,
               "max_tokens": max_tokens, "stream": False}
    if args.seed is not None:
        payload["seed"] = args.seed
    if args.thinking == "off":
        payload["reasoning_effort"] = "none"  # the switch LM Studio honours for Qwen3.5 thinking
    if tools:
        payload["tools"] = tools
        if tool_choice:
            payload["tool_choice"] = tool_choice
    started = time.monotonic()
    response = http_json(args.api_base.rstrip("/") + "/chat/completions", payload, args.request_timeout)
    return response, time.monotonic() - started


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
    print(f"[setup] Model {args.model}: quantization {info.get('quantization', '?')}, "
          f"architecture {info.get('arch', '?')}, context {args.context_limit}.", flush=True)
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
    """Build the toolbox when dist/ is missing or older than its sources. dist/ is not in
    git, so after a pull the old build would otherwise verify with the old verifier."""
    built = toolbox / "dist" / "confidenceAgentTools.js"
    sources = [p for p in (toolbox / "src").rglob("*") if p.suffix in (".ts", ".py")]
    if built.exists() and all(p.stat().st_mtime <= built.stat().st_mtime for p in sources):
        return
    npm = shutil.which("npm")  # resolves npm.cmd on Windows
    if not npm:
        sys.exit("The toolbox build is missing or out of date and npm was not found. Run `npm ci && npm run build` in "
                 + str(toolbox))
    print("[setup] The toolbox build is missing or older than its sources: running npm run build ...", flush=True)
    if not (toolbox / "node_modules").exists():
        subprocess.run([npm, "ci", "--no-audit", "--no-fund"], cwd=str(toolbox), check=True)
    subprocess.run([npm, "run", "build"], cwd=str(toolbox), check=True)


def bridge(args, request: dict | None = None, describe: bool = False) -> tuple:
    """One tool call through tool_bridge.cjs. A crashed bridge process (for example exit
    0xC0000409 on Windows, seen three times in run 1) is retried; a timeout is not.
    Returns the tool result and how the call went."""
    cmd = ["node", str(BRIDGE), str(args.toolbox)]
    if args.package_evidence:
        cmd += ["--package-evidence", str(args.package_evidence)]
    if describe:
        cmd.append("--describe")
    env = {**os.environ, "CONFIDENCE_PYTHON": args.python}
    started, failures, result, attempts = time.monotonic(), [], None, 0
    for _ in range(args.tool_retries + 1):
        attempts += 1
        try:
            out = subprocess.run(cmd, input=json.dumps(request or {}), capture_output=True, text=True,
                                 encoding="utf-8", timeout=args.tool_timeout, env=env)
        except subprocess.TimeoutExpired:
            result = {"error": f"verify_candidate timed out after {args.tool_timeout} s."}
            failures.append("timeout")
            break
        try:
            result = json.loads(out.stdout)
            break
        except json.JSONDecodeError:
            result = {"error": f"Tool bridge failed (exit {out.returncode}): {(out.stderr or out.stdout)[-500:]}"}
            failures.append(f"exit {out.returncode}")
    return result, {"seconds": round(time.monotonic() - started, 3), "attempts": attempts, "failures": failures}


def verify_tool_schema(args) -> list:
    described, _ = bridge(args, describe=True)
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
    fp = {"benchmark_version": BENCHMARK_VERSION, "mode": mode, "model": args.model, "system_prompt_sha256": sha256(prompt),
          "temperature": args.temperature, "max_tokens": args.max_tokens, "thinking": args.thinking, "seed": args.seed}
    if mode == "intervention":
        fp["max_turns"] = args.max_turns
        fp["package_evidence_sha256"] = content_sha256(args.package_evidence) if args.package_evidence else None
    return fp


def open_run(mode: str, args, prompt: str, info: dict, power: PowerMonitor) -> Path:
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
    save_text(run_dir / "system_prompt.md", prompt)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {"invocations": []}
    manifest.update({"settings": fingerprint, "model_label": run_dir.name, "api_base": args.api_base,
                     "lmstudio_model_info": info, "context_limit": args.context_limit,
                     "request_timeout_seconds": args.request_timeout})
    if mode == "intervention":
        manifest.update({"toolbox": str(args.toolbox), "verification_python": args.python,
                         "toolbox_prompt_source": str(args.intervention_prompt),
                         "package_evidence": str(args.package_evidence) if args.package_evidence else None,
                         "tool_retries": args.tool_retries})
    manifest["invocations"].append({"started": now(), "git_commit": git_commit(), "dataset": str(args.dataset),
                                    "dataset_sha256": content_sha256(args.dataset), "argv": sys.argv[1:],
                                    "environment": environment(args, power), "power": power.describe()})
    write_json(manifest_path, manifest)
    return run_dir


def rebuild_jsonl(mode: str) -> None:
    """Rebuild the JSONL indexes from the result.json files on disk, so an interrupted or
    resumed run never leaves duplicate or missing lines.

    Each model label's folder gets its own results.jsonl (it travels with the folder when
    a run is archived). The shared file at the Benchmark root holds every label: labels
    with a folder on disk are rebuilt from it, and rows of labels whose folder is no
    longer on disk (for example a run archived as a zip) are kept as they were."""
    on_disk: dict = {}
    for result in sorted(MODE_DIRS[mode].glob("*/*/result.json")):
        on_disk.setdefault(result.parent.parent.name, []).append(json.loads(result.read_text(encoding="utf-8"))["jsonl"])
    lines = lambda rows: "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    for label, rows in on_disk.items():
        save_text(MODE_DIRS[mode] / label / "results.jsonl", lines(rows))
    kept = []
    if MODE_JSONL[mode].exists():
        for line in MODE_JSONL[mode].read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                if sanitize_label(row.get("model_label") or "") not in on_disk:
                    kept.append(row)
    save_text(MODE_JSONL[mode], lines(kept + [r for label in sorted(on_disk) for r in on_disk[label]]))


def distribution(values) -> dict | None:
    v = sorted(x for x in values if isinstance(x, (int, float)))
    if not v:
        return None
    return {"n": len(v), "total": round(sum(v), 3), "mean": round(statistics.mean(v), 3),
            "median": round(statistics.median(v), 3), "p95": round(v[max(0, math.ceil(0.95 * len(v)) - 1)], 3),  # nearest rank
            "min": round(v[0], 3), "max": round(v[-1], 3)}


def write_run_summary(mode: str, run_dir: Path) -> dict:
    """Run-level statistics, rebuilt from every result.json in the folder."""
    records = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(run_dir.glob("*/result.json"))]
    metas, rows = [r["meta"] for r in records], [r["jsonl"] for r in records]
    count = lambda values: dict(sorted(((str(k), values.count(k)) for k in set(values)), key=lambda kv: -kv[1]))
    summary = {
        "benchmark_version": BENCHMARK_VERSION, "mode": mode, "model_label": run_dir.name, "tasks": len(records),
        "errors": count([m.get("error") for m in metas if m.get("error")]),
        "seconds_per_task": distribution(m.get("duration_seconds") for m in metas),
        "model_seconds_per_task": distribution((m.get("timing") or {}).get("model_seconds") for m in metas),
        "prompt_tokens_per_task": distribution((m.get("tokens") or {}).get("prompt_tokens") for m in metas),
        "completion_tokens_per_task": distribution((m.get("tokens") or {}).get("completion_tokens") for m in metas),
        "model_requests_per_task": distribution((m.get("tokens") or {}).get("requests") for m in metas),
        "gpu_energy_j_per_task": distribution((m.get("power") or {}).get("gpu_energy_j") for m in metas),
        "cpu_energy_j_per_task": distribution((m.get("power") or {}).get("cpu_energy_j") for m in metas),
        "measured_energy_j_per_task": distribution((m.get("power") or {}).get("measured_energy_j") for m in metas),
        "measured_energy_above_idle_j_per_task": distribution((m.get("power") or {}).get("measured_energy_above_idle_j") for m in metas),
        "gpu_mean_w_per_task": distribution((m.get("power") or {}).get("gpu_mean_w") for m in metas),
        "cpu_mean_w_per_task": distribution((m.get("power") or {}).get("cpu_mean_w") for m in metas),
    }
    if mode == "baseline":
        summary["with_code_block"] = sum(1 for r in rows if r.get("has_code_block"))
        summary["finish_reasons"] = count([r.get("finish_reason") for r in rows])
    else:
        summary.update({
            "decisions": count([r.get("decision") for r in rows]),
            "tool_seconds_per_task": distribution((m.get("timing") or {}).get("tool_seconds") for m in metas),
            "verification_calls": count([r.get("verification_calls") for r in rows]),
            "tool_failures": sum(r.get("tool_failures") or 0 for r in rows),
            "first_had_contradiction": sum(1 for r in rows if r.get("first_has_contradiction")),
            "correction_attempted": sum(1 for r in rows if r.get("correction_attempted")),
            "correction_attempted_when_allowed": sum(1 for r in rows if r.get("correction_attempted") and r.get("correction_allowed")),
            "final_reply_prompted": sum(1 for r in rows if r.get("final_reply_prompted")),
            "reply_matches_report": sum(1 for m in metas if (m.get("final_reply") or {}).get("matches_report")),
            "protocol_notes": count([n for r in rows for n in r.get("protocol_notes") or []]),
        })
    write_json(run_dir / "run_summary.json", summary)
    return summary


def run_mode(mode: str, tasks: list, args, info: dict, power: PowerMonitor) -> None:
    prompt = (args.baseline_prompt.read_text(encoding="utf-8") if mode == "baseline"
              else load_intervention_prompt(args.intervention_prompt))
    tools = verify_tool_schema(args) if mode == "intervention" else None
    run_dir = open_run(mode, args, prompt, info, power)
    harness_errors = []
    for n, task in enumerate(tasks, 1):
        task_dir = run_dir / task["task_id"]
        if (task_dir / "result.json").exists() and not args.overwrite:
            print(f"[{mode}] {n}/{len(tasks)} {task['task_id']}: done earlier, skipped", flush=True)
            continue
        if task_dir.exists():
            shutil.rmtree(task_dir)  # a partial folder from an interrupted task
        task_dir.mkdir(parents=True)
        started_at, t0 = now(), time.monotonic()
        try:
            record = (run_baseline_task if mode == "baseline" else run_intervention_task)(task, prompt, tools, task_dir, args)
        except Exception as e:  # noqa: BLE001 - one broken task must not end a long run
            # No result.json is written, so the task is retried when the run is resumed.
            harness_errors.append(task["task_id"])
            save_text(task_dir / "harness_error.txt", f"{now()} {type(e).__name__}: {e}\n")
            print(f"[{mode}] {n}/{len(tasks)} {task['task_id']}: HARNESS ERROR {type(e).__name__}: {e} "
                  "(no result written; rerun the same command to retry)", flush=True)
            continue
        t1 = time.monotonic()
        duration = t1 - t0
        timing = record["meta"].setdefault("timing", {})
        timing["other_seconds"] = rounded(duration - (timing.get("model_seconds") or 0) - (timing.get("tool_seconds") or 0))
        energy = power.energy(t0, t1)
        record["meta"].update({"task_id": task["task_id"], "mode": mode, "model": args.model, "model_label": run_dir.name,
                               "dataset": str(args.dataset), "instruction": task["natural_language_instruction"],
                               "started": started_at, "finished": now(), "duration_seconds": round(duration, 3),
                               "power": energy})
        tokens = record["meta"].get("tokens") or {}
        record["jsonl"] = {"prompt_id": task["task_id"], "model": args.model, "model_label": run_dir.name, **record["jsonl"],
                           "duration_seconds": round(duration, 3), "model_seconds": timing.get("model_seconds"),
                           "tool_seconds": timing.get("tool_seconds"), "prompt_tokens": tokens.get("prompt_tokens"),
                           "completion_tokens": tokens.get("completion_tokens"),
                           "gpu_energy_j": energy.get("gpu_energy_j"), "cpu_energy_j": energy.get("cpu_energy_j"),
                           "measured_energy_j": energy.get("measured_energy_j"),
                           "measured_energy_above_idle_j": energy.get("measured_energy_above_idle_j")}
        write_json(task_dir / "result.json", record)
        rebuild_jsonl(mode)
        watts = f", {energy['measured_energy_j']} J" if energy.get("measured") else ""
        print(f"[{mode}] {n}/{len(tasks)} {task['task_id']}: {record['summary']} ({round(duration, 3)} s{watts})", flush=True)
    summary = write_run_summary(mode, run_dir)
    print(f"[{mode}] summary: {run_dir / 'run_summary.json'} ({summary['tasks']} tasks)", flush=True)
    if harness_errors:
        print(f"[{mode}] {len(harness_errors)} task(s) have no result because of a harness error: "
              f"{', '.join(harness_errors)}. Run the same command again to retry them.", flush=True)


def run_baseline_task(task: dict, prompt: str, tools, task_dir: Path, args) -> dict:
    messages = [{"role": "system", "content": prompt}, {"role": "user", "content": task["natural_language_instruction"]}]
    error, text, code, response, seconds = None, "", None, None, None
    max_tokens = budget(messages, args)
    if max_tokens <= 0:
        error = f"prompt exceeds the {args.context_limit}-token context"
    else:
        try:
            response, seconds = chat(args, messages, max_tokens)
            text = response["choices"][0]["message"].get("content") or ""
            code = extract_code(text)
            write_json(task_dir / "raw_response.json", response)
        except (LMStudioError, KeyError, IndexError, TypeError) as e:
            error = str(e)
    finish = response["choices"][0].get("finish_reason") if response else None
    save_text(task_dir / "response.md", text)
    save_text(task_dir / "solution.py", code or "")
    tokens = usage_totals([response.get("usage")] if response else [])
    tokens["completion_tokens_per_second"] = rounded(tokens["completion_tokens"] / seconds) if seconds else None
    return {"meta": {"finish_reason": finish, "usage": response.get("usage") if response else None, "tokens": tokens,
                     "timing": {"model_seconds": rounded(seconds)}, "error": error},
            "jsonl": {"code": code, "has_code_block": code is not None, "finish_reason": finish, "error": error},
            "summary": error or ("code" if code is not None else "no code block") + (f", {finish}" if finish != "stop" else "")}


def run_intervention_task(task: dict, prompt: str, tools, task_dir: Path, args) -> dict:
    messages = [{"role": "system", "content": prompt}, {"role": "user", "content": task["natural_language_instruction"]}]
    turns, verifications, failures, other_tools = [], [], [], []
    error, reply, finish, prompted, model_seconds, tool_seconds = None, None, None, False, 0.0, 0.0
    turns_dir = task_dir / "turns"
    turns_dir.mkdir()
    for turn in range(1, args.max_turns + 1):
        max_tokens = budget(messages, args)
        if max_tokens <= 0:
            error = f"conversation exceeds the {args.context_limit}-token context"
            break
        try:
            response, seconds = chat(args, messages, max_tokens, tools)
            message = response["choices"][0]["message"]
            finish = response["choices"][0].get("finish_reason")
        except (LMStudioError, KeyError, IndexError, TypeError) as e:
            error = f"model request failed: {e}"
            break
        model_seconds += seconds
        write_json(turns_dir / f"turn_{turn:02d}_response.json", response)
        calls = message.get("tool_calls") or []
        messages.append({"role": "assistant", "content": message.get("content") or "", **({"tool_calls": calls} if calls else {})})
        turns.append({"turn": turn, "finish_reason": finish, "usage": response.get("usage"), "model_seconds": round(seconds, 3),
                      "tool_calls": [c.get("function", {}).get("name") for c in calls]})
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
                result, call_info = bridge(args, {"name": "verify_candidate", "arguments": arguments})
                tool_seconds += call_info["seconds"]
                code = arguments["code"]
                if "decision" not in result:
                    # The tool did not run (bridge crash or timeout after retries). This is not a
                    # verification: the decision stays with the last successful one.
                    index = len(failures) + 1
                    save_text(task_dir / f"failed_candidate_{index}.py", code)
                    write_json(task_dir / f"tool_failure_{index}.json", {**result, "call": call_info})
                    failures.append({"index": index, "turn": turn, "code_sha256": sha256(code), "error": result.get("error"), **call_info})
                else:
                    index = len(verifications) + 1
                    save_text(task_dir / f"verified_candidate_{index}.py", code)
                    write_json(task_dir / f"verification_{index}.json", result)
                    layers = result.get("layers") or []
                    verifications.append({
                        "index": index, "turn": turn, "code": code, "code_sha256": sha256(code),
                        "candidate_hash_matches": result.get("candidate_hash") == sha256(code),
                        "decision": result.get("decision"), "ewcs": (result.get("ewcs_report") or {}).get("ewcs"),
                        "layers": {l.get("layer"): l.get("state") for l in layers},
                        "has_contradiction": any(l.get("state") == "verified_incorrect" for l in layers),
                        "evidence_selection": result.get("evidence_selection"), "report": result.get("report"),
                        "extra_arguments": sorted(k for k in arguments if k != "code"),
                        "tool_seconds": call_info["seconds"], "bridge_attempts": call_info["attempts"],
                        "bridge_failures": call_info["failures"]})
            messages.append({"role": "tool", "tool_call_id": call.get("id", ""), "content": json.dumps(result, ensure_ascii=False)})
    else:
        # The model used every turn without replying (typically re-verifying after a final
        # abstain). Its attempts stay on record; it is then asked once, with tool calls
        # disabled, for the report, so every task ends with a reply the evaluation can read.
        prompted = True
        messages.append({"role": "user", "content": FINAL_REPLY_REQUEST if verifications else FINAL_REPLY_REQUEST_UNVERIFIED})
        max_tokens = budget(messages, args)
        if max_tokens <= 0:
            error = f"turn limit reached and no room left in the {args.context_limit}-token context for a final reply"
        else:
            try:
                response, seconds = chat(args, messages, max_tokens, tools, tool_choice="none")
                model_seconds += seconds
                message = response["choices"][0]["message"]
                finish = response["choices"][0].get("finish_reason")
                write_json(turns_dir / f"turn_{args.max_turns + 1:02d}_response.json", response)
                ignored = bool(message.get("tool_calls"))
                messages.append({"role": "assistant", "content": message.get("content") or "", **({"tool_calls": message["tool_calls"]} if ignored else {})})
                turns.append({"turn": args.max_turns + 1, "finish_reason": finish, "usage": response.get("usage"),
                              "model_seconds": round(seconds, 3), "final_reply_request": True,
                              "tool_calls": [c.get("function", {}).get("name") for c in message.get("tool_calls") or []]})
                if ignored:
                    error = "turn limit reached; the model answered the final-reply request with another tool call"
                else:
                    reply = strip_think(message.get("content") or "")
            except (LMStudioError, KeyError, IndexError, TypeError) as e:
                error = f"final-reply request failed: {e}"
    write_json(task_dir / "conversation.json", messages)
    save_text(task_dir / "response.md", reply or "")
    record = intervention_record(verifications, failures, other_tools, turns, reply, finish, error, prompted)
    tokens = usage_totals([t.get("usage") for t in turns])
    tokens["completion_tokens_per_second"] = rounded(tokens["completion_tokens"] / model_seconds) if model_seconds else None
    record["meta"].update({"tokens": tokens, "timing": {"model_seconds": rounded(model_seconds), "tool_seconds": rounded(tool_seconds)}})
    return record


def intervention_record(verifications, failures, other_tools, turns, reply, finish, error, prompted=False) -> dict:
    """What the model did, and what the tool decided. Only the tool's decisions count as
    decisions; the model's compliance with the prompt is recorded, not enforced.
    `verifications` holds successful tool runs only; `failures` holds tool calls that
    could not be run."""
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
    if prompted:
        notes.append("reached the turn limit; the benchmark asked for the final reply")
    if not verifications:
        notes.append("never called verify_candidate" if not failures else "no successful verification (tool failures)")
    if failures:
        notes.append(f"tool failed {len(failures)} time(s) after retries")
    if attempted and not allowed:
        notes.append("corrected without a verified_incorrect layer")
    if changes > 1:
        notes.append("more than one correction")
    if allowed and not attempted and not prompted:
        notes.append("replied without correcting after a verified_incorrect layer")
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
    summary = (error or f"{decision or 'no successful verification'}; {len(verifications)} verification(s)"
               + (f"; {len(failures)} tool failure(s)" if failures else "")
               + ("; correction attempted" if attempted else "") + ("; final reply requested" if prompted else "")
               + (f"; {len(notes)} protocol note(s)" if notes else ""))
    return {
        "meta": {"turns": turns, "verifications": [{k: v for k, v in x.items() if k != "code"} for x in verifications],
                 "tool_failures": failures, "correction": correction, "protocol_notes": notes, "final_finish_reason": finish,
                 "final_reply": {"present": reply is not None, "prompted_by_benchmark": prompted,
                                 "matches_report": bool(reply is not None and final and final.get("report")
                                                        and reply.strip() == final["report"].strip())},
                 "error": error},
        "jsonl": {"decision": decision, "ewcs": final["ewcs"] if final else None, "code_output": delivered,
                  "first_candidate": first["code"] if first else None, "final_candidate": final["code"] if final else None,
                  "reply_code": reply_code, "final_reply_present": reply is not None, "final_reply_prompted": prompted,
                  "verification_calls": len(verifications), "tool_failures": len(failures),
                  "model_turns": len(turns),
                  "correction_attempted": attempted, "correction_allowed": allowed, "correction_count": changes,
                  "first_decision": correction["first_decision"], "first_has_contradiction": allowed,
                  "first_ewcs": first["ewcs"] if first else None,
                  "protocol_notes": notes, "error": error},
        "summary": summary}


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------
def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Confident Agent Benchmark Runner (produces results only)")
    p.add_argument("--mode", choices=["baseline", "intervention", "both"])
    p.add_argument("--model", help="Model identifier exactly as LM Studio serves it (lms ps)")
    p.add_argument("--model-label", default=None, help="Results folder name for this model/quantization, e.g. 'Qwen3.5-9B-Q4_K_M'")
    p.add_argument("--api-base", default="http://127.0.0.1:1234/v1")
    p.add_argument("--dataset", type=Path, default=DATASET_DEFAULT)
    p.add_argument("--tasks", default=None, help="Comma-separated task ids to run (default: all)")
    p.add_argument("--limit", type=int, default=None, help="Only the first N tasks (smoke test)")
    p.add_argument("--toolbox", type=Path, default=TOOLBOX_DEFAULT, help="confident-agent-toolbox folder (default: the repo's)")
    p.add_argument("--baseline-prompt", type=Path, default=BASELINE_PROMPT_DEFAULT)
    p.add_argument("--intervention-prompt", type=Path, default=INTERVENTION_PROMPT_DEFAULT)
    p.add_argument("--package-evidence", type=Path, default=PACKAGE_EVIDENCE_DEFAULT,
                   help="Frozen PyPI metadata for the interface layer (imports not in it are looked up live)")
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
    p.add_argument("--tool-retries", type=int, default=2, help="Retries when the tool bridge process crashes")
    p.add_argument("--power", choices=["auto", "nvidia", "lhm", "none"], default="auto",
                   help="energy per task: nvidia-smi, or LibreHardwareMonitor's web server (AMD GPUs, CPU package); "
                        "auto uses whichever is available")
    p.add_argument("--power-interval-ms", type=int, default=500, help="power sampling interval")
    p.add_argument("--lhm-url", default=LHM_URL_DEFAULT, help="LibreHardwareMonitor Remote Web Server data.json URL")
    p.add_argument("--lhm-gpu", default=None, help="part of the GPU's name to measure, e.g. '9070' (default: the GPU drawing most power)")
    p.add_argument("--lhm-gpu-sensor", default=None, help="exact LHM GPU power sensor name (default: best available)")
    p.add_argument("--power-check", action="store_true", help="show the power sensors that would be used, then exit")
    p.add_argument("--idle-seconds", type=float, default=10, help="Idle GPU power measured before the run (0 to skip)")
    p.add_argument("--overwrite", action="store_true", help="Redo tasks that already have results")
    return p


def main() -> None:
    # Windows consoles default to cp1252; a model reply or error text must not crash the run.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    parser = build_arg_parser()
    args = parser.parse_args()
    if args.power_check:
        monitor = PowerMonitor(args.power, args.power_interval_ms, args.lhm_url, args.lhm_gpu, args.lhm_gpu_sensor)
        try:
            power_check(monitor)
        finally:
            monitor.stop()
        return
    if not args.mode or not args.model:
        parser.error("--mode and --model are required (except with --power-check)")
    args.toolbox = args.toolbox.resolve()
    args.python = toolbox_python(args.toolbox)
    if args.package_evidence and not args.package_evidence.exists():
        sys.exit(f"Package evidence file not found: {args.package_evidence}")
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
    power = PowerMonitor(args.power, args.power_interval_ms, args.lhm_url, args.lhm_gpu, args.lhm_gpu_sensor)
    print(f"[setup] Power: {power.summary_line()}.", flush=True)
    try:
        power.measure_idle(args.idle_seconds)
        for mode in modes:
            run_mode(mode, tasks, args, info, power)
    finally:
        power.stop()
    print("Done.")


if __name__ == "__main__":
    main()
