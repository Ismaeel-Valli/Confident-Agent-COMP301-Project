# Chart code, exec'd by build_tempstats.py (shares its namespace).
from matplotlib.gridspec import GridSpec
from matplotlib.colors import LinearSegmentedColormap

MODES = [("baseline", BASE, "Baseline (no verifier)"), ("intervention", CA, "Confident Agent")]
XQ = np.arange(3)
BW = 0.36


def lighten(hexc, f):
    hexc = hexc.lstrip("#")
    r, g, b = [int(hexc[i:i + 2], 16) for i in (0, 2, 4)]
    return "#%02x%02x%02x" % tuple(int(c + (255 - c) * f) for c in (r, g, b))


def seq_cmap(hexc):
    return LinearSegmentedColormap.from_list("s", [lighten(hexc, 0.92), lighten(hexc, 0.5), hexc])


def grouped(ax, vals_b, vals_i, fmt, err_b=None, err_i=None, ylabel=None, title=None, mult=True, ymax=None, lab_fs=9.5):
    """two bars per quantization; err_* = (low, high) arrays."""
    for k, (vals, col, err, off) in enumerate(((vals_b, BASE, err_b, -BW / 2 - 0.01), (vals_i, CA, err_i, BW / 2 + 0.01))):
        ax.bar(XQ + off, vals, BW, color=col, zorder=3, linewidth=0)
        if err is not None:
            lo, hi = np.array(err[0]), np.array(err[1])
            ax.errorbar(XQ + off, vals, yerr=[np.array(vals) - lo, hi - np.array(vals)], fmt="none", ecolor=INK, elinewidth=1,
                        capsize=3, zorder=4)
        top = (np.array(err[1]) if err is not None else np.array(vals))
        for x, v, t in zip(XQ + off, vals, top):
            ax.text(x, t + (ymax or max(vals_i)) * 0.012, fmt(v), ha="center", va="bottom", fontsize=lab_fs, color=INK)
    if mult:
        for x, b, i in zip(XQ, vals_b, vals_i):
            ax.text(x, -0.0, "", ha="center")
    ax.set_xticks(XQ)
    ax.set_xticklabels(QS, fontsize=11)
    ax.tick_params(axis="x", length=0)
    if ylabel:
        ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title, loc="left", fontsize=12, fontweight="bold", color=INK, pad=22)
    clean_ax(ax, "y")
    if ymax:
        ax.set_ylim(0, ymax)
    else:
        ax.set_ylim(0, max(max(vals_i), max(vals_b)) * 1.22)


def mode_legend(fig, y=0.93, x=0.985):
    h = [Patch(color=BASE, label="Baseline (no verifier)"), Patch(color=CA, label="Confident Agent (verified)")]
    fig.legend(handles=h, loc="upper right", bbox_to_anchor=(x, y), ncol=2, fontsize=10, frameon=False)


def xmult(ax, vb, vi, fmt="{:.1f}×"):
    for x, b, i in zip(XQ, vb, vi):
        ax.text(x, ax.get_ylim()[1] * 0.985, fmt.format(i / b), ha="center", va="top", fontsize=11, fontweight="bold", color=CA)


# ============================================================================= 00 scorecard
def scorecard():
    fig = plt.figure(figsize=(14, 9.2))
    header(fig, "Confident Agent: scorecard", "Baseline → Confident Agent, per quantization (990 scored tasks each). "
           "Cost = electricity (GPU + CPU package) priced at the Durban Central tariff.", cost=True)
    tiles = [
        ("Hallucinated code\nreaching the user", lambda q: (f"{QC_.loc[q,'b_hallucination_rate']*100:.1f}%", f"{QC_.loc[q,'i_hallucination_rate']*100:.1f}%"), GOOD, "lower is better"),
        ("Correct code\nreaching the user", lambda q: (f"{QC_.loc[q,'b_correct_rate']*100:.1f}%", f"{QC_.loc[q,'i_correct_rate']*100:.1f}%"), GOOD, "higher is better"),
        ("Time per prompt", lambda q: (f"{H.loc[q,'baseline_mean_s']:.1f} s", f"{H.loc[q,'intervention_mean_s']:.1f} s"), BAD, f"×{{}} slower"),
        ("Electricity / 1,000 prompts\n(incl. VAT)", lambda q: (f"R{H.loc[q,'baseline_rand_per_1000']:.2f}", f"R{H.loc[q,'intervention_rand_per_1000']:.2f}"), BAD, "×{} dearer"),
        ("Electricity per correct\nanswer delivered", lambda q: (f"{H.loc[q,'baseline_rand_per_correct']*100:.2f}c", f"{H.loc[q,'intervention_rand_per_correct']*100:.2f}c"), BAD, "×{} dearer"),
        ("Time per correct\nanswer delivered", lambda q: (f"{H.loc[q,'baseline_sec_per_correct']:.0f} s", f"{H.loc[q,'intervention_sec_per_correct']:.0f} s"), BAD, "×{} slower"),
    ]
    gs = GridSpec(len(tiles), 3, left=0.27, right=0.985, top=0.86, bottom=0.12, hspace=0.18, wspace=0.05)
    for r, (name, fn, _, hint) in enumerate(tiles):
        fig.text(0.015, 0.86 - (r + 0.5) * (0.74 / len(tiles)) + 0.02, name, ha="left", va="center", fontsize=10.5, fontweight="bold", color=INK)
        fig.text(0.015, 0.86 - (r + 0.5) * (0.74 / len(tiles)) - 0.012, hint.split("{}")[0].strip() if "{}" not in hint else "intervention vs baseline", ha="left", va="center", fontsize=8.5, color=MUTED)
        for c, q in enumerate(QS):
            ax = fig.add_subplot(gs[r, c])
            ax.set_facecolor("#f4f3ef")
            for s in ax.spines.values():
                s.set_visible(False)
            ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
            b, i = fn(q)
            ax.text(0.2, 0.52, b, ha="center", va="center", fontsize=17, color=BASE, fontweight="bold", transform=ax.transAxes)
            ax.text(0.5, 0.52, "→", ha="center", va="center", fontsize=15, color=MUTED, transform=ax.transAxes)
            ax.text(0.8, 0.52, i, ha="center", va="center", fontsize=17, color=CA, fontweight="bold", transform=ax.transAxes)
            if r == 0:
                ax.set_title(q, fontsize=13, fontweight="bold", color=QC[q], pad=6)
            if "{}" in hint:
                num = {2: H.loc[q, "time_x"], 3: H.loc[q, "energy_x"],
                       4: H.loc[q, "intervention_rand_per_correct"] / H.loc[q, "baseline_rand_per_correct"],
                       5: H.loc[q, "intervention_sec_per_correct"] / H.loc[q, "baseline_sec_per_correct"]}[r]
                ax.text(0.5, 0.12, hint.format(f"{num:.1f}"), ha="center", va="center", fontsize=9, color=INK2, transform=ax.transAxes)
            else:
                d = (QC_.loc[q, "i_hallucination_rate"] - QC_.loc[q, "b_hallucination_rate"]) * 100 if r == 0 else (QC_.loc[q, "i_correct_rate"] - QC_.loc[q, "b_correct_rate"]) * 100
                ax.text(0.5, 0.12, f"{d:+.1f} percentage points", ha="center", va="center", fontsize=9, color=INK2, transform=ax.transAxes)
    h = [Patch(color=BASE, label="Baseline"), Patch(color=CA, label="Confident Agent")]
    fig.legend(handles=h, loc="upper right", bbox_to_anchor=(0.985, 0.985), ncol=2, fontsize=10)
    save(fig, "00_scorecard.png")


