# Confident Agent Toolbox

Static verification of REST API claims in LLM-generated Python code, for the UKZN
COMP301 Confident Agent project. It contains:

- an **LM Studio tools provider** for interactive demonstrations, and
- an **external controller CLI** (`npm run verify`) that enforces verification,
  at most one correction and the decision policy. Use the CLI for experiments;
  chat results are model-controlled.

Candidate code is **never executed**. Pyright is the only subprocess run on it,
and it performs static analysis. Evidence comes from frozen, bundled OpenAPI
snapshots, selected by the host the code calls.

## What the model can call

| Tool | Purpose |
|---|---|
| `verify_candidate` | Runs all six layers, scores (EWCS) and decides. Pass only `code`. The normal path. |
| `extract_claims` | AST claim extraction (imports, calls, endpoints, inputs, response fields). |
| `verify_interface` | Layer 1: imported modules (PyPI metadata, standard library). |
| `verify_identifier` | Layer 2: names, attributes and calls (Pyright). |
| `verify_access_point` | Layer 3: host, path and HTTP method. |
| `verify_input_contract` | Layer 4: parameters, locations, types, bodies. |
| `verify_output_contract` | Layer 5: response fields read by the code. |
| `verify_contextual` | Layer 6: authentication placement and scheme. |
| `compute_ewcs`, `make_decision`, `present_report` | Scoring, policy and report (inspection only; only `verify_candidate` binds a report to code). |
| `query_pypi`, `resolve_api_spec` | Package metadata; spec discovery summary (never the full document). |
| `save_code` | Writes a file inside the configured workspace. |
| `run_pyright` | Raw Pyright JSON diagnostics for inspection. |

Evidence for these hosts is bundled: `jsonplaceholder.typicode.com`,
`api.github.com`, `api.open-meteo.com`, `air-quality-api.open-meteo.com`,
`marine-api.open-meteo.com`, `dummyjson.com`, `api.restcountries.com`,
`petstore3.swagger.io`. Other hosts abstain on layers 3 to 6.

## Windows setup

Requirements: Node.js 22.13 or later, Python 3.12, LM Studio 0.4 or later with
the `lms` command available.

In Command Prompt, from the extracted `confident-agent-toolbox` folder:

```bat
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-verification.txt
npm ci
npm run build
set "CONFIDENCE_PYTHON=%CD%\.venv\Scripts\python.exe"
npm test
```

In PowerShell, set the variable with `$env:CONFIDENCE_PYTHON = "$PWD\.venv\Scripts\python.exe"`.

`npm test` runs the offline suite. The behavioural evaluator that executes the
shipped pilot fixtures is opt-in (`set RUN_BEHAVIOR_EVAL=1`), because one fixture
is model-generated code.

## LM Studio setup

1. From this folder run `lms dev`. LM Studio loads the plugin as
   `comp301-skeptics/confident-agent-toolbox`.
2. In the plugin settings:
   - **Confident Agent tools**: on.
   - **Allow Pyright**: on (static analysis only).
   - **Verification Python**: the full path to `.venv\Scripts\python.exe` in
     this folder. LM Studio does not inherit your terminal's `CONFIDENCE_PYTHON`.
   - **save_code folder**: optional; defaults to `%USERPROFILE%\confident-agent-workspace`.
3. Start a new chat and use `instructions/CONFIDENCE_AGENT_PROMPT.md` as the
   system prompt.
4. A `verify_candidate` result should report `toolbox_version: "3.0.0"` and an
   `evidence_selection` line naming the frozen snapshot.

To publish with `lms push`, first change `owner` in `manifest.json` to your
LM Studio Hub username.

## Controller CLI (experiments)

```bat
npm run verify -- --code candidate.py
npm run verify -- --code candidate.py --model <exact-lm-studio-model-id> --task "<original task text>"
```

Without `--spec`, evidence is selected from `evidence/registry.json` by host.
`--model` enables one correction through LM Studio's local API
(`http://127.0.0.1:1234/v1`). Each run saves `report.md`, `audit.json` and, only
on delivery, `delivered.py` in a new folder under `verification-runs/`.
`--policy threshold-only` disables the uncertainty gate for labelled exploratory
sensitivity runs only.

