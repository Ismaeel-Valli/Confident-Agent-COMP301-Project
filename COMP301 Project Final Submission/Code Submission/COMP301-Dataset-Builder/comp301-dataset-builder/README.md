# COMP301 REST API dataset builder

This package contains a working generator, a checked 10-task pilot and **1,000 draft task records** following the seven top-level fields in Progress Report 2. It also contains a prompt-only export and a 100-task review queue.

**The API counts match the report. The operation, difficulty and authentication proportions do not yet match its targets. Independent human review is pending.** Read `DATASET_AUDIT.md` for the actual counts and remaining work. These are candidate ground-truth records, not a certified final benchmark.

## Start here

1. Extract the ZIP and open `comp301-dataset-builder` in VS Code.
2. Open `pilot/first_task_readable.json`. Read the prompt, API details, reference code and expected request to understand one complete record.
3. Open `DATASET_AUDIT.md`. It explains what was checked and what still needs your group's attention.
4. Open `review/review_100.csv` in Excel or another CSV editor to begin the planned 10% review. The complete selected records are in `review/review_100.jsonl`.
5. To regenerate the files, install the dependencies and run the pipeline as below. The data files are already included, so regeneration is optional.

## Run on Windows

Use Python 3.10 or later; this package was checked with Python 3.12.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_pipeline.py
```

If the `py` launcher is unavailable, use `python` for the first command. On macOS/Linux, use `python3 -m venv .venv`, followed by `.venv/bin/python` for the remaining commands.

Dependency installation needs internet access. **The generator and validator then run offline using the bundled snapshots.** They do not need an LLM, LM Studio, a GPU, paid API access or real credentials. They do not execute generated reference programs or call service endpoints. `requests` is listed because the reference Python code uses it; the builder itself does not send requests.

Running the pipeline regenerates its draft outputs. The source files stay unchanged. The review-pack script refuses to overwrite a CSV containing decisions, reviewer names or notes. Back up edited outputs before regenerating.

## Main files

| File                                     | Purpose                                                                                                                   |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `output/rest_api_tasks_v1_DRAFT.jsonl`   | 1,000 complete records, including candidate reference answers.                                                            |
| `output/rest_api_prompts_v1_DRAFT.jsonl` | The corresponding ID/language/instruction records, with answers removed.                                                  |
| `pilot/rest_api_tasks_pilot.jsonl`       | A 10-task development batch spanning all six APIs.                                                                        |
| `pilot/first_task_readable.json`         | A formatted example for learning the structure.                                                                           |
| `output/validation_report.json`          | Automated results, actual distributions and limitations.                                                                  |
| `output/release_status.json`             | Explicitly records that final release is not ready.                                                                       |
| `review/review_100.csv`                  | A seeded, API-stratified 100-task review queue.                                                                           |
| `review/operation_families.csv`          | Groups related tasks by their underlying operation.                                                                       |
| `sources/`                               | Provider specifications, curated subsets, provenance manifest and source licenses.                                        |
| `build_dataset.py`                       | Builds prompts, contracts, reference code, test expectations and metadata from source rules.                              |
| `validate_dataset.py`                    | Checks source consistency and reads reference requests statically.                                                        |
| `test_validation.py`                     | Regression checks showing that common record/code mistakes are rejected.                                                  |
| `make_review_pack.py`                    | Recreates the review queue and coverage audit.                                                                            |
| `curate_sources.py`                      | Reproduces the three hand-curated specification drafts; use only deliberately, because it overwrites those curated files. |

The pilot folder is a small practice batch of 10 tasks so you can understand and test the workflow before using all 1,000.

It contains:

File Purpose
first_task_readable.json One task formatted clearly so you can understand its seven fields.
rest_api_tasks_pilot.jsonl The 10 complete tasks, including reference answers.
rest_api_prompts_pilot.jsonl Those same tasks with the answers removed, ready to give to the LLM.
validation_report.json Results of the automated dataset checks.
pilot_rejections.json Any candidate tasks rejected during generation, with reasons.

Start with first_task_readable.json. Then try a prompt from the prompt-only file in LM Studio and compare the response with its reference answer.

The output folder contains the full 1,000-task draft dataset and its checking results.

File Purpose
rest_api_tasks_v1_DRAFT.jsonl Master dataset: all seven fields, including reference answers and API specifications.
rest_api_prompts_v1_DRAFT.jsonl Questions for the LLM: only the task ID, language and instruction.
validation_report.json Automated check results and the dataset’s actual composition.
generation_rejections.json Candidate tasks rejected during generation and their reasons.
release_status.json Records what still needs completing before final experimental use.

For your experiment, feed the prompts file to the LLM and use the master file as the answer key for evaluation, once it has been reviewed.

The pilot folder lets you try the process on 10 tasks; output contains the full set.

The pilot helps you catch problems with loading, generating and checking answers before running the full experiment.

The pilot overlaps the full draft and is for development only. A final held-out experiment needs a deliberate split that keeps related operation families together.

## How the automation works

The builder selects documented operations, varies supported optional parameters, request fields and requested response fields, then constructs each record with a checked Python template. Open-Meteo tasks also vary the requested measurements and forecast options. It does not call a model to invent reference answers.

Variants differ by an operation, selected contract features or requested response behavior. Merely changing a resource ID or paraphrasing an instruction does not count as a new scenario. Related variants remain correlated; the family IDs make this visible.

An API specification supplies the rules. The script supplies the IDs, instruction text, reference implementation, test expectations and metadata. Every record preserves your seven top-level fields:

`task_id`, `language`, `natural_language_instruction`, `api_specification`, `ground_truth`, `test_case`, `metadata`.

`test_case.expected_request` gives the exact reference HTTP request for synthetic inputs. `expected_output` describes the expected decoded JSON, optional response field, empty response or HTTP status. When the source does not document a JSON success body, the task asks for the status code instead of assuming a JSON body exists. It is not a captured live API payload or a runtime test result. The nested fields extend the report's illustrative schema; review this representation with your group before freezing the final schema.

## What the checks establish

The checks cover record structure, unique IDs/prompts/scenarios, source hashes, endpoint/method existence, required parameters, request-value schemas, encoding, and agreement between a reference program and its expected request. A restricted AST reader examines the reference template without `eval` or `exec`.

The checks cannot prove that every prose-only API condition has been encoded correctly. The three curated specifications and reference intentions still need independent review. Do not use this template-specific validator as your experimental evaluator: it is unsuitable for arbitrary LLM-generated code, and evaluating the project against its own authoring logic would create circular evidence.

The reference request is an example of correct behavior, not necessarily the only acceptable request. Evaluate semantic API correctness rather than exact code equality. DummyJSON's update tasks explicitly allow both PUT and PATCH. Other valid alternative routes, optional fields and authentication forms should be recorded during review.

## Source provenance

| API             | Basis                                                                                                                                                                                                                                                                                                    |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GitHub          | Provider OpenAPI snapshot from [github/rest-api-description](https://github.com/github/rest-api-description); [official authentication documentation](https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api) supplies the token/header rule. Prompts pin API version 2026-03-10. |
| Petstore        | Provider [OpenAPI 3 JSON](https://petstore3.swagger.io/api/v3/openapi.json).                                                                                                                                                                                                                             |
| Open-Meteo      | Provider forecast, air-quality and marine specifications from [the official OpenAPI directory](https://github.com/open-meteo/open-meteo/tree/main/openapi), converted from YAML to JSON without changing their contract data.                                                                            |
| JSONPlaceholder | A partial specification curated from the [guide](https://jsonplaceholder.typicode.com/guide/) and [resource overview](https://jsonplaceholder.typicode.com/). Selected mutable fields remain proposals for review.                                                                                       |
| DummyJSON       | A partial specification curated from its [official documentation](https://dummyjson.com/docs) for products, users, posts and todos.                                                                                                                                                                      |
| REST Countries  | A partial specification curated from the [current v5 documentation](https://restcountries.com/docs/countries), including its documented API-key authentication. Historical v3.1 endpoints are outside this snapshot.                                                                                     |

Source retrieval was performed on 2026-09-21. Byte hashes of bundled specification files are in `sources/bundled_manifest.json` and in every task. Provider branch URLs can change; the bundled bytes define this draft. Official-source licenses are included. The curated specifications are marked as researcher-authored subsets; missing entries are not proof that an API operation or field is invalid.

## Next action for your group

Begin with the 10-task pilot and review the curated source contracts. Then complete the 100-task sample, correct the dataset and resolve the distribution differences in `DATASET_AUDIT.md`. Only after review should you create a frozen `rest_api_tasks_v1.jsonl` for the final experiment. Keep the current `_DRAFT` suffix until then.
