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

Each candidate is compared with the task's `test_case.expected_request` (method, URL,
query, JSON body, credential placement) and `api_specification` (declared parameters,
body fields, acceptable methods, `response_schema`), with the task's test inputs bound to
`inputs`. Code is read statically.

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

## 5. Answer-key audit

The answer key reads code with the toolbox's own claim extractor, a component the
verifier also uses (evaluator bias). A random sample of 50 decided candidates per mode,
stratified by API, is classified by hand as in §4; the answer key's error rate on the
sample is reported.

## 6. Statistics (§4.7)

- **Test:** exact McNemar test on the paired primary outcome; two-sided, α = 0.05.
- **Effect size:** the difference in proportions with a 95% confidence interval, and the
  ratio of discordant pairs.
- **Several runs** (quantizations, models): one test per run, with Holm's correction
  across runs. Differences between runs are described, not tested, unless the same tasks
  are repeated with several seeds.
- Results are broken down by API descriptively.

## 7. Runs

- **Run 1** (benchmark 2026-09-26.2) and **run 2** (benchmark 2026-09-27.1) are scored
  with this plan. Run 2 is the main result.
- Run 2 includes a verifier change found by inspecting run 1: an undeclared request-body
  field in a schema that does not mention extra fields is now unresolved, as an undeclared
  query parameter already was. This is disclosed as a change made after seeing run 1;
  both runs are reported so its effect is visible.
- The benchmark prompts and the dataset are not changed between runs (§4.6).

## Changes after 2026-09-27

None yet.
