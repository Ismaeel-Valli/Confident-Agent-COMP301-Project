"""Report figures and tables that tempstats does not already provide.

Reads only finished data:
  ../../Unprocessed Data/            evaluator and stats-compiler output (main runs)
  ../../../Benchmark/Completed Runs/ the zipped runs (stored verification results)
  the dataset's task file             expected requests (answer key)
and writes  charts/R*.png  and  tables/R*.csv  next to this file.

  R01 primary and secondary effects with task and operation-family intervals
  R02 what happens to each baseline outcome under the Confident Agent (alluvial)
  R03 which API version the baseline model reached for (training-data staleness)
  R04 sensitivity of decisions to the EWCS weights, thresholds and uncertainty gate
  R05 agent protocol deviations
  R06 the pilot (Practical Three) verdicts, reconciled

Run:  python -X utf8 build_report_figures.py      (pandas, numpy, matplotlib)
"""
from __future__ import annotations

import json
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, PathPatch, Rectangle
from matplotlib.path import Path as MPath

HERE = Path(__file__).resolve().parent
ANALYSIS = HERE.parents[1]                      # Findings/Statistical Analysis
RAW = ANALYSIS / "Unprocessed Data"
FINDINGS = ANALYSIS.parent
RUNS = FINDINGS / "Benchmark" / "Completed Runs"
TASKS = (FINDINGS.parent / "Code Submission" / "COMP301-Dataset-Builder" / "comp301-dataset-builder"
         / "output" / "rest_api_tasks_v1_DRAFT.jsonl")
CH, TB = HERE / "charts", HERE / "tables"
CH.mkdir(exist_ok=True)
TB.mkdir(exist_ok=True)

LABELS = {"Q4_K_M": "Qwen3.5-9B-Q4_KM-full-Latest", "Q6_K": "QQwen3.5-9B-Q6_K-full-Latest", "Q8_0": "Qwen3.5-9B-Q8_0-full-Latest"}
FOLDERS = {"Q4_K_M": "Qwen3.5-9B-Q4_K_M", "Q6_K": "Qwen3.5-9B-Q6_K", "Q8_0": "Qwen3.5-9B-Q8_0"}
QS = list(LABELS)

# palette and style shared with build_tempstats.py (validated categorical pairs)
BASE, CA = "#2a78d6", "#eb6834"
QC = {"Q4_K_M": "#1baf7a", "Q6_K": "#6250d6", "Q8_0": "#e87ba4"}
INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
CLS = {"correct": "#2a78d6", "A": "#d03b3b", "B": "#e8a200", "crash": "#7a7974", "withheld": "#c4c2bb"}
SOURCE = ("Source: Findings/Statistical Analysis/Unprocessed Data (main runs, 990 scored tasks per quantization, "
          "pilot excluded) | Qwen3.5-9B, AMD RX 9070 XT + Ryzen 7 5700X3D")
plt.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
    "font.family": "DejaVu Sans", "font.size": 10.5, "text.color": INK,
    "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": GRID,
    "grid.linewidth": 0.7, "axes.axisbelow": True, "legend.frameon": False,
})


def title(fig, text, sub):
    fig.text(0.012, 0.985, text, fontsize=17, fontweight="bold", va="top", color=INK)
    fig.text(0.012, 0.925, sub, fontsize=10.5, va="top", color=INK2)


def footer(fig, extra=""):
    fig.text(0.012, 0.012, SOURCE + (("\n" + extra) if extra else ""), fontsize=8, color=MUTED, va="bottom")


def save(fig, name):
    fig.savefig(CH / name, dpi=220)
    plt.close(fig)
    print("wrote", name)


def per_task(q):
    rows = [json.loads(l) for l in (RAW / "evaluation" / LABELS[q] / "per_task.jsonl").open(encoding="utf-8")]
    return [r for r in rows if not r["pilot"]]


def evaluation(q):
    return json.loads((RAW / "evaluation" / LABELS[q] / "evaluation.json").read_text(encoding="utf-8"))


TASK = {t["task_id"]: t for t in map(json.loads, TASKS.open(encoding="utf-8"))}
PROMPTS = pd.read_csv(RAW / "stats" / "combined" / "prompt_stats.csv")
PROMPTS = PROMPTS[(PROMPTS.run_role == "main") & (PROMPTS.pilot == 0)]


