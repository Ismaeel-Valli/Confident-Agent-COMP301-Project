#!/usr/bin/env python3
"""
Audit analysis
==============

Summarises the two human audits (evaluation plan §5). Standard library only.

1. Evaluator audit (reviews/audit_reviews.csv): a stratified random sample of 102 decided
   candidates from the Q6_K run (52 baseline, 50 shown by the agent), drawn by
   evaluate_benchmark.py as audit_sample.csv and classified independently by two group
   members. The completed sample is kept here because evaluate_benchmark.py rewrites
   audit_sample.csv on every run. Agreement is reported between each reviewer and the
   evaluator, between the reviewers, and between the agreed class and the evaluator, for the
   full class and for the primary outcome (class A or not).
2. Answer-key audit (review_100.csv in the dataset builder): a stratified 100-task sample of
   the answer key checked against the providers' documentation.

Output: ../Statistical Analysis/Unprocessed Data/evaluation/audit_analysis.json

Usage:  python audit_analysis.py
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from evaluate_benchmark import DATASET_DIR, ROOT, UNPROCESSED

AUDIT = ROOT / "reviews" / "audit_reviews.csv"
ANSWER_KEY_REVIEW = DATASET_DIR / "review" / "review_100.csv"
CHECKS = ("source_contract_correct", "prompt_unambiguous", "reference_code_correct", "test_case_correct",
          "alternative_valid_calls_considered", "difficulty_label_checked")


def read(path: Path) -> list:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def agreement(a: list, b: list) -> dict:
    n = len(a)
    if not n:
        return {"n": 0}
    agree = sum(x == y for x, y in zip(a, b)) / n
    chance = sum((a.count(c) / n) * (b.count(c) / n) for c in set(a) | set(b))
    return {"n": n, "agreement": agree, "kappa": (agree - chance) / (1 - chance) if chance < 1 else 1.0,
            "disagreements": dict(Counter(f"{x}->{y}" for x, y in zip(a, b) if x != y))}


def compare(rows: list, left: str, right: str) -> dict:
    rows = [r for r in rows if r[left] and r[right]]
    full = agreement([r[left] for r in rows], [r[right] for r in rows])
    primary = agreement([r[left] == "A" for r in rows], [r[right] == "A" for r in rows])
    primary.pop("disagreements", None)
    return {"class": full, "class_A_or_not": primary}


def main() -> None:
    audit = read(AUDIT)
    out = {"evaluator_audit": {
        "file": str(AUDIT.relative_to(ROOT)), "runs": sorted({r["label"] for r in audit}),
        "candidates": len(audit), "by_role": dict(Counter(r["role"] for r in audit)),
        "automatic_classes": dict(Counter(r["automatic_class"] for r in audit)),
        "adjudicated": sum(1 for r in audit if r["agreed_class"]),
        "awaiting_adjudication": [r["task_id"] + "/" + r["role"] for r in audit if not r["agreed_class"]],
        "reviewer_1_vs_evaluator": compare(audit, "reviewer_1_class", "automatic_class"),
        "reviewer_2_vs_evaluator": compare(audit, "reviewer_2_class", "automatic_class"),
        "reviewer_1_vs_reviewer_2": compare(audit, "reviewer_1_class", "reviewer_2_class"),
        "agreed_vs_evaluator": compare(audit, "agreed_class", "automatic_class"),
    }}
    key = read(ANSWER_KEY_REVIEW)
    out["answer_key_audit"] = {
        "file": "review_100.csv", "tasks": len(key), "by_api": dict(Counter(r["api"] for r in key)),
        "reviewers": dict(Counter(r["reviewer"] for r in key)), "decisions": dict(Counter(r["decision"] for r in key)),
        "checks_passed": {c: sum(r[c].strip().upper() == "YES" for r in key) for c in CHECKS},
    }
    path = UNPROCESSED / "evaluation" / "audit_analysis.json"
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    ev = out["evaluator_audit"]
    for name in ("reviewer_1_vs_evaluator", "reviewer_2_vs_evaluator", "reviewer_1_vs_reviewer_2", "agreed_vs_evaluator"):
        c, p = ev[name]["class"], ev[name]["class_A_or_not"]
        print(f"{name:26} n={c['n']:3}  class {c['agreement']:.3f} (kappa {c['kappa']:.2f})  "
              f"A-or-not {p['agreement']:.3f} (kappa {p['kappa']:.2f})  {c['disagreements']}")
    print(f"adjudicated {ev['adjudicated']}/{ev['candidates']}; answer key: {out['answer_key_audit']['decisions']}")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
