#!/usr/bin/env python3
"""
Stats compiler
==============

Compiles every statistic of the project into CSV files, laid out for data processing:
per prompt, per group, per run and per quantization. Standard library only.

Sources (nothing is re-run):
  - Unprocessed Data/evaluation/<label>/per_task.jsonl   classes from evaluate_benchmark.py
  - Benchmark result.json and run_manifest.json files, from run folders or from zipped
    archives anywhere under Benchmark/ (e.g. Completed Runs/...)   time, tokens, energy,
    agent behaviour, settings, machine
  - the dataset's task file                               API, category, method, difficulty, auth

Output (Findings/Statistical Analysis/Unprocessed Data/stats/, described in its STATS_README.md):
  runs.csv                          one row per run: settings, machine, role, totals
  combined/                         every run in one file per table (run_role column to filter)
  by_quantization/<quant>/<label>/  the main runs, one folder per quantization level
  preliminary/<quant>/<label>/      runs made with an older benchmark version
each folder: prompt_stats.csv, group_stats.csv, verifier_detection.csv, error_kinds.csv,
metrics_long.csv (tidy: one measurement per row), run_info.json.
combined/ also has run_comparison.csv (one row per run) and, for the main runs,
quantization_comparison.csv (one row per quantization, one column per headline measure).

Usage:  python compile_stats.py            (after python evaluate_benchmark.py)
"""
from __future__ import annotations

import csv
import json
import shutil
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

from evaluate_benchmark import TASKS_DEFAULT, UNPROCESSED, hallucination_types, load_jsonl, runtime_failure_type, task_error_types
from evaluator import runs as run_registry
from evaluator.stats import holm, mcnemar_exact, wilson

ROOT = Path(__file__).resolve().parent
BENCHMARK = ROOT.parent / "Benchmark"
RESULTS = UNPROCESSED / "evaluation"
OUT = UNPROCESSED / "stats"
DIMENSIONS = ["overall", "api", "operation_category", "http_method", "difficulty", "auth_type", "spec_source"]


# ---------------------------------------------------------------- per-prompt values
def num(x):
    return x if isinstance(x, (int, float)) and not isinstance(x, bool) else None


