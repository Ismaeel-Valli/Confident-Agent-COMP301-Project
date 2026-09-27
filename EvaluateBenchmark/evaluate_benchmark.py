#!/usr/bin/env python3
"""
Evaluate Benchmark
==================

Scores the results of the Confident Agent Benchmark (../Benchmark) as fixed in
../Benchmark/EVALUATION_PLAN.md. Standard library only.

For every task of every run (model label) in both modes it:
  1. runs the candidate in an isolated sandbox with a recording stand-in for `requests`
     and the task's test inputs, so the exact request is known (evaluator_design.md);
  2. classifies it against the task's answer key and pinned OpenAPI source:
     correct / A (API hallucination) / B (valid call, wrong for the task) /
     runtime_failure / undetermined;
  3. computes the paired comparison (exact McNemar, bootstrap and operation-family
     cluster-bootstrap intervals, Holm across runs), the intervention's confusion matrix,
     EWCS calibration, corrections, protocol compliance, behaviour checks and cost.

Before scoring model output it scores the dataset's reference solutions: all must be
correct (self-check, plan §5).

Usage
-----
    python evaluate_benchmark.py                      # every run found in ../Benchmark
    python evaluate_benchmark.py --labels "Qwen3.5-9B-Q4_K_M-full"
    python evaluate_benchmark.py --self-check-only
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import csv
import hashlib
import json
import random
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from evaluator import stats
from evaluator.classify import TaskContext, classify, code_hash
from evaluator.report import write_report
from evaluator.spec import Spec

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
DATASET_DIR = REPO / "COMP301-Dataset-Builder" / "comp301-dataset-builder"
TASKS_DEFAULT = DATASET_DIR / "output" / "rest_api_tasks_v1_DRAFT.jsonl"
TASKS_SHA256 = "7a09f2bb566dbabbe2b28366bc14a78992b5affd892eb76501cba616d1849a12"  # plan §2, LF endings
EVALUATOR_VERSION = "2026-09-27.1"
DECIDED = ("correct", "A", "B", "runtime_failure")
# Kinds of API hallucination (project description, appendix A.2), read from the class-A reasons
# in this order (the first match names a reason's kind).
HALLUCINATION_TYPES = [
    ("non-existent requests API", ("uses requests API that does not exist",)),
    ("undocumented response field", ("reads response field",)),
    ("wrong host, version or base path", ("not the task's API",)),
    ("invented endpoint or method", ("no declared path", "is not declared for")),
    ("missing required part or credential", ("is missing", "credential", "Authorization is", "expected the form")),
    ("invented parameter or body field", ("is not declared", "is not allowed", "the operation does not declare")),
    ("invalid value or structure", (": expected ", "not one of the documented values", "the operation accepts")),
]
DELIVERED = ("deliver", "deliver_with_flag")


def content_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def load_jsonl(path: Path) -> list:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()] if path.exists() else []


def build_contexts(tasks: list) -> dict:
    specs, contexts, problems = {}, {}, []
    for task in tasks:
        api = task["api_specification"]
        source = DATASET_DIR / api["source_file"]
        if not source.exists():
            source = DATASET_DIR / "sources" / Path(api["source_file"]).name
        if source not in specs:
            if content_sha256(source) != api["source_sha256"] and \
                    hashlib.sha256(source.read_bytes()).hexdigest() != api["source_sha256"]:
                problems.append(f"{source.name} does not match its pinned SHA-256")
            specs[source] = Spec(source)
        contexts[task["task_id"]] = TaskContext(task, specs[source])
    return contexts, sorted(set(problems))


class Evaluator:
    def __init__(self, contexts: dict, jobs: int, timeout: float):
        self.contexts, self.jobs, self.timeout = contexts, jobs, timeout
        self.cache: dict = {}

    def run_all(self, items: list) -> None:
        """items: (task_id, code); results are cached by task and code hash."""
        todo = {(t, code_hash(c)): (t, c) for t, c in items if c and (t, code_hash(c)) not in self.cache}
        with cf.ThreadPoolExecutor(self.jobs) as pool:
            futures = {pool.submit(classify, self.contexts[t], c, self.timeout): key for key, (t, c) in todo.items()}
            for n, future in enumerate(cf.as_completed(futures), 1):
                self.cache[futures[future]] = future.result()
                if n % 250 == 0:
                    print(f"  {n}/{len(futures)} candidates classified", flush=True)

    def get(self, task_id: str, code: str | None) -> dict:
        if not code or not code.strip():
            return {"class": "no_code", "reasons": ["no code"], "requests": 0}
        return self.cache[(task_id, code_hash(code))]


def self_check(evaluator: Evaluator, tasks: list) -> dict:
    evaluator.run_all([(t["task_id"], t["ground_truth"]["code"]) for t in tasks])
    results = {t["task_id"]: evaluator.get(t["task_id"], t["ground_truth"]["code"]) for t in tasks}
    failures = {k: v for k, v in results.items() if v["class"] != "correct" or not all((v.get("behaviour") or {}).values())}
    return {"references": len(results), "correct": sum(v["class"] == "correct" for v in results.values()),
            "behaviour_all_ok": sum(all((v.get("behaviour") or {}).values()) for v in results.values()),
            "failures": {k: {"class": v["class"], "reasons": v["reasons"], "behaviour": v.get("behaviour")}
                         for k, v in failures.items()}}


def load_reviews(path: Path) -> dict:
    """reviews.csv: label, task_id, role, code_sha256, reviewer_1_class, reviewer_2_class, agreed_class, notes."""
    reviews = {}
    if path.exists():
        with path.open(encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                if row.get("code_sha256"):
                    reviews[(row["task_id"], row["code_sha256"])] = row
    return reviews


def reviewed(result: dict, task_id: str, code: str | None, reviews: dict) -> dict:
    if result["class"] != "undetermined" or not code:
        return result
    row = reviews.get((task_id, code_hash(code)))
    if row and row.get("agreed_class") in DECIDED:
        return {**result, "class": row["agreed_class"], "automatic_class": "undetermined", "reviewed": True}
    return result


def task_record(task: dict, base: dict, inter: dict, evaluator: Evaluator, reviews: dict, pilot: set) -> dict:
    tid = task["task_id"]
    shown = inter.get("code_output") or inter.get("reply_code")
    cls = lambda code: reviewed(evaluator.get(tid, code), tid, code, reviews)
    b, s, f, first = cls(base.get("code")), cls(shown), cls(inter.get("final_candidate")), cls(inter.get("first_candidate"))
    return {
        "task_id": tid, "api": task["api_specification"]["api_name"], "family": task["metadata"]["operation_family_id"],
        "category": task["metadata"]["category"], "pilot": tid in pilot,
        "baseline_class": b["class"], "baseline_reasons": b["reasons"], "baseline_a_reasons": b.get("a_reasons") or [],
        "baseline_b_reasons": b.get("b_reasons") or [],
        "baseline_behaviour": b.get("behaviour"),
        "decision": inter.get("decision"), "delivered": inter.get("decision") in DELIVERED,
        "code_shown": shown is not None, "shown_is_unapproved_reply": inter.get("code_output") is None and shown is not None,
        "shown_class": s["class"] if shown else "nothing_shown", "shown_reasons": s["reasons"] if shown else [],
        "shown_a_reasons": (s.get("a_reasons") or []) if shown else [],
        "shown_b_reasons": (s.get("b_reasons") or []) if shown else [],
        "shown_behaviour": s.get("behaviour") if shown else None,
        "final_class": f["class"], "final_reasons": f["reasons"], "first_class": first["class"],
        "ewcs": inter.get("ewcs"), "correction_attempted": inter.get("correction_attempted"),
        "correction_allowed": inter.get("correction_allowed"), "protocol_notes": inter.get("protocol_notes") or [],
        "cost": {"baseline": {k: base.get(k) for k in ("duration_seconds", "model_seconds", "prompt_tokens", "completion_tokens",
                                                       "gpu_energy_j", "cpu_energy_j", "measured_energy_j")},
                 "intervention": {k: inter.get(k) for k in ("duration_seconds", "model_seconds", "tool_seconds", "prompt_tokens",
                                                            "completion_tokens", "gpu_energy_j", "cpu_energy_j", "measured_energy_j")}},
        "codes": {"baseline": base.get("code"), "shown": shown, "final": inter.get("final_candidate")},
    }


# Kinds of task-fidelity error (class B): a valid API call that is not the task's.
TASK_ERROR_TYPES = [
    ("different declared endpoint", ("a different declared endpoint",)),
    ("method not acceptable for the task", ("is not acceptable for this task",)),
    ("omitted parameter the task specifies", ("omits query parameter",)),
    ("different parameter value", (", the task needs ",)),
    ("omitted request body", ("omits the request body",)),
    ("unrequested request body", ("sends a body the task does not ask for",)),
    ("request body differs (fields or values)", ("differs from the task's",)),
    ("extra requests", ("requests; the task needs one",)),
    ("credential missing or malformed (API requirement unknown)", ("credential", "Authorization is")),
    ("JSON body sent as form data", ("sends the JSON body as data=",)),
    ("insecure scheme (http)", ("instead of https",)),
]
# Kinds of runtime failure: the code makes no request.
RUNTIME_FAILURE_TYPES = [
    ("input used as the wrong type (e.g. credential string as a dict)", ("'str' object has no attribute", "string indices must be integers",
                                                                          "'NoneType' object is not a mapping")),
    ("reads an input the task does not provide", ("KeyError",)),
    ("syntax error", ("SyntaxError", "IndentationError")),
    ("makes no request", ("never calls the API",)),
    ("does not finish (timeout)", ("Timeout",)),
    ("blocked operation (file, network or process)", ("PermissionError",)),
    ("undefined name", ("NameError", "UnboundLocalError")),
    ("raises its own error before the request", ("ValueError", "Exception:", "RuntimeError")),
    ("wrong call or argument types", ("TypeError", "AttributeError")),
]


def kinds_of(reasons: list, table: list) -> set:
    """Kinds named by a list of reasons, per table (first match per reason)."""
    return {next((name for name, needles in table if any(n in reason for n in needles)), "other") for reason in reasons}


def task_error_types(reasons: list) -> set:
    return kinds_of([r for r in reasons if not r.startswith("no request matches")], TASK_ERROR_TYPES)


def runtime_failure_type(reasons: list) -> str:
    return next(iter(kinds_of(reasons[:1], RUNTIME_FAILURE_TYPES)), "other") if reasons else "other"


def hallucination_types(reasons: list) -> set:
    """The kinds of hallucination in a class-A candidate's reasons (first matching kind per reason)."""
    kinds = set()
    for reason in reasons:
        kinds.add(next((name for name, needles in HALLUCINATION_TYPES if any(n in reason for n in needles)), "other"))
    return kinds