# ============================================================================= 01 hero
def hero():
    fig, axs = plt.subplots(1, 3, figsize=(16, 6.4))
    fig.subplots_adjust(left=0.05, right=0.99, top=0.76, bottom=0.17, wspace=0.22)
    header(fig, "What the intervention costs, per prompt", "Mean per prompt with 95% bootstrap CI (5,000 paired resamples). "
           "Every task's cost rises: Wilcoxon signed-rank p < 1e-160 in all 18 tests.", cost=True)
    mode_legend(fig, 0.9)
    specs = [("duration_s", 1, "Time per prompt (seconds)", lambda v: f"{v:.1f}s"),
             ("energy_j", R_PER_J * 1000, "Electricity per 1,000 prompts (Rand incl. VAT)", lambda v: f"R{v:.2f}"),
             ("total_tokens", 1e-3, "Tokens per prompt (thousands)", lambda v: f"{v:.1f}k" if v > 1 else f"{v*1000:.0f}")]
    for ax, (c, k, ttl, f) in zip(axs, specs):
        vb = [CIB[(q, c)][0] * k for q in QS]
        vi = [CIB[(q, c)][1] * k for q in QS]
        eb = ([CIB[(q, c)][2][0] * k for q in QS], [CIB[(q, c)][2][1] * k for q in QS])
        ei = ([CIB[(q, c)][3][0] * k for q in QS], [CIB[(q, c)][3][1] * k for q in QS])
        grouped(ax, vb, vi, f, eb, ei, title=ttl)
        xmult(ax, vb, vi)
    save(fig, "01_cost_per_prompt.png")


# ============================================================================= 02 whole run
def whole_run():
    fig, axs = plt.subplots(1, 3, figsize=(16, 6.4))
    fig.subplots_adjust(left=0.05, right=0.99, top=0.76, bottom=0.17, wspace=0.22)
    header(fig, "Whole-benchmark bill: 1,000 prompts per mode per quantization",
           "Totals as actually run (pilot included), from runs.csv. The verifier turns a 1.6–2.0 h job into 10–13 h; "
           "across the three runs it added 29 h and R32.59 of electricity.", cost=True)
    mode_legend(fig, 0.9)
    wq = W.loc[QS]
    grouped(axs[0], wq.baseline_hours.values, wq.intervention_hours.values, lambda v: f"{v:.1f} h", title="Wall-clock time (hours)")
    grouped(axs[1], wq.baseline_rand.values, wq.intervention_rand.values, lambda v: f"R{v:.2f}", title="Electricity cost (Rand incl. VAT)")
    grouped(axs[2], wq.baseline_wh.values / 1000, wq.intervention_wh.values / 1000, lambda v: f"{v:.2f}", title="Energy (kWh, GPU + CPU)")
    for ax, c in zip(axs, ("hours", "rand", "wh")):
        xmult(ax, wq[f"baseline_{c}"].values, wq[f"intervention_{c}"].values)
    save(fig, "02_whole_run_time_and_rand.png")


# ============================================================================= 03 cost per outcome
def per_outcome():
    fig, axs = plt.subplots(2, 2, figsize=(14.5, 9.4))
    fig.subplots_adjust(left=0.06, right=0.99, top=0.8, bottom=0.12, hspace=0.62, wspace=0.2)
    header(fig, "Price of a good outcome", "Total cost ÷ outcomes: what one correct answer, one prevented hallucination "
           "and one extra correct answer cost in electricity and in time.", cost=True)
    mode_legend(fig, 0.9)
    h = H.loc[QS]
    grouped(axs[0, 0], h.baseline_rand_per_correct * 100, h.intervention_rand_per_correct * 100, lambda v: f"{v:.2f}c",
            title="Electricity per correct answer delivered (cents)")
    xmult(axs[0, 0], h.baseline_rand_per_correct.values, h.intervention_rand_per_correct.values)
    grouped(axs[0, 1], h.baseline_sec_per_correct, h.intervention_sec_per_correct, lambda v: f"{v:.0f}s",
            title="Time per correct answer delivered (seconds)")
    xmult(axs[0, 1], h.baseline_sec_per_correct.values, h.intervention_sec_per_correct.values)
    for ax, col, ttl, f in ((axs[1, 0], "extra_rand_per_hallucination_prevented", "Extra electricity per hallucination prevented (cents)", lambda v: f"{v:.2f}c"),
                            (axs[1, 1], "extra_min_per_hallucination_prevented", "Extra time per hallucination prevented (minutes)", lambda v: f"{v:.2f} min")):
        vals = h[col].values * (100 if "rand" in col else 1)
        ax.bar(XQ, vals, 0.5, color=CA, zorder=3)
        for x, v in zip(XQ, vals):
            ax.text(x, v + max(vals) * 0.015, f(v), ha="center", va="bottom", fontsize=10.5)
        ax.set_xticks(XQ); ax.set_xticklabels(QS, fontsize=11); ax.tick_params(axis="x", length=0)
        ax.set_ylim(0, max(vals) * 1.25); clean_ax(ax, "y")
        ax.set_title(ttl, loc="left", fontsize=12, fontweight="bold", pad=10)
    for ax in axs[1]:
        pass
    # annotate extra correct answer
    for q, x in zip(QS, XQ):
        axs[1, 0].text(x, -max(h.extra_rand_per_hallucination_prevented * 100) * 0.16,
                       f"+{int(h.loc[q,'extra_correct_answers'])} extra correct\n−{int(h.loc[q,'hallucinations_prevented'])} hallucinations",
                       ha="center", va="top", fontsize=8.8, color=INK2)
        axs[1, 1].text(x, -max(h.extra_min_per_hallucination_prevented) * 0.16,
                       f"{h.loc[q,'extra_min_per_extra_correct']:.1f} min / extra\ncorrect answer",
                       ha="center", va="top", fontsize=8.8, color=INK2)
    save(fig, "03_price_of_a_good_outcome.png")


# ============================================================================= 04 frontier
def frontier():
    fig, axs = plt.subplots(1, 2, figsize=(15, 6.8))
    fig.subplots_adjust(left=0.065, right=0.985, top=0.86, bottom=0.14, wspace=0.16)
    header(fig, "Cost versus quality frontier", "Each marker is one run. The arrow shows what adding the verifier does: "
           "a lot more cost, far fewer hallucinations, more correct code.", cost=True)
    mk = {"Q4_K_M": "o", "Q6_K": "s", "Q8_0": "^"}
    for ax, (ycol_b, ycol_i, yl, good) in zip(axs, (("baseline_correct_delivered", "intervention_correct_delivered", "Correct code reaching the user (%)", "up"),
                                                     ("baseline_hallucinations_to_user", "intervention_hallucinations_to_user", "Hallucinated code reaching the user (%)", "down"))):
        for q in QS:
            xb, xi = H.loc[q, "baseline_rand_per_1000"], H.loc[q, "intervention_rand_per_1000"]
            yb, yi = H.loc[q, ycol_b] / 990 * 100, H.loc[q, ycol_i] / 990 * 100
            ax.annotate("", xy=(xi, yi), xytext=(xb, yb), arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.3, shrinkA=9, shrinkB=9), zorder=2)
            ax.scatter([xb], [yb], s=170, color=BASE, marker=mk[q], zorder=3, edgecolor=SURF, linewidth=1.8)
            ax.scatter([xi], [yi], s=170, color=CA, marker=mk[q], zorder=3, edgecolor=SURF, linewidth=1.8)
            ax.text(xb + 0.5, yb + (({"Q4_K_M": 0, "Q6_K": 1.2, "Q8_0": -1.2}) if good == "up" else {"Q4_K_M": 0.8, "Q6_K": -2.4, "Q8_0": 2.0})[q], q, ha="left", va="center", fontsize=9, color=INK2)
            ax.text(xi, yi + 3.2, q, ha="center", fontsize=9, color=INK2)
        ax.set_xlabel("Electricity per 1,000 prompts (Rand incl. VAT)")
        ax.set_ylabel(yl)
        ax.set_xlim(0, 17)
        ax.set_ylim(-3, 62)
        clean_ax(ax, "both")
    h = [Line2D([0], [0], marker="o", color="none", markerfacecolor=BASE, markersize=11, label="Baseline"),
         Line2D([0], [0], marker="o", color="none", markerfacecolor=CA, markersize=11, label="Confident Agent")]
    fig.legend(handles=h, loc="upper right", bbox_to_anchor=(0.985, 0.97), ncol=2, fontsize=10)
    save(fig, "04_cost_vs_quality_frontier.png")


