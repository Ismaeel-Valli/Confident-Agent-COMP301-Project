# Evaluation report

Evaluator 2026-09-27.1, 2026-09-30T15:07:12+00:00. Rules: `Benchmark/EVALUATION_PLAN.md`.

- Answer key: task file SHA-256 `7a09f2bb566dbabb…` (matches the plan).
- Self-check: 1000/1000 reference solutions scored correct; behaviour requirements met by 1000.
- Manual reviews applied from: none yet (undetermined candidates are excluded from the primary result).
- Intervals: 10000 bootstrap resamples (seed 301), over tasks and over operation families.

## Qwen3.5-9B-Q4_K_M-full

Quantization Q4_K_M, benchmark 2026-09-26.2, GPU n/a: preliminary run (benchmark 2026-09-26.2 is older than 2026-09-27.2: earlier measurements and verifier).

### Unacceptable hallucinations reaching the user (primary, plan §3)

Rate = share of tasks whose code reaching the user is class A (API hallucination). Baseline: the code block; intervention: the delivered code, or code shown in the reply. Pilot tasks excluded; difference = baseline − intervention; discordant = baseline-only / intervention-only.

| Comparison | Tasks | Baseline | Intervention | Difference | 95% CI (tasks) | 95% CI (families) | Discordant | McNemar p |
|---|---:|---:|---:|---:|---|---|---|---:|
| **Primary** (undetermined excluded) | 976 | 52.3% | 3.1% | +49.2 pp | [+46.0, +52.5] pp | [+33.0, +62.6] pp | 494 / 14 | < 0.0001 |
| Undetermined counted as hallucination | 990 | 52.5% | 3.4% | +49.1 pp | [+45.8, +52.4] pp | [+33.0, +62.4] pp | 504 / 18 | < 0.0001 |
| Undetermined counted as correct | 990 | 51.5% | 3.0% | +48.5 pp | [+45.2, +51.8] pp | [+32.3, +61.9] pp | 494 / 14 | < 0.0001 |
| Including pilot tasks | 986 | 52.1% | 3.0% | +49.1 pp | [+45.8, +52.4] pp | [+33.0, +62.5] pp | 498 / 14 | < 0.0001 |
| A or B (secondary) | 976 | 60.5% | 12.9% | +47.5 pp | [+44.0, +51.1] pp | [+32.9, +60.2] pp | 508 / 44 | < 0.0001 |
| A, B or runtime failure | 976 | 76.8% | 13.3% | +63.5 pp | [+60.2, +66.8] pp | [+51.8, +73.4] pp | 642 / 22 | < 0.0001 |

Not in the Holm family (preliminary run): the p-value above is uncorrected. Undetermined pairs excluded from the primary row: 14. Operation families: 141.

### Classes (pilot excluded)

| Class | Baseline code | Intervention: shown to user | Intervention: final candidate |
|---|---:|---:|---:|
| A | 510 | 30 | 321 |
| B | 82 | 96 | 99 |
| correct | 228 | 489 | 513 |
| nothing_shown | 0 | 366 | 0 |
| runtime_failure | 160 | 5 | 8 |
| undetermined | 10 | 4 | 49 |

### Kinds of API hallucination reaching the user (tasks; a task can have several)

| Kind | Baseline | Intervention |
|---|---:|---:|
| wrong host, version or base path | 456 | 1 |
| invented endpoint or method | 31 | 0 |
| invented parameter or body field | 14 | 4 |
| invalid value or structure | 10 | 18 |
| missing required part or credential | 8 | 5 |
| non-existent requests API | 2 | 0 |
| undocumented response field | 0 | 2 |

Tasks with a hallucination other than a wrong host, version or base path: baseline 56, intervention 29. The intervention prompt names the current hosts (by design, Benchmark README), so this row separates that context from what verification catches.


### Intervention decisions against the final candidate's class

