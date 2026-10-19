# Evaluation plan

Fixed on 2026-09-27, **before** benchmark run 2, so that the scoring rules are not chosen
after seeing the results (project description §4.8, overfitting and evaluator bias). Any
later change must be listed at the end of this file with its reason.

`evaluate_benchmark` implements this plan. It reads the benchmark's results and the
dataset; it never runs generated code.

## 1. What is compared

- **Unit:** one benchmark task. Every task has one baseline result and one intervention
  result from the same model, settings and prompt text (§4.4–4.6), so the comparison is
  paired.
- **Baseline:** the model with `BASELINE_SYSTEM_PROMPT.md`; its code block is what a user
  would receive.
- **Intervention:** the Confident Agent (toolbox prompt plus `verify_candidate`). Code
  reaches the user only when the tool's final decision is `deliver` or
  `deliver_with_flag`, or when the model's reply shows code anyway (`reply_code`).
- Each model or quantization is a separate run (`--model-label`) scored the same way.

## 2. Answer key and error classes

The answer key is the dataset's task file,
`Code Submission/COMP301-Dataset-Builder/comp301-dataset-builder/output/rest_api_tasks_v1_DRAFT.jsonl`
(SHA-256 with LF line endings `7a09f2bb…a12`), together with the provider specifications
it pins in `sources/` (file name and SHA-256 per task). Its prompts are exactly those the
benchmark sent (`rest_api_prompts_v1_DRAFT.jsonl`, `c4c68a64…278` with LF endings; run 1
recorded `a8eeb5e4…` for the same content with CRLF endings). See §8 for the checks made
on it.

Each candidate is compared with the task's `test_case.expected_request` (method, URL,
query, JSON body, credential placement) and `api_specification` (declared parameters,
body fields, acceptable methods, `response_schema`), with the task's test inputs bound to
`inputs`. `$ref`s in `api_specification` (most GitHub and Petstore response schemas) are
resolved in the pinned source file.

**Partial specifications.** JSONPlaceholder, DummyJSON and REST Countries use
documentation-derived partial specifications (450 tasks). A missing entry in a partial
specification is not proof that a name does not exist (dataset audit). For these APIs an
undeclared parameter, body field or response field is class A only when the provider's
public documentation confirms it does not exist; otherwise the candidate is
**undetermined** and goes to the manual review of §4.

| Class | Meaning | Examples | Counts as |
|---|---|---|---|
| **A: API hallucination** | The code breaks the API's contract | wrong host or outdated version (`petstore.swagger.io/v2`); undeclared path or method; undeclared parameter or body field (`name` for `new_name`); missing required parameter or field; value of the wrong type, enum or structure; reading a response field the response schema does not define | **unacceptable hallucination** (primary outcome) |
| **B: task-fidelity error** | A valid API call, but not the one the task asked for | method outside the task's `acceptable_methods` (PUT for a partial update); a different declared endpoint; omitting a parameter the task specified; a different value | reported separately (secondary outcome) |
| **C: equivalent** | Different text, same accepted request | `Authorization: token X` for `Bearer X` (GitHub accepts both for personal tokens); a method listed in `acceptable_methods`; `3` for `"3"` in a query; an extra optional parameter the specification documents and the task does not constrain | correct |
| **Correct** | No A or B difference | | correct |

A candidate with both A and B differences is class A. The list of equivalences in C is
closed: anything else that differs is A or B.

### Response fields (part of class A)

The request can be right while the code reads fields the response does not have (for
example `data["product"]["id"]` when DummyJSON returns the product at the top level).
The answer key therefore also checks every response field the code reads against
`api_specification.response_schema`: a field the schema does not define is class A,
unless the schema explicitly allows additional properties. Without this check such code
would be scored correct and its rejection by the verifier scored as a false rejection.

## 3. Outcomes

**Primary (hypothesis, §1.3):** *an unacceptable hallucination reaches the user*, per task:
- baseline: the code block is class A;
- intervention: the delivered code or the code shown in the reply is class A.

**Secondary:**
- the same with class A or B;
- incorrect rejection (§4.6): the intervention withholds code that is correct or class C;
- the intervention's confusion matrix: correct/incorrect acceptance and rejection;
- confidence metric: EWCS for correct against incorrect final candidates (AUC, share
  correct per decision band);
- corrections: how often a contradiction was corrected, and whether the correction was
  correct;
- protocol compliance of the agent (from `protocol_notes`);
- cost (§4.8): time, model tokens and GPU energy per task, baseline against intervention.

## 4. Candidates the answer key cannot decide

When the request depends on a condition or a value the static reading cannot resolve
(for example `if "limit" in inputs: params["limit"] = ...`), the answer key reports
**undetermined** instead of guessing (run 1: 152 baseline, 16 intervention).

1. **Manual review.** Two group members classify every undetermined candidate
   independently with the rules of §2, reading the code with the task's test inputs.
   Disagreements are settled by discussion. Both first classifications are kept, and
   agreement is reported as Cohen's kappa.