# --------------------------------------------------------------------------- R01 effects
def paired_ci(b, i, families, reps=10000, seed=301):
    """Difference baseline - intervention with percentile intervals over tasks and over operation families."""
    rng = np.random.default_rng(seed)
    b, i = np.asarray(b, float), np.asarray(i, float)
    d = b - i
    n = len(d)
    boot = d[rng.integers(0, n, (reps, n))].mean(axis=1)
    fam = pd.Series(d).groupby(np.asarray(families))
    sums, counts = fam.sum().to_numpy(), fam.count().to_numpy()
    idx = rng.integers(0, len(sums), (reps, len(sums)))
    cboot = sums[idx].sum(axis=1) / counts[idx].sum(axis=1)
    return d.mean(), np.percentile(boot, [2.5, 97.5]), np.percentile(cboot, [2.5, 97.5])


def r01():
    rows = []
    for q in QS:
        ev = evaluation(q)
        for key, name in (("primary", "Hallucination (class A) reaching the user"),
                          ("secondary", "Class A or B reaching the user"),
                          ("any_error", "Any error (A, B or runtime failure)")):
            e = ev[key]
            rows.append({"quantization": q, "outcome": name, "baseline": e["baseline_rate"],
                         "intervention": e["intervention_rate"], "difference": -e["difference"],
                         "ci_tasks_low": -e["ci_tasks"][1], "ci_tasks_high": -e["ci_tasks"][0],
                         "ci_families_low": -e["ci_families"][1], "ci_families_high": -e["ci_families"][0],
                         "mcnemar_p": e["mcnemar_p"], "discordant": f"{e['discordant_baseline_only']} / {e['discordant_intervention_only']}"})
        p = PROMPTS[PROMPTS.quantization == q]
        bc, ic = p.b_correct.fillna(0).to_numpy(), p.i_correct_reaches_user.fillna(0).to_numpy()
        mean, ci_t, ci_f = paired_ci(ic, bc, p.operation_family)   # gain: intervention - baseline
        better, worse = int(((ic == 1) & (bc == 0)).sum()), int(((ic == 0) & (bc == 1)).sum())
        from math import comb
        k, n = min(better, worse), better + worse
        pval = min(1.0, 2 * sum(comb(n, j) for j in range(k + 1)) / 2 ** n) if n else 1.0
        rows.append({"quantization": q, "outcome": "Correct code reaching the user", "baseline": bc.mean(),
                     "intervention": ic.mean(), "difference": mean, "ci_tasks_low": ci_t[0], "ci_tasks_high": ci_t[1],
                     "ci_families_low": ci_f[0], "ci_families_high": ci_f[1], "mcnemar_p": pval,
                     "discordant": f"{better} / {worse}"})
    df = pd.DataFrame(rows)
    df.to_csv(TB / "R01_effects.csv", index=False)

    outcomes = list(dict.fromkeys(df.outcome))
    fig, ax = plt.subplots(figsize=(12.5, 6.2))
    fig.subplots_adjust(left=0.27, right=0.97, top=0.80, bottom=0.17)
    y = 0
    yt, yl = [], []
    for o in outcomes:
        for k, q in enumerate(QS):
            r = df[(df.outcome == o) & (df.quantization == q)].iloc[0]
            yy = y + k * 0.28
            ax.plot([r.ci_families_low * 100, r.ci_families_high * 100], [yy, yy], color=QC[q], lw=1.4, alpha=0.55)
            ax.plot([r.ci_tasks_low * 100, r.ci_tasks_high * 100], [yy, yy], color=QC[q], lw=5, solid_capstyle="round")
            ax.plot(r.difference * 100, yy, "o", ms=8, color=QC[q], mec=SURF, mew=1.5, zorder=3)
            ax.text(r.ci_families_high * 100 + 1.2, yy, f"{r.difference*100:+.1f} pp", va="center", fontsize=8.5, color=INK2)
        yt.append(y + 0.28)
        yl.append(o)
        y += 1.35
    ax.axvline(0, color=INK2, lw=1)
    ax.set_yticks(yt, yl)
    ax.invert_yaxis()
    ax.set_xlabel("Change, Confident Agent minus baseline (percentage points)")
    ax.set_xlim(-75, 50)
    handles = [plt.Line2D([], [], color=QC[q], marker="o", lw=5, label=q) for q in QS]
    handles += [plt.Line2D([], [], color=MUTED, lw=5, label="95% CI over tasks"),
                plt.Line2D([], [], color=MUTED, lw=1.4, alpha=0.6, label="95% CI over operation families")]
    ax.legend(handles=handles, loc="upper right", fontsize=9, ncol=1)
    title(fig, "Every outcome moves in the intended direction, in every run",
          "Paired differences per task (10,000 bootstrap resamples). Thick bar: interval over tasks; thin bar: over the 141 operation "
          "families,\nwhich allows for related prompts. Exact McNemar p < 1e-19 for every row (Holm-adjusted for the primary row).")
    footer(fig)
    save(fig, "R01_effects_forest.png")
    return df


