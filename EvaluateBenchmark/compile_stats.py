#!/usr/bin/env python3
"""
Stats compiler
==============

Compiles every statistic of the project into CSV files, one row per prompt and run plus
grouped summaries. Standard library only.

Sources (nothing is re-run):
  - EvaluateBenchmark/results/<label>/per_task.jsonl   classes from evaluate_benchmark.py
  - Benchmark result.json files per task, read from the run folders or from the zipped
    archives (Benchmark/*.zip)                            time, tokens, energy, agent behaviour
  - Benchmark run_manifest.json per run                   model, quantization, settings, machine
  - the dataset's task file                               API, category, method, difficulty, auth

Output (EvaluateBenchmark/stats/, described column by column in STATS_README.md):
  prompt_stats.csv          one row per prompt and run: every label and measure
  group_stats.csv           per run and group (overall, API, category, method, difficulty,
                            authentication, specification source): rates, repairs and
                            regressions with McNemar, abstention, cost
  model_comparison.csv      one row per run (model / quantization): headline figures
  verifier_detection.csv    the verifier as a hallucination detector: precision, recall, F1
  error_kinds.csv           kinds of error reaching the user (A: API hallucination, B: task
                            fidelity, runtime failure), per run, mode and category

Usage:  python compile_stats.py            (after python evaluate_benchmark.py)
"""
from __future__ import annotations

import csv
import json
import re
import statistics
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

from evaluate_benchmark import TASKS_DEFAULT, hallucination_types, load_jsonl, runtime_failure_type, task_error_types
from evaluator.stats import holm, mcnemar_exact, wilson

ROOT = Path(__file__).resolve().parent
BENCHMARK = ROOT.parent / "Benchmark"
RESULTS = ROOT / "results"
OUT = ROOT / "stats"
MODES = {"baseline": "Baseline_Tests", "intervention": "Intervention_Tests"}
DIMENSIONS = ["overall", "api", "operation_category", "http_method", "difficulty", "auth_type", "spec_source"]


# ---------------------------------------------------------------- reading the benchmark
class BenchmarkFiles:
    """result.json and run_manifest.json from run folders, or from zipped archives."""

    def __init__(self, root: Path):
        self.root = root
        self.zipped: dict = {}
        for archive in sorted(root.glob("*.zip")):
            with zipfile.ZipFile(archive) as z:
                for name in z.namelist():
                    parts = name.replace("\\", "/").split("/")
                    if len(parts) >= 3 and parts[0] in MODES.values() and parts[-1] in ("result.json", "run_manifest.json"):
                        self.zipped[tuple(parts)] = (archive, name)

    def read(self, *parts: str) -> dict | None:
        path = self.root.joinpath(*parts)
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        hit = self.zipped.get(tuple(parts))
        if hit:
            with zipfile.ZipFile(hit[0]) as z:
                return json.loads(z.read(hit[1]).decode("utf-8"))
        return None

    def result(self, mode: str, label: str, task: str) -> dict | None:
        return self.read(MODES[mode], label, task, "result.json")

    def manifest(self, mode: str, label: str) -> dict:
        return self.read(MODES[mode], label, "run_manifest.json") or {}


# ---------------------------------------------------------------- per-prompt values
def num(x):
    return x if isinstance(x, (int, float)) and not isinstance(x, bool) else None


def tokens(meta: dict) -> dict:
    """Token counts: the benchmark's summed figures (run 2 on), else summed usage (run 1)."""
    if meta.get("tokens"):
        return meta["tokens"]
    usages = [meta.get("usage")] if meta.get("usage") else [t.get("usage") for t in meta.get("turns") or []]
    total = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "requests": 0}
    for u in usages:
        if u:
            total["requests"] += 1
            for k in ("prompt_tokens", "completion_tokens", "total_tokens"):
                total[k] += u.get(k) or 0
    return total if total["requests"] else {}