def event(cls: str, which: str, undetermined_as: str | None = None) -> int | None:
    """Did an error of this kind reach the user? None when undecided."""
    if cls == "undetermined":
        if undetermined_as is None:
            return None
        cls = undetermined_as
    bad = {"primary": ("A",), "secondary": ("A", "B"), "any": ("A", "B", "runtime_failure")}[which]
    return int(cls in bad)


def comparison(records: list, which: str, include_pilot: bool, undetermined_as: str | None, resamples: int, seed: int) -> dict:
    pairs, clusters, excluded = [], [], 0
    for r in records:
        if r["pilot"] and not include_pilot:
            continue
        b = event(r["baseline_class"], which, undetermined_as)
        i = 0 if r["shown_class"] == "nothing_shown" else event(r["shown_class"], which, undetermined_as)
        if b is None or i is None:
            excluded += 1
            continue
        pairs.append((b, i))
        clusters.append(r["family"])
    n = len(pairs)
    bc = sum(1 for b, i in pairs if b and not i)
    cb = sum(1 for b, i in pairs if i and not b)
    base_rate = sum(b for b, _ in pairs) / n if n else float("nan")
    int_rate = sum(i for _, i in pairs) / n if n else float("nan")
    return {"tasks": n, "excluded_undetermined": excluded, "baseline_rate": base_rate, "intervention_rate": int_rate,
            "difference": stats.paired_difference(pairs), "discordant_baseline_only": bc, "discordant_intervention_only": cb,
            "mcnemar_p": stats.mcnemar_exact(bc, cb),
            "ci_tasks": stats.bootstrap_ci(pairs, None, resamples, seed),
            "ci_families": stats.bootstrap_ci(pairs, clusters, resamples, seed),
            "families": len(set(clusters))}


