# Evaluate Benchmark

Scores the results of the [Confident Agent Benchmark](../Benchmark) as fixed in
[`Benchmark/EVALUATION_PLAN.md`](../Benchmark/EVALUATION_PLAN.md). Python 3.9+,
standard library only. It never uses the toolbox's verifier or claim extractor, so the
evaluation does not share the intervention's blind spots (plan §5).

```bat
cd EvaluateBenchmark
python evaluate_benchmark.py                          REM every run with results in both modes
python evaluate_benchmark.py --labels "Qwen3.5-9B-Q4_K_M-full-run2"
python evaluate_benchmark.py --self-check-only
python -m unittest discover tests                     REM known-answer tests of the evaluator
```

It reads `Benchmark/complete_test_baseline.jsonl` and `complete_test_intervention.jsonl`
(every model label, including archived runs) and the answer key
`COMP301-Dataset-Builder/.../output/rest_api_tasks_v1_DRAFT.jsonl` with its pinned sources.

## How a candidate is scored

1. **Run it in a sandbox** (`sandbox_harness.py`): a separate `python -I -S` process with
   the task's test inputs, where `requests` is a recording stand-in with the real
   library's names and signatures. It returns a response built from the operation's
   documented response schema. Sockets, subprocesses and file writes are blocked,
   `time.sleep` returns at once and each run has a 10 s limit. This keeps model output
   off the network and the disk; it is not a defence against deliberately hostile code.
   Each candidate runs three times: a documented success response, an empty success
   (204) and a server error (500).
2. **Read what it did**: the exact requests (method, URL, query as `requests` would encode
   it, JSON or form body, headers, auth), the response fields it read and whether each is
   documented, any `requests` function or keyword that does not exist, and the return
   value or exception.
3. **Classify** against the task's pinned OpenAPI source and `expected_request`
   (`evaluator/classify.py`, plan §2):

| Class | When |
|---|---|
| `A` | wrong host, version or base path; undeclared path or method; undeclared query parameter or body field; missing required parameter, body field or credential (when the API requires it); value of the wrong type, enum or structure; reading an undocumented response field; a `requests` API that does not exist |
| `B` | a valid call that is not the task's: another declared endpoint, a method outside `acceptable_methods`, a parameter or body value the task specifies omitted or different, an extra body field, extra requests |
| `correct` | the task's request; class C equivalences allowed (GitHub `token` for `Bearer`, methods in `acceptable_methods`, documented optional query parameters, text/number forms of query values) |
| `runtime_failure` | the code makes no request: syntax error, crash (e.g. a missing input key), or never calls the API |
| `undetermined` | an undeclared name in a **partial** specification (JSONPlaceholder, DummyJSON, REST Countries), a real `requests` feature the sandbox does not model, or another HTTP client; goes to manual review |

Behaviour (secondary, reported separately): the right return value, `None` (or the
status code) for an empty success, and an exception for a server error.

## Output (`results/`)

| File | Content |
|---|---|
| `report.md` | all runs: primary comparison with sensitivity rows, classes, the intervention's decisions against the final candidate's class, EWCS calibration, corrections, protocol notes, behaviour, per-API figures, cost |
| `self_check.json` | the dataset's reference solutions scored (all must be correct, plan §5) |
| `<label>/evaluation.json` | every figure for one run |
| `<label>/per_task.jsonl` | every task's classes and reasons |
| `<label>/review_queue.csv` | undetermined candidates for the manual review (plan §4), with their code in `review_code/` |
| `<label>/audit_sample.csv` | a stratified random sample of 50 decided candidates per mode to check by hand (plan §5) |

## Manual review

Copy rows of `review_queue.csv` (and `audit_sample.csv`) into `reviews/reviews.csv`,
have two group members fill `reviewer_1_class` and `reviewer_2_class` independently with
`correct`, `A`, `B` or `runtime_failure` using the plan's rules, then agree an
`agreed_class`. Rerun the evaluator: undetermined candidates with an agreed class are
scored with it (marked as reviewed), and agreement is reported.

## Statistics (plan §6)

Exact McNemar test on the paired primary outcome; the difference in rates with 95%
bootstrap intervals over tasks and over the 142 operation families; Holm's correction
across runs. The 10 pilot tasks are excluded from the primary result and reported in a
sensitivity row, as are the two extreme treatments of undetermined candidates.