| Final candidate | Delivered | Withheld |
|---|---:|---:|
| A | 30 | 291 |
| B | 96 | 3 |
| correct | 489 | 24 |
| runtime_failure | 5 | 3 |
| undetermined | 4 | 45 |

- Incorrect acceptance (class A shown to the user): 30
- Incorrect rejection (correct final candidate withheld): 24
- Code shown in a reply without the tool's approval: 0

### Confidence metric (EWCS of the final candidate)

AUC, correct vs class A: 0.905 (correct n=513, A n=320).

| EWCS band | Correct | Of decided (correct, A, B) |
|---|---:|---:|
| 0.60-0.85 | 468 | 648 |
| <0.60 | 3 | 217 |
| >=0.85 | 42 | 67 |

### Corrections

Attempted 395 (allowed by the prompt: 344).

| First candidate → final | Tasks |
|---|---:|
| A->A | 158 |
| A->correct | 126 |
| A->B | 35 |
| undetermined->A | 28 |
| runtime_failure->correct | 14 |
| undetermined->correct | 6 |
| undetermined->undetermined | 5 |
| runtime_failure->B | 5 |
| undetermined->B | 3 |
| runtime_failure->runtime_failure | 3 |
| runtime_failure->undetermined | 3 |
| correct->correct | 2 |
| A->undetermined | 2 |
| B->B | 2 |
| runtime_failure->A | 2 |
| B->correct | 1 |

### Agent protocol notes

| Note | Tasks |
|---|---:|
| reached the turn limit; the benchmark asked for the final reply | 330 |
| verified the same code more than once | 305 |
| more than one correction | 139 |
| reply differs from the final report | 97 |
| corrected without a verified_incorrect layer | 51 |

### Task behaviour (secondary)

| Requirement | Baseline | Intervention (shown) |
|---|---:|---:|
| returns expected value | 691/830 | 492/619 |
| empty response ok | 109/830 | 152/619 |
| error raises | 829/830 | 619/619 |

### By API

| API | Tasks | Baseline A | Intervention A shown | Delivered | Undetermined (baseline / shown) |
|---|---:|---:|---:|---:|---|
| DummyJSON | 148 | 100 | 0 | 100 | 5 / 0 |
| GitHub | 248 | 15 | 6 | 228 | 0 / 0 |
| JSONPlaceholder | 148 | 17 | 0 | 143 | 5 / 4 |
| Open-Meteo | 148 | 110 | 1 | 76 | 0 / 0 |
| Petstore | 149 | 119 | 23 | 77 | 0 / 0 |
| REST Countries | 149 | 149 | 0 | 0 | 0 / 0 |

### Cost per task (plan §3, project description §4.8)

| Measure | Baseline mean | Intervention mean | Ratio |
|---|---:|---:|---:|
| (not recorded in this run) | | | |

Manual review: 60 undetermined candidates in `Qwen3.5-9B-Q4_K_M-full/review_queue.csv`; audit sample of 100 in `Qwen3.5-9B-Q4_K_M-full/audit_sample.csv` (plan §4–5).

## Qwen3.5-9B-Q4_K_M-full-run2

Quantization Q4_K_M, benchmark 2026-09-27.2, GPU AMD Radeon RX 9070 XT: main run (benchmark 2026-09-27.2).

### Unacceptable hallucinations reaching the user (primary, plan §3)

Rate = share of tasks whose code reaching the user is class A (API hallucination). Baseline: the code block; intervention: the delivered code, or code shown in the reply. Pilot tasks excluded; difference = baseline − intervention; discordant = baseline-only / intervention-only.

