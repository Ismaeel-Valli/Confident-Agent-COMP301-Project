"""tempstats: cost-of-intervention statistics and charts for the Confident Agent benchmark.

Reads ONLY the raw files in "Unprocessed Data/" (stats/ and evaluation/) and writes
  tempstats/tables/*.csv   every number quoted in FINDINGS.md
  tempstats/charts/*.png   the charts
Run:  python3 -I build_tempstats.py        (pandas, numpy, scipy, matplotlib)

Electricity tariff (see FINDINGS.md): eThekwini Municipality, Durban Central, September 2026:
R3.5747 per kWh excluding VAT; 15% VAT added => R4.110905 per kWh.
"""
from pathlib import Path
import json

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from scipy import stats as st

HERE = Path(__file__).resolve().parent
RAW = HERE.parent / "Unprocessed Data"
STATS = RAW / "stats"
EVAL = RAW / "evaluation"
CH = HERE / "charts"
TB = HERE / "tables"
CH.mkdir(exist_ok=True)
TB.mkdir(exist_ok=True)

# ----------------------------------------------------------------------------- tariff
TARIFF_EXCL = 3.5747            # R/kWh excl. VAT (eThekwini, Durban Central, Sept 2026)
VAT = 0.15
TARIFF = TARIFF_EXCL * (1 + VAT)  # R/kWh incl. VAT = 4.110905
R_PER_J = TARIFF / 3.6e6
TARIFF_NOTE = (f"Electricity at R{TARIFF_EXCL:.4f}/kWh excl. VAT + 15% VAT = R{TARIFF:.4f}/kWh "
               "(eThekwini Municipality bill, Durban Central, Sept 2026)")
SOURCE = ("Source: Unprocessed Data/stats (main runs, 990 scored tasks per quantization, pilot excluded) | "
          "Qwen3.5-9B, AMD RX 9070 XT + Ryzen 7 5700X3D")

# ----------------------------------------------------------------------------- palette (validated)
BASE, CA = "#2a78d6", "#eb6834"          # baseline blue, Confident Agent orange
QC = {"Q4_K_M": "#1baf7a", "Q6_K": "#6250d6", "Q8_0": "#e87ba4"}
INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
GOOD, BAD = "#0ca30c", "#d03b3b"
QS = ["Q4_K_M", "Q6_K", "Q8_0"]
QLAB = {"Q4_K_M": "Q4_K_M", "Q6_K": "Q6_K", "Q8_0": "Q8_0"}

plt.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
    "font.family": "DejaVu Sans", "font.size": 10.5, "text.color": INK,
    "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": GRID,
    "grid.linewidth": 0.7, "axes.axisbelow": True, "legend.frameon": False,
})


def header(fig, title, sub=None, cost=False, foot=None):
    fig.text(0.015, 0.985, title, ha="left", va="top", fontsize=17, fontweight="bold", color=INK)
    if sub:
        fig.text(0.015, 0.985 - 0.045, sub, ha="left", va="top", fontsize=10.5, color=INK2)
    f = SOURCE + ("\n" + TARIFF_NOTE if cost else "")
    if foot:
        f = foot + "\n" + f
    fig.text(0.015, 0.008, f, ha="left", va="bottom", fontsize=7.6, color=MUTED, linespacing=1.4)


def save(fig, name):
    fig.savefig(CH / name, dpi=170)
    plt.close(fig)
    print("saved", name)


def clean_ax(ax, grid="y"):
    ax.grid(False)
    if grid:
        ax.grid(True, axis=grid)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)


def fmt_p(p):
    if p == 0 or p < 1e-300:
        return "<1e-300"
    return f"{p:.1e}"


# ----------------------------------------------------------------------------- load
runs = pd.read_csv(STATS / "runs.csv")
P = pd.read_csv(STATS / "combined" / "prompt_stats.csv")
P = P[P.run_role == "main"].copy()
Pall = P.copy()                       # incl. pilot (whole-run totals)
P = P[P.pilot == 0].copy()           # 990 scored tasks per run
EK = pd.read_csv(STATS / "combined" / "error_kinds.csv")
VD = pd.read_csv(STATS / "combined" / "verifier_detection.csv")
QC_ = pd.read_csv(STATS / "combined" / "quantization_comparison.csv").set_index("quantization")
runs = runs[runs.role == "main"].set_index("quantization")

