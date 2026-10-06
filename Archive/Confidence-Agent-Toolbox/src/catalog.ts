/** Single source for tool descriptions and individual toggle defaults. */
export const catalog = {
  "read_document": {
    "group": "Filesystem",
    "description": "Read content from PDF or DOCX files.",
    "defaultEnabled": true
  },
  "save_file": {
    "group": "Filesystem",
    "description": "Save content to a specified file in the current working directory. This tool returns the full path to the saved file. You should then output this full path to the user.",
    "defaultEnabled": true
  },
  "replace_text_in_file": {
    "group": "Filesystem",
    "description": "Replace a specific string in a file with a new string. Useful for making small edits without rewriting the entire file. Ensure 'old_string' matches exactly (including whitespace) or the replace will fail.",
    "defaultEnabled": true
  },
  "multi_replace_text": {
    "group": "Filesystem",
    "description": "Replace multiple scattered text blocks in a single file safely. Each replacement must specify start_line, end_line, old_string, and new_string. The old_string must perfectly match what is currently in the file.",
    "defaultEnabled": true
  },
  "search_directory": {
    "group": "Filesystem",
    "description": "Search an entire directory for a regex pattern (like grep). Returns matching file paths and line numbers.",
    "defaultEnabled": true
  },
  "list_directory": {
    "group": "Filesystem",
    "description": "List the files and directories in the current working directory or a specified subdirectory.",
    "defaultEnabled": true
  },
  "read_file": {
    "group": "Filesystem",
    "description": "Read the content of a file in the current working directory.",
    "defaultEnabled": true
  },
  "make_directory": {
    "group": "Filesystem",
    "description": "Create a new directory in the current working directory.",
    "defaultEnabled": true
  },
  "delete_path": {
    "group": "Filesystem",
    "description": "Delete a file or directory in the current working directory. Be careful!",
    "defaultEnabled": false
  },
  "delete_files_by_pattern": {
    "group": "Filesystem",
    "description": "Delete multiple files in the current directory that match a regex pattern.",
    "defaultEnabled": false
  },
  "move_file": {
    "group": "Filesystem",
    "description": "Move or rename a file or directory.",
    "defaultEnabled": true
  },
  "copy_file": {
    "group": "Filesystem",
    "description": "Copy a file to a new location.",
    "defaultEnabled": true
  },
  "find_files": {
    "group": "Filesystem",
    "description": "Find files recursively in the current directory matching a name pattern.",
    "defaultEnabled": true
  },
  "fuzzy_find_local_files": {
    "group": "Filesystem",
    "description": "Fuzzy find local files by path/name similarity using Levenshtein scoring.",
    "defaultEnabled": true
  },
  "get_file_metadata": {
    "group": "Filesystem",
    "description": "Get metadata (size, dates) for a specific file.",
    "defaultEnabled": true
  },
  "open_file": {
    "group": "Filesystem",
    "description": "Open a file or URL in the system's default application. Use this to preview images, PDFs, or open web pages.",
    "defaultEnabled": true
  },
  "preview_html": {
    "group": "Filesystem",
    "description": "Render and preview HTML content in the system's default browser. Useful for visualizing code or UIs.",
    "defaultEnabled": true
  },
  "rag_local_files": {
    "group": "Filesystem",
    "description": "Perform RAG (Retrieval-Augmented Generation) on files in the current workspace. Use this to find code snippets or information within local files relevant to a query.",
    "defaultEnabled": true
  },
  "insert_at_line": {
    "group": "Filesystem",
    "description": "Insert content at a specific line number in a file. The line_number is 1-indexed (line 1 is the first line). Existing content at that line and below will be pushed down.",
    "defaultEnabled": true
  },
  "append_file": {
    "group": "Filesystem",
    "description": "Append content to the end of a file. If the file doesn't exist, it will be created. Useful for adding logs, entries, or building files incrementally.",
    "defaultEnabled": true
  },
  "read_file_range": {
    "group": "Filesystem",
    "description": "Read a specific range of lines from a file. Returns the content with line numbers for easy reference. Line numbers are 1-indexed (line 1 is the first line).",
    "defaultEnabled": true
  },
  "search_in_file": {
    "group": "Filesystem",
    "description": "Search for a pattern within a single file (grep-like functionality). Returns matching lines with their line numbers. The pattern can be a simple substring or a regex pattern.",
    "defaultEnabled": true
  },
  "delete_lines_in_file": {
    "group": "Filesystem",
    "description": "Delete a specific line or range of lines from a file. Line numbers are 1-indexed (line 1 is the first line). If end_line is omitted, only start_line will be deleted.",
    "defaultEnabled": true
  },
  "web_search": {
    "group": "Web",
    "description": "Search the web using multiple providers (DuckDuckGo, Google, Bing). Uses no-key, no-Chrome providers first, then browser providers as fallback.",
    "defaultEnabled": true
  },
  "fetch_web_content": {
    "group": "Web",
    "description": "Fetch the clean, text-based content of a webpage URL.",
    "defaultEnabled": true
  },
  "rag_web_content": {
    "group": "Web",
    "description": "Fetch content from a URL, and then use RAG to find and return only the text chunks most relevant to a specific query.",
    "defaultEnabled": true
  },
  "wikipedia_search": {
    "group": "Web",
    "description": "Search Wikipedia for a given query and return page summaries.",
    "defaultEnabled": true
  },
  "browser_session_open": {
    "group": "Web",
    "description": "Open a persistent browser session (single active page), navigate to URL, and return page text for context.",
    "defaultEnabled": false
  },
  "browser_session_control": {
    "group": "Web",
    "description": "Control the active persistent browser session. Supports actions, page reading, screenshot capture, and fuzzy finding in-page text/selectors.",
    "defaultEnabled": false
  },
  "browser_session_close": {
    "group": "Web",
    "description": "Close the active persistent browser session.",
    "defaultEnabled": true
  },
  "browser_open_page": {
    "group": "Web",
    "description": "Open a webpage in a headless browser (Puppeteer), render it once, and return content. One-shot only; do not use for multi-step navigation.",
    "defaultEnabled": false
  },
  "verify_candidate": {
    "group": "Confidence",
    "description": "Run the six API verification layers on the exact candidate, calculate EWCS and return a delivery decision and report. Requires all component tools and Pyright to be enabled. This source verifies API claims, not general task correctness; native calls do not automatically correct code.",
    "defaultEnabled": true
  },
  "resolve_api_spec": {
    "group": "Confidence",
    "description": "Discover a JSON OpenAPI 3.0 contract and provenance; unresolved discovery returns spec:null. Review and freeze a snapshot for experiments.",
    "defaultEnabled": true
  },
  "query_pypi": {
    "group": "Confidence",
    "description": "Query package metadata. exists:null/status:unverifiable means lookup failed, not that the package is nonexistent.",
    "defaultEnabled": true
  },
  "extract_claims": {
    "group": "Confidence",
    "description": "Static Python extraction for a documented requests subset. Returns complete/limitations, operation-linked claims and a candidate hash. Runtime input values can be bound explicitly.",
    "defaultEnabled": true
  },
  "verify_interface": {
    "group": "Confidence",
    "description": "Check imports against registry evidence and explicit import/distribution mappings. Missing evidence and registry failures stay unverifiable.",
    "defaultEnabled": true
  },
  "verify_identifier": {
    "group": "Confidence",
    "description": "Check structured Pyright diagnostics for the exact code. Missing packages/stubs and process failure are unverifiable.",
    "defaultEnabled": true
  },
  "verify_access_point": {
    "group": "Confidence",
    "description": "Match server origin/base path, endpoint and HTTP method. Dynamic endpoints and unsupported specs remain unverifiable.",
    "defaultEnabled": true
  },
  "verify_input_contract": {
    "group": "Confidence",
    "description": "Check every request separately: required parameters, locations, supported values and JSON bodies. Unknown values block verification.",
    "defaultEnabled": true
  },
  "verify_output_contract": {
    "group": "Confidence",
    "description": "Follow response provenance and local references to success schemas. A clean Pyright run never substitutes for JSON response evidence.",
    "defaultEnabled": true
  },
  "verify_contextual": {
    "group": "Confidence",
    "description": "Check operation-level inherited authentication alternatives against actual request arguments. Comments are not authentication.",
    "defaultEnabled": true
  },
  "compute_ewcs": {
    "group": "Confidence",
    "description": "Diagnostic score with canonical weights; missing checks retain weight and an empty applicable set has ewcs:null. Controller results are authoritative.",
    "defaultEnabled": true
  },
  "make_decision": {
    "group": "Confidence",
    "description": "Validate all six contributions. Contradiction requests correction; incomplete/unverifiable critical checks abstain before thresholds 0.85/0.60.",
    "defaultEnabled": true
  },
  "save_code": {
    "group": "Confidence",
    "description": "Save the exact candidate to a workspace-relative file. Saving is an internal record, not verified delivery.",
    "defaultEnabled": true
  },
  "present_report": {
    "group": "Confidence",
    "description": "Format the verification decision and evidence. Withhold code for abstain/correct and reject inconsistent delivery requests.",
    "defaultEnabled": true
  },
  "list_api_references": {
    "group": "Confidence",
    "description": "List bundled OpenAPI references, their identifiers, scope and evidence provenance. This supplied source includes jsonplaceholder-posts.",
    "defaultEnabled": true
  },
  "change_directory": {
    "group": "Filesystem",
    "description": "Change the working directory to an existing directory. Relative paths resolve from the current directory. Persists independently in toolbox state.",
    "defaultEnabled": true
  },
  "get_system_info": {
    "group": "Execution",
    "description": "Report OS, CPU, memory, Node version and active working directory.",
    "defaultEnabled": true
  },
  "run_python": {
    "group": "Execution",
    "description": "Execute Python source in the working directory using the configured interpreter. Returns stdout, stderr and exit status; not sandboxed. Disabled by default.",
    "defaultEnabled": false
  },
  "run_pyright": {
    "group": "Execution",
    "description": "Run pinned Pyright static analysis on Python source without executing the candidate. Returns structured diagnostics and exit status.",
    "defaultEnabled": true
  },
  "save_memory": {
    "group": "Memory",
    "description": "Append a fact to persistent toolbox memory for the configured workspace.",
    "defaultEnabled": true
  },
  "read_memory": {
    "group": "Memory",
    "description": "Read saved toolbox memory explicitly. Memory is never automatically injected into prompts.",
    "defaultEnabled": true
  },
  "search_memory": {
    "group": "Memory",
    "description": "Search saved toolbox memory for a case-insensitive text fragment.",
    "defaultEnabled": true
  },
  "delete_memory": {
    "group": "Memory",
    "description": "Delete one saved memory entry by its ID.",
    "defaultEnabled": false
  },
  "lookup_documentation": {
    "group": "Web",
    "description": "Search official documentation for a supported API and retrieve result pages with hashes and timestamps. Requires web_search and fetch_web_content. Prose remains unreviewed evidence and never automatically changes a verification score.",
    "defaultEnabled": true
  }
} as const;