| Comparison | Tasks | Baseline | Intervention | Difference | 95% CI (tasks) | 95% CI (families) | Discordant | McNemar p |
|---|---:|---:|---:|---:|---|---|---|---:|
| **Primary** (undetermined excluded) | 982 | 50.8% | 1.6% | +49.2 pp | [+46.0, +52.3] pp | [+33.1, +62.3] pp | 490 / 7 | < 0.0001 |
| Undetermined counted as hallucination | 990 | 51.2% | 1.6% | +49.6 pp | [+46.4, +52.7] pp | [+33.9, +62.7] pp | 498 / 7 | < 0.0001 |
| Undetermined counted as correct | 990 | 50.4% | 1.6% | +48.8 pp | [+45.6, +51.9] pp | [+32.8, +62.1] pp | 490 / 7 | < 0.0001 |
| Including pilot tasks | 992 | 50.9% | 1.6% | +49.3 pp | [+46.1, +52.5] pp | [+33.6, +62.4] pp | 496 / 7 | < 0.0001 |
| A or B (secondary) | 982 | 58.8% | 9.9% | +48.9 pp | [+45.3, +52.4] pp | [+34.3, +61.3] pp | 519 / 39 | < 0.0001 |
| A, B or runtime failure | 982 | 75.8% | 10.6% | +65.2 pp | [+61.9, +68.2] pp | [+53.0, +74.8] pp | 656 / 16 | < 0.0001 |

Holm-adjusted McNemar p across the main runs: < 0.0001. Undetermined pairs excluded from the primary row: 8. Operation families: 141.

### Classes (pilot excluded)

| Class | Baseline code | Intervention: shown to user | Intervention: final candidate |
|---|---:|---:|---:|
| A | 499 | 16 | 322 |
| B | 78 | 81 | 86 |
| correct | 235 | 500 | 527 |
| no_code | 3 | 0 | 0 |
| nothing_shown | 0 | 386 | 0 |
| runtime_failure | 167 | 7 | 8 |
| undetermined | 8 | 0 | 47 |

### Kinds of API hallucination reaching the user (tasks; a task can have several)

| Kind | Baseline | Intervention |
|---|---:|---:|
| wrong host, version or base path | 445 | 1 |
| invented endpoint or method | 38 | 0 |
| invalid value or structure | 8 | 10 |
| missing required part or credential | 6 | 4 |
| invented parameter or body field | 6 | 0 |
| non-existent requests API | 2 | 0 |
| other | 1 | 0 |
| undocumented response field | 1 | 1 |

Tasks with a hallucination other than a wrong host, version or base path: baseline 56, intervention 15. The intervention prompt names the current hosts (by design, Benchmark README), so this row separates that context from what verification catches.


### Intervention decisions against the final candidate's class

| Final candidate | Delivered | Withheld |
|---|---:|---:|
| A | 16 | 306 |
| B | 81 | 5 |
| correct | 500 | 27 |
| runtime_failure | 7 | 1 |
| undetermined | 0 | 47 |

- Incorrect acceptance (class A shown to the user): 16
- Incorrect rejection (correct final candidate withheld): 27
- Code shown in a reply without the tool's approval: 0

### Confidence metric (EWCS of the final candidate)

AUC, correct vs class A: 0.941 (correct n=527, A n=322).

| EWCS band | Correct | Of decided (correct, A, B) |
|---|---:|---:|
| 0.60-0.85 | 479 | 657 |
| <0.60 | 3 | 220 |
| >=0.85 | 45 | 58 |

### Corrections

Attempted 386 (allowed by the prompt: 342).

| First candidate → final | Tasks |
|---|---:|
| A->A | 147 |
| A->correct | 125 |
| runtime_failure->correct | 30 |
| undetermined->A | 26 |
| A->B | 24 |
| undetermined->correct | 7 |
| runtime_failure->B | 5 |
| undetermined->undetermined | 4 |
| correct->correct | 4 |
| runtime_failure->runtime_failure | 4 |
| A->undetermined | 2 |
| undetermined->B | 2 |
| B->B | 2 |
| runtime_failure->A | 2 |
| runtime_failure->undetermined | 1 |
| B->correct | 1 |

### Agent protocol notes

