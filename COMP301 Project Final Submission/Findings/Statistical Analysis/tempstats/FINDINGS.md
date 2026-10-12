# Confident Agent: cost-of-intervention statistics

Everything below is computed from `Unprocessed Data/` only (per-prompt `stats/combined/prompt_stats.csv`, `runs.csv`, `verifier_detection.csv`, `error_kinds.csv`). The 3 main runs (Qwen3.5-9B at Q4_K_M, Q6_K, Q8_0; AMD RX 9070 XT + Ryzen 7 5700X3D) each have 990 scored tasks, pilot excluded, unless stated. Reproduce with `python3 -I build_tempstats.py`. Charts are in `charts/`, every number in `tables/`.

## How the Rand values are worked out

- Tariff basis: eThekwini Municipality electricity tariff for Durban Central (where the test took place), September 2026: **R3.5747/kWh excl. VAT**, plus 15% VAT = **R4.1109/kWh incl. VAT** (3.5747 × 1.15 = 4.110905). The figure was supplied by you; the municipal bill itself was not in the archive, so it is cited as the bill/tariff for the test site rather than checked against a scan of it.
- Energy is what the benchmark measured (GPU + CPU package via LibreHardwareMonitor, idle draw included). It excludes motherboard, RAM, storage and PSU losses, so a wall-socket bill would be higher. "Above idle" figures are in `tables/01` for the marginal view.
- Times are wall-clock seconds per prompt as recorded by the benchmark.

## Headline results

| | Q4_K_M | Q6_K | Q8_0 |
|---|---|---|---|
| Hallucinated code reaching user: baseline → CA | 51.8% → 1.6% | 50.8% → 2.3% | 55.2% → 2.0% |
| Change (95% CI, pp) | −50.2 (−53.3, −47.0) | −48.5 (−51.7, −45.4) | −53.1 (−56.3, −50.0) |
| Correct code reaching user | 24.9% → 50.9% | 36.9% → 50.4% | 34.4% → 51.5% |
| Time per prompt | 5.8 s → 36.9 s (6.4×) | 6.2 s → 38.3 s (6.2×) | 7.4 s → 48.4 s (6.6×) |
| Electricity per 1,000 prompts (incl. VAT) | R1.95 → R10.51 (5.4×) | R2.20 → R13.78 (6.3×) | R2.42 → R14.87 (6.1×) |
| Electricity per correct answer delivered | 0.78c → 2.06c | 0.60c → 2.73c | 0.70c → 2.89c |
| Time per correct answer delivered | 23 s → 73 s | 17 s → 76 s | 21 s → 94 s |
| Extra electricity per hallucination prevented | 1.70c | 2.39c | 2.34c |
| Extra time per hallucination prevented | 1.03 min | 1.10 min | 1.29 min |
| Extra time / electricity per extra correct answer | 2.0 min / 3.3c | 4.0 min / 8.6c | 4.0 min / 7.3c |

