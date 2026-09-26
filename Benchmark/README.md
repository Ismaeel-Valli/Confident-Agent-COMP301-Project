# Confident Agent Benchmark

Runs the REST API code-generation dataset against a model served by LM Studio,
once as a **baseline** and once as the **Confident Agent intervention**, and logs
everything. This benchmark only **produces** results; `evaluate_benchmark`
(separate) scores them against the dataset's expected requests.

| Mode | System prompt | Tools | Who decides |
|---|---|---|---|
| baseline | `instructions/Baseline/BASELINE_SYSTEM_PROMPT.md` | none | nothing is decided; the reply is logged |
| intervention | `confident-agent-toolbox/instructions/CONFIDENCE_AGENT_PROMPT.md` | `verify_candidate` from the toolbox, via the API's function calling | the **tool** decides deliver / deliver_with_flag / abstain; the **model** decides whether to call it and whether to correct |

The intervention is the Confident Agent as a package (prompt plus tool, used by the
model), the same setup as an LM Studio chat with the plugin, but automated. The
model controls the workflow, so the benchmark records whether it followed the
prompt (calls, corrections, verbatim report) instead of enforcing it. Results must
be described as model-controlled.

Generated code is never executed. `verify_candidate` analyses it statically
(claim extraction, Pyright, frozen OpenAPI evidence).

## Layout

```
Benchmark/
  run_benchmark.py                  the runner (Python 3.9+, standard library only)
  tool_bridge.cjs                   runs one verify_candidate call with the toolbox
  instructions/Baseline/BASELINE_SYSTEM_PROMPT.md
  dataset/rest_api_prompts_pilot.jsonl   task_id, language, natural_language_instruction
  Baseline_Tests/<model-label>/     one folder per task, plus run_manifest.json and system_prompt.md
  Intervention_Tests/<model-label>/ the same for the intervention
  complete_test_baseline.jsonl      one line per task and model label (rebuilt after every task)
  complete_test_intervention.jsonl
```

The intervention uses the repository's `confident-agent-toolbox` folder directly
(`--toolbox` to point elsewhere), so the benchmark always runs the current
verifier and prompt instead of a copy that can fall behind.

## Setup (Windows, once)

```bat
cd confident-agent-toolbox
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-verification.txt
npm ci
npm run build
```

The benchmark uses `confident-agent-toolbox\.venv` for claim extraction and Pyright
automatically; set `CONFIDENCE_PYTHON` to use another interpreter.

## LM Studio

Load the model with enough context for the intervention (system prompt about 2.6K
tokens, each `verify_candidate` result about 2.5K, a correction doubles that), and
start the server:

```bat
lms load qwen/qwen3.5-9b --context-length 16384 --gpu max --parallel 1
lms server start
```

The benchmark reads the loaded context length from LM Studio and plans every
request under it; it also records the quantization and context in
`run_manifest.json`.

## Running

From the `Benchmark` folder, a full run of the pilot set in both modes:

```bat
python run_benchmark.py --mode both --model qwen/qwen3.5-9b --model-label "Qwen3.5-9B-Q4_K_M"
```

The following are **alternatives, not further steps**. Use a separate `--model-label`
for smoke tests and for each dataset, so results that belong together stay together:

```bat
REM smoke test: first 2 tasks, baseline only
python run_benchmark.py --mode baseline --model qwen/qwen3.5-9b --model-label "smoke" --limit 2
REM one task
python run_benchmark.py --mode intervention --model qwen/qwen3.5-9b --model-label "smoke" --tasks REST_PY_PS_0001
REM the full 1,000-task dataset
python run_benchmark.py --mode both --model qwen/qwen3.5-9b --model-label "Qwen3.5-9B-Q4_K_M-full" --dataset ..\COMP301-Dataset-Builder\comp301-dataset-builder\output\rest_api_prompts_v1_DRAFT.jsonl
```

| Option | Default | Notes |
|---|---|---|
| `--thinking off\|on` | off | `off` sends `reasoning_effort: "none"` (about 9x faster on CPU for Qwen3.5). Keep it the same across compared runs |
| `--temperature`, `--seed` | 0.2, none | recorded |
| `--max-tokens` | 4096 | ceiling per reply, reduced to fit the context |
| `--max-turns` | 4 | model turns per intervention task (the prompt's workflow needs at most 3); then the final reply is requested |
| `--request-timeout`, `--tool-timeout` | 900 s, 300 s | per model request, per verification |
| `--overwrite` | off | redo tasks that already have results |

**Resuming.** A task with `result.json` is skipped, so an interrupted run continues
where it stopped. A model label's folder belongs to one set of settings (model,
prompt, temperature, thinking, seed, max tokens, max turns, benchmark version):
running again with different settings is refused; use a new `--model-label`. Each
`result.json` also records the dataset file it came from.

