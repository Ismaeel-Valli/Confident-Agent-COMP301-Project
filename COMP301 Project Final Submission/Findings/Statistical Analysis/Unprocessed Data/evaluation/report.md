# Evaluation report

Evaluator 2026-09-27.1, 2026-10-09T13:17:15+00:00. Rules: `Benchmark/EVALUATION_PLAN.md`.

- Answer key: task file SHA-256 `7a09f2bb566dbabb…` (matches the plan).
- Self-check: 1000/1000 reference solutions scored correct; behaviour requirements met by 1000.
- Manual reviews applied from: reviews\reviews.csv.
- Intervals: 10000 bootstrap resamples (seed 301), over tasks and over operation families.

## QQwen3.5-9B-Q6_K-full-Latest

Quantization Q6_K, benchmark 2026-09-27.2, GPU AMD Radeon RX 9070 XT: main run (benchmark 2026-09-27.2).

### Unacceptable hallucinations reaching the user (primary, plan §3)

Rate = share of tasks whose code reaching the user is class A (API hallucination). Baseline: the code block; intervention: the delivered code, or code shown in the reply. Pilot tasks excluded; difference = baseline − intervention; discordant = baseline-only / intervention-only.

| Comparison | Tasks | Baseline | Intervention | Difference | 95% CI (tasks) | 95% CI (families) | Discordant | McNemar p |
|---|---:|---:|---:|---:|---|---|---|---:|
| **Primary** (undetermined excluded) | 990 | 50.8% | 2.3% | +48.5 pp | [+45.3, +51.7] pp | [+32.7, +62.1] pp | 490 / 10 | < 0.0001 |
| Undetermined counted as hallucination | 990 | 50.8% | 2.3% | +48.5 pp | [+45.3, +51.7] pp | [+32.7, +62.1] pp | 490 / 10 | < 0.0001 |
| Undetermined counted as correct | 990 | 50.8% | 2.3% | +48.5 pp | [+45.3, +51.7] pp | [+32.7, +62.1] pp | 490 / 10 | < 0.0001 |
| Including pilot tasks | 1000 | 50.7% | 2.3% | +48.4 pp | [+45.2, +51.6] pp | [+32.8, +61.7] pp | 494 / 10 | < 0.0001 |
| A or B (secondary) | 990 | 56.5% | 9.4% | +47.1 pp | [+43.5, +50.5] pp | [+31.5, +60.5] pp | 493 / 27 | < 0.0001 |
| A, B or runtime failure | 990 | 62.8% | 10.1% | +52.7 pp | [+49.4, +56.1] pp | [+37.9, +65.1] pp | 541 / 19 | < 0.0001 |

Holm-adjusted McNemar p across the main runs: < 0.0001. Undetermined pairs excluded from the primary row: 0. Operation families: 141.

### Classes (pilot excluded)

| Class | Baseline code | Intervention: shown to user | Intervention: final candidate |
|---|---:|---:|---:|
| A | 503 | 23 | 370 |
| B | 56 | 70 | 90 |
| correct | 365 | 499 | 519 |
| no_code | 3 | 0 | 0 |
| nothing_shown | 0 | 391 | 0 |
| runtime_failure | 63 | 7 | 11 |

### Kinds of API hallucination reaching the user (tasks; a task can have several)

| Kind | Baseline | Intervention |
|---|---:|---:|
| wrong host, version or base path | 408 | 0 |
| invented endpoint or method | 70 | 0 |
| invalid value or structure | 11 | 21 |
| invented parameter or body field | 5 | 0 |
| missing required part or credential | 3 | 2 |
| undocumented response field | 3 | 0 |

Tasks with a hallucination other than a wrong host, version or base path: baseline 87, intervention 23. The intervention prompt names the current hosts (by design, Benchmark README), so this row separates that context from what verification catches.


### Intervention decisions against the final candidate's class

| Final candidate | Delivered | Withheld |
|---|---:|---:|
| A | 23 | 347 |
| B | 70 | 20 |
| correct | 499 | 20 |
| runtime_failure | 7 | 4 |