# --------------------------------------------------------------------------- R02 alluvial
def bucket_baseline(c):
    return {"correct": "correct", "A": "A", "B": "B"}.get(c, "crash")


def bucket_shown(c):
    return {"correct": "correct", "A": "A", "B": "B", "nothing_shown": "withheld"}.get(c, "crash")


def band(ax, x0, x1, y0a, y0b, y1a, y1b, color, alpha=0.42):
    """A smooth ribbon from [y0a, y0b] at x0 to [y1a, y1b] at x1."""
    xm = (x0 + x1) / 2
    verts = [(x0, y0a), (xm, y0a), (xm, y1a), (x1, y1a), (x1, y1b), (xm, y1b), (xm, y0b), (x0, y0b), (x0, y0a)]
    codes = [MPath.MOVETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4, MPath.LINETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4, MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(verts, codes), facecolor=color, edgecolor="none", alpha=alpha))


def r02():
    flows = Counter()
    for q in QS:
        for r in per_task(q):
            flows[(bucket_baseline(r["baseline_class"]), bucket_shown(r["shown_class"]))] += 1
    total = sum(flows.values())
    left_order = ["correct", "B", "A", "crash"]
    right_order = ["correct", "B", "A", "crash", "withheld"]
    names = {"correct": "Correct", "A": "API hallucination (A)", "B": "Valid call, wrong task (B)",
             "crash": "Crash / no request", "withheld": "Withheld (nothing shown)"}
    pd.DataFrame([{"baseline": a, "confident_agent": b, "tasks": n} for (a, b), n in sorted(flows.items())]).to_csv(TB / "R02_flows.csv", index=False)

    fig, ax = plt.subplots(figsize=(12.5, 7.2))
    fig.subplots_adjust(left=0.03, right=0.97, top=0.84, bottom=0.08)
    ax.axis("off")
    gap = 0.012
    xL, xR, w = 0.20, 0.70, 0.035
    lefts = {k: sum(v for (a, _), v in flows.items() if a == k) / total for k in left_order}
    rights = {k: sum(v for (_, b), v in flows.items() if b == k) / total for k in right_order}

    def stack(sizes, order):
        pos, y = {}, 1.0
        for k in order:
            pos[k] = [y - sizes[k], y]
            y -= sizes[k] + gap
        return pos
    lp, rp = stack(lefts, left_order), stack(rights, right_order)
    lcur = {k: lp[k][1] for k in left_order}
    rcur = {k: rp[k][1] for k in right_order}
    for a in left_order:
        for b in right_order:
            v = flows.get((a, b), 0) / total
            if not v:
                continue
            band(ax, xL + w, xR, lcur[a], lcur[a] - v, rcur[b], rcur[b] - v, CLS[b] if b != "withheld" else CLS["A"] if a == "A" else "#9a988f",
                 alpha=0.45 if b != "withheld" else 0.30)
            lcur[a] -= v
            rcur[b] -= v
    for k in left_order:
        ax.add_patch(Rectangle((xL, lp[k][0]), w, lp[k][1] - lp[k][0], color=CLS[k]))
        n = sum(v for (a, _), v in flows.items() if a == k)
        ax.text(xL - 0.01, (lp[k][0] + lp[k][1]) / 2, f"{names[k]}\n{n:,} ({n/total:.0%})", ha="right", va="center", fontsize=10)
    label_y, last = {}, 2.0
    for k in right_order:                       # keep right-hand labels at least 0.075 apart
        yy = min((rp[k][0] + rp[k][1]) / 2, last - 0.075)
        label_y[k], last = yy, yy
    for k in right_order:
        ax.add_patch(Rectangle((xR, rp[k][0]), w, rp[k][1] - rp[k][0], color=CLS[k]))
        n = sum(v for (_, b), v in flows.items() if b == k)
        mid = (rp[k][0] + rp[k][1]) / 2
        if abs(label_y[k] - mid) > 0.01:
            ax.plot([xR + w + 0.003, xR + w + 0.012], [mid, label_y[k]], color=MUTED, lw=0.8)
        ax.text(xR + w + 0.015, label_y[k], f"{names[k]}  {n:,} ({n/total:.1%})", ha="left", va="center", fontsize=10)
    ax.text(xL + w / 2, 1.04, "Baseline model\n(what the user receives)", ha="center", fontsize=11, fontweight="bold")
    ax.text(xR + w / 2, 1.04, "Confident Agent\n(what the user receives)", ha="center", fontsize=11, fontweight="bold")
    a_to = {b: flows.get(("A", b), 0) for b in right_order}
    ax.text(0.5, -0.12, f"Of {lefts['A']*total:,.0f} baseline hallucinations, the same tasks under the Confident Agent ended "
            f"withheld {a_to['withheld']:,}, correct {a_to['correct']:,}, wrong-task {a_to['B']:,}, still hallucinated {a_to['A']:,}.",
            ha="center", fontsize=9.5, color=INK2)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.15, 1.12)
    title(fig, "Where the hallucinations went", f"The same {total:,} tasks (990 per quantization, three runs pooled) answered by the plain model "
          "and by the Confident Agent. Ribbon width = number of tasks.")
    footer(fig)
    save(fig, "R02_outcome_flow.png")
    return flows


