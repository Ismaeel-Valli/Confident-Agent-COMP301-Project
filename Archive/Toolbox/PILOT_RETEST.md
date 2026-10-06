# Retest the 0-score pilot — toolbox 1.5.0

The old run combined an outdated prompt, truncated PyPI evidence, an incorrect spec argument, unused-parameter warnings and unsupported response guards. This release fixes the workflow and broadens a bounded part of extraction. It does not change the EWCS weights, tier factors or thresholds.

## 1. Install and reload

Extract this archive and open a Windows Command Prompt in its `Toolbox` folder. If `.venv` already exists here from the earlier installation, reuse it; otherwise create it:

```bat
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-verification.txt
set "CONFIDENCE_PYTHON=%CD%\.venv\Scripts\python.exe"
npm ci
npm run ci
lms dev
```

Stop the previous development process before starting this one. Start a fresh LM Studio chat, enable Confidence Agent and Allow Pyright, and replace the entire old verification prompt with `instructions/CONFIDENCE_AGENT_PROMPT.md`. The `verify_candidate` result should contain `toolbox_version: "1.5.0"`. If it does not, check which installation is loaded.

For the supplied JSONPlaceholder task, the native tool arguments should contain the exact candidate and `reference_id: "jsonplaceholder-posts"`. There is no need to ask Qwen to copy a full spec, PyPI response or six layer results. Native calls still use live PyPI retrieval; network failures may cause abstention. The external controller is the enforced path for the experiment.

## 2. Reproduce the controlled positive case

In another terminal, in Toolbox, set `CONFIDENCE_PYTHON` again, then run:

```bat
npm run verify -- --code examples/jsonplaceholder-solve.py --spec examples/jsonplaceholder-posts.openapi.json --package-evidence examples/evidence/requests-pypi-pilot.json
```

With the pinned environment and recorded evidence, the expected result is **EWCS 0.725, deliver_with_flag**. Interface contributes 2.4, identifier 1.5, access point 3.2 and input contract 1.6: 8.7/12. The function returns the whole decoded JSON, so it has no individual response-field claims; the reference has no authentication requirement. Those two layers are explicitly not applicable.

This is a reproducible development check using frozen package evidence. Omit `--package-evidence ...` for a live retrieval run. Registry or environment failures must remain visible; do not change them to passes.

## 3. Independently check behavior

```bat
npm run evaluate:pilot
```

This executes only two shipped, reviewed development functions, with mocked requests and a blocked fallback HTTP path. It makes no real API request and is never called by the static verifier. It is not a sandbox for arbitrary generated code.

The original pilot function fails five of eleven cases; the corrected reference passes all eleven. The cases cover populated/empty bodies, other success statuses, an empty JSON array, HTTP failures, an unresolved redirect, invalid JSON and a transport timeout. Here, “empty response” means an empty HTTP body; a body containing `[]` returns the decoded empty list. If the benchmark defines that phrase differently, record and apply its contract consistently before evaluation.

The original function can now obtain the same API-claim score as the reference: its endpoint, imports and types do not reveal that it discards decoded posts. **A passing EWCS must never be labeled proof of task correctness.** The independent behavioral results expose this limitation. They are not fed back into EWCS or used to give the model the answer.

## 4. Run paired experiments

Generate and save one baseline using `instructions/BASELINE_GENERATION_PROMPT.md`. Feed that same saved code to `npm run verify -- --code ... --spec ...`. Supply `--model` with the exact LM Studio model ID and `--task` with the original task to permit one correction after a verified contradiction. Keep generation parameters, evidence snapshots and model configuration fixed and recorded.

The controller saves `report.md`, `audit.json`, and (only on delivery) `delivered.py` in a new run directory. Independently adjudicate task behavior and REST API claims; distinguish logic errors, verification limits, tool failures and hallucinations. Count incorrect deliveries and correct candidates withheld. A lower abstention rate alone does not establish better hallucination detection.