- Incorrect acceptance (class A shown to the user): 23
- Incorrect rejection (correct final candidate withheld): 20
- Code shown in a reply without the tool's approval: 0

### Confidence metric (EWCS of the final candidate)

AUC, correct vs class A: 0.932 (correct n=519, A n=370).

| EWCS band | Correct | Of decided (correct, A, B) |
|---|---:|---:|
| 0.60-0.85 | 487 | 672 |
| <0.60 | 0 | 252 |
| >=0.85 | 32 | 55 |

### Corrections

Attempted 425 (allowed by the prompt: 377).

| First candidate → final | Tasks |
|---|---:|
| A->A | 165 |
| A->correct | 123 |
| undetermined->A | 63 |
| A->B | 33 |
| correct->correct | 14 |
| undetermined->B | 9 |
| runtime_failure->runtime_failure | 7 |
| undetermined->correct | 6 |
| runtime_failure->correct | 2 |
| B->B | 2 |
| runtime_failure->A | 1 |

### Agent protocol notes

| Note | Tasks |
|---|---:|
| reached the turn limit; the benchmark asked for the final reply | 371 |
| verified the same code more than once | 289 |
| more than one correction | 186 |
| reply differs from the final report | 68 |
| corrected without a verified_incorrect layer | 48 |
| replied without correcting after a verified_incorrect layer | 1 |

### Task behaviour (secondary)

| Requirement | Baseline | Intervention (shown) |
|---|---:|---:|
| returns expected value | 794/924 | 485/592 |
| empty response ok | 195/924 | 144/592 |
| error raises | 923/924 | 592/592 |

### By API

| API | Tasks | Baseline A | Intervention A shown | Delivered | Undetermined (baseline / shown) |
|---|---:|---:|---:|---:|---|
| DummyJSON | 148 | 59 | 0 | 114 | 0 / 0 |
| GitHub | 248 | 38 | 0 | 223 | 0 / 0 |
| JSONPlaceholder | 148 | 27 | 0 | 136 | 0 / 0 |
| Open-Meteo | 148 | 107 | 0 | 62 | 0 / 0 |
| Petstore | 149 | 124 | 23 | 64 | 0 / 0 |
| REST Countries | 149 | 148 | 0 | 0 | 0 / 0 |

### Cost per task (plan §3, project description §4.8)

| Measure | Baseline mean | Intervention mean | Ratio |
|---|---:|---:|---:|
| completion_tokens | 349.5 | 1464.8 | 4.2x |
| cpu_energy_j | 285.2 | 1725.7 | 6.1x |
| duration_seconds | 6.2 | 38.3 | 6.2x |
| gpu_energy_j | 1637.7 | 10340.6 | 6.3x |
| measured_energy_j | 1923.0 | 12066.4 | 6.3x |
| model_seconds | 6.2 | 36.0 | 5.8x |
| prompt_tokens | 156.5 | 21305.9 | 136.1x |
| tool_seconds | n/a | 2.3 | n/a |

Manual review: 0 undetermined candidates in `QQwen3.5-9B-Q6_K-full-Latest/review_queue.csv`; audit sample of 102 in `QQwen3.5-9B-Q6_K-full-Latest/audit_sample.csv` (plan §4–5).

## Qwen3.5-9B-Q4_KM-full-Latest

Quantization Q4_K_M, benchmark 2026-09-27.2, GPU AMD Radeon RX 9070 XT: main run (benchmark 2026-09-27.2).

### Unacceptable hallucinations reaching the user (primary, plan §3)

Rate = share of tasks whose code reaching the user is class A (API hallucination). Baseline: the code block; intervention: the delivered code, or code shown in the reply. Pilot tasks excluded; difference = baseline − intervention; discordant = baseline-only / intervention-only.