2. **Robustness.** The primary result is also reported with every undetermined candidate
   counted as class A, and with every one counted as correct. A conclusion is only drawn
   if it holds in all three versions.

## 5. Evaluator independence and audit

The evaluator must not reuse the toolbox's claim extractor or verifier: a component shared
with the intervention would share its blind spots (evaluator bias, §4.8; the dataset audit
asks for an independent evaluator). `evaluate_benchmark` reconstructs each candidate's
request with its own code. It must at least handle what the dataset's reference solutions
use; the shared extractor, for example, leaves all 150 Open-Meteo references undetermined
(`",".join(str(v) for v in [...])`).

**Method (decided 2026-09-27): sandboxed execution.** Each candidate runs in a separate,
isolated Python process with the task's test inputs, against a recording stand-in for
`requests` that has the real library's names and signatures and returns a response built
from the documented response schema. No request leaves the machine; sockets,
subprocesses and file writes are blocked. This gives the exact request the code sends
(conditions, loops and comprehensions included), the response fields it reads, and uses
of `requests` functions or keywords that do not exist (class A). Each candidate also runs
against an empty success and a server error for the behaviour checks. Details:
`Findings/EvaluateBenchmark/README.md`.

**Interpretations fixed with the method:** a candidate that makes no request (syntax
error, crash such as a missing input key, or no call) is `runtime_failure`: not an API
hallucination, counted in the "any error" row; an extra body field the specification
documents is class B (it changes what is written), while an extra documented query
parameter is class C (§2); a real `requests` feature the stand-in does not model, or
another HTTP client, is undetermined.

**Self-check.** Before scoring, the evaluator scores the dataset's 1,000 reference
solutions: all must be correct. Any that are not point to an evaluator or answer-key error
and are resolved before scoring model output.

**Audit.** A random sample of 50 decided candidates per mode, stratified by API, is
classified by hand as in §4; the evaluator's error rate on the sample is reported.

## 6. Statistics (§4.7)

- **Test:** exact McNemar test on the paired primary outcome; two-sided, α = 0.05.
- **Effect size:** the difference in proportions with a 95% confidence interval, and the
  ratio of discordant pairs.
- **Related tasks.** The 1,000 tasks come from 142 operation families (Open-Meteo 3,
  REST Countries 4), so tasks are not independent. A cluster bootstrap over operation
  families (10,000 resamples) gives a second 95% interval for the difference; a
  conclusion is drawn only if it holds under both.
- **Pilot tasks.** The 10 pilot tasks (`dataset/rest_api_prompts_pilot.jsonl`) were used
  to develop the agent and are excluded from the primary analysis; results including them
  are reported as a sensitivity check.
- **Several runs** (quantizations, models): one test per run, with Holm's correction
  across runs. Differences between runs are described, not tested, unless the same tasks
  are repeated with several seeds.
- Results are broken down by API descriptively.

## 7. Runs

- **Final runs (from 2026-10-06).** The findings use one complete set of runs of
  Qwen3.5-9B, made 30 September to 3 October 2026 with benchmark 2026-09-27.2 on one
  machine: Q4_K_M, Q6_K and Q8_0 (`Benchmark/Completed Runs/`). These are the main
  runs and the Holm family of §6. The earlier runs below are kept in
  a superseded-runs folder kept outside the public repository (their rows remain in `complete_test_*.jsonl`) and are not part of the findings; see the change
  of 2026-10-06 for why.
- **Run 1** (benchmark 2026-09-26.2) and **run 2** (benchmark 2026-09-27.2) are scored
  with this plan. Run 2 was the main result until the final runs replaced it.
- **Quantizations.** The same model at further quantization levels (Q6_K, Q8_0) is run
  with run 2's benchmark version, settings and machine, and scored with this plan.
  A run is **main** when it used the newest benchmark version among the runs, and
  **preliminary** when it used an older one (run 1: no power or timing data, and the
  verifier before the fixes). Only main runs are compared with each other and form the
  Holm family of §6; preliminary runs are scored and reported with their uncorrected
  p-value. The quantization of a run is the one LM Studio reported for the loaded model,
  not the one in its label.
- Run 2 includes a verifier change found by inspecting run 1: an undeclared request-body
  field in a schema that does not mention extra fields is now unresolved, as an undeclared
  query parameter already was. This is disclosed as a change made after seeing run 1;
  both runs are reported so its effect is visible.
- The benchmark prompts and the dataset are not changed between runs (§4.6).

## 8. Dataset readiness

**Checked on 2026-09-27 (before run 2):**