for m in ("b", "i"):
    P[f"{m}_kwh"] = P[f"{m}_energy_j"] / 3.6e6
    P[f"{m}_rand"] = P[f"{m}_energy_j"] * R_PER_J
    P[f"{m}_rand_idle"] = P[f"{m}_energy_above_idle_j"] * R_PER_J
P["i_correct"] = P.i_correct_reaches_user.astype(int)
P["b_correct_i"] = P.b_correct.astype(int)
P["b_hall"] = P.b_hallucination.astype(int)
P["i_hall"] = P.i_hallucination_reaches_user.astype(int)

rng = np.random.default_rng(301)
NB = 5000

# ============================================================================= TABLE 1: headline cost per run
rows = []
for q in QS:
    d = P[P.quantization == q]
    n = len(d)
    r = {"quantization": q, "n_tasks": n}
    for m, nm in (("b", "baseline"), ("i", "intervention")):
        r[f"{nm}_mean_s"] = d[f"{m}_duration_s"].mean()
        r[f"{nm}_median_s"] = d[f"{m}_duration_s"].median()
        r[f"{nm}_total_h"] = d[f"{m}_duration_s"].sum() / 3600
        r[f"{nm}_mean_wh"] = d[f"{m}_energy_wh"].mean()
        r[f"{nm}_total_kwh"] = d[f"{m}_kwh"].sum()
        r[f"{nm}_total_rand"] = d[f"{m}_rand"].sum()
        r[f"{nm}_rand_per_1000"] = d[f"{m}_rand"].mean() * 1000
        r[f"{nm}_cents_per_prompt"] = d[f"{m}_rand"].mean() * 100
        r[f"{nm}_total_rand_above_idle"] = d[f"{m}_rand_idle"].sum()
        r[f"{nm}_mean_tokens"] = d[f"{m}_total_tokens"].mean()
        r[f"{nm}_mean_completion_tokens"] = d[f"{m}_completion_tokens"].mean()
        r[f"{nm}_mean_prompt_tokens"] = d[f"{m}_prompt_tokens"].mean()
        r[f"{nm}_total_tokens_M"] = d[f"{m}_total_tokens"].sum() / 1e6
        r[f"{nm}_mean_power_w"] = d[f"{m}_energy_j"].sum() / d[f"{m}_duration_s"].sum()
        r[f"{nm}_gpu_share"] = d[f"{m}_gpu_energy_j"].sum() / d[f"{m}_energy_j"].sum()
        r[f"{nm}_correct_delivered"] = int(d.b_correct_i.sum() if m == "b" else d.i_correct.sum())
        r[f"{nm}_hallucinations_to_user"] = int(d.b_hall.sum() if m == "b" else d.i_hall.sum())
        cd = r[f"{nm}_correct_delivered"]
        r[f"{nm}_rand_per_correct"] = r[f"{nm}_total_rand"] / cd
        r[f"{nm}_sec_per_correct"] = d[f"{m}_duration_s"].sum() / cd
        r[f"{nm}_wh_per_correct"] = d[f"{m}_energy_wh"].sum() / cd
    r["time_x"] = r["intervention_mean_s"] / r["baseline_mean_s"]
    r["energy_x"] = r["intervention_rand_per_1000"] / r["baseline_rand_per_1000"]
    r["token_x"] = r["intervention_mean_tokens"] / r["baseline_mean_tokens"]
    r["extra_rand_total"] = r["intervention_total_rand"] - r["baseline_total_rand"]
    r["extra_hours_total"] = r["intervention_total_h"] - r["baseline_total_h"]
    r["extra_kwh_total"] = r["intervention_total_kwh"] - r["baseline_total_kwh"]
    dh = r["baseline_hallucinations_to_user"] - r["intervention_hallucinations_to_user"]
    dc = r["intervention_correct_delivered"] - r["baseline_correct_delivered"]
    r["hallucinations_prevented"] = dh
    r["extra_correct_answers"] = dc
    r["extra_rand_per_hallucination_prevented"] = r["extra_rand_total"] / dh
    r["extra_min_per_hallucination_prevented"] = r["extra_hours_total"] * 60 / dh
    r["extra_rand_per_extra_correct"] = r["extra_rand_total"] / dc
    r["extra_min_per_extra_correct"] = r["extra_hours_total"] * 60 / dc
    rows.append(r)
