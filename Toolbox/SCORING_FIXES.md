# Why layer scores came back as 0, and what changed (toolbox 1.6.0 / standalone 2.1.0)

The verification core (`verificationTypes`, `verificationPolicy`, `openApiVerifier`,
`extract_claims.py`, `pyrightRunner`, `packageEvidence`, `verificationController`) is
shared, byte for byte, by `Toolbox/` and `Confidence-Agent-Toolbox/src/confidence/`.
That is why removing the Beledarian tools did not change the scores: the problem was
never in the LM Studio integration.

## How it was reproduced

`scripts/verify-reference-solutions.cjs` runs the verifier over the benchmark's own
reference solutions (known-valid code) and over mutated copies (known-invalid code),
with frozen package evidence, the pinned Pyright 1.1.414 and the provider snapshot
selected from the host in the candidate (`evidence/registry.json`).

| Run (2026-09-25, Windows 11, Python 3.12, Pyright 1.1.414) | Mean EWCS | Decisions |
|---|---|---|
| Before: committed code, 150-task stratified sample | 0.007 | 138 abstain, 12 false `correct` (valid REST Countries code "contradicted") |
| After: all 1,000 reference solutions | 0.771 | 888 `deliver_with_flag`, 5 `deliver`, 107 `abstain`, 0 contradictions |
| After OAuth2 scope change (decision 6, 2026-09-26): all 1,000 reference solutions | 0.784 | 888 `deliver_with_flag`, 99 `deliver`, 13 `abstain`, 0 contradictions |
| After: 1,000 invented-path mutants | - | 1,000 `correct` (contradiction detected) |
| After: 1,000 undeclared-method mutants | - | 1,000 `correct` |
| After: 1,000 wrong-host mutants | - | 1,000 `abstain` (no evidence for an unknown host) |

Before the fix, L1 was established in 0 of 150 cases, L2 in 10 and L3 in 0. After the fix,
L1 and L2 are established for all 1,000 references and L3 for 999. The 107 abstentions
are evidence limits: Petstore OAuth2 scopes (94), GitHub request bodies declared with
`oneOf` (12, unsupported for input values) and one ambiguous GitHub path template (1).
Since decision 6 the Petstore scope abstentions are gone; 13 remain (the GitHub `oneOf`
bodies and the ambiguous template).

## Root causes

| # | Cause | Effect on scores | Fix |
|---|---|---|---|
| 1 | Any unsupported construct marked extraction incomplete, and that downgraded **every** layer (and turned not-applicable layers into unverifiable) | One `headers['Accept'] = ...`, `quote(...)`, list comprehension, `json.dumps`, `os.getenv` or call to `main()` zeroed all six layers | Each extraction issue now names the layers it can affect (`affects`); only those are downgraded |
| 2 | Subscript assignment (`headers['X'] = v`, `params['k'] = v`) was unsupported **and the stale value was kept** | Every reference solution was incomplete; REST Countries got a false "credential absent" contradiction because the Authorization header added by subscript was invisible | Container mutation is tracked copy-on-write; a mutation that cannot be followed makes the container unknown, never stale |
| 3 | `from urllib.parse import quote` was classified as an unsupported HTTP client (`urllib.` prefix); `requests.HTTPError(...)` likewise | The pilot example itself became incomplete | Only real HTTP clients (`urllib.request`, `httpx`, `aiohttp`, ...) are flagged; `requests.*` helpers and `urllib.parse` are ordinary calls |
| 4 | A URL containing any runtime value (function parameter, `inputs[...]`) became completely unknown | L3-L6 unverifiable for nearly every task, because tasks take inputs | URLs are kept as templates (`https://host/posts/{...}`) and matched against OpenAPI path templates |
| 5 | Every `if`/`try`/`with` block erased all known values and all response provenance afterwards | Fields read after the standard empty-body guard were silently lost | Branches are joined: equal values survive, differing values become unknown, conflicting response provenance is flagged for L5 only |
| 6 | Pyright ran in **strict** mode, and any error was blocking | Unannotated `def solve(inputs):` made L2 unverifiable in 140/150 cases | Standard mode; attribute/name/call errors are L2 contradictions, argument-type errors only on API lines; other errors are reported as general Python diagnostics, not scored |
| 7 | Runtime input values made the whole input layer unverifiable | L4 = 0 whenever a value came from `inputs` | Names, locations, requiredness and body keys are still checked; an opaque runtime value's content is a noncritical note. Statically typed mismatches (for example `len(x)` sent as a string field) are still contradictions |
| 8 | A documented but optional response field was unverifiable | L5 = 0 for curated specs that list no `required` fields | The field is permitted by the contract (report section 6.7), so it verifies, with a noncritical presence note |
| 9 | Only OpenAPI 3.0 was accepted; relative servers and missing servers were unresolvable; `format` made every schema "unsupported" | Open-Meteo (3.1, no servers) and Petstore (relative `/api/v3`) were unverifiable in L3-L6 | OpenAPI 3.1 type arrays and numeric exclusive bounds, `allOf` and pure `oneOf`/`anyOf` in responses, `format` as an annotation, server variables, and relative servers resolved against a recorded `document_url`. Missing servers come from a cited registry overlay, never from guessing |
| 10 | Standard-library imports used tier 4 | `import json` lowered L1 from 0.8 to 0.5 | The pinned interpreter's `sys.stdlib_module_names` is a directly inspected, versioned inventory: tier 2 |
| 11 | The extractor was passed on the command line | The larger extractor exceeds the Windows 32,767-character limit (`ENAMETOOLONG`) | The script is sent over stdin |
| 12 | Branches were joined per variable, so a dict entry set inside an `if` (an optional query parameter, a conditional header) made the whole dict unknown | Valid code with an optional declared parameter abstained with "query dictionary has unresolved keys"; invented parameters were hidden behind the same message | Dicts are joined key by key; an entry set on some paths only is marked optional (`{$ca:'maybe'}`). Its name and value are checked; a required parameter, required body property or credential that is only sent on some paths stays unverifiable |
| 13 | A function returning different values on different branches (`data['id']` / `data['user']['id']`) was reported as returning "data from different operations" | Layer 5 unverifiable for a common defensive pattern, even when the result is never read further | The ambiguity is reported only where a field is read from such a value (a caller of the helper), which already raised its own issue |