def cost_columns(prefix: str, result: dict | None) -> dict:
    meta = (result or {}).get("meta") or {}
    tok, timing, power = tokens(meta), meta.get("timing") or {}, meta.get("power") or {}
    duration, model_s = num(meta.get("duration_seconds")), num(timing.get("model_seconds"))
    completion = num(tok.get("completion_tokens"))
    return {f"{prefix}_duration_s": duration, f"{prefix}_model_s": model_s, f"{prefix}_tool_s": num(timing.get("tool_seconds")),
            f"{prefix}_model_requests": num(tok.get("requests")), f"{prefix}_prompt_tokens": num(tok.get("prompt_tokens")),
            f"{prefix}_completion_tokens": completion, f"{prefix}_total_tokens": num(tok.get("total_tokens")),
            f"{prefix}_completion_tokens_per_s": round(completion / (model_s or duration), 2) if completion and (model_s or duration) else None,
            f"{prefix}_gpu_energy_j": num(power.get("gpu_energy_j")), f"{prefix}_cpu_energy_j": num(power.get("cpu_energy_j")),
            f"{prefix}_energy_j": num(power.get("measured_energy_j")),
            f"{prefix}_energy_wh": round(power["measured_energy_j"] / 3600, 5) if num(power.get("measured_energy_j")) else None,
            f"{prefix}_energy_above_idle_j": num(power.get("measured_energy_above_idle_j")),
            f"{prefix}_energy_source": power.get("source") if power.get("measured") else None,
            f"{prefix}_started": meta.get("started"), f"{prefix}_error": meta.get("error")}


def hallucinated(cls: str | None):
    """1 = API hallucination (class A), 0 = decided otherwise, None = undetermined."""
    if cls in (None, "undetermined"):
        return None
    return int(cls == "A")


def correct(cls: str | None):
    if cls in (None, "undetermined"):
        return None
    return int(cls == "correct")


def pair(b, i) -> str | None:
    """Paired outcome of a 0/1 'bad' event (hallucination): repair = baseline bad, intervention not."""
    if b is None or i is None:
        return None
    return {(1, 1): "both", (1, 0): "repair", (0, 1): "regression", (0, 0): "neither"}[(b, i)]


def pair_good(b, i) -> str | None:
    """Paired outcome of a 0/1 'good' event (correct code reaches the user)."""
    if b is None or i is None:
        return None
    return {(1, 1): "both", (0, 1): "repair", (1, 0): "regression", (0, 0): "neither"}[(b, i)]


