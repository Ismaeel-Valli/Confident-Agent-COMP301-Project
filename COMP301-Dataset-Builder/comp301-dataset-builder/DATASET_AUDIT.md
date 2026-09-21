# Dataset audit

**Status: DRAFT. Automated integrity checks pass; human review and report-distribution alignment remain open.**

## Actual API composition

| API | Target | Generated | Operation families |
|---|---:|---:|---:|
| JSONPlaceholder | 150 | 150 | 36 |
| GitHub | 250 | 250 | 65 |
| Open-Meteo | 150 | 150 | 3 |
| DummyJSON | 150 | 150 | 23 |
| REST Countries | 150 | 150 | 4 |
| Petstore | 150 | 150 | 11 |

The 1,000 tasks include related variants of the same operations. Changing only an ID or rewording a prompt does not create a new generated scenario. Some scenarios vary only the requested response field; those remain in the same operation family.

## Differences from Progress Report 2

| Measure | Report target (approx.) | Actual draft |
|---|---:|---:|
| GET total (list/single/search) | 600 | 538 |
| POST | 150 | 233 |
| PUT/PATCH | 150 | 199 |
| DELETE | 100 | 30 |
| Easy (heuristic) | 400 | 271 |
| Medium (heuristic) | 400 | 726 |
| Hard (heuristic) | 200 | 3 |
| No credential | 550 | 501 |
| API key | 150 | 155 |
| Bearer token | 200 | 250 |
| OAuth2 token | 100 | 94 |

The generator guarantees the six API totals. It does not claim to satisfy the proposed operation, difficulty or authentication balance. GET list/single/search subcategories also need a reviewed classification. Do not relabel tasks just to hit a percentage. Add/select genuinely appropriate operations and scenarios, or document an agreed revision to the report.

Difficulty currently uses an explicit heuristic: easy has at most two selected parameters/body fields and no credential; hard has at least seven; remaining tasks are medium. This is not a measured difficulty estimate. OAuth2 here means use of an already-issued token; there is no OAuth login flow.

## Source and correctness limits

- GitHub, Petstore and Open-Meteo use downloaded provider OpenAPI descriptions. JSONPlaceholder, DummyJSON and REST Countries use clearly marked documentation-derived partial specifications.
- Review the three curated specifications before treating them as answer keys. Example fields do not establish mandatory fields, exhaustive parameter lists or all valid alternatives. Some mutable-field choices are proposals requiring source review.
- REST Countries targets the current documented v5 interface. Petstore targets the OpenAPI 3 service. Do not mix historical API versions into their grading rules.
- A reference request is one valid implementation candidate. Do not require exact Python text or reject an alternative documented route/method that satisfies the task. DummyJSON updates record PUT and PATCH as acceptable alternatives.
- A missing entry in a partial source is insufficient evidence for VERIFIED_INCORRECT. Preserve UNVERIFIABLE where the evidence is incomplete.
- The fixtures describe inputs and expected HTTP requests. Expected outputs describe decoded JSON/optional fields/empty responses; these are not live API payloads. No credentials, endpoint calls from generated code, account state or service responses were evaluated.
- The template AST checker is an authoring integrity tool. It cannot grade arbitrary LLM code. Build the experimental evaluator independently and audit its labels against original sources.

## Before the final experiment

1. Review source curation and all distinct operation families, including prose-only conditions and response fields.
2. Complete the supplied 100-task stratified random review; expand review if systematic errors appear. The CSV is an empty review queue, not a claim of completed review.
3. Resolve the distribution differences above and freeze the dataset, sources, settings and approved labels.
4. Keep development/pilot examples and their related operation families out of a held-out final test. The included pilot deliberately overlaps this draft; it is for development only. The draft has no final train/test split.
5. Generate each initial model answer once and reuse it for the paired baseline/intervention comparison. Give the model the prompt-only record; keep task-specific reference answers out of its context.
6. Report operation-family correlation and consider grouped analysis rather than treating every related variant as independent evidence.
