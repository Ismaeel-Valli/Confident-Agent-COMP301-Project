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
3. Audit-informed re-scoring of every main run. The adjudication applied two rules the
   evaluator does not: an Accept header naming an undocumented GitHub media type (for example
   vnd.github.v2026-03-10+json) is class A, and Open-Meteo's legacy variable names
   (windspeed_10m for wind_speed_10m) are class C. The primary outcome is recomputed with both
   rules, as a robustness check of the pre-registered result; the evaluator is unchanged.
   The Accept rule reads the media type from the code's text, which is an approximation.

Output: ../Statistical Analysis/Unprocessed Data/evaluation/audit_analysis.json

Usage:  python audit_analysis.py
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

from evaluate_benchmark import DATASET_DIR, FINDINGS, ROOT, UNPROCESSED, load_jsonl
from evaluator import runs as run_registry
from evaluator.stats import holm, mcnemar_exact, wilson

AUDIT = ROOT / "reviews" / "audit_reviews.csv"
BENCHMARK = FINDINGS / "Benchmark"
# A GitHub media type other than the documented application/vnd.github+json and the long-standing
# v3 form, written literally (v2, a date) or built from a variable (f"...github.{version}-preview+json").
INVENTED_GITHUB_MEDIA_TYPE = re.compile(r"application/vnd\.github\.(?!v3\+json)")
LEGACY_OPEN_METEO = re.compile(r"\b(windspeed|winddirection|windgusts)_")
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


def primary_errors_by_role(rows: list) -> dict:
    """Evaluator errors on the primary outcome against the adjudicated class, per role, with the
    share of the role's sampled candidates (the sample is random within each role and API)."""
    out = {}
    for role in sorted({r["role"] for r in rows}):
        rs = [r for r in rows if r["role"] == role and r["agreed_class"]]
        missed = [r["task_id"] for r in rs if r["automatic_class"] != "A" and r["agreed_class"] == "A"]
        false = [r["task_id"] for r in rs if r["automatic_class"] == "A" and r["agreed_class"] != "A"]
        out[role] = {"n": len(rs), "missed_hallucinations": missed, "false_hallucinations": false,
                     "missed_share": len(missed) / len(rs), "missed_share_wilson95": wilson(len(missed), len(rs)),
                     "false_share": len(false) / len(rs), "false_share_wilson95": wilson(len(false), len(rs))}
    return out


def rescore(evaluation: Path) -> dict:
    """The primary outcome of every main run with the two adjudicated rules applied."""
    base_rows, inter_rows = load_jsonl(BENCHMARK / "complete_test_baseline.jsonl"), load_jsonl(BENCHMARK / "complete_test_intervention.jsonl")
    labels = sorted({r["model_label"] for r in base_rows} & {r["model_label"] for r in inter_rows})
    registry = run_registry.discover(BENCHMARK, labels)
    out, pvalues = {}, {}
    for label in (l for l in labels if registry[l]["role"] == "main"):
        base = {r["prompt_id"]: r.get("code") or "" for r in base_rows if r["model_label"] == label}
        shown = {r["prompt_id"]: r.get("code_output") or r.get("reply_code") or "" for r in inter_rows if r["model_label"] == label}
        records = [r for r in load_jsonl(evaluation / label / "per_task.jsonl") if not r["pilot"]]
        changes = Counter()

        def is_a(r, role):
            cls, reasons, code = ((r["baseline_class"], r["baseline_a_reasons"], base.get(r["task_id"], "")) if role == "baseline"
                                  else (r["shown_class"], r["shown_a_reasons"], shown.get(r["task_id"], "")))
            if cls == "A" and reasons and all(LEGACY_OPEN_METEO.search(x) for x in reasons):
                changes[f"{role}: A -> C (legacy Open-Meteo name)"] += 1
                return False
            if cls in ("correct", "B") and r["api"] == "GitHub" and INVENTED_GITHUB_MEDIA_TYPE.search(code):
                changes[f"{role}: {cls} -> A (invented GitHub media type)"] += 1
                return True
            return cls == "A"

        pairs = [(is_a(r, "baseline"), r["code_shown"] and is_a(r, "shown")) for r in records]
        b = sum(1 for x, y in pairs if x and not y)
        c = sum(1 for x, y in pairs if y and not x)
        n = len(pairs)
        out[label] = {"quantization": registry[label].get("quantization"), "tasks": n, "changes": dict(changes),
                      "baseline_rate": sum(x for x, _ in pairs) / n, "intervention_rate": sum(y for _, y in pairs) / n,
                      "discordant_baseline_only": b, "discordant_intervention_only": c, "mcnemar_p": mcnemar_exact(b, c)}
        pvalues[label] = out[label]["mcnemar_p"]
    for label, p in holm(pvalues).items():
        out[label]["mcnemar_p_holm"] = p
    return out


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
        "primary_errors_by_role": primary_errors_by_role(audit),
    }}
    out["audit_informed_rescoring"] = rescore(UNPROCESSED / "evaluation")
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
    for role, e in ev["primary_errors_by_role"].items():
        print(f"{role:8} n={e['n']} missed A {e['missed_hallucinations']} false A {e['false_hallucinations']}")
    for label, s in out["audit_informed_rescoring"].items():
        print(f"[{s['quantization']}] A: baseline {s['baseline_rate']:.3f} -> agent {s['intervention_rate']:.3f}  "
              f"b/c {s['discordant_baseline_only']}/{s['discordant_intervention_only']}  Holm p {s['mcnemar_p_holm']:.2g}  {s['changes']}")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