def prompt_row(label: str, task: dict, ev: dict, bres: dict | None, ires: dict | None, run_info: dict) -> dict:
    api, meta = task["api_specification"], task["metadata"]
    bmeta, imeta = (bres or {}).get("meta") or {}, (ires or {}).get("meta") or {}
    ijsonl = (ires or {}).get("jsonl") or {}
    b_cls, s_cls, f_cls = ev["baseline_class"], ev["shown_class"], ev["final_class"]
    shown = s_cls if s_cls != "nothing_shown" else None
    b_h, i_h = hallucinated(b_cls), (0 if s_cls == "nothing_shown" else hallucinated(s_cls))
    b_ok, i_ok = correct(b_cls), (0 if s_cls == "nothing_shown" else correct(s_cls))
    final_positive = hallucinated(f_cls)
    withheld = not ev["delivered"]
    verifier = None if final_positive is None else ("TP" if final_positive and withheld else "FN" if final_positive
                                                     else "FP" if withheld else "TN")
    bb, ib = ev.get("baseline_behaviour") or {}, ev.get("shown_behaviour") or {}
    row = {
        "model_label": label, "model": run_info.get("model"), "quantization": run_info.get("quantization"),
        "architecture": run_info.get("arch"), "context_length": run_info.get("context"), "thinking": run_info.get("thinking"),
        "temperature": run_info.get("temperature"), "benchmark_version": run_info.get("benchmark_version"),
        "machine_gpu": run_info.get("gpu"), "machine_cpu": run_info.get("cpu"),
        "task_id": task["task_id"], "api": api["api_name"], "operation_category": meta["category"],
        "http_method": api["method"], "endpoint": api["endpoint"], "difficulty": meta.get("difficulty"),
        "auth_type": (api.get("auth") or {}).get("type") or "none",
        "spec_source": "partial" if str(api.get("coverage", "")).lower().startswith("partial") else "official",
        "operation_family": meta.get("operation_family_id"), "pilot": int(ev["pilot"]),
        "instruction_chars": len(task["natural_language_instruction"]),
        # baseline
        "b_class": b_cls, "b_hallucination": b_h, "b_correct": b_ok,
        "b_hallucination_kinds": "|".join(sorted(hallucination_types(ev.get("baseline_a_reasons") or []))) if b_cls == "A" else "",
        "b_task_error_kinds": "|".join(sorted(task_error_types(ev.get("baseline_b_reasons") or []))) if b_cls == "B" else "",
        "b_runtime_failure_kind": runtime_failure_type(ev.get("baseline_reasons") or []) if b_cls == "runtime_failure" else "",
        "b_reasons": " | ".join(ev.get("baseline_reasons") or [])[:500],
        "b_has_code": int(b_cls != "no_code"), "b_finish_reason": ((bres or {}).get("jsonl") or {}).get("finish_reason"),
        "b_returns_expected": num(bb.get("returns_expected_value")) if bb else None,
        "b_empty_response_ok": num(bb.get("empty_response_ok")) if bb else None,
        "b_error_raises": num(bb.get("error_raises")) if bb else None,
        **cost_columns("b", bres),
        # intervention
        "i_decision": ev["decision"], "i_delivered": int(ev["delivered"]), "i_withheld": int(withheld),
        "i_ewcs": num(ev.get("ewcs")), "i_first_decision": ijsonl.get("first_decision"), "i_first_ewcs": num(ijsonl.get("first_ewcs")),
        "i_code_shown": int(ev["code_shown"]), "i_unapproved_code_shown": int(ev["shown_is_unapproved_reply"]),
        "i_shown_class": s_cls, "i_hallucination_reaches_user": i_h, "i_correct_reaches_user": i_ok,
        "i_hallucination_kinds": "|".join(sorted(hallucination_types(ev.get("shown_a_reasons") or []))) if shown == "A" else "",
        "i_task_error_kinds": "|".join(sorted(task_error_types(ev.get("shown_b_reasons") or []))) if shown == "B" else "",
        "i_runtime_failure_kind": runtime_failure_type(ev.get("shown_reasons") or []) if shown == "runtime_failure" else "",
        "i_shown_reasons": " | ".join(ev.get("shown_reasons") or [])[:500],
        "i_final_class": f_cls, "i_first_class": ev.get("first_class"),
        "i_verification_calls": num(ijsonl.get("verification_calls")), "i_tool_failures": num(ijsonl.get("tool_failures")),
        "i_model_turns": len(imeta.get("turns") or []) or num(ijsonl.get("model_turns")),
        "i_first_had_contradiction": num(ijsonl.get("first_has_contradiction")),
        "i_correction_attempted": num(ijsonl.get("correction_attempted")),
        "i_correction_allowed": num(ijsonl.get("correction_allowed")), "i_correction_count": num(ijsonl.get("correction_count")),
        "i_correction_outcome": f"{ev.get('first_class')}->{f_cls}" if ijsonl.get("correction_attempted") else "",
        "i_final_reply_prompted": num(ijsonl.get("final_reply_prompted")),
        "i_reply_matches_report": num((imeta.get("final_reply") or {}).get("matches_report")),
        "i_protocol_note_count": len(ev.get("protocol_notes") or []), "i_protocol_notes": " | ".join(ev.get("protocol_notes") or []),
        "i_returns_expected": num(ib.get("returns_expected_value")) if ib else None,
        "i_empty_response_ok": num(ib.get("empty_response_ok")) if ib else None,
        "i_error_raises": num(ib.get("error_raises")) if ib else None,
        **cost_columns("i", ires),
        # paired
        "pair_hallucination": pair(b_h, i_h), "pair_correct": pair_good(b_ok, i_ok), "verifier_outcome": verifier,
    }
    bd, idur = row["b_duration_s"], row["i_duration_s"]
    row["time_ratio"] = round(idur / bd, 2) if bd and idur else None
    row["extra_tokens"] = (row["i_total_tokens"] - row["b_total_tokens"]) if row["i_total_tokens"] is not None and row["b_total_tokens"] is not None else None
    row["energy_ratio"] = round(row["i_energy_j"] / row["b_energy_j"], 2) if row["b_energy_j"] and row["i_energy_j"] else None
    return row