# --------------------------------------------------------------------------- R03 staleness
URL_RE = re.compile(r"request \d+ \([A-Z]+ (https?://[^\s)]+)\)")
STALE_ORDER = ["current", "retired", "invented", "sibling", "other", "none"]
STALE_NAMES = {"current": "Current documented host and version",
               "retired": "Retired version the model learned (Petstore v2, REST Countries v2/v3.x)",
               "invented": "Non-existent version extrapolated from the prompt (e.g. REST Countries v5.1)",
               "sibling": "A sibling service (JSONPlaceholder for DummyJSON; wrong Open-Meteo subdomain)",
               "other": "Other wrong host or base path",
               "none": "No request made (crash, no code)"}
STALE_COLORS = {"current": "#2a78d6", "retired": "#d03b3b", "invented": "#b0306f", "sibling": "#e8a200", "other": "#eb6834", "none": "#c4c2bb"}


def host_base(url):
    m = re.match(r"https?://([^/]+)(/[^?]*)?", url)
    return (m.group(1).lower(), (m.group(2) or "/")) if m else ("", "/")


def staleness(r):
    task = TASK[r["task_id"]]
    exp_host, exp_path = host_base(task["test_case"]["expected_request"]["url"])
    urls = [m.group(1) for reason in r["baseline_reasons"] for m in [URL_RE.match(reason)] if m]
    if not urls:
        return "none" if r["baseline_class"] in ("runtime_failure", "no_code") else "current"
    cats = []
    for u in urls:
        host, path = host_base(u)
        if r["api"] == "Petstore" and host == "petstore.swagger.io":
            cats.append("retired")
        elif r["api"] == "REST Countries" and host in ("restcountries.com", "api.restcountries.com") and not path.startswith("/countries/v5"):
            cats.append("retired" if re.match(r"/(v1|v2|v3)(\.\d+)?(/|$)", path) or host == "restcountries.com" and re.match(r"/rest/", path)
                        else "invented")
        elif r["api"] == "DummyJSON" and host == "jsonplaceholder.typicode.com":
            cats.append("sibling")
        elif r["api"] == "Open-Meteo" and host.endswith("open-meteo.com") and host != exp_host:
            cats.append("sibling")
        elif host != exp_host:
            cats.append("other")
        else:
            cats.append("current")
    for c in ("retired", "invented", "sibling", "other"):
        if c in cats:
            return c
    return "current"