| Comparison | Tasks | Baseline | Intervention | Difference | 95% CI (tasks) | 95% CI (families) | Discordant | McNemar p |
|---|---:|---:|---:|---:|---|---|---|---:|
| **Primary** (undetermined excluded) | 990 | 51.8% | 1.6% | +50.2 pp | [+47.0, +53.3] pp | [+34.6, +63.2] pp | 505 / 8 | < 0.0001 |
| Undetermined counted as hallucination | 990 | 51.8% | 1.6% | +50.2 pp | [+47.0, +53.3] pp | [+34.6, +63.2] pp | 505 / 8 | < 0.0001 |
| Undetermined counted as correct | 990 | 51.8% | 1.6% | +50.2 pp | [+47.0, +53.3] pp | [+34.6, +63.2] pp | 505 / 8 | < 0.0001 |
| Including pilot tasks | 1000 | 51.8% | 1.6% | +50.2 pp | [+47.0, +53.4] pp | [+34.8, +63.1] pp | 510 / 8 | < 0.0001 |
| A or B (secondary) | 990 | 59.8% | 11.1% | +48.7 pp | [+45.1, +52.3] pp | [+34.8, +61.0] pp | 523 / 41 | < 0.0001 |
| A, B or runtime failure | 990 | 74.9% | 11.5% | +63.4 pp | [+60.1, +66.7] pp | [+51.3, +73.5] pp | 647 / 19 | < 0.0001 |

Holm-adjusted McNemar p across the main runs: < 0.0001. Undetermined pairs excluded from the primary row: 0. Operation families: 141.

### Classes (pilot excluded)

| Class | Baseline code | Intervention: shown to user | Intervention: final candidate |
|---|---:|---:|---:|
| A | 513 | 16 | 357 |
| B | 79 | 94 | 100 |
| correct | 247 | 504 | 525 |
| no_code | 1 | 0 | 0 |
| nothing_shown | 0 | 372 | 0 |
| runtime_failure | 150 | 4 | 8 |

### Kinds of API hallucination reaching the user (tasks; a task can have several)

| Kind | Baseline | Intervention |
|---|---:|---:|
| wrong host, version or base path | 449 | 1 |
| invented endpoint or method | 39 | 0 |
| invalid value or structure | 9 | 11 |
| invented parameter or body field | 8 | 0 |
| missing required part or credential | 5 | 3 |
| non-existent requests API | 1 | 0 |
| other | 1 | 0 |
| undocumented response field | 0 | 1 |

Tasks with a hallucination other than a wrong host, version or base path: baseline 58, intervention 15. The intervention prompt names the current hosts (by design, Benchmark README), so this row separates that context from what verification catches.


### Intervention decisions against the final candidate's class

| Final candidate | Delivered | Withheld |
|---|---:|---:|
| A | 16 | 341 |
| B | 94 | 6 |
| correct | 504 | 21 |
| runtime_failure | 4 | 4 |

- Incorrect acceptance (class A shown to the user): 16
- Incorrect rejection (correct final candidate withheld): 21
- Code shown in a reply without the tool's approval: 0

### Confidence metric (EWCS of the final candidate)

AUC, correct vs class A: 0.943 (correct n=525, A n=357).

| EWCS band | Correct | Of decided (correct, A, B) |
|---|---:|---:|
| 0.60-0.85 | 484 | 685 |
| <0.60 | 2 | 244 |
| >=0.85 | 39 | 53 |

### Corrections

Attempted 403 (allowed by the prompt: 349).

| First candidate → final | Tasks |
|---|---:|
| A->A | 164 |
| A->correct | 121 |
| A->B | 36 |
| undetermined->A | 27 |
| runtime_failure->correct | 23 |
| undetermined->B | 8 |
| runtime_failure->B | 6 |
| undetermined->correct | 4 |
| correct->correct | 4 |
| runtime_failure->runtime_failure | 4 |
| B->B | 3 |
| runtime_failure->A | 3 |

### Agent protocol notes

| Note | Tasks |
|---|---:|
| reached the turn limit; the benchmark asked for the final reply | 337 |
| verified the same code more than once | 310 |
| more than one correction | 150 |
| reply differs from the final report | 90 |
| corrected without a verified_incorrect layer | 54 |

### Task behaviour (secondary)

| Requirement | Baseline | Intervention (shown) |
|---|---:|---:|
| returns expected value | 672/839 | 508/614 |
| empty response ok | 97/839 | 152/614 |
| error raises | 837/839 | 613/614 |