H = pd.DataFrame(rows).set_index("quantization")
H.T.to_csv(TB / "01_headline_cost_by_quantization.csv")

# whole-run totals incl. the 10 pilot prompts, from runs.csv (as actually run)
W = pd.DataFrame({
    "baseline_hours": runs.b_run_hours, "intervention_hours": runs.i_run_hours,
    "baseline_wh": runs.b_run_energy_wh, "intervention_wh": runs.i_run_energy_wh,
    "baseline_tokens": runs.b_run_tokens, "intervention_tokens": runs.i_run_tokens})
W["baseline_rand"] = W.baseline_wh / 1000 * TARIFF
W["intervention_rand"] = W.intervention_wh / 1000 * TARIFF
W["baseline_rand_excl_vat"] = W.baseline_wh / 1000 * TARIFF_EXCL
W["intervention_rand_excl_vat"] = W.intervention_wh / 1000 * TARIFF_EXCL
W["extra_rand"] = W.intervention_rand - W.baseline_rand
W["extra_hours"] = W.intervention_hours - W.baseline_hours
W = W.loc[QS]
W.loc["ALL 3 RUNS"] = W.sum()
W.to_csv(TB / "02_whole_run_totals_incl_pilot.csv")

# ============================================================================= TABLE 3: paired tests + bootstrap
def boot_ratio(b, i, B=NB):
    n = len(b)
    idx = rng.integers(0, n, (B, n))
    bm, im = b.values[idx].mean(1), i.values[idx].mean(1)
    return np.percentile(bm, [2.5, 97.5]), np.percentile(im, [2.5, 97.5]), np.percentile(im / bm, [2.5, 97.5])


def rank_biserial(d):
    d = d[d != 0]
    r = st.rankdata(np.abs(d))
    return (r[d > 0].sum() - r[d < 0].sum()) / r.sum()


tests = []
METR = [("Duration (s)", "duration_s"), ("Energy (J)", "energy_j"), ("Total tokens", "total_tokens"),
        ("Completion tokens", "completion_tokens"), ("GPU energy (J)", "gpu_energy_j"), ("CPU energy (J)", "cpu_energy_j")]
CIB = {}
for q in QS:
    d = P[P.quantization == q]
    for lab, c in METR:
        b, i = d[f"b_{c}"], d[f"i_{c}"]
        w = st.wilcoxon(i, b)
        bci, ici, rci = boot_ratio(b, i)
        CIB[(q, c)] = (b.mean(), i.mean(), bci, ici, rci)
        tests.append({"quantization": q, "metric": lab, "n": len(d), "baseline_mean": b.mean(), "baseline_median": b.median(),
                      "intervention_mean": i.mean(), "intervention_median": i.median(),
                      "ratio_of_means": i.mean() / b.mean(), "ratio_ci_low": rci[0], "ratio_ci_high": rci[1],
                      "median_paired_ratio": (i / b).median(), "wilcoxon_W": w.statistic, "wilcoxon_p": w.pvalue,
                      "rank_biserial_r": rank_biserial((i - b).values),
                      "share_of_tasks_where_intervention_costs_more": float((i > b).mean())})
T3 = pd.DataFrame(tests)
T3.to_csv(TB / "03_paired_wilcoxon_cost.csv", index=False)