# ---------------------------------------------------------------- summaries
def mean(values):
    v = [x for x in values if isinstance(x, (int, float))]
    return round(statistics.mean(v), 4) if v else None


def median(values):
    v = [x for x in values if isinstance(x, (int, float))]
    return round(statistics.median(v), 4) if v else None


def total(values):
    v = [x for x in values if isinstance(x, (int, float))]
    return round(sum(v), 3) if v else None


def rate(values):
    v = [x for x in values if x is not None]
    return (round(sum(v) / len(v), 4), len(v)) if v else (None, 0)


def group_summary(rows: list) -> dict:
    out = {"n": len(rows)}
    for name, key_b, key_i, pair_key in (("hallucination", "b_hallucination", "i_hallucination_reaches_user", "pair_hallucination"),
                                        ("correct", "b_correct", "i_correct_reaches_user", "pair_correct")):
        (bb, nb), (ii, ni) = rate(r[key_b] for r in rows), rate(r[key_i] for r in rows)
        pairs = Counter(r[pair_key] for r in rows if r[pair_key])
        out.update({f"b_{name}_rate": bb, f"i_{name}_rate": ii,
                    f"b_{name}_rate_ci": fmt_ci(wilson(round(bb * nb), nb)) if bb is not None else None,
                    f"i_{name}_rate_ci": fmt_ci(wilson(round(ii * ni), ni)) if ii is not None else None,
                    f"{name}_paired_n": sum(pairs.values()), f"{name}_repairs": pairs["repair"],
                    f"{name}_regressions": pairs["regression"], f"{name}_both": pairs["both"], f"{name}_neither": pairs["neither"],
                    # repairs minus regressions over paired tasks: positive = the intervention is better
                    f"{name}_improvement": round((pairs["repair"] - pairs["regression"]) / sum(pairs.values()), 4) if pairs else None,
                    f"{name}_mcnemar_p": mcnemar_exact(pairs["repair"], pairs["regression"]) if pairs else None})
    for cls in ("B", "runtime_failure", "undetermined"):
        out[f"b_{cls}_count"] = sum(r["b_class"] == cls for r in rows)
        out[f"i_{cls}_count"] = sum(r["i_shown_class"] == cls for r in rows)
    out.update({
        "i_abstention_rate": rate(r["i_withheld"] for r in rows)[0],
        "i_incorrect_acceptance": sum(r["i_hallucination_reaches_user"] == 1 for r in rows),
        "i_incorrect_rejection": sum(r["i_withheld"] == 1 and r["i_final_class"] == "correct" for r in rows),
        "i_unapproved_code_shown": sum(r["i_unapproved_code_shown"] for r in rows),
        "i_mean_ewcs": mean(r["i_ewcs"] for r in rows),
        "i_mean_verification_calls": mean(r["i_verification_calls"] for r in rows),
        "i_tool_failures": total(r["i_tool_failures"] for r in rows),
        "i_corrections_attempted": sum(r["i_correction_attempted"] == 1 for r in rows),
        "i_correction_success_rate": rate(int(r["i_final_class"] == "correct") for r in rows if r["i_correction_attempted"] == 1)[0],
        "i_final_reply_prompted_rate": rate(r["i_final_reply_prompted"] for r in rows)[0],
        "i_protocol_compliance_rate": rate(int(r["i_protocol_note_count"] == 0) for r in rows)[0],
        "b_behaviour_all_ok_rate": rate(int(all(r[k] == 1 for k in ("b_returns_expected", "b_empty_response_ok", "b_error_raises")))
                                        for r in rows if r["b_returns_expected"] is not None)[0],
        "i_behaviour_all_ok_rate": rate(int(all(r[k] == 1 for k in ("i_returns_expected", "i_empty_response_ok", "i_error_raises")))
                                        for r in rows if r["i_returns_expected"] is not None)[0],
    })
    for m in ("b", "i"):
        out.update({f"{m}_mean_duration_s": mean(r[f"{m}_duration_s"] for r in rows),
                    f"{m}_median_duration_s": median(r[f"{m}_duration_s"] for r in rows),
                    f"{m}_total_duration_h": round(total(r[f"{m}_duration_s"] for r in rows) / 3600, 3) if total(r[f"{m}_duration_s"] for r in rows) else None,
                    f"{m}_mean_total_tokens": mean(r[f"{m}_total_tokens"] for r in rows),
                    f"{m}_mean_energy_j": mean(r[f"{m}_energy_j"] for r in rows),
                    f"{m}_total_energy_wh": round(total(r[f"{m}_energy_j"] for r in rows) / 3600, 3) if total(r[f"{m}_energy_j"] for r in rows) else None})
    correct_b = sum(r["b_correct"] == 1 for r in rows)
    correct_i = sum(r["i_correct_reaches_user"] == 1 for r in rows)
    out["b_seconds_per_correct_answer"] = round(total(r["b_duration_s"] for r in rows) / correct_b, 2) if correct_b and total(r["b_duration_s"] for r in rows) else None
    out["i_seconds_per_correct_answer"] = round(total(r["i_duration_s"] for r in rows) / correct_i, 2) if correct_i and total(r["i_duration_s"] for r in rows) else None
    out["b_wh_per_correct_answer"] = round(total(r["b_energy_j"] for r in rows) / 3600 / correct_b, 4) if correct_b and total(r["b_energy_j"] for r in rows) else None
    out["i_wh_per_correct_answer"] = round(total(r["i_energy_j"] for r in rows) / 3600 / correct_i, 4) if correct_i and total(r["i_energy_j"] for r in rows) else None
    return out