| Check | Result |
|---|---|
| Task and prompt files agree (ids, instructions) | ✔ 1,000 tasks, identical instructions, no duplicates |
| Prompts are those run 1 sent | ✔ same content (only line endings differ) |
| Pinned sources present and unchanged | ✔ all 8 files match their SHA-256 |
| Reference solutions satisfy the answer key | ✔ none judged wrong (850 correct; 150 Open-Meteo undetermined by the shared extractor, see §5) |
| Tasks that return one field: the reference reads it | ✔ 251 of 251 |
| Expected values follow from the instruction or the test inputs | ✔ apart from natural-language mappings the model is meant to know (e.g. "temperature at two metres" → `temperature_2m`) |
| Method rules consistent | ✔ PATCH for partial updates, PUT for replacement; DummyJSON documents both |
| Verifier on the reference solutions | ✔ no contradictions (see the toolbox's reference regression) |

**Still required, by the team, before the final scoring:**

1. **Human review** of the stratified 100-task sample in
   `Code Submission/COMP301-Dataset-Builder/comp301-dataset-builder/review/review_100.csv` (still empty):
   is each task's expected request correct and the only acceptable one, against the
   provider's documentation? Two reviewers, as in §4. Systematic errors widen the review.
   Every answer-key correction is logged below and applied to all runs alike.
2. **Report** the differences from Progress Report 2 in operation, difficulty and
   authentication mix (`DATASET_AUDIT.md`). The prompts cannot be changed after the
   baseline (§4.6), so they are described, not fixed.
3. **State the design choice** that departs from the dataset audit's recommendation 5
   (reuse one initial answer for both conditions): each mode generates its own answer
   because the intervention is the agent package (prompt plus tool), not the verifier alone.

## Changes after 2026-09-27

- 2026-09-27 (before run 2): §2 answer-key identity, `$ref` resolution and the rule for
  partial specifications; §5 evaluator independence and self-check; §6 operation-family
  clustering and exclusion of the pilot tasks; §8 dataset readiness. Prompted by the
  dataset audit and the dataset checks in §8, not by run 1's outcomes.
- 2026-09-27 (before run 2): §5 evaluation method (sandboxed execution) and the
  interpretations fixed with it (runtime failures, extra body fields). Chosen by the team
  before the evaluator had scored any model output; the evaluator's self-check on the
  1,000 reference solutions passed (all correct) before it was run on run 1.
- 2026-09-30: §6 and §7 clarify the Holm family: the main runs only (newest benchmark
  version), with run 1 as a preliminary run. Run 2 and the Q6_K and Q8_0 runs had been
  made but not yet scored when this was decided, so it was fixed before their results were
  seen. Also corrects run 2's benchmark version to 2026-09-27.2 (§7).
- 2026-10-06: §7 the findings use the final set of runs (Q4_K_M, Q6_K and Q8_0, made
  30 September to 3 October 2026) instead of run 2 and the first Q6_K and Q8_0 runs. Reason:
  during the first Q6_K intervention run the machine's throughput fell to about half
  (GPU power about 240 W to 193 W, from about 12:30 on 29 September) and stayed there,
  so the cost figures of the first series were not comparable across quantizations. The
  team reran all three quantizations in one series, with the same benchmark version,
  settings, toolbox and machine. LM Studio's runtime (ROCm) updated itself automatically
  twice after the first series; the runtime version is not recorded in the run manifests,
  so whether it changed within the final series cannot be shown from the data. The scoring
  rules are unchanged. The final runs were evaluated once
  (2026-10-05) before this decision; their accuracy figures agree with the first series
  within about 2 percentage points (repairs, regressions and Holm-corrected significance
  alike), so the choice does not change the conclusions. The superseded runs are kept in
  a superseded-runs folder kept outside the public repository (their rows remain in `complete_test_*.jsonl`); Q4_K_M and Q8_0, each run twice with the same
  settings, can be reported as a repeat-run check.
- 2026-10-06: §4 manual review of the final runs' undetermined candidates (396 distinct
  candidates: 46 that reached the user, 350 that were withheld). For lack of time it was made
  with AI assistance (Claude), not by two group members independently, so no agreement
  (kappa) can be reported. Each question a partial specification left open was checked once
  against the provider's documentation and, where the documentation is silent, the live
  public API; the answers are recorded as rules with their evidence in
  `EvaluateBenchmark/reviews/review_rules.py`, and every decision with its reason in
  `reviews/reviews.csv` (`reviewer_2_class` left for a group member's check). The §2 rules
  were applied unchanged: a name the provider does not have is class A; a name it has is
  judged as for an official specification.
- 2026-10-07: §4 second review. A group member classified the 46 reviewed candidates that
  reached the user (`reviewer_2_class`) independently of the first review: agreement on 43
  of 46, Cohen's kappa 0.88 (first review AI-assisted, second by a group member). The three
  disagreements (REST_PY_JP_0009, _0015, _0071: the agent's shown code reads the resource
  from a list endpoint, `/comments?id=` or `/albums`, instead of `/comments/{id}` or
  `/albums/{id}`) were settled by the group as correct, because the code returns the
  resource the task asks for. Under the closed list of §2 a different declared endpoint is
  class B, so this relaxes §2 for these three candidates; it changes only the intervention's
  correct-code figures (Q6_K one task, Q8_0 two, Q4_K_M none) and no hallucination figure. The 350 withheld
  candidates have the first review only.