# ============================================================================= 05 ECDF
def ecdf():
    fig, axs = plt.subplots(1, 2, figsize=(15, 6.2))
    fig.subplots_adjust(left=0.06, right=0.985, top=0.76, bottom=0.15, wspace=0.14)
    header(fig, "Every prompt's cost, not just the average",
           "Cumulative share of prompts at or below a given cost (log axis). The two modes barely overlap: "
           "the cheapest verified prompt costs more than the typical baseline one.", cost=True)
    ls = {"Q4_K_M": "-", "Q6_K": "--", "Q8_0": ":"}
    for ax, (col, scale, xl) in zip(axs, (("duration_s", 1, "Seconds per prompt"), ("rand", 100, "Electricity per prompt (cents, incl. VAT)"))):
        for q in QS:
            d = P[P.quantization == q]
            for m, c in (("b", BASE), ("i", CA)):
                v = np.sort(d[f"{m}_{col}"].values * scale)
                ax.plot(v, np.arange(1, len(v) + 1) / len(v) * 100, color=c, ls=ls[q], lw=2.1)
        ax.set_xscale("log")
        ax.set_xlabel(xl)
        ax.set_ylabel("Share of prompts (%)")
        clean_ax(ax, "both")
        for m, c, nm in (("b", BASE, "baseline"), ("i", CA, "CA")):
            med = P[f"{m}_{col}"].median() * scale
            ax.axvline(med, color=c, lw=0.8, alpha=0.5)
            ax.text(med, 3, f" median {nm}: {med:.2f}" if scale > 1 else f" median {nm}: {med:.1f}s", color=INK2, fontsize=8.5, rotation=90, va="bottom", ha="right")
    h = [Line2D([0], [0], color=BASE, lw=2.5, label="Baseline"), Line2D([0], [0], color=CA, lw=2.5, label="Confident Agent")]
    h += [Line2D([0], [0], color=INK2, ls=ls[q], lw=1.8, label=q) for q in QS]
    fig.legend(handles=h, loc="upper right", bbox_to_anchor=(0.985, 0.885), ncol=5, fontsize=9.5)
    save(fig, "05_cost_distribution_ecdf.png")


# ============================================================================= 06 where the time goes
def time_goes():
    fig, axs = plt.subplots(1, 3, figsize=(16.5, 6.4))
    fig.subplots_adjust(left=0.05, right=0.99, top=0.76, bottom=0.15, wspace=0.25)
    header(fig, "Where the extra time and tokens come from",
           "The verifier loop re-sends the growing conversation on every turn: ~21,000 prompt tokens per task versus ~160, "
           "so latency tracks context size.", cost=True)
    ax = axs[0]
    bm = [P[P.quantization == q].b_model_s.mean() for q in QS]
    im = [P[P.quantization == q].i_model_s.mean() for q in QS]
    it = [P[P.quantization == q].i_tool_s.mean() for q in QS]
    ax.bar(XQ - BW / 2 - 0.01, bm, BW, color=BASE, zorder=3, label="Model (baseline)")
    ax.bar(XQ + BW / 2 + 0.01, im, BW, color=CA, zorder=3, label="Model (verified)")
    ax.bar(XQ + BW / 2 + 0.01, it, BW, bottom=im, color=lighten(CA, 0.55), zorder=3, label="Verifier tool")
    for x, b, m, t in zip(XQ, bm, im, it):
        ax.text(x - BW / 2 - 0.01, b + 0.8, f"{b:.1f}s", ha="center", fontsize=9.5)
        ax.text(x + BW / 2 + 0.01, m / 2, f"{m:.1f}s", ha="center", va="center", fontsize=9.5, color="white")
        ax.text(x + BW / 2 + 0.01, m + t + 0.8, f"{t:.1f}s tool\n= {t/(m+t)*100:.0f}%", ha="center", va="bottom", fontsize=8.5, color=INK2)
    ax.set_xticks(XQ); ax.set_xticklabels(QS); ax.set_ylim(0, 62); clean_ax(ax, "y")
    ax.set_title("Seconds per prompt, split by who is working", loc="left", fontsize=12, fontweight="bold", pad=10)
    ax.legend(loc="upper left", fontsize=8.8)
    ax = axs[1]
    for k, (nm, col, off) in enumerate((("b", BASE, -1), ("i", CA, 1))):
        pt = [P[P.quantization == q][f"{nm}_prompt_tokens"].mean() / 1000 for q in QS]
        ct = [P[P.quantization == q][f"{nm}_completion_tokens"].mean() / 1000 for q in QS]
        ax.bar(XQ + off * (BW / 2 + 0.01), pt, BW, color=col, zorder=3)
        ax.bar(XQ + off * (BW / 2 + 0.01), ct, BW, bottom=pt, color=lighten(col, 0.55), zorder=3)
        for x, a, b in zip(XQ, pt, ct):
            ax.text(x + off * (BW / 2 + 0.01), a + b + 0.4, f"{a:.1f}k in\n+{b:.2f}k out" if nm == "i" else f"{a*1000:.0f} in\n+{b*1000:.0f} out",
                    ha="center", va="bottom", fontsize=8.6)
    ax.set_xticks(XQ); ax.set_xticklabels(QS); ax.set_ylim(0, 33); clean_ax(ax, "y")
    ax.set_title("Tokens per prompt (thousands): input vs generated", loc="left", fontsize=12, fontweight="bold", pad=10)
    ax.legend(handles=[Patch(color=BASE, label="Baseline"), Patch(color=CA, label="Confident Agent"),
                       Patch(color="#c9c8c2", label="lighter = generated (output)")], loc="upper left", fontsize=8.8)
    ax = axs[2]
    for q in QS:
        d = P[P.quantization == q]
        ax.scatter(d.i_prompt_tokens / 1000, d.i_duration_s, s=10, color=QC[q], alpha=0.35, linewidths=0, label=q)
    rho = st.spearmanr(P.i_prompt_tokens, P.i_duration_s)
    ax.text(0.03, 0.95, f"Spearman ρ = {rho.statistic:.2f}\n(all 2,970 verified prompts)", transform=ax.transAxes, va="top", fontsize=10, color=INK2)
    ax.set_xlabel("Input tokens in the verified run (thousands)")
    ax.set_ylabel("Seconds for the prompt")
    ax.set_title("Cost follows context length", loc="left", fontsize=12, fontweight="bold", pad=10)
    clean_ax(ax, "both")
    ax.legend(loc="lower right", fontsize=9, markerscale=2)
    save(fig, "06_where_the_time_goes.png")
    return rho