### By API

| API | Tasks | Baseline A | Intervention A shown | Delivered | Undetermined (baseline / shown) |
|---|---:|---:|---:|---:|---|
| DummyJSON | 148 | 103 | 0 | 108 | 0 / 0 |
| GitHub | 248 | 12 | 1 | 220 | 0 / 0 |
| JSONPlaceholder | 148 | 23 | 0 | 145 | 0 / 0 |
| Open-Meteo | 148 | 109 | 1 | 83 | 0 / 0 |
| Petstore | 149 | 118 | 14 | 62 | 0 / 0 |
| REST Countries | 149 | 148 | 0 | 0 | 0 / 0 |

### Cost per task (plan §3, project description §4.8)

| Measure | Baseline mean | Intervention mean | Ratio |
|---|---:|---:|---:|
| completion_tokens | 373.1 | 1302.7 | 3.5x |
| cpu_energy_j | 273.9 | 1524.9 | 5.6x |
| duration_seconds | 5.8 | 36.9 | 6.4x |
| gpu_energy_j | 1437.9 | 7678.2 | 5.3x |
| measured_energy_j | 1711.9 | 9203.1 | 5.4x |
| model_seconds | 5.8 | 27.8 | 4.8x |
| prompt_tokens | 156.5 | 20117.7 | 128.6x |
| tool_seconds | n/a | 9.1 | n/a |

Manual review: 0 undetermined candidates in `Qwen3.5-9B-Q4_KM-full-Latest/review_queue.csv`; audit sample of 103 in `Qwen3.5-9B-Q4_KM-full-Latest/audit_sample.csv` (plan §4–5).

## Qwen3.5-9B-Q8_0-full-Latest

Quantization Q8_0, benchmark 2026-09-27.2, GPU AMD Radeon RX 9070 XT: main run (benchmark 2026-09-27.2).

### Unacceptable hallucinations reaching the user (primary, plan §3)

Rate = share of tasks whose code reaching the user is class A (API hallucination). Baseline: the code block; intervention: the delivered code, or code shown in the reply. Pilot tasks excluded; difference = baseline − intervention; discordant = baseline-only / intervention-only.

| Comparison | Tasks | Baseline | Intervention | Difference | 95% CI (tasks) | 95% CI (families) | Discordant | McNemar p |
|---|---:|---:|---:|---:|---|---|---|---:|
| **Primary** (undetermined excluded) | 990 | 55.2% | 2.0% | +53.1 pp | [+50.0, +56.3] pp | [+37.9, +65.7] pp | 529 / 3 | < 0.0001 |
| Undetermined counted as hallucination | 990 | 55.2% | 2.0% | +53.1 pp | [+50.0, +56.3] pp | [+37.9, +65.7] pp | 529 / 3 | < 0.0001 |
| Undetermined counted as correct | 990 | 55.2% | 2.0% | +53.1 pp | [+50.0, +56.3] pp | [+37.9, +65.7] pp | 529 / 3 | < 0.0001 |
| Including pilot tasks | 1000 | 55.0% | 2.0% | +53.0 pp | [+49.9, +56.0] pp | [+38.0, +65.5] pp | 533 / 3 | < 0.0001 |
| A or B (secondary) | 990 | 61.0% | 9.5% | +51.5 pp | [+48.2, +54.8] pp | [+36.7, +63.9] pp | 532 / 22 | < 0.0001 |
| A, B or runtime failure | 990 | 65.4% | 9.8% | +55.6 pp | [+52.2, +58.8] pp | [+41.4, +67.1] pp | 571 / 21 | < 0.0001 |

Holm-adjusted McNemar p across the main runs: < 0.0001. Undetermined pairs excluded from the primary row: 0. Operation families: 141.

### Classes (pilot excluded)

| Class | Baseline code | Intervention: shown to user | Intervention: final candidate |
|---|---:|---:|---:|
| A | 546 | 20 | 350 |
| B | 58 | 74 | 96 |
| correct | 341 | 510 | 538 |
| no_code | 2 | 0 | 0 |
| nothing_shown | 0 | 383 | 0 |
| runtime_failure | 43 | 3 | 6 |

