# Confidence Agent Toolbox 2.0.0

Standalone LM Studio plugin. Tools are independently enabled in plugin settings. Disabled tools are not registered.

## Settings

- `Workspace`: working directory for files and generated code.
- `Python executable`: interpreter used by Python, extraction, and Pyright.
- `Embedding model`: LM Studio embedding model used by local and web retrieval.

## Filesystem

### `append_file`

Append content to the end of a file. If the file doesn't exist, it will be created. Useful for adding logs, entries, or building files incrementally.

**Default:** enabled

### `change_directory`

Change the working directory to an existing directory. Relative paths resolve from the current directory. Persists independently in toolbox state.

**Default:** enabled

### `copy_file`

Copy a file to a new location.

**Default:** enabled

### `delete_files_by_pattern`

Delete multiple files in the current directory that match a regex pattern.

**Default:** disabled

### `delete_lines_in_file`

Delete a specific line or range of lines from a file. Line numbers are 1-indexed (line 1 is the first line). If end_line is omitted, only start_line will be deleted.

**Default:** enabled

### `delete_path`

Delete a file or directory in the current working directory. Be careful!

**Default:** disabled

### `find_files`

Find files recursively in the current directory matching a name pattern.

**Default:** enabled

### `fuzzy_find_local_files`

Fuzzy find local files by path/name similarity using Levenshtein scoring.

**Default:** enabled

### `get_file_metadata`

Get metadata (size, dates) for a specific file.

**Default:** enabled

### `insert_at_line`

Insert content at a specific line number in a file. The line_number is 1-indexed (line 1 is the first line). Existing content at that line and below will be pushed down.

**Default:** enabled

### `list_directory`

List the files and directories in the current working directory or a specified subdirectory.

**Default:** enabled

### `make_directory`

Create a new directory in the current working directory.

**Default:** enabled

### `move_file`

Move or rename a file or directory.

**Default:** enabled

### `multi_replace_text`

Replace multiple scattered text blocks in a single file safely. Each replacement must specify start_line, end_line, old_string, and new_string. The old_string must perfectly match what is currently in the file.

**Default:** enabled

### `open_file`

Open a file or URL in the system's default application. Use this to preview images, PDFs, or open web pages.

**Default:** enabled

### `preview_html`

Render and preview HTML content in the system's default browser. Useful for visualizing code or UIs.

**Default:** enabled

### `rag_local_files`

Perform RAG (Retrieval-Augmented Generation) on files in the current workspace. Use this to find code snippets or information within local files relevant to a query.

**Default:** enabled

### `read_document`

Read content from PDF or DOCX files.

**Default:** enabled

### `read_file`

Read the content of a file in the current working directory.

**Default:** enabled

### `read_file_range`

Read a specific range of lines from a file. Returns the content with line numbers for easy reference. Line numbers are 1-indexed (line 1 is the first line).

**Default:** enabled

### `replace_text_in_file`

Replace a specific string in a file with a new string. Useful for making small edits without rewriting the entire file. Ensure 'old_string' matches exactly (including whitespace) or the replace will fail.

**Default:** enabled

### `save_file`

Save content to a specified file in the current working directory. This tool returns the full path to the saved file. You should then output this full path to the user.

**Default:** enabled

### `search_directory`

Search an entire directory for a regex pattern (like grep). Returns matching file paths and line numbers.

**Default:** enabled

### `search_in_file`

Search for a pattern within a single file (grep-like functionality). Returns matching lines with their line numbers. The pattern can be a simple substring or a regex pattern.

**Default:** enabled

## Web

### `browser_open_page`

Open a webpage in a headless browser (Puppeteer), render it once, and return content. One-shot only; do not use for multi-step navigation.

**Default:** disabled

### `browser_session_close`

Close the active persistent browser session.

**Default:** enabled

### `browser_session_control`

Control the active persistent browser session. Supports actions, page reading, screenshot capture, and fuzzy finding in-page text/selectors.

**Default:** disabled

### `browser_session_open`

Open a persistent browser session (single active page), navigate to URL, and return page text for context.

**Default:** disabled

### `fetch_web_content`

Fetch the clean, text-based content of a webpage URL.

**Default:** enabled

### `lookup_documentation`