def r03():
    counts = defaultdict(Counter)
    for q in QS:
        for r in per_task(q):
            counts[r["api"]][staleness(r)] += 1
    apis = ["Petstore", "REST Countries", "Open-Meteo", "DummyJSON", "GitHub", "JSONPlaceholder"]
    tab = pd.DataFrame([{"api": a, **{c: counts[a][c] for c in STALE_ORDER}, "tasks": sum(counts[a].values())} for a in apis])
    tab.to_csv(TB / "R03_baseline_api_versions.csv", index=False)
    fig, ax = plt.subplots(figsize=(12.5, 5.6))
    fig.subplots_adjust(left=0.14, right=0.97, top=0.78, bottom=0.30)
    for i, a in enumerate(apis):
        left = 0
        n = sum(counts[a].values())
        for c in STALE_ORDER:
            v = counts[a][c] / n * 100
            if v <= 0:
                continue
            ax.barh(i, v, left=left, color=STALE_COLORS[c], edgecolor=SURF, linewidth=1.5, height=0.66)
            if v >= 6:
                ax.text(left + v / 2, i, f"{v:.0f}%", ha="center", va="center", fontsize=9,
                        color="white" if c not in ("sibling", "none") else INK)
            left += v
    ax.set_yticks(range(len(apis)), apis)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of baseline answers (three runs pooled)")
    ax.grid(axis="y", visible=False)
    ax.legend(handles=[Patch(color=STALE_COLORS[c], label=STALE_NAMES[c]) for c in STALE_ORDER], loc="upper center",
              bbox_to_anchor=(0.45, -0.17), ncol=2, fontsize=9)
    title(fig, "The model writes the API it was trained on, not the API that exists today",
          "Which host and version each baseline answer called, against the frozen specification the task pins (retrieved 21 September 2026).\n"
          "Petstore retired its Swagger 2 host for OpenAPI 3; REST Countries moved to an authenticated v5 service on a new host.")
    footer(fig)
    save(fig, "R03_training_cutoff_versions.png")
    return tab


# --------------------------------------------------------------------------- R04 sensitivity
SCHEMES = {
    "A. Proposed (used)": ({"interface": 3, "identifier": 3, "access_point": 4, "input_contract": 2, "output_contract": 1, "contextual": 2}, 0.85, 0.60, True),
    "B. Equal weights": ({k: 1 for k in ("interface", "identifier", "access_point", "input_contract", "output_contract", "contextual")}, 0.85, 0.60, True),
    "C. Endpoint-heavy": ({"interface": 2, "identifier": 2, "access_point": 6, "input_contract": 2, "output_contract": 1, "contextual": 2}, 0.85, 0.60, True),
    "D. Strict thresholds": ({"interface": 3, "identifier": 3, "access_point": 4, "input_contract": 2, "output_contract": 1, "contextual": 2}, 0.90, 0.70, True),
    "E. Lenient thresholds": ({"interface": 3, "identifier": 3, "access_point": 4, "input_contract": 2, "output_contract": 1, "contextual": 2}, 0.80, 0.50, True),
    "F. Gate off (exploratory)": ({"interface": 3, "identifier": 3, "access_point": 4, "input_contract": 2, "output_contract": 1, "contextual": 2}, 0.85, 0.60, False),
}
TIER = {"tier_1": 1.0, "tier_2": 0.8, "tier_3": 0.9, "tier_4": 0.5, "none": 0.0}


def decide(report, weights, deliver, flag, gate):
    rows = report["contributions"]
    if any(c["state"] == "verified_incorrect" for c in rows):
        return "abstain"            # the tool cannot correct; the agent may (prompt), but the decision on this candidate is abstain
    if report.get("missing_layers") or report.get("failed_layers"):
        return "abstain"
    applicable = [c for c in rows if c["state"] != "not_applicable"]
    total = sum(weights[c["layer"]] for c in applicable)
    if not total:
        return "abstain"
    ewcs = sum(weights[c["layer"]] * TIER[c["tier"]] for c in applicable if c["state"] == "verified_correct") / total
    if gate and (report.get("extraction_complete") is not True or any(c["state"] == "unverifiable" for c in applicable)):
        return "abstain"
    return "deliver" if ewcs >= deliver - 1e-9 else "deliver_with_flag" if ewcs >= flag - 1e-9 else "abstain"


def final_reports(q):
    """task -> ewcs_report of the last candidate the tool verified, from the stored run."""
    out = {}
    with zipfile.ZipFile(RUNS / FOLDERS[q] / "Intervention_Tests.zip") as z:
        last = {}
        for n in z.namelist():
            m = re.match(r"[^/]+/([^/]+)/verification_(\d+)\.json$", n)
            if m and int(m.group(2)) > last.get(m.group(1), (0, ""))[0]:
                last[m.group(1)] = (int(m.group(2)), n)
        for t, (_, n) in last.items():
            v = json.loads(z.read(n))
            out[t] = (v["ewcs_report"], v["decision"])
    return out


