# Confident Agent Benchmark

Runs the REST-API code-generation dataset against a model served by LM
Studio, in **baseline** and **intervention** configurations, and logs
everything automatically. The model only ever writes code — every folder,
file, and JSONL line is produced by `run_benchmark.py`, not by the model.

## Layout

```
Benchmark/
  instructions/
    Baseline/BASELINE_SYSTEM_PROMPT.md          <- baseline system prompt
    Intervention/CONFIDENCE_AGENT_SYSTEM_PROMPT.md <- intervention system prompt
  dataset/
    rest_api_prompts_pilot.jsonl                <- task_id, language, instruction
  toolbox/
    confident-agent-toolbox/                    <- the verification tool (your upload)
  Baseline_Tests/<MODEL_LABEL>/<TASK_ID>/        <- one folder per baseline run, grouped by model
  Intervention_Tests/<MODEL_LABEL>/<TASK_ID>/    <- one folder per intervention run, grouped by model
  complete_test_baseline.jsonl                   <- created on first run, appended per task
  complete_test_intervention.jsonl               <- created on first run, appended per task
  run_benchmark.py
```

## Exposing the model's API from LM Studio, with a capped context

LM Studio's `/v1/chat/completions` endpoint (what this script calls) does
**not** accept a context-length parameter per request — the context window
(how many tokens the model will hold in memory) is a property of the
*loaded* model, set when you load it. So the 30K cap is set once, at load
time, not per call:

1. **Load the model with a capped context**, either:
   - In the LM Studio GUI's **Developer** tab, select the model, set
     **Context Length** to `30000` before loading, or
   - From the command line, with LM Studio's `lms` CLI:

     ```
     lms load "<model-key-from-lms-ls>" --context-length 30000 --identifier "Qwen-9B-Q8"
     ```

     `lms ls` lists the model keys you have downloaded. `--identifier` is
     optional but useful: it becomes the exact string you pass to
     `run_benchmark.py --model`, so you can give a run a clean, stable
     name (e.g. `Qwen-9B-Q8`) instead of the full file/quant path.

2. **Start the local server** so the API is reachable, either:
   - In the GUI's **Developer** tab, toggle **Status: Running** (it shows
     the base URL, by default `http://127.0.0.1:1234/v1`), or
   - From the command line: `lms server start`

3. Point the benchmark at it with `--api-base` (only needed if you changed
   the port) and `--model` set to whatever `lms ps` / the GUI shows as the
   loaded model's identifier.

The benchmark also keeps its own side of the budget: it estimates the
token size of each system+task prompt and shrinks the per-request
`max_tokens` so the estimated prompt + completion stays under
`--context-limit` (default `30000`, matching the value you loaded the
model with). This is a safety net, not the real enforcement — if you load
the model with a different context length, pass the same number with
`--context-limit` so the two stay in sync. A task whose prompt alone would
already blow the cap is skipped and logged with an error rather than sent.

## One-time setup