Hallucination change is paired (exact McNemar p between 1e-130 and 1e-153; my values match the evaluator's report). Correct-code gains are significant too (p between 1e-19 and 1e-51).

## The cost, in time and Rand

- **Per prompt:** the verifier costs 6.2–6.6× the time and 5.4–6.3× the electricity. In every one of the 18 paired Wilcoxon tests (time, energy, tokens, generated tokens, GPU and CPU energy × 3 quantizations) the intervention costs more, p < 1e-160, rank-biserial r ≥ 0.995, and 99.5–100% of individual prompts cost more.
- **In cents:** about 0.20–0.24c per prompt without the verifier and 1.05–1.49c with it. Electricity is therefore small money: R10.51–R14.87 per 1,000 verified prompts.
- **Whole benchmark (1,000 prompts per mode, pilot included, `tables/02`):** baseline 1.6–2.0 h and R1.95–R2.42 per quantization; with the verifier 10.2–13.5 h and R10.49–R14.87. Across all three runs: 5.4 h and R6.56 without, 34.4 h and R39.15 with, so the verifier added 29.0 h and R32.59 (R28.34 excl. VAT).
- **At scale (`tables/18`):** 10,000 prompts is 0.7–0.9 days and R20–R24 for baseline versus 4.3–5.6 days and R105–R149 verified. 100,000 prompts is 43–56 days versus 7–9 days.
- **Throughput:** 490–620 prompts/hour baseline vs 74–97 verified; 413–512 prompts per R1 vs 67–95. Correct answers per hour: 155–214 vs 38–50; per R1: 128–168 vs 35–48.
- **Why it costs so much:** the loop re-sends the growing conversation, so input goes from ~156 to 20–22k tokens per prompt (about 130×). Input length alone tracks time (Spearman ρ = 0.92). Tokens rise 40–46× but energy only 5–6×, because input tokens are cheap to process (energy per 1,000 tokens falls from 3.2–4.2 kJ to 0.43–0.56 kJ). Generated tokens rise 3.5–4.3×. The verifier tool is 6–25% of time (2.3 s at Q6_K, but 9.1 s and 9.6 s at Q4_K_M and Q8_0, an unexplained difference worth checking).

## What the money buys, and where it is wasted

- Roughly 4 in 10 verified prompts end with nothing shown (38–39%). The verifier spends 5.0–6.2 h per run (R5.0–R6.7) on withheld hallucinations (a good catch, but no deliverable), and 0.30–0.57 h (R0.30–R0.63) on correct answers it then withheld (false alarms).
- **REST Countries (api_key auth) delivered nothing:** the verifier withheld 99.8% of its tasks, so 7.1 h and R7.93 across the three runs produced no code. The baseline hallucinated 99.5% of these tasks, so this API is a model/prompt problem rather than something the verifier can fix.
- **Correction rounds:** prompts needing 0, 1, 2 or 3 corrections cost 34, 45, 57 and 61 s. Success collapses as rounds grow: correct code reaches the user for 64%, 51%, 15% and 1% of those prompts, and 95% of 3-round prompts are withheld. A correct answer from a 3-round prompt costs about 5,000 s on average (small n, and harder tasks need more rounds, so this is not causal), so a hard cap on correction rounds is where savings would come from.
- **Verifier as detector (class A):** recall 94–96%, precision 86–92%, specificity 92–95%, F1 0.90–0.94. Misses: 16/23/20 hallucinations delivered. The EWCS confidence score has AUC 0.93–0.94, with correct code scoring 0.825 versus 0.279 for hallucinations (median).
- **Residual hallucinations are nearly all Petstore:** 57 of the 59 hallucinations still reaching users across the runs (12.7% of Petstore tasks). OAuth2 tasks are the other weak spot (12–23% residual).

## Effect of quantization

- Baseline cost rises with precision: 5.8 s/R1.95 per 1,000 at Q4 vs 7.4 s/R2.42 at Q8 (Kruskal–Wallis on time and energy p < 1e-49; all Holm-adjusted pairwise tests significant except tokens Q6 vs Q8).
- With the verifier, accuracy is almost identical across quantizations (correct 50.4–51.5%; hallucination 1.6–2.3%), but Q4_K_M is cheapest and fastest: 36.9 s and R10.51 per prompt/1,000 vs 48.4 s and R14.87 at Q8_0, and 48 correct answers per R1 vs 35. Q4_K_M's average draw during verified runs was only 249 W vs 269–315 W.
- Q4_K_M gains most (+26 pp correct) because its baseline is weakest (15% of baseline answers crash). Q4_K_M therefore gives the best value here.
- Comparisons between quantizations are descriptive: one run each, on different days (30 Sep–3 Oct), so differences cannot be separated from run-to-run variation. Per-prompt cost follows the API mix and is highly repeatable in shape across runs (chart 17).

## Caveats

1. The intervention prompt names the correct API hosts (by design, per the benchmark README). "Wrong host, version or base path" accounts for 1,303 of the baseline's 1,562 hallucinated tasks across the runs, so part of the hallucination drop comes from that context, not from verification. Hallucinations other than wrong host still fall from 58/87/93 (Q4/Q6/Q8) to 15/23/20 (about 75%).
2. Costs are measured on one machine at the benchmark settings (thinking off, 4 turns, context 30,208). Scaled figures are linear extrapolations.
3. Electricity at this tariff is a small share of a realistic cost. Latency (6×) and GPU occupancy are the real price; a GPU-hour or labour rate would let both be added in Rand if you want one.
4. The measured energy covers GPU and CPU package only.

## Chart index

00 scorecard · 01 cost per prompt · 02 whole-run bill · 03 price of a good outcome · 04 cost vs quality · 05 cost distributions · 06 where time goes · 07 spend by outcome · 08 correction rounds · 09 by API · 10 subgroup heatmaps · 11 verifier as detector · 12 EWCS / ROC · 13 what reaches the user · 14 unit economics · 15 effect sizes · 16 energy anatomy · 17 run profile · 18 hallucination kinds · 19 scaling