# ============================================================================= 07 spend by outcome
def spend():
    fig = plt.figure(figsize=(16, 7.4))
    gs = GridSpec(1, 2, left=0.16, right=0.985, top=0.82, bottom=0.27, wspace=0.27, width_ratios=[1.45, 1])
    header(fig, "Where the Confident Agent's time and money go",
           "Time spent on each kind of outcome. Work that ends in a withheld answer still costs the full loop: "
           "the bill for the ~39% of prompts the verifier refuses to deliver.", cost=True)
    cols = {"Delivered, correct": "#2a78d6", "Delivered, wrong (A/B/runtime)": "#898781",
            "Withheld, was hallucination (good catch)": "#6250d6", "Withheld, was correct (false alarm)": "#eb6834",
            "Withheld, other (B / runtime failure)": "#eda100"}
    ax = fig.add_subplot(gs[0, 0])
    ylab = []
    for qi, q in enumerate(QS[::-1]):
        left = 0
        d = sp[sp.quantization == q].set_index("spend_cat")
        tot = d.hours.sum()
        for c in CATS:
            hrs = d.hours.get(c, 0)
            ax.barh(qi, hrs, left=left, color=cols[c], height=0.62, edgecolor=SURF, linewidth=2, zorder=3)
            if hrs / tot > 0.045:
                ax.text(left + hrs / 2, qi, f"{hrs:.1f} h\nR{d.rand.get(c,0):.2f}", ha="center", va="center", fontsize=9, color="white", fontweight="bold")
            left += hrs
        ax.text(left + 0.2, qi, f"{tot:.1f} h\nR{d.rand.sum():.2f}", va="center", fontsize=9.5, color=INK, fontweight="bold")
    ax.set_yticks(range(3)); ax.set_yticklabels(QS[::-1], fontsize=12)
    ax.set_xlabel("Hours of verified processing (990 tasks)")
    ax.set_xlim(0, 15.5)
    clean_ax(ax, "x")
    ax.set_title("Time and electricity by outcome", loc="left", fontsize=12, fontweight="bold", pad=10)
    ax.legend(handles=[Patch(color=cols[c], label=c) for c in CATS], loc="upper center", bbox_to_anchor=(0.45, -0.2), ncol=3, fontsize=8.8)
    ax = fig.add_subplot(gs[0, 1])
    pooled = sp.groupby("spend_cat").agg(prompts=("prompts", "sum"), hours=("hours", "sum"), rand=("rand", "sum"))
    pooled["mean_s"] = pooled.hours * 3600 / pooled.prompts
    y = np.arange(len(CATS))[::-1]
    for yy, c in zip(y, CATS):
        v = pooled.mean_s.get(c, 0)
        ax.barh(yy, v, color=cols[c], height=0.6, zorder=3)
        ax.text(v + 0.8, yy, f"{v:.0f} s   (n={int(pooled.prompts.get(c,0))})", va="center", fontsize=9.5)
    ax.set_yticks([]); ax.set_xlim(0, 80); clean_ax(ax, "x")
    ax.set_xlabel("Mean seconds per prompt (3 runs pooled)")
    ax.set_title("Unit cost of each outcome", loc="left", fontsize=12, fontweight="bold", pad=10)
    save(fig, "07_intervention_spend_by_outcome.png")


# ============================================================================= 08 corrections
def corrections():
    fig, axs = plt.subplots(1, 3, figsize=(16.5, 6.2))
    fig.subplots_adjust(left=0.055, right=0.99, top=0.76, bottom=0.15, wspace=0.26)
    header(fig, "Each correction round costs more time, but how often does it pay off?",
           "Prompts grouped by how many corrections the agent made after the verifier objected "
           "(0–3, three runs pooled). Harder tasks need more rounds, so read this as marginal cost, not cause.", cost=True)
    c = cr.set_index("i_correction_count")
    x = np.arange(4)
    ax = axs[0]
    ax.bar(x, c.mean_s, 0.6, color=CA, zorder=3)
    for xi, v, n, r_ in zip(x, c.mean_s, c.prompts, c.rand_per_1000):
        ax.text(xi, v + 1, f"{v:.0f}s\nR{r_:.1f}/1k", ha="center", va="bottom", fontsize=9.5)
        ax.text(xi, 1.5, f"n={int(n)}", ha="center", fontsize=8.5, color="white")
    ax.set_xticks(x); ax.set_xticklabels(["0", "1", "2", "3"]); ax.set_xlabel("Correction rounds")
    ax.set_ylim(0, 90); clean_ax(ax, "y")
    ax.set_title("Seconds per prompt (and R per 1,000)", loc="left", fontsize=12, fontweight="bold", pad=10)
    ax = axs[1]
    for col, nm, col_c in (("correct_to_user", "Correct code reaches user", BASE), ("withheld", "Withheld", "#898781"), ("halluc_to_user", "Hallucination reaches user", BAD)):
        ax.plot(x, c[col] * 100, marker="o", ms=8, lw=2.2, color=col_c)
        for xi, v in zip(x, c[col] * 100):
            ax.text(xi, v + (-7 if (col == "halluc_to_user" and v < 2) else 3.2), f"{v:.0f}%", ha="center", fontsize=9, color=INK2)
        ax.plot([], [], marker="o", color=col_c, label=nm)
    ax.set_xlim(-0.2, 3.3); ax.set_ylim(-11, 108); ax.legend(loc="upper left", fontsize=8.8, bbox_to_anchor=(0.0, 1.0))
    ax.set_xticks(x); ax.set_xlabel("Correction rounds"); ax.set_ylabel("Share of prompts (%)"); clean_ax(ax, "y")
    ax.set_title("Outcome by correction rounds", loc="left", fontsize=12, fontweight="bold", pad=10)
    ax = axs[2]
    g = P.groupby("i_correction_count")
    spc = g.i_duration_s.sum() / g.i_correct.sum()
    ax.bar(x, spc.values, 0.6, color="#6250d6", zorder=3)
    for xi, v in zip(x, spc.values):
        ax.text(xi, v + 4, f"{v:.0f}s\n({v/spc.iloc[0]:.1f}×)", ha="center", va="bottom", fontsize=9.5)
    ax.set_xticks(x); ax.set_xlabel("Correction rounds"); ax.set_ylim(0, max(spc.values) * 1.25); clean_ax(ax, "y")
    ax.set_title("Seconds per correct answer delivered", loc="left", fontsize=12, fontweight="bold", pad=10)
    pd.DataFrame({"seconds_per_correct": spc}).to_csv(TB / "07b_seconds_per_correct_by_correction_rounds.csv")
    save(fig, "08_correction_rounds_marginal_cost.png")
    return spc


# ============================================================================= 09 by API
def by_api():
    apis = ["DummyJSON", "GitHub", "JSONPlaceholder", "Open-Meteo", "Petstore", "REST Countries"]
    a = API.loc[apis]
    xa = np.arange(len(apis))
    fig, axs = plt.subplots(2, 2, figsize=(15, 9.6))
    fig.subplots_adjust(left=0.06, right=0.99, top=0.8, bottom=0.12, hspace=0.55, wspace=0.17)
    header(fig, "Cost and quality by API", "Three runs pooled (≈ 148–248 tasks per API per run). "
           "REST Countries: the verifier withheld essentially everything, so the whole bill bought no delivered code.", cost=True)
    mode_legend(fig, 0.9)

    def g2(ax, vb, vi, f, ttl, ylab=None, mx=None):
        ax.bar(xa - BW / 2 - 0.01, np.nan_to_num(vb), BW, color=BASE, zorder=3)
        ax.bar(xa + BW / 2 + 0.01, np.nan_to_num(vi), BW, color=CA, zorder=3)
        top = mx or np.nanmax(np.r_[vb, vi])
        
        for x_, b, i in zip(xa, vb, vi):
            for dx, v in ((-BW / 2 - 0.01, b), (BW / 2 + 0.01, i)):
                if not np.isnan(v) and v > 0:
                    ax.text(x_ + dx, v + top * 0.012, f(v), ha="center", va="bottom", fontsize=8.5)
        ax.set_xticks(xa); ax.set_xticklabels([t.replace("JSONPlaceholder", "JSON\nPlaceholder").replace("REST Countries", "REST\nCountries") for t in apis], fontsize=9.5)
        ax.set_ylim(0, top * 1.2); clean_ax(ax, "y"); ax.tick_params(axis="x", length=0)
        ax.set_title(ttl, loc="left", fontsize=12, fontweight="bold", pad=10)

    g2(axs[0, 0], a.b_mean_s.values, a.i_mean_s.values, lambda v: f"{v:.0f}s", "Seconds per prompt")
    g2(axs[0, 1], API.loc[apis].eval("b_hall*100").values, API.loc[apis].eval("i_hall*100").values, lambda v: f"{v:.0f}%", "Hallucinated code reaching the user (%)", mx=100)
    cb = np.array([a.b_correct_n[k] / 2970 * 0 + a.b_correct_n[k] / (P.api == k).sum() * 100 for k in apis])
    ci = np.array([a.i_correct_n[k] / (P.api == k).sum() * 100 for k in apis])
    g2(axs[1, 0], cb, ci, lambda v: f"{v:.0f}%", "Correct code reaching the user (%)", mx=100)
    vb = (a.b_rand_per_correct * 100).values
    vi = (a.i_rand_per_correct * 100).values
    g2(axs[1, 1], vb, vi, lambda v: f"{v:.2f}c", "Electricity per correct answer delivered (cents)")
    for k, (b, i) in enumerate(zip(vb, vi)):
        if np.isnan(i) or np.isnan(b):
            axs[1, 1].text(xa[k], np.nanmax(vi) * 1.6, "no correct\ncode delivered" if np.isnan(i) else "no correct\nbaseline code", ha="center", fontsize=8.5, color=BAD, fontweight="bold")
    save(fig, "09_cost_and_quality_by_api.png")