| Note | Tasks |
|---|---:|
| reached the turn limit; the benchmark asked for the final reply | 344 |
| verified the same code more than once | 338 |
| more than one correction | 126 |
| reply differs from the final report | 96 |
| corrected without a verified_incorrect layer | 44 |

### Task behaviour (secondary)

| Requirement | Baseline | Intervention (shown) |
|---|---:|---:|
| returns expected value | 674/820 | 479/597 |
| empty response ok | 111/820 | 146/597 |
| error raises | 817/820 | 597/597 |

### By API

| API | Tasks | Baseline A | Intervention A shown | Delivered | Undetermined (baseline / shown) |
|---|---:|---:|---:|---:|---|
| DummyJSON | 148 | 100 | 0 | 98 | 0 / 0 |
| GitHub | 248 | 14 | 1 | 225 | 0 / 0 |
| JSONPlaceholder | 148 | 21 | 0 | 139 | 8 / 0 |
| Open-Meteo | 148 | 106 | 1 | 70 | 0 / 0 |
| Petstore | 149 | 110 | 14 | 72 | 0 / 0 |
| REST Countries | 149 | 148 | 0 | 0 | 0 / 0 |

### Cost per task (plan §3, project description §4.8)

| Measure | Baseline mean | Intervention mean | Ratio |
|---|---:|---:|---:|
| completion_tokens | 381.9 | 1301.2 | 3.4x |
| cpu_energy_j | 300.7 | 1689.5 | 5.6x |
| duration_seconds | 5.8 | 36.5 | 6.2x |
| gpu_energy_j | 1534.4 | 8244.7 | 5.4x |
| measured_energy_j | 1835.1 | 9934.2 | 5.4x |
| model_seconds | 5.8 | 28.2 | 4.8x |
| prompt_tokens | 156.5 | 20184.2 | 129.0x |
| tool_seconds | n/a | 8.3 | n/a |

Manual review: 57 undetermined candidates in `Qwen3.5-9B-Q4_K_M-full-run2/review_queue.csv`; audit sample of 103 in `Qwen3.5-9B-Q4_K_M-full-run2/audit_sample.csv` (plan §4–5).

## Qwen3.5-9B-Q6_0-full

Quantization Q6_K, benchmark 2026-09-27.2, GPU AMD Radeon RX 9070 XT: main run (benchmark 2026-09-27.2); **the label does not match the quantization LM Studio reported (Q6_K)**.

### Unacceptable hallucinations reaching the user (primary, plan §3)

Rate = share of tasks whose code reaching the user is class A (API hallucination). Baseline: the code block; intervention: the delivered code, or code shown in the reply. Pilot tasks excluded; difference = baseline − intervention; discordant = baseline-only / intervention-only.

| Comparison | Tasks | Baseline | Intervention | Difference | 95% CI (tasks) | 95% CI (families) | Discordant | McNemar p |
|---|---:|---:|---:|---:|---|---|---|---:|
| **Primary** (undetermined excluded) | 970 | 51.1% | 3.0% | +48.1 pp | [+44.9, +51.3] pp | [+31.4, +62.0] pp | 475 / 8 | < 0.0001 |
| Undetermined counted as hallucination | 990 | 52.1% | 2.9% | +49.2 pp | [+46.0, +52.4] pp | [+33.4, +62.8] pp | 495 / 8 | < 0.0001 |
| Undetermined counted as correct | 990 | 50.1% | 2.9% | +47.2 pp | [+43.9, +50.4] pp | [+30.7, +61.1] pp | 475 / 8 | < 0.0001 |
| Including pilot tasks | 979 | 51.1% | 3.0% | +48.1 pp | [+44.9, +51.3] pp | [+31.7, +61.7] pp | 479 / 8 | < 0.0001 |
| A or B (secondary) | 970 | 55.9% | 10.4% | +45.5 pp | [+42.0, +48.9] pp | [+28.6, +59.6] pp | 468 / 27 | < 0.0001 |
| A, B or runtime failure | 970 | 62.9% | 11.1% | +51.8 pp | [+48.2, +55.2] pp | [+35.7, +64.7] pp | 526 / 24 | < 0.0001 |