The current code had also removed the uncertainty gate (policy rule 2) from
`makeDecision`, probably to escape the zeros. With the gate removed, a disabled Pyright
or an offline PyPI lookup still produced `deliver_with_flag`, and 14 of the team's own 61
tests failed. The gate is restored as the default (`POLICY_VERSION 2026-09-25.1`).
`--policy threshold-only` on the CLI reproduces the ungated behaviour for labelled
exploratory sensitivity runs only.

## Decisions for the team to confirm

Every item below is written into code and tests and can be reverted in one place:

1. **Runtime input values are noncritical** (`checkValue`, abstract values). Without this
   rule the benchmark design (`solve(inputs)`) forces L4 to zero on almost every task.
2. **Optional documented response fields verify** (`stepInto`). The 1.5.0 behaviour
   (direct subscript on a non-required field is unverifiable) was stricter than the report.
3. **Undeclared headers are noncritical; undeclared query parameters stay unverifiable** (and, since decision 7, undeclared body fields):
   an extra query parameter is a common hallucinated filter.
4. **Standard-library imports are tier 2.**
5. **Policy rule 2 is enforced again.**
6. **OAuth2 scopes are noncritical** (`authCheck`, 2026-09-26). OAuth2 and OpenID
   Connect tokens are checked as `Authorization: Bearer` credentials (a wrong
   scheme or a missing token is still a contradiction). Required scopes are granted
   to the token, not expressed by the code, so they are reported as a note, like
   credential validity. Before this, every Petstore operation requiring
   `petstore_auth` abstained (94 of the 107 reference abstentions).
7. **Undeclared request-body fields are unresolved** (`checkValue`, 2026-09-27). A
   body field the schema does not declare is treated like an undeclared query
   parameter: unverifiable, unless the schema explicitly allows extra properties
   (`additionalProperties: true`, then a note) or forbids them (`false`, then a
   contradiction). Found in benchmark run 1: 8 deliveries sent hallucinated fields
   (for example `name` where the GitHub label API declares `new_name`), and no
   correct delivery depended on an undeclared field. This change was made after
   inspecting run 1 and is disclosed as such in `Benchmark/EVALUATION_PLAN.md`.

## Remaining low scores that are legitimate evidence gaps (not bugs)

- **Tier ceilings.** With curated (tier 2) specifications and Pyright at tier 4, the
  maximum EWCS is about 0.74, so JSONPlaceholder, DummyJSON and REST Countries can reach
  `deliver_with_flag` but never `deliver`. Official specifications without response-field
  or auth claims top out at 0.825. This follows from the researcher-defined weights and
  tiers (report section 7.4) and should be discussed, not patched.
- **GitHub and Open-Meteo do not model authentication in their OpenAPI files**, so L6 is
  reported as not applicable. Report section 6.7 says missing security documentation
  should be unverifiable. Deciding this needs either a cited, reviewed security overlay
  for GitHub or accepting L6 as unverifiable (which, with rule 2, withholds GitHub tasks).
  The code keeps the previous behaviour; this is flagged, not silently changed.
- **Petstore OAuth2 scopes** cannot be established statically. Since decision 6 they
  are reported as a note; the Bearer placement is still checked.
- **Open schemas**: a field not listed in an extensible schema remains unverifiable.
- **Evidence is chosen by the candidate's host**: an invented host has no evidence and is
  withheld (abstain) rather than contradicted.
- **Still unsupported, reported as scoped extraction issues**: `requests.Session`, other
  HTTP clients, classes, async code, `match`, `global`, response data passed into
  user-defined functions, and `data=json.dumps(...)` bodies.

## Running the checks

```bash
npm run build
node scripts/verify-reference-solutions.cjs --per-api 25 --mutants
npm run verify -- --code candidate.py --package-evidence examples/evidence/requests-pypi-pilot.json
```

Without `--spec`, the CLI selects the frozen specification by the candidate's host from
`evidence/registry.json`. Reference solutions and mutants are engineering checks of the
verifier. They are not hallucination measurements and must not be reported as experimental
results.
