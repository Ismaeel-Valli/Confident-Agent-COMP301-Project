# Notices and attribution

## Origin of this code

This toolbox is derived from **Beledarian's LM Studio Toolbox**
(https://github.com/Beledarian/Beledarians_LM_Studio_Toolbox), MIT License,
Copyright (c) 2025 Laurin Feulner. The original copyright and permission notice
are retained in `LICENSE`, as the MIT License requires. The general-purpose
tools, sub-agent framework and branding of that project were removed; the
LM Studio plugin entry structure (`.lmstudio/entry.ts`, build scripts) is retained.

The verification code (claim extraction, the six verification layers, EWCS
scoring, decision policy, Pyright adapter, evidence registry and CLI controller)
was written for the UKZN COMP301 Confident Agent project by The Skeptics, with
assistance from AI coding tools as recorded in the project report.

## Runtime dependencies (npm, not bundled into `.lmstudio/dev.js`)

| Package | Version | Licence |
|---|---|---|
| @lmstudio/sdk | 1.4.0 | Apache-2.0 |
| pyright | 1.1.414 | MIT |
| zod | 3.24.1 | MIT |

## Bundled evidence snapshots (`evidence/snapshots/`)

| File | Source | Licence |
|---|---|---|
| `github.openapi.json` | GitHub REST API description (github/rest-api-description) | MIT, see `github-license.txt` |
| `petstore.openapi.json` | Swagger Petstore OpenAPI 3 | Apache-2.0, see `petstore-license.txt` |
| `openmeteo-*.openapi.json` | Converted from the Open-Meteo repository YAML | AGPL-3.0, see `openmeteo-license.txt` |
| `jsonplaceholder.curated.openapi.json`, `dummyjson.curated.openapi.json`, `restcountries.curated.openapi.json` | Researcher-authored partial contracts derived from provider documentation | Team work; not provider-issued specifications |

Retrieval URLs, dates and SHA-256 hashes are in `evidence/snapshots/manifest.json`
and `evidence/snapshots/bundled_manifest.json`. Keep the licence files with the
snapshots when sharing them.
