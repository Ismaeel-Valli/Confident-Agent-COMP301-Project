#!/usr/bin/env python3
"""
Stage analysis
==============

Two analyses added for the final report, after the lecturer's feedback on the first draft.
Standard library only; nothing in evaluate_benchmark.py changes.

1. Where in the intervention the reduction happens. The benchmark stores the first candidate
   the model submitted for verification: it was written under the Confident Agent prompt but
   before any verification feedback. This script classifies it with the same evaluator and the
   same manual-review decisions as every other candidate, and counts its kinds of hallucination
   exactly as evaluate_benchmark.py does for the baseline and the delivered code. Baseline ->
   first candidate -> delivered code is a decomposition by stage, not an ablation.
2. How related the three quantization runs are: per-task agreement (Cohen's kappa) between
   runs, for the baseline's hallucination indicator, the baseline class and the agent's
   delivered/withheld decision, read from per_task.jsonl.
3. API conformance against the whole task: how often the delivered code is class "correct"
   (the right request) and also meets all three behaviour checks, read from per_task.jsonl.

Output: ../Statistical Analysis/Unprocessed Data/evaluation/stage_analysis.json

Usage:  python stage_analysis.py            (after python evaluate_benchmark.py; about 15 minutes)
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

from evaluate_benchmark import (FINDINGS, ROOT, TASKS_DEFAULT, UNPROCESSED, Evaluator, build_contexts,
                                hallucination_types, load_jsonl, load_reviews, reviewed)
from evaluator import runs as run_registry

WRONG_HOST = "wrong host, version or base path"


def kappa(a: list, b: list) -> tuple[float, float]:
    n = len(a)
    agree = sum(x == y for x, y in zip(a, b)) / n
    chance = sum((a.count(c) / n) * (b.count(c) / n) for c in set(a) | set(b))
    return agree, (agree - chance) / (1 - chance) if chance < 1 else 1.0


def all_ok(behaviour: dict | None) -> bool:
    return bool(behaviour) and all(behaviour.values())


def task_behaviour(records: list) -> dict:
    """Behaviour checks on the code each condition delivered (per_task.jsonl records)."""
    base_programs = [r for r in records if r["baseline_behaviour"]]
    shown = [r for r in records if r["code_shown"] and r["shown_behaviour"]]
    shown_correct = [r for r in shown if r["shown_class"] == "correct"]
    return {
        "baseline_all_checks_share_of_programs": sum(all_ok(r["baseline_behaviour"]) for r in base_programs) / len(base_programs),
        "agent_all_checks_share_of_delivered_programs": sum(all_ok(r["shown_behaviour"]) for r in shown) / len(shown),
        "fully_correct_share_of_tasks": {  # class correct and all three behaviour checks met
            "baseline": sum(1 for r in records if r["baseline_class"] == "correct" and all_ok(r["baseline_behaviour"])) / len(records),
            "agent": sum(1 for r in shown_correct if all_ok(r["shown_behaviour"])) / len(records)},
        "agent_correct_delivered_check_shares": {
            k: sum(1 for r in shown_correct if r["shown_behaviour"][k]) / len(shown_correct)
            for k in ("returns_expected_value", "empty_response_ok", "error_raises")},
    }


def summarise(results: list) -> dict:
    """results: one evaluator result per task. Kinds are read from the class-A reasons only,
    as in evaluate_benchmark.analyse()."""
    classes = Counter(r["class"] for r in results)
    a = [r for r in results if r["class"] == "A"]
    kinds = Counter(k for r in a for k in hallucination_types(r.get("a_reasons") or []))
    return {"tasks": len(results), "classes": dict(classes),
            "A_rate": classes["A"] / len(results),
            "A_rate_undetermined_as_A": (classes["A"] + classes["undetermined"]) / len(results),
            "hallucination_types": dict(kinds),
            "A_other_than_wrong_host": sum(1 for r in a if hallucination_types(r.get("a_reasons") or []) - {WRONG_HOST})}


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    p = argparse.ArgumentParser(description="Stage analysis: first candidates and agreement between runs")
    p.add_argument("--benchmark", type=Path, default=FINDINGS / "Benchmark")
    p.add_argument("--dataset", type=Path, default=TASKS_DEFAULT)
    p.add_argument("--evaluation", type=Path, default=UNPROCESSED / "evaluation")
    p.add_argument("--reviews", type=Path, default=ROOT / "reviews" / "reviews.csv")
    p.add_argument("--jobs", type=int, default=8)
    p.add_argument("--timeout", type=float, default=10.0, help="seconds per sandboxed run")
    args = p.parse_args()

    tasks = load_jsonl(args.dataset)
    by_id = {t["task_id"]: t for t in tasks}
    contexts, _ = build_contexts(tasks)
    evaluator = Evaluator(contexts, args.jobs, args.timeout)
    reviews = load_reviews(args.reviews)
    base_rows = load_jsonl(args.benchmark / "complete_test_baseline.jsonl")
    inter_rows = load_jsonl(args.benchmark / "complete_test_intervention.jsonl")
    pilot = {json.loads(l)["task_id"] for l in (args.benchmark / "dataset" / "rest_api_prompts_pilot.jsonl")
             .read_text(encoding="utf-8").splitlines() if l.strip()}
    labels = sorted({r["model_label"] for r in base_rows} & {r["model_label"] for r in inter_rows})
    registry = run_registry.discover(args.benchmark, labels)
    main_runs = [l for l in labels if registry[l]["role"] == "main"]

    out = {"stages": {}, "agreement_between_runs": {}}
    per_task = {}
    for label in main_runs:
        base = {r["prompt_id"]: r for r in base_rows if r["model_label"] == label}
        inter = {r["prompt_id"]: r for r in inter_rows if r["model_label"] == label}
        ids = sorted(t for t in set(base) & set(inter) & set(by_id) if t not in pilot)
        print(f"[{label}] {len(ids)} tasks; classifying baseline code and first candidates ...", flush=True)
        evaluator.run_all([(t, c) for t in ids for c in (base[t].get("code"), inter[t].get("first_candidate"))])
        cls = lambda t, code: reviewed(evaluator.get(t, code), t, code, reviews)
        records = {r["task_id"]: r for r in load_jsonl(args.evaluation / label / "per_task.jsonl") if not r["pilot"]}
        per_task[label] = records
        shown_a = [r for r in records.values() if r["shown_class"] == "A"]
        out["stages"][label] = {
            "quantization": registry[label].get("quantization"),
            "baseline": summarise([cls(t, base[t].get("code")) for t in ids]),
            "first_candidate": summarise([cls(t, inter[t].get("first_candidate")) for t in ids]),
            "delivered": {"tasks": len(records), "A": len(shown_a), "A_rate": len(shown_a) / len(records),
                          "withheld": sum(1 for r in records.values() if not r["code_shown"]),
                          "A_other_than_wrong_host": sum(1 for r in shown_a if hallucination_types(r["shown_a_reasons"]) - {WRONG_HOST})},
            "task_behaviour": task_behaviour(list(records.values())),
        }
    measures = {"baseline_A": lambda r: r["baseline_class"] == "A", "baseline_class": lambda r: r["baseline_class"],
                "agent_delivered": lambda r: r["delivered"]}
    for x, y in itertools.combinations(main_runs, 2):
        ids = sorted(set(per_task[x]) & set(per_task[y]))
        out["agreement_between_runs"][f"{x} | {y}"] = {
            name: dict(zip(("agreement", "kappa"), kappa([f(per_task[x][t]) for t in ids], [f(per_task[y][t]) for t in ids])))
            for name, f in measures.items()}
    if len(main_runs) == 3:
        common = sorted(set.intersection(*(set(per_task[l]) for l in main_runs)))
        counts = Counter(sum(per_task[l][t]["baseline_class"] == "A" for l in main_runs) for t in common)
        out["baseline_A_in_how_many_runs"] = {str(k): counts.get(k, 0) for k in range(4)}
    path = args.evaluation / "stage_analysis.json"
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    for label, s in out["stages"].items():
        print(f"[{label}] class A: baseline {s['baseline']['A_rate']:.3f}, first candidate {s['first_candidate']['A_rate']:.3f} "
              f"({s['first_candidate']['A_rate_undetermined_as_A']:.3f} with undetermined as A), delivered {s['delivered']['A_rate']:.3f}")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
