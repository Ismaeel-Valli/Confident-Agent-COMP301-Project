# Validation — toolbox repair 1.5.0

Completed on 2026-09-24 in Linux. This follows the 1.4.0 safeguards repair and addresses the supplied JSONPlaceholder pilot trace.

## Completed checks

- TypeScript type-check, compilation and fresh native plugin bundle: passed.
- Full test suite: **154 passed, 0 failed, 0 skipped** (the prior 137 plus 17 pilot-coverage tests).
- Environment: Python 3.12.14, Node.js 24.19.0, pinned Pyright 1.1.414, requests 2.32.5, types-requests 2.32.4.20250913. Exact npm dependencies remain recorded in the lockfile.
- Real command-line verification of `examples/jsonplaceholder-solve.py`, with the reviewed reference and recorded pilot package metadata: **EWCS 0.725, deliver_with_flag**. The controller saved its report/audit and delivered the matching candidate.
- Native SDK `verify_candidate` was invoked with `reference_id: "jsonplaceholder-posts"`, a mocked registry response and real Pyright. It preserved metadata internally, reported version 1.5.0, used the correct reference hash and returned 0.725. A conflicting explicit spec was rejected.
- Independent mocked behavioral evaluation: **corrected reference 11/11**, **original pilot 6/11**. The original fails populated 200, empty 200, empty 204, populated 201 and empty-array cases. Case results and candidate hashes are in `evaluation/PILOT_BEHAVIOR_RESULTS.json`.

Final suite command:

```sh
CONFIDENCE_PYTHON="$PWD/.verification-venv/bin/python" npm run ci
```

Windows setup and exact retest commands are in `PILOT_RETEST.md`.

## What the new checks establish

Response guards on tracked responses retain request/response provenance. New requests in conditions are captured; branches that change requests, aliases, headers or flow remain incomplete. Incomplete extraction keeps its delivery block. Explicit import evidence survives independent response-flow limitations, without asserting exhaustive import coverage.

Real Pyright tests confirm unused-parameter annotation diagnostics are nonblocking, while used and closure-captured untyped parameters remain unresolved. The filter uses exact diagnostic locations and same-candidate AST metadata, and the controller retains raw diagnostics. Missing packages/stubs, malformed output, process failure, undefined names and other relevant errors keep the previous safeguards.

The reviewed partial reference no longer declares example properties universally required or invents an integer-only filter contract. Optional property access can be checked; direct access to a non-guaranteed field remains uncertain. Unsupported filters and operations remain unresolved.

The original 1.4.0 suite continues to check missing layers, hash binding, failed checkers, failed lookups, wrong hosts/methods, required inputs, multiple operations, response provenance, authentication, correction limits and withholding. The CLI correction integration uses a local OpenAI-compatible stub and real Pyright on both candidates; it does not measure Qwen performance.

## Independent evaluation and a known limitation

`evaluation/PILOT_STATIC_RESULTS.json` records static results for both exact fixtures, using the same frozen evidence. **Both score 0.725 and meet API-claim delivery policy.** The original's incorrect return value is not contradicted by its valid endpoint/import claims. The separate behavioral evaluator exposes the bug. No benchmark answer, behavioral pass count or evaluator outcome is fed into EWCS or correction.

The new report explicitly limits its claim to API/static evidence. Delivery is not proof of complete task correctness. The behavioral check is a separate development evaluator, explicitly invoked with `npm run evaluate:pilot`; it executes only two shipped, reviewed fixtures with mocked HTTP. It is not a sandbox, does not accept arbitrary paths, and is not run by verification or the controller.

Here, successful empty response means an empty HTTP body; `[]` is decoded to an empty list. HTTP failure is checked before JSON parsing. If a benchmark specifies different semantics, freeze and document that interpretation before evaluation.

## Remaining boundaries

- No Windows runtime or real LM Studio/Qwen session was run here. Native SDK invocation and rebuilding the bundle are not a substitute for the Windows pilot.
- Deterministic positive checks use recorded/injected package evidence. This release does not claim successful fresh PyPI retrieval; native chat still depends on live retrieval. The previous live lookup timeout correctly abstained.
- The JSONPlaceholder snapshot is a reviewed, secondary, partial reference at tier 2, with documented assumptions. It is not official OpenAPI or an exhaustive service contract. See `examples/JSONPLACEHOLDER_REFERENCE_REVIEW.md`.
- The extractor supports the documented bounded requests/response-guard subset. General control flow, sessions, other clients and interprocedural analysis remain outside scope.
- A native model can still skip tools or rewrite the report. Use the external controller for experimental delivery and preserve saved-baseline pairing.
- These development results do not establish hallucination reduction. Independently evaluate incorrect deliveries, correct candidates withheld, API-claim errors and unrelated logic errors across the frozen benchmark.
