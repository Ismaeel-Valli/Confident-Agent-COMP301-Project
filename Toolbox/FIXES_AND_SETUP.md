# Toolbox repair: setup and verified delivery

This is the corrected successor to the supplied `confidence-agent-toolboxv3.zip`. The original broad toolbox remains available. New verification code is split into smaller modules and includes an external controller.

## Windows installation (Command Prompt)

Extract this archive. Put its `Toolbox` folder at the root of your GitHub repository, then open Command Prompt in `Toolbox`.

Use official Python 3.12 and Node.js 22.13 or newer. The previous MSYS2 Python is not the verification environment. Run these commands one at a time:

```bat
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-verification.txt
set "CONFIDENCE_PYTHON=%CD%\.venv\Scripts\python.exe"
npm ci
npm run ci
lms dev
```

The environment variable selects the same interpreter for AST extraction and Pyright. Set it again in a new Command Prompt; launch `lms dev` from that prompt so the plugin inherits it. The pinned Pyright npm package is launched via Node, avoiding Windows `.cmd` resolution and global pip/Pyright PATH problems. Enable the Confidence Agent tools and Allow Pyright in LM Studio.

In PowerShell, the equivalent environment assignment is:

```powershell
$env:CONFIDENCE_PYTHON = "$PWD\.venv\Scripts\python.exe"
```

The plugin identity remains `beledarian/confidence-agent-toolbox`. Stop an older development instance before starting this one. `npm run build` compiles TypeScript and rebuilds `.lmstudio/dev.js` from the current source. Do not copy the old V3 bundle into this folder. `npm run ci` performs type-checking, the build and the complete test suite. Tests do not require a running LM Studio model, but require the verification Python environment above.

## Retest the September pilot

Start with `PILOT_RETEST.md` for the new native prompt, bundled reference, reproducible controller command and independent behavioral checks. `verify_candidate` now accepts `reference_id: "jsonplaceholder-posts"` and returns `toolbox_version: "1.5.0"`. Do not reuse the old per-layer prompt.

## Run the enforced verification path

A native tools-provider plugin exposes functions; it cannot stop Qwen from skipping them or writing a different chat reply. The external controller is the delivery boundary. It takes the same saved initial candidate as your baseline, always runs all six layers, scores the actual returned results, optionally requests one correction, rechecks it, and writes the final report itself.

Keep LM Studio's local server running only if you want a model correction. The verification/controller path does not execute candidate programs. The separate, explicitly invoked `evaluate:pilot` development check executes only the two shipped reviewed fixtures with mocked HTTP.

Run a valid development example without correction:

```bat
npm run verify -- --code examples/jsonplaceholder-valid.py --spec examples/jsonplaceholder-posts.openapi.json
```

Run a parameterized example with explicit task inputs:

```bat
npm run verify -- --code examples/jsonplaceholder-parameterized.py --spec examples/jsonplaceholder-posts.openapi.json --inputs examples/inputs.json
```

Omitting input bindings for a dynamic URL intentionally produces an unverifiable result and abstention. Bindings are verification assumptions, included in the audit; they are not a claim that the function works for every possible input.

To permit exactly one correction, supply the **exact model identifier from LM Studio**:

```bat
npm run verify -- --code examples/jsonplaceholder-invalid.py --spec examples/jsonplaceholder-posts.openapi.json --model YOUR_EXACT_MODEL_ID
```

Do not type the placeholder unchanged. For your current setup, select the identifier of your Qwen3-1.7B model. The default server is `http://127.0.0.1:1234/v1`; `--endpoint` can override it. The controller asks that same model for one minimal rewrite only after a verified contradiction. It does not ask the model to score or approve its own answer. Timeout, refusal, truncation, invalid source, unsuccessful correction or remaining critical uncertainty produces abstention. Correction settings are recorded: temperature 0.3, top-p 0.9, maximum output 4,096 tokens. Keep model/quantization/context settings fixed and recorded for the experiment.

Each run creates a new `verification-runs/run-...` folder:

- `report.md`: final user-facing report. Withheld candidates are not included.
- `audit.json`: experiment record containing initial and corrected candidates, six results, Pyright output/version/environment, evidence, hashes, decisions and correction failures. This audit intentionally preserves withheld code for researchers.
- `delivered.py`: created only for `deliver` or `deliver_with_flag`.

`--out-dir` specifies a **new** run directory. An existing destination is rejected so an old delivered file cannot be mistaken for a new successful result. `--task` supplies the original task description for correction. Do not score correction success solely from EWCS; independently assess whether the rewrite still solves that task.

PyPI retrieval failure now causes uncertainty, not a nonexistent-library verdict. For reproducible offline runs, save the `evidence.packages` object from a reviewed successful run and provide it through `--package-evidence saved-packages.json`. Use that same frozen evidence across the paired conditions. A snapshot is a trusted experiment input; do not ask the model to generate it. The test suite's synthetic metadata is for testing only.

## What was fixed

