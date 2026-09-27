# Evaluation report

Evaluator 2026-09-27.1, 2026-09-27T20:04:19+00:00. Rules: `Benchmark/EVALUATION_PLAN.md`.

- Answer key: task file SHA-256 `7a09f2bb566dbabb…` (matches the plan).
- Self-check: 1000/1000 reference solutions scored correct; behaviour requirements met by 1000.
- Manual reviews applied from: none yet (undetermined candidates are excluded from the primary result).
- Intervals: 10000 bootstrap resamples (seed 301), over tasks and over operation families.

## Qwen3.5-9B-Q4_K_M-full

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

Holm-adjusted McNemar p across runs: < 0.0001. Undetermined pairs excluded from the primary row: 14. Operation families: 141.

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
| missing required part or credential | 7 | 5 |
| non-existent requests API | 2 | 0 |
| other | 1 | 0 |
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