def analyse(label: str, records: list, resamples: int, seed: int) -> dict:
    out = {"label": label, "tasks": len(records)}
    out["primary"] = comparison(records, "primary", False, None, resamples, seed)
    out["sensitivity"] = {
        "undetermined_as_hallucination": comparison(records, "primary", False, "A", resamples, seed),
        "undetermined_as_correct": comparison(records, "primary", False, "correct", resamples, seed),
        "including_pilot": comparison(records, "primary", True, None, resamples, seed)}
    out["secondary"] = comparison(records, "secondary", False, None, resamples, seed)
    out["any_error"] = comparison(records, "any", False, None, resamples, seed)
    main = [r for r in records if not r["pilot"]]
    out["baseline_classes"] = dict(Counter(r["baseline_class"] for r in main))
    # Tasks with each kind of hallucination in the code reaching the user (a task can have several).
    out["hallucination_types"] = {
        mode: dict(Counter(k for r in main if r[cls] == "A" for k in hallucination_types(r[reasons])))
        for mode, cls, reasons in (("baseline", "baseline_class", "baseline_a_reasons"), ("intervention_shown", "shown_class", "shown_a_reasons"))}
    wrong_host = "wrong host, version or base path"
    out["primary_excluding_wrong_host"] = {
        mode: sum(1 for r in main if r[cls] == "A" and hallucination_types(r[reasons]) - {wrong_host})
        for mode, cls, reasons in (("baseline", "baseline_class", "baseline_a_reasons"), ("intervention_shown", "shown_class", "shown_a_reasons"))}
    out["shown_classes"] = dict(Counter(r["shown_class"] for r in main))
    out["final_classes"] = dict(Counter(r["final_class"] for r in main))
    # Intervention confusion matrix: the final verified candidate against what the tool decided.
    matrix = Counter((r["final_class"], "delivered" if r["delivered"] else "withheld") for r in main)
    out["confusion"] = {f"{c}|{d}": n for (c, d), n in matrix.items()}
    out["incorrect_rejection"] = sum(1 for r in main if not r["delivered"] and r["final_class"] == "correct")
    out["incorrect_acceptance_primary"] = sum(1 for r in main if r["shown_class"] == "A")
    out["unapproved_code_shown"] = sum(1 for r in main if r["shown_is_unapproved_reply"])
    # EWCS calibration on the final candidate.
    good = [r["ewcs"] for r in main if r["final_class"] == "correct" and isinstance(r["ewcs"], (int, float))]
    bad = [r["ewcs"] for r in main if r["final_class"] == "A" and isinstance(r["ewcs"], (int, float))]
    bands = defaultdict(lambda: [0, 0])
    for r in main:
        if isinstance(r["ewcs"], (int, float)) and r["final_class"] in ("correct", "A", "B"):
            band = "<0.60" if r["ewcs"] < 0.6 else "0.60-0.85" if r["ewcs"] < 0.85 else ">=0.85"
            bands[band][r["final_class"] == "correct"] += 1
    out["ewcs"] = {"auc_correct_vs_A": stats.auc(good, bad), "correct_n": len(good), "A_n": len(bad),
                   "share_correct_by_band": {b: {"correct": ok, "total": ok + no} for b, (no, ok) in sorted(bands.items())}}
    # Corrections
    corrected = [r for r in main if r["correction_attempted"]]
    out["corrections"] = {"attempted": len(corrected), "allowed": sum(1 for r in corrected if r["correction_allowed"]),
                          "transitions": dict(Counter(f"{r['first_class']}->{r['final_class']}" for r in corrected))}
    out["protocol_notes"] = dict(Counter(n for r in main for n in r["protocol_notes"]))
    # Behaviour (secondary): of candidates that ran, the share meeting each requirement.
    for mode, key in (("baseline", "baseline_behaviour"), ("intervention_shown", "shown_behaviour")):
        rows = [r[key] for r in main if r.get(key)]
        out.setdefault("behaviour", {})[mode] = {k: {"ok": sum(1 for b in rows if b.get(k)), "of": len(rows)}
                                                 for k in ("returns_expected_value", "empty_response_ok", "error_raises")}
    out["by_api"] = {}
    for api in sorted({r["api"] for r in main}):
        rows = [r for r in main if r["api"] == api]
        out["by_api"][api] = {"tasks": len(rows),
                              "baseline_A": sum(r["baseline_class"] == "A" for r in rows),
                              "intervention_A_shown": sum(r["shown_class"] == "A" for r in rows),
                              "baseline_undetermined": sum(r["baseline_class"] == "undetermined" for r in rows),
                              "intervention_undetermined": sum(r["shown_class"] == "undetermined" for r in rows),
                              "delivered": sum(r["delivered"] for r in rows)}
    out["cost"] = {}
    for mode in ("baseline", "intervention"):
        values = defaultdict(list)
        for r in main:
            for k, v in (r["cost"][mode] or {}).items():
                if isinstance(v, (int, float)):
                    values[k].append(v)
        out["cost"][mode] = {k: {"mean": statistics.mean(v), "median": statistics.median(v), "total": sum(v), "n": len(v)}
                             for k, v in values.items()}
    return out