| Previous failure | Corrected behavior |
|---|---|
| Only one successful layer could yield 100% and delivery | Missing layers retain their canonical weights; complete evidence is required before delivery. |
| An empty applicable set looked like a meaningful zero | EWCS and signed score are `null`; the policy abstains. |
| Pyright configuration/process failure could become a pass | Structured JSON, process status, analyzed-file count and diagnostic consistency are validated. Missing packages/stubs and relevant unknown types are uncertainty. Annotation diagnostics for AST-confirmed unused parameters are nonblocking; raw diagnostics remain in the audit. |
| Clean Pyright was used as proof of arbitrary JSON fields | Output verification requires a linked response schema. Pyright cannot replace missing REST evidence. |
| Network errors were called nonexistent libraries | Lookup has explicit found/not-found/unverifiable states. Even a registry 404 does not prove a local/private import is nonexistent. |
| Input dictionary reads were treated as response fields | Response provenance starts at the particular HTTP call's `.json()` value. |
| Variable URLs/input dictionaries disappeared | Literal assignments and aliases resolve statically; runtime URLs remain explicit unresolved claims, or resolve against supplied task bindings. |
| Only the first endpoint/path was checked | Every call has an identifier; server origin/base path/method and each call's own contract are checked. |
| Missing required inputs and invalid values passed | Required inputs, locations, scalar constraints, JSON bodies and local references are checked for the supported subset. |
| A comment containing “bearer” passed authentication | Only actual request arguments count; inherited/overridden security, OR alternatives and AND requirements are respected. |
| Abstain/correct reports contained source | Code is omitted. Candidate hashes and restrictive decisions are checked before including it. |
| Floating-point noise appeared in layer contributions | Contributions and aggregate display values are rounded to four decimal places. |
| Model-controlled tool order/correction/report copying | External controller preserves actual results, enforces one correction and owns final output. |
| Stale bundled plugin | Build now regenerates `.lmstudio/dev.js`, including `verify_candidate` and structured Pyright. |

Weights remain 3/3/4/2/1/2, tier factors remain 1.0/0.8/0.9/0.5, and delivery thresholds remain 0.85/0.60. All applicable categories are treated as critical in this first supported subset. Contradiction requests one correction; after the budget is exhausted it abstains. Otherwise incomplete extraction, failed required checks or any unverifiable applicable layer causes abstention before thresholds are considered.

The original 3.9/8 worked example remains 0.4875. The fix does not inflate scores to make correct code pass. EWCS is an evidence score, not a calibrated probability that the code is correct.

## Supported scope and limitations

- Python 3.12, direct `requests.get/post/put/patch/delete/head/options/request` calls, import aliases, simple literal assignments, dictionary arguments, string concatenation/f-strings with known values, simple function parameters with explicit bindings, response `.json()`, response aliases, nested subscripts and simple iteration over JSON arrays.
- OpenAPI **3.0.x JSON** with explicit absolute server URLs, operation/path server overrides, inherited parameters, local JSON-pointer `$ref`, scalar types, enums, common numeric/string/array/object constraints, required properties and JSON bodies. OpenAPI 2/3.1, external/cyclic refs, unions/compositions and unimplemented constraints stay unverifiable. Unsupported schema semantics must not be used to assert a contradiction.
- Native dictionary input reads are not output claims. Session objects, alternate HTTP clients, dynamic callables, custom JSON decoding, checker-suppression directives, mutations and unsupported control flow produce explicit extraction limitations. Response guards on tracked content/text/status/ok are supported when each nonempty branch terminates in return or a supported exception, optionally after simple local assignments. Ordinary branch changes to requests, aliases or headers remain unresolved. Extend the supported subset with regression tests rather than suppressing those limitations.
- Input serialization supports primitive parameters and JSON bodies. Complex query encodings, form/multipart bodies and custom auth adapters are unresolved. Extra query/header/cookie names are **undocumented**, not automatically forbidden by OpenAPI; they remain unverifiable. Undeclared response fields are a contradiction only in a closed schema; open schemas remain uncertain.
- Output checks concern documented success-response field shapes. They do not execute requests, prove array bounds, ensure network success or prove application logic. Missing/optional fields, ambiguous success responses and missing JSON schemas remain uncertain.
- Authentication checks cover static placement and shape of API keys and HTTP bearer/basic credentials. They do not validate credentials with a provider; OAuth scopes, dynamic tokens and undocumented version/deprecation requirements remain unresolved.
- Pyright checks the pinned configured environment; it is supporting evidence, not proof of arbitrary runtime behavior. No user-selected Python module is imported to resolve package-existence claims.

The JSONPlaceholder file is a **reviewed partial reference derived from provider documentation**, not an official OpenAPI document or a complete API inventory. See `examples/JSONPLACEHOLDER_REFERENCE_REVIEW.md` for the evidence and limitations. Example fields are optional and filtering is outside this snapshot. It uses tier 2. Freeze its hash and record the review method before experimental use. Operations outside that subset remain unverifiable. The synthetic closed API fixture in `tests/fixtures/api.json` is strictly a regression fixture.

## Validation and experimental use

See `VALIDATION.md` for the exact completed checks and their limits. Unit tests use injected network/process/model responses to reproduce failures, and integration tests also run the real pinned Pyright. The CLI adapter is checked against an OpenAI-compatible local test server; that does not establish Qwen's correction quality. Run the LM Studio pilot on your Windows machine after installing this package.

Preserve baseline and intervention pairing, separately count incorrect code delivered and correct code withheld, and independently adjudicate corrections. The 1.7B model and its context settings are a different experimental configuration from the earlier 9B pilot.

References: [OpenAPI 3.0.3](https://spec.openapis.org/oas/v3.0.3), [Pyright CLI and JSON diagnostics](https://github.com/microsoft/pyright/blob/main/docs/command-line.md), [JSONPlaceholder guide](https://jsonplaceholder.typicode.com/guide/).

## Coverage refinement in 1.5.0

Registry evidence for explicit imports is retained even when response-flow extraction is incomplete. This is not a claim of exhaustive import coverage. Other affected checks stay unresolved, and incomplete extraction still blocks delivery before thresholds. Unsupported or used untyped parameters still produce uncertainty; only precisely located annotation diagnostics for unused parameters are filtered.

Reports now include actual layer explanations and state that task behavior is not verified. The independent pilot evaluator catches the original always-return-None bug; it is separate from the six API-claim layers and never affects EWCS. See `evaluation/PILOT_BEHAVIOR_RESULTS.json` for the checked fixtures and their hashes.