## Output

### Baseline: `Baseline_Tests/<label>/<task>/`

`response.md` (the reply), `solution.py` (the extracted code block, empty if none),
`raw_response.json`, `result.json`.

`complete_test_baseline.jsonl`:

```json
{"prompt_id": "REST_PY_JP_0001", "model": "qwen/qwen3.5-9b", "model_label": "Qwen3.5-9B-Q4_K_M",
 "code": "...", "has_code_block": true, "finish_reason": "stop", "error": null}
```

### Intervention: `Intervention_Tests/<label>/<task>/`

| File | Content |
|---|---|
| `conversation.json` | every message: system, task, model turns, tool calls and tool results |
| `turns/turn_NN_response.json` | raw LM Studio response per model turn |
| `verified_candidate_N.py`, `verification_N.json` | each candidate the model submitted, and the tool's full result |
| `response.md` | the model's final reply (the report, if it followed the prompt) |
| `result.json` | everything below, plus per-turn usage and the correction details |

`complete_test_intervention.jsonl`:

```json
{"prompt_id": "REST_PY_PS_0001", "model": "qwen/qwen3.5-9b", "model_label": "Qwen3.5-9B-Q4_K_M",
 "decision": "abstain", "ewcs": 0.2786, "code_output": null,
 "first_candidate": "...", "final_candidate": "...", "reply_code": null,
 "final_reply_present": true, "final_reply_prompted": false,
 "verification_calls": 2, "correction_attempted": true, "correction_allowed": true, "correction_count": 1,
 "first_decision": "abstain", "first_has_contradiction": true, "protocol_notes": [], "error": null}
```

| Field | Meaning |
|---|---|
| `decision`, `ewcs` | the tool's result for the **last** candidate the model verified (null if it never verified) |
| `code_output` | that candidate when the decision is deliver or deliver_with_flag, else null |
| `reply_code` | a code block in the model's final reply, if any (what a user would actually see) |
| `final_reply_present` | the model ended with a text reply |
| `final_reply_prompted` | the model reached `--max-turns` without replying and the benchmark asked for the reply (see Design notes) |
| `correction_attempted` | the model submitted different code after its first verification |
| `correction_allowed` | the first verification had a `verified_incorrect` layer, the only case the prompt allows a correction |
| `correction_count` | number of times the submitted code changed |
| `protocol_notes` | deviations from the prompt: never verified, corrected without a contradiction, more than one correction, replied without correcting after a contradiction, verified the same code twice, called another tool, reply differs from the report, reply shows code the tool did not approve, passed arguments other than code |

## Design notes

- **One model, two configurations, same tasks.** Both modes use the same dataset,
  model and sampling settings, so evaluation can compare them task by task (for
  example McNemar's test). Each mode generates its own code: the comparison is the
  plain model against the Confident Agent package, not the verifier on identical
  code. For that, use `confident-agent-toolbox/scripts/run-pipeline.cjs`, where an
  external controller verifies and corrects one candidate.
- **Task text unchanged.** Both modes pass the task instruction as is; it names the
  API but no URL.
- **The intervention supplies current context by design.** The Confidence Agent
  prompt lists the hosts the toolbox holds frozen evidence for (for example
  `petstore3.swagger.io`, `api.restcountries.com`); the baseline prompt does not.
  This is intended: the model's training data predates the current API versions
  (it defaults to `petstore.swagger.io/v2`), and giving the agent current context
  is part of how the intervention reduces hallucinations. Report the intervention
  as prompt plus tool, not as verification alone.
- **Every intervention task ends with a reply.** The model may use all
  `--max-turns` turns (re-verifying, correcting more than allowed); all of it is
  recorded. If it has not replied by then, the benchmark sends one fixed message
  with tool calls disabled (`tool_choice: "none"`): verification is finished, reply
  with the report from the last `verify_candidate` result. The reply is flagged
  `final_reply_prompted`, and whether it matches the report is recorded. The
  tool's decision on the last candidate is what counts, whatever the reply says.
- **Only `verify_candidate` is offered.** The prompt names the debugging tools as
  not part of the workflow; a call to any other tool is answered with an error and
  recorded as a protocol note.
- **The operator note is not sent.** The toolbox prompt starts with a note for
  people setting up LM Studio (blockquote lines). It is removed before sending;
  the exact text sent is saved as `system_prompt.md`.
- **Live PyPI.** The interface layer looks the imports up on PyPI during the run;
  the result is in each `verification_N.json`.
- **Single sample per task.** Run again with another `--seed` and `--model-label`
  to measure run-to-run variation.