Search official documentation for a supported API and retrieve result pages with hashes and timestamps. Requires web_search and fetch_web_content. Prose remains unreviewed evidence and never automatically changes a verification score.

**Default:** enabled

### `rag_web_content`

Fetch content from a URL, and then use RAG to find and return only the text chunks most relevant to a specific query.

**Default:** enabled

### `web_search`

Search the web using multiple providers (DuckDuckGo, Google, Bing). Uses no-key, no-Chrome providers first, then browser providers as fallback.

**Default:** enabled

### `wikipedia_search`

Search Wikipedia for a given query and return page summaries.

**Default:** enabled

## Confidence

### `compute_ewcs`

Diagnostic score with canonical weights; missing checks retain weight and an empty applicable set has ewcs:null. Controller results are authoritative.

**Default:** enabled

### `extract_claims`

Static Python extraction for a documented requests subset. Returns complete/limitations, operation-linked claims and a candidate hash. Runtime input values can be bound explicitly.

**Default:** enabled

### `list_api_references`

List bundled OpenAPI references, their identifiers, scope and evidence provenance. This supplied source includes jsonplaceholder-posts.

**Default:** enabled

### `make_decision`

Validate all six contributions. Contradiction requests correction; incomplete/unverifiable critical checks abstain before thresholds 0.85/0.60.

**Default:** enabled

### `present_report`

Format the verification decision and evidence. Withhold code for abstain/correct and reject inconsistent delivery requests.

**Default:** enabled

### `query_pypi`

Query package metadata. exists:null/status:unverifiable means lookup failed, not that the package is nonexistent.

**Default:** enabled

### `resolve_api_spec`

Discover a JSON OpenAPI 3.0 contract and provenance; unresolved discovery returns spec:null. Review and freeze a snapshot for experiments.

**Default:** enabled

### `save_code`

Save the exact candidate to a workspace-relative file. Saving is an internal record, not verified delivery.

**Default:** enabled

### `verify_access_point`

Match server origin/base path, endpoint and HTTP method. Dynamic endpoints and unsupported specs remain unverifiable.

**Default:** enabled

### `verify_candidate`

Run the six API verification layers on the exact candidate, calculate EWCS and return a delivery decision and report. Requires all component tools and Pyright to be enabled. This source verifies API claims, not general task correctness; native calls do not automatically correct code.

**Default:** enabled

### `verify_contextual`

Check operation-level inherited authentication alternatives against actual request arguments. Comments are not authentication.

**Default:** enabled

### `verify_identifier`

Check structured Pyright diagnostics for the exact code. Missing packages/stubs and process failure are unverifiable.

**Default:** enabled

### `verify_input_contract`

Check every request separately: required parameters, locations, supported values and JSON bodies. Unknown values block verification.

**Default:** enabled

### `verify_interface`

Check imports against registry evidence and explicit import/distribution mappings. Missing evidence and registry failures stay unverifiable.

**Default:** enabled

### `verify_output_contract`

Follow response provenance and local references to success schemas. A clean Pyright run never substitutes for JSON response evidence.

**Default:** enabled

## Execution

### `get_system_info`

Report OS, CPU, memory, Node version and active working directory.

**Default:** enabled

### `run_pyright`

Run pinned Pyright static analysis on Python source without executing the candidate. Returns structured diagnostics and exit status.

**Default:** enabled

### `run_python`

Execute Python source in the working directory using the configured interpreter. Returns stdout, stderr and exit status; not sandboxed. Disabled by default.

**Default:** disabled

## Memory

### `delete_memory`

Delete one saved memory entry by its ID.

**Default:** disabled

### `read_memory`

Read saved toolbox memory explicitly. Memory is never automatically injected into prompts.

**Default:** enabled

### `save_memory`

Append a fact to persistent toolbox memory for the configured workspace.

**Default:** enabled

### `search_memory`

Search saved toolbox memory for a case-insensitive text fragment.

**Default:** enabled

## Confidence verification boundary

The confidence tools verify extracted API claims against a supplied or bundled contract and compute EWCS. EWCS is evidence strength, not a probability or guarantee. Documentation lookup returns hashed, review-required evidence; it does not silently alter a verification result. `verify_candidate` requires every confidence step and Pyright to be enabled.
