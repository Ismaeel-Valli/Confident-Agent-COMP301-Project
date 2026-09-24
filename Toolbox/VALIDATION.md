# Validation — toolbox repair 1.4.0

Completed on 2026-09-24 in a Linux execution environment.

## Results

- TypeScript type-check: passed.
- TypeScript compilation: passed.
- Plugin bundle: rebuilt successfully from current source. The generated `.lmstudio/dev.js` contains `verify_candidate`, structured Pyright invocation and the revised missing-layer policy.
- Full test suite: **137 passed, 0 failed, 0 skipped**. This comprises 93 existing tests and **44 new verification regression/integration tests**.
- Verification environment: Python 3.12.14, Node.js 24.19.0, Pyright 1.1.414, requests 2.32.5 and types-requests 2.32.4.20250913. Pyright and esbuild 0.28.2 are exact npm dependencies recorded in the lockfile.

The final command used the verification virtual environment:

```sh
CONFIDENCE_PYTHON="$PWD/.verification-venv/bin/python" npm run ci
```

On Windows, follow `FIXES_AND_SETUP.md` to create `.venv` and set `CONFIDENCE_PYTHON` before running `npm run ci`.

## What the new tests establish

They reproduce missing-verifier delivery, failed/malformed checker output, package lookup failure, response-provenance mistakes, unresolved URLs, wrong hosts/base paths/methods, missing and invalid inputs, mixed operations, local references, response arrays, authentication comments and security overrides. They also exercise schema limitations, suppressed checker diagnostics, style-only diagnostics, hash binding, rounding, withholding and the correction budget.

Real Pyright integration detects `undefined_name` and checks a valid requests candidate. The shipped parameterized JSONPlaceholder example is delivered with a flag when explicit task bindings are supplied, and withheld without those bindings. Package metadata is injected in those tests to keep them independent of live registry availability.

The CLI integration test starts a local OpenAI-compatible test server, sends exactly one correction request, runs real Pyright on both candidates, rechecks all contracts, preserves the initial candidate in the audit, and creates `delivered.py` only after the corrected candidate meets policy. This server supplies a fixed correction; it is not Qwen and does not measure model performance.

A separate command-line run using live PyPI retrieval encountered a network timeout. It returned `interface: unverifiable`, abstained and withheld code. It did not claim that requests was nonexistent. This demonstrates the corrected failure behavior; it is not a successful live-registry verification result.

## Limits

- The plugin has **not** been launched inside a real LM Studio instance or tested on Windows in this environment. Repeat the native tool-call smoke test after installing it on your PC.
- No real Qwen model correction was run here. Context limits, model output quality and local server availability need the LM Studio pilot.
- Verification is restricted to the documented Python requests/OpenAPI 3.0 subset. Unsupported code or contract features are withheld as uncertainty. These tests do not prove correctness for arbitrary Python or arbitrary API specifications.
- Native chat remains controlled by the model. The external controller is the route that enforces verification and final delivery.
- The JSONPlaceholder reference is a curated, partial development fixture, not a provider-published OpenAPI document. Its assumptions require team review before benchmark use.
- No effectiveness claim is made about hallucination reduction. That requires independently adjudicated paired baseline/intervention results, including correct code withheld.