Holm-adjusted McNemar p across the main runs: < 0.0001. Undetermined pairs excluded from the primary row: 20. Operation families: 141.

### Classes (pilot excluded)

| Class | Baseline code | Intervention: shown to user | Intervention: final candidate |
|---|---:|---:|---:|
| A | 496 | 29 | 222 |
| B | 46 | 76 | 81 |
| correct | 360 | 483 | 502 |
| nothing_shown | 0 | 395 | 0 |
| runtime_failure | 68 | 7 | 12 |
| undetermined | 20 | 0 | 173 |

### Kinds of API hallucination reaching the user (tasks; a task can have several)

| Kind | Baseline | Intervention |
|---|---:|---:|
| wrong host, version or base path | 418 | 0 |
| invented endpoint or method | 60 | 0 |
| invalid value or structure | 9 | 23 |
| invented parameter or body field | 6 | 1 |
| missing required part or credential | 5 | 4 |
| undocumented response field | 2 | 1 |
| non-existent requests API | 1 | 0 |

Tasks with a hallucination other than a wrong host, version or base path: baseline 78, intervention 29. The intervention prompt names the current hosts (by design, Benchmark README), so this row separates that context from what verification catches.


### Intervention decisions against the final candidate's class

| Final candidate | Delivered | Withheld |
|---|---:|---:|
| A | 29 | 193 |
| B | 76 | 5 |
| correct | 483 | 19 |
| runtime_failure | 7 | 5 |
| undetermined | 0 | 173 |

- Incorrect acceptance (class A shown to the user): 29
- Incorrect rejection (correct final candidate withheld): 19
- Code shown in a reply without the tool's approval: 0

### Confidence metric (EWCS of the final candidate)

AUC, correct vs class A: 0.866 (correct n=502, A n=222).

| EWCS band | Correct | Of decided (correct, A, B) |
|---|---:|---:|
| 0.60-0.85 | 466 | 644 |
| <0.60 | 0 | 98 |
| >=0.85 | 36 | 63 |

### Corrections

Attempted 415 (allowed by the prompt: 363).

| First candidate → final | Tasks |
|---|---:|
| A->A | 164 |
| A->correct | 136 |
| undetermined->undetermined | 44 |
| A->B | 23 |
| undetermined->A | 11 |
| correct->correct | 10 |
| undetermined->B | 9 |
| A->undetermined | 7 |
| runtime_failure->runtime_failure | 4 |
| undetermined->correct | 3 |
| B->B | 2 |
| runtime_failure->A | 1 |
| runtime_failure->undetermined | 1 |

### Agent protocol notes

| Note | Tasks |
|---|---:|
| reached the turn limit; the benchmark asked for the final reply | 384 |
| verified the same code more than once | 301 |
| more than one correction | 186 |
| reply differs from the final report | 68 |
| corrected without a verified_incorrect layer | 52 |
| replied without correcting after a verified_incorrect layer | 1 |

### Task behaviour (secondary)

| Requirement | Baseline | Intervention (shown) |
|---|---:|---:|
| returns expected value | 781/922 | 488/588 |
| empty response ok | 176/922 | 161/588 |
| error raises | 922/922 | 586/588 |

### By API

| API | Tasks | Baseline A | Intervention A shown | Delivered | Undetermined (baseline / shown) |
|---|---:|---:|---:|---:|---|
| DummyJSON | 148 | 48 | 0 | 111 | 9 / 0 |
| GitHub | 248 | 35 | 1 | 224 | 0 / 0 |
| JSONPlaceholder | 148 | 28 | 1 | 135 | 11 / 0 |
| Open-Meteo | 148 | 108 | 0 | 52 | 0 / 0 |
| Petstore | 149 | 128 | 27 | 73 | 0 / 0 |
| REST Countries | 149 | 149 | 0 | 0 | 0 / 0 |