def fmt_ci(interval) -> str:
    lo, hi = interval
    return f"[{lo:.4f}, {hi:.4f}]"


def detection(rows: list, target: str) -> dict:
    """The verifier as a detector: positive = the final candidate is a hallucination
    (target 'A') or wrong for the task ('A_or_B'); predicted positive = withheld."""
    counts = Counter()
    for r in rows:
        cls = r["i_final_class"]
        if cls in (None, "undetermined", "no_code"):
            continue
        positive = cls == "A" if target == "A" else cls in ("A", "B")
        counts[("TP" if r["i_withheld"] else "FN") if positive else ("FP" if r["i_withheld"] else "TN")] += 1
    tp, fp, fn, tn = (counts[k] for k in ("TP", "FP", "FN", "TN"))
    div = lambda a, b: round(a / b, 4) if b else None
    precision, recall = div(tp, tp + fp), div(tp, tp + fn)
    return {"target": target, "n": tp + fp + fn + tn, "TP": tp, "FP": fp, "FN": fn, "TN": tn,
            "precision": precision, "recall": recall,
            "f1": round(2 * precision * recall / (precision + recall), 4) if precision and recall else None,
            "false_positive_rate": div(fp, fp + tn), "false_negative_rate": div(fn, fn + tp),
            "specificity": div(tn, tn + fp), "accuracy": div(tp + tn, tp + fp + fn + tn)}


