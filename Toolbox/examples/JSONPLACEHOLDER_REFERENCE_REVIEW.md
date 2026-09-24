# JSONPlaceholder reference review — 24 September 2026

Review method: a coding assistant compared the snapshot with the provider's [guide](https://jsonplaceholder.typicode.com/guide/) and [routes page](https://jsonplaceholder.typicode.com/). This is a reviewed secondary reference, not provider certification or independent group approval. It remains partial and uses evidence tier 2 (factor 0.8).

| Reference statement | Evidence and boundary |
| --- | --- |
| HTTPS origin and GET /posts | Both provider pages show the route. The guide illustrates a JSON array. |
| GET /posts/1 | Both pages show this example route. The guide illustrates one object. Other IDs are outside this snapshot. |
| id, userId, title, body | The single-post example contains these properties. Their illustrated types are encoded, but no field is marked required: examples do not establish universal presence. |
| No required authentication | Public provider examples omit credentials. Explicit `security: []` records this scoped inference. It is not a guarantee about other operations or future service changes. |
| Successful JSON representation | The successful examples are modeled as 200 application/json. Other statuses, content types and error schemas are not inferred. |
| Inputs | Unfiltered GET requests are covered. Although the guide demonstrates filtering, this snapshot does not infer a complete filter type/value contract. Supplied filters remain unresolved. |

Review changes: removed the previous required-field assumptions and the inferred integer-only userId query contract. Added explicit coverage, sources and review method. The properties remain open; undocumented fields are not automatically declared impossible. Optional `.get("title")` is used in the title examples; direct indexing cannot assume the field is present.

The task's empty-response and failure-handling requirements come from the user prompt. Mocked 201/204/302/4xx/5xx cases test those requirements; they do not assert that this service produces those responses on GET /posts.

The snapshot is `jsonplaceholder-posts.openapi.json`. The controller stores its content and SHA-256 in each audit. The archive also hashes it in `BUILD_SHA256.json`. Freeze the reviewed file and its hash before the main experiment; record any later reference revision as a configuration change. Do not use independent behavioral fixtures as API evidence.

## Frozen package evidence

`evidence/requests-pypi-pilot.json` preserves the complete successful PyPI result from the supplied 24 September pilot, including source URL, retrieval time, import name and distribution. It is captured metadata, not a fresh lookup by this repair. Its latest-version field is not the version installed for Pyright (the verification environment remains pinned separately). Use `--package-evidence` to reproduce that evidence condition without another network lookup, or omit the flag when measuring live retrieval. Do not pool those conditions without labeling them.