def r04():
    rows, check = [], Counter()
    for q in QS:
        reports = final_reports(q)
        tasks = per_task(q)
        for name, (w, d, f, g) in SCHEMES.items():
            dec = Counter()
            a_del = c_del = b_del = 0
            for r in tasks:
                rep = reports.get(r["task_id"])
                if not rep:
                    dec["no verification"] += 1
                    continue
                k = decide(rep[0], w, d, f, g)
                if name.startswith("A."):
                    check["match" if k == rep[1] else "mismatch"] += 1
                dec[k] += 1
                if k in ("deliver", "deliver_with_flag"):
                    a_del += r["final_class"] == "A"
                    c_del += r["final_class"] == "correct"
                    b_del += r["final_class"] == "B"
            rows.append({"quantization": q, "scheme": name, "deliver": dec["deliver"], "deliver_with_flag": dec["deliver_with_flag"],
                         "abstain": dec["abstain"], "no_verification": dec["no verification"],
                         "hallucinations_delivered": a_del, "correct_delivered": c_del, "wrong_task_delivered": b_del})
    df = pd.DataFrame(rows)
    df.to_csv(TB / "R04_sensitivity_schemes.csv", index=False)
    print("scheme A reproduces the recorded decision:", dict(check))

    pooled = df.groupby("scheme", sort=False)[["deliver", "deliver_with_flag", "abstain", "no_verification",
                                              "hallucinations_delivered", "correct_delivered"]].sum()
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13.5, 5.9), gridspec_kw={"width_ratios": [1.35, 1]})
    fig.subplots_adjust(left=0.17, right=0.98, top=0.80, bottom=0.17, wspace=0.08)
    names = list(pooled.index)
    y = np.arange(len(names))
    left = np.zeros(len(names))
    for col, color, lab in (("deliver", "#2a78d6", "deliver"), ("deliver_with_flag", "#8fb6ea", "deliver with flag"),
                            ("abstain", "#c4c2bb", "abstain (on the final candidate)")):
        v = pooled[col].to_numpy()
        a1.barh(y, v, left=left, color=color, edgecolor=SURF, linewidth=1.5, height=0.62, label=lab)
        for yy, vv, ll in zip(y, v, left):
            if vv > 140:
                a1.text(ll + vv / 2, yy, f"{vv:,}", ha="center", va="center", fontsize=8.5, color="white" if col == "deliver" else INK)
        left += v
    a1.set_yticks(y, names)
    a1.invert_yaxis()
    a1.set_xlabel("Decisions on the final verified candidate (2,970 tasks)")
    a1.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=3, fontsize=8.5)
    a1.grid(axis="y", visible=False)
    a2.barh(y - 0.18, pooled["hallucinations_delivered"], height=0.34, color="#d03b3b", label="hallucinations delivered")
    a2.barh(y + 0.18, pooled["correct_delivered"] / 10, height=0.34, color="#2a78d6", label="correct code delivered (÷10)")
    for yy, a, c in zip(y, pooled["hallucinations_delivered"], pooled["correct_delivered"]):
        a2.text(a + 3, yy - 0.18, f"{a}", va="center", fontsize=8.5)
        a2.text(c / 10 + 3, yy + 0.18, f"{c:,}", va="center", fontsize=8.5)
    a2.set_yticks(y, [""] * len(y))
    a2.invert_yaxis()
    a2.set_xlabel("Tasks (three runs pooled)")
    a2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, fontsize=8.5)
    a2.grid(axis="y", visible=False)
    title(fig, "The weights move the flag, not the safety of what is delivered",
          "The stored layer results of each task's final candidate re-scored under the five planned schemes (Progress Report 2, section 7.8)\n"
          "and with the uncertainty gate removed. Hard rules (contradiction, unverifiable critical check) decide withholding before any threshold.")
    footer(fig)
    save(fig, "R04_sensitivity_schemes.png")
    return df, check