# McNemar (exact) + bootstrap CI for outcome differences
out = []
for q in QS:
    d = P[P.quantization == q]
    n = len(d)
    for lab, bcol, icol, sign in (("Hallucination reaching user", "b_hall", "i_hall", -1),
                                  ("Correct code reaching user", "b_correct_i", "i_correct", +1)):
        b, i = d[bcol].values, d[icol].values
        n10 = int(((b == 1) & (i == 0)).sum())
        n01 = int(((b == 0) & (i == 1)).sum())
        p = st.binomtest(n10, n10 + n01, 0.5).pvalue if n10 + n01 else 1
        idx = rng.integers(0, n, (NB, n))
        diff = (i[idx].mean(1) - b[idx].mean(1)) * 100
        ci = np.percentile(diff, [2.5, 97.5])
        out.append({"quantization": q, "outcome": lab, "baseline_pct": b.mean() * 100, "intervention_pct": i.mean() * 100,
                    "diff_pp(int-base)": (i.mean() - b.mean()) * 100, "ci_low": ci[0], "ci_high": ci[1],
                    "base_only": n10, "int_only": n01, "mcnemar_exact_p": p})
T4 = pd.DataFrame(out)
T4.to_csv(TB / "04_outcome_differences_mcnemar.csv", index=False)

# quantization effect on cost (Kruskal-Wallis + Holm pairwise Mann-Whitney)
qt = []
for m, nm in (("b", "baseline"), ("i", "intervention")):
    for lab, c in (("Duration (s)", "duration_s"), ("Energy (J)", "energy_j"), ("Total tokens", "total_tokens")):
        groups = [P[P.quantization == q][f"{m}_{c}"].values for q in QS]
        kw = st.kruskal(*groups)
        pairs = [("Q4_K_M", "Q6_K"), ("Q4_K_M", "Q8_0"), ("Q6_K", "Q8_0")]
        pv = [st.mannwhitneyu(P[P.quantization == a][f"{m}_{c}"], P[P.quantization == b][f"{m}_{c}"]).pvalue for a, b in pairs]
        order = np.argsort(pv)
        holm = np.empty(3)
        run = 0
        for rank, k in enumerate(order):
            run = max(run, min(1, pv[k] * (3 - rank)))
            holm[k] = run
        rec = {"mode": nm, "metric": lab, "kruskal_H": kw.statistic, "kruskal_p": kw.pvalue}
        for (a, b), p_ in zip(pairs, holm):
            rec[f"{a}_vs_{b}_holm_p"] = p_
        for q in QS:
            rec[f"{q}_median"] = P[P.quantization == q][f"{m}_{c}"].median()
        qt.append(rec)
T5 = pd.DataFrame(qt)
T5.to_csv(TB / "05_quantization_effect_on_cost.csv", index=False)

# ============================================================================= TABLE 6: where the intervention's money goes
P["i_class_fin"] = P.i_final_class
# categories: delivered correct / delivered wrong / withheld hallucination (A) / withheld correct / withheld other
def spend_cat(r):
    if r.i_delivered == 1:
        return "Delivered, correct" if r.i_shown_class == "correct" else "Delivered, wrong (A/B/runtime)"
    if r.i_final_class == "A":
        return "Withheld, was hallucination (good catch)"
    if r.i_final_class == "correct":
        return "Withheld, was correct (false alarm)"
    return "Withheld, other (B / runtime failure)"
P["spend_cat"] = P.apply(spend_cat, axis=1)
CATS = ["Delivered, correct", "Delivered, wrong (A/B/runtime)", "Withheld, was hallucination (good catch)",
        "Withheld, was correct (false alarm)", "Withheld, other (B / runtime failure)"]
sp = (P.groupby(["quantization", "spend_cat"])
      .agg(prompts=("task_id", "size"), hours=("i_duration_s", lambda s: s.sum() / 3600), rand=("i_rand", "sum"),
           mean_s=("i_duration_s", "mean")).reset_index())
sp.to_csv(TB / "06_intervention_spend_by_outcome.csv", index=False)

# decision / corrections
cr = (P.groupby("i_correction_count")
      .agg(prompts=("task_id", "size"), mean_s=("i_duration_s", "mean"), mean_rand=("i_rand", "mean"),
           mean_tokens=("i_total_tokens", "mean"), correct_to_user=("i_correct", "mean"),
           halluc_to_user=("i_hall", "mean"), withheld=("i_withheld", "mean")).reset_index())
cr["rand_per_1000"] = cr.mean_rand * 1000
cr.to_csv(TB / "07_cost_by_correction_rounds.csv", index=False)