def flag(x):
    """A true/false value as 1/0; None when it was not recorded. (num() above deliberately
    rejects booleans, which made every true/false column blank in the first version.)"""
    return int(x) if isinstance(x, bool) or x in (0, 1) and x is not None else None


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
        "model_label": label, "run_role": run_info.get("role"), "model": run_info.get("model"),
        "quantization": run_info.get("quantization"), "architecture": run_info.get("architecture"),
        "context_length": run_info.get("context_length"), "thinking": run_info.get("thinking"),
        "temperature": run_info.get("temperature"), "benchmark_version": run_info.get("benchmark_version"),
        "machine_gpu": run_info.get("machine_gpu"), "machine_cpu": run_info.get("machine_cpu"),
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
        "b_returns_expected": flag(bb.get("returns_expected_value")) if bb else None,
        "b_empty_response_ok": flag(bb.get("empty_response_ok")) if bb else None,
        "b_error_raises": flag(bb.get("error_raises")) if bb else None,
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
        "i_first_had_contradiction": flag(ijsonl.get("first_has_contradiction")),
        "i_correction_attempted": flag(ijsonl.get("correction_attempted")),
        "i_correction_allowed": flag(ijsonl.get("correction_allowed")), "i_correction_count": num(ijsonl.get("correction_count")),
        "i_correction_outcome": f"{ev.get('first_class')}->{f_cls}" if ijsonl.get("correction_attempted") else "",
        "i_final_reply_prompted": flag(ijsonl.get("final_reply_prompted")),
        "i_reply_matches_report": flag((imeta.get("final_reply") or {}).get("matches_report")),
        "i_protocol_note_count": len(ev.get("protocol_notes") or []), "i_protocol_notes": " | ".join(ev.get("protocol_notes") or []),
        "i_returns_expected": flag(ib.get("returns_expected_value")) if ib else None,
        "i_empty_response_ok": flag(ib.get("empty_response_ok")) if ib else None,
        "i_error_raises": flag(ib.get("error_raises")) if ib else None,
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
                    **ci_columns(f"b_{name}_rate", bb, nb), **ci_columns(f"i_{name}_rate", ii, ni),
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
        seconds, joules = total(r[f"{m}_duration_s"] for r in rows), total(r[f"{m}_energy_j"] for r in rows)
        wh = lambda key: round(total(r[key] for r in rows) / 3600, 3) if total(r[key] for r in rows) else None
        out.update({f"{m}_mean_duration_s": mean(r[f"{m}_duration_s"] for r in rows),
                    f"{m}_median_duration_s": median(r[f"{m}_duration_s"] for r in rows),
                    f"{m}_mean_model_s": mean(r[f"{m}_model_s"] for r in rows), f"{m}_mean_tool_s": mean(r[f"{m}_tool_s"] for r in rows),
                    f"{m}_total_duration_h": round(seconds / 3600, 3) if seconds else None,
                    f"{m}_mean_prompt_tokens": mean(r[f"{m}_prompt_tokens"] for r in rows),
                    f"{m}_mean_completion_tokens": mean(r[f"{m}_completion_tokens"] for r in rows),
                    f"{m}_mean_total_tokens": mean(r[f"{m}_total_tokens"] for r in rows),
                    f"{m}_total_tokens": total(r[f"{m}_total_tokens"] for r in rows),
                    f"{m}_mean_completion_tokens_per_s": mean(r[f"{m}_completion_tokens_per_s"] for r in rows),
                    f"{m}_mean_energy_j": mean(r[f"{m}_energy_j"] for r in rows),
                    f"{m}_mean_energy_above_idle_j": mean(r[f"{m}_energy_above_idle_j"] for r in rows),
                    f"{m}_total_energy_wh": wh(f"{m}_energy_j"), f"{m}_total_gpu_energy_wh": wh(f"{m}_gpu_energy_j"),
                    f"{m}_total_cpu_energy_wh": wh(f"{m}_cpu_energy_j"), f"{m}_total_energy_above_idle_wh": wh(f"{m}_energy_above_idle_j"),
                    f"{m}_mean_power_w": round(joules / seconds, 1) if joules and seconds else None})
    correct_b = sum(r["b_correct"] == 1 for r in rows)
    correct_i = sum(r["i_correct_reaches_user"] == 1 for r in rows)
    out["b_seconds_per_correct_answer"] = round(total(r["b_duration_s"] for r in rows) / correct_b, 2) if correct_b and total(r["b_duration_s"] for r in rows) else None
    out["i_seconds_per_correct_answer"] = round(total(r["i_duration_s"] for r in rows) / correct_i, 2) if correct_i and total(r["i_duration_s"] for r in rows) else None
    out["b_wh_per_correct_answer"] = round(total(r["b_energy_j"] for r in rows) / 3600 / correct_b, 4) if correct_b and total(r["b_energy_j"] for r in rows) else None
    out["i_wh_per_correct_answer"] = round(total(r["i_energy_j"] for r in rows) / 3600 / correct_i, 4) if correct_i and total(r["i_energy_j"] for r in rows) else None
    return out


def ci_columns(prefix: str, rate_value, n: int) -> dict:
    """Wilson 95% interval of a rate, as two numeric columns."""
    if rate_value is None:
        return {f"{prefix}_ci_low": None, f"{prefix}_ci_high": None}
    lo, hi = wilson(round(rate_value * n), n)
    return {f"{prefix}_ci_low": round(lo, 4), f"{prefix}_ci_high": round(hi, 4)}


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


ID_COLUMNS = ("model_label", "quantization", "run_role", "benchmark_version", "dimension", "group")


def metrics_long(group_rows: list) -> list:
    """Tidy table: one measurement per row, for pivoting in pandas, R or a spreadsheet."""
    out = []
    for g in group_rows:
        for metric, value in g.items():
            if metric in ID_COLUMNS or not isinstance(value, (int, float)) or isinstance(value, bool):
                continue
            if metric.startswith("b_"):
                mode, name = "baseline", metric[2:]
            elif metric.startswith("i_"):
                mode, name = "intervention", metric[2:]
            else:
                mode, name = "paired", metric
            out.append({**{k: g.get(k) for k in ID_COLUMNS}, "mode": mode, "metric": name, "value": value})
    return out


def write_csv(path: Path, rows: list) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