### Cost per task (plan §3, project description §4.8)

| Measure | Baseline mean | Intervention mean | Ratio |
|---|---:|---:|---:|
| completion_tokens | 347.2 | 1464.9 | 4.2x |
| cpu_energy_j | 308.5 | 3738.5 | 12.1x |
| duration_seconds | 6.4 | 81.0 | 12.6x |
| gpu_energy_j | 1562.5 | 16270.6 | 10.4x |
| measured_energy_j | 1871.0 | 20009.1 | 10.7x |
| model_seconds | 6.4 | 71.9 | 11.2x |
| prompt_tokens | 156.5 | 21540.0 | 137.6x |
| tool_seconds | n/a | 9.0 | n/a |

Manual review: 195 undetermined candidates in `Qwen3.5-9B-Q6_0-full/review_queue.csv`; audit sample of 100 in `Qwen3.5-9B-Q6_0-full/audit_sample.csv` (plan §4–5).

## Qwen3.5-9B-Q8_0-full

Quantization Q8_0, benchmark 2026-09-27.2, GPU AMD Radeon RX 9070 XT: main run (benchmark 2026-09-27.2).

### Unacceptable hallucinations reaching the user (primary, plan §3)

Rate = share of tasks whose code reaching the user is class A (API hallucination). Baseline: the code block; intervention: the delivered code, or code shown in the reply. Pilot tasks excluded; difference = baseline − intervention; discordant = baseline-only / intervention-only.

| Comparison | Tasks | Baseline | Intervention | Difference | 95% CI (tasks) | 95% CI (families) | Discordant | McNemar p |
|---|---:|---:|---:|---:|---|---|---|---:|
| **Primary** (undetermined excluded) | 973 | 53.1% | 2.1% | +51.1 pp | [+47.9, +54.3] pp | [+35.0, +64.4] pp | 499 / 2 | < 0.0001 |
| Undetermined counted as hallucination | 990 | 53.8% | 2.1% | +51.7 pp | [+48.6, +54.8] pp | [+36.2, +64.6] pp | 515 / 3 | < 0.0001 |
| Undetermined counted as correct | 990 | 52.2% | 2.0% | +50.2 pp | [+47.1, +53.3] pp | [+34.4, +63.5] pp | 499 / 2 | < 0.0001 |
| Including pilot tasks | 983 | 53.1% | 2.0% | +51.1 pp | [+47.8, +54.3] pp | [+34.9, +64.3] pp | 504 / 2 | < 0.0001 |
| A or B (secondary) | 973 | 59.0% | 8.7% | +50.3 pp | [+46.9, +53.6] pp | [+34.3, +63.5] pp | 506 / 17 | < 0.0001 |
| A, B or runtime failure | 973 | 63.6% | 9.1% | +54.5 pp | [+51.1, +57.9] pp | [+38.9, +67.0] pp | 549 / 19 | < 0.0001 |

Holm-adjusted McNemar p across the main runs: < 0.0001. Undetermined pairs excluded from the primary row: 17. Operation families: 139.

### Classes (pilot excluded)

| Class | Baseline code | Intervention: shown to user | Intervention: final candidate |
|---|---:|---:|---:|
| A | 517 | 20 | 222 |
| B | 57 | 68 | 80 |
| correct | 355 | 497 | 517 |
| no_code | 0 | 0 | 1 |
| nothing_shown | 0 | 399 | 0 |
| runtime_failure | 45 | 5 | 7 |
| undetermined | 16 | 1 | 163 |

### Kinds of API hallucination reaching the user (tasks; a task can have several)

| Kind | Baseline | Intervention |
|---|---:|---:|
| wrong host, version or base path | 426 | 0 |
| invented endpoint or method | 72 | 0 |
| missing required part or credential | 8 | 5 |
| invalid value or structure | 7 | 15 |
| invented parameter or body field | 5 | 0 |
| undocumented response field | 3 | 0 |