### Kinds of API hallucination reaching the user (tasks; a task can have several)

| Kind | Baseline | Intervention |
|---|---:|---:|
| wrong host, version or base path | 446 | 0 |
| invented endpoint or method | 72 | 0 |
| missing required part or credential | 8 | 4 |
| invalid value or structure | 7 | 16 |
| invented parameter or body field | 7 | 0 |
| undocumented response field | 4 | 0 |
| non-existent requests API | 1 | 0 |

Tasks with a hallucination other than a wrong host, version or base path: baseline 93, intervention 20. The intervention prompt names the current hosts (by design, Benchmark README), so this row separates that context from what verification catches.


### Intervention decisions against the final candidate's class

| Final candidate | Delivered | Withheld |
|---|---:|---:|
| A | 20 | 330 |
| B | 74 | 22 |
| correct | 510 | 28 |
| runtime_failure | 3 | 3 |

- Incorrect acceptance (class A shown to the user): 20
- Incorrect rejection (correct final candidate withheld): 28
- Code shown in a reply without the tool's approval: 0

### Confidence metric (EWCS of the final candidate)

AUC, correct vs class A: 0.937 (correct n=538, A n=350).

| EWCS band | Correct | Of decided (correct, A, B) |
|---|---:|---:|
| 0.60-0.85 | 498 | 684 |
| <0.60 | 1 | 242 |
| >=0.85 | 39 | 58 |

### Corrections

Attempted 444 (allowed by the prompt: 387).

| First candidate → final | Tasks |
|---|---:|
| A->A | 166 |
| A->correct | 150 |
| undetermined->A | 62 |
| A->B | 36 |
| undetermined->B | 10 |
| undetermined->correct | 9 |
| correct->correct | 8 |
| B->B | 2 |
| B->correct | 1 |

### Agent protocol notes

| Note | Tasks |
|---|---:|
| reached the turn limit; the benchmark asked for the final reply | 383 |
| verified the same code more than once | 296 |
| more than one correction | 192 |
| corrected without a verified_incorrect layer | 57 |
| reply differs from the final report | 54 |

### Task behaviour (secondary)

| Requirement | Baseline | Intervention (shown) |
|---|---:|---:|
| returns expected value | 811/945 | 506/604 |
| empty response ok | 206/945 | 157/604 |
| error raises | 945/945 | 600/604 |

### By API

| API | Tasks | Baseline A | Intervention A shown | Delivered | Undetermined (baseline / shown) |
|---|---:|---:|---:|---:|---|
| DummyJSON | 148 | 87 | 0 | 110 | 0 / 0 |
| GitHub | 248 | 43 | 0 | 230 | 0 / 0 |
| JSONPlaceholder | 148 | 23 | 0 | 138 | 0 / 0 |
| Open-Meteo | 148 | 109 | 0 | 63 | 0 / 0 |
| Petstore | 149 | 135 | 20 | 65 | 0 / 0 |
| REST Countries | 149 | 149 | 0 | 1 | 0 / 0 |

### Cost per task (plan §3, project description §4.8)

| Measure | Baseline mean | Intervention mean | Ratio |
|---|---:|---:|---:|
| completion_tokens | 347.4 | 1502.9 | 4.3x |
| cpu_energy_j | 330.4 | 2136.9 | 6.5x |
| duration_seconds | 7.4 | 48.4 | 6.6x |
| gpu_energy_j | 1791.3 | 10888.3 | 6.1x |
| measured_energy_j | 2121.8 | 13025.2 | 6.1x |
| model_seconds | 7.4 | 38.8 | 5.3x |
| prompt_tokens | 156.5 | 21555.5 | 137.7x |
| tool_seconds | n/a | 9.6 | n/a |

Manual review: 0 undetermined candidates in `Qwen3.5-9B-Q8_0-full-Latest/review_queue.csv`; audit sample of 102 in `Qwen3.5-9B-Q8_0-full-Latest/audit_sample.csv` (plan §4–5).

