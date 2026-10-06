"""Markdown report of an evaluation."""
from __future__ import annotations

from pathlib import Path


def pct(x) -> str:
    return "n/a" if x is None or x != x else f"{100 * x:.1f}%"


def pp(x) -> str:
    return "n/a" if x is None or x != x else f"{100 * x:+.1f} pp"


def ci(interval) -> str:
    lo, hi = interval
    return "n/a" if lo != lo else f"[{100 * lo:+.1f}, {100 * hi:+.1f}] pp"


def pval(p) -> str:
    return "n/a" if p is None else ("< 0.0001" if p < 1e-4 else f"{p:.4f}")


def comparison_row(name: str, c: dict) -> str:
    return (f"| {name} | {c['tasks']} | {pct(c['baseline_rate'])} | {pct(c['intervention_rate'])} | {pp(c['difference'])} | "
            f"{ci(c['ci_tasks'])} | {ci(c['ci_families'])} | {c['discordant_baseline_only']} / {c['discordant_intervention_only']} | "
            f"{pval(c['mcnemar_p'])} |")


def write_report(path: Path, analyses: dict, meta: dict) -> None:
    lines = ["# Evaluation report", "",
             f"Evaluator {meta['evaluator_version']}, {meta['evaluated']}. Rules: `Benchmark/EVALUATION_PLAN.md`.", "",
             f"- Answer key: task file SHA-256 `{meta['task_file_sha256'][:16]}…` "
             f"({'matches the plan' if meta['task_file_matches_plan'] else '**differs from the plan: log the change**'}).",
             f"- Self-check: {meta['self_check']['correct']}/{meta['self_check']['references']} reference solutions scored "
             f"correct; behaviour requirements met by {meta['self_check']['behaviour_all_ok']}.",
             f"- Manual reviews applied from: {meta['reviews_file'] or 'none yet (undetermined candidates are excluded from the primary result)'}.",
             f"- Intervals: {meta['bootstrap_resamples']} bootstrap resamples (seed {meta['seed']}), over tasks and over operation families.",
             ""]
    for label, a in analyses.items():
        p = a["primary"]
        run = a.get("run") or {}
        role = (f"{run.get('role', 'unknown')} run ({run.get('role_reason', '')})"
                + ("" if run.get("label_matches_quantization", True) else
                   f"; **the label does not match the quantization LM Studio reported ({run.get('quantization')})**"))
        lines += [f"## {label}", "", f"Quantization {run.get('quantization', 'n/a')}, benchmark {run.get('benchmark_version', 'n/a')}, "
                  f"GPU {run.get('machine_gpu') or 'n/a'}: {role}.", "",
                  "### Unacceptable hallucinations reaching the user (primary, plan §3)", "",
                  "Rate = share of tasks whose code reaching the user is class A (API hallucination). "
                  "Baseline: the code block; intervention: the delivered code, or code shown in the reply. "
                  "Pilot tasks excluded; difference = baseline − intervention; discordant = baseline-only / intervention-only.", "",
                  "| Comparison | Tasks | Baseline | Intervention | Difference | 95% CI (tasks) | 95% CI (families) | Discordant | McNemar p |",
                  "|---|---:|---:|---:|---:|---|---|---|---:|",
                  comparison_row("**Primary** (undetermined excluded)", p),
                  comparison_row("Undetermined counted as hallucination", a["sensitivity"]["undetermined_as_hallucination"]),
                  comparison_row("Undetermined counted as correct", a["sensitivity"]["undetermined_as_correct"]),
                  comparison_row("Including pilot tasks", a["sensitivity"]["including_pilot"]),
                  comparison_row("A or B (secondary)", a["secondary"]),
                  comparison_row("A, B or runtime failure", a["any_error"]),
                  "", (f"Holm-adjusted McNemar p across the main runs: {pval(p.get('mcnemar_p_holm'))}. " if p.get("mcnemar_p_holm") is not None
                       else "Not in the Holm family (preliminary run): the p-value above is uncorrected. ") +
                      f"Undetermined pairs excluded from the primary row: {p['excluded_undetermined']}. "
                      f"Operation families: {p['families']}.", ""]
        classes = sorted(set(a["baseline_classes"]) | set(a["shown_classes"]) | set(a["final_classes"]))
        lines += ["### Classes (pilot excluded)", "", "| Class | Baseline code | Intervention: shown to user | Intervention: final candidate |",
                  "|---|---:|---:|---:|"]
        lines += [f"| {c} | {a['baseline_classes'].get(c, 0)} | {a['shown_classes'].get(c, 0)} | {a['final_classes'].get(c, 0)} |" for c in classes]
        ht = a["hallucination_types"]
        lines += ["", "### Kinds of API hallucination reaching the user (tasks; a task can have several)", "",
                  "| Kind | Baseline | Intervention |", "|---|---:|---:|"]
        for kind in sorted(set(ht["baseline"]) | set(ht["intervention_shown"]), key=lambda k: -ht["baseline"].get(k, 0)):
            lines.append(f"| {kind} | {ht['baseline'].get(kind, 0)} | {ht['intervention_shown'].get(kind, 0)} |")
        ex = a["primary_excluding_wrong_host"]
        lines += ["", f"Tasks with a hallucination other than a wrong host, version or base path: baseline {ex['baseline']}, "
                      f"intervention {ex['intervention_shown']}. The intervention prompt names the current hosts (by design, "
                      "Benchmark README), so this row separates that context from what verification catches.", ""]
        conf = a["confusion"]
        lines += ["", "### Intervention decisions against the final candidate's class", "",
                  "| Final candidate | Delivered | Withheld |", "|---|---:|---:|"]
        for c in sorted({k.split('|')[0] for k in conf}):
            lines.append(f"| {c} | {conf.get(c + '|delivered', 0)} | {conf.get(c + '|withheld', 0)} |")
        lines += ["", f"- Incorrect acceptance (class A shown to the user): {a['incorrect_acceptance_primary']}",
                  f"- Incorrect rejection (correct final candidate withheld): {a['incorrect_rejection']}",
                  f"- Code shown in a reply without the tool's approval: {a['unapproved_code_shown']}", ""]
        e = a["ewcs"]
        auc_text = "n/a" if e["auc_correct_vs_A"] is None else f"{e['auc_correct_vs_A']:.3f}"
        lines += ["### Confidence metric (EWCS of the final candidate)", "",
                  f"AUC, correct vs class A: {auc_text} "
                  f"(correct n={e['correct_n']}, A n={e['A_n']}).", "", "| EWCS band | Correct | Of decided (correct, A, B) |", "|---|---:|---:|"]
        lines += [f"| {band} | {v['correct']} | {v['total']} |" for band, v in e["share_correct_by_band"].items()]
        c = a["corrections"]
        lines += ["", "### Corrections", "", f"Attempted {c['attempted']} (allowed by the prompt: {c['allowed']}).", "",
                  "| First candidate → final | Tasks |", "|---|---:|"]
        lines += [f"| {k} | {v} |" for k, v in sorted(c["transitions"].items(), key=lambda kv: -kv[1])]
        lines += ["", "### Agent protocol notes", "", "| Note | Tasks |", "|---|---:|"]
        lines += [f"| {k} | {v} |" for k, v in sorted(a["protocol_notes"].items(), key=lambda kv: -kv[1])]
        lines += ["", "### Task behaviour (secondary)", "", "| Requirement | Baseline | Intervention (shown) |", "|---|---:|---:|"]
        for req in ("returns_expected_value", "empty_response_ok", "error_raises"):
            b, i = a["behaviour"]["baseline"][req], a["behaviour"]["intervention_shown"][req]
            lines.append(f"| {req.replace('_', ' ')} | {b['ok']}/{b['of']} | {i['ok']}/{i['of']} |")
        lines += ["", "### By API", "", "| API | Tasks | Baseline A | Intervention A shown | Delivered | Undetermined (baseline / shown) |",
                  "|---|---:|---:|---:|---:|---|"]
        lines += [f"| {api} | {v['tasks']} | {v['baseline_A']} | {v['intervention_A_shown']} | {v['delivered']} | "
                  f"{v['baseline_undetermined']} / {v['intervention_undetermined']} |" for api, v in a["by_api"].items()]
        lines += ["", "### Cost per task (plan §3, project description §4.8)", "", "| Measure | Baseline mean | Intervention mean | Ratio |", "|---|---:|---:|---:|"]
        for k in sorted(set(a["cost"]["baseline"]) | set(a["cost"]["intervention"])):
            b, i = a["cost"]["baseline"].get(k), a["cost"]["intervention"].get(k)
            ratio = f"{i['mean'] / b['mean']:.1f}x" if b and i and b["mean"] else "n/a"
            lines.append(f"| {k} | {b['mean']:.1f} | {i['mean']:.1f} | {ratio} |" if b and i else
                         f"| {k} | {b['mean']:.1f} | n/a | n/a |" if b else f"| {k} | n/a | {i['mean']:.1f} | n/a |")
        if not a["cost"]["baseline"] and not a["cost"]["intervention"]:
            lines.append("| (not recorded in this run) | | | |")
        rf = a["review_files"]
        lines += ["", f"Manual review: {rf['review_queue']} undetermined candidates in `{label}/review_queue.csv`; "
                      f"audit sample of {rf['audit_sample']} in `{label}/audit_sample.csv` (plan §4–5).", ""]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="")