Pipeline over benchmark tasks with a model served by LM Studio (the model sees the
task instruction only; the controller verifies, allows one correction and decides):

```bat
node scripts/run-pipeline.cjs --per-api 2 --model qwen/qwen3.5-9b
node scripts/run-pipeline.cjs --api Petstore --per-api 2 --context base-url
```

`--thinking off` (the default) sends `reasoning_effort: "none"`; `--context base-url`
adds the task's documented base URL to the instruction. Both change what is measured,
so report them. Runs are resumable, and a saved `candidate.py` is reused.

Score a run against the dataset's expected requests (correct/false abstentions and
deliveries; static comparison with the task's test inputs bound, nothing executed):

```bat
node scripts/score-pipeline.cjs verification-runs\pipeline-NAME --out verification-runs\pipeline-NAME\outcomes.md
```

Verifier regression over the benchmark reference solutions and mutants (needs
the dataset from `COMP301-Dataset-Builder`):

```bat
npm run verify:references -- --dataset ..\COMP301-Dataset-Builder\comp301-dataset-builder\output\rest_api_tasks_v1_DRAFT.jsonl --per-api 25 --mutants
```

These are engineering checks of the verifier, not hallucination measurements.

## Migrating from the Beledarian-based `Toolbox`

- **Plugin identity changed** (`beledarian/confidence-agent-toolbox` to
  `comp301-skeptics/confident-agent-toolbox`). LM Studio treats it as a new
  plugin: disable or remove the old one so tools are not listed twice, and set
  the settings again.
- **Tool names and inputs/outputs are unchanged** for every retained tool.
  `resolve_api_spec` now returns a summary instead of the full document (as in
  the latest Toolbox).
- **Settings kept:** `enableConfidenceAgentTools`, `allowPyrightExecution`
  (now on by default). **New:** `pythonExecutable`, `workspacePath`.
  **Removed:** all code-execution, terminal, browser, memory, RAG, Wikipedia,
  sub-agent, plan-mode, language and embedding settings.
- **Removed tools:** `run_python`, `run_javascript`, `run_cpp`, `run_java`,
  shell/terminal commands, file editing and directory tools, web search and
  fetch, browser automation, Git tools, memory, notifications and
  `consult_secondary_agent`.
- **No prompt injection:** the plugin no longer adds startup documentation,
  delegation advice or plan-mode hints to messages.
- **Workspace moved** from `%USERPROFILE%\.beledarians-llm-toolbox\workspace`
  to `%USERPROFILE%\confident-agent-workspace`. No per-plugin state file is kept.
- **Evidence is bundled** in `evidence/snapshots/`; the toolbox no longer needs
  the repository's dataset folder at run time.

## Layout

```
src/                     plugin entry, settings, tools and the verification core
src/python/              claim extractor source (embedded into src/extractorScript.ts at build)
evidence/                registry and bundled snapshots with provenance and licences
instructions/            chat system prompt for demonstrations
examples/, tests/        fixtures and the offline test suite
evaluation/              opt-in behavioural evaluator for the pilot fixtures
scripts/                 build, embed, reference regression, evaluator launcher
docs/reference/          original EWCS documentation and Python reference
SCORING_FIXES.md         why layer scores were 0 and what changed
```

## Limitations

- Supports the documented `requests` subset. Sessions, other HTTP clients,
  classes, async code, `data=json.dumps(...)` bodies and response data passed
  into helper functions are reported as extraction limits and abstain.
- Curated JSONPlaceholder, DummyJSON and REST Countries contracts are partial,
  researcher-authored and tier 2, so those tasks can reach "deliver with flag"
  but not "deliver".
- GitHub and Open-Meteo specifications do not model authentication, so layer 6
  is reported as not applicable there. OAuth2 scopes cannot be checked
  statically; they are reported as a note and only the Bearer placement is checked.
- Open schemas: an undocumented response field is unverifiable, not a contradiction.
- A clean result is evidence about API claims only. It does not establish task
  behaviour or runtime success.