def write_csv(path: Path, rows: list) -> None:
    if not rows:
        return
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def run_info(files: BenchmarkFiles, label: str) -> dict:
    info = {}
    for mode in ("intervention", "baseline"):
        m = files.manifest(mode, label)
        if not m:
            continue
        model = m.get("lmstudio_model_info") or {}
        settings = m.get("settings") or {}
        env = ((m.get("invocations") or [{}])[-1].get("environment") or {})
        power = ((m.get("invocations") or [{}])[-1].get("power") or {})
        info.setdefault("model", settings.get("model"))
        info.setdefault("quantization", model.get("quantization"))
        info.setdefault("arch", model.get("arch"))
        info.setdefault("context", m.get("context_limit"))
        info.setdefault("thinking", settings.get("thinking"))
        info.setdefault("temperature", settings.get("temperature"))
        info.setdefault("benchmark_version", settings.get("benchmark_version") or "2026-09-26.2 or earlier")
        gpus = power.get("gpus") or env.get("gpus") or []
        info.setdefault("gpu", ", ".join(g.get("name", "") for g in gpus) or None)
        info.setdefault("cpu", env.get("cpu"))
    return info


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    tasks = {t["task_id"]: t for t in load_jsonl(TASKS_DEFAULT)}
    files = BenchmarkFiles(BENCHMARK)
    labels = sorted(p.name for p in RESULTS.iterdir() if (p / "per_task.jsonl").exists()) if RESULTS.exists() else []
    if not labels:
        sys.exit("No evaluated runs found: run python evaluate_benchmark.py first.")
    OUT.mkdir(exist_ok=True)
    prompt_rows, group_rows, model_rows, detect_rows, kind_rows = [], [], [], [], []
    for label in labels:
        info = run_info(files, label)
        evaluated = load_jsonl(RESULTS / label / "per_task.jsonl")
        rows = []
        for ev in evaluated:
            t = ev["task_id"]
            rows.append(prompt_row(label, tasks[t], ev, files.result("baseline", label, t), files.result("intervention", label, t), info))
        missing_cost = sum(r["b_duration_s"] is None for r in rows)
        print(f"[{label}] {len(rows)} prompts" + (f"; {missing_cost} without benchmark result files" if missing_cost else ""))
        prompt_rows += rows
        main_rows = [r for r in rows if not r["pilot"]]  # plan §6: pilot tasks excluded from summaries
        for dim in DIMENSIONS:
            groups = {"all": main_rows} if dim == "overall" else defaultdict(list)
            if dim != "overall":
                for r in main_rows:
                    groups[r[dim]].append(r)
            for value, members in sorted(groups.items(), key=lambda kv: str(kv[0])):
                group_rows.append({"model_label": label, "quantization": info.get("quantization"), "dimension": dim,
                                   "group": value, **group_summary(members)})
        overall = next(g for g in group_rows if g["model_label"] == label and g["dimension"] == "overall")
        model_rows.append({"model_label": label, **{k: info.get(k) for k in ("model", "quantization", "arch", "context", "thinking",
                                                                            "temperature", "benchmark_version", "gpu", "cpu")},
                           **{k: v for k, v in overall.items() if k not in ("model_label", "quantization", "dimension", "group")}})
        for dim in ("overall", "api"):
            groups = {"all": main_rows} if dim == "overall" else defaultdict(list)
            if dim == "api":
                for r in main_rows:
                    groups[r["api"]].append(r)
            for value, members in sorted(groups.items()):
                for target in ("A", "A_or_B"):
                    detect_rows.append({"model_label": label, "dimension": dim, "group": value, **detection(members, target)})
        for dim in DIMENSIONS:
            groups = {"all": main_rows} if dim == "overall" else defaultdict(list)
            if dim != "overall":
                for r in main_rows:
                    groups[r[dim]].append(r)
            for value, members in sorted(groups.items(), key=lambda kv: str(kv[0])):
                for mode, prefix in (("baseline", "b"), ("intervention", "i")):
                    for error_class, key in (("A", "hallucination_kinds"), ("B", "task_error_kinds"),
                                             ("runtime_failure", "runtime_failure_kind")):
                        kinds = Counter(k for r in members for k in r[f"{prefix}_{key}"].split("|") if k)
                        for kind, n in sorted(kinds.items(), key=lambda kv: -kv[1]):
                            kind_rows.append({"model_label": label, "mode": mode, "error_class": error_class,
                                              "dimension": dim, "group": value, "kind": kind, "tasks": n,
                                              "group_tasks": len(members), "share_of_group": round(n / len(members), 4)})
    adjusted = holm({m["model_label"]: m["hallucination_mcnemar_p"] for m in model_rows if m["hallucination_mcnemar_p"] is not None})
    for m in model_rows:
        m["hallucination_mcnemar_p_holm"] = adjusted.get(m["model_label"])
    write_csv(OUT / "prompt_stats.csv", prompt_rows)
    write_csv(OUT / "group_stats.csv", group_rows)
    write_csv(OUT / "model_comparison.csv", model_rows)
    write_csv(OUT / "verifier_detection.csv", detect_rows)
    write_csv(OUT / "error_kinds.csv", kind_rows)
    print(f"Wrote {len(prompt_rows)} prompt rows, {len(group_rows)} group rows, {len(model_rows)} run(s) to {OUT}")


if __name__ == "__main__":
    main()