# ============================================================================= TABLE 8: per API / category
def grp_table(col):
    rows = []
    for (g, q), d in P.groupby([col, "quantization"]):
        rows.append({col: g, "quantization": q, "n": len(d),
                     "b_hall": d.b_hall.mean(), "i_hall": d.i_hall.mean(),
                     "b_correct": d.b_correct_i.mean(), "i_correct": d.i_correct.mean(),
                     "abstain": d.i_withheld.mean(),
                     "b_mean_s": d.b_duration_s.mean(), "i_mean_s": d.i_duration_s.mean(),
                     "b_rand_per_1000": d.b_rand.mean() * 1000, "i_rand_per_1000": d.i_rand.mean() * 1000,
                     "b_rand_per_correct": d.b_rand.sum() / max(d.b_correct_i.sum(), 1) if d.b_correct_i.sum() else np.nan,
                     "i_rand_per_correct": d.i_rand.sum() / d.i_correct.sum() if d.i_correct.sum() else np.nan,
                     "b_sec_per_correct": d.b_duration_s.sum() / d.b_correct_i.sum() if d.b_correct_i.sum() else np.nan,
                     "i_sec_per_correct": d.i_duration_s.sum() / d.i_correct.sum() if d.i_correct.sum() else np.nan})
    return pd.DataFrame(rows)


G_api = grp_table("api")
G_api.to_csv(TB / "08_by_api_and_quantization.csv", index=False)
grp_table("operation_category").to_csv(TB / "09_by_operation_category.csv", index=False)
grp_table("auth_type").to_csv(TB / "10_by_auth_type.csv", index=False)
grp_table("difficulty").to_csv(TB / "11_by_difficulty.csv", index=False)
grp_table("spec_source").to_csv(TB / "12_by_spec_source.csv", index=False)

# pooled-API (3 runs) cost
api_pool = []
for a, d in P.groupby("api"):
    api_pool.append({"api": a, "n": len(d),
                     "b_mean_s": d.b_duration_s.mean(), "i_mean_s": d.i_duration_s.mean(),
                     "b_rand_per_1000": d.b_rand.mean() * 1000, "i_rand_per_1000": d.i_rand.mean() * 1000,
                     "b_correct_n": int(d.b_correct_i.sum()), "i_correct_n": int(d.i_correct.sum()),
                     "b_rand_per_correct": d.b_rand.sum() / d.b_correct_i.sum() if d.b_correct_i.sum() else np.nan,
                     "i_rand_per_correct": d.i_rand.sum() / d.i_correct.sum() if d.i_correct.sum() else np.nan,
                     "b_hall": d.b_hall.mean(), "i_hall": d.i_hall.mean(), "abstain": d.i_withheld.mean(),
                     "i_total_rand": d.i_rand.sum(), "i_total_hours": d.i_duration_s.sum() / 3600})
API = pd.DataFrame(api_pool).set_index("api")
API.to_csv(TB / "13_by_api_pooled.csv")

# ============================================================================= verifier / EWCS
vd = VD[(VD.dimension == "overall") & (VD.target == "A")].set_index("quantization").loc[QS]
vd.to_csv(TB / "14_verifier_detection_overall.csv")
vd2 = VD[(VD.dimension == "overall") & (VD.target == "A_or_B")].set_index("quantization").loc[QS]
vd2.to_csv(TB / "14b_verifier_detection_A_or_B.csv")

fp_cost = []
for q in QS:
    d = P[P.quantization == q]
    fp = d[(d.verifier_outcome == "FP")]
    tp = d[(d.verifier_outcome == "TP")]
    fn = d[(d.verifier_outcome == "FN")]
    fp_cost.append({"quantization": q, "FP_n": len(fp), "FP_hours": fp.i_duration_s.sum() / 3600, "FP_rand": fp.i_rand.sum(),
                    "TP_n": len(tp), "TP_hours": tp.i_duration_s.sum() / 3600, "TP_rand": tp.i_rand.sum(),
                    "FN_n": len(fn), "FN_hours": fn.i_duration_s.sum() / 3600, "FN_rand": fn.i_rand.sum()})
pd.DataFrame(fp_cost).to_csv(TB / "15_verifier_error_cost.csv", index=False)