1. Python 3.9+ (uses only the standard library — no pip installs needed).
2. Node.js >= 22.13 (the toolbox's engine requirement).
3. Build the toolbox once:

   ```
   cd toolbox/confident-agent-toolbox
   npm install
   npm run build
   ```

   (`run_benchmark.py` will also do this automatically on first
   intervention run if `dist/verificationCli.js` is missing.)

4. The verifier runs Pyright against a Python environment that has
   `requests` installed (see `toolbox/confident-agent-toolbox/requirements-verification.txt`).
   By default it uses whatever `python` resolves to on PATH. Point it at a
   specific virtual environment with:

   ```
   export CONFIDENCE_PYTHON=/path/to/venv/bin/python
   ```

5. Load your model in LM Studio and start the local server (default
   `http://127.0.0.1:1234/v1`).

## Running

```
python run_benchmark.py --mode baseline     --model <exact-lm-studio-model-id> --model-label "Qwen 9B Q8"
python run_benchmark.py --mode intervention --model <exact-lm-studio-model-id> --model-label "Qwen 9B Q8"
python run_benchmark.py --mode both         --model <exact-lm-studio-model-id> --model-label "Qwen 9B Q8"
```

Useful flags:

- `--model-label` — a human-readable name and parameters for this run (e.g.
  `"Qwen 9B Q8"`, `"Llama-3.1-8B-Q4_K_M"`). All of this run's task folders go
  under `Baseline_Tests/<model-label>/` and `Intervention_Tests/<model-label>/`,
  so results from different models/quantizations never mix. Defaults to
  `--model` itself if you don't set it.
- `--api-base URL` — LM Studio endpoint (default `http://127.0.0.1:1234/v1`).
- `--context-limit N` — token budget to plan around (default `30000`); must
  match the context length the model was actually loaded with in LM Studio
  (see the section above).
- `--dataset PATH` — a different task file.
- `--limit N` — only run the first N tasks (smoke-testing).
- `--no-correction` — disable the verifier's one-shot model-side correction
  of a contradicted candidate (by default it is enabled and will make one
  extra call to LM Studio per contradicted candidate, exactly the
  "correct at most once" step in the toolbox's own workflow).
- `--temperature`, `--max-tokens` — generation settings sent to LM Studio.
  `--max-tokens` is a ceiling: the benchmark will shrink it further per task
  to stay under `--context-limit`, never raise it.

Re-running is additive: existing per-task folders are overwritten, and
JSONL lines are always appended, so re-running the same task twice will
produce two lines for it in the JSONL files (delete the JSONL if you want
a clean append log for a fresh full run).

## What each mode does

### Baseline

For each task: sends `BASELINE_SYSTEM_PROMPT.md` + the task instruction to
the model, saves the raw response, extracts the code from the fenced code
block, and logs it. No tool, no verification.

Per task, `Baseline_Tests/<MODEL_LABEL>/<TASK_ID>/` contains:

- `solution.py` — extracted candidate code
- `response.md` — the full raw model reply
- `raw_response.json` — the full LM Studio API response
- `meta.json` — task id, model, instruction, timing, any error

`complete_test_baseline.jsonl` gets one appended line per task:

```json
{"prompt_id": "REST_PY_JP_0001", "model": "qwen2.5-9b-instruct-q8_0", "model_label": "Qwen_9B_Q8", "code": "...", "error": null}
```

### Intervention

For each task: sends `CONFIDENCE_AGENT_SYSTEM_PROMPT.md` + the task
instruction to the model to get a candidate, saves it, then invokes the
toolbox's external verification controller
(`toolbox/confident-agent-toolbox/dist/verificationCli.js`) as a
subprocess — this **is** "the tool": it runs the six static verification
layers against frozen API evidence, computes EWCS, and makes the
`deliver` / `deliver_with_flag` / `abstain` decision, exactly as described
in `instructions/CONFIDENCE_AGENT_PROMPT.md` inside the toolbox. If a layer
comes back `verified_incorrect`, the controller itself makes the one
permitted correction call to LM Studio and re-verifies — the model never
decides this; the benchmark does, by calling the controller.

Per task, `Intervention_Tests/<MODEL_LABEL>/<TASK_ID>/` contains:

- `candidate.py` — the model's initial candidate
- `verification/` — the controller's own output directory: `report.md`,
  `audit.json` (full machine-readable record: layers, EWCS, decision,
  every attempt), and `delivered.py` if the decision allowed delivery
- `report.md`, `delivered.py` — convenience copies of the same, at the top
  level of the task folder
- `response.md`, `raw_response.json`, `meta.json` — as in baseline

`complete_test_intervention.jsonl` gets one appended line per task:

```json
{"prompt_id": "REST_PY_JP_0001", "model": "qwen2.5-9b-instruct-q8_0", "model_label": "Qwen_9B_Q8", "code_output": "...", "ewcs": 0.7308, "decision": "deliver_with_flag", "error": null}
```

`code_output` is `null` when the decision was `abstain` (the controller
withholds code on abstention) or when generation/verification failed.

## Next step

A separate **Evaluate Benchmark** pass (comparing the two
`complete_test_*.jsonl` files, e.g. with McNemar's test) is intentionally
not part of this script and will be built next.