# ============================================================================= 10 heatmaps
def heatmaps():
    dims = [("api", "API"), ("operation_category", "Operation"), ("auth_type", "Auth"), ("spec_source", "Spec"), ("difficulty", "Difficulty")]
    rows, labels, ns = [], [], []
    for col, nm in dims:
        for g, d in P.groupby(col):
            labels.append(f"{nm}: {g}")
            ns.append(len(d) // 3)
            rows.append([(d[d.quantization == q][c].mean() * 100) for q in QS for c in (("b_hall", "i_hall"), ("b_correct_i", "i_correct"))[0]])
    # build explicit matrices
    def mat(bcol, icol):
        out = []
        for col, nm in dims:
            for g, d in P.groupby(col):
                r = []
                for q in QS:
                    dq = d[d.quantization == q]
                    r += [dq[bcol].mean() * 100, dq[icol].mean() * 100]
                out.append(r)
        return np.array(out)
    mh = mat("b_hall", "i_hall")
    mc = mat("b_correct_i", "i_correct")
    ab = np.array([[d[d.quantization == q].i_withheld.mean() * 100 for q in QS] for col, nm in dims for g, d in P.groupby(col)])
    fig, axs = plt.subplots(1, 3, figsize=(17.5, 10.5), gridspec_kw={"width_ratios": [1, 1, 0.55]})
    fig.subplots_adjust(left=0.2, right=0.985, top=0.86, bottom=0.07, wspace=0.07)
    header(fig, "Where it works and where it struggles", "Rates per subgroup (rows) and run (columns); B = baseline, CA = Confident Agent. "
           "Cells with fewer than 30 prompts (e.g. 'hard', 9 tasks) are noisy.")
    xt = [f"{q}\n{m}" for q in QS for m in ("B", "CA")]
    for ax, M, ttl, hue in ((axs[0], mh, "Hallucinated code reaching the user (%)", CA), (axs[1], mc, "Correct code reaching the user (%)", BASE)):
        ax.imshow(M, cmap=seq_cmap(hue), vmin=0, vmax=100, aspect="auto")
        ax.grid(False)
        for r in range(M.shape[0]):
            for c in range(M.shape[1]):
                v = M[r, c]
                ax.text(c, r, f"{v:.0f}", ha="center", va="center", fontsize=8.5, color="white" if v > 58 else INK)
        ax.set_xticks(range(6)); ax.set_xticklabels(xt, fontsize=8.5)
        ax.xaxis.tick_top()
        ax.set_title(ttl, fontsize=11.5, fontweight="bold", pad=34, loc="left")
        for s in ax.spines.values():
            s.set_visible(False)
        for c in (1.5, 3.5):
            ax.axvline(c, color=SURF, lw=4)
    axs[0].set_yticks(range(len(labels))); axs[0].set_yticklabels([f"{l}  (n={n})" for l, n in zip(labels, ns)], fontsize=9)
    axs[1].set_yticks([])
    ax = axs[2]
    ax.imshow(ab, cmap=seq_cmap("#6250d6"), vmin=0, vmax=100, aspect="auto"); ax.grid(False)
    for r in range(ab.shape[0]):
        for c in range(3):
            ax.text(c, r, f"{ab[r,c]:.0f}", ha="center", va="center", fontsize=8.5, color="white" if ab[r, c] > 58 else INK)
    ax.set_xticks(range(3)); ax.set_xticklabels(QS, fontsize=8.5); ax.xaxis.tick_top(); ax.set_yticks([])
    ax.set_title("Withheld by the verifier (%)", fontsize=11.5, fontweight="bold", pad=34, loc="left")
    for s in ax.spines.values():
        s.set_visible(False)
    save(fig, "10_subgroup_heatmaps.png")
    pd.DataFrame(np.c_[mh, mc, ab], index=labels, columns=[f"halluc_{q}_{m}" for q in QS for m in ("B", "CA")] +
                 [f"correct_{q}_{m}" for q in QS for m in ("B", "CA")] + [f"withheld_{q}" for q in QS]).round(1).to_csv(TB / "20_subgroup_heatmap_values.csv")


# ============================================================================= 11 verifier
def verifier():
    fig = plt.figure(figsize=(16, 9.4))
    gs = GridSpec(2, 6, left=0.055, right=0.985, top=0.8, bottom=0.08, hspace=0.62, wspace=1.0)
    header(fig, "Is the verifier a good hallucination detector?",
           "Positive = final candidate is a hallucination (class A); predicted positive = withheld. "
           "Recall 94–96%: it rarely lets a hallucination through, but it also withholds some good work (20–28 correct answers per run).", cost=True)
    ax = fig.add_subplot(gs[0, :4])
    mets = [("recall", "Recall\n(hallucinations caught)"), ("precision", "Precision\n(withheld ones were bad)"), ("specificity", "Specificity\n(good code delivered)"), ("f1", "F1")]
    xm = np.arange(len(mets))
    w = 0.26
    for k, q in enumerate(QS):
        v = [vd.loc[q, m] * 100 for m, _ in mets]
        ax.bar(xm + (k - 1) * w, v, w * 0.92, color=QC[q], zorder=3, label=q)
        for x, vv in zip(xm + (k - 1) * w, v):
            ax.text(x, vv + 1, f"{vv:.0f}", ha="center", fontsize=8.8)
    ax.set_xticks(xm); ax.set_xticklabels([m[1] for m in mets], fontsize=10); ax.set_ylim(0, 110); ax.set_ylabel("%")
    clean_ax(ax, "y"); ax.legend(ncol=3, loc="lower center", fontsize=9.5, bbox_to_anchor=(0.5, -0.4))
    ax.set_title("Detector quality (target: class A)", loc="left", fontsize=12, fontweight="bold", pad=8)
    ax = fig.add_subplot(gs[0, 4:])
    fc = pd.DataFrame(fp_cost).set_index("quantization")
    ax.bar(XQ - 0.2, fc.FP_hours, 0.38, color="#eb6834", zorder=3, label="False alarms (non-hallucination withheld)")
    ax.bar(XQ + 0.2, fc.FN_hours, 0.38, color="#898781", zorder=3, label="Misses (hallucination delivered)")
    for x, a, b, fa, fb in zip(XQ, fc.FP_hours, fc.FN_hours, fc.FP_n, fc.FN_n):
        ax.text(x - 0.2, a + 0.03, f"{a:.2f}h\nn={fa}", ha="center", fontsize=8.5)
        ax.text(x + 0.2, b + 0.03, f"{b:.2f}h\nn={fb}", ha="center", fontsize=8.5)
    ax.set_xticks(XQ); ax.set_xticklabels(QS); ax.set_ylim(0, 1.6); clean_ax(ax, "y"); ax.set_ylabel("Hours of processing")
    ax.set_title("Time spent on the verifier's mistakes", loc="left", fontsize=12, fontweight="bold", pad=8)
    ax.legend(fontsize=8.3, loc="upper left")
    cmap = seq_cmap("#2a78d6")
    for k, q in enumerate(QS):
        ax = fig.add_subplot(gs[1, k * 2:(k + 1) * 2])
        r = vd.loc[q]
        M = np.array([[r.TP, r.FN], [r.FP, r.TN]])
        ax.imshow(M, cmap=cmap, vmin=0, vmax=700); ax.grid(False)
        lab = [["TP\nhallucination\nwithheld", "FN\nhallucination\ndelivered"], ["FP\nnon-hallucination\nwithheld", "TN\nnon-hallucination\ndelivered"]]
        for i in range(2):
            for j in range(2):
                ax.text(j, i, f"{int(M[i,j])}", ha="center", va="center", fontsize=17, fontweight="bold", color="white" if M[i, j] > 330 else INK)
                ax.text(j, i + 0.34, lab[i][j].split("\n", 1)[1].replace("\n", " "), ha="center", va="center", fontsize=6.8, color="white" if M[i, j] > 330 else INK2)
        ax.set_xticks([0, 1]); ax.set_xticklabels(["withheld", "delivered"][::1] if False else ["predicted bad\n(withheld)", "predicted ok\n(delivered)"], fontsize=8.5)
        ax.set_yticks([0, 1]); ax.set_yticklabels(["actually A", "not A"], fontsize=9)
        ax.set_xticks([0, 1]); ax.set_xticklabels(["withheld", "delivered"], fontsize=9)
        ax.set_title(q, fontsize=11.5, fontweight="bold", color=QC[q])
        for s in ax.spines.values():
            s.set_visible(False)
    # note: confusion matrix layout
    save(fig, "11_verifier_as_detector.png")


# ============================================================================= 12 ewcs
def ewcs():
    fig, axs = plt.subplots(1, 2, figsize=(14.5, 6.4))
    fig.subplots_adjust(left=0.06, right=0.985, top=0.78, bottom=0.13, wspace=0.17)
    header(fig, "The confidence score (EWCS) separates good code from hallucinations",
           "EWCS of the final candidate. ROC for 'correct' vs 'class A' (left) and score distributions with the report's bands (right).")
    ax = axs[0]
    for q in QS:
        f, t, a = roc[q]
        ax.plot(f, t, color=QC[q], lw=2.4, label=f"{q}  AUC {a:.3f}")
    ax.plot([0, 1], [0, 1], color=MUTED, ls="--", lw=1)
    ax.set_xlabel("False positive rate (hallucination scored as correct)"); ax.set_ylabel("True positive rate (correct code scored as correct)")
    ax.legend(loc="lower right", fontsize=10); clean_ax(ax, "both")
    ax.set_title("ROC", loc="left", fontsize=12, fontweight="bold", pad=8)
    ax = axs[1]
    dd = P[P.i_final_class.isin(["correct", "A", "B"]) & P.i_ewcs.notna()]
    bins = np.linspace(0, 1, 41)
    for cls, col, nm in (("correct", BASE, "Correct"), ("A", CA, "Hallucination (A)"), ("B", "#898781", "Wrong for task (B)")):
        v = dd[dd.i_final_class == cls].i_ewcs
        ax.hist(v, bins=bins, color=col, alpha=0.85 if cls != "B" else 0.55, label=f"{nm} (n={len(v)})", zorder=3, edgecolor=SURF, linewidth=0.5)
    for xv, tl in ((0.60, "0.60"), (0.85, "0.85")):
        ax.axvline(xv, color=INK2, ls=":", lw=1.2)
        ax.text(xv, ax.get_ylim()[1] * 0.98, f" {tl}", fontsize=9, va="top", color=INK2)
    ax.set_xlabel("EWCS of final candidate"); ax.set_ylabel("Prompts (3 runs pooled)")
    ax.legend(fontsize=9.5, loc="upper left"); clean_ax(ax, "y")
    ax.set_title("Score distribution", loc="left", fontsize=12, fontweight="bold", pad=8)
    save(fig, "12_confidence_score_roc.png")


# ============================================================================= 13 outcome flow
def outcomes():
    fig, axs = plt.subplots(1, 2, figsize=(16, 6.6), gridspec_kw={"width_ratios": [1.35, 1]})
    fig.subplots_adjust(left=0.115, right=0.985, top=0.86, bottom=0.2, wspace=0.14)
    header(fig, "What actually reaches the user", "Left: classification of what the user receives. Right: paired task-level changes "
           "(repairs vs regressions); every difference has exact McNemar p < 1e-19.")
    ax = axs[0]
    cats = [("correct", "Correct", BASE), ("A", "Hallucination (A)", BAD), ("B", "Valid call, wrong task (B)", "#eda100"),
            ("rf", "Crash / no code", "#898781"), ("withheld", "Withheld (nothing shown)", "#c3c2b7")]
    pos = []
    labels = []
    xi = 0
    for q in QS:
        d = P[P.quantization == q]
        for m in ("b", "i"):
            if m == "b":
                cl = d.b_class
                vals = {"correct": (cl == "correct").mean(), "A": (cl == "A").mean(), "B": (cl == "B").mean(),
                        "rf": cl.isin(["runtime_failure", "no_code"]).mean(), "withheld": 0}
            else:
                cl = d.i_shown_class
                vals = {"correct": (cl == "correct").mean(), "A": (cl == "A").mean(), "B": (cl == "B").mean(),
                        "rf": (cl == "runtime_failure").mean(), "withheld": (cl == "nothing_shown").mean()}
            left = 0
            for k, nm, col in cats:
                v = vals[k] * 100
                ax.barh(xi, v, left=left, color=col, height=0.7, edgecolor=SURF, linewidth=1.5, zorder=3)
                if v >= 4:
                    ax.text(left + v / 2, xi, f"{v:.0f}%", ha="center", va="center", fontsize=9, color="white" if k in ("correct", "A", "rf") else INK, fontweight="bold")
                left += v
            labels.append(f"{q}  {'baseline' if m == 'b' else 'CA'}")
            pos.append(xi)
            xi += 1
        xi += 0.5
    ax.set_yticks(pos); ax.set_yticklabels(labels, fontsize=10); ax.invert_yaxis(); ax.set_xlim(0, 100); ax.set_xlabel("% of 990 tasks")
    clean_ax(ax, "x")
    ax.legend(handles=[Patch(color=c, label=n) for _, n, c in cats], loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=5, fontsize=8.8)
    ax = axs[1]
    pr = []
    for q in QS:
        d = P[P.quantization == q]
        pr.append((q, (d.pair_hallucination == "repair").sum(), (d.pair_hallucination == "regression").sum(),
                   (d.pair_correct == "repair").sum(), (d.pair_correct == "regression").sum()))
    y0 = np.arange(len(QS)) * 2.4
    for k, (q, hr, hg, cr_, cg) in enumerate(pr):
        for off, rep, reg, nm in ((0.55, hr, hg, "hallucination"), (-0.35, cr_, cg, "correct")):
            ax.barh(y0[k] + off, rep, height=0.7, color=BASE if nm == "correct" else CA, zorder=3)
            ax.barh(y0[k] + off, -reg, height=0.7, color="#898781", zorder=3)
            ax.text(rep + 8, y0[k] + off, f"+{rep}", va="center", fontsize=9.5)
            ax.text(-reg - 8, y0[k] + off, f"−{reg}", va="center", ha="right", fontsize=9.5, color=INK2)
        ax.text(-640, y0[k] + 0.1, q, fontsize=11, fontweight="bold", color=QC[q], ha="left")
    ax.axvline(0, color=INK2, lw=1)
    ax.set_yticks([]); ax.set_xlim(-650, 650); ax.invert_yaxis()
    ax.set_xlabel("Tasks   ← regressions | repairs →"); clean_ax(ax, "x")
    ax.legend(handles=[Patch(color=CA, label="Hallucination repaired"), Patch(color=BASE, label="Correct code newly reaching user"),
                       Patch(color="#898781", label="Regression")], loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=3, fontsize=8.8)
    save(fig, "13_what_reaches_the_user.png")


# ============================================================================= 14 unit economics
def unit_econ():
    fig, axs = plt.subplots(2, 2, figsize=(14.5, 9.4))
    fig.subplots_adjust(left=0.06, right=0.99, top=0.8, bottom=0.07, hspace=0.55, wspace=0.18)
    header(fig, "Throughput per hour and per Rand", "How much each hour of GPU time and each rand of electricity buys.", cost=True)
    mode_legend(fig, 0.9)
    u = UE.set_index(["mode", "quantization"])
    for ax, col, ttl, f in ((axs[0, 0], "prompts_per_hour", "Prompts processed per hour", lambda v: f"{v:.0f}"),
                            (axs[0, 1], "prompts_per_R1", "Prompts processed per R1 of electricity", lambda v: f"{v:.0f}"),
                            (axs[1, 0], "correct_per_hour", "Correct answers delivered per hour", lambda v: f"{v:.1f}"),
                            (axs[1, 1], "correct_per_R1", "Correct answers delivered per R1 of electricity", lambda v: f"{v:.0f}")):
        vb = [u.loc[("baseline", q), col] for q in QS]
        vi = [u.loc[("intervention", q), col] for q in QS]
        grouped(ax, vb, vi, f, title=ttl)
        for x, b, i in zip(XQ, vb, vi):
            ax.text(x, ax.get_ylim()[1] * 0.985, f"{b/i:.1f}× fewer", ha="center", va="top", fontsize=10.5, fontweight="bold", color=CA)
    save(fig, "14_unit_economics.png")


# ============================================================================= 15 forest
def forest():
    fig, axs = plt.subplots(1, 2, figsize=(16, 7.2), gridspec_kw={"width_ratios": [1.2, 1]})
    fig.subplots_adjust(left=0.13, right=0.985, top=0.84, bottom=0.13, wspace=0.28)
    header(fig, "Effect sizes with confidence intervals",
           "Left: intervention ÷ baseline ratio of means (paired bootstrap 95% CI). Right: change in outcome, percentage points (paired bootstrap).")
    ax = axs[0]
    mets = [("duration_s", "Time"), ("energy_j", "Energy / electricity"), ("completion_tokens", "Generated tokens"), ("total_tokens", "All tokens")]
    y = 0
    yt, yl = [], []
    for c, nm in mets:
        for q in QS:
            b, i, bci, ici, rci = CIB[(q, c)]
            r = i / b
            ax.plot(rci, [y, y], color=QC[q], lw=3, solid_capstyle="round", zorder=3)
            ax.scatter([r], [y], s=70, color=QC[q], zorder=4, edgecolor=SURF)
            ax.text(rci[1] * 1.04, y, f"{r:.1f}×", va="center", fontsize=9, color=INK2)
            y += 1
        yt.append(y - 2); yl.append(nm)
        y += 0.8
    ax.set_xscale("log"); ax.axvline(1, color=INK2, lw=1)
    ax.set_yticks(yt); ax.set_yticklabels(yl, fontsize=11); ax.invert_yaxis()
    ax.set_xlabel("Ratio, Confident Agent ÷ baseline (log scale; 1 = no change)")
    ax.set_xlim(2.5, 70)
    ax.set_xticks([3, 5, 10, 20, 40, 60]); ax.set_xticklabels(["3×", "5×", "10×", "20×", "40×", "60×"]); ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    clean_ax(ax, "x")
    ax.legend(handles=[Line2D([0], [0], color=QC[q], lw=3, label=q) for q in QS], loc="center right", fontsize=9.5)
    ax.minorticks_off()
    ax.set_title("Cost ratios (all Wilcoxon p < 1e-160)", loc="left", fontsize=12, fontweight="bold", pad=8)
    ax = axs[1]
    y = 0
    yt, yl = [], []
    for lab in ("Hallucination reaching user", "Correct code reaching user"):
        for q in QS:
            r = T4[(T4.quantization == q) & (T4.outcome == lab)].iloc[0]
            ax.plot([r.ci_low, r.ci_high], [y, y], color=QC[q], lw=3, solid_capstyle="round")
            ax.scatter([r["diff_pp(int-base)"]], [y], s=70, color=QC[q], zorder=4, edgecolor=SURF)
            ax.text(r.ci_high + 2 if r["diff_pp(int-base)"] > 0 else r.ci_low - 2, y, f"{r['diff_pp(int-base)']:+.1f} pp",
                    va="center", ha="left" if r["diff_pp(int-base)"] > 0 else "right", fontsize=9, color=INK2)
            y += 1
        yt.append(y - 2); yl.append(lab.replace(" reaching user", "\nreaching user").replace(" reaching", "\nreaching"))
        y += 1
    ax.axvline(0, color=INK2, lw=1)
    ax.set_yticks(yt); ax.set_yticklabels(yl, fontsize=11); ax.invert_yaxis()
    ax.set_xlim(-72, 42); ax.set_xlabel("Change, Confident Agent − baseline (percentage points)")
    clean_ax(ax, "x")
    ax.set_title("Outcome changes (McNemar p < 1e-19 in all 6)", loc="left", fontsize=12, fontweight="bold", pad=8)
    save(fig, "15_effect_sizes_forest.png")


# ============================================================================= 16 energy anatomy
def energy():
    fig, axs = plt.subplots(2, 2, figsize=(15, 9.8))
    fig.subplots_adjust(left=0.06, right=0.99, top=0.8, bottom=0.07, hspace=0.5, wspace=0.18)
    header(fig, "Energy anatomy", "Measured by LibreHardwareMonitor on the GPU and the CPU package only; "
           "the wall socket draws more (motherboard, RAM, storage, PSU losses) so true bills would be somewhat higher.", cost=True)
    mode_legend(fig, 0.9)
    pw = PW.set_index(["mode", "quantization"])
    ax = axs[0, 0]
    for off, nm, col in ((-1, "baseline", BASE), (1, "intervention", CA)):
        g = [pw.loc[(nm, q), "gpu_wh_per_prompt"] for q in QS]
        c = [pw.loc[(nm, q), "cpu_wh_per_prompt"] for q in QS]
        ax.bar(XQ + off * (BW / 2 + 0.01), g, BW, color=col, zorder=3)
        ax.bar(XQ + off * (BW / 2 + 0.01), c, BW, bottom=g, color=lighten(col, 0.55), zorder=3)
        for x, gg, cc in zip(XQ, g, c):
            ax.text(x + off * (BW / 2 + 0.01), gg + cc + 0.05, f"{gg+cc:.2f} Wh", ha="center", fontsize=9)
    ax.set_xticks(XQ); ax.set_xticklabels(QS); ax.set_ylim(0, 4.4); clean_ax(ax, "y")
    ax.set_title("Energy per prompt (Wh): GPU dark, CPU light", loc="left", fontsize=12, fontweight="bold", pad=8)
    ax = axs[0, 1]
    pb = [pw.loc[("baseline", q), "mean_power_w"] for q in QS]
    pi = [pw.loc[("intervention", q), "mean_power_w"] for q in QS]
    grouped(ax, pb, pi, lambda v: f"{v:.0f} W", title="Average power draw during the run (W)", mult=False, ymax=420)
    for k, q in enumerate(QS):
        iw = pw.loc[("baseline", q), "idle_w_gpu_plus_cpu"]
        ax.plot([k - 0.45, k + 0.45], [iw, iw], color=INK2, ls="--", lw=1.2, zorder=5, label="idle draw, GPU + CPU (≈ 95 W)" if k == 0 else None)
    ax.legend(loc="upper left", fontsize=9, bbox_to_anchor=(0, 1.0))
    ax = axs[1, 0]
    tb = [pw.loc[("baseline", q), "completion_tok_per_s"] for q in QS]
    ti = [pw.loc[("intervention", q), "completion_tok_per_s"] for q in QS]
    grouped(ax, tb, ti, lambda v: f"{v:.0f}", title="Generation speed (output tokens / second)", mult=False)
    ax = axs[1, 1]
    jb = [pw.loc[("baseline", q), "J_per_1k_total_tokens"] for q in QS]
    ji = [pw.loc[("intervention", q), "J_per_1k_total_tokens"] for q in QS]
    grouped(ax, jb, ji, lambda v: f"{v:.0f} J", title="Energy per 1,000 tokens processed (Joules)", mult=False)
    ax.text(1.0, -0.13, "Input tokens are cheap (prefill): the verifier moves ~42× more tokens\nfor only ~6× the energy, so energy per token falls ~7×.",
            transform=ax.transAxes, ha="right", va="top", fontsize=8.8, color=INK2)
    save(fig, "16_energy_power_anatomy.png")


# ============================================================================= 17 timeline
def timeline():
    fig, axs = plt.subplots(2, 2, figsize=(15.5, 9), sharex=True)
    fig.subplots_adjust(left=0.065, right=0.985, top=0.86, bottom=0.08, hspace=0.14, wspace=0.12)
    header(fig, "Run profile: cost follows the task mix, not the clock",
           "Rolling median (50 prompts) in the order the tasks ran (shaded = API block). The same shape repeats in every quantization, "
           "so the swings are task difficulty, not throttling; Q8_0 sits highest throughout.")
    def blocks_for(m):
        ref = P[P.quantization == "Q6_K"].copy()
        ref["t"] = pd.to_datetime(ref[f"{m}_started"])
        ref = ref.sort_values("t").reset_index(drop=True)
        out, start = [], 0
        for k in range(1, len(ref) + 1):
            if k == len(ref) or ref.api[k] != ref.api[start]:
                out.append((start, k, ref.api[start]))
                start = k
        return out
    shades = ["#f1f0eb", "#fcfcfb"]
    for c, (m, nm) in enumerate((("b", "Baseline"), ("i", "Confident Agent"))):
        for r, (metric, yl) in enumerate((("duration_s", "Seconds per prompt"), ("energy_j", "Energy per prompt (J)"))):
            ax = axs[r, c]
            for bi, (a, b, nmapi) in enumerate(blocks_for(m)):
                ax.axvspan(a, b, color=shades[bi % 2], zorder=0)
                if r == 0:
                    ax.text((a + b) / 2, 1.01, nmapi.replace("JSONPlaceholder", "JSONPlace-\nholder").replace("REST Countries", "REST\nCountries"),
                            transform=ax.get_xaxis_transform(), ha="center", va="bottom", fontsize=8, color=INK2)
            for q in QS:
                d = P[P.quantization == q].copy()
                d["t"] = pd.to_datetime(d[f"{m}_started"])
                d = d.sort_values("t").reset_index(drop=True)
                ax.plot(d.index, d[f"{m}_{metric}"].rolling(50, min_periods=10).median(), color=QC[q], lw=1.8, label=q)
            clean_ax(ax, "y")
            ax.set_ylim(0, None)
            ax.set_xlim(0, 990)
            if c == 0:
                ax.set_ylabel(yl)
            if r == 1:
                ax.set_xlabel("Task order within the phase")
            if r == 0:
                ax.set_title(nm, loc="left", fontsize=12, fontweight="bold", pad=26)
    axs[1, 0].legend(ncol=3, fontsize=9.5, loc="upper left")
    save(fig, "17_run_profile_by_task_order.png")


# ============================================================================= 18 kinds
def kinds():
    kk = ekp.copy()
    kk = kk.sort_values("baseline", ascending=True)
    fig, ax = plt.subplots(figsize=(13, 6.2))
    fig.subplots_adjust(left=0.28, right=0.97, top=0.8, bottom=0.14)
    header(fig, "What kind of hallucination is it?", "Class A tasks by kind, three runs pooled (a task can have several kinds).\n"
           "Caveat: the intervention prompt names the correct hosts, so the 'wrong host' collapse is partly by design (benchmark README).")
    y = np.arange(len(kk))
    ax.barh(y + 0.19, kk.baseline, 0.36, color=BASE, zorder=3)
    ax.barh(y - 0.19, kk.intervention, 0.36, color=CA, zorder=3)
    for yy, b, i in zip(y, kk.baseline, kk.intervention):
        ax.text(b + 8, yy + 0.19, f"{int(b)}", va="center", fontsize=9.5)
        ax.text(i + 8, yy - 0.19, f"{int(i)}", va="center", fontsize=9.5)
    ax.set_yticks(y); ax.set_yticklabels(kk.index, fontsize=10)
    ax.set_xlabel("Tasks (990 × 3 runs)"); clean_ax(ax, "x")
    ax.legend(handles=[Patch(color=BASE, label="Baseline"), Patch(color=CA, label="Confident Agent (reaching user)")], loc="lower right", fontsize=10)
    save(fig, "18_hallucination_kinds.png")


# ============================================================================= 19 scaling
def scaling():
    fig, axs = plt.subplots(1, 3, figsize=(16.5, 6.4))
    fig.subplots_adjust(left=0.05, right=0.99, top=0.76, bottom=0.17, wspace=0.24)
    header(fig, "What it costs at scale", "Linear extrapolation of the measured per-prompt cost to 10,000 prompts "
           "(100,000 in the table: tables/18_unit_economics_and_scaling.csv). Assumes the same hardware and workload mix.", cost=True)
    mode_legend(fig, 0.9)
    u = UE.set_index(["mode", "quantization"])
    for ax, col, ttl, f in ((axs[0], "days_per_10000_prompts", "Days of continuous GPU time", lambda v: f"{v:.1f} d"),
                            (axs[1], "days_per_100000_prompts", "Days of GPU time (100,000 prompts: ×10)", lambda v: f"{v:.0f} d"),
                            (axs[2], "rand_per_10000_prompts", "Electricity (Rand incl. VAT)", lambda v: f"R{v:.0f}")):
        vb = [u.loc[("baseline", q), col] for q in QS]
        vi = [u.loc[("intervention", q), col] for q in QS]
        grouped(ax, vb, vi, f, title=ttl + ("" if "100,000" in ttl else " per 10,000 prompts"))
        xmult(ax, vb, vi)
    save(fig, "19_scaling_to_10000_prompts.png")


scorecard()
hero()
whole_run()
per_outcome()
frontier()
ecdf()
rho = time_goes()
spend()
spc = corrections()
by_api()
heatmaps()
verifier()
ewcs()
outcomes()
unit_econ()
forest()
energy()
timeline()
kinds()
scaling()
print("spearman prompt tokens vs duration:", rho)
print(spc)