# AUC / ROC (correct vs class A, final candidate EWCS)
roc = {}
auc_rows = []
for q in QS:
    d = P[(P.quantization == q) & P.i_final_class.isin(["correct", "A"]) & P.i_ewcs.notna()]
    y = (d.i_final_class == "correct").astype(int).values
    s = d.i_ewcs.values
    auc = st.mannwhitneyu(s[y == 1], s[y == 0]).statistic / (y.sum() * (1 - y).sum())
    thr = np.unique(s)[::-1]
    tpr = [(s[y == 1] >= t).mean() for t in thr]
    fpr = [(s[y == 0] >= t).mean() for t in thr]
    roc[q] = (np.r_[0, fpr, 1], np.r_[0, tpr, 1], auc)
    auc_rows.append({"quantization": q, "AUC_correct_vs_A": auc, "n_correct": int(y.sum()), "n_A": int((1 - y).sum()),
                     "median_ewcs_correct": np.median(s[y == 1]), "median_ewcs_A": np.median(s[y == 0])})
pd.DataFrame(auc_rows).to_csv(TB / "16_ewcs_auc.csv", index=False)

# ============================================================================= hallucination kinds
ek = EK[(EK.dimension == "overall") & (EK.error_class == "A") & (EK.run_role == "main")]
ekp = ek.pivot_table(index="kind", columns="mode", values="tasks", aggfunc="sum").fillna(0)
ekp.to_csv(TB / "17_hallucination_kinds_all_runs.csv")
non_host = P.copy()

# ============================================================================= unit economics
ue = []
for q in QS:
    r = H.loc[q]
    for nm in ("baseline", "intervention"):
        hrs = r[f"{nm}_total_h"]
        rand = r[f"{nm}_total_rand"]
        cd = r[f"{nm}_correct_delivered"]
        ue.append({"quantization": q, "mode": nm, "prompts_per_hour": 990 / hrs, "prompts_per_R1": 990 / rand,
                   "correct_per_hour": cd / hrs, "correct_per_R1": cd / rand,
                   "rand_per_10000_prompts": rand / 990 * 10000, "hours_per_10000_prompts": hrs / 990 * 10000,
                   "days_per_10000_prompts": hrs / 990 * 10000 / 24,
                   "rand_per_100000_prompts": rand / 990 * 100000, "days_per_100000_prompts": hrs / 990 * 100000 / 24})
UE = pd.DataFrame(ue)
UE.to_csv(TB / "18_unit_economics_and_scaling.csv", index=False)

# power
pw = []
idle = runs.power_idle_w.apply(json.loads)
for q in QS:
    d = P[P.quantization == q]
    idle_w = idle[q]["gpu"] + idle[q]["cpu"]
    for m, nm in (("b", "baseline"), ("i", "intervention")):
        pw.append({"quantization": q, "mode": nm, "mean_power_w": d[f"{m}_energy_j"].sum() / d[f"{m}_duration_s"].sum(),
                   "idle_w_gpu_plus_cpu": idle_w,
                   "above_idle_w": d[f"{m}_energy_above_idle_j"].sum() / d[f"{m}_duration_s"].sum(),
                   "gpu_wh_per_prompt": d[f"{m}_gpu_energy_j"].mean() / 3600, "cpu_wh_per_prompt": d[f"{m}_cpu_energy_j"].mean() / 3600,
                   "completion_tok_per_s": d[f"{m}_completion_tokens"].sum() / d[f"{m}_model_s"].sum(),
                   "J_per_1k_total_tokens": d[f"{m}_energy_j"].sum() / d[f"{m}_total_tokens"].sum() * 1000,
                   "J_per_completion_token": d[f"{m}_energy_j"].sum() / d[f"{m}_completion_tokens"].sum(),
                   "tool_seconds_mean": d[f"{m}_tool_s"].mean() if m == "i" else 0,
                   "model_seconds_mean": d[f"{m}_model_s"].mean()})
PW = pd.DataFrame(pw)
PW.to_csv(TB / "19_power_and_throughput.csv", index=False)

# =============================================================================
print(H[["time_x", "energy_x", "token_x", "baseline_rand_per_1000", "intervention_rand_per_1000"]])
print(T4)
exec(open(HERE / "charts_part.py").read())