HEADLINE = ("n", "b_hallucination_rate", "i_hallucination_rate", "hallucination_improvement", "hallucination_repairs",
            "hallucination_regressions", "hallucination_mcnemar_p", "hallucination_mcnemar_p_holm", "b_correct_rate",
            "i_correct_rate", "correct_improvement", "i_abstention_rate", "i_incorrect_acceptance", "i_incorrect_rejection",
            "i_mean_ewcs", "i_corrections_attempted", "i_correction_success_rate", "i_protocol_compliance_rate",
            "i_final_reply_prompted_rate", "b_behaviour_all_ok_rate", "i_behaviour_all_ok_rate", "b_mean_duration_s",
            "i_mean_duration_s", "b_total_duration_h", "i_total_duration_h", "b_mean_total_tokens", "i_mean_total_tokens",
            "b_mean_energy_j", "i_mean_energy_j", "b_total_energy_wh", "i_total_energy_wh", "b_mean_power_w", "i_mean_power_w",
            "b_seconds_per_correct_answer", "i_seconds_per_correct_answer", "b_wh_per_correct_answer", "i_wh_per_correct_answer")


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    tasks = {t["task_id"]: t for t in load_jsonl(TASKS_DEFAULT)}
    labels = sorted(p.name for p in RESULTS.iterdir() if (p / "per_task.jsonl").exists()) if RESULTS.exists() else []
    if not labels:
        sys.exit("No evaluated runs found: run python evaluate_benchmark.py first.")
    registry = run_registry.discover(BENCHMARK, labels)
    files = run_registry.BenchmarkFiles(BENCHMARK)
    prompt_rows, group_rows, model_rows, detect_rows, kind_rows, run_rows = [], [], [], [], [], []
    per_run: dict = {}
    for label in labels:
        info = registry[label]
        rows = []
        for ev in load_jsonl(RESULTS / label / "per_task.jsonl"):
            t = ev["task_id"]
            rows.append(prompt_row(label, tasks[t], ev, files.result("baseline", label, t), files.result("intervention", label, t), info))
        without = sum(r["b_duration_s"] is None for r in rows)
        print(f"[{label}] {info['quantization']} ({info['role']}): {len(rows)} prompts"
              + (f"; {without} without benchmark result files (cost columns empty)" if without else ""), flush=True)
        main_rows = [r for r in rows if not r["pilot"]]  # plan §6: pilot tasks are excluded from summaries
        g_rows, d_rows, k_rows = [], [], []
        for dim in DIMENSIONS:
            groups = {"all": main_rows} if dim == "overall" else defaultdict(list)
            if dim != "overall":
                for r in main_rows:
                    groups[r[dim]].append(r)
            for value, members in sorted(groups.items(), key=lambda kv: str(kv[0])):
                g_rows.append({"model_label": label, "quantization": info["quantization"], "run_role": info["role"],
                               "benchmark_version": info["benchmark_version"], "dimension": dim, "group": value,
                               **group_summary(members)})
                for mode, prefix in (("baseline", "b"), ("intervention", "i")):
                    for error_class, key in (("A", "hallucination_kinds"), ("B", "task_error_kinds"),
                                             ("runtime_failure", "runtime_failure_kind")):
                        kinds = Counter(k for r in members for k in r[f"{prefix}_{key}"].split("|") if k)
                        for kind, n in sorted(kinds.items(), key=lambda kv: -kv[1]):
                            k_rows.append({"model_label": label, "quantization": info["quantization"], "run_role": info["role"],
                                           "mode": mode, "error_class": error_class, "dimension": dim, "group": value,
                                           "kind": kind, "tasks": n, "group_tasks": len(members),
                                           "share_of_group": round(n / len(members), 4)})
                if dim in ("overall", "api"):
                    for target in ("A", "A_or_B"):
                        d_rows.append({"model_label": label, "quantization": info["quantization"], "run_role": info["role"],
                                       "dimension": dim, "group": value, **detection(members, target)})
        overall = next(g for g in g_rows if g["dimension"] == "overall")
        # whole-run totals over every prompt, pilot included: what the run actually cost
        totals = {}
        for m in ("b", "i"):
            secs = total(r[f"{m}_duration_s"] for r in rows)
            joules = total(r[f"{m}_energy_j"] for r in rows)
            totals.update({f"{m}_run_hours": round(secs / 3600, 3) if secs else None,
                           f"{m}_run_energy_wh": round(joules / 3600, 3) if joules else None,
                           f"{m}_run_tokens": total(r[f"{m}_total_tokens"] for r in rows)})
        run_rows.append({"model_label": label, "quantization": info["quantization"], "role": info["role"],
                         "role_reason": info["role_reason"], "label_matches_quantization": int(info["label_matches_quantization"]),
                         **{k: info.get(k) for k in ("model", "architecture", "context_length", "thinking", "temperature",
                                                     "max_tokens", "max_turns", "seed", "benchmark_version", "frozen_package_evidence",
                                                     "started_first", "machine_cpu", "machine_gpu", "machine_ram_gb",
                                                     "power_backend", "power_idle_w")},
                         "git_commits": " ".join(info["commits"]), "prompts": len(rows), "prompts_summarised": len(main_rows), **totals})
        model_rows.append({"model_label": label, "run_role": info["role"], "model": info.get("model"),
                           "quantization": info["quantization"], "architecture": info.get("architecture"),
                           "context_length": info.get("context_length"), "benchmark_version": info["benchmark_version"],
                           "machine_gpu": info.get("machine_gpu"), **{k: v for k, v in overall.items() if k not in ID_COLUMNS}})
        per_run[label] = (rows, g_rows, d_rows, k_rows)
        prompt_rows += rows
        group_rows += g_rows
        detect_rows += d_rows
        kind_rows += k_rows
    files.close()
    # Holm's correction across the main runs only (plan §6); preliminary runs keep their raw p-value.
    adjusted = holm({m["model_label"]: m["hallucination_mcnemar_p"] for m in model_rows
                     if m["run_role"] == "main" and m["hallucination_mcnemar_p"] is not None})
    for m in model_rows:
        m["hallucination_mcnemar_p_holm"] = adjusted.get(m["model_label"])
    holm_by_label = {m["model_label"]: m["hallucination_mcnemar_p_holm"] for m in model_rows}
    for g in group_rows:
        if g["dimension"] == "overall":
            g["hallucination_mcnemar_p_holm"] = holm_by_label.get(g["model_label"])

    # ---- write: regenerate the tables from scratch (they are never edited by hand)
    for name in ("combined", "by_quantization", "preliminary"):
        shutil.rmtree(OUT / name, ignore_errors=True)
    for stale in ("prompt_stats.csv", "group_stats.csv", "model_comparison.csv", "verifier_detection.csv",
                  "hallucination_kinds.csv", "error_kinds.csv"):
        (OUT / stale).unlink(missing_ok=True)  # the flat layout of earlier versions
    OUT.mkdir(exist_ok=True)
    write_csv(OUT / "runs.csv", sorted(run_rows, key=lambda r: (r["role"] != "main", r["quantization"] or "", r["model_label"])))
    combined = OUT / "combined"
    write_csv(combined / "prompt_stats.csv", prompt_rows)
    write_csv(combined / "group_stats.csv", group_rows)
    write_csv(combined / "verifier_detection.csv", detect_rows)
    write_csv(combined / "error_kinds.csv", kind_rows)
    write_csv(combined / "metrics_long.csv", metrics_long(group_rows))
    ordered = sorted(model_rows, key=lambda r: (r["run_role"] != "main", r["quantization"] or "", r["model_label"]))
    write_csv(combined / "run_comparison.csv", ordered)
    write_csv(combined / "quantization_comparison.csv", [
        {"quantization": m["quantization"], "model_label": m["model_label"], "model": m["model"], **{k: m.get(k) for k in HEADLINE}}
        for m in ordered if m["run_role"] == "main"])
    for label, (rows, g_rows, d_rows, k_rows) in per_run.items():
        info = registry[label]
        folder = OUT / ("by_quantization" if info["role"] == "main" else "preliminary") / (info["quantization"] or "unknown") / label
        write_csv(folder / "prompt_stats.csv", rows)
        write_csv(folder / "group_stats.csv", g_rows)
        write_csv(folder / "verifier_detection.csv", d_rows)
        write_csv(folder / "error_kinds.csv", k_rows)
        write_csv(folder / "metrics_long.csv", metrics_long(g_rows))
        overall = next(g for g in g_rows if g["dimension"] == "overall")
        headline = {k: overall.get(k) for k in HEADLINE if k != "hallucination_mcnemar_p_holm"}
        headline["hallucination_mcnemar_p_holm"] = holm_by_label.get(label)
        (folder / "run_info.json").write_text(json.dumps(
            {"run": {k: v for k, v in info.items() if k not in ("versions", "started")}, "prompts": len(rows),
             "headline": headline}, indent=2), encoding="utf-8")
        print(f"  -> {folder.relative_to(ROOT.parent)}", flush=True)
    print(f"Wrote {len(prompt_rows)} prompt rows for {len(labels)} run(s) to {OUT}")


if __name__ == "__main__":
    main()