def write_review_files(label: str, records: list, out_dir: Path, seed: int) -> dict:
    """Undetermined candidates for manual review (plan §4), and the audit sample (plan §5)."""
    review_dir = out_dir / "review_code"
    review_dir.mkdir(parents=True, exist_ok=True)
    fields = ["label", "task_id", "role", "code_sha256", "automatic_class", "automatic_reasons", "code_file",
              "reviewer_1_class", "reviewer_2_class", "agreed_class", "notes"]
    queue, seen = [], set()
    for r in records:
        for role, cls_key, reasons_key in (("baseline", "baseline_class", "baseline_reasons"),
                                            ("shown", "shown_class", "shown_reasons"), ("final", "final_class", "final_reasons")):
            code = r["codes"]["baseline" if role == "baseline" else role]
            if r[cls_key] != "undetermined" or not code or (r["task_id"], code_hash(code)) in seen:
                continue
            seen.add((r["task_id"], code_hash(code)))
            file = review_dir / f"{r['task_id']}__{role}.py"
            file.write_text(code, encoding="utf-8", newline="")
            queue.append({"label": label, "task_id": r["task_id"], "role": role, "code_sha256": code_hash(code),
                          "automatic_class": "undetermined", "automatic_reasons": " | ".join(r[reasons_key])[:1000],
                          "code_file": str(file.relative_to(out_dir))})
    with (out_dir / "review_queue.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(queue)
    rng = random.Random(seed)
    audit = []
    for role, cls_key, reasons_key in (("baseline", "baseline_class", "baseline_reasons"), ("shown", "shown_class", "shown_reasons")):
        by_api = defaultdict(list)
        for r in records:
            if r[cls_key] in DECIDED and r["codes"]["baseline" if role == "baseline" else role]:
                by_api[r["api"]].append(r)
        total = sum(len(v) for v in by_api.values())
        for api, rows in sorted(by_api.items()):
            k = max(1, round(50 * len(rows) / total)) if total else 0
            for r in rng.sample(rows, min(k, len(rows))):
                code = r["codes"]["baseline" if role == "baseline" else role]
                file = review_dir / f"audit__{r['task_id']}__{role}.py"
                file.write_text(code, encoding="utf-8", newline="")
                audit.append({"label": label, "task_id": r["task_id"], "role": role, "code_sha256": code_hash(code),
                              "automatic_class": r[cls_key], "automatic_reasons": " | ".join(r[reasons_key])[:1000],
                              "code_file": str(file.relative_to(out_dir))})
    with (out_dir / "audit_sample.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(audit)
    return {"review_queue": len(queue), "audit_sample": len(audit)}


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    p = argparse.ArgumentParser(description="Evaluate Benchmark: scores the Confident Agent Benchmark's results")
    p.add_argument("--benchmark", type=Path, default=REPO / "Benchmark")
    p.add_argument("--dataset", type=Path, default=TASKS_DEFAULT)
    p.add_argument("--labels", default=None, help="comma-separated model labels (default: every label in both modes)")
    p.add_argument("--out", type=Path, default=ROOT / "results")
    p.add_argument("--reviews", type=Path, default=ROOT / "reviews" / "reviews.csv")
    p.add_argument("--jobs", type=int, default=8)
    p.add_argument("--timeout", type=float, default=10.0, help="seconds per sandboxed run")
    p.add_argument("--bootstrap", type=int, default=10000)
    p.add_argument("--seed", type=int, default=301)
    p.add_argument("--self-check-only", action="store_true")
    p.add_argument("--force", action="store_true", help="score even if the self-check fails")
    args = p.parse_args()

    tasks = load_jsonl(args.dataset)
    sha = content_sha256(args.dataset)
    if sha != TASKS_SHA256:
        print(f"[warning] the task file's SHA-256 ({sha[:12]}…) differs from the plan's ({TASKS_SHA256[:12]}…); "
              "record the answer-key change in EVALUATION_PLAN.md", flush=True)
    by_id = {t["task_id"]: t for t in tasks}
    contexts, source_problems = build_contexts(tasks)
    for problem in source_problems:
        print(f"[warning] {problem}", flush=True)
    evaluator = Evaluator(contexts, args.jobs, args.timeout)
    args.out.mkdir(parents=True, exist_ok=True)

    print("[self-check] scoring the dataset's reference solutions ...", flush=True)
    check = self_check(evaluator, tasks)
    (args.out / "self_check.json").write_text(json.dumps(check, indent=2), encoding="utf-8")
    print(f"[self-check] {check['correct']}/{check['references']} correct, behaviour ok for {check['behaviour_all_ok']}", flush=True)
    if check["failures"] and not args.force:
        sys.exit("Self-check failed: some reference solutions are not scored correct (see self_check.json). "
                 "Fix the evaluator or the answer key first, or use --force.")
    if args.self_check_only:
        return

    base_rows, inter_rows = load_jsonl(args.benchmark / "complete_test_baseline.jsonl"), \
        load_jsonl(args.benchmark / "complete_test_intervention.jsonl")
    labels = sorted({r["model_label"] for r in base_rows} & {r["model_label"] for r in inter_rows})
    if args.labels:
        labels = [l for l in (x.strip() for x in args.labels.split(",")) if l in labels]
    if not labels:
        sys.exit("No model label has results in both modes.")
    pilot = {json.loads(l)["task_id"] for l in (args.benchmark / "dataset" / "rest_api_prompts_pilot.jsonl")
             .read_text(encoding="utf-8").splitlines() if l.strip()}
    reviews = load_reviews(args.reviews)
    analyses = {}
    for label in labels:
        base = {r["prompt_id"]: r for r in base_rows if r["model_label"] == label}
        inter = {r["prompt_id"]: r for r in inter_rows if r["model_label"] == label}
        ids = sorted(set(base) & set(inter) & set(by_id))
        print(f"[{label}] {len(ids)} paired tasks; classifying candidates ...", flush=True)
        items = [(t, c) for t in ids for c in (base[t].get("code"), inter[t].get("code_output"), inter[t].get("reply_code"),
                                               inter[t].get("final_candidate"), inter[t].get("first_candidate"))]
        evaluator.run_all(items)
        records = [task_record(by_id[t], base[t], inter[t], evaluator, reviews, pilot) for t in ids]
        out_dir = args.out / label
        out_dir.mkdir(parents=True, exist_ok=True)
        analysis = analyse(label, records, args.bootstrap, args.seed)
        analysis["review_files"] = write_review_files(label, records, out_dir, args.seed)
        with (out_dir / "per_task.jsonl").open("w", encoding="utf-8", newline="") as f:
            for r in records:
                f.write(json.dumps({k: v for k, v in r.items() if k != "codes"}, ensure_ascii=False) + "\n")
        (out_dir / "evaluation.json").write_text(json.dumps(analysis, indent=2, default=str), encoding="utf-8")
        analyses[label] = analysis
        print(f"[{label}] hallucination reaching the user: baseline {analysis['primary']['baseline_rate']:.3f}, "
              f"intervention {analysis['primary']['intervention_rate']:.3f} (McNemar p={analysis['primary']['mcnemar_p']:.3g})", flush=True)
    adjusted = stats.holm({l: a["primary"]["mcnemar_p"] for l, a in analyses.items()})
    for label, a in analyses.items():
        a["primary"]["mcnemar_p_holm"] = adjusted[label]
        (args.out / label / "evaluation.json").write_text(json.dumps(a, indent=2, default=str), encoding="utf-8")
    meta = {"evaluator_version": EVALUATOR_VERSION, "evaluated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "task_file_sha256": sha, "task_file_matches_plan": sha == TASKS_SHA256, "self_check": {k: v for k, v in check.items() if k != "failures"},
            "reviews_file": (str(args.reviews.relative_to(ROOT)) if args.reviews.is_relative_to(ROOT) else str(args.reviews))
            if args.reviews.exists() and len(load_reviews(args.reviews)) else None, "bootstrap_resamples": args.bootstrap, "seed": args.seed}
    write_report(args.out / "report.md", analyses, meta)
    print(f"Report: {args.out / 'report.md'}")


if __name__ == "__main__":
    main()