Tasks with a hallucination other than a wrong host, version or base path: baseline 91, intervention 20. The intervention prompt names the current hosts (by design, Benchmark README), so this row separates that context from what verification catches.


### Intervention decisions against the final candidate's class

| Final candidate | Delivered | Withheld |
|---|---:|---:|
| A | 20 | 202 |
| B | 68 | 12 |
| correct | 496 | 21 |
| no_code | 0 | 1 |
| runtime_failure | 5 | 2 |
| undetermined | 1 | 162 |

- Incorrect acceptance (class A shown to the user): 20
- Incorrect rejection (correct final candidate withheld): 21
- Code shown in a reply without the tool's approval: 1

### Confidence metric (EWCS of the final candidate)

AUC, correct vs class A: 0.898 (correct n=517, A n=222).

| EWCS band | Correct | Of decided (correct, A, B) |
|---|---:|---:|
| 0.60-0.85 | 476 | 644 |
| <0.60 | 2 | 117 |
| >=0.85 | 39 | 58 |

### Corrections

Attempted 430 (allowed by the prompt: 384).

| First candidate → final | Tasks |
|---|---:|
| A->A | 166 |
| A->correct | 142 |
| undetermined->undetermined | 42 |
| A->B | 32 |
| undetermined->A | 25 |
| undetermined->B | 10 |
| undetermined->correct | 5 |
| A->undetermined | 4 |
| correct->correct | 2 |
| B->B | 1 |
| runtime_failure->A | 1 |

### Agent protocol notes

| Note | Tasks |
|---|---:|
| reached the turn limit; the benchmark asked for the final reply | 397 |
| verified the same code more than once | 317 |
| more than one correction | 188 |
| reply differs from the final report | 60 |
| corrected without a verified_incorrect layer | 46 |
| never called verify_candidate | 1 |
| reply shows code the tool did not approve | 1 |

### Task behaviour (secondary)

| Requirement | Baseline | Intervention (shown) |
|---|---:|---:|
| returns expected value | 794/945 | 499/586 |
| empty response ok | 187/945 | 153/586 |
| error raises | 943/945 | 585/586 |

### By API

| API | Tasks | Baseline A | Intervention A shown | Delivered | Undetermined (baseline / shown) |
|---|---:|---:|---:|---:|---|
| DummyJSON | 148 | 70 | 0 | 111 | 7 / 0 |
| GitHub | 248 | 40 | 0 | 226 | 1 / 0 |
| JSONPlaceholder | 148 | 25 | 0 | 135 | 8 / 1 |
| Open-Meteo | 148 | 106 | 0 | 57 | 0 / 0 |
| Petstore | 149 | 127 | 20 | 60 | 0 / 0 |
| REST Countries | 149 | 149 | 0 | 1 | 0 / 0 |

### Cost per task (plan §3, project description §4.8)

| Measure | Baseline mean | Intervention mean | Ratio |
|---|---:|---:|---:|
| completion_tokens | 339.6 | 1508.1 | 4.4x |
| cpu_energy_j | 331.4 | 2435.6 | 7.3x |
| duration_seconds | 7.1 | 52.0 | 7.3x |
| gpu_energy_j | 1736.4 | 11767.2 | 6.8x |
| measured_energy_j | 2067.8 | 14202.7 | 6.9x |
| model_seconds | 7.1 | 49.5 | 7.0x |
| prompt_tokens | 156.5 | 21895.4 | 139.9x |
| tool_seconds | n/a | 2.5 | n/a |

Manual review: 180 undetermined candidates in `Qwen3.5-9B-Q8_0-full/review_queue.csv`; audit sample of 101 in `Qwen3.5-9B-Q8_0-full/audit_sample.csv` (plan §4–5).