# --------------------------------------------------------------------------- R05 protocol
NOTE_SHORT = {
    "reached the turn limit; the benchmark asked for the final reply": "Hit the 4-turn limit; reply requested",
    "verified the same code more than once": "Verified identical code again",
    "more than one correction": "More than one correction",
    "reply differs from the final report": "Reply differs from the report",
    "corrected without a verified_incorrect layer": "Corrected without a contradiction",
    "replied without correcting after a verified_incorrect layer": "Replied without correcting",
    "never verified": "Never verified",
    "reply shows code the tool did not approve": "Showed unapproved code",
}


def r05():
    rows = []
    for q in QS:
        for note, n in evaluation(q)["protocol_notes"].items():
            rows.append({"quantization": q, "note": NOTE_SHORT.get(note, note), "tasks": n})
    df = pd.DataFrame(rows)
    df.to_csv(TB / "R05_protocol_notes.csv", index=False)
    order = df.groupby("note")["tasks"].sum().sort_values(ascending=True).index.tolist()
    fig, ax = plt.subplots(figsize=(12.5, 5.4))
    fig.subplots_adjust(left=0.27, right=0.97, top=0.80, bottom=0.13)
    y = np.arange(len(order))
    for k, q in enumerate(QS):
        v = [int(df[(df.note == o) & (df.quantization == q)].tasks.sum()) for o in order]
        ax.barh(y + (k - 1) * 0.26, v, height=0.24, color=QC[q], label=q)
        for yy, vv in zip(y, v):
            ax.text(vv + 3, yy + (k - 1) * 0.26, str(vv), va="center", fontsize=8)
    ax.set_yticks(y, order)
    ax.set_xlabel("Tasks out of 990 per run")
    ax.legend(loc="lower right")
    ax.grid(axis="y", visible=False)
    title(fig, "The model often bends the protocol, but the tool still decides",
          "Deviations from the Confident Agent prompt recorded by the benchmark. The tool's decision on the last verified candidate is what counts;\n"
          "in no task of any run did the user see code the tool had not approved.")
    footer(fig)
    save(fig, "R05_protocol_deviations.png")
    return df


# --------------------------------------------------------------------------- R06 pilot
def r06():
    systems = ["Qwen (pilot model)", "Gemini", "ChatGPT", "Copilot", "DeepSeek"]
    workbook = [6, 2, 2, 1, 8]          # Summary sheet of Baseline_Template_Final_V9.xlsx
    practical = [6, 2, 2, 2, 8]         # Practical Three report, figure 1
    reconciled = [6, 2, 2, 4, 8]        # verdict justifications re-read (Copilot P5, P8, P9, P10)
    pd.DataFrame({"system": systems, "workbook_summary": workbook, "practical_three_report": practical,
                  "reconciled_from_justifications": reconciled}).to_csv(TB / "R06_pilot_reconciliation.csv", index=False)
    fig, ax = plt.subplots(figsize=(11.5, 4.6))
    fig.subplots_adjust(left=0.07, right=0.97, top=0.76, bottom=0.14)
    x = np.arange(len(systems))
    for k, (vals, col, lab) in enumerate(((workbook, "#c4c2bb", "Workbook V9 summary sheet"),
                                         (practical, "#8fb6ea", "Practical Three report"),
                                         (reconciled, "#2a78d6", "Reconciled (this report)"))):
        ax.bar(x + (k - 1) * 0.26, vals, width=0.24, color=col, label=lab)
        for xx, v in zip(x, vals):
            ax.text(xx + (k - 1) * 0.26, v + 0.12, str(v), ha="center", fontsize=8.5)
    ax.set_xticks(x, systems)
    ax.set_ylabel("Hallucinations out of 10")
    ax.set_ylim(0, 10)
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(axis="x", visible=False)
    title(fig, "Pilot (Practical Three): the counts agree except Copilot's",
          "Ten trap-heavy prompts, one response per system. Copilot's verdict cells are free text; read by their justifications they record\n"
          "hallucinations on P5, P8, P9 and P10. The pilot is supplementary evidence, not the experiment.")
    fig.text(0.012, 0.012, "Source: Final Report and Documentation/COMP301 The Skeptics Practical Three/Baseline_Template_Final_V9.xlsx",
             fontsize=8, color=MUTED)
    save(fig, "R06_pilot_reconciliation.png")


if __name__ == "__main__":
    r01()
    r02()
    r03()
    df4, check = r04()
    r05()
    r06()
