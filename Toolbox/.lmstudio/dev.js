"use strict";
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __esm = (fn, res, err) => function __init() {
  if (err) throw err[0];
  try {
    return fn && (res = (0, fn[__getOwnPropNames(fn)[0]])(fn = 0)), res;
  } catch (e) {
    throw err = [e], e;
  }
};
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));

// src/locales/en.ts
var en;
var init_en = __esm({
  "src/locales/en.ts"() {
    "use strict";
    en = {
      config: {
        messageLanguage: {
          displayName: "Message Language",
          subtitle: "Language used for runtime messages, hints, and prompt injections. Changes take effect immediately without restart."
        },
        uiLanguageOverride: {
          displayName: "UI Language Override (Next Restart)",
          subtitle: "Force the Config UI to a specific locale on the next plugin restart, overriding OS detection. Set to 'auto' to use OS detection. Options: auto, en, zh-CN, zh-TW, de."
        },
        planMode: {
          displayName: "Plan Mode",
          subtitle: "Controls when the model should explore and propose a plan before making changes. Options: 'always', 'when_useful', 'never'."
        },
        retrievalLimit: {
          displayName: "Retrieval Limit",
          subtitle: "When retrieval is triggered, this is the maximum number of chunks to return."
        },
        retrievalAffinityThreshold: {
          displayName: "Retrieval Affinity Threshold",
          subtitle: "The minimum similarity score for a chunk to be considered relevant."
        },
        allowJavascriptExecution: {
          displayName: "Allow JavaScript Execution",
          subtitle: "Enable the 'run_javascript' tool. DANGER: Code runs on your machine."
        },
        allowPythonExecution: {
          displayName: "Allow Python Execution",
          subtitle: "Enable the 'run_python' tool. DANGER: Code runs on your machine."
        },
        allowCppExecution: {
          displayName: "Allow C++ Execution",
          subtitle: "Enable the 'run_cpp' tool. Requires g++. DANGER: Code runs on your machine."
        },
        allowJavaExecution: {
          displayName: "Allow Java Execution",
          subtitle: "Enable the 'run_java' tool. Requires a JDK (javac/java). DANGER: Code runs on your machine."
        },
        allowPyrightExecution: {
          displayName: "Allow Pyright Type-Checking",
          subtitle: "Enable the 'run_pyright' tool. Requires pyright installed and on PATH. Static analysis only \u2014 it does not execute your code."
        },
        allowTerminalExecution: {
          displayName: "Allow Terminal Execution",
          subtitle: "Enable the 'run_in_terminal' tool. Opens real terminal windows."
        },
        allowShellCommandExecution: {
          displayName: "Allow Shell Command Execution",
          subtitle: "Enable the 'execute_command' tool. DANGER: Commands run on your machine."
        },
        allowBrowserControl: {
          displayName: "Allow Browser Control",
          subtitle: "Enable browser automation tools ('browser_open_page' and browser session tools). DANGER: Automated browsing/actions run on your machine."
        },
        allowGitOperations: {
          displayName: "Allow Git Operations",
          subtitle: "Enable native git tools (status, diff, show, commit, log, add, checkout, push)."
        },
        allowGitHubTools: {
          displayName: "Allow GitHub CLI Tools",
          subtitle: "Enable native GitHub CLI tools. Requires 'gh' installed."
        },
        allowDatabaseInspection: {
          displayName: "Allow Database Inspection",
          subtitle: "Enable 'query_database' for SQLite files."
        },
        allowSystemNotifications: {
          displayName: "Allow System Notifications",
          subtitle: "Enable the agent to send OS notifications."
        },
        allowAllCode: {
          displayName: "Allow All Code Execution",
          subtitle: "MASTER SWITCH: Overrides all other settings to enable ALL execution tools."
        },
        protectedPaths: {
          displayName: "Protected Paths",
          subtitle: "List of drives or paths to block all file/shell operations on (e.g. D:\\, C:\\Windows). One per line. Shell commands cannot be fully blocked by path matching \u2014 use this as a safeguard, not a security boundary."
        },
        searchApiKey: {
          displayName: "Search API Key",
          subtitle: "Optional API key for search services (if supported) to avoid rate limits."
        },
        embeddingModel: {
          displayName: "Embedding Model",
          subtitle: "Model to use for RAG features (default: nomic-ai/nomic-embed-text-v1.5-GGUF)"
        },
        defaultWorkspacePath: {
          displayName: "Default Workspace Path",
          subtitle: "Optional startup workspace path. Leave empty to use the built-in default workspace directory."
        },
        enableMemory: {
          displayName: "Enable Memory",
          subtitle: "If enabled, the model can save and recall information from a 'memory.md' file in the workspace."
        },
        enableWikipediaTool: {
          displayName: "Enable Wikipedia Tool",
          subtitle: "Enable the 'wikipedia_search' tool."
        },
        enableLocalRag: {
          displayName: "Enable Local RAG",
          subtitle: "Enable the 'rag_local_files' tool for searching workspace files."
        },
        enableConfidenceAgentTools: {
          displayName: "Enable Confidence Agent Tool box",
          subtitle: "Enable the API-code verification pipeline (resolve_api_spec, query_pypi, extract_claims, the six verify_* layer tools, compute_ewcs, make_decision, present_report, save_code)."
        },
        enableSecondaryAgent: {
          displayName: "Enable Secondary Agent/Model",
          subtitle: "Allow the main model to delegate tasks to a secondary model (e.g., for summarization)."
        },
        useMainModelForSubAgent: {
          displayName: "Use Main Model as Sub-Agent",
          subtitle: "If enabled, the sub-agent loop will use your main LM Studio server (localhost:1234). Ignores 'Endpoint' setting."
        },
        secondaryAgentEndpoint: {
          displayName: "Secondary Agent Endpoint",
          subtitle: "The API endpoint for the secondary model (e.g., 'http://localhost:1234/v1')."
        },
        secondaryModelId: {
          displayName: "Secondary Model ID",
          subtitle: "The ID of the model to use for the secondary agent (must be loaded/available)."
        },
        subAgentProfiles: {
          displayName: "Sub-Agent Profiles (JSON)",
          subtitle: 'Define available sub-agents. Format: {"coder": "You are a coding expert...", ...}'
        },
        subAgentFrequency: {
          displayName: "Sub-Agent Frequency",
          subtitle: "Controls how often the agent is encouraged to delegate. Options: 'always', 'when_useful', 'hard_tasks', 'never'."
        },
        subAgentAllowFileSystem: {
          displayName: "Sub-Agent: Allow File System",
          subtitle: "If enabled, sub-agents can read/list files."
        },
        subAgentAllowWeb: {
          displayName: "Sub-Agent: Allow Web Search",
          subtitle: "If enabled, sub-agents can use Wikipedia and DuckDuckGo."
        },
        subAgentAllowCode: {
          displayName: "Sub-Agent: Allow Code Execution",
          subtitle: "If enabled, sub-agents can run Python/JS code. DANGER!"
        },
        subAgentAllowBrowserControl: {
          displayName: "Sub-Agent: Allow Browser Control",
          subtitle: "If enabled, sub-agents can use browser automation tools (requires global 'Allow Browser Control' and 'Sub-Agent: Allow Web Search')."
        },
        subAgentTimeLimit: {
          displayName: "Sub-Agent Time Limit (seconds)",
          subtitle: "Maximum time allowed for sub-agent tasks before forced termination. Default: 600s (10 mins)."
        },
        enableDebugMode: {
          displayName: "Enable Auto-Debug Mode",
          subtitle: "If enabled, coding tasks delegated to sub-agents will automatically trigger a second 'Reviewer' pass to check for errors."
        },
        enableSubAgentDebugLogging: {
          displayName: "Enable Sub-Agent Debug Logging",
          subtitle: "If enabled, logs sub-agent tool-call parsing details to the console for troubleshooting."
        },
        subAgentAutoSave: {
          displayName: "Sub-Agent: Auto-Save Code",
          subtitle: "If enabled, code blocks generated by the sub-agent that aren't explicitly saved will be automatically saved to files."
        },
        showFullCodeOutput: {
          displayName: "Show Full Code Output",
          subtitle: "If enabled, the Main Agent will display the full code content of generated files instead of just the file paths."
        },
        simpleSystemPrompt: {
          displayName: "Simplified System Prompt",
          subtitle: "Use a condensed system prompt to reduce latency for CPU-only workflows. Warning: May reduce tool-use accuracy with some models."
        }
      },
      runtime: {
        statusLoadingEmbeddingModel: "Loading an embedding model for retrieval...",
        statusRetrievingCitations: "Retrieving relevant citations for user query...",
        statusRetrievedCitations: (count) => `Retrieved ${count} relevant citations for user query`,
        statusNoRelevantCitations: "No relevant citations found for user query",
        statusDecidingStrategy: "Deciding how to handle the document(s)...",
        statusLoadingParser: (fileName) => `Loading parser for ${fileName}...`,
        statusStrategyChosen: (strategy, detail) => `Chosen context injection strategy: '${strategy}'. ${detail}`,
        citationPrefix: "The following citations were found in the files provided by the user:\n\n",
        citationEntry: (num, text3) => `Citation ${num}: "${text3}"

`,
        citationSuffix: (userQuery) => `Use the citations above to respond to the user query, only if they are relevant. Otherwise, respond to the best of your ability without them.

User Query:

${userQuery}`,
        noRelevantCitationsNote: "Important: No citations were found in the user files for the user query. In less than one sentence, inform the user of this. Then respond to the query to the best of your ability.",
        documentInjectionHeader: "This is a Enriched Context Generation scenario.\n\nThe following content was found in the files provided by the user.\n",
        documentInjectionFileBlock: (fileName, content) => `

** ${fileName} full content **

${content}

** end of ${fileName} **

`,
        documentInjectionSuffix: (userQuery) => `Based on the content above, please provide a response to the user query.

User query: ${userQuery}`,
        delegationHintAlways: "\n\n**SYSTEM MANDATE:** You MUST delegate ALL information retrieval, news summaries, and **ALL coding tasks** (creation, editing, refactoring) to the secondary agent. Do NOT write code or use search tools yourself. Use `consult_secondary_agent` with `allow_tools: true`.\n\n**PRE-DELEGATION CHECKLIST:**\n1. Run `list_directory` to see what files already exist.\n2. Read `beledarian_info.md` or `README.md` if present.\n3. CALL `consult_secondary_agent` with the context.",
        delegationHintWhenUseful: "\n\n**SYSTEM ADVICE:** For complex tasks (e.g., 'create an app', 'refactor this module', 'research and summarize'), you **MUST** delegate to the secondary agent using `consult_secondary_agent` (set `allow_tools: true`).\n\n**Why Delegate?**\n- The Sub-Agent has a specialized loop for coding and debugging.\n- It will automatically SAVE all files. You do not need to do it.\n\n**How to Delegate:**\n1. Gather context (`list_directory`, `read_file`).\n2. Call `consult_secondary_agent` with a clear task description and the context you found.\n",
        delegationHintWhenUsefulDebug: "Note: 'Auto-Debug' is ACTIVE. The Sub-Agent will verify and fix its own code. This is the safest way to generate code.\n",
        delegationHintHardTasks: "\n\n**Delegation Hint:** Only delegate EXTREMELY complex or computationally expensive tasks to the secondary agent. Handle standard queries and file reads yourself.\n",
        planHintAlways: "\n\n**PLAN MODE [ACTIVE]:** Before making ANY file changes or implementing features, you MUST:\n1. **EXPLORE:** Use `list_directory`, `read_file`, and other exploration tools to understand the codebase structure.\n2. **PROPOSE:** Present a clear, step-by-step plan outlining what you will do and why.\n3. **WAIT:** Do NOT start implementing until the user approves your plan or gives explicit permission to proceed.\n\n**Exception:** Simple conversations, clarifications, or trivial single-line edits do not require planning.",
        planHintWhenUseful: "\n\n**PLAN MODE [When Useful]:** For larger, complex, or ambiguous requests:\n1. **EXPLORE FIRST:** Use `list_directory`, `read_file` to understand the codebase before making changes.\n2. **PROPOSE A PLAN:** Outline your approach and key steps before implementing.\n3. **SKIP FOR SIMPLE TASKS:** Normal conversations or small edits (e.g., typo fixes, single function changes) do not require planning."
      }
    };
  }
});

// src/locales/zh-CN.ts
var zhCN;
var init_zh_CN = __esm({
  "src/locales/zh-CN.ts"() {
    "use strict";
    zhCN = {
      config: {
        messageLanguage: {
          displayName: "\u6D88\u606F\u8BED\u8A00",
          subtitle: "\u8FD0\u884C\u65F6\u6D88\u606F\u3001\u63D0\u793A\u548C\u63D0\u793A\u8BCD\u6CE8\u5165\u6240\u4F7F\u7528\u7684\u8BED\u8A00\u3002\u66F4\u6539\u7ACB\u5373\u751F\u6548\uFF0C\u65E0\u9700\u91CD\u542F\u63D2\u4EF6\u3002"
        },
        uiLanguageOverride: {
          displayName: "\u754C\u9762\u8BED\u8A00\uFF08\u91CD\u542F\u540E\u751F\u6548\uFF09",
          subtitle: "\u5728\u4E0B\u6B21\u63D2\u4EF6\u91CD\u542F\u65F6\u5F3A\u5236\u4F7F\u7528\u6307\u5B9A\u8BED\u8A00\uFF0C\u8986\u76D6\u7CFB\u7EDF\u8BED\u8A00\u68C0\u6D4B\u3002\u8BBE\u4E3A 'auto' \u5219\u8DDF\u968F\u64CD\u4F5C\u7CFB\u7EDF\u8BED\u8A00\u3002\u9009\u9879\uFF1Aauto\u3001en\u3001zh-CN\u3001zh-TW\u3001de\u3002"
        },
        planMode: {
          displayName: "\u8BA1\u5212\u6A21\u5F0F",
          subtitle: "\u63A7\u5236\u6A21\u578B\u5728\u4FEE\u6539\u4EE3\u7801\u524D\u662F\u5426\u5148\u63A2\u7D22\u9879\u76EE\u7ED3\u6784\u5E76\u63D0\u51FA\u8BA1\u5212\u3002\u9009\u9879\uFF1A'always'\u3001'when_useful'\u3001'never'\u3002"
        },
        retrievalLimit: {
          displayName: "\u68C0\u7D22\u6570\u91CF\u4E0A\u9650",
          subtitle: "\u89E6\u53D1\u68C0\u7D22\u65F6\uFF0C\u6700\u591A\u8FD4\u56DE\u7684\u6587\u672C\u5757\u6570\u91CF\u3002"
        },
        retrievalAffinityThreshold: {
          displayName: "\u68C0\u7D22\u76F8\u4F3C\u5EA6\u9608\u503C",
          subtitle: "\u6587\u672C\u5757\u88AB\u89C6\u4E3A\u76F8\u5173\u7684\u6700\u4F4E\u76F8\u4F3C\u5EA6\u5206\u6570\u3002\u4E2D\u6587\u5185\u5BB9\u5EFA\u8BAE\u8C03\u4F4E\u81F3 0.35\u20130.45\u3002"
        },
        allowJavascriptExecution: {
          displayName: "\u5141\u8BB8\u6267\u884C JavaScript",
          subtitle: "\u542F\u7528 'run_javascript' \u5DE5\u5177\u3002\u26A0\uFE0F \u5371\u9669\uFF1A\u4EE3\u7801\u5C06\u5728\u60A8\u7684\u8BA1\u7B97\u673A\u4E0A\u8FD0\u884C\u3002"
        },
        allowPythonExecution: {
          displayName: "\u5141\u8BB8\u6267\u884C Python",
          subtitle: "\u542F\u7528 'run_python' \u5DE5\u5177\u3002\u26A0\uFE0F \u5371\u9669\uFF1A\u4EE3\u7801\u5C06\u5728\u60A8\u7684\u8BA1\u7B97\u673A\u4E0A\u8FD0\u884C\u3002"
        },
        allowCppExecution: {
          displayName: "\u5141\u8BB8\u6267\u884C C++",
          subtitle: "\u542F\u7528 'run_cpp' \u5DE5\u5177\uFF0C\u9700\u8981 g++\u3002\u26A0\uFE0F \u5371\u9669\uFF1A\u4EE3\u7801\u5C06\u5728\u60A8\u7684\u8BA1\u7B97\u673A\u4E0A\u8FD0\u884C\u3002"
        },
        allowJavaExecution: {
          displayName: "\u5141\u8BB8\u6267\u884C Java",
          subtitle: "\u542F\u7528 'run_java' \u5DE5\u5177\uFF0C\u9700\u8981 JDK\uFF08javac/java\uFF09\u3002\u26A0\uFE0F \u5371\u9669\uFF1A\u4EE3\u7801\u5C06\u5728\u60A8\u7684\u8BA1\u7B97\u673A\u4E0A\u8FD0\u884C\u3002"
        },
        allowPyrightExecution: {
          displayName: "\u5141\u8BB8 Pyright \u7C7B\u578B\u68C0\u67E5",
          subtitle: "\u542F\u7528 'run_pyright' \u5DE5\u5177\uFF0C\u9700\u8981\u5DF2\u5B89\u88C5\u5E76\u52A0\u5165 PATH \u7684 pyright\u3002\u4EC5\u9759\u6001\u5206\u6790\u2014\u4E0D\u4F1A\u6267\u884C\u60A8\u7684\u4EE3\u7801\u3002"
        },
        allowTerminalExecution: {
          displayName: "\u5141\u8BB8\u7EC8\u7AEF\u6267\u884C",
          subtitle: "\u542F\u7528 'run_in_terminal' \u5DE5\u5177\u3002\u5C06\u6253\u5F00\u771F\u5B9E\u7684\u7EC8\u7AEF\u7A97\u53E3\u3002"
        },
        allowShellCommandExecution: {
          displayName: "\u5141\u8BB8\u6267\u884C Shell \u547D\u4EE4",
          subtitle: "\u542F\u7528 'execute_command' \u5DE5\u5177\u3002\u26A0\uFE0F \u5371\u9669\uFF1A\u547D\u4EE4\u5C06\u5728\u60A8\u7684\u8BA1\u7B97\u673A\u4E0A\u8FD0\u884C\u3002"
        },
        allowBrowserControl: {
          displayName: "\u5141\u8BB8\u6D4F\u89C8\u5668\u63A7\u5236",
          subtitle: "\u542F\u7528\u6D4F\u89C8\u5668\u81EA\u52A8\u5316\u5DE5\u5177\uFF08'browser_open_page' \u53CA\u6D4F\u89C8\u5668\u4F1A\u8BDD\u5DE5\u5177\uFF09\u3002\u26A0\uFE0F \u5371\u9669\uFF1A\u81EA\u52A8\u5316\u64CD\u4F5C\u5C06\u5728\u60A8\u7684\u8BA1\u7B97\u673A\u4E0A\u8FD0\u884C\u3002"
        },
        allowGitOperations: {
          displayName: "\u5141\u8BB8 Git \u64CD\u4F5C",
          subtitle: "\u542F\u7528\u539F\u751F Git \u5DE5\u5177\uFF08status\u3001diff\u3001show\u3001commit\u3001log\u3001add\u3001checkout\u3001push\uFF09\u3002"
        },
        allowGitHubTools: {
          displayName: "\u5141\u8BB8 GitHub CLI \u5DE5\u5177",
          subtitle: "\u542F\u7528\u539F\u751F GitHub CLI \u5DE5\u5177\uFF08gh_auth\u3001gh_create_issue\u3001gh_create_pr \u7B49\uFF09\u3002\u9700\u5B89\u88C5 'gh' \u547D\u4EE4\u884C\u5DE5\u5177\u3002"
        },
        allowDatabaseInspection: {
          displayName: "\u5141\u8BB8\u6570\u636E\u5E93\u68C0\u67E5",
          subtitle: "\u542F\u7528 'query_database' \u4EE5\u67E5\u8BE2 SQLite \u6587\u4EF6\u3002"
        },
        allowSystemNotifications: {
          displayName: "\u5141\u8BB8\u7CFB\u7EDF\u901A\u77E5",
          subtitle: "\u5141\u8BB8\u667A\u80FD\u4F53\u53D1\u9001\u64CD\u4F5C\u7CFB\u7EDF\u684C\u9762\u901A\u77E5\u3002"
        },
        allowAllCode: {
          displayName: "\u5141\u8BB8\u6240\u6709\u4EE3\u7801\u6267\u884C",
          subtitle: "\u{1F534} \u4E3B\u5F00\u5173\uFF1A\u8986\u76D6\u4E0A\u8FF0\u5404\u9879\u8BBE\u7F6E\uFF0C\u4E00\u952E\u542F\u7528\u6240\u6709\u4EE3\u7801/\u547D\u4EE4\u6267\u884C\u5DE5\u5177\u3002"
        },
        protectedPaths: {
          displayName: "\u53D7\u4FDD\u62A4\u8DEF\u5F84",
          subtitle: "\u8981\u7981\u6B62\u6240\u6709\u64CD\u4F5C\u7684\u76D8\u7B26\u6216\u8DEF\u5F84\u5217\u8868\uFF08\u4F8B\u5982 D:\\\u3001C:\\Windows\uFF09\u3002\u6BCF\u884C\u4E00\u4E2A\u3002\u26A0\uFE0F Shell \u547D\u4EE4\u65E0\u6CD5\u901A\u8FC7\u8DEF\u5F84\u5339\u914D\u5B8C\u5168\u62E6\u622A\u2014\u2014\u6B64\u529F\u80FD\u4F5C\u4E3A\u9632\u62A4\u5C4F\u969C\u4F7F\u7528\uFF0C\u800C\u975E\u5B89\u5168\u8FB9\u754C\u3002"
        },
        searchApiKey: {
          displayName: "\u641C\u7D22 API \u5BC6\u94A5",
          subtitle: "\u641C\u7D22\u670D\u52A1\u7684\u53EF\u9009 API \u5BC6\u94A5\uFF08\u5982\u652F\u6301\uFF09\uFF0C\u53EF\u907F\u514D\u901F\u7387\u9650\u5236\u3002"
        },
        embeddingModel: {
          displayName: "\u5D4C\u5165\u6A21\u578B",
          subtitle: "\u7528\u4E8E RAG \u529F\u80FD\u7684\u6A21\u578B\uFF08\u9ED8\u8BA4\uFF1Anomic-ai/nomic-embed-text-v1.5-GGUF\uFF09\u3002\u4E2D\u6587\u5185\u5BB9\u63A8\u8350\u4F7F\u7528 BAAI/bge-m3-gguf\u3002"
        },
        defaultWorkspacePath: {
          displayName: "\u9ED8\u8BA4\u5DE5\u4F5C\u533A\u8DEF\u5F84",
          subtitle: "\u53EF\u9009\u7684\u542F\u52A8\u5DE5\u4F5C\u533A\u8DEF\u5F84\u3002\u7559\u7A7A\u5219\u4F7F\u7528\u7CFB\u7EDF\u5185\u7F6E\u9ED8\u8BA4\u76EE\u5F55\u3002"
        },
        enableMemory: {
          displayName: "\u542F\u7528\u8BB0\u5FC6\u529F\u80FD",
          subtitle: "\u542F\u7528\u540E\uFF0C\u6A21\u578B\u53EF\u4ECE\u5DE5\u4F5C\u533A\u7684 'memory.md' \u6587\u4EF6\u4E2D\u4FDD\u5B58\u548C\u8BFB\u53D6\u4FE1\u606F\uFF0C\u5B9E\u73B0\u957F\u671F\u8BB0\u5FC6\u3002"
        },
        enableWikipediaTool: {
          displayName: "\u542F\u7528\u7EF4\u57FA\u767E\u79D1\u641C\u7D22",
          subtitle: "\u542F\u7528 'wikipedia_search' \u5DE5\u5177\u3002"
        },
        enableLocalRag: {
          displayName: "\u542F\u7528\u672C\u5730 RAG",
          subtitle: "\u542F\u7528 'rag_local_files' \u5DE5\u5177\uFF0C\u53EF\u5728\u5DE5\u4F5C\u533A\u6587\u4EF6\u4E2D\u8FDB\u884C\u8BED\u4E49\u641C\u7D22\u3002"
        },
        enableConfidenceAgentTools: {
          displayName: "\u542F\u7528 Confidence Agent Tool box",
          subtitle: "\u542F\u7528 API \u4EE3\u7801\u9A8C\u8BC1\u6D41\u6C34\u7EBF\uFF08resolve_api_spec\u3001query_pypi\u3001extract_claims\u3001\u516D\u4E2A verify_* \u5206\u5C42\u5DE5\u5177\u3001compute_ewcs\u3001make_decision\u3001present_report\u3001save_code\uFF09\u3002"
        },
        enableSecondaryAgent: {
          displayName: "\u542F\u7528\u8F85\u52A9\u667A\u80FD\u4F53",
          subtitle: "\u5141\u8BB8\u4E3B\u6A21\u578B\u5C06\u590D\u6742\u4EFB\u52A1\u59D4\u6258\u7ED9\u8F85\u52A9\u6A21\u578B\u5904\u7406\uFF08\u4F8B\u5982\u4EE3\u7801\u7F16\u5199\u3001\u6458\u8981\u603B\u7ED3\u7B49\uFF09\u3002"
        },
        useMainModelForSubAgent: {
          displayName: "\u7528\u4E3B\u6A21\u578B\u4F5C\u4E3A\u5B50\u667A\u80FD\u4F53",
          subtitle: "\u542F\u7528\u540E\uFF0C\u5B50\u667A\u80FD\u4F53\u5C06\u76F4\u63A5\u4F7F\u7528 LM Studio \u5F53\u524D\u52A0\u8F7D\u7684\u4E3B\u6A21\u578B\uFF08localhost:1234\uFF09\uFF0C\u5FFD\u7565\u4E0B\u65B9\u7684\u201C\u7AEF\u70B9\u201D\u548C\u201C\u6A21\u578B ID\u201D\u8BBE\u7F6E\u3002"
        },
        secondaryAgentEndpoint: {
          displayName: "\u8F85\u52A9\u667A\u80FD\u4F53 API \u7AEF\u70B9",
          subtitle: "\u8F85\u52A9\u6A21\u578B\u7684 API \u5730\u5740\uFF08\u4F8B\u5982 'http://localhost:1234/v1'\uFF09\u3002"
        },
        secondaryModelId: {
          displayName: "\u8F85\u52A9\u6A21\u578B ID",
          subtitle: "\u7528\u4E8E\u8F85\u52A9\u667A\u80FD\u4F53\u7684\u6A21\u578B\u6807\u8BC6\u7B26\uFF08\u987B\u5DF2\u52A0\u8F7D/\u53EF\u7528\uFF09\u3002"
        },
        subAgentProfiles: {
          displayName: "\u5B50\u667A\u80FD\u4F53\u914D\u7F6E\u6587\u4EF6\uFF08JSON\uFF09",
          subtitle: '\u5B9A\u4E49\u53EF\u7528\u7684\u5B50\u667A\u80FD\u4F53\u89D2\u8272\u3002\u683C\u5F0F\uFF1A{"coder": "\u4F60\u662F\u4E00\u4F4D\u7F16\u7A0B\u4E13\u5BB6...", ...}'
        },
        subAgentFrequency: {
          displayName: "\u5B50\u667A\u80FD\u4F53\u8C03\u7528\u9891\u7387",
          subtitle: "\u63A7\u5236\u6A21\u578B\u5728\u4EC0\u4E48\u60C5\u51B5\u4E0B\u5EFA\u8BAE\u59D4\u6258\u4EFB\u52A1\u7ED9\u5B50\u667A\u80FD\u4F53\u3002\u9009\u9879\uFF1A'always'\uFF08\u59CB\u7EC8\uFF09\u3001'when_useful'\uFF08\u9700\u8981\u65F6\uFF09\u3001'hard_tasks'\uFF08\u4EC5\u590D\u6742\u4EFB\u52A1\uFF09\u3001'never'\uFF08\u4ECE\u4E0D\uFF09\u3002"
        },
        subAgentAllowFileSystem: {
          displayName: "\u5B50\u667A\u80FD\u4F53\uFF1A\u5141\u8BB8\u6587\u4EF6\u7CFB\u7EDF",
          subtitle: "\u542F\u7528\u540E\uFF0C\u5B50\u667A\u80FD\u4F53\u53EF\u4EE5\u8BFB\u53D6\u548C\u5217\u51FA\u5DE5\u4F5C\u533A\u6587\u4EF6\u3002"
        },
        subAgentAllowWeb: {
          displayName: "\u5B50\u667A\u80FD\u4F53\uFF1A\u5141\u8BB8\u7F51\u7EDC\u641C\u7D22",
          subtitle: "\u542F\u7528\u540E\uFF0C\u5B50\u667A\u80FD\u4F53\u53EF\u4EE5\u4F7F\u7528\u7EF4\u57FA\u767E\u79D1\u548C DuckDuckGo\u3002"
        },
        subAgentAllowCode: {
          displayName: "\u5B50\u667A\u80FD\u4F53\uFF1A\u5141\u8BB8\u4EE3\u7801\u6267\u884C",
          subtitle: "\u542F\u7528\u540E\uFF0C\u5B50\u667A\u80FD\u4F53\u53EF\u4EE5\u8FD0\u884C Python/JS \u4EE3\u7801\u3002\u26A0\uFE0F \u5371\u9669\uFF01"
        },
        subAgentAllowBrowserControl: {
          displayName: "\u5B50\u667A\u80FD\u4F53\uFF1A\u5141\u8BB8\u6D4F\u89C8\u5668\u63A7\u5236",
          subtitle: "\u542F\u7528\u540E\uFF0C\u5B50\u667A\u80FD\u4F53\u53EF\u4F7F\u7528\u6D4F\u89C8\u5668\u81EA\u52A8\u5316\u5DE5\u5177\uFF08\u9700\u540C\u65F6\u542F\u7528\u5168\u5C40\u201C\u5141\u8BB8\u6D4F\u89C8\u5668\u63A7\u5236\u201D\u548C\u201C\u5B50\u667A\u80FD\u4F53\uFF1A\u5141\u8BB8\u7F51\u7EDC\u641C\u7D22\u201D\uFF09\u3002"
        },
        subAgentTimeLimit: {
          displayName: "\u5B50\u667A\u80FD\u4F53\u8D85\u65F6\u65F6\u95F4\uFF08\u79D2\uFF09",
          subtitle: "\u5B50\u667A\u80FD\u4F53\u4EFB\u52A1\u5F3A\u5236\u7EC8\u6B62\u524D\u7684\u6700\u957F\u8FD0\u884C\u65F6\u95F4\u3002\u9ED8\u8BA4\uFF1A600 \u79D2\uFF0810 \u5206\u949F\uFF09\u3002"
        },
        enableDebugMode: {
          displayName: "\u542F\u7528\u81EA\u52A8\u8C03\u8BD5\u6A21\u5F0F",
          subtitle: "\u542F\u7528\u540E\uFF0C\u59D4\u6258\u7ED9\u5B50\u667A\u80FD\u4F53\u7684\u7F16\u7A0B\u4EFB\u52A1\u5B8C\u6210\u540E\u4F1A\u81EA\u52A8\u89E6\u53D1\u7B2C\u4E8C\u8F6E\u201C\u5BA1\u67E5\u5458\u201D\u68C0\u67E5\uFF0C\u53D1\u73B0\u5E76\u4FEE\u590D\u6F5C\u5728\u9519\u8BEF\u3002"
        },
        enableSubAgentDebugLogging: {
          displayName: "\u542F\u7528\u5B50\u667A\u80FD\u4F53\u8C03\u8BD5\u65E5\u5FD7",
          subtitle: "\u542F\u7528\u540E\uFF0C\u5B50\u667A\u80FD\u4F53\u7684\u5DE5\u5177\u8C03\u7528\u89E3\u6790\u8BE6\u60C5\u5C06\u8F93\u51FA\u5230\u63A7\u5236\u53F0\uFF0C\u7528\u4E8E\u6392\u67E5\u95EE\u9898\u3002"
        },
        subAgentAutoSave: {
          displayName: "\u5B50\u667A\u80FD\u4F53\uFF1A\u81EA\u52A8\u4FDD\u5B58\u4EE3\u7801",
          subtitle: "\u542F\u7528\u540E\uFF0C\u5B50\u667A\u80FD\u4F53\u751F\u6210\u4F46\u672A\u663E\u5F0F\u4FDD\u5B58\u7684\u4EE3\u7801\u5757\u5C06\u81EA\u52A8\u5199\u5165\u6587\u4EF6\u3002"
        },
        showFullCodeOutput: {
          displayName: "\u663E\u793A\u5B8C\u6574\u4EE3\u7801\u8F93\u51FA",
          subtitle: "\u542F\u7528\u540E\uFF0C\u4E3B\u4EE3\u7406\u5C06\u663E\u793A\u751F\u6210\u6587\u4EF6\u7684\u5B8C\u6574\u4EE3\u7801\u5185\u5BB9\uFF0C\u800C\u975E\u4EC5\u663E\u793A\u6587\u4EF6\u8DEF\u5F84\u3002"
        },
        simpleSystemPrompt: {
          displayName: "\u7B80\u5316\u7CFB\u7EDF\u63D0\u793A",
          subtitle: "\u4F7F\u7528\u7CBE\u7B80\u7684\u7CFB\u7EDF\u63D0\u793A\u4EE5\u964D\u4F4E CPU \u5DE5\u4F5C\u6D41\u7A0B\u7684\u5EF6\u8FDF\u3002\u8B66\u544A\uFF1A\u67D0\u4E9B\u6A21\u578B\u53EF\u80FD\u4F1A\u964D\u4F4E\u5DE5\u5177\u4F7F\u7528\u51C6\u786E\u6027\u3002"
        }
      },
      runtime: {
        statusLoadingEmbeddingModel: "\u6B63\u5728\u52A0\u8F7D\u68C0\u7D22\u6240\u9700\u7684\u5D4C\u5165\u6A21\u578B...",
        statusRetrievingCitations: "\u6B63\u5728\u68C0\u7D22\u4E0E\u7528\u6237\u67E5\u8BE2\u76F8\u5173\u7684\u5F15\u7528...",
        statusRetrievedCitations: (count) => `\u5DF2\u4E3A\u7528\u6237\u67E5\u8BE2\u68C0\u7D22\u5230 ${count} \u6761\u76F8\u5173\u5F15\u7528`,
        statusNoRelevantCitations: "\u672A\u627E\u5230\u4E0E\u7528\u6237\u67E5\u8BE2\u76F8\u5173\u7684\u5F15\u7528",
        statusDecidingStrategy: "\u6B63\u5728\u51B3\u5B9A\u6587\u6863\u5904\u7406\u7B56\u7565...",
        statusLoadingParser: (fileName) => `\u6B63\u5728\u4E3A ${fileName} \u52A0\u8F7D\u89E3\u6790\u5668...`,
        statusStrategyChosen: (strategy, detail) => `\u5DF2\u9009\u62E9\u4E0A\u4E0B\u6587\u6CE8\u5165\u7B56\u7565\uFF1A'${strategy}'\u3002${detail}`,
        citationPrefix: "\u5728\u7528\u6237\u63D0\u4F9B\u7684\u6587\u4EF6\u4E2D\u627E\u5230\u4EE5\u4E0B\u5F15\u7528\u5185\u5BB9\uFF1A\n\n",
        citationEntry: (num, text3) => `\u5F15\u7528 ${num}\uFF1A"${text3}"

`,
        citationSuffix: (userQuery) => `\u8BF7\u6839\u636E\u4E0A\u8FF0\u5F15\u7528\u5185\u5BB9\u56DE\u7B54\u7528\u6237\u95EE\u9898\uFF08\u4EC5\u5728\u76F8\u5173\u65F6\u4F7F\u7528\uFF09\uFF0C\u5426\u5219\u8BF7\u5C3D\u529B\u72EC\u7ACB\u4F5C\u7B54\u3002

\u7528\u6237\u95EE\u9898\uFF1A

${userQuery}`,
        noRelevantCitationsNote: "\u91CD\u8981\u63D0\u793A\uFF1A\u5728\u7528\u6237\u63D0\u4F9B\u7684\u6587\u4EF6\u4E2D\u672A\u627E\u5230\u4E0E\u67E5\u8BE2\u76F8\u5173\u7684\u5F15\u7528\u3002\u8BF7\u7528\u4E00\u53E5\u8BDD\u544A\u77E5\u7528\u6237\u6B64\u60C5\u51B5\uFF0C\u7136\u540E\u5C3D\u529B\u56DE\u7B54\u8BE5\u95EE\u9898\u3002",
        documentInjectionHeader: "\u8FD9\u662F\u4E00\u4E2A\u589E\u5F3A\u4E0A\u4E0B\u6587\u751F\u6210\u573A\u666F\u3002\n\n\u4EE5\u4E0B\u5185\u5BB9\u6765\u81EA\u7528\u6237\u63D0\u4F9B\u7684\u6587\u4EF6\u3002\n",
        documentInjectionFileBlock: (fileName, content) => `

** ${fileName} \u5B8C\u6574\u5185\u5BB9 **

${content}

** ${fileName} \u7ED3\u675F **

`,
        documentInjectionSuffix: (userQuery) => `\u8BF7\u57FA\u4E8E\u4EE5\u4E0A\u5185\u5BB9\u56DE\u7B54\u7528\u6237\u95EE\u9898\u3002

\u7528\u6237\u95EE\u9898\uFF1A${userQuery}`,
        delegationHintAlways: "\n\n**\u7CFB\u7EDF\u8981\u6C42\uFF1A** \u60A8\u5FC5\u987B\u5C06\u6240\u6709\u4FE1\u606F\u68C0\u7D22\u3001\u65B0\u95FB\u6458\u8981\u53CA**\u6240\u6709\u7F16\u7A0B\u4EFB\u52A1**\uFF08\u521B\u5EFA\u3001\u7F16\u8F91\u3001\u91CD\u6784\uFF09\u59D4\u6258\u7ED9\u8F85\u52A9\u667A\u80FD\u4F53\u3002\u8BF7\u52FF\u81EA\u884C\u7F16\u5199\u4EE3\u7801\u6216\u4F7F\u7528\u641C\u7D22\u5DE5\u5177\u3002\u4F7F\u7528 `consult_secondary_agent`\uFF08\u8BBE\u7F6E `allow_tools: true`\uFF09\u3002\n\n**\u59D4\u6258\u524D\u68C0\u67E5\u6E05\u5355\uFF1A**\n1. \u8FD0\u884C `list_directory` \u67E5\u770B\u73B0\u6709\u6587\u4EF6\u3002\n2. \u9605\u8BFB `beledarian_info.md` \u6216 `README.md`\uFF08\u5982\u5B58\u5728\uFF09\u3002\n3. \u643A\u5E26\u4E0A\u4E0B\u6587\u8C03\u7528 `consult_secondary_agent`\u3002",
        delegationHintWhenUseful: "\n\n**\u7CFB\u7EDF\u5EFA\u8BAE\uFF1A** \u5BF9\u4E8E\u590D\u6742\u4EFB\u52A1\uFF08\u4F8B\u5982\u201C\u521B\u5EFA\u4E00\u4E2A\u5E94\u7528\u201D\u3001\u201C\u91CD\u6784\u8FD9\u4E2A\u6A21\u5757\u201D\u3001\u201C\u7814\u7A76\u5E76\u603B\u7ED3\u201D\uFF09\uFF0C\u60A8**\u5FC5\u987B**\u4F7F\u7528 `consult_secondary_agent`\uFF08\u8BBE\u7F6E `allow_tools: true`\uFF09\u59D4\u6258\u7ED9\u8F85\u52A9\u667A\u80FD\u4F53\u3002\n\n**\u4E3A\u4EC0\u4E48\u8981\u59D4\u6258\uFF1F**\n- \u5B50\u667A\u80FD\u4F53\u6709\u4E13\u95E8\u7684\u7F16\u7A0B\u548C\u8C03\u8BD5\u5FAA\u73AF\u3002\n- \u5B83\u4F1A\u81EA\u52A8\u4FDD\u5B58\u6240\u6709\u6587\u4EF6\uFF0C\u60A8\u65E0\u9700\u624B\u52A8\u4FDD\u5B58\u3002\n\n**\u5982\u4F55\u59D4\u6258\uFF1A**\n1. \u6536\u96C6\u4E0A\u4E0B\u6587\uFF08`list_directory`\u3001`read_file`\uFF09\u3002\n2. \u643A\u5E26\u660E\u786E\u7684\u4EFB\u52A1\u63CF\u8FF0\u548C\u6536\u96C6\u5230\u7684\u4E0A\u4E0B\u6587\uFF0C\u8C03\u7528 `consult_secondary_agent`\u3002\n",
        delegationHintWhenUsefulDebug: "\u6CE8\u610F\uFF1A\u300C\u81EA\u52A8\u8C03\u8BD5\u300D\u5DF2\u5F00\u542F\u3002\u5B50\u667A\u80FD\u4F53\u5C06\u9A8C\u8BC1\u5E76\u4FEE\u590D\u81EA\u8EAB\u4EE3\u7801\uFF0C\u8FD9\u662F\u751F\u6210\u4EE3\u7801\u6700\u5B89\u5168\u7684\u65B9\u5F0F\u3002\n",
        delegationHintHardTasks: "\n\n**\u59D4\u6258\u63D0\u793A\uFF1A** \u4EC5\u5C06\u6781\u5176\u590D\u6742\u6216\u8BA1\u7B97\u91CF\u5927\u7684\u4EFB\u52A1\u59D4\u6258\u7ED9\u8F85\u52A9\u667A\u80FD\u4F53\u3002\u5E38\u89C4\u67E5\u8BE2\u548C\u6587\u4EF6\u8BFB\u53D6\u8BF7\u81EA\u884C\u5904\u7406\u3002\n",
        planHintAlways: "\n\n**\u8BA1\u5212\u6A21\u5F0F [\u5DF2\u5F00\u542F]\uFF1A** \u5728\u8FDB\u884C\u4EFB\u4F55\u6587\u4EF6\u66F4\u6539\u6216\u5B9E\u73B0\u529F\u80FD\u4E4B\u524D\uFF0C\u60A8\u5FC5\u987B\uFF1A\n1. **\u63A2\u7D22\uFF1A** \u4F7F\u7528 `list_directory`\u3001`read_file` \u53CA\u5176\u4ED6\u63A2\u7D22\u5DE5\u5177\u4E86\u89E3\u4EE3\u7801\u5E93\u7ED3\u6784\u548C\u4E0A\u4E0B\u6587\u3002\n2. **\u63D0\u6848\uFF1A** \u63D0\u51FA\u6E05\u6670\u7684\u5206\u6B65\u8BA1\u5212\uFF0C\u8BF4\u660E\u60A8\u8981\u505A\u4EC0\u4E48\u4EE5\u53CA\u4E3A\u4EC0\u4E48\u8FD9\u6837\u505A\u3002\n3. **\u7B49\u5F85\uFF1A** \u5728\u7528\u6237\u6279\u51C6\u8BA1\u5212\u6216\u660E\u786E\u5141\u8BB8\u7EE7\u7EED\u4E4B\u524D\uFF0C\u4E0D\u5F97\u5F00\u59CB\u5B9E\u65BD\u3002\n\n**\u4F8B\u5916\uFF1A** \u7B80\u5355\u5BF9\u8BDD\u3001\u6F84\u6E05\u95EE\u9898\u6216\u5FAE\u4E0D\u8DB3\u9053\u7684\u5355\u884C\u7F16\u8F91\u65E0\u9700\u8BA1\u5212\u3002",
        planHintWhenUseful: "\n\n**\u8BA1\u5212\u6A21\u5F0F [\u6309\u9700]\uFF1A** \u5BF9\u4E8E\u8F83\u5927\u3001\u590D\u6742\u6216\u542B\u7CCA\u7684\u8BF7\u6C42\uFF1A\n1. **\u5148\u63A2\u7D22\uFF1A** \u4F7F\u7528 `list_directory`\u3001`read_file` \u5728\u66F4\u6539\u4E4B\u524D\u7406\u89E3\u4EE3\u7801\u5E93\u3002\n2. **\u63D0\u51FA\u8BA1\u5212\uFF1A** \u5728\u5B9E\u65BD\u524D\u5148\u6982\u8FF0\u60A8\u7684\u65B9\u6CD5\u548C\u5173\u952E\u6B65\u9AA4\u3002\n3. **\u7B80\u5355\u4EFB\u52A1\u8DF3\u8FC7\uFF1A** \u666E\u901A\u5BF9\u8BDD\u6216\u5C0F\u578B\u7F16\u8F91\uFF08\u5982\u4FEE\u6B63\u62FC\u5199\u3001\u4FEE\u6539\u5355\u4E2A\u51FD\u6570\uFF09\u65E0\u9700\u8BA1\u5212\u3002"
      }
    };
  }
});

// src/locales/zh-TW.ts
var zhTW;
var init_zh_TW = __esm({
  "src/locales/zh-TW.ts"() {
    "use strict";
    zhTW = {
      config: {
        messageLanguage: {
          displayName: "\u8A0A\u606F\u8A9E\u8A00",
          subtitle: "\u57F7\u884C\u6642\u8A0A\u606F\u3001\u63D0\u793A\u53CA\u63D0\u793A\u8A5E\u6CE8\u5165\u6240\u4F7F\u7528\u7684\u8A9E\u8A00\u3002\u8B8A\u66F4\u7ACB\u5373\u751F\u6548\uFF0C\u7121\u9700\u91CD\u65B0\u555F\u52D5\u63D2\u4EF6\u3002"
        },
        uiLanguageOverride: {
          displayName: "\u4ECB\u9762\u8A9E\u8A00\u8986\u5BEB\uFF08\u4E0B\u6B21\u91CD\u555F\u751F\u6548\uFF09",
          subtitle: "\u5728\u4E0B\u6B21\u63D2\u4EF6\u91CD\u65B0\u555F\u52D5\u6642\u5F37\u5236\u4F7F\u7528\u6307\u5B9A\u5730\u5340\u8A2D\u5B9A\uFF0C\u8986\u5BEB\u4F5C\u696D\u7CFB\u7D71\u5075\u6E2C\u7D50\u679C\u3002\u8A2D\u5B9A\u70BA 'auto' \u5247\u4F7F\u7528\u4F5C\u696D\u7CFB\u7D71\u8A9E\u8A00\u3002\u9078\u9805\uFF1Aauto\u3001en\u3001zh-CN\u3001zh-TW\u3001de\u3002"
        },
        planMode: {
          displayName: "\u8A08\u5283\u6A21\u5F0F",
          subtitle: "\u63A7\u5236\u6A21\u578B\u5728\u9032\u884C\u8B8A\u66F4\u4E4B\u524D\u662F\u5426\u63A2\u7D22\u4E26\u63D0\u51FA\u8A08\u5283\u3002\u9078\u9805\uFF1A'always'\u3001'when_useful'\u3001'never'\u3002"
        },
        retrievalLimit: {
          displayName: "\u64F7\u53D6\u4E0A\u9650",
          subtitle: "\u89F8\u767C\u64F7\u53D6\u6642\uFF0C\u6700\u591A\u8FD4\u56DE\u7684\u6587\u5B57\u5340\u584A\u6578\u91CF\u3002"
        },
        retrievalAffinityThreshold: {
          displayName: "\u64F7\u53D6\u76F8\u95DC\u6027\u95BE\u503C",
          subtitle: "\u6587\u5B57\u5340\u584A\u88AB\u8996\u70BA\u76F8\u95DC\u6240\u9700\u7684\u6700\u4F4E\u76F8\u4F3C\u5EA6\u5206\u6578\u3002\u4E2D\u6587\u5167\u5BB9\u5EFA\u8B70\u8ABF\u4F4E\u81F3 0.35\u20130.45\u3002"
        },
        allowJavascriptExecution: {
          displayName: "\u5141\u8A31\u57F7\u884C JavaScript",
          subtitle: "\u555F\u7528 'run_javascript' \u5DE5\u5177\u3002\u5371\u96AA\uFF1A\u7A0B\u5F0F\u78BC\u5C07\u5728\u60A8\u7684\u96FB\u8166\u4E0A\u57F7\u884C\u3002"
        },
        allowPythonExecution: {
          displayName: "\u5141\u8A31\u57F7\u884C Python",
          subtitle: "\u555F\u7528 'run_python' \u5DE5\u5177\u3002\u5371\u96AA\uFF1A\u7A0B\u5F0F\u78BC\u5C07\u5728\u60A8\u7684\u96FB\u8166\u4E0A\u57F7\u884C\u3002"
        },
        allowCppExecution: {
          displayName: "\u5141\u8A31\u57F7\u884C C++",
          subtitle: "\u555F\u7528 'run_cpp' \u5DE5\u5177\uFF0C\u9700\u8981 g++\u3002\u5371\u96AA\uFF1A\u7A0B\u5F0F\u78BC\u5C07\u5728\u60A8\u7684\u96FB\u8166\u4E0A\u57F7\u884C\u3002"
        },
        allowJavaExecution: {
          displayName: "\u5141\u8A31\u57F7\u884C Java",
          subtitle: "\u555F\u7528 'run_java' \u5DE5\u5177\uFF0C\u9700\u8981 JDK\uFF08javac/java\uFF09\u3002\u5371\u96AA\uFF1A\u7A0B\u5F0F\u78BC\u5C07\u5728\u60A8\u7684\u96FB\u8166\u4E0A\u57F7\u884C\u3002"
        },
        allowPyrightExecution: {
          displayName: "\u5141\u8A31 Pyright \u578B\u5225\u6AA2\u67E5",
          subtitle: "\u555F\u7528 'run_pyright' \u5DE5\u5177\uFF0C\u9700\u8981\u5DF2\u5B89\u88DD\u4E26\u52A0\u5165 PATH \u7684 pyright\u3002\u50C5\u975C\u614B\u5206\u6790\u2014\u4E0D\u6703\u57F7\u884C\u60A8\u7684\u7A0B\u5F0F\u78BC\u3002"
        },
        allowTerminalExecution: {
          displayName: "\u5141\u8A31\u7D42\u7AEF\u6A5F\u57F7\u884C",
          subtitle: "\u555F\u7528 'run_in_terminal' \u5DE5\u5177\u3002\u5C07\u958B\u555F\u771F\u5BE6\u7684\u7D42\u7AEF\u6A5F\u8996\u7A97\u3002"
        },
        allowShellCommandExecution: {
          displayName: "\u5141\u8A31\u57F7\u884C Shell \u6307\u4EE4",
          subtitle: "\u555F\u7528 'execute_command' \u5DE5\u5177\u3002\u5371\u96AA\uFF1A\u6307\u4EE4\u5C07\u5728\u60A8\u7684\u96FB\u8166\u4E0A\u57F7\u884C\u3002"
        },
        allowBrowserControl: {
          displayName: "\u5141\u8A31\u700F\u89BD\u5668\u63A7\u5236",
          subtitle: "\u555F\u7528\u700F\u89BD\u5668\u81EA\u52D5\u5316\u5DE5\u5177\u3002\u5371\u96AA\uFF1A\u81EA\u52D5\u5316\u64CD\u4F5C\u5C07\u5728\u60A8\u7684\u96FB\u8166\u4E0A\u57F7\u884C\u3002"
        },
        allowGitOperations: {
          displayName: "\u5141\u8A31 Git \u64CD\u4F5C",
          subtitle: "\u555F\u7528\u539F\u751F Git \u5DE5\u5177\uFF08status\u3001diff\u3001show\u3001commit\u3001log\u3001add\u3001checkout\u3001push\uFF09\u3002"
        },
        allowGitHubTools: {
          displayName: "\u5141\u8A31 GitHub CLI \u5DE5\u5177",
          subtitle: "\u555F\u7528\u539F\u751F GitHub CLI \u5DE5\u5177\u3002\u9700\u5B89\u88DD 'gh'\u3002"
        },
        allowDatabaseInspection: {
          displayName: "\u5141\u8A31\u8CC7\u6599\u5EAB\u6AA2\u67E5",
          subtitle: "\u555F\u7528 'query_database' \u4EE5\u67E5\u8A62 SQLite \u6A94\u6848\u3002"
        },
        allowSystemNotifications: {
          displayName: "\u5141\u8A31\u7CFB\u7D71\u901A\u77E5",
          subtitle: "\u5141\u8A31\u667A\u80FD\u9AD4\u50B3\u9001\u4F5C\u696D\u7CFB\u7D71\u901A\u77E5\u3002"
        },
        allowAllCode: {
          displayName: "\u5141\u8A31\u6240\u6709\u7A0B\u5F0F\u78BC\u57F7\u884C",
          subtitle: "\u4E3B\u958B\u95DC\uFF1A\u8986\u84CB\u6240\u6709\u5176\u4ED6\u8A2D\u5B9A\uFF0C\u555F\u7528\u5168\u90E8\u57F7\u884C\u5DE5\u5177\u3002"
        },
        protectedPaths: {
          displayName: "\u53D7\u4FDD\u8B77\u8DEF\u5F91",
          subtitle: "\u8981\u7981\u6B62\u6240\u6709\u64CD\u4F5C\u7684\u78C1\u789F\u6A5F\u6216\u8DEF\u5F91\u5217\u8868\uFF08\u4F8B\u5982 D:\\\u3001C:\\Windows\uFF09\u3002\u6BCF\u884C\u4E00\u500B\u3002\u26A0\uFE0F Shell \u6307\u4EE4\u7121\u6CD5\u900F\u904E\u8DEF\u5F91\u6BD4\u5C0D\u5B8C\u5168\u6514\u622A\u2014\u2014\u8ACB\u5C07\u6B64\u529F\u80FD\u8996\u70BA\u9632\u8B77\u63AA\u65BD\uFF0C\u800C\u975E\u5B89\u5168\u908A\u754C\u3002"
        },
        searchApiKey: {
          displayName: "\u641C\u5C0B API \u91D1\u9470",
          subtitle: "\u641C\u5C0B\u670D\u52D9\u7684\u9078\u7528 API \u91D1\u9470\uFF0C\u53EF\u907F\u514D\u901F\u7387\u9650\u5236\u3002"
        },
        embeddingModel: {
          displayName: "\u5D4C\u5165\u6A21\u578B",
          subtitle: "\u7528\u65BC RAG \u529F\u80FD\u7684\u6A21\u578B\uFF08\u9810\u8A2D\uFF1Anomic-ai/nomic-embed-text-v1.5-GGUF\uFF09\u3002\u4E2D\u6587\u5167\u5BB9\u63A8\u85A6\u4F7F\u7528 BAAI/bge-m3-gguf\u3002"
        },
        defaultWorkspacePath: {
          displayName: "\u9810\u8A2D\u5DE5\u4F5C\u5340\u8DEF\u5F91",
          subtitle: "\u9078\u7528\u7684\u555F\u52D5\u5DE5\u4F5C\u5340\u8DEF\u5F91\u3002\u7559\u7A7A\u5247\u4F7F\u7528\u5167\u5EFA\u9810\u8A2D\u76EE\u9304\u3002"
        },
        enableMemory: {
          displayName: "\u555F\u7528\u8A18\u61B6",
          subtitle: "\u555F\u7528\u5F8C\uFF0C\u6A21\u578B\u53EF\u5F9E\u5DE5\u4F5C\u5340\u7684 'memory.md' \u6A94\u6848\u4E2D\u5132\u5B58\u548C\u8B80\u53D6\u8CC7\u8A0A\u3002"
        },
        enableWikipediaTool: {
          displayName: "\u555F\u7528\u7DAD\u57FA\u767E\u79D1\u5DE5\u5177",
          subtitle: "\u555F\u7528 'wikipedia_search' \u5DE5\u5177\u3002"
        },
        enableLocalRag: {
          displayName: "\u555F\u7528\u672C\u5730 RAG",
          subtitle: "\u555F\u7528 'rag_local_files' \u5DE5\u5177\u4EE5\u641C\u5C0B\u5DE5\u4F5C\u5340\u6A94\u6848\u3002"
        },
        enableConfidenceAgentTools: {
          displayName: "\u555F\u7528 Confidence Agent Tool box",
          subtitle: "\u555F\u7528 API \u7A0B\u5F0F\u78BC\u9A57\u8B49\u6D41\u7A0B\uFF08resolve_api_spec\u3001query_pypi\u3001extract_claims\u3001\u516D\u500B verify_* \u5206\u5C64\u5DE5\u5177\u3001compute_ewcs\u3001make_decision\u3001present_report\u3001save_code\uFF09\u3002"
        },
        enableSecondaryAgent: {
          displayName: "\u555F\u7528\u8F14\u52A9\u667A\u80FD\u9AD4/\u6A21\u578B",
          subtitle: "\u5141\u8A31\u4E3B\u6A21\u578B\u5C07\u4EFB\u52D9\u59D4\u6D3E\u7D66\u8F14\u52A9\u6A21\u578B\uFF08\u4F8B\u5982\u7528\u65BC\u6458\u8981\uFF09\u3002"
        },
        useMainModelForSubAgent: {
          displayName: "\u4F7F\u7528\u4E3B\u6A21\u578B\u4F5C\u70BA\u5B50\u667A\u80FD\u9AD4",
          subtitle: "\u555F\u7528\u5F8C\uFF0C\u5B50\u667A\u80FD\u9AD4\u8FF4\u5708\u5C07\u4F7F\u7528\u4E3B LM Studio \u4F3A\u670D\u5668\uFF08localhost:1234\uFF09\uFF0C\u5FFD\u7565\u300C\u7AEF\u9EDE\u300D\u8A2D\u5B9A\u3002"
        },
        secondaryAgentEndpoint: {
          displayName: "\u8F14\u52A9\u667A\u80FD\u9AD4\u7AEF\u9EDE",
          subtitle: "\u8F14\u52A9\u6A21\u578B\u7684 API \u7AEF\u9EDE\uFF08\u4F8B\u5982 'http://localhost:1234/v1'\uFF09\u3002"
        },
        secondaryModelId: {
          displayName: "\u8F14\u52A9\u6A21\u578B ID",
          subtitle: "\u7528\u65BC\u8F14\u52A9\u667A\u80FD\u9AD4\u7684\u6A21\u578B ID\uFF08\u5FC5\u9808\u5DF2\u8F09\u5165/\u53EF\u7528\uFF09\u3002"
        },
        subAgentProfiles: {
          displayName: "\u5B50\u667A\u80FD\u9AD4\u8A2D\u5B9A\u6A94\uFF08JSON\uFF09",
          subtitle: '\u5B9A\u7FA9\u53EF\u7528\u7684\u5B50\u667A\u80FD\u9AD4\u3002\u683C\u5F0F\uFF1A{"coder": "\u4F60\u662F\u4E00\u4F4D\u7A0B\u5F0F\u8A2D\u8A08\u5C08\u5BB6...", ...}'
        },
        subAgentFrequency: {
          displayName: "\u5B50\u667A\u80FD\u9AD4\u547C\u53EB\u983B\u7387",
          subtitle: "\u63A7\u5236\u59D4\u6D3E\u983B\u7387\u3002\u9078\u9805\uFF1A'always'\u3001'when_useful'\u3001'hard_tasks'\u3001'never'\u3002"
        },
        subAgentAllowFileSystem: {
          displayName: "\u5B50\u667A\u80FD\u9AD4\uFF1A\u5141\u8A31\u6A94\u6848\u7CFB\u7D71",
          subtitle: "\u555F\u7528\u5F8C\uFF0C\u5B50\u667A\u80FD\u9AD4\u53EF\u4EE5\u8B80\u53D6\u548C\u5217\u51FA\u6A94\u6848\u3002"
        },
        subAgentAllowWeb: {
          displayName: "\u5B50\u667A\u80FD\u9AD4\uFF1A\u5141\u8A31\u7DB2\u8DEF\u641C\u5C0B",
          subtitle: "\u555F\u7528\u5F8C\uFF0C\u5B50\u667A\u80FD\u9AD4\u53EF\u4EE5\u4F7F\u7528\u7DAD\u57FA\u767E\u79D1\u548C DuckDuckGo\u3002"
        },
        subAgentAllowCode: {
          displayName: "\u5B50\u667A\u80FD\u9AD4\uFF1A\u5141\u8A31\u7A0B\u5F0F\u78BC\u57F7\u884C",
          subtitle: "\u555F\u7528\u5F8C\uFF0C\u5B50\u667A\u80FD\u9AD4\u53EF\u4EE5\u57F7\u884C Python/JS \u7A0B\u5F0F\u78BC\u3002\u5371\u96AA\uFF01"
        },
        subAgentAllowBrowserControl: {
          displayName: "\u5B50\u667A\u80FD\u9AD4\uFF1A\u5141\u8A31\u700F\u89BD\u5668\u63A7\u5236",
          subtitle: "\u555F\u7528\u5F8C\uFF0C\u5B50\u667A\u80FD\u9AD4\u53EF\u4EE5\u4F7F\u7528\u700F\u89BD\u5668\u81EA\u52D5\u5316\u5DE5\u5177\uFF08\u9700\u555F\u7528\u5168\u57DF\u300C\u5141\u8A31\u700F\u89BD\u5668\u63A7\u5236\u300D\uFF09\u3002"
        },
        subAgentTimeLimit: {
          displayName: "\u5B50\u667A\u80FD\u9AD4\u6642\u9593\u9650\u5236\uFF08\u79D2\uFF09",
          subtitle: "\u5B50\u667A\u80FD\u9AD4\u4EFB\u52D9\u5F37\u5236\u7D42\u6B62\u524D\u7684\u6700\u9577\u6642\u9593\u3002\u9810\u8A2D\uFF1A600 \u79D2\uFF0810 \u5206\u9418\uFF09\u3002"
        },
        enableDebugMode: {
          displayName: "\u555F\u7528\u81EA\u52D5\u5075\u932F\u6A21\u5F0F",
          subtitle: "\u555F\u7528\u5F8C\uFF0C\u59D4\u6D3E\u7D66\u5B50\u667A\u80FD\u9AD4\u7684\u7A0B\u5F0F\u8A2D\u8A08\u4EFB\u52D9\u5C07\u81EA\u52D5\u89F8\u767C\u300C\u5BE9\u67E5\u54E1\u300D\u4E8C\u6B21\u6AA2\u67E5\u3002"
        },
        enableSubAgentDebugLogging: {
          displayName: "\u555F\u7528\u5B50\u667A\u80FD\u9AD4\u5075\u932F\u8A18\u9304",
          subtitle: "\u555F\u7528\u5F8C\uFF0C\u5C07\u5B50\u667A\u80FD\u9AD4\u5DE5\u5177\u547C\u53EB\u89E3\u6790\u8A73\u60C5\u8A18\u9304\u81F3\u4E3B\u63A7\u53F0\u3002"
        },
        subAgentAutoSave: {
          displayName: "\u5B50\u667A\u80FD\u9AD4\uFF1A\u81EA\u52D5\u5132\u5B58\u7A0B\u5F0F\u78BC",
          subtitle: "\u555F\u7528\u5F8C\uFF0C\u5B50\u667A\u80FD\u9AD4\u751F\u6210\u4F46\u672A\u660E\u78BA\u5132\u5B58\u7684\u7A0B\u5F0F\u78BC\u5340\u584A\u5C07\u81EA\u52D5\u5132\u5B58\u81F3\u6A94\u6848\u3002"
        },
        showFullCodeOutput: {
          displayName: "\u986F\u793A\u5B8C\u6574\u7A0B\u5F0F\u78BC\u8F38\u51FA",
          subtitle: "\u555F\u7528\u5F8C\uFF0C\u4E3B\u4EE3\u7406\u5C07\u986F\u793A\u751F\u6210\u6A94\u6848\u7684\u5B8C\u6574\u7A0B\u5F0F\u78BC\u5167\u5BB9\uFF0C\u800C\u975E\u50C5\u986F\u793A\u6A94\u6848\u8DEF\u5F91\u3002"
        },
        simpleSystemPrompt: {
          displayName: "\u7C21\u5316\u7CFB\u7D71\u63D0\u793A",
          subtitle: "\u4F7F\u7528\u7CBE\u7C21\u7684\u7CFB\u7D71\u63D0\u793A\u4EE5\u964D\u4F4E CPU \u5DE5\u4F5C\u6D41\u7A0B\u7684\u5EF6\u9072\u3002\u8B66\u544A\uFF1A\u67D0\u4E9B\u6A21\u578B\u53EF\u80FD\u6703\u964D\u4F4E\u5DE5\u5177\u4F7F\u7528\u6E96\u78BA\u6027\u3002"
        }
      },
      runtime: {
        statusLoadingEmbeddingModel: "\u6B63\u5728\u8F09\u5165\u64F7\u53D6\u7528\u5D4C\u5165\u6A21\u578B...",
        statusRetrievingCitations: "\u6B63\u5728\u64F7\u53D6\u4F7F\u7528\u8005\u67E5\u8A62\u7684\u76F8\u95DC\u5F15\u7528...",
        statusRetrievedCitations: (count) => `\u5DF2\u70BA\u4F7F\u7528\u8005\u67E5\u8A62\u64F7\u53D6\u5230 ${count} \u689D\u76F8\u95DC\u5F15\u7528`,
        statusNoRelevantCitations: "\u672A\u627E\u5230\u8207\u4F7F\u7528\u8005\u67E5\u8A62\u76F8\u95DC\u7684\u5F15\u7528",
        statusDecidingStrategy: "\u6B63\u5728\u6C7A\u5B9A\u6587\u4EF6\u8655\u7406\u65B9\u5F0F...",
        statusLoadingParser: (fileName) => `\u6B63\u5728\u8F09\u5165 ${fileName} \u7684\u89E3\u6790\u5668...`,
        statusStrategyChosen: (strategy, detail) => `\u5DF2\u9078\u64C7\u4E0A\u4E0B\u6587\u6CE8\u5165\u7B56\u7565\uFF1A'${strategy}'\u3002${detail}`,
        citationPrefix: "\u4EE5\u4E0B\u5F15\u7528\u5167\u5BB9\u4F86\u81EA\u4F7F\u7528\u8005\u63D0\u4F9B\u7684\u6A94\u6848\uFF1A\n\n",
        citationEntry: (num, text3) => `\u5F15\u7528 ${num}\uFF1A\u300C${text3}\u300D

`,
        citationSuffix: (userQuery) => `\u8ACB\u6839\u64DA\u4E0A\u8FF0\u5F15\u7528\u5167\u5BB9\u56DE\u7B54\u4F7F\u7528\u8005\u7684\u554F\u984C\uFF08\u50C5\u5728\u76F8\u95DC\u6642\u4F7F\u7528\uFF09\uFF0C\u5426\u5247\u8ACB\u76E1\u529B\u7368\u7ACB\u4F5C\u7B54\u3002

\u4F7F\u7528\u8005\u554F\u984C\uFF1A

${userQuery}`,
        noRelevantCitationsNote: "\u91CD\u8981\u63D0\u793A\uFF1A\u5728\u4F7F\u7528\u8005\u6A94\u6848\u4E2D\u672A\u627E\u5230\u8207\u67E5\u8A62\u76F8\u95DC\u7684\u5F15\u7528\u3002\u8ACB\u7528\u4E00\u53E5\u8A71\u544A\u77E5\u4F7F\u7528\u8005\uFF0C\u7136\u5F8C\u76E1\u529B\u4F5C\u7B54\u3002",
        documentInjectionHeader: "\u9019\u662F\u4E00\u500B\u589E\u5F37\u4E0A\u4E0B\u6587\u751F\u6210\u5834\u666F\u3002\n\n\u4EE5\u4E0B\u5167\u5BB9\u4F86\u81EA\u4F7F\u7528\u8005\u63D0\u4F9B\u7684\u6A94\u6848\u3002\n",
        documentInjectionFileBlock: (fileName, content) => `

** ${fileName} \u5B8C\u6574\u5167\u5BB9 **

${content}

** ${fileName} \u7D50\u675F **

`,
        documentInjectionSuffix: (userQuery) => `\u8ACB\u6839\u64DA\u4EE5\u4E0A\u5167\u5BB9\u56DE\u7B54\u4F7F\u7528\u8005\u7684\u554F\u984C\u3002

\u4F7F\u7528\u8005\u554F\u984C\uFF1A${userQuery}`,
        delegationHintAlways: "\n\n**\u7CFB\u7D71\u6307\u4EE4\uFF1A** \u60A8\u5FC5\u9808\u5C07\u6240\u6709\u8CC7\u8A0A\u64F7\u53D6\u3001\u65B0\u805E\u6458\u8981\u53CA**\u6240\u6709\u7A0B\u5F0F\u8A2D\u8A08\u4EFB\u52D9**\u59D4\u6D3E\u7D66\u8F14\u52A9\u667A\u80FD\u9AD4\u3002\u8ACB\u52FF\u81EA\u884C\u64B0\u5BEB\u7A0B\u5F0F\u78BC\u3002\u4F7F\u7528 `consult_secondary_agent`\uFF08\u8A2D\u5B9A `allow_tools: true`\uFF09\u3002\n\n**\u59D4\u6D3E\u524D\u6AA2\u67E5\uFF1A**\n1. \u57F7\u884C `list_directory` \u67E5\u770B\u73FE\u6709\u6A94\u6848\u3002\n2. \u95B1\u8B80 `beledarian_info.md` \u6216 `README.md`\uFF08\u5982\u5B58\u5728\uFF09\u3002\n3. \u651C\u5E36\u4E0A\u4E0B\u6587\u547C\u53EB `consult_secondary_agent`\u3002",
        delegationHintWhenUseful: "\n\n**\u7CFB\u7D71\u5EFA\u8B70\uFF1A** \u5C0D\u65BC\u8907\u96DC\u4EFB\u52D9\uFF0C\u8ACB\u4F7F\u7528 `consult_secondary_agent`\uFF08`allow_tools: true`\uFF09\u59D4\u6D3E\u7D66\u8F14\u52A9\u667A\u80FD\u9AD4\u3002\n\n**\u5982\u4F55\u59D4\u6D3E\uFF1A**\n1. \u6536\u96C6\u4E0A\u4E0B\u6587\uFF08`list_directory`\u3001`read_file`\uFF09\u3002\n2. \u651C\u5E36\u660E\u78BA\u4EFB\u52D9\u63CF\u8FF0\u547C\u53EB `consult_secondary_agent`\u3002\n",
        delegationHintWhenUsefulDebug: "\u6CE8\u610F\uFF1A\u300C\u81EA\u52D5\u5075\u932F\u300D\u5DF2\u555F\u52D5\u3002\u5B50\u667A\u80FD\u9AD4\u5C07\u9A57\u8B49\u4E26\u4FEE\u5FA9\u81EA\u8EAB\u7A0B\u5F0F\u78BC\u3002\n",
        delegationHintHardTasks: "\n\n**\u59D4\u6D3E\u63D0\u793A\uFF1A** \u50C5\u5C07\u6975\u5176\u8907\u96DC\u7684\u4EFB\u52D9\u59D4\u6D3E\u7D66\u8F14\u52A9\u667A\u80FD\u9AD4\u3002\u6A19\u6E96\u67E5\u8A62\u8ACB\u81EA\u884C\u8655\u7406\u3002\n",
        planHintAlways: "\n\n**\u8A08\u5283\u6A21\u5F0F [\u5DF2\u555F\u52D5]\uFF1A** \u5728\u9032\u884C\u4EFB\u4F55\u8B8A\u66F4\u4E4B\u524D\uFF0C\u60A8\u5FC5\u9808\uFF1A\n1. **\u63A2\u7D22\uFF1A** \u4F7F\u7528 `list_directory`\u3001`read_file` \u4E86\u89E3\u7A0B\u5F0F\u78BC\u5EAB\u3002\n2. **\u63D0\u6848\uFF1A** \u6E05\u6670\u5217\u51FA\u5206\u6B65\u8A08\u5283\u3002\n3. **\u7B49\u5F85\uFF1A** \u4F7F\u7528\u8005\u6279\u51C6\u5F8C\u518D\u5BE6\u65BD\u3002\n\n**\u4F8B\u5916\uFF1A** \u7C21\u55AE\u5C0D\u8A71\u6216\u5FAE\u5C0F\u7DE8\u8F2F\u7121\u9700\u8A08\u5283\u3002",
        planHintWhenUseful: "\n\n**\u8A08\u5283\u6A21\u5F0F [\u6709\u9700\u8981\u6642]\uFF1A** \u5C0D\u65BC\u8907\u96DC\u8ACB\u6C42\uFF1A\n1. **\u5148\u884C\u63A2\u7D22** \u7A0B\u5F0F\u78BC\u5EAB\u3002\n2. **\u63D0\u51FA\u8A08\u5283** \u518D\u5BE6\u65BD\u3002\n3. **\u7C21\u55AE\u4EFB\u52D9\u8DF3\u904E\u3002**"
      }
    };
  }
});

// src/locales/de.ts
var de;
var init_de = __esm({
  "src/locales/de.ts"() {
    "use strict";
    de = {
      config: {
        messageLanguage: {
          displayName: "Nachrichtensprache",
          subtitle: "Sprache f\xFCr Laufzeitmeldungen, Hinweise und Prompt-Injektionen. \xC4nderungen gelten sofort ohne Neustart."
        },
        uiLanguageOverride: {
          displayName: "UI-Sprache \xFCberschreiben (beim n\xE4chsten Neustart)",
          subtitle: "Erzwingt beim n\xE4chsten Plugin-Neustart eine bestimmte Sprache f\xFCr die Oberfl\xE4che, \xFCberschreibt die OS-Erkennung. 'auto' verwendet die OS-Sprache. Optionen: auto, en, zh-CN, zh-TW, de."
        },
        planMode: {
          displayName: "Planungsmodus",
          subtitle: "Legt fest, wann das Modell vor \xC4nderungen einen Plan erkunden und vorschlagen soll. Optionen: 'always', 'when_useful', 'never'."
        },
        retrievalLimit: {
          displayName: "Abruf-Limit",
          subtitle: "Maximale Anzahl zur\xFCckgegebener Textabschnitte bei einem Abruf."
        },
        retrievalAffinityThreshold: {
          displayName: "Abruf-\xC4hnlichkeitsschwellwert",
          subtitle: "Mindestrelevanzwert, ab dem ein Textabschnitt als relevant gilt."
        },
        allowJavascriptExecution: {
          displayName: "JavaScript-Ausf\xFChrung erlauben",
          subtitle: "Aktiviert das 'run_javascript'-Tool. GEFAHR: Code l\xE4uft auf Ihrem Rechner."
        },
        allowPythonExecution: {
          displayName: "Python-Ausf\xFChrung erlauben",
          subtitle: "Aktiviert das 'run_python'-Tool. GEFAHR: Code l\xE4uft auf Ihrem Rechner."
        },
        allowCppExecution: {
          displayName: "C++-Ausf\xFChrung erlauben",
          subtitle: "Aktiviert das 'run_cpp'-Tool. Erfordert g++. GEFAHR: Code l\xE4uft auf Ihrem Rechner."
        },
        allowJavaExecution: {
          displayName: "Java-Ausf\xFChrung erlauben",
          subtitle: "Aktiviert das 'run_java'-Tool. Erfordert ein JDK (javac/java). GEFAHR: Code l\xE4uft auf Ihrem Rechner."
        },
        allowPyrightExecution: {
          displayName: "Pyright-Typpr\xFCfung erlauben",
          subtitle: "Aktiviert das 'run_pyright'-Tool. Erfordert eine installierte pyright im PATH. Nur statische Analyse \u2014 f\xFChrt Ihren Code nicht aus."
        },
        allowTerminalExecution: {
          displayName: "Terminal-Ausf\xFChrung erlauben",
          subtitle: "Aktiviert das 'run_in_terminal'-Tool. \xD6ffnet echte Terminal-Fenster."
        },
        allowShellCommandExecution: {
          displayName: "Shell-Befehlsausf\xFChrung erlauben",
          subtitle: "Aktiviert das 'execute_command'-Tool. GEFAHR: Befehle laufen auf Ihrem Rechner."
        },
        allowBrowserControl: {
          displayName: "Browser-Steuerung erlauben",
          subtitle: "Aktiviert Browser-Automatisierungstools. GEFAHR: Automatisierte Aktionen laufen auf Ihrem Rechner."
        },
        allowGitOperations: {
          displayName: "Git-Operationen erlauben",
          subtitle: "Aktiviert native Git-Tools (status, diff, show, commit, log, add, checkout, push)."
        },
        allowGitHubTools: {
          displayName: "GitHub-CLI-Tools erlauben",
          subtitle: "Aktiviert native GitHub-CLI-Tools. Erfordert installiertes 'gh'."
        },
        allowDatabaseInspection: {
          displayName: "Datenbankinspektion erlauben",
          subtitle: "Aktiviert 'query_database' f\xFCr SQLite-Dateien."
        },
        allowSystemNotifications: {
          displayName: "Systembenachrichtigungen erlauben",
          subtitle: "Erlaubt dem Agenten, OS-Benachrichtigungen zu senden."
        },
        allowAllCode: {
          displayName: "Alle Codeausf\xFChrung erlauben",
          subtitle: "HAUPTSCHALTER: \xDCberschreibt alle anderen Einstellungen und aktiviert ALLE Ausf\xFChrungstools."
        },
        protectedPaths: {
          displayName: "Gesch\xFCtzte Pfade",
          subtitle: "Liste der Laufwerke oder Pfade, f\xFCr die alle Vorg\xE4nge blockiert werden sollen (z. B. D:\\, C:\\Windows). Eine pro Zeile. Shell-Befehle k\xF6nnen durch Pfadabgleich nicht vollst\xE4ndig blockiert werden \u2013 als Schutzma\xDFnahme verwenden, nicht als Sicherheitsgrenze."
        },
        searchApiKey: {
          displayName: "Such-API-Schl\xFCssel",
          subtitle: "Optionaler API-Schl\xFCssel f\xFCr Suchdienste zur Vermeidung von Rate-Limits."
        },
        embeddingModel: {
          displayName: "Einbettungsmodell",
          subtitle: "Modell f\xFCr RAG-Funktionen (Standard: nomic-ai/nomic-embed-text-v1.5-GGUF)."
        },
        defaultWorkspacePath: {
          displayName: "Standard-Arbeitsbereichspfad",
          subtitle: "Optionaler Startarbeitsbereichspfad. Leer lassen f\xFCr das eingebaute Standardverzeichnis."
        },
        enableMemory: {
          displayName: "Ged\xE4chtnis aktivieren",
          subtitle: "Wenn aktiviert, kann das Modell Informationen aus einer 'memory.md'-Datei im Arbeitsbereich speichern und abrufen."
        },
        enableWikipediaTool: {
          displayName: "Wikipedia-Tool aktivieren",
          subtitle: "Aktiviert das 'wikipedia_search'-Tool."
        },
        enableLocalRag: {
          displayName: "Lokales RAG aktivieren",
          subtitle: "Aktiviert das 'rag_local_files'-Tool zur Suche in Arbeitsbereichsdateien."
        },
        enableConfidenceAgentTools: {
          displayName: "Confidence Agent Tool box aktivieren",
          subtitle: "Aktiviert die Verifikations-Pipeline f\xFCr API-Code (resolve_api_spec, query_pypi, extract_claims, die sechs verify_*-Tools, compute_ewcs, make_decision, present_report, save_code)."
        },
        enableSecondaryAgent: {
          displayName: "Sekund\xE4ren Agenten/Modell aktivieren",
          subtitle: "Erlaubt dem Hauptmodell, Aufgaben an ein sekund\xE4res Modell zu delegieren."
        },
        useMainModelForSubAgent: {
          displayName: "Hauptmodell als Sub-Agenten verwenden",
          subtitle: "Wenn aktiviert, verwendet die Sub-Agenten-Schleife den Haupt-LM-Studio-Server (localhost:1234). Ignoriert die 'Endpunkt'-Einstellung."
        },
        secondaryAgentEndpoint: {
          displayName: "Sekund\xE4rer Agenten-Endpunkt",
          subtitle: "API-Endpunkt des sekund\xE4ren Modells (z. B. 'http://localhost:1234/v1')."
        },
        secondaryModelId: {
          displayName: "Sekund\xE4re Modell-ID",
          subtitle: "ID des f\xFCr den Sub-Agenten zu verwendenden Modells (muss geladen/verf\xFCgbar sein)."
        },
        subAgentProfiles: {
          displayName: "Sub-Agenten-Profile (JSON)",
          subtitle: 'Verf\xFCgbare Sub-Agenten definieren. Format: {"coder": "Du bist ein Coding-Experte...", ...}'
        },
        subAgentFrequency: {
          displayName: "Sub-Agenten-H\xE4ufigkeit",
          subtitle: "Steuert, wie oft der Agent zur Delegation angehalten wird. Optionen: 'always', 'when_useful', 'hard_tasks', 'never'."
        },
        subAgentAllowFileSystem: {
          displayName: "Sub-Agent: Dateisystem erlauben",
          subtitle: "Wenn aktiviert, k\xF6nnen Sub-Agenten Dateien lesen und auflisten."
        },
        subAgentAllowWeb: {
          displayName: "Sub-Agent: Websuche erlauben",
          subtitle: "Wenn aktiviert, k\xF6nnen Sub-Agenten Wikipedia und DuckDuckGo verwenden."
        },
        subAgentAllowCode: {
          displayName: "Sub-Agent: Codeausf\xFChrung erlauben",
          subtitle: "Wenn aktiviert, k\xF6nnen Sub-Agenten Python/JS-Code ausf\xFChren. GEFAHR!"
        },
        subAgentAllowBrowserControl: {
          displayName: "Sub-Agent: Browser-Steuerung erlauben",
          subtitle: "Wenn aktiviert, k\xF6nnen Sub-Agenten Browser-Automatisierungstools verwenden (erfordert globale 'Browser-Steuerung')."
        },
        subAgentTimeLimit: {
          displayName: "Sub-Agenten-Zeitlimit (Sekunden)",
          subtitle: "Maximale Zeit f\xFCr Sub-Agenten-Aufgaben vor erzwungener Beendigung. Standard: 600 s (10 Min.)."
        },
        enableDebugMode: {
          displayName: "Auto-Debug-Modus aktivieren",
          subtitle: "Wenn aktiviert, l\xF6sen an Sub-Agenten delegierte Coding-Aufgaben automatisch einen zweiten 'Reviewer'-Durchlauf aus."
        },
        enableSubAgentDebugLogging: {
          displayName: "Sub-Agenten-Debug-Protokollierung aktivieren",
          subtitle: "Wenn aktiviert, werden Tool-Call-Parsing-Details des Sub-Agenten zur Fehlersuche in der Konsole protokolliert."
        },
        subAgentAutoSave: {
          displayName: "Sub-Agent: Code automatisch speichern",
          subtitle: "Wenn aktiviert, werden vom Sub-Agenten generierte, nicht explizit gespeicherte Code-Bl\xF6cke automatisch in Dateien gespeichert."
        },
        showFullCodeOutput: {
          displayName: "Vollst\xE4ndige Codeausgabe anzeigen",
          subtitle: "Wenn aktiviert, zeigt der Haupt-Agent den vollst\xE4ndigen Code-Inhalt generierter Dateien anstelle nur der Dateipfade."
        },
        simpleSystemPrompt: {
          displayName: "Vereinfachter System-Prompt",
          subtitle: "Verwendet einen komprimierten System-Prompt, um die Latenz bei CPU-Workflows zu reduzieren. Warnung: Kann die Tool-Nutzungsgenauigkeit bei einigen Modellen verringern."
        }
      },
      runtime: {
        statusLoadingEmbeddingModel: "Einbettungsmodell f\xFCr den Abruf wird geladen...",
        statusRetrievingCitations: "Relevante Zitate f\xFCr die Nutzeranfrage werden abgerufen...",
        statusRetrievedCitations: (count) => `${count} relevante Zitate f\xFCr die Nutzeranfrage abgerufen`,
        statusNoRelevantCitations: "Keine relevanten Zitate f\xFCr die Nutzeranfrage gefunden",
        statusDecidingStrategy: "Dokumentenverarbeitungsstrategie wird ermittelt...",
        statusLoadingParser: (fileName) => `Parser f\xFCr ${fileName} wird geladen...`,
        statusStrategyChosen: (strategy, detail) => `Kontext-Injektionsstrategie gew\xE4hlt: '${strategy}'. ${detail}`,
        citationPrefix: "Folgende Zitate wurden in den vom Nutzer bereitgestellten Dateien gefunden:\n\n",
        citationEntry: (num, text3) => `Zitat ${num}: \u201E${text3}"

`,
        citationSuffix: (userQuery) => `Verwenden Sie die obigen Zitate zur Beantwortung der Nutzeranfrage, sofern relevant. Andernfalls antworten Sie nach bestem Wissen ohne diese.

Nutzeranfrage:

${userQuery}`,
        noRelevantCitationsNote: "Wichtig: In den Nutzerdateien wurden keine relevanten Zitate zur Anfrage gefunden. Informieren Sie den Nutzer in einem Satz dar\xFCber. Beantworten Sie die Anfrage dann nach bestem Wissen.",
        documentInjectionHeader: "Dies ist ein Szenario zur erweiterten Kontextgenerierung.\n\nFolgender Inhalt wurde in den vom Nutzer bereitgestellten Dateien gefunden.\n",
        documentInjectionFileBlock: (fileName, content) => `

** Vollst\xE4ndiger Inhalt von ${fileName} **

${content}

** Ende von ${fileName} **

`,
        documentInjectionSuffix: (userQuery) => `Bitte antworten Sie auf Basis der obigen Inhalte auf die Nutzeranfrage.

Nutzeranfrage: ${userQuery}`,
        delegationHintAlways: "\n\n**SYSTEMAUFTRAG:** Sie M\xDCSSEN alle Informationsabrufe, Nachrichtenzusammenfassungen und **alle Coding-Aufgaben** (Erstellen, Bearbeiten, Refaktorieren) an den Sekund\xE4r-Agenten delegieren. Schreiben Sie KEINEN Code selbst. Verwenden Sie `consult_secondary_agent` mit `allow_tools: true`.\n\n**Vor-Delegations-Checkliste:**\n1. `list_directory` ausf\xFChren, um vorhandene Dateien zu sehen.\n2. `beledarian_info.md` oder `README.md` lesen, falls vorhanden.\n3. `consult_secondary_agent` mit dem Kontext aufrufen.",
        delegationHintWhenUseful: "\n\n**SYSTEMEMPFEHLUNG:** F\xFCr komplexe Aufgaben (z. B. 'App erstellen', 'Modul refaktorieren', 'recherchieren und zusammenfassen') **M\xDCSSEN** Sie mit `consult_secondary_agent` (mit `allow_tools: true`) an den Sekund\xE4r-Agenten delegieren.\n\n**So delegieren Sie:**\n1. Kontext sammeln (`list_directory`, `read_file`).\n2. `consult_secondary_agent` mit einer klaren Aufgabenbeschreibung aufrufen.\n",
        delegationHintWhenUsefulDebug: "Hinweis: 'Auto-Debug' ist AKTIV. Der Sub-Agent \xFCberpr\xFCft und korrigiert seinen eigenen Code.\n",
        delegationHintHardTasks: "\n\n**Delegations-Hinweis:** Delegieren Sie nur EXTREM komplexe oder rechenintensive Aufgaben an den Sekund\xE4r-Agenten. Standardanfragen und Datei-Lesevorg\xE4nge selbst bearbeiten.\n",
        planHintAlways: "\n\n**PLANUNGSMODUS [AKTIV]:** Vor JEGLICHEN Datei\xE4nderungen oder Implementierungen M\xDCSSEN Sie:\n1. **ERKUNDEN:** `list_directory`, `read_file` und andere Erkundungstools nutzen.\n2. **VORSCHLAGEN:** Einen klaren Schritt-f\xFCr-Schritt-Plan darlegen.\n3. **WARTEN:** NICHT implementieren, bis der Nutzer den Plan genehmigt.\n\n**Ausnahme:** Einfache Gespr\xE4che oder triviale Einzeilen-\xC4nderungen erfordern keine Planung.",
        planHintWhenUseful: "\n\n**PLANUNGSMODUS [Bei Bedarf]:** F\xFCr gr\xF6\xDFere, komplexe oder mehrdeutige Anfragen:\n1. **ZUERST ERKUNDEN:** Codebase vor \xC4nderungen mit `list_directory`, `read_file` verstehen.\n2. **PLAN VORSCHLAGEN:** Vorgehen und wichtigste Schritte vor der Implementierung skizzieren.\n3. **EINFACHE AUFGABEN \xDCBERSPRINGEN:** Normale Gespr\xE4che oder kleine \xC4nderungen erfordern keine Planung."
      }
    };
  }
});

// src/locales/i18n.ts
function readPersistedLocaleOverride() {
  try {
    const statePath = (0, import_path.join)(os.homedir(), ".beledarians-llm-toolbox", ".plugin_state.json");
    const raw = (0, import_fs.readFileSync)(statePath, "utf-8");
    const state = JSON.parse(raw);
    const override = state?.uiLanguageOverride;
    if (typeof override === "string" && override && override !== "auto") {
      return override;
    }
  } catch {
  }
  return "";
}
function detectSystemLanguage() {
  try {
    const intlLocale = Intl.DateTimeFormat().resolvedOptions().locale;
    if (intlLocale && intlLocale !== "C" && intlLocale !== "POSIX" && intlLocale.length > 1) {
      return intlLocale;
    }
  } catch {
  }
  const posixVars = ["LC_ALL", "LANGUAGE", "LANG"];
  for (const envVar of posixVars) {
    const raw = process.env[envVar];
    if (raw && raw.length > 1 && raw !== "C" && raw !== "POSIX") {
      return raw.split(".")[0].replace(/_/g, "-");
    }
  }
  return "en";
}
function resolveLocale(raw) {
  if (!raw || typeof raw !== "string") return "en";
  const tag = raw.toLowerCase();
  if (tag.startsWith("zh-tw") || tag.startsWith("zh-hk") || tag.startsWith("zh-mo") || tag.startsWith("zh-hant") || tag === "zh_tw" || tag === "zh_hk") {
    return "zh-TW";
  }
  if (tag.startsWith("zh-cn") || tag.startsWith("zh-hans") || tag.startsWith("zh-sg") || tag === "zh_cn" || tag === "zh") {
    return "zh-CN";
  }
  if (tag.startsWith("de")) {
    return "de";
  }
  return "en";
}
function getDict(locale) {
  if (locale && LOCALES[locale]) {
    return LOCALES[locale];
  }
  return en;
}
function getSystemDict() {
  const persistedOverride = readPersistedLocaleOverride();
  if (persistedOverride) {
    const resolvedLocale3 = resolveLocale(persistedOverride);
    return { dict: getDict(resolvedLocale3), resolvedLocale: resolvedLocale3 };
  }
  const raw = detectSystemLanguage();
  const resolvedLocale2 = resolveLocale(raw);
  return { dict: getDict(resolvedLocale2), resolvedLocale: resolvedLocale2 };
}
var import_fs, import_path, os, LOCALES, SUPPORTED_LOCALE_IDS;
var init_i18n = __esm({
  "src/locales/i18n.ts"() {
    "use strict";
    init_en();
    init_zh_CN();
    init_zh_TW();
    init_de();
    import_fs = require("fs");
    import_path = require("path");
    os = __toESM(require("os"));
    LOCALES = {
      en,
      "zh-CN": zhCN,
      "zh-TW": zhTW,
      de
    };
    SUPPORTED_LOCALE_IDS = Object.keys(LOCALES);
  }
});

// src/config.ts
var import_sdk, t, resolvedLocale, c, pluginConfigSchematics;
var init_config = __esm({
  "src/config.ts"() {
    "use strict";
    import_sdk = require("@lmstudio/sdk");
    init_i18n();
    ({ dict: t, resolvedLocale } = getSystemDict());
    c = t.config;
    pluginConfigSchematics = (0, import_sdk.createConfigSchematics)().field("messageLanguage", "string", {
      displayName: c.messageLanguage.displayName,
      subtitle: c.messageLanguage.subtitle
    }, resolvedLocale).field("uiLanguageOverride", "string", {
      displayName: c.uiLanguageOverride.displayName,
      subtitle: c.uiLanguageOverride.subtitle
    }, "auto").field("planMode", "string", {
      displayName: c.planMode.displayName,
      subtitle: c.planMode.subtitle
    }, "when_useful").field("retrievalLimit", "numeric", {
      int: true,
      min: 1,
      displayName: c.retrievalLimit.displayName,
      subtitle: c.retrievalLimit.subtitle,
      slider: { min: 1, max: 10, step: 1 }
    }, 3).field("retrievalAffinityThreshold", "numeric", {
      min: 0,
      max: 1,
      displayName: c.retrievalAffinityThreshold.displayName,
      subtitle: c.retrievalAffinityThreshold.subtitle,
      slider: { min: 0, max: 1, step: 0.01 }
    }, 0.5).field("allowJavascriptExecution", "boolean", {
      displayName: c.allowJavascriptExecution.displayName,
      subtitle: c.allowJavascriptExecution.subtitle
    }, false).field("allowPythonExecution", "boolean", {
      displayName: c.allowPythonExecution.displayName,
      subtitle: c.allowPythonExecution.subtitle
    }, false).field("allowCppExecution", "boolean", {
      displayName: c.allowCppExecution.displayName,
      subtitle: c.allowCppExecution.subtitle
    }, false).field("allowJavaExecution", "boolean", {
      displayName: c.allowJavaExecution.displayName,
      subtitle: c.allowJavaExecution.subtitle
    }, false).field("allowPyrightExecution", "boolean", {
      displayName: c.allowPyrightExecution.displayName,
      subtitle: c.allowPyrightExecution.subtitle
    }, false).field("allowTerminalExecution", "boolean", {
      displayName: c.allowTerminalExecution.displayName,
      subtitle: c.allowTerminalExecution.subtitle
    }, false).field("allowShellCommandExecution", "boolean", {
      displayName: c.allowShellCommandExecution.displayName,
      subtitle: c.allowShellCommandExecution.subtitle
    }, false).field("allowBrowserControl", "boolean", {
      displayName: c.allowBrowserControl.displayName,
      subtitle: c.allowBrowserControl.subtitle
    }, false).field("allowGitOperations", "boolean", {
      displayName: c.allowGitOperations.displayName,
      subtitle: c.allowGitOperations.subtitle
    }, true).field("allowGitHubTools", "boolean", {
      displayName: c.allowGitHubTools.displayName,
      subtitle: c.allowGitHubTools.subtitle
    }, true).field("allowDatabaseInspection", "boolean", {
      displayName: c.allowDatabaseInspection.displayName,
      subtitle: c.allowDatabaseInspection.subtitle
    }, false).field("allowSystemNotifications", "boolean", {
      displayName: c.allowSystemNotifications.displayName,
      subtitle: c.allowSystemNotifications.subtitle
    }, true).field("allowAllCode", "boolean", {
      displayName: c.allowAllCode.displayName,
      subtitle: c.allowAllCode.subtitle
    }, false).field("protectedPaths", "string", {
      displayName: c.protectedPaths.displayName,
      subtitle: c.protectedPaths.subtitle
    }, "").field("searchApiKey", "string", {
      displayName: c.searchApiKey.displayName,
      subtitle: c.searchApiKey.subtitle
    }, "").field("embeddingModel", "string", {
      displayName: c.embeddingModel.displayName,
      subtitle: c.embeddingModel.subtitle
    }, "nomic-ai/nomic-embed-text-v1.5-GGUF").field("defaultWorkspacePath", "string", {
      displayName: c.defaultWorkspacePath.displayName,
      subtitle: c.defaultWorkspacePath.subtitle
    }, "").field("enableMemory", "boolean", {
      displayName: c.enableMemory.displayName,
      subtitle: c.enableMemory.subtitle
    }, false).field("enableWikipediaTool", "boolean", {
      displayName: c.enableWikipediaTool.displayName,
      subtitle: c.enableWikipediaTool.subtitle
    }, true).field("enableLocalRag", "boolean", {
      displayName: c.enableLocalRag.displayName,
      subtitle: c.enableLocalRag.subtitle
    }, true).field("enableConfidenceAgentTools", "boolean", {
      displayName: c.enableConfidenceAgentTools.displayName,
      subtitle: c.enableConfidenceAgentTools.subtitle
    }, true).field("enableSecondaryAgent", "boolean", {
      displayName: c.enableSecondaryAgent.displayName,
      subtitle: c.enableSecondaryAgent.subtitle
    }, false).field("useMainModelForSubAgent", "boolean", {
      displayName: c.useMainModelForSubAgent.displayName,
      subtitle: c.useMainModelForSubAgent.subtitle
    }, false).field("secondaryAgentEndpoint", "string", {
      displayName: c.secondaryAgentEndpoint.displayName,
      subtitle: c.secondaryAgentEndpoint.subtitle
    }, "http://localhost:1234/v1").field("secondaryModelId", "string", {
      displayName: c.secondaryModelId.displayName,
      subtitle: c.secondaryModelId.subtitle
    }, "local-model").field("subAgentProfiles", "string", {
      displayName: c.subAgentProfiles.displayName,
      subtitle: c.subAgentProfiles.subtitle
    }, '{"summarizer": "You are a summarization expert. Summarize the content concisely.", "coder": "You are a software engineer. Write efficient and safe code."}').field("subAgentFrequency", "string", {
      displayName: c.subAgentFrequency.displayName,
      subtitle: c.subAgentFrequency.subtitle
    }, "when_useful").field("subAgentAllowFileSystem", "boolean", {
      displayName: c.subAgentAllowFileSystem.displayName,
      subtitle: c.subAgentAllowFileSystem.subtitle
    }, true).field("subAgentAllowWeb", "boolean", {
      displayName: c.subAgentAllowWeb.displayName,
      subtitle: c.subAgentAllowWeb.subtitle
    }, true).field("subAgentAllowCode", "boolean", {
      displayName: c.subAgentAllowCode.displayName,
      subtitle: c.subAgentAllowCode.subtitle
    }, false).field("subAgentAllowBrowserControl", "boolean", {
      displayName: c.subAgentAllowBrowserControl.displayName,
      subtitle: c.subAgentAllowBrowserControl.subtitle
    }, false).field("subAgentTimeLimit", "numeric", {
      int: true,
      min: 30,
      max: 3600,
      displayName: c.subAgentTimeLimit.displayName,
      subtitle: c.subAgentTimeLimit.subtitle
    }, 600).field("enableDebugMode", "boolean", {
      displayName: c.enableDebugMode.displayName,
      subtitle: c.enableDebugMode.subtitle
    }, false).field("enableSubAgentDebugLogging", "boolean", {
      displayName: c.enableSubAgentDebugLogging.displayName,
      subtitle: c.enableSubAgentDebugLogging.subtitle
    }, false).field("subAgentAutoSave", "boolean", {
      displayName: c.subAgentAutoSave.displayName,
      subtitle: c.subAgentAutoSave.subtitle
    }, true).field("showFullCodeOutput", "boolean", {
      displayName: c.showFullCodeOutput.displayName,
      subtitle: c.showFullCodeOutput.subtitle
    }, false).field("simpleSystemPrompt", "boolean", {
      displayName: c.simpleSystemPrompt.displayName,
      subtitle: c.simpleSystemPrompt.subtitle
    }, false).build();
  }
});

// src/findLMStudioHome.ts
function findLMStudioHome() {
  if (lmstudioHome !== null) {
    return lmstudioHome;
  }
  const resolvedHomeDir = (0, import_fs2.realpathSync)((0, import_os.homedir)());
  const pointerFilePath = (0, import_path2.join)(resolvedHomeDir, ".lmstudio-home-pointer");
  if ((0, import_fs2.existsSync)(pointerFilePath)) {
    lmstudioHome = (0, import_fs2.readFileSync)(pointerFilePath, "utf-8").trim();
    return lmstudioHome;
  }
  const cacheHome = (0, import_path2.join)(resolvedHomeDir, ".cache", "lm-studio");
  if ((0, import_fs2.existsSync)(cacheHome)) {
    lmstudioHome = cacheHome;
    (0, import_fs2.writeFileSync)(pointerFilePath, lmstudioHome, "utf-8");
    return lmstudioHome;
  }
  const home = (0, import_path2.join)(resolvedHomeDir, ".lmstudio");
  lmstudioHome = home;
  (0, import_fs2.writeFileSync)(pointerFilePath, lmstudioHome, "utf-8");
  return lmstudioHome;
}
var import_fs2, import_os, import_path2, lmstudioHome;
var init_findLMStudioHome = __esm({
  "src/findLMStudioHome.ts"() {
    "use strict";
    import_fs2 = require("fs");
    import_os = require("os");
    import_path2 = require("path");
    lmstudioHome = null;
  }
});

// src/stateManager.ts
function resolveWorkspaceDirectory(configuredWorkspacePath) {
  const raw = (configuredWorkspacePath ?? "").trim();
  if (!raw) return DEFAULT_DIR;
  const expanded = raw.replace(/%([^%]+)%/g, (_match, varName) => process.env[varName] ?? `%${varName}%`);
  return (0, import_path3.isAbsolute)(expanded) ? expanded : (0, import_path3.resolve)(DEFAULT_DIR, expanded);
}
async function getPersistedState(configuredWorkspacePath) {
  const configuredDirectory = resolveWorkspaceDirectory(configuredWorkspacePath);
  try {
    const statePath = (0, import_path3.join)(os2.homedir(), ".beledarians-llm-toolbox", CONFIG_FILE_NAME);
    const content = await (0, import_promises.readFile)(statePath, "utf-8");
    const state = JSON.parse(content);
    return {
      // configuredDirectory is a startup default/fallback, not a forced override
      currentWorkingDirectory: state.currentWorkingDirectory ?? configuredDirectory,
      messageCount: state.messageCount ?? 0,
      dontAskToCompress: state.dontAskToCompress ?? false,
      subAgentDocsInjected: state.subAgentDocsInjected ?? false,
      uiLanguageOverride: state.uiLanguageOverride ?? "auto"
    };
  } catch (error) {
    return {
      currentWorkingDirectory: configuredDirectory,
      messageCount: 0,
      dontAskToCompress: false,
      subAgentDocsInjected: false,
      uiLanguageOverride: "auto"
    };
  }
}
async function savePersistedState(state) {
  try {
    const statePath = (0, import_path3.join)(os2.homedir(), ".beledarians-llm-toolbox", CONFIG_FILE_NAME);
    const dir = (0, import_path3.join)(os2.homedir(), ".beledarians-llm-toolbox");
    await (0, import_promises.mkdir)(dir, { recursive: true });
    await (0, import_promises.writeFile)(statePath, JSON.stringify(state, null, 2), "utf-8");
  } catch (error) {
    console.error("Failed to save plugin state:", error);
  }
}
async function ensureWorkspaceExists(path) {
  try {
    await (0, import_promises.mkdir)(path, { recursive: true });
  } catch (error) {
    console.error(`Failed to create/access directory ${path}`, error);
  }
}
var import_promises, import_path3, os2, CONFIG_FILE_NAME, DEFAULT_DIR;
var init_stateManager = __esm({
  "src/stateManager.ts"() {
    "use strict";
    import_promises = require("fs/promises");
    import_path3 = require("path");
    os2 = __toESM(require("os"));
    CONFIG_FILE_NAME = ".plugin_state.json";
    DEFAULT_DIR = (0, import_path3.join)(os2.homedir(), ".beledarians-llm-toolbox", "workspace");
  }
});

// src/browserActions.ts
async function executeBrowserActions(page, actions) {
  const actionLog = [];
  const clickRetryDelayMs = 300;
  const safeClick = async (selector, clickCount) => {
    await page.waitForSelector(selector, { timeout: 15e3 });
    const performClick = async () => {
      if (clickCount) {
        await page.click(selector, { clickCount });
      } else {
        await page.click(selector);
      }
    };
    try {
      await performClick();
      return;
    } catch {
      try {
        await new Promise((resolve5) => setTimeout(resolve5, clickRetryDelayMs));
        await performClick();
        return;
      } catch {
      }
      const fallbackResult = await page.evaluate(
        ({ targetSelector, targetClickCount }) => {
          const target = document.querySelector(targetSelector);
          if (!(target instanceof HTMLElement)) {
            return { ok: false, reason: "not-an-element" };
          }
          target.scrollIntoView({ behavior: "auto", block: "center", inline: "center" });
          const rect = target.getBoundingClientRect();
          if (rect.width <= 0 || rect.height <= 0) {
            return { ok: false, reason: "not-clickable" };
          }
          if (targetClickCount && targetClickCount >= 3 && (target instanceof HTMLInputElement || target instanceof HTMLTextAreaElement)) {
            target.select();
          }
          target.click();
          return { ok: true };
        },
        { targetSelector: selector, targetClickCount: clickCount ?? 1 }
      );
      if (!fallbackResult?.ok) {
        const reason = fallbackResult?.reason || "unknown";
        throw new Error(`Action 'click' failed for selector '${selector}' (${reason}).`);
      }
    }
  };
  for (const action of actions) {
    if (action.type === "wait_for_selector") {
      if (!action.selector) throw new Error("Action 'wait_for_selector' requires 'selector'.");
      await page.waitForSelector(action.selector, { timeout: 15e3 });
      actionLog.push(`wait_for_selector:${action.selector}`);
    } else if (action.type === "wait") {
      const ms = action.milliseconds ?? 500;
      await new Promise((resolve5) => setTimeout(resolve5, ms));
      actionLog.push(`wait:${ms}`);
    } else if (action.type === "click") {
      if (!action.selector) throw new Error("Action 'click' requires 'selector'.");
      await safeClick(action.selector);
      actionLog.push(`click:${action.selector}`);
    } else if (action.type === "type") {
      if (!action.selector) throw new Error("Action 'type' requires 'selector'.");
      if (typeof action.text !== "string") throw new Error("Action 'type' requires 'text'.");
      await safeClick(action.selector, 3);
      await page.keyboard.press("Backspace");
      await page.type(action.selector, action.text, { delay: 20 });
      actionLog.push(`type:${action.selector}`);
    } else if (action.type === "press") {
      if (!action.key) throw new Error("Action 'press' requires 'key'.");
      await page.keyboard.press(action.key);
      actionLog.push(`press:${action.key}`);
    } else if (action.type === "select") {
      if (!action.selector) throw new Error("Action 'select' requires 'selector'.");
      if (typeof action.value !== "string") throw new Error("Action 'select' requires 'value'.");
      const selected = await page.select(action.selector, action.value);
      if (selected.length === 0) throw new Error(`Action 'select' found no matching option for '${action.value}'.`);
      actionLog.push(`select:${action.selector}`);
    } else if (action.type === "hover") {
      if (!action.selector) throw new Error("Action 'hover' requires 'selector'.");
      await page.hover(action.selector);
      actionLog.push(`hover:${action.selector}`);
    } else if (action.type === "scroll") {
      if (action.selector) {
        await page.evaluate((selector) => {
          const target = document.querySelector(selector);
          if (!target) throw new Error(`Selector not found: ${selector}`);
          target.scrollIntoView({ behavior: "auto", block: "center", inline: "nearest" });
        }, action.selector);
        actionLog.push(`scroll_into_view:${action.selector}`);
      } else {
        const x = action.x ?? 0;
        const y = action.y ?? 600;
        await page.evaluate(
          ({ dx, dy }) => {
            window.scrollBy(dx, dy);
          },
          { dx: x, dy: y }
        );
        actionLog.push(`scroll:${x},${y}`);
      }
    } else if (action.type === "evaluate") {
      if (!action.script) throw new Error("Action 'evaluate' requires 'script'.");
      await page.evaluate((script) => {
        return Function(`"use strict";
${script}`)();
      }, action.script);
      actionLog.push("evaluate");
    }
  }
  return actionLog;
}
var init_browserActions = __esm({
  "src/browserActions.ts"() {
    "use strict";
  }
});

// src/fuzzySearch.ts
function normalize(input) {
  return input.toLowerCase().replace(/\s+/g, " ").trim();
}
function levenshteinDistance(a, b) {
  const left = normalize(a);
  const right = normalize(b);
  const m = left.length;
  const n = right.length;
  if (m === 0) return n;
  if (n === 0) return m;
  const prev = new Array(n + 1);
  const curr = new Array(n + 1);
  for (let j = 0; j <= n; j++) prev[j] = j;
  for (let i = 1; i <= m; i++) {
    curr[0] = i;
    for (let j = 1; j <= n; j++) {
      const cost = left[i - 1] === right[j - 1] ? 0 : 1;
      curr[j] = Math.min(
        prev[j] + 1,
        curr[j - 1] + 1,
        prev[j - 1] + cost
      );
    }
    for (let j = 0; j <= n; j++) prev[j] = curr[j];
  }
  return prev[n];
}
function computeFuzzyScore(query, candidate) {
  const q = normalize(query);
  const c2 = normalize(candidate);
  if (!q || !c2) return 0;
  if (q === c2) return 1;
  if (c2.includes(q)) {
    const coverage = q.length / c2.length;
    return Math.min(1, 0.85 + coverage * 0.15);
  }
  const distance = levenshteinDistance(q, c2);
  const maxLen = Math.max(q.length, c2.length);
  return Math.max(0, 1 - distance / maxLen);
}
function rankFuzzyMatches(query, candidates, limit = 5) {
  const ranked = candidates.map((value) => ({ value, score: computeFuzzyScore(query, value) })).sort((a, b) => b.score - a.score || a.value.length - b.value.length).slice(0, limit);
  return ranked;
}
var init_fuzzySearch = __esm({
  "src/fuzzySearch.ts"() {
    "use strict";
  }
});

// src/handoffMessage.ts
function extractHandoffMessage(rawContent) {
  const markerRegex = /\[HANDOFF_MESSAGE\]([\s\S]*?)\[\/HANDOFF_MESSAGE\]/i;
  const markerMatch = rawContent.match(markerRegex);
  if (markerMatch) {
    const handoff = markerMatch[1].trim();
    const response = rawContent.replace(markerRegex, "").trim();
    return {
      response,
      handoffMessage: handoff || void 0
    };
  }
  const candidates = [];
  const trimmed = rawContent.trim();
  if (trimmed.startsWith("{") && trimmed.endsWith("}")) {
    candidates.push({ json: trimmed });
  }
  const fenceRegex = /```json\s*([\s\S]*?)```/gi;
  let fenceMatch;
  while ((fenceMatch = fenceRegex.exec(rawContent)) !== null) {
    candidates.push({ json: fenceMatch[1], fullMatch: fenceMatch[0] });
  }
  for (const candidate of candidates) {
    try {
      const parsed = JSON.parse(candidate.json);
      if (!parsed || typeof parsed !== "object") continue;
      const handoff = typeof parsed.handoff_message === "string" ? parsed.handoff_message.trim() : "";
      if (!handoff) continue;
      const explicitResponse = typeof parsed.response === "string" ? parsed.response.trim() : typeof parsed.final_response === "string" ? parsed.final_response.trim() : "";
      let response = explicitResponse;
      if (!response && candidate.fullMatch) {
        response = rawContent.replace(candidate.fullMatch, "").trim();
      }
      if (!response && !candidate.fullMatch) {
        response = "";
      }
      return {
        response,
        handoffMessage: handoff
      };
    } catch {
    }
  }
  return { response: rawContent };
}
var init_handoffMessage = __esm({
  "src/handoffMessage.ts"() {
    "use strict";
  }
});

// src/subAgentToolCallParser.ts
function isRecord(value) {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
function sanitizeContent(text3) {
  return text3.replace(/<\|tool_call\>/gi, "").replace(/<tool_call\|>/gi, "").replace(/<\|.*?\|>/g, "").replace(/<antThinking[^>]*>[\s\S]*?(?:<\/antThinking>|$)/gi, "").replace(/<thinking[^>]*>[\s\S]*?(?:<\/thinking>|$)/gi, "").replace(/^Thought:[\s\S]*?(?:\n\n|\r\n\r\n|\n|$)/, "").replace(/^Thought for [\d.]+ seconds?\s*/i, "").trim();
}
function normalizeContent(content) {
  if (typeof content === "string") return content;
  if (isRecord(content)) {
    const text3 = content.text;
    if (typeof text3 === "string") return text3;
    const nested = content.content;
    if (typeof nested === "string") return nested;
  }
  if (!Array.isArray(content)) return "";
  const chunks = [];
  for (const part of content) {
    if (typeof part === "string") {
      chunks.push(part);
      continue;
    }
    if (!isRecord(part)) continue;
    const text3 = part.text;
    if (typeof text3 === "string") {
      chunks.push(text3);
      continue;
    }
    const nested = part.content;
    if (typeof nested === "string") {
      chunks.push(nested);
    }
  }
  return chunks.join("\n");
}
function normalizeToolName(value) {
  if (typeof value !== "string") return null;
  let normalized = value.trim().toLowerCase();
  if (!normalized) return null;
  if (normalized.startsWith("functions.")) {
    normalized = normalized.slice("functions.".length);
  }
  const mapping = {
    "write_file": "save_file",
    "savefile": "save_file",
    "create_file": "save_file",
    "overwrite_file": "save_file",
    "readfile": "read_file",
    "list_dir": "list_directory",
    "ls": "list_directory",
    "find_file": "find_files",
    "search_file": "search_file_content",
    "grep": "search_file_content",
    "replace_text": "replace_text_in_file",
    "replace_in_file": "replace_text_in_file"
  };
  return mapping[normalized] || normalized;
}
function tryParseJson(text3) {
  try {
    return JSON.parse(text3);
  } catch {
    return void 0;
  }
}
function normalizeArgs(toolName, args) {
  let normalized = args;
  if (toolName === "save_file" && Array.isArray(normalized)) {
    normalized = { files: normalized };
  }
  if (!isRecord(normalized)) {
    return {};
  }
  const result2 = { ...normalized };
  const fileTools = [
    "read_file",
    "save_file",
    "replace_text_in_file",
    "read_file_range",
    "search_file_content",
    "search_in_file",
    "insert_at_line",
    "append_file",
    "delete_lines_in_file"
  ];
  if (fileTools.includes(toolName)) {
    if (typeof result2.path === "string" && result2.file_name === void 0) {
      result2.file_name = result2.path;
    }
    if (typeof result2.file_path === "string" && result2.file_name === void 0) {
      result2.file_name = result2.file_path;
    }
    if (typeof result2.name === "string" && result2.file_name === void 0) {
      result2.file_name = result2.name;
    }
  }
  if (["save_file", "append_file", "insert_at_line"].includes(toolName)) {
    if (typeof result2.data === "string" && result2.content === void 0) {
      result2.content = result2.data;
    }
    if (toolName === "insert_at_line" && typeof result2.content === "string" && result2.content_to_insert === void 0) {
      result2.content_to_insert = result2.content;
    }
  }
  if (toolName === "fuzzy_find_local_files" && !result2.query && result2.pattern) {
    result2.query = result2.pattern;
  }
  if ((toolName === "search_file_content" || toolName === "search_in_file") && !result2.pattern && result2.query) {
    result2.pattern = result2.query;
  }
  return result2;
}
function buildToolCall(toolName, args) {
  const normalizedName = normalizeToolName(toolName);
  if (!normalizedName) return null;
  return {
    tool: normalizedName,
    args: normalizeArgs(normalizedName, args)
  };
}
function isMatchingBracket(open, close) {
  return open === "{" && close === "}" || open === "[" && close === "]";
}
function extractBalancedJsonSnippets(text3, maxSnippets = 12) {
  const snippets = [];
  let iterations = 0;
  const MAX_ITERATIONS = 1e6;
  for (let start = 0; start < text3.length; start++) {
    if (iterations > MAX_ITERATIONS) break;
    const opener = text3[start];
    if (opener !== "{" && opener !== "[") continue;
    const stack = [opener];
    let inString = false;
    let escaped = false;
    let invalid = false;
    const endLimit = Math.min(text3.length, start + 1e5);
    for (let end = start + 1; end < endLimit; end++) {
      iterations++;
      if (iterations > MAX_ITERATIONS) break;
      const char = text3[end];
      if (inString) {
        if (escaped) {
          escaped = false;
        } else if (char === "\\") {
          escaped = true;
        } else if (char === '"') {
          inString = false;
        }
        continue;
      }
      if (char === '"') {
        inString = true;
        continue;
      }
      if (char === "{" || char === "[") {
        stack.push(char);
        continue;
      }
      if (char === "}" || char === "]") {
        const currentOpen = stack.pop();
        if (!currentOpen || !isMatchingBracket(currentOpen, char)) {
          invalid = true;
          break;
        }
        if (stack.length === 0) {
          snippets.push(text3.slice(start, end + 1));
          start = end;
          break;
        }
      }
    }
    if (invalid) continue;
    if (snippets.length >= maxSnippets) break;
  }
  return snippets;
}
function extractJsonCandidates(text3) {
  const candidates = [];
  const seen = /* @__PURE__ */ new Set();
  const pushCandidate = (value) => {
    const trimmed2 = value.trim();
    if (!trimmed2 || seen.has(trimmed2)) return;
    seen.add(trimmed2);
    candidates.push(trimmed2);
  };
  const fencedRegex = /```(?:json|javascript|js|ts|python|py)?\s*([\s\S]*?)```/gi;
  let fenceMatch;
  while ((fenceMatch = fencedRegex.exec(text3)) !== null) {
    pushCandidate(fenceMatch[1]);
  }
  const trimmed = text3.trim();
  if (trimmed.startsWith("{") && trimmed.endsWith("}") || trimmed.startsWith("[") && trimmed.endsWith("]")) {
    pushCandidate(trimmed);
  }
  for (const snippet of extractBalancedJsonSnippets(text3)) {
    pushCandidate(snippet);
  }
  return candidates;
}
function parseToolCallFromToolCalls(toolCalls) {
  if (!Array.isArray(toolCalls)) return null;
  for (const entry of toolCalls) {
    if (!isRecord(entry)) continue;
    const fn = entry.function;
    if (isRecord(fn)) {
      let args = fn.arguments;
      if (typeof args === "string") {
        args = tryParseJson(args) ?? {};
      }
      const parsed = buildToolCall(fn.name, args);
      if (parsed) return parsed;
    }
    let fallbackArgs = entry.arguments;
    if (typeof fallbackArgs === "string") {
      fallbackArgs = tryParseJson(fallbackArgs) ?? {};
    }
    const fallback = buildToolCall(entry.name, fallbackArgs);
    if (fallback) return fallback;
  }
  return null;
}
function findMatchingBrace(text3, openBraceIndex) {
  let depth = 0;
  let inString = false;
  let quote = '"';
  let escaped = false;
  for (let i = openBraceIndex; i < text3.length; i++) {
    const ch = text3[i];
    if (inString) {
      if (escaped) {
        escaped = false;
      } else if (ch === "\\") {
        escaped = true;
      } else if (ch === quote) {
        inString = false;
      }
      continue;
    }
    if (ch === '"' || ch === "'") {
      inString = true;
      quote = ch;
      continue;
    }
    if (ch === "{") {
      depth++;
      continue;
    }
    if (ch === "}") {
      depth--;
      if (depth === 0) return i;
    }
  }
  return -1;
}
function parseLooseObject(insideBraces) {
  let normalized = insideBraces.trim();
  if (!normalized) return {};
  normalized = normalized.replace(/(^|[{,]\s*)([a-zA-Z_][\w-]*)\s*:/g, '$1"$2":');
  normalized = normalized.replace(/'([^'\\]*(?:\\.[^'\\]*)*)'/g, (_match, inner) => {
    const escapedInner = inner.replace(/\\'/g, "'").replace(/"/g, '\\"');
    return `"${escapedInner}"`;
  });
  const parsed = tryParseJson(`{${normalized}}`);
  return isRecord(parsed) ? parsed : null;
}
function parseToolCallFromLegacySyntax(text3) {
  const callRegex = /call\s*:\s*([a-zA-Z0-9_.-]+)\s*\{/gi;
  let match;
  while ((match = callRegex.exec(text3)) !== null) {
    const toolName = match[1];
    const openBraceIndex = text3.indexOf("{", match.index + match[0].length - 1);
    if (openBraceIndex < 0) continue;
    const closeBraceIndex = findMatchingBrace(text3, openBraceIndex);
    if (closeBraceIndex < 0) continue;
    const body = text3.slice(openBraceIndex + 1, closeBraceIndex);
    const strictParsed = tryParseJson(`{${body}}`);
    const parsedArgs = isRecord(strictParsed) ? strictParsed : parseLooseObject(body);
    if (!parsedArgs) continue;
    const parsed = buildToolCall(toolName, parsedArgs);
    if (parsed) return parsed;
  }
  return null;
}
function parseToolCallObject(candidate, originalText) {
  if (Array.isArray(candidate)) {
    if (candidate.length > 0 && candidate.every((item) => isRecord(item))) {
      const asBatchSave = buildToolCall("save_file", candidate);
      if (asBatchSave) return asBatchSave;
    }
    for (const item of candidate) {
      const parsed = parseToolCallObject(item, originalText);
      if (parsed) return parsed;
    }
    return null;
  }
  if (!isRecord(candidate)) return null;
  const nestedToolCalls = parseToolCallFromToolCalls(candidate.tool_calls);
  if (nestedToolCalls) return nestedToolCalls;
  if ("tool" in candidate && "args" in candidate) {
    const parsed = buildToolCall(candidate.tool, candidate.args);
    if (parsed) return parsed;
  }
  if ("tool" in candidate && "parameters" in candidate) {
    const parsed = buildToolCall(candidate.tool, candidate.parameters);
    if (parsed) return parsed;
  }
  if ("function" in candidate && "parameters" in candidate) {
    let args = candidate.parameters;
    if (typeof args === "string") {
      args = tryParseJson(args) ?? {};
    }
    const parsed = buildToolCall(candidate.function, args);
    if (parsed) return parsed;
  }
  if ("function" in candidate && "arguments" in candidate) {
    let args = candidate.arguments;
    if (typeof args === "string") {
      args = tryParseJson(args) ?? {};
    }
    const parsed = buildToolCall(candidate.function, args);
    if (parsed) return parsed;
  }
  if ("name" in candidate && "arguments" in candidate) {
    let args = candidate.arguments;
    if (typeof args === "string") {
      args = tryParseJson(args) ?? {};
    }
    const parsed = buildToolCall(candidate.name, args);
    if (parsed) return parsed;
  }
  if (typeof candidate.file_name === "string" && typeof candidate.content === "string" || typeof candidate.path === "string" && typeof candidate.data === "string") {
    const parsed = buildToolCall("save_file", candidate);
    if (parsed) return parsed;
  }
  const toToolNameMatch = originalText.match(/to=([a-zA-Z0-9_.-]+)/);
  if (toToolNameMatch) {
    const parsed = buildToolCall(toToolNameMatch[1], candidate);
    if (parsed) return parsed;
  }
  return null;
}
function parseToolCallFromContent(text3) {
  if (!text3.trim()) return null;
  const legacyCall = parseToolCallFromLegacySyntax(text3);
  if (legacyCall) return legacyCall;
  for (const candidateText of extractJsonCandidates(text3)) {
    const parsedJson = tryParseJson(candidateText);
    if (parsedJson === void 0) continue;
    const parsedTool = parseToolCallObject(parsedJson, text3);
    if (parsedTool) return parsedTool;
  }
  const toolMatch = text3.match(/\{"[\s]*tool[\s]*"[\s]*:[\s]*"([a-zA-Z0-9_.-]+)"/);
  if (toolMatch) {
    const argsStartIdx = text3.indexOf("{", toolMatch.index || 0);
    if (argsStartIdx >= 0) {
      const closeBraceIdx = findMatchingBrace(text3, argsStartIdx);
      if (closeBraceIdx > 0) {
        const jsonSnippet = text3.slice(argsStartIdx, closeBraceIdx + 1);
        const parsedJson = tryParseJson(jsonSnippet);
        if (parsedJson && isRecord(parsedJson)) {
          const parsedTool = parseToolCallObject(parsedJson, text3);
          if (parsedTool) return parsedTool;
        }
      }
    }
  }
  return null;
}
function parseSubAgentResponseMessage(message) {
  if (!isRecord(message)) {
    const content2 = sanitizeContent(typeof message === "string" ? message : "");
    const contentToolCall2 = parseToolCallFromContent(content2);
    return {
      content: content2,
      toolCall: contentToolCall2,
      toolCallSource: contentToolCall2 ? "content" : "none"
    };
  }
  const content = sanitizeContent(normalizeContent(message.content));
  const reasoningContent = sanitizeContent(
    normalizeContent(message.reasoning_content ?? message.reasoning ?? message.thinking ?? "")
  );
  const structuredToolCall = parseToolCallFromToolCalls(message.tool_calls) || parseToolCallFromToolCalls(message.calls) || parseToolCallFromToolCalls(message.function_call ? [message.function_call] : void 0);
  if (structuredToolCall) {
    return {
      content,
      toolCall: structuredToolCall,
      toolCallSource: "tool_calls"
    };
  }
  const contentToolCall = parseToolCallFromContent(content);
  if (contentToolCall) {
    return {
      content,
      toolCall: contentToolCall,
      toolCallSource: "content"
    };
  }
  const reasoningToolCall = parseToolCallFromContent(reasoningContent);
  if (reasoningToolCall) {
    return {
      content,
      toolCall: reasoningToolCall,
      toolCallSource: "reasoning"
    };
  }
  return {
    content,
    toolCall: null,
    toolCallSource: "none"
  };
}
var init_subAgentToolCallParser = __esm({
  "src/subAgentToolCallParser.ts"() {
    "use strict";
  }
});

// src/toolCallValidator.ts
function validateToolCall(toolName, args = {}) {
  let toolValidationError = null;
  if (toolName === "finish_task") {
    return null;
  }
  if (toolName === "save_file") {
    if (Array.isArray(args.files)) {
      for (const file of args.files) {
        const fileName2 = file.file_name || file.name || file.path;
        const fileContent2 = file.content || file.data;
        if (!fileName2 && !fileContent2) {
          return `Tool 'save_file' batch mode requires [file_name, content] in all objects.`;
        } else if (!fileName2) {
          return `Tool 'save_file' batch missing 'file_name'. Hint: Use 'file_name'.`;
        } else if (!fileContent2) {
          return `Tool 'save_file' batch missing 'content'. Hint: Use 'content'.`;
        } else if ((0, import_path4.isAbsolute)(fileName2)) {
          return `Tool 'save_file' batch rejected absolute path: '${fileName2}'. SECURITY: Files can only be saved within workspace.`;
        }
      }
      return null;
    }
    const fileName = args.file_name || args.name || args.path;
    const fileContent = args.content || args.data;
    if (!fileName && fileContent === void 0) {
      toolValidationError = `Tool 'save_file' requires parameters: [file_name, content]. Provided keys: ${Object.keys(args).join(", ") || "none"}.`;
    } else if (!fileName) {
      toolValidationError = `Tool 'save_file' missing required parameter: 'file_name'.`;
    } else if (fileContent === void 0 || fileContent === null) {
      toolValidationError = `Tool 'save_file' missing required parameter: 'content'.`;
    } else if ((0, import_path4.isAbsolute)(fileName)) {
      toolValidationError = `Tool 'save_file' rejected absolute path: '${fileName}'. SECURITY: Files can only be saved within workspace. Use relative path like 'test.html'.`;
    }
  }
  if (toolName === "read_file") {
    const fileName = args.file_name || args.path || args.name;
    if (!fileName) {
      toolValidationError = `Tool 'read_file' requires parameter: [file_name]. Provided keys: ${Object.keys(args).join(", ") || "none"}. Hint: Use 'file_name' (not 'path', 'filepath', or 'file_path').`;
    } else if ((0, import_path4.isAbsolute)(fileName)) {
      toolValidationError = `Tool 'read_file' rejected absolute path. SECURITY: Only workspace paths allowed.`;
    }
  }
  if (toolName === "replace_text_in_file") {
    const fileName = args.file_name || args.path || args.name;
    const missing = [];
    if (!fileName) missing.push("file_name");
    if (!args.old_string) missing.push("old_string");
    if (!args.new_string) missing.push("new_string");
    if (missing.length > 0) {
      toolValidationError = `Tool 'replace_text_in_file' missing parameters: [${missing.join(", ")}]. Provided keys: ${Object.keys(args).join(", ") || "none"}.`;
    } else if ((0, import_path4.isAbsolute)(fileName)) {
      toolValidationError = `Tool 'replace_text_in_file' rejected absolute path. SECURITY: Only workspace paths allowed.`;
    }
  }
  if (toolName === "multi_replace_text") {
    const fileName = args.file_name || args.path || args.name;
    if (!fileName) {
      toolValidationError = `Tool 'multi_replace_text' missing parameter: 'file_name'.`;
    } else if ((0, import_path4.isAbsolute)(fileName)) {
      toolValidationError = `Tool 'multi_replace_text' rejected absolute path. SECURITY: Only workspace paths allowed.`;
    } else if (!Array.isArray(args.replacements) || args.replacements.length === 0) {
      toolValidationError = `Tool 'multi_replace_text' requires an array 'replacements' with at least one replacement object.`;
    } else {
      for (let i = 0; i < args.replacements.length; i++) {
        const rep = args.replacements[i];
        if (!rep.start_line || !rep.end_line || !rep.old_string || typeof rep.new_string !== "string") {
          toolValidationError = `Tool 'multi_replace_text' replacements[${i}] missing required fields (start_line, end_line, old_string, new_string).`;
          break;
        }
      }
    }
  }
  return toolValidationError;
}
var import_path4;
var init_toolCallValidator = __esm({
  "src/toolCallValidator.ts"() {
    "use strict";
    import_path4 = require("path");
  }
});

// src/backgroundCommands.ts
function generateId() {
  return (0, import_crypto.randomBytes)(8).toString("hex");
}
var import_crypto, backgroundCommands;
var init_backgroundCommands = __esm({
  "src/backgroundCommands.ts"() {
    "use strict";
    import_crypto = require("crypto");
    backgroundCommands = /* @__PURE__ */ new Map();
  }
});

// src/extractorScript.ts
var EXTRACTION_SCRIPT;
var init_extractorScript = __esm({
  "src/extractorScript.ts"() {
    "use strict";
    EXTRACTION_SCRIPT = `"""Conservative static extraction. Never imports or executes the candidate.\r
\r
Values are abstract. A value is either a statically known Python literal\r
(str/int/float/bool/None, a dict with string keys, a list), an Opaque runtime\r
value (optionally with a statically evident Python type), or a Template: a\r
string whose literal parts are known and whose holes are runtime values, such\r
as f"https://host/users/{user_id}". Unknown values are never guessed, and a\r
container that is changed in a way the analysis cannot follow becomes Opaque\r
rather than keeping a stale value.\r
\r
Each extraction issue lists the verification layers whose claim inventory it\r
can make incomplete ("affects"). Other layers keep their evidence.\r
"""\r
import ast\r
import builtins\r
import io\r
import json\r
import string\r
import sys\r
import tokenize\r
import types\r
import urllib.parse\r
\r
payload = json.load(sys.stdin)\r
code = payload.get('code', '')\r
bindings = payload.get('input_bindings', {}) or {}\r
\r
ALL = ['interface', 'identifier', 'access_point', 'input_contract', 'output_contract', 'contextual']\r
API = ['access_point', 'input_contract', 'output_contract', 'contextual']\r
REQUEST = ['input_contract', 'contextual']\r
RESPONSE = ['output_contract']\r
IDENTIFIER = ['identifier']\r
\r
HTTP = {'get', 'post', 'put', 'patch', 'delete', 'head', 'options'}\r
# requests.<verb>(url, <positional>...) as defined by requests.api.\r
POSITIONAL = {'get': ['params'], 'post': ['data', 'json'], 'put': ['data'], 'patch': ['data'],\r
              'delete': [], 'head': [], 'options': [], 'request': []}\r
REQUEST_KWARGS = {'url', 'method', 'params', 'json', 'data', 'headers', 'cookies', 'auth',\r
                  'timeout', 'allow_redirects', 'verify', 'stream', 'proxies', 'cert'}\r
OTHER_HTTP_CLIENTS = ('httpx.', 'aiohttp.', 'urllib.request.', 'urllib3.', 'http.client.', 'pycurl.')\r
# Calls that neither mutate their arguments nor perform HTTP requests.\r
PURE = {\r
    'print', 'len', 'str', 'int', 'float', 'bool', 'bytes', 'bytearray', 'complex', 'frozenset',\r
    'object', 'slice', 'memoryview', 'format', 'isinstance', 'issubclass', 'hasattr', 'callable',\r
    'type', 'id', 'repr', 'hash', 'dir', 'list', 'dict', 'set', 'tuple', 'range', 'enumerate',\r
    'zip', 'iter', 'next', 'reversed', 'sorted', 'min', 'max', 'sum', 'abs', 'round', 'pow',\r
    'divmod', 'bin', 'hex', 'oct', 'chr', 'ord', 'any', 'all', 'super', 'property',\r
    'classmethod', 'staticmethod',\r
    'json.dumps', 'json.loads', 'json.dump', 'os.getenv', 'os.environ.get',\r
    'urllib.parse.quote', 'urllib.parse.quote_plus', 'urllib.parse.unquote',\r
    'urllib.parse.urlencode', 'urllib.parse.urljoin', 'urllib.parse.urlparse',\r
    'time.sleep', 'time.time', 'sys.exit', 'logging.debug', 'logging.info', 'logging.warning',\r
    'logging.error', 'logging.exception', 'logging.critical', 'logging.getLogger',\r
    'datetime.datetime.now', 'datetime.date.today',\r
}\r
BUILTIN_EXCEPTIONS = {n for n in dir(builtins) if n.endswith(('Error', 'Exception', 'Warning', 'Exit', 'Interrupt'))}\r
MUTATORS = {'update', 'setdefault', 'pop', 'popitem', 'clear', 'append', 'extend', 'insert', 'remove', 'sort', 'reverse'}\r
DYNAMIC_CODE = {'getattr', 'setattr', 'delattr', 'eval', 'exec', 'compile', '__import__', 'globals', 'importlib.import_module'}\r
\r
claims, issues, unused_parameters = [], [], []\r
\r
\r
class Opaque:\r
    """A runtime value. type is a statically evident Python type name, if any."""\r
    __slots__ = ('label', 'type')\r
\r
    def __init__(self, label='', type_=None):\r
        self.label, self.type = label, type_\r
\r
    def __eq__(self, other):\r
        return isinstance(other, Opaque) and other.label == self.label and other.type == self.type\r
\r
    __hash__ = None\r
\r
\r
class Template:\r
    """A string with known literal parts and Opaque holes."""\r
    __slots__ = ('parts',)\r
\r
    def __init__(self, parts):\r
        self.parts = tuple(parts)\r
\r
    def __eq__(self, other):\r
        return isinstance(other, Template) and other.parts == self.parts\r
\r
    __hash__ = None\r
\r
\r
class Maybe:\r
    """A dict entry that is present on some control-flow paths only, e.g. an optional\r
    query parameter added inside an if. The key is known; its presence is not."""\r
    __slots__ = ('value',)\r
\r
    def __init__(self, value):\r
        self.value = value\r
\r
    def __eq__(self, other):\r
        return isinstance(other, Maybe) and other.value == self.value\r
\r
    __hash__ = None\r
\r
\r
def present(value):\r
    """The value a dict entry holds when it is present."""\r
    return value.value if isinstance(value, Maybe) else value\r
\r
\r
def join_values(values, name):\r
    """Join the values one variable has at the end of several branches."""\r
    first = values[0]\r
    if all(v == first for v in values[1:]):\r
        return first\r
    if all(isinstance(v, dict) for v in values):\r
        # Key-wise, so an entry added on one branch does not make the whole dict unknown.\r
        keys = []\r
        for v in values:\r
            keys.extend(k for k in v if k not in keys)\r
        joined = {}\r
        for k in keys:\r
            held = [v[k] for v in values if k in v]\r
            value = join_values([present(h) for h in held], k)\r
            joined[k] = Maybe(value) if len(held) < len(values) or any(isinstance(h, Maybe) for h in held) else value\r
        return joined\r
    types = {type_of(v) for v in values}\r
    return Opaque(name, types.pop() if len(types) == 1 else None)\r
\r
\r
AMBIGUOUS = object()  # provenance that differs across control-flow paths\r
MISSING = object()\r
\r
\r
def make_string(parts):\r
    """Normalise parts (str, Template, Opaque) into a str or a Template."""\r
    flat = []\r
    for part in parts:\r
        if isinstance(part, Template):\r
            flat.extend(part.parts)\r
        elif isinstance(part, str):\r
            flat.append(part)\r
        else:\r
            flat.append(part if isinstance(part, Opaque) else Opaque(str(part)))\r
    merged = []\r
    for part in flat:\r
        if isinstance(part, str) and merged and isinstance(merged[-1], str):\r
            merged[-1] += part\r
        elif part != '':\r
            merged.append(part)\r
    if all(isinstance(p, str) for p in merged):\r
        return ''.join(merged)\r
    return Template(merged)\r
\r
\r
def label(node):\r
    try:\r
        text = ast.unparse(node)\r
    except Exception:  # pragma: no cover - defensive\r
        text = type(node).__name__\r
    return text if len(text) <= 80 else text[:77] + '...'\r
\r
\r
def issue(node, reason, affects=None):\r
    item = {'line': getattr(node, 'lineno', 0), 'reason': reason, 'affects': list(affects or ALL)}\r
    if not any(i['line'] == item['line'] and i['reason'] == reason for i in issues):\r
        issues.append(item)\r
\r
\r
def add(node, kind, **fields):\r
    result = {'id': 'claim_%s' % (len(claims) + 1), 'type': kind, 'line': getattr(node, 'lineno', 0), **fields}\r
    claims.append(result)\r
    return result\r
\r
\r
def known(value):\r
    if isinstance(value, (Opaque, Template, Maybe)):\r
        return False\r
    if isinstance(value, dict):\r
        return all(known(v) for v in value.values())\r
    if isinstance(value, (list, tuple)):\r
        return all(known(v) for v in value)\r
    return True\r
\r
\r
def public(value):\r
    return encode(value) if known(value) else None\r
\r
\r
def encode(value):\r
    """JSON form of an abstract value; unknown parts are explicit markers."""\r
    if isinstance(value, Opaque):\r
        return {'$ca': 'unknown', 'label': value.label, 'type': value.type}\r
    if isinstance(value, Maybe):\r
        return {'$ca': 'maybe', 'value': encode(value.value)}\r
    if isinstance(value, Template):\r
        return {'$ca': 'template', 'parts': [p if isinstance(p, str) else {'hole': p.label} for p in value.parts]}\r
    if isinstance(value, dict):\r
        return {k: encode(v) for k, v in value.items()}\r
    if isinstance(value, (list, tuple)):\r
        return [encode(v) for v in value]\r
    if isinstance(value, (str, int, float, bool)) or value is None:\r
        return value\r
    return {'$ca': 'unknown', 'label': repr(value)[:80], 'type': type(value).__name__}\r
\r
\r
def type_of(value):\r
    if isinstance(value, Maybe):\r
        return type_of(value.value)\r
    if isinstance(value, Opaque):\r
        return value.type\r
    if isinstance(value, Template):\r
        return 'str'\r
    return type(value).__name__\r
\r
\r
def origin_known(url):\r
    """True when a Template's scheme and host are literal."""\r
    if not isinstance(url, Template) or not url.parts or not isinstance(url.parts[0], str):\r
        return False\r
    head = url.parts[0]\r
    if '://' not in head:\r
        return False\r
    rest = head.split('://', 1)[1]\r
    return any(c in rest for c in '/?#') and rest.split('/')[0].split('?')[0] != ''\r
\r
\r
def copy_value(value):\r
    if isinstance(value, dict):\r
        return {k: copy_value(v) for k, v in value.items()}\r
    if isinstance(value, list):\r
        return [copy_value(v) for v in value]\r
    return value\r
\r
\r
def assigned_names(nodes):\r
    """Names (re)bound or mutated anywhere inside the statements."""\r
    names = set()\r
    for stmt in nodes:\r
        for n in ast.walk(stmt):\r
            if isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):\r
                names.add(n.id)\r
            elif isinstance(n, (ast.Subscript, ast.Attribute)) and isinstance(n.ctx, (ast.Store, ast.Del)):\r
                root = n\r
                while isinstance(root, (ast.Subscript, ast.Attribute)):\r
                    root = root.value\r
                if isinstance(root, ast.Name):\r
                    names.add(root.id)\r
            elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in MUTATORS \\\r
                    and isinstance(n.func.value, ast.Name):\r
                names.add(n.func.value.id)\r
            elif isinstance(n, (ast.Global, ast.Nonlocal)):\r
                names.update(n.names)\r
    return names\r
\r
\r
class Context:\r
    def __init__(self):\r
        self.calls = {}           # id(ast.Call) -> call_id for HTTP requests\r
        self.functions = {}       # module-level function name -> FunctionInfo\r
        self.module = None        # module-level Analyzer\r
\r
\r
class FunctionInfo:\r
    def __init__(self, node):\r
        self.node, self.done, self.running, self.summary = node, False, False, None\r
\r
\r
CTX = Context()\r
\r
\r
class Analyzer:\r
    def __init__(self, env=None, imports=None, provenance=None, local_functions=None):\r
        self.env = dict(env or {})\r
        self.imports = dict(imports or {})\r
        self.prov = dict(provenance or {})\r
        self.local_functions = dict(local_functions or {})\r
        self.returns = []\r
\r
    # ------------------------------------------------------------------ state\r
    def fork(self):\r
        child = Analyzer(self.env, self.imports, self.prov, self.local_functions)\r
        return child\r
\r
    def collect(self, *branches):\r
        for b in branches:\r
            if b is not None and b is not self:\r
                self.returns.extend(b.returns)\r
                b.returns = []\r
\r
    def join(self, branches, node):\r
        """Merge the end states of the branches that fall through."""\r
        live = [b for b in branches if b is not None]\r
        if not live:\r
            return\r
        if len(live) == 1:\r
            only = live[0]\r
            self.env, self.prov, self.imports = dict(only.env), dict(only.prov), dict(only.imports)\r
            self.local_functions = dict(only.local_functions)\r
            return\r
        env, prov = {}, {}\r
        for name in set().union(*(b.env.keys() for b in live)):\r
            values = [b.env.get(name, MISSING) for b in live]\r
            first = values[0]\r
            if first is not MISSING and all(v is not MISSING and v == first for v in values[1:]):\r
                env[name] = first\r
            elif MISSING not in values:\r
                env[name] = join_values(values, name)\r
            else:\r
                types = {type_of(v) for v in values if v is not MISSING}\r
                env[name] = Opaque(name, types.pop() if len(types) == 1 and MISSING not in values else None)\r
        for name in set().union(*(b.prov.keys() for b in live)):\r
            tracked = [b.prov.get(name) for b in live if b.prov.get(name) is not None]\r
            if any(t is AMBIGUOUS for t in tracked) or any(t != tracked[0] for t in tracked[1:]):\r
                # Reported where a field is read from it (scan, method_call, iteration), not here:\r
                # data that is never read further does not limit the extraction.\r
                prov[name] = AMBIGUOUS\r
            else:\r
                # May-alias: fields read later are checked against the response they may come from.\r
                prov[name] = tracked[0]\r
        self.env, self.prov = env, prov\r
        self.imports = dict(live[0].imports)\r
        for b in live[1:]:\r
            for k in list(self.imports):\r
                if b.imports.get(k) != self.imports[k]:\r
                    self.imports.pop(k)\r
\r
    def havoc(self, names, keep_provenance=True):\r
        for name in names:\r
            self.env[name] = Opaque(name)\r
            self.imports.pop(name, None)\r
            if not keep_provenance:\r
                self.prov.pop(name, None)\r
\r
    # ------------------------------------------------------------- resolution\r
    def qualified(self, node):\r
        if isinstance(node, ast.Name):\r
            if node.id in self.env and node.id not in self.imports:\r
                return ''\r
            return self.imports.get(node.id, node.id)\r
        if isinstance(node, ast.Attribute):\r
            base = self.qualified(node.value)\r
            return base + '.' + node.attr if base else ''\r
        return ''\r
\r
    def function_info(self, name):\r
        info = self.local_functions.get(name)\r
        if info is None and name not in self.env and name not in self.imports:\r
            info = CTX.functions.get(name)\r
        return info\r
\r
    def ensure_analyzed(self, info):\r
        if info.done or info.running:\r
            return\r
        module = CTX.module\r
        self.analyze_function(info, module.env if module else self.env, module.imports if module else self.imports, module.prov if module else self.prov)\r
\r
    def analyze_function(self, info, env, imports, provenance=None):\r
        """Analyze a body once; globals/closure values and response provenance are visible."""\r
        node = info.node\r
        info.running = True\r
        child = Analyzer(env, imports, provenance, self.local_functions)\r
        all_args = node.args.posonlyargs + node.args.args + node.args.kwonlyargs\r
        extra = [a for a in (node.args.vararg, node.args.kwarg) if a is not None]\r
        for arg in all_args + extra:\r
            child.env[arg.arg] = copy_value(bindings[arg.arg]) if arg.arg in bindings else Opaque(arg.arg)\r
            child.imports.pop(arg.arg, None)\r
            child.prov.pop(arg.arg, None)\r
        record_unused_parameters(node, all_args)\r
        if isinstance(node, ast.AsyncFunctionDef):\r
            issue(node, 'Async functions are outside the supported extraction subset.', API)\r
        child.statements(node.body)\r
        tracked = [r for r in child.returns if r is not None]\r
        if any(r is AMBIGUOUS for r in tracked) or any(r != tracked[0] for r in tracked[1:]):\r
            # Different returned values (e.g. data['id'] on one branch, data['user']['id'] on\r
            # another). Only a caller reading fields from the result is limited, and that read\r
            # reports the ambiguity itself.\r
            info.summary = AMBIGUOUS\r
        else:\r
            info.summary = tracked[0] if tracked else None\r
        info.running, info.done = False, True\r
\r
    # ------------------------------------------------------------ evaluation\r
    def value(self, node):\r
        if node is None:\r
            return None\r
        if isinstance(node, ast.Constant):\r
            return node.value\r
        if isinstance(node, ast.Name):\r
            if node.id in self.env:\r
                return self.env[node.id]\r
            return Opaque(node.id)\r
        if isinstance(node, ast.Dict):\r
            result = {}\r
            for k, v in zip(node.keys, node.values):\r
                if k is None:\r
                    spread = self.value(v)\r
                    if isinstance(spread, dict):\r
                        result.update(spread)\r
                        continue\r
                    return Opaque(label(node), 'dict')\r
                key = self.value(k)\r
                if not isinstance(key, str):\r
                    return Opaque(label(node), 'dict')\r
                result[key] = self.value(v)\r
            return result\r
        if isinstance(node, (ast.List, ast.Tuple)):\r
            if any(isinstance(e, ast.Starred) for e in node.elts):\r
                return Opaque(label(node), 'list')\r
            return [self.value(v) for v in node.elts]\r
        if isinstance(node, ast.Subscript):\r
            obj, key = self.value(node.value), self.value(node.slice)\r
            if isinstance(obj, (dict, list, str)) and known(key) and not isinstance(node.slice, ast.Slice):\r
                try:\r
                    return present(obj[key])\r
                except (KeyError, IndexError, TypeError):\r
                    pass\r
            return Opaque(label(node))\r
        if isinstance(node, ast.BinOp):\r
            left, right = self.value(node.left), self.value(node.right)\r
            if isinstance(node.op, ast.Add):\r
                if isinstance(left, (str, Template)) or isinstance(right, (str, Template)):\r
                    if isinstance(left, (int, float, bool, list, dict)) or isinstance(right, (int, float, bool, list, dict)):\r
                        return Opaque(label(node))  # a TypeError at runtime; not a URL\r
                    return make_string([left, right])\r
            if isinstance(node.op, ast.Mod) and isinstance(left, str) and known(right):\r
                try:\r
                    return left % (tuple(right) if isinstance(right, list) else right)\r
                except (TypeError, ValueError, KeyError):\r
                    return Opaque(label(node), 'str')\r
            if known(left) and known(right) and isinstance(left, (int, float)) and isinstance(right, (int, float)):\r
                try:\r
                    return eval_binop(node.op, left, right)\r
                except Exception:\r
                    pass\r
            if isinstance(left, (str, Template)) and isinstance(node.op, ast.Mod):\r
                return Opaque(label(node), 'str')\r
            return Opaque(label(node))\r
        if isinstance(node, ast.JoinedStr):\r
            parts = []\r
            for part in node.values:\r
                if isinstance(part, ast.Constant):\r
                    parts.append(part.value)\r
                elif isinstance(part, ast.FormattedValue):\r
                    val = self.value(part.value)\r
                    plain = part.format_spec is None and part.conversion == -1\r
                    if plain and isinstance(val, (str, Template)):\r
                        parts.append(val)\r
                    elif plain and (val is None or isinstance(val, (int, float, bool))):\r
                        parts.append(str(val))\r
                    else:\r
                        parts.append(Opaque(label(part.value), 'str'))\r
            return make_string(parts)\r
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):\r
            v = self.value(node.operand)\r
            if isinstance(v, (int, float)) and not isinstance(v, bool):\r
                return -v if isinstance(node.op, ast.USub) else v\r
            return Opaque(label(node))\r
        if isinstance(node, ast.IfExp):\r
            a, b = self.value(node.body), self.value(node.orelse)\r
            return a if a == b else Opaque(label(node), type_of(a) if type_of(a) == type_of(b) else None)\r
        if isinstance(node, ast.NamedExpr):\r
            return self.value(node.value)\r
        if isinstance(node, ast.Compare):\r
            return Opaque(label(node), 'bool')\r
        if isinstance(node, (ast.ListComp, ast.GeneratorExp)):\r
            return Opaque(label(node), 'list')\r
        if isinstance(node, ast.DictComp):\r
            return Opaque(label(node), 'dict')\r
        if isinstance(node, ast.Call):\r
            return self.call_value(node)\r
        return Opaque(label(node))\r
\r
    def call_value(self, node):\r
        """Pure evaluation of a call's result. Side effects are handled by scan()."""\r
        if id(node) in CTX.calls:\r
            return Opaque(label(node), 'requests.Response')\r
        name = self.qualified(node.func)\r
        args = [self.value(a) for a in node.args]\r
        kwargs = {kw.arg: self.value(kw.value) for kw in node.keywords if kw.arg}\r
        if name == 'str' and len(args) == 1:\r
            v = args[0]\r
            if isinstance(v, (str, Template)):\r
                return v\r
            if known(v) and isinstance(v, (int, float, bool)) or v is None:\r
                return str(v)\r
            return Opaque(label(node.args[0]), 'str')\r
        if name in ('int', 'float', 'bool') and len(args) == 1:\r
            if known(args[0]):\r
                try:\r
                    return {'int': int, 'float': float, 'bool': bool}[name](args[0])\r
                except (TypeError, ValueError):\r
                    pass\r
            return Opaque(label(node), name)\r
        if name in ('requests.Session', 'requests.session', 'requests.sessions.Session'):\r
            return Opaque(label(node), 'requests.Session')\r
        if name in ('requests.auth.HTTPBasicAuth', 'requests.HTTPBasicAuth'):\r
            return Opaque(label(node), 'requests.auth.HTTPBasicAuth')\r
        if name == 'len':\r
            return Opaque(label(node), 'int')\r
        if name == 'dict' and not args:\r
            return kwargs if all(kw.arg for kw in node.keywords) else Opaque(label(node), 'dict')\r
        if name in ('urllib.parse.quote', 'urllib.parse.quote_plus', 'requests.utils.quote'):\r
            if args and isinstance(args[0], str):\r
                safe = kwargs.get('safe', args[1] if len(args) > 1 else '/')\r
                fn = urllib.parse.quote_plus if name.endswith('quote_plus') else urllib.parse.quote\r
                return fn(args[0], safe=safe) if isinstance(safe, str) else Opaque(label(node), 'str')\r
            return Opaque(label(node.args[0]) if node.args else label(node), 'str')\r
        if name == 'urllib.parse.urlencode' and args and known(args[0]):\r
            try:\r
                return urllib.parse.urlencode(args[0])\r
            except (TypeError, ValueError):\r
                return Opaque(label(node), 'str')\r
        if name == 'urllib.parse.urljoin' and len(args) == 2 and all(isinstance(a, str) for a in args):\r
            return urllib.parse.urljoin(args[0], args[1])\r
        if name in ('os.getenv', 'os.environ.get'):\r
            return Opaque(label(node), 'str' if len(args) > 1 and isinstance(args[1], str) else None)\r
        if name in ('json.dumps',):\r
            return Opaque(label(node), 'str')\r
        if isinstance(node.func, ast.Attribute):\r
            receiver = self.value(node.func.value)\r
            method = node.func.attr\r
            if isinstance(receiver, dict) and method == 'get' and args and isinstance(args[0], str):\r
                default = args[1] if len(args) > 1 else kwargs.get('default')\r
                held = receiver.get(args[0], default)\r
                # An entry present on some paths only yields its value or the default.\r
                return held if not isinstance(held, Maybe) else held.value if held.value == default else Opaque(label(node))\r
            if isinstance(receiver, dict) and method == 'copy':\r
                return dict(receiver)\r
            if isinstance(receiver, str):\r
                return self.string_method(node, receiver, method, args, kwargs)\r
            if isinstance(receiver, Template):\r
                return self.template_method(node, receiver, method, args)\r
        return Opaque(label(node))\r
\r
    def string_method(self, node, receiver, method, args, kwargs):\r
        if method == 'replace' and len(args) >= 2 and isinstance(args[0], str) and args[0]:\r
            if isinstance(args[1], str):\r
                return receiver.replace(args[0], args[1])\r
            pieces = receiver.split(args[0])\r
            parts = [pieces[0]]\r
            for piece in pieces[1:]:\r
                parts.extend([args[1] if isinstance(args[1], (Template, Opaque)) else Opaque(label(node.args[1]), 'str'), piece])\r
            return make_string(parts)\r
        if method == 'format':\r
            return self.format_string(node, receiver, args, kwargs)\r
        if method in ('strip', 'rstrip', 'lstrip', 'lower', 'upper', 'title', 'capitalize') and all(isinstance(a, str) for a in args):\r
            return getattr(receiver, method)(*args)\r
        if method == 'join' and len(args) == 1 and isinstance(args[0], list) and all(isinstance(a, str) for a in args[0]):\r
            return receiver.join(args[0])\r
        if method in ('join', 'replace', 'format', 'strip', 'rstrip', 'lstrip', 'lower', 'upper'):\r
            return Opaque(label(node), 'str')\r
        return Opaque(label(node))\r
\r
    def template_method(self, node, receiver, method, args):\r
        if method == 'replace' and len(args) >= 2 and isinstance(args[0], str) and args[0]:\r
            parts = []\r
            for part in receiver.parts:\r
                if isinstance(part, str) and args[0] in part:\r
                    pieces = part.split(args[0])\r
                    parts.append(pieces[0])\r
                    for piece in pieces[1:]:\r
                        parts.extend([args[1] if isinstance(args[1], (str, Template, Opaque)) else Opaque(label(node.args[1]), 'str'), piece])\r
                else:\r
                    parts.append(part)\r
            return make_string(parts)\r
        if method in ('rstrip', 'strip') and receiver.parts and isinstance(receiver.parts[-1], str) and all(isinstance(a, str) for a in args):\r
            return make_string(list(receiver.parts[:-1]) + [receiver.parts[-1].rstrip(*args)]) if method == 'rstrip' else Opaque(label(node), 'str')\r
        return Opaque(label(node), 'str')\r
\r
    def format_string(self, node, template, args, kwargs):\r
        parts, auto = [], 0\r
        try:\r
            for literal, field, spec, conversion in string.Formatter().parse(template):\r
                parts.append(literal)\r
                if field is None:\r
                    continue\r
                if field == '':\r
                    key, auto = auto, auto + 1\r
                elif field.isdigit():\r
                    key = int(field)\r
                else:\r
                    key = field\r
                if isinstance(key, int):\r
                    val = args[key] if key < len(args) else Opaque(label(node), 'str')\r
                elif key.isidentifier():\r
                    val = kwargs.get(key, Opaque(key, 'str'))\r
                else:\r
                    val = Opaque(key, 'str')\r
                if spec or conversion or not (isinstance(val, (str, Template)) or known(val) and isinstance(val, (int, float, bool))):\r
                    val = Opaque(field or str(key), 'str')\r
                parts.append(val if isinstance(val, (str, Template, Opaque)) else str(val))\r
        except (ValueError, IndexError):\r
            return Opaque(label(node), 'str')\r
        return make_string(parts)\r
\r
    # ------------------------------------------------------------ provenance\r
    def origin(self, node):\r
        """(call_id, None) for a raw Response, (call_id, path) for decoded JSON data."""\r
        if isinstance(node, ast.Name):\r
            return self.prov.get(node.id)\r
        if isinstance(node, ast.NamedExpr):\r
            return self.origin(node.value)\r
        if isinstance(node, ast.Call):\r
            if id(node) in CTX.calls:\r
                return (CTX.calls[id(node)], None)\r
            if isinstance(node.func, ast.Attribute):\r
                source = self.origin(node.func.value)\r
                attr = node.func.attr\r
                if source is AMBIGUOUS:\r
                    return AMBIGUOUS if attr in ('json', 'get', 'copy') else None\r
                if source and source[1] is None and attr == 'json':\r
                    return (source[0], [])\r
                if source and source[1] is not None and attr == 'get' and node.args:\r
                    key = self.value(node.args[0])\r
                    return (source[0], source[1] + [key if isinstance(key, str) else '*'])\r
                if source and source[1] is not None and attr == 'copy':\r
                    return source\r
            if isinstance(node.func, ast.Name):\r
                if node.func.id in ('list', 'sorted', 'reversed', 'dict', 'tuple') and len(node.args) == 1:\r
                    return self.origin(node.args[0])\r
                info = self.function_info(node.func.id)\r
                if info is not None:\r
                    self.ensure_analyzed(info)\r
                    return info.summary\r
            return None\r
        if isinstance(node, ast.Subscript):\r
            source = self.origin(node.value)\r
            if source is AMBIGUOUS:\r
                return AMBIGUOUS\r
            if source and source[1] is not None:\r
                if isinstance(node.slice, ast.Slice):\r
                    return source\r
                key = self.value(node.slice)\r
                if isinstance(key, bool) or not isinstance(key, (str, int)):\r
                    return (source[0], source[1] + ['*'])\r
                return (source[0], source[1] + [key])\r
            return None\r
        if isinstance(node, ast.IfExp):\r
            return self.merge_origins([self.origin(node.body), self.origin(node.orelse)], node)\r
        if isinstance(node, ast.BoolOp):\r
            return self.merge_origins([self.origin(v) for v in node.values], node)\r
        return None\r
\r
    def merge_origins(self, origins, node):\r
        tracked = [o for o in origins if o is not None]\r
        if not tracked:\r
            return None\r
        if any(o is AMBIGUOUS for o in tracked) or any(o != tracked[0] for o in tracked[1:]):\r
            return AMBIGUOUS  # reported if a field is later read from it\r
        return tracked[0]\r
\r
    # --------------------------------------------------------------- scanning\r
    def scan(self, node):\r
        if node is None:\r
            return\r
        if isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)):\r
            self.comprehension(node)\r
            return\r
        if isinstance(node, ast.Lambda):\r
            child = self.fork()\r
            for arg in node.args.posonlyargs + node.args.args + node.args.kwonlyargs:\r
                child.env[arg.arg] = Opaque(arg.arg)\r
                child.prov.pop(arg.arg, None)\r
            child.scan(node.body)\r
            return\r
        if isinstance(node, ast.Await):\r
            issue(node, 'Await expressions are outside the supported extraction subset.', API)\r
        for child in ast.iter_child_nodes(node):\r
            self.scan(child)\r
        if isinstance(node, ast.NamedExpr):\r
            self.assign(node.target, node.value)\r
        if isinstance(node, ast.Subscript) and isinstance(node.ctx, ast.Load):\r
            source = self.origin(node)\r
            if source is AMBIGUOUS:\r
                issue(node, 'Response field read from data with ambiguous provenance.', RESPONSE)\r
            elif source and source[1]:\r
                add(node, 'output_field', call_id=source[0], field=source[1][-1], path=source[1])\r
        if isinstance(node, ast.Call):\r
            self.call(node)\r
\r
    def comprehension(self, node):\r
        child = self.fork()\r
        for gen in node.generators:\r
            child.scan(gen.iter)\r
            source = child.origin(gen.iter)\r
            child.bind_iteration(gen.target, gen.iter, source)\r
            for cond in gen.ifs:\r
                child.scan(cond)\r
        if isinstance(node, ast.DictComp):\r
            child.scan(node.key)\r
            child.scan(node.value)\r
        else:\r
            child.scan(node.elt)\r
\r
    def bind_iteration(self, target, iterator, source):\r
        """Bind a for/comprehension target, retaining response-item provenance."""\r
        items_call = isinstance(iterator, ast.Call) and isinstance(iterator.func, ast.Attribute) \\\r
            and iterator.func.attr in ('items', 'values', 'keys') and not iterator.args\r
        if items_call:\r
            base = self.origin(iterator.func.value)\r
            if base is AMBIGUOUS:\r
                issue(iterator, 'Iteration over data with ambiguous provenance.', RESPONSE)\r
                base = None\r
            names = target.elts if isinstance(target, ast.Tuple) else [target]\r
            for i, t in enumerate(names):\r
                if isinstance(t, ast.Name):\r
                    self.env[t.id] = Opaque(t.id)\r
                    self.imports.pop(t.id, None)\r
                    is_value = iterator.func.attr == 'values' or (iterator.func.attr == 'items' and i == 1)\r
                    if base and base[1] is not None and is_value:\r
                        self.prov[t.id] = (base[0], base[1] + ['*'])\r
                    else:\r
                        self.prov.pop(t.id, None)\r
                else:\r
                    self.assign(t, None)\r
            return\r
        if isinstance(iterator, ast.Call) and isinstance(iterator.func, ast.Name) and iterator.func.id == 'enumerate' \\\r
                and iterator.args and isinstance(target, ast.Tuple) and len(target.elts) == 2:\r
            inner = self.origin(iterator.args[0])\r
            self.bind_iteration(target.elts[0], ast.Constant(0), None)\r
            self.bind_iteration(target.elts[1], iterator.args[0], inner)\r
            return\r
        if source is AMBIGUOUS:\r
            issue(iterator, 'Iteration over data with ambiguous provenance.', RESPONSE)\r
            source = None\r
        if isinstance(target, ast.Name):\r
            self.env[target.id] = Opaque(target.id)\r
            self.imports.pop(target.id, None)\r
            if source and source[1] is not None:\r
                self.prov[target.id] = (source[0], source[1] + [0])\r
            else:\r
                self.prov.pop(target.id, None)\r
        else:\r
            if source and source[1] is not None:\r
                issue(target, 'Destructuring items of a response is outside the supported subset.', RESPONSE)\r
            for n in ast.walk(target):\r
                if isinstance(n, ast.Name):\r
                    self.env[n.id] = Opaque(n.id)\r
                    self.prov.pop(n.id, None)\r
\r
    def call(self, node):\r
        name = self.qualified(node.func)\r
        method = name[len('requests.'):] if name.startswith('requests.') else ''\r
        if method.startswith('api.'):\r
            method = method[4:]\r
        if name == 'requests' or name.startswith('requests.'):\r
            add(node, 'method_call', library='requests', method=name[len('requests.'):] if name.startswith('requests.') else '')\r
        if method in HTTP or method == 'request':\r
            self.http(node, method)\r
            return\r
        if name in DYNAMIC_CODE or (isinstance(node.func, ast.Name) and node.func.id in DYNAMIC_CODE and node.func.id not in self.env):\r
            issue(node, 'Dynamic code or attribute access is unsupported.', ALL)\r
            return\r
        if name.startswith(OTHER_HTTP_CLIENTS):\r
            issue(node, 'Only direct requests calls are supported; other HTTP clients are unresolved: ' + name, API)\r
            return\r
        if name.startswith('requests.'):\r
            return  # exceptions, auth helpers, adapters and utilities: recorded, no HTTP claim\r
        if name:  # a callable resolved by name: module function, import or builtin\r
            if isinstance(node.func, ast.Name):\r
                info = self.function_info(node.func.id)\r
                if info is not None:\r
                    self.ensure_analyzed(info)\r
                    for arg in list(node.args) + [kw.value for kw in node.keywords]:\r
                        source = self.origin(arg)\r
                        if source is AMBIGUOUS or source and source[1] is not None:\r
                            issue(node, 'Response data is passed into user-defined function %s; field accesses inside it are not linked.' % node.func.id, RESPONSE)\r
                    self.havoc_arguments(node)\r
                    return\r
            if name in PURE or name in BUILTIN_EXCEPTIONS or name.split('.')[-1] in BUILTIN_EXCEPTIONS:\r
                return\r
            self.havoc_arguments(node)\r
            for arg in node.args:\r
                if isinstance(arg, ast.Lambda) and any(self.origin(a) is not None for a in node.args if a is not arg):\r
                    issue(node, 'A lambda applied to response data is outside the supported subset.', RESPONSE)\r
            return\r
        if isinstance(node.func, ast.Attribute):\r
            self.method_call(node)\r
            return\r
        self.havoc_arguments(node)\r
\r
    def havoc_arguments(self, node):\r
        """An unknown callee may mutate container arguments; forget their contents."""\r
        for arg in list(node.args) + [kw.value for kw in node.keywords]:\r
            if isinstance(arg, ast.Starred):\r
                arg = arg.value\r
            if isinstance(arg, ast.Name) and isinstance(self.env.get(arg.id), (dict, list)):\r
                self.env[arg.id] = Opaque(arg.id, type_of(self.env[arg.id]))\r
\r
    def method_call(self, node):\r
        receiver_node, attr = node.func.value, node.func.attr\r
        source = self.origin(receiver_node)\r
        if source is AMBIGUOUS:\r
            if attr == 'get':\r
                issue(node, 'Response field read from data with ambiguous provenance.', RESPONSE)\r
            return\r
        if source is not None:\r
            if source[1] is None:  # raw Response\r
                if attr == 'json' and (node.args or node.keywords):\r
                    issue(node, 'Custom JSON decoding arguments can change response shape.', RESPONSE)\r
                return\r
            if attr == 'get' and node.args:\r
                add(node, 'output_field', call_id=source[0], field=self.origin(node)[1][-1], path=self.origin(node)[1], optional_access=True)\r
            elif attr == 'pop' and node.args:\r
                key = self.value(node.args[0])\r
                path = source[1] + [key if isinstance(key, str) else '*']\r
                add(node, 'output_field', call_id=source[0], field=path[-1], path=path, optional_access=len(node.args) > 1)\r
                self.forget_response_data(receiver_node, node)\r
            elif attr in MUTATORS:\r
                self.forget_response_data(receiver_node, node)\r
            return\r
        receiver = self.value(receiver_node)\r
        if isinstance(receiver_node, ast.Name) and receiver_node.id in self.env and attr in MUTATORS:\r
            self.mutate(receiver_node.id, attr, node)\r
            return\r
        if attr in HTTP or attr == 'request':\r
            if isinstance(receiver, Opaque) and receiver.type == 'requests.Session':\r
                issue(node, 'Session-based requests are outside the supported subset.', API)\r
            elif isinstance(receiver, (Opaque, Template)) and not self.qualified(receiver_node):\r
                if attr != 'get' or self.looks_like_request(node):\r
                    issue(node, 'Unresolved HTTP-like call receiver: ' + label(node.func), API)\r
        if not self.qualified(receiver_node) and not isinstance(receiver, (str, Template, dict)):\r
            self.havoc_arguments(node)\r
\r
    def looks_like_request(self, node):\r
        if any(kw.arg in REQUEST_KWARGS - {'url'} for kw in node.keywords):\r
            return True\r
        if node.args:\r
            first = self.value(node.args[0])\r
            text = first if isinstance(first, str) else first.parts[0] if isinstance(first, Template) and isinstance(first.parts[0], str) else ''\r
            return text.startswith(('http://', 'https://', '/'))\r
        return False\r
\r
    def forget_response_data(self, receiver_node, node):\r
        issue(node, 'Response data is mutated; later field reads may not come from the API.', RESPONSE)\r
        if isinstance(receiver_node, ast.Name):\r
            self.prov[receiver_node.id] = AMBIGUOUS\r
\r
    def mutate(self, name, attr, node):\r
        """Apply a container mutation (copy-on-write) or forget the container."""\r
        current = self.env[name]\r
        args = [self.value(a) for a in node.args]\r
        kwargs = {kw.arg: self.value(kw.value) for kw in node.keywords if kw.arg}\r
        new = MISSING\r
        if isinstance(current, dict):\r
            if attr == 'update' and not any(kw.arg is None for kw in node.keywords):\r
                if not args or (len(args) == 1 and isinstance(args[0], dict)):\r
                    new = {**current, **(args[0] if args else {}), **kwargs}\r
            elif attr == 'setdefault' and args and isinstance(args[0], str):\r
                new = dict(current)\r
                new.setdefault(args[0], args[1] if len(args) > 1 else None)\r
            elif attr == 'pop' and args and isinstance(args[0], str):\r
                new = {k: v for k, v in current.items() if k != args[0]}\r
            elif attr == 'clear':\r
                new = {}\r
        elif isinstance(current, list):\r
            if attr == 'append' and len(args) == 1:\r
                new = current + [args[0]]\r
            elif attr == 'extend' and len(args) == 1 and isinstance(args[0], list):\r
                new = current + list(args[0])\r
            elif attr == 'clear':\r
                new = []\r
        if new is MISSING:\r
            new = Opaque(name, type_of(current))\r
        self.set_container(name, new)\r
\r
    def set_container(self, name, new):\r
        old = self.env.get(name)\r
        for other, value in list(self.env.items()):\r
            if other != name and value is old and isinstance(old, (dict, list)):\r
                self.env[other] = new  # keep aliases consistent\r
            elif other != name and isinstance(value, (dict, list)) and contains(value, old):\r
                self.env[other] = Opaque(other, type_of(value))\r
        self.env[name] = new\r
\r
    def http(self, node, method):\r
        args = list(node.args)\r
        kwargs = {kw.arg: kw.value for kw in node.keywords if kw.arg}\r
        expanded = any(kw.arg is None for kw in node.keywords)\r
        if expanded:\r
            issue(node, 'Expanded request keyword arguments are unsupported.', API)\r
        if method == 'request':\r
            method_node = kwargs.get('method') or (args.pop(0) if args else None)\r
            method_value = self.value(method_node)\r
        else:\r
            method_value = method.upper()\r
        url_node = kwargs.get('url') or (args.pop(0) if args else None)\r
        url = self.value(url_node)\r
        for key, val in zip(POSITIONAL.get(method, []), args):\r
            if key in kwargs:\r
                issue(node, 'Duplicate request argument.', REQUEST)\r
            kwargs[key] = val\r
        if len(args) > len(POSITIONAL.get(method, [])):\r
            issue(node, 'Unsupported positional request arguments.', REQUEST)\r
        call_id = 'call_%s_%s' % (node.lineno, node.col_offset)\r
        CTX.calls[id(node)] = call_id\r
        request = {}\r
        for via in ('params', 'json', 'data', 'headers', 'cookies', 'auth'):\r
            if via in kwargs:\r
                value = self.value(kwargs[via])\r
                request[via] = {'provided': True, 'known': known(value), 'value': public(value),\r
                                'keys_known': isinstance(value, dict), 'shape': encode(value),\r
                                'fields': {k: {'known': known(v), 'value': public(v), 'shape': encode(v)} for k, v in value.items()} if isinstance(value, dict) else {}}\r
                if isinstance(value, dict):\r
                    for field, val in value.items():\r
                        add(node, 'input_field', call_id=call_id, field=field, via=via, known=known(val), value=public(val))\r
        method_ok = isinstance(method_value, str) and method_value.upper() in {m.upper() for m in HTTP}\r
        url_ok = isinstance(url, str) or origin_known(url)\r
        if not url_ok or not method_ok:\r
            issue(node, 'Dynamic endpoint or HTTP method requires explicit input_bindings.', API)\r
        add(node, 'endpoint', call_id=call_id, endpoint=url if isinstance(url, str) else None,\r
            endpoint_template=encode(url) if isinstance(url, Template) else None,\r
            http_method=method_value.upper() if isinstance(method_value, str) else None,\r
            resolved=url_ok and method_ok, request=request, request_complete=not expanded)\r
        if 'verify' in kwargs and self.value(kwargs['verify']) is False:\r
            issue(node, 'TLS verification disabled; outside supported verification scope.', ['contextual'])\r
        if 'files' in kwargs:\r
            issue(node, 'Multipart file uploads are outside the supported request subset.', REQUEST)\r
        if any(k not in REQUEST_KWARGS | {'files'} for k in kwargs):\r
            issue(node, 'Unsupported requests keyword argument.', REQUEST)\r
\r
    # -------------------------------------------------------------- binding\r
    def assign(self, target, node, value=MISSING):\r
        if value is MISSING:\r
            value = self.value(node) if node is not None else Opaque(label(target))\r
        if isinstance(target, ast.Name):\r
            self.env[target.id] = value\r
            self.imports.pop(target.id, None)\r
            self.local_functions.pop(target.id, None)\r
            source = self.origin(node) if node is not None else None\r
            if source is not None:\r
                self.prov[target.id] = source\r
            else:\r
                self.prov.pop(target.id, None)\r
        elif isinstance(target, (ast.Tuple, ast.List)):\r
            elts = target.elts\r
            if node is not None and isinstance(node, (ast.Tuple, ast.List)) and len(node.elts) == len(elts) \\\r
                    and not any(isinstance(e, ast.Starred) for e in elts + node.elts):\r
                values = [self.value(e) for e in node.elts]\r
                for t, n, v in zip(elts, node.elts, values):\r
                    self.assign(t, n, v)\r
                return\r
            source = self.origin(node) if node is not None else None\r
            if source is AMBIGUOUS or source and source[1] is not None:\r
                issue(target, 'Destructuring response data is outside the supported subset.', RESPONSE)\r
            for t in elts:\r
                self.assign(t.value if isinstance(t, ast.Starred) else t, None, Opaque(label(t)))\r
        elif isinstance(target, ast.Subscript):\r
            self.assign_item(target, value)\r
        elif isinstance(target, ast.Attribute):\r
            root = target\r
            while isinstance(root, (ast.Attribute, ast.Subscript)):\r
                root = root.value\r
            if isinstance(root, ast.Name) and isinstance(self.env.get(root.id), (dict, list)):\r
                self.set_container(root.id, Opaque(root.id, type_of(self.env[root.id])))\r
        elif isinstance(target, ast.Starred):\r
            self.assign(target.value, None, Opaque(label(target)))\r
\r
    def assign_item(self, target, value):\r
        """d[k] = v on a tracked container (copy-on-write); otherwise forget the container."""\r
        chain = []\r
        node = target\r
        while isinstance(node, ast.Subscript):\r
            chain.append(node.slice)\r
            node = node.value\r
        if not isinstance(node, ast.Name):\r
            return\r
        name = node.id\r
        source = self.prov.get(name)\r
        if source is not None and name not in self.env or source is not None and not isinstance(self.env.get(name), (dict, list)):\r
            self.forget_response_data(node, target)\r
            return\r
        keys = [self.value(k) for k in reversed(chain)]\r
        root = self.env.get(name)\r
\r
        def update(container, path):\r
            if not path:\r
                return value\r
            key = path[0]\r
            container = present(container)\r
            if isinstance(container, dict) and isinstance(key, str):\r
                new = dict(container)\r
                new[key] = update(container.get(key, {}) if len(path) > 1 else None, path[1:])\r
                return new\r
            if isinstance(container, list) and isinstance(key, int) and -len(container) <= key < len(container):\r
                new = list(container)\r
                new[key] = update(container[key], path[1:])\r
                return new\r
            return MISSING\r
\r
        new = update(root, keys) if isinstance(root, (dict, list)) else MISSING\r
        if new is MISSING or contains_missing(new):\r
            new = Opaque(name, type_of(root) if root is not None else None)\r
        if name in self.env or isinstance(new, (dict, list)):\r
            self.set_container(name, new)\r
\r
    # ------------------------------------------------------------ statements\r
    def statements(self, statements):\r
        """Analyze a block; return True when it cannot fall through."""\r
        for node in statements:\r
            if self.statement(node):\r
                return True\r
        return False\r
\r
    def statement(self, node):\r
        if isinstance(node, ast.Import):\r
            for alias in node.names:\r
                self.imports[alias.asname or alias.name.split('.')[0]] = alias.name if alias.asname else alias.name.split('.')[0]\r
                self.env.pop(alias.asname or alias.name.split('.')[0], None)\r
                top = alias.name.split('.')[0]\r
                add(node, 'import', library=alias.name, stdlib=top in getattr(sys, 'stdlib_module_names', set()), local=False)\r
            return False\r
        if isinstance(node, ast.ImportFrom):\r
            mod = node.module or ''\r
            for alias in node.names:\r
                if alias.name == '*':\r
                    issue(node, 'Wildcard import is unsupported.', ALL)\r
                else:\r
                    self.imports[alias.asname or alias.name] = (mod + '.' if mod else '') + alias.name\r
                    self.env.pop(alias.asname or alias.name, None)\r
                add(node, 'import', library=mod, stdlib=mod.split('.')[0] in getattr(sys, 'stdlib_module_names', set()), local=node.level > 0)\r
            return False\r
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):\r
            for decorator in node.decorator_list:\r
                self.scan(decorator)\r
            self.env.pop(node.name, None)\r
            self.imports.pop(node.name, None)\r
            self.prov.pop(node.name, None)\r
            registered = CTX.functions.get(node.name)\r
            if self is CTX.module and registered is not None and registered.node is node:\r
                return False  # analyzed on first call, or at module end with final globals\r
            info = FunctionInfo(node)\r
            self.local_functions[node.name] = info\r
            self.analyze_function(info, self.env, self.imports, self.prov)\r
            return False\r
        if isinstance(node, ast.ClassDef):\r
            issue(node, 'Classes are outside the supported extraction subset.', API)\r
            for stmt in node.body:\r
                if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):\r
                    self.analyze_function(FunctionInfo(stmt), self.env, self.imports, self.prov)\r
            self.env.pop(node.name, None)\r
            return False\r
        if isinstance(node, ast.Assign):\r
            self.scan(node.value)\r
            value = self.value(node.value)\r
            for target in node.targets:\r
                self.scan_target(target)\r
                self.assign(target, node.value, value)\r
            return False\r
        if isinstance(node, ast.AnnAssign):\r
            if node.value is not None:\r
                self.scan(node.value)\r
                self.scan_target(node.target)\r
                self.assign(node.target, node.value)\r
            return False\r
        if isinstance(node, ast.AugAssign):\r
            self.scan(node.value)\r
            self.scan_target(node.target)\r
            if isinstance(node.target, ast.Name):\r
                combined = ast.BinOp(left=ast.Name(id=node.target.id, ctx=ast.Load()), op=node.op, right=node.value)\r
                ast.copy_location(combined, node)\r
                value = self.value(combined)\r
                if self.prov.get(node.target.id) is not None:\r
                    self.forget_response_data(node.target, node)\r
                self.env[node.target.id] = value\r
                self.imports.pop(node.target.id, None)\r
            else:\r
                self.assign(node.target, None, Opaque(label(node.target)))\r
            return False\r
        if isinstance(node, (ast.Expr,)):\r
            self.scan(node.value)\r
            return False\r
        if isinstance(node, ast.Return):\r
            self.scan(node.value)\r
            if node.value is not None:\r
                self.returns.append(self.origin(node.value))\r
            return True\r
        if isinstance(node, ast.Raise):\r
            self.scan(node.exc)\r
            self.scan(node.cause)\r
            return True\r
        if isinstance(node, (ast.Break, ast.Continue)):\r
            return True\r
        if isinstance(node, ast.Pass):\r
            return False\r
        if isinstance(node, ast.If):\r
            self.scan(node.test)\r
            body, orelse = self.fork(), self.fork()\r
            body_ends = body.statements(node.body)\r
            else_ends = orelse.statements(node.orelse)\r
            self.collect(body, orelse)\r
            self.join([None if body_ends else body, None if else_ends else orelse], node)\r
            return body_ends and else_ends\r
        if isinstance(node, (ast.For, ast.AsyncFor, ast.While)):\r
            if isinstance(node, ast.AsyncFor):\r
                issue(node, 'Async iteration is outside the supported extraction subset.', API)\r
            self.loop(node)\r
            return False\r
        if isinstance(node, (ast.Try, getattr(ast, 'TryStar', ast.Try))):\r
            return self.try_statement(node)\r
        if isinstance(node, (ast.With, ast.AsyncWith)):\r
            if isinstance(node, ast.AsyncWith):\r
                issue(node, 'Async context managers are outside the supported extraction subset.', API)\r
            for item in node.items:\r
                self.scan(item.context_expr)\r
                if item.optional_vars is not None:\r
                    source = self.origin(item.context_expr)\r
                    name = self.qualified(item.context_expr.func) if isinstance(item.context_expr, ast.Call) else ''\r
                    typed = Opaque(label(item.optional_vars), 'requests.Session' if name in ('requests.Session', 'requests.session') else None)\r
                    self.assign(item.optional_vars, None, typed)\r
                    if isinstance(item.optional_vars, ast.Name) and source is not None:\r
                        self.prov[item.optional_vars.id] = source\r
            return self.statements(node.body)\r
        if isinstance(node, ast.Delete):\r
            for target in node.targets:\r
                if isinstance(target, ast.Name):\r
                    self.env.pop(target.id, None)\r
                    self.prov.pop(target.id, None)\r
                elif isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name) and isinstance(self.env.get(target.value.id), dict):\r
                    key = self.value(target.slice)\r
                    current = self.env[target.value.id]\r
                    self.set_container(target.value.id, {k: v for k, v in current.items() if k != key} if isinstance(key, str) else Opaque(target.value.id, 'dict'))\r
                elif isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name) and self.prov.get(target.value.id) is not None:\r
                    self.forget_response_data(target.value, node)\r
            return False\r
        if isinstance(node, ast.Assert):\r
            self.scan(node.test)\r
            self.scan(node.msg)\r
            return False\r
        if isinstance(node, (ast.Global, ast.Nonlocal)):\r
            issue(node, 'global/nonlocal rebinding is outside the supported extraction subset.', API)\r
            self.havoc(node.names, keep_provenance=False)\r
            return False\r
        if isinstance(node, getattr(ast, 'Match', ())):\r
            issue(node, 'Match statements are outside the supported extraction subset.', API)\r
            self.scan(node.subject)\r
            branches = []\r
            for case in node.cases:\r
                branch = self.fork()\r
                ends = branch.statements(case.body)\r
                self.collect(branch)\r
                branches.append(None if ends else branch)\r
            self.join(branches + [self.fork()], node)\r
            return False\r
        if isinstance(node, getattr(ast, 'TypeAlias', ())):\r
            return False\r
        issue(node, 'Unsupported statement: ' + type(node).__name__, API)\r
        return False\r
\r
    def scan_target(self, target):\r
        """Scan index expressions in an assignment target without recording field reads."""\r
        if isinstance(target, ast.Subscript):\r
            self.scan_target(target.value)\r
            self.scan(target.slice)\r
        elif isinstance(target, ast.Attribute):\r
            self.scan_target(target.value)\r
        elif isinstance(target, (ast.Tuple, ast.List)):\r
            for t in target.elts:\r
                self.scan_target(t)\r
\r
    def loop(self, node):\r
        body_nodes = node.body + node.orelse\r
        changed = assigned_names(body_nodes)\r
        if isinstance(node, (ast.For, ast.AsyncFor)):\r
            self.scan(node.iter)\r
            changed |= {n.id for n in ast.walk(node.target) if isinstance(n, ast.Name)}\r
        before = {name: self.prov.get(name) for name in changed}\r
        # Any iteration may see values from an earlier iteration: forget changed values.\r
        for name in changed:\r
            if name in self.env:\r
                self.env[name] = Opaque(name, type_of(self.env[name]))\r
        if isinstance(node, ast.While):\r
            self.scan(node.test)\r
        entry = self.fork()\r
        body = self.fork()\r
        if isinstance(node, (ast.For, ast.AsyncFor)):\r
            body.bind_iteration(node.target, node.iter, self.origin(node.iter))\r
        body.statements(node.body)\r
        self.collect(body)\r
        for name in changed:\r
            start, end = before.get(name), body.prov.get(name)\r
            if start is not None and end is not None and start != end:\r
                issue(node, 'Response provenance of %s changes across loop iterations.' % name, RESPONSE)\r
                body.prov[name] = AMBIGUOUS\r
        self.join([entry, body], node)\r
        if node.orelse:\r
            self.statements(node.orelse)\r
\r
    def try_statement(self, node):\r
        before = self.fork()\r
        body = self.fork()\r
        body_ends = body.statements(node.body)\r
        changed = assigned_names(node.body)\r
        ends = []\r
        if not body_ends:\r
            else_ends = body.statements(node.orelse) if node.orelse else False\r
            ends.append(None if else_ends else body)\r
        self.collect(body)\r
        for handler in node.handlers:\r
            h = before.fork()\r
            # A handler may start after any prefix of the body ran.\r
            for name in changed:\r
                if name in h.env or name in body.env:\r
                    h.env[name] = Opaque(name)\r
                if body.prov.get(name) is not None and h.prov.get(name) != body.prov.get(name):\r
                    h.prov[name] = body.prov[name] if h.prov.get(name) is None else AMBIGUOUS\r
            if handler.name:\r
                h.env[handler.name] = Opaque(handler.name)\r
                h.prov.pop(handler.name, None)\r
            handler_ends = h.statements(handler.body)\r
            self.collect(h)\r
            ends.append(None if handler_ends else h)\r
        reachable = any(e is not None for e in ends)\r
        self.join(ends if reachable else [before], node)\r
        final_ends = self.statements(node.finalbody) if node.finalbody else False\r
        return final_ends or not reachable\r
\r
\r
def contains(container, target):\r
    if container is target:\r
        return True\r
    if isinstance(container, dict):\r
        return any(contains(v, target) for v in container.values())\r
    if isinstance(container, list):\r
        return any(contains(v, target) for v in container)\r
    return False\r
\r
\r
def contains_missing(value):\r
    if value is MISSING:\r
        return True\r
    if isinstance(value, dict):\r
        return any(contains_missing(v) for v in value.values())\r
    if isinstance(value, list):\r
        return any(contains_missing(v) for v in value)\r
    return False\r
\r
\r
def eval_binop(op, left, right):\r
    if isinstance(op, ast.Add):\r
        return left + right\r
    if isinstance(op, ast.Sub):\r
        return left - right\r
    if isinstance(op, ast.Mult):\r
        return left * right\r
    if isinstance(op, ast.Div):\r
        return left / right\r
    if isinstance(op, ast.FloorDiv):\r
        return left // right\r
    if isinstance(op, ast.Mod):\r
        return left % right\r
    raise ValueError('unsupported')\r
\r
\r
def record_unused_parameters(node, all_args):\r
    referenced = set()\r
    reflective = False\r
    for stmt in node.body:\r
        for descendant in ast.walk(stmt):\r
            if isinstance(descendant, ast.Name):\r
                referenced.add(descendant.id)\r
                if descendant.id in ('locals', 'vars'):\r
                    reflective = True\r
    if reflective:\r
        return\r
    for arg in all_args:\r
        if arg.arg in ('self', 'cls') or arg.arg in referenced:\r
            continue\r
        # Pyright ranges are 0-indexed lines; ast lines are 1-indexed.\r
        unused_parameters.append({'name': arg.arg, 'line': arg.lineno - 1,\r
                                  'start_character': arg.col_offset, 'end_character': arg.col_offset + len(arg.arg)})\r
\r
\r
def prepass(tree):\r
    """Register module-level functions so calls resolve before definitions."""\r
    counts = {}\r
    for stmt in tree.body:\r
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):\r
            counts[stmt.name] = counts.get(stmt.name, 0) + 1\r
    for stmt in tree.body:\r
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)) and counts[stmt.name] == 1:\r
            CTX.functions[stmt.name] = FunctionInfo(stmt)\r
\r
\r
try:\r
    tree = ast.parse(code)\r
    for token in tokenize.generate_tokens(io.StringIO(code).readline):\r
        if token.type == tokenize.COMMENT and ('pyright:' in token.string.lower() or 'type: ignore' in token.string.lower()):\r
            issue(types.SimpleNamespace(lineno=token.start[0]), 'Candidate contains checker suppression/configuration directives.', IDENTIFIER)\r
    module = Analyzer()\r
    CTX.module = module\r
    prepass(tree)\r
    module.statements(tree.body)\r
    for info in list(CTX.functions.values()):\r
        if not info.done:\r
            module.analyze_function(info, module.env, module.imports, module.prov)\r
    print(json.dumps({\r
        'claims': claims,\r
        'complete': not issues,\r
        'issues': issues,\r
        'unused_parameters': unused_parameters,\r
    }))\r
except (SyntaxError, ValueError) as e:\r
    print(json.dumps({'claims': [], 'complete': False, 'issues': [], 'unused_parameters': [], 'error': str(e)}))\r
`;
  }
});

// src/verificationTypes.ts
function result(layer, state, tier2, source, detail, kind = null) {
  return { layer, state, tier: tier2, weight: LAYER_WEIGHTS[layer], evidence_source: source, evidence_detail: detail, hallucination_type: kind };
}
function unknown(layer, detail) {
  return result(layer, "unverifiable", "none", "verification", detail);
}
function aggregate(layer, rows, emptyReason) {
  const applicable = rows.filter((r) => r.state !== "not_applicable");
  if (!applicable.length) return result(layer, "not_applicable", "none", "extraction / specification", rows.length ? rows.map((r) => r.evidence_detail).join("\n") : emptyReason);
  const incorrect = applicable.filter((r) => r.state === "verified_incorrect");
  const unresolved = applicable.filter((r) => r.state === "unverifiable");
  const selected = incorrect.length ? incorrect.sort((a, b) => TIER_FACTORS[b.tier] - TIER_FACTORS[a.tier])[0] : unresolved.length ? unresolved[0] : applicable.sort((a, b) => TIER_FACTORS[a.tier] - TIER_FACTORS[b.tier])[0];
  return { ...selected, evidence_detail: rows.map((r) => r.evidence_detail).join("\n"), claim_ids: rows.flatMap((r) => r.claim_ids || []) };
}
function extractionLimits(source) {
  const layers = /* @__PURE__ */ new Set(), reasons = [];
  const records = Array.isArray(source) ? source.filter((c2) => c2.type === "extraction_issue") : source.error || !source.complete ? [{ issues: source.issues, error: source.error ?? (source.issues?.length ? void 0 : "Extraction incomplete.") }] : [];
  for (const record of records) {
    if (record.error) {
      ALL_LAYERS.forEach((l) => layers.add(l));
      reasons.push(String(record.error));
    }
    for (const i of record.issues || []) {
      const affects = Array.isArray(i?.affects) && i.affects.length ? i.affects : ALL_LAYERS;
      for (const l of affects) if (ALL_LAYERS.includes(l)) layers.add(l);
      reasons.push(`line ${i?.line ?? "?"}: ${i?.reason ?? "unsupported construct"}`);
    }
    if (!record.error && !(record.issues || []).length) ALL_LAYERS.forEach((l) => layers.add(l));
  }
  return { layers, reasons };
}
function aggregateExtracted(layer, claims, rows, emptyReason) {
  const r = aggregate(layer, rows, emptyReason);
  const relevant = { interface: ["import"], identifier: ["method_call"], access_point: ["endpoint"], input_contract: ["endpoint", "input_field"], output_contract: ["output_field"], contextual: ["endpoint", "input_field"] };
  r.claim_ids = claims.filter((c2) => relevant[layer].includes(c2.type) && typeof c2.id === "string").map((c2) => c2.id);
  const limits = extractionLimits(claims);
  if (limits.layers.has(layer) && (r.state === "verified_correct" || r.state === "not_applicable")) {
    return { ...unknown(layer, `Extraction is incomplete for this layer; unsupported claims may be missing (${limits.reasons.join("; ")}). ` + r.evidence_detail), claim_ids: r.claim_ids };
  }
  if (limits.reasons.length && !limits.layers.has(layer)) {
    r.evidence_detail += `
Extraction limitations elsewhere do not affect this layer; evidence covers the extracted ${layer === "interface" ? "imports" : "claims"} only.`;
  }
  return r;
}
var import_crypto2, LAYER_WEIGHTS, ALL_LAYERS, TIER_FACTORS, hashCode, ofType;
var init_verificationTypes = __esm({
  "src/verificationTypes.ts"() {
    "use strict";
    import_crypto2 = require("crypto");
    LAYER_WEIGHTS = { interface: 3, identifier: 3, access_point: 4, input_contract: 2, output_contract: 1, contextual: 2 };
    ALL_LAYERS = Object.keys(LAYER_WEIGHTS);
    TIER_FACTORS = { tier_1: 1, tier_2: 0.8, tier_3: 0.9, tier_4: 0.5, none: 0 };
    hashCode = (code) => (0, import_crypto2.createHash)("sha256").update(code).digest("hex");
    ofType = (claims, type) => claims.filter((c2) => c2.type === type);
  }
});

// src/claimExtractor.ts
async function extractClaims({ code, input_bindings = {} }) {
  const failed = (error) => ({ claims: [], complete: false, issues: [], error, candidate_hash: hashCode(code) });
  if (!code.trim()) return failed("No candidate code supplied.");
  return new Promise((resolve5) => {
    const child = (0, import_child_process.spawn)(process.env.CONFIDENCE_PYTHON || "python", ["-c", BOOTSTRAP], { stdio: "pipe", timeout: 1e4 });
    let stdout = "", stderr = "";
    child.stdout.setEncoding("utf8");
    child.stderr.setEncoding("utf8");
    child.stdout.on("data", (d) => {
      stdout += d;
    });
    child.stderr.on("data", (d) => {
      stderr += d;
    });
    child.on("error", (e) => resolve5(failed(`Python extraction could not start: ${e.message}`)));
    child.stdin.on("error", () => {
    });
    child.on("close", (exitCode, signal) => {
      if (exitCode !== 0 || signal) return resolve5(failed(`Extraction failed (${exitCode ?? signal}): ${stderr}`));
      try {
        const data = JSON.parse(stdout);
        if (!Array.isArray(data.claims) || typeof data.complete !== "boolean" || !Array.isArray(data.issues)) throw new Error("Invalid extractor result");
        if (!data.complete) data.claims.push({ id: "extraction_limitations", type: "extraction_issue", issues: data.issues, error: data.error });
        resolve5({ ...data, candidate_hash: hashCode(code) });
      } catch {
        resolve5(failed(`Invalid extraction output: ${stderr || stdout.slice(0, 200)}`));
      }
    });
    child.stdin.end(JSON.stringify(EXTRACTION_SCRIPT) + "\n" + JSON.stringify({ code, input_bindings }));
  });
}
var import_child_process, BOOTSTRAP;
var init_claimExtractor = __esm({
  "src/claimExtractor.ts"() {
    "use strict";
    import_child_process = require("child_process");
    init_extractorScript();
    init_verificationTypes();
    BOOTSTRAP = "import sys, json; exec(compile(json.loads(sys.stdin.readline()), '<extract_claims>', 'exec'))";
  }
});

// src/packageEvidence.ts
async function queryPypi({ library_name }, fetcher = fetch) {
  const top = library_name.split(".")[0], distribution = IMPORT_DISTRIBUTIONS[top] || top;
  const source_url = `https://pypi.org/pypi/${encodeURIComponent(distribution)}/json`;
  const base = { source_url, retrieved_at: (/* @__PURE__ */ new Date()).toISOString(), import_name: top, distribution };
  if (!/^[A-Za-z_][A-Za-z0-9_.-]*$/.test(top)) return { ...base, exists: null, status: "unverifiable", summary: "Invalid or relative import name." };
  try {
    const response = await fetcher(source_url, { signal: AbortSignal.timeout(8e3) });
    if (response.status === 404) return { ...base, exists: false, status: "not_found", summary: "Distribution absent from PyPI; this alone does not prove an import nonexistent." };
    if (!response.ok) return { ...base, exists: null, status: "unverifiable", summary: `PyPI HTTP ${response.status}` };
    const data = await response.json();
    if (!data.info || typeof data.info.name !== "string" || typeof data.info.version !== "string") throw new Error("Malformed PyPI metadata");
    const normalize2 = (name) => name.toLowerCase().replace(/[-_.]+/g, "-");
    if (normalize2(data.info.name) !== normalize2(distribution)) throw new Error("PyPI metadata names a different distribution.");
    return { ...base, exists: true, status: "found", latest_version: data.info.version, summary: data.info.summary || "" };
  } catch (e) {
    return { ...base, exists: null, status: "unverifiable", summary: `Package lookup failed: ${String(e)}` };
  }
}
function pickDatum(container, top) {
  if (!container) return void 0;
  const direct = container[top];
  if (direct) return direct;
  const self = container;
  if (self.distribution === top || self.import_name === top) return self;
  return void 0;
}
async function verifyInterface({ claims, pypi_data = {} }) {
  const rows = ofType(claims, "import").map((imp) => {
    const top = String(imp.library || "").split(".")[0];
    if (imp.stdlib === true) return result("interface", "verified_correct", "tier_2", "Pinned interpreter standard-library inventory", `${top} is in the verification interpreter's standard library (sys.stdlib_module_names).`);
    if (imp.local) return unknown("interface", `Local import ${imp.library} cannot be verified without its source.`);
    const datum = pickDatum(pypi_data, top);
    if (!datum || datum.status === "unverifiable" || datum.exists === null) return unknown("interface", `No usable package evidence for ${top}: ${datum?.summary || "lookup missing"}`);
    if (!Object.hasOwn(IMPORT_DISTRIBUTIONS, top)) return unknown("interface", `No reviewed import-to-distribution mapping for ${top}; registry existence or 404 cannot settle this import.`);
    if (datum.status === "not_found" && datum.exists === false) return unknown("interface", `Expected distribution ${IMPORT_DISTRIBUTIONS[top]} not found; cannot establish import nonexistence.`);
    if (datum.status !== "found" || datum.exists !== true || datum.distribution !== IMPORT_DISTRIBUTIONS[top]) return unknown(
      "interface",
      `Inconsistent package evidence for ${top}: expected status=found, exists=true and distribution=${IMPORT_DISTRIBUTIONS[top]}; received status=${datum.status}, exists=${datum.exists}, distribution=${datum.distribution ?? "(missing)"}. Preserve the full query_pypi result or use verify_candidate.`
    );
    return result("interface", "verified_correct", "tier_2", "PyPI metadata + reviewed import mapping", `${top} maps to ${datum.distribution} (${datum.latest_version || "version unknown"}). Installation/callables checked separately by Pyright.`);
  });
  return aggregateExtracted("interface", claims, rows, "No imports in the extracted candidate.");
}
var IMPORT_DISTRIBUTIONS;
var init_packageEvidence = __esm({
  "src/packageEvidence.ts"() {
    "use strict";
    init_verificationTypes();
    IMPORT_DISTRIBUTIONS = { requests: "requests", numpy: "numpy", pandas: "pandas", PIL: "Pillow", sklearn: "scikit-learn", yaml: "PyYAML", bs4: "beautifulsoup4", cv2: "opencv-python" };
  }
});

// src/specDiscovery.ts
async function resolveApiSpec({ base_url }) {
  let base;
  try {
    base = new URL(base_url);
  } catch {
    return { spec: null, source_url: null, note: "Invalid absolute URL." };
  }
  if (!["https:", "http:"].includes(base.protocol)) return { spec: null, source_url: null, note: "Only HTTP(S) discovery is supported." };
  const direct = /\.json(?:$|\?)/i.test(base_url) || /openapi|swagger|api-docs/i.test(base.pathname);
  const candidates = direct ? [base_url] : ["/openapi.json", "/swagger.json", "/v3/api-docs"].map((p) => base_url.replace(/\/$/, "") + p);
  for (const url of candidates) {
    try {
      const r = await fetch(url, { signal: AbortSignal.timeout(5e3) });
      if (!r.ok) continue;
      const raw = await r.text(), spec = JSON.parse(raw);
      if (!/^3\.0\./.test(spec.openapi || "") || !spec.paths) continue;
      return { spec, source_url: r.url || url, retrieved_at: (/* @__PURE__ */ new Date()).toISOString(), content_hash: hashCode(raw), review_required: true };
    } catch {
    }
  }
  return { spec: null, source_url: null, note: "No supported JSON OpenAPI 3.0 contract resolved. Supply a reviewed snapshot; YAML/Swagger 2/OpenAPI 3.1 are not silently interpreted as 3.0." };
}
var init_specDiscovery = __esm({
  "src/specDiscovery.ts"() {
    "use strict";
    init_verificationTypes();
  }
});

// src/pyrightRunner.ts
async function launch(command, args, timeout) {
  return new Promise((resolve5) => {
    const child = (0, import_child_process2.spawn)(command, args, { stdio: "pipe", timeout });
    let stdout = "", stderr = "";
    child.stdout.setEncoding("utf8");
    child.stderr.setEncoding("utf8");
    child.stdout.on("data", (d) => {
      stdout += d;
    });
    child.stderr.on("data", (d) => {
      stderr += d;
    });
    child.on("error", (e) => resolve5({ stdout, stderr, exit_code: null, error: e.message }));
    child.on("close", (code, signal) => resolve5({ stdout, stderr, exit_code: code, signal, timed_out: signal === "SIGTERM" }));
    child.stdin.end();
  });
}
function createPyrightRunner() {
  return async ({ python, timeout_seconds = 20 }) => {
    const candidate_hash = hashCode(python);
    const env = await launch(process.env.CONFIDENCE_PYTHON || "python", ["-c", "import sys; print(sys.executable)"], 1e4);
    if (env.exit_code !== 0 || !env.stdout.trim()) return { ...env, candidate_hash, error: "Could not resolve the verification Python environment." };
    const directory = await (0, import_promises2.mkdtemp)((0, import_path5.join)((0, import_os2.tmpdir)(), "confidence-pyright-"));
    try {
      const path = (0, import_path5.join)(directory, "candidate.py");
      await (0, import_promises2.writeFile)(path, python, "utf8");
      const config = (0, import_path5.join)(directory, "pyrightconfig.json");
      await (0, import_promises2.writeFile)(config, JSON.stringify({
        typeCheckingMode: "standard",
        pythonVersion: "3.12",
        include: ["candidate.py"],
        reportMissingModuleSource: "warning"
      }));
      const r = await launch(process.execPath, [
        require.resolve("pyright/index.js"),
        "--outputjson",
        "--project",
        config,
        "--pythonpath",
        env.stdout.trim(),
        path
      ], Math.min(60, Math.max(0.1, timeout_seconds)) * 1e3);
      const metadata = { candidate_hash, python_executable: env.stdout.trim() };
      try {
        const json = JSON.parse(r.stdout);
        return { ...r, ...metadata, checker_version: json.version, diagnostics: json.generalDiagnostics, summary: json.summary };
      } catch {
        return { ...r, ...metadata, error: r.error || "Pyright returned no valid JSON diagnostics." };
      }
    } catch (e) {
      return { stdout: "", stderr: "", exit_code: null, candidate_hash, error: String(e) };
    } finally {
      await (0, import_promises2.rm)(directory, { recursive: true, force: true });
    }
  };
}
function parsePyright(r, code) {
  if (r.error || r.timed_out || r.signal || ![0, 1].includes(r.exit_code)) return { diagnostics: [], error: r.error || `Pyright process failed (${r.exit_code ?? r.signal}). ${r.stderr}` };
  if (r.candidate_hash && r.candidate_hash !== hashCode(code)) return { diagnostics: [], error: "Pyright result belongs to a different candidate." };
  try {
    const data = JSON.parse(r.stdout);
    if (!Array.isArray(data.generalDiagnostics) || !data.summary || data.summary.filesAnalyzed < 1 || !Number.isInteger(data.summary.errorCount) || data.summary.errorCount < 0 || data.generalDiagnostics.some((d) => typeof d.message !== "string" || !["error", "warning", "information"].includes(d.severity))) throw new Error();
    const errors = data.generalDiagnostics.filter((d) => d.severity === "error").length;
    if (errors !== data.summary.errorCount || r.exit_code === 0 && errors > 0 || r.exit_code === 1 && errors === 0) throw new Error();
    return { diagnostics: data.generalDiagnostics };
  } catch {
    return { diagnostics: [], error: "Missing, malformed or inconsistent Pyright JSON output." };
  }
}
async function verifyIdentifier(code, runPyright, allowPyright = true, extraction) {
  if (!allowPyright) return unknown("identifier", "Pyright is disabled.");
  if (!code.trim()) return unknown("identifier", "No candidate supplied.");
  try {
    const parsed = parsePyright(await runPyright({ python: code }), code);
    if (parsed.error) return unknown("identifier", parsed.error);
    const context = extraction && extraction.candidate_hash === hashCode(code) ? extraction : await extractClaims({ code });
    const apiLines = new Set((context.claims || []).filter((c2) => ["import", "method_call", "endpoint"].includes(c2.type)).map((c2) => Number(c2.line) - 1));
    const errors = parsed.diagnostics.filter((d) => d.severity === "error" && !/^report(?:Unused|Unnecessary)/.test(d.rule || ""));
    const onApiLine = (d) => Number.isInteger(d.range?.start?.line) && apiLines.has(d.range.start.line);
    const text3 = (d) => `${d.rule || "syntax/type error"} (line ${(d.range?.start?.line ?? -1) + 1}): ${d.message}`;
    const incorrect = errors.filter((d) => !d.rule || IDENTIFIER_RULES.has(d.rule) || API_SIGNATURE_RULES.has(d.rule) && onApiLine(d));
    const gaps = errors.filter((d) => !incorrect.includes(d) && (EVIDENCE_GAP_RULES.has(d.rule || "") || onApiLine(d)));
    const general = errors.filter((d) => !incorrect.includes(d) && !gaps.includes(d));
    const generalNote = general.length ? "\nGeneral Python diagnostics (not API claims; reported separately, not scored): " + general.map(text3).join("; ") : "";
    if (incorrect.length) return result(
      "identifier",
      "verified_incorrect",
      "tier_4",
      "Pyright structured diagnostics",
      incorrect.map(text3).join("\n") + generalNote,
      "static_identifier_or_type_error"
    );
    if (gaps.length) return unknown("identifier", "Incomplete static evidence for API identifiers: " + gaps.map(text3).join("\n") + generalNote);
    return result(
      "identifier",
      "verified_correct",
      "tier_4",
      "Pyright structured diagnostics",
      "No identifier, attribute or API-call diagnostics in the configured environment (Pyright standard mode). A clean check does not establish REST contracts or task behavior." + generalNote
    );
  } catch (e) {
    return unknown("identifier", `Pyright failed: ${String(e)}`);
  }
}
var import_child_process2, import_promises2, import_os2, import_path5, IDENTIFIER_RULES, API_SIGNATURE_RULES, EVIDENCE_GAP_RULES;
var init_pyrightRunner = __esm({
  "src/pyrightRunner.ts"() {
    "use strict";
    import_child_process2 = require("child_process");
    import_promises2 = require("fs/promises");
    import_os2 = require("os");
    import_path5 = require("path");
    init_verificationTypes();
    init_claimExtractor();
    IDENTIFIER_RULES = /* @__PURE__ */ new Set(["reportAttributeAccessIssue", "reportUndefinedVariable", "reportCallIssue", "reportPrivateImportUsage"]);
    API_SIGNATURE_RULES = /* @__PURE__ */ new Set(["reportArgumentType"]);
    EVIDENCE_GAP_RULES = /* @__PURE__ */ new Set(["reportMissingImports"]);
  }
});

// src/openApiVerifier.ts
function tier(spec) {
  return evidenceOf(spec).kind === "curated" ? "tier_2" : "tier_1";
}
function finish(layer, c2, spec, success) {
  const notes = c2.notes?.length ? "\nNoncritical: " + [...new Set(c2.notes)].join("; ") : "";
  if (c2.bad.length) return result(layer, "verified_incorrect", tier(spec), "OpenAPI contract", c2.bad.join("\n") + notes, "contract_violation");
  if (c2.unknown.length) return unknown(layer, c2.unknown.join("\n") + notes);
  return result(layer, "verified_correct", tier(spec), "OpenAPI contract", success + notes);
}
function concrete(v) {
  if (isAbstract(v) || isMaybe(v)) return false;
  if (Array.isArray(v)) return v.every(concrete);
  if (v && typeof v === "object") return Object.values(v).every(concrete);
  return true;
}
function shapeOf(entry, fallbackLabel) {
  if (entry == null) return void 0;
  if (own(entry, "shape")) return entry.shape;
  if (entry.known) return entry.value;
  if (entry.keys_known && entry.fields) return Object.fromEntries(Object.entries(entry.fields).map(([k, v]) => [k, shapeOf(v, k)]));
  return { $ca: "unknown", label: fallbackLabel, type: null };
}
function deref(value, spec) {
  const seen = /* @__PURE__ */ new Set();
  while (value && typeof value === "object" && own(value, "$ref")) {
    const ref = value.$ref;
    if (typeof ref !== "string" || !ref.startsWith("#/")) return { error: "External or invalid $ref is unsupported." };
    if (seen.has(ref)) return { error: "Cyclic reference is unresolved." };
    seen.add(ref);
    let target = spec;
    for (const key of ref.slice(2).split("/").map((k) => k.replace(/~1/g, "/").replace(/~0/g, "~"))) {
      if (!own(target, key)) return { error: `Unresolved reference ${ref}` };
      target = target[key];
    }
    value = target;
  }
  if (!value || typeof value !== "object" || Array.isArray(value)) return { error: "Missing or unsupported schema/object." };
  return { value };
}
function rootServers(spec) {
  if (Array.isArray(spec.servers) && spec.servers.length) return spec.servers;
  const overlay = evidenceOf(spec).servers;
  return Array.isArray(overlay) ? overlay : [];
}
function specProblem(spec) {
  if (!spec) return "No API specification available.";
  if (own(spec, "spec") && !own(spec, "openapi")) return "Received a discovery-result wrapper. Pass its spec field (the OpenAPI document or null), or use a bundled reference with verify_candidate.";
  if (own(spec, "distribution") || own(spec, "import_name")) return "Received a PyPI package datum, not an OpenAPI spec. Pass the spec field from resolve_api_spec (the OpenAPI document) or null.";
  if (own(spec, "note") && !own(spec, "openapi")) return "Received a discovery note, not an OpenAPI document. Pass the spec field from resolve_api_spec or null.";
  if (own(spec, "swagger")) return "Swagger/OpenAPI 2.0 documents are not read as OpenAPI 3.x; convert and review them first.";
  if (!/^3\.[01]\./.test(spec.openapi || "")) return "Only OpenAPI 3.0.x and 3.1.x contracts are supported.";
  if (!spec.paths || typeof spec.paths !== "object" || Array.isArray(spec.paths)) return "Specification has no valid paths map.";
  if (!rootServers(spec).length) return "Specification has no servers array. A spec without a server URL cannot resolve endpoint origins. Supply a reviewed snapshot whose x-confidence-evidence.servers cites the official base URL.";
}
function serverBases(spec, servers) {
  const bases = [];
  let uncertain = false;
  const documentUrl = evidenceOf(spec).document_url;
  for (const server of servers) {
    if (!server || typeof server.url !== "string") {
      uncertain = true;
      continue;
    }
    let urls = [server.url];
    for (const [name] of server.url.matchAll(/\{([^}]+)\}/g)) {
      const variable = server.variables?.[name.slice(1, -1)];
      if (!variable || typeof variable.default !== "string") {
        uncertain = true;
        urls = [];
        break;
      }
      const options = Array.isArray(variable.enum) && variable.enum.length ? variable.enum : [variable.default];
      urls = urls.flatMap((u) => options.map((o) => u.replace(name, o)));
    }
    for (const u of urls) {
      try {
        bases.push(documentUrl ? new URL(u, documentUrl) : new URL(u));
      } catch {
        uncertain = true;
      }
    }
  }
  return { bases, uncertain };
}
function parseTarget(ep) {
  const empty2 = { values: {}, complete: true };
  if (typeof ep.endpoint === "string") {
    let url;
    try {
      url = new URL(ep.endpoint);
    } catch {
      return { query: empty2, display: ep.endpoint, problem: "An absolute endpoint URL is required to establish the server." };
    }
    if (!["http:", "https:"].includes(url.protocol)) return { query: empty2, display: ep.endpoint, problem: "bad-protocol" };
    if (url.username || url.password) return { query: empty2, display: ep.endpoint, problem: "Credentials embedded in URLs are outside supported authentication analysis." };
    const values2 = /* @__PURE__ */ Object.create(null);
    let complete2 = true;
    for (const [k, v] of url.searchParams) {
      if (own(values2, k)) complete2 = false;
      else values2[k] = v;
    }
    const segments2 = url.pathname.split("/").slice(1).map((s) => {
      try {
        return { lit: decodeURIComponent(s) };
      } catch {
        return { mixed: [s] };
      }
    });
    return { origin: url.origin, segments: segments2, query: { values: values2, complete: complete2 }, display: `${url.origin}${url.pathname}` };
  }
  if (!isTemplate(ep.endpoint_template)) return { query: empty2, display: "(dynamic)", problem: "Endpoint or method is dynamic/unresolved." };
  const parts = ep.endpoint_template.parts, holes = [];
  const rendered = parts.map((p) => typeof p === "string" ? p.replace(/\u0000/g, "") : (holes.push(p.hole), HOLE)).join("");
  const display = templateText(ep.endpoint_template);
  const m = /^(https?):\/\/([^/?#\u0000]+)(?=$|[/?#])/i.exec(rendered);
  if (!m) return { query: empty2, display, problem: "The endpoint origin is a runtime value; the server cannot be established." };
  let origin;
  try {
    const u = new URL(m[0]);
    if (u.username || u.password) return { query: empty2, display, problem: "Credentials embedded in URLs are outside supported authentication analysis." };
    origin = u.origin;
  } catch {
    return { query: empty2, display, problem: "Invalid endpoint origin." };
  }
  let rest = rendered.slice(m[0].length).split("#")[0];
  const q = rest.indexOf("?");
  const pathText = q >= 0 ? rest.slice(0, q) : rest, queryText = q >= 0 ? rest.slice(q + 1) : "";
  let holeIndex = 0;
  const fragment = (text3) => {
    const pieces = [];
    text3.split(HOLE).forEach((lit, i, all) => {
      if (lit) pieces.push(lit);
      if (i < all.length - 1) pieces.push({ hole: holes[holeIndex++] ?? "value" });
    });
    if (pieces.length === 1 && typeof pieces[0] !== "string") return { $ca: "unknown", label: pieces[0].hole, type: "str" };
    return pieces.every((p) => typeof p === "string") ? pieces.join("") : { $ca: "template", parts: pieces };
  };
  const segments = (pathText || "/").split("/").slice(1).map((seg) => {
    if (!seg.includes(HOLE)) {
      try {
        return { lit: decodeURIComponent(seg) };
      } catch {
        return { mixed: [seg] };
      }
    }
    const value = fragment(seg);
    return isOpaque(value) ? { hole: value.label } : { mixed: value.parts };
  });
  const values = /* @__PURE__ */ Object.create(null);
  let complete = true;
  for (const pair of queryText ? queryText.split("&") : []) {
    const eq = pair.indexOf("="), key = eq >= 0 ? pair.slice(0, eq) : pair, raw = eq >= 0 ? pair.slice(eq + 1) : "";
    if (key.includes(HOLE)) {
      complete = false;
      fragment(key);
      fragment(raw);
      continue;
    }
    let name;
    try {
      name = decodeURIComponent(key.replace(/\+/g, " "));
    } catch {
      complete = false;
      continue;
    }
    const value = raw.includes(HOLE) ? fragment(raw) : (() => {
      try {
        return decodeURIComponent(raw.replace(/\+/g, " "));
      } catch {
        return raw;
      }
    })();
    if (own(values, name)) complete = false;
    else values[name] = value;
  }
  return { origin, segments, query: { values, complete }, display };
}
function findOperation(spec, endpoint) {
  const problem = specProblem(spec);
  if (problem) return { unknown: problem };
  if (endpoint.resolved === false || typeof endpoint.http_method !== "string" || typeof endpoint.endpoint !== "string" && !isTemplate(endpoint.endpoint_template))
    return { unknown: "Endpoint or method is dynamic/unresolved." };
  const target = parseTarget(endpoint);
  if (target.problem === "bad-protocol") return { bad: "The request does not use an HTTP(S) URL." };
  if (target.problem || !target.segments) return { unknown: target.problem || "Endpoint unresolved." };
  let serverKnown = false, serverMatches = false, uncertainServer = false, prefixUnresolved = false;
  const matches = [];
  let unmatchedRest;
  for (const pathKey of Object.keys(spec.paths)) {
    const item = deref(spec.paths[pathKey], spec);
    if (item.error) {
      uncertainServer = true;
      continue;
    }
    const pathItem = item.value, operation = pathItem[endpoint.http_method.toLowerCase()];
    const servers = operation?.servers ?? pathItem.servers ?? rootServers(spec);
    if (!Array.isArray(servers) || !servers.length) {
      uncertainServer = true;
      continue;
    }
    const { bases, uncertain } = serverBases(spec, servers);
    if (uncertain) uncertainServer = true;
    for (const base of bases) {
      serverKnown = true;
      if (base.origin !== target.origin) continue;
      const prefix = base.pathname.split("/").filter(Boolean).map((s) => {
        try {
          return decodeURIComponent(s);
        } catch {
          return s;
        }
      });
      const segs = target.segments;
      const head = segs.slice(0, prefix.length);
      if (head.some((s) => !("lit" in s))) {
        prefixUnresolved = true;
        continue;
      }
      if (segs.length < prefix.length || head.some((s, i) => s.lit !== prefix[i])) continue;
      serverMatches = true;
      let rest = segs.slice(prefix.length);
      if (rest.length === 1 && "lit" in rest[0] && rest[0].lit === "") rest = [];
      unmatchedRest ??= rest;
      const keys = pathKey.split("/").slice(1);
      if (pathKey === "/") keys.length = 0;
      if (keys.length !== rest.length || !operation || typeof operation !== "object") continue;
      const params = /* @__PURE__ */ Object.create(null);
      let ok = true;
      keys.forEach((key, i) => {
        if (!ok) return;
        const seg = rest[i], whole = /^\{([^}]+)\}$/.exec(key);
        if (whole) {
          if ("lit" in seg) params[whole[1]] = seg.lit;
          else if ("hole" in seg) params[whole[1]] = { $ca: "unknown", label: seg.hole, type: "str" };
          else params[whole[1]] = { $ca: "template", parts: seg.mixed };
          return;
        }
        if (!key.includes("{")) {
          ok = "lit" in seg && seg.lit === key;
          return;
        }
        if (!("lit" in seg)) {
          ok = false;
          return;
        }
        const names = [];
        const regex = new RegExp("^" + key.split(/(\{[^}]+\})/).map((p) => {
          const n = /^\{([^}]+)\}$/.exec(p);
          if (n) {
            names.push(n[1]);
            return "([^/]+)";
          }
          return p.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
        }).join("") + "$");
        const m = regex.exec(seg.lit);
        if (!m) {
          ok = false;
          return;
        }
        names.forEach((n, j) => {
          params[n] = m[j + 1];
        });
      });
      if (ok) matches.push({ pathKey, operation, pathItem, params, query: target.query, display: target.display });
    }
  }
  if (matches.length) {
    const exact = matches.filter((m) => !m.pathKey.includes("{"));
    const selected = exact.length ? exact : matches;
    if (new Set(selected.map((m) => m.pathKey)).size > 1) return { unknown: "Ambiguous templated path match." };
    return { match: selected[0] };
  }
  if (prefixUnresolved) return { unknown: "The server base path of the endpoint is a runtime value." };
  if (!serverKnown || uncertainServer) return { unknown: "Server identity or operation could not be resolved from the specification." };
  if (!serverMatches) return { bad: `Endpoint origin/base path does not match the declared API servers: ${target.display}` };
  if (evidenceOf(spec).partial) return { unknown: "Operation is outside the curated reference subset." };
  return { bad: `No declared operation matches ${endpoint.http_method} ${target.display}.${closestOperations(spec, unmatchedRest ?? [], endpoint.http_method)}` };
}
function closestOperations(spec, rest, method) {
  const wanted = method.toLowerCase(), METHODS = ["get", "put", "post", "delete", "patch", "head", "options", "trace"];
  const shape = [], withMethod = [];
  for (const key of Object.keys(spec.paths || {})) {
    const item = deref(spec.paths[key], spec);
    if (item.error || !item.value || typeof item.value !== "object") continue;
    const methods = METHODS.filter((m) => item.value[m]);
    const keys = key === "/" ? [] : key.split("/").slice(1);
    let n = 0;
    while (n < Math.min(keys.length, rest.length) && (/^\{[^}]+\}$/.test(keys[n]) || "lit" in rest[n] && rest[n].lit === keys[n])) n++;
    if (n === keys.length && n === rest.length && methods.length) shape.push(`${key} allows ${methods.map((m) => m.toUpperCase()).join(", ")}`);
    else if (n >= 1 && methods.includes(wanted)) withMethod.push({ key, n, gap: Math.abs(keys.length - rest.length) });
  }
  withMethod.sort((a, b) => b.n - a.n || a.gap - b.gap);
  const parts = [...shape.slice(0, 4), ...withMethod.slice(0, 3).map((w) => `${method.toUpperCase()} is declared on ${w.key}`)];
  return parts.length ? ` Closest declared operations (paths relative to the server): ${parts.join("; ")}.` : "";
}
function typesOf(s, spec) {
  if (s.type === void 0) return void 0;
  const list = Array.isArray(s.type) ? s.type : [s.type];
  return s.nullable === true ? [...list, "null"] : list;
}
function schemaProblems(schema, spec) {
  const errors = Object.keys(schema).filter((k) => !supported.has(k) && !k.startsWith("x-")).map((k) => `Unsupported schema constraint: ${k}`);
  if (schema.required !== void 0 && (!Array.isArray(schema.required) || schema.required.some((x) => typeof x !== "string"))) errors.push("Invalid required declaration.");
  if (schema.enum !== void 0 && !Array.isArray(schema.enum)) errors.push("Invalid enum declaration.");
  if (schema.type !== void 0) {
    const list = Array.isArray(schema.type) && (spec === void 0 || isOas31(spec)) ? schema.type : [schema.type];
    if (!list.length || list.some((t2) => !TYPES.includes(t2) && !(t2 === "null" && Array.isArray(schema.type)))) errors.push("Unsupported schema type.");
  }
  if (schema.properties !== void 0 && (!schema.properties || typeof schema.properties !== "object" || Array.isArray(schema.properties))) errors.push("Invalid properties declaration.");
  for (const key of ["nullable", "uniqueItems", "readOnly", "writeOnly"]) if (schema[key] !== void 0 && typeof schema[key] !== "boolean") errors.push("Invalid " + key + " declaration.");
  for (const key of ["exclusiveMinimum", "exclusiveMaximum"]) if (schema[key] !== void 0 && typeof schema[key] !== "boolean" && (typeof schema[key] !== "number" || !Number.isFinite(schema[key]))) errors.push("Invalid " + key + " declaration.");
  for (const key of ["minimum", "maximum", "multipleOf", "minLength", "maxLength", "minItems", "maxItems", "minProperties", "maxProperties"]) if (schema[key] !== void 0 && (typeof schema[key] !== "number" || !Number.isFinite(schema[key]))) errors.push("Invalid " + key + " declaration.");
  return errors;
}
function checkValue(value, raw, spec, label, serialized = false, depth = 0) {
  if (isMaybe(value)) return checkValue(value.value, raw, spec, label, serialized, depth);
  const c2 = empty();
  if (depth > 30) {
    c2.unknown.push(`${label}: schema depth limit`);
    return c2;
  }
  const resolved = deref(raw, spec);
  if (resolved.error) {
    c2.unknown.push(`${label}: ${resolved.error}`);
    return c2;
  }
  const s = resolved.value;
  c2.unknown.push(...schemaProblems(s, spec).map((x) => `${label}: ${x}`));
  if (c2.unknown.length) return c2;
  const types = typesOf(s, spec);
  if (isAbstract(value)) {
    const pyType = isTemplate(value) ? "str" : value.type;
    const jsonTypes = pyType ? PY_TO_JSON[pyType] : void 0;
    if (!serialized && types && jsonTypes && !jsonTypes.some((t2) => types.includes(t2))) c2.bad.push(`${label}: a Python ${pyType} value is sent where the contract expects ${types.join("/")}.`);
    else note(c2, `${label}: ${describe(value)} is not statically known; its value constraints are not checked`);
    return c2;
  }
  if (value === null && types?.includes("null")) return c2;
  let v = value;
  if (serialized && typeof v === "string" && types) {
    if ((types.includes("integer") || types.includes("number")) && !types.includes("string") && /^-?(?:0|[1-9]\d*)(?:\.\d+)?$/.test(v)) v = Number(v);
    if (types.includes("boolean") && !types.includes("string") && ["true", "false"].includes(v)) v = v === "true";
  }
  if (!types) {
    c2.unknown.push(`${label}: schema type is unspecified.`);
    return c2;
  }
  const matchesType = (type) => type === "string" ? typeof v === "string" : type === "integer" ? Number.isInteger(v) : type === "number" ? typeof v === "number" && Number.isFinite(v) : type === "boolean" ? typeof v === "boolean" : type === "array" ? Array.isArray(v) : type === "object" ? v !== null && typeof v === "object" && !Array.isArray(v) : type === "null" ? v === null : false;
  if (!types.some(matchesType)) {
    c2.bad.push(`${label}: expected ${types.join("/")}.`);
    return c2;
  }
  if (s.const !== void 0 && JSON.stringify(s.const) !== JSON.stringify(v)) c2.bad.push(`${label}: value differs from const.`);
  if (Array.isArray(s.enum) && !s.enum.some((x) => JSON.stringify(x) === JSON.stringify(v))) c2.bad.push(`${label}: value is outside enum.`);
  if (typeof s.format === "string" && v !== null) {
    if (INT_FORMATS[s.format] && typeof v === "number") {
      const [lo, hi] = INT_FORMATS[s.format];
      if (v < lo || v > hi) c2.bad.push(`${label}: outside ${s.format} range.`);
    } else if (!["float", "double", "int32", "int64"].includes(s.format) || typeof v !== "number") c2.unknown.push(`${label}: format ${s.format} is not validated.`);
  }
  if (typeof v === "number") {
    const exMin = typeof s.exclusiveMinimum === "number" ? s.exclusiveMinimum : s.exclusiveMinimum === true ? s.minimum : void 0;
    const exMax = typeof s.exclusiveMaximum === "number" ? s.exclusiveMaximum : s.exclusiveMaximum === true ? s.maximum : void 0;
    if (exMin !== void 0 && v <= exMin || s.minimum !== void 0 && s.exclusiveMinimum !== true && v < s.minimum) c2.bad.push(`${label}: below minimum.`);
    if (exMax !== void 0 && v >= exMax || s.maximum !== void 0 && s.exclusiveMaximum !== true && v > s.maximum) c2.bad.push(`${label}: above maximum.`);
    if (s.multipleOf !== void 0 && (s.multipleOf <= 0 || Math.abs(v / s.multipleOf - Math.round(v / s.multipleOf)) > 1e-9)) c2.bad.push(`${label}: violates multipleOf.`);
  }
  if (typeof v === "string") {
    const length = [...v].length;
    if (s.minLength !== void 0 && length < s.minLength || s.maxLength !== void 0 && length > s.maxLength) c2.bad.push(`${label}: invalid string length.`);
    if (typeof s.pattern === "string") {
      try {
        if (!new RegExp(s.pattern, "u").test(v)) c2.bad.push(`${label}: pattern mismatch.`);
      } catch {
        c2.unknown.push(`${label}: unsupported regular expression.`);
      }
    }
  }
  if (Array.isArray(v)) {
    if (s.minItems !== void 0 && v.length < s.minItems || s.maxItems !== void 0 && v.length > s.maxItems) c2.bad.push(`${label}: invalid array length.`);
    if (s.uniqueItems && concrete(v) && new Set(v.map((x) => JSON.stringify(x))).size !== v.length) c2.bad.push(`${label}: items are not unique.`);
    v.forEach((x, i) => merge(c2, checkValue(x, s.items, spec, `${label}[${i}]`, false, depth + 1)));
  } else if (v && typeof v === "object") {
    const count = Object.keys(v).length, sure = Object.values(v).filter((x) => !isMaybe(x)).length;
    if (s.minProperties !== void 0 && count < s.minProperties || s.maxProperties !== void 0 && sure > s.maxProperties) c2.bad.push(`${label}: invalid property count.`);
    else if (s.minProperties !== void 0 && sure < s.minProperties || s.maxProperties !== void 0 && count > s.maxProperties) c2.unknown.push(`${label}: property count depends on which optional entries are sent.`);
    for (const required of s.required || []) {
      if (!own(v, required) && !deref(s.properties?.[required], spec).value?.readOnly) c2.bad.push(`${label}: missing required property ${required}.`);
      else if (isMaybe(v[required])) c2.unknown.push(`${label}: required property ${required} is only sent on some code paths.`);
    }
    for (const [key, val] of Object.entries(v)) {
      if (own(s.properties, key)) {
        if (deref(s.properties[key], spec).value?.readOnly) c2.bad.push(`${label}.${key}: readOnly property sent in request.`);
        merge(c2, checkValue(val, s.properties[key], spec, `${label}.${key}`, false, depth + 1));
      } else if (s.additionalProperties === false) c2.bad.push(`${label}: undeclared property ${key}.`);
      else if (typeof s.additionalProperties === "object") merge(c2, checkValue(val, s.additionalProperties, spec, `${label}.${key}`, false, depth + 1));
      else if (s.additionalProperties === true) note(c2, `${label}: property ${key} is not declared; the schema explicitly allows additional properties`);
      else c2.unknown.push(`${label}: property ${key} is not declared; acceptance is undocumented.`);
    }
  }
  return c2;
}
function locate(layer, spec, ep) {
  const found = findOperation(spec, ep);
  if (found.match) return { match: found.match };
  return { row: found.bad && layer === "access_point" ? finish(layer, { bad: [found.bad], unknown: [] }, spec, "") : unknown(layer, found.unknown || found.bad || "Operation unresolved.") };
}
async function verifyAccessPoint({ claims, spec }) {
  return aggregateExtracted("access_point", claims, ofType(claims, "endpoint").map((ep) => {
    const l = locate("access_point", spec, ep);
    if (l.row) return l.row;
    const m = l.match, templated = typeof ep.endpoint !== "string";
    return result("access_point", "verified_correct", tier(spec), "OpenAPI servers + path + method", `${ep.http_method} ${m.display} matches the declared server and operation ${ep.http_method} ${m.pathKey}.` + (templated ? "\nNoncritical: runtime path values are assumed to stay within one path segment." : ""));
  }), "No HTTP calls in the supported extraction.");
}
function parameters(match, spec) {
  const map = /* @__PURE__ */ new Map(), errors = [];
  for (const list of [match.pathItem.parameters, match.operation.parameters]) {
    if (list !== void 0 && !Array.isArray(list)) {
      errors.push("Invalid parameter declaration.");
      continue;
    }
    for (const raw of list || []) {
      const p = deref(raw, spec);
      if (p.error) {
        errors.push(p.error);
        continue;
      }
      if (typeof p.value.name !== "string" || !["path", "query", "header", "cookie"].includes(p.value.in)) {
        errors.push("Invalid parameter name/location.");
        continue;
      }
      const key = p.value.in + ":" + (p.value.in === "header" ? p.value.name.toLowerCase() : p.value.name);
      map.set(key, p.value);
    }
  }
  return { values: [...map.values()], errors };
}
function fields(ep, via) {
  const container = ep.request?.[via], optional = /* @__PURE__ */ new Set();
  if (!container) return { values: {}, complete: ep.request_complete === true, optional };
  const shape = shapeOf(container, via);
  if (shape === null) return { values: {}, complete: true, optional };
  if (!shape || typeof shape !== "object" || Array.isArray(shape) || isAbstract(shape) || isMaybe(shape)) return { values: {}, complete: false, optional };
  const values = /* @__PURE__ */ Object.create(null);
  for (const [k, v] of Object.entries(shape)) {
    const key = via === "headers" ? k.toLowerCase() : k;
    values[key] = presentValue(v);
    if (isMaybe(v)) optional.add(key);
  }
  return { values, complete: true, optional };
}
function requestFields(ep, match) {
  const query = fields(ep, "params");
  for (const [key, value] of Object.entries(match.query.values)) {
    if (own(query.values, key)) query.complete = false;
    else query.values[key] = value;
  }
  if (!match.query.complete) query.complete = false;
  return { query, header: fields(ep, "headers"), cookie: fields(ep, "cookies"), path: { values: match.params, complete: true, optional: /* @__PURE__ */ new Set() } };
}
function securityNames(spec, operation) {
  const names = { header: /* @__PURE__ */ new Set(["authorization", "content-type", "accept", "user-agent"]), query: /* @__PURE__ */ new Set(), cookie: /* @__PURE__ */ new Set() };
  const requirements = operation.security ?? spec.security ?? [];
  const requiredNames = new Set((Array.isArray(requirements) ? requirements : []).flatMap((r) => Object.keys(r || {})));
  for (const [name, raw] of Object.entries(spec.components?.securitySchemes || {})) {
    if (!requiredNames.has(name)) continue;
    const s = deref(raw, spec).value;
    if (s?.type === "apiKey" && names[s.in] && typeof s.name === "string") names[s.in].add(s.in === "header" ? s.name.toLowerCase() : s.name);
  }
  return names;
}
function jsonSchemaOf(content) {
  if (!content || typeof content !== "object") return { found: false };
  const key = Object.keys(content).find((k) => JSON_MEDIA.test(k));
  return key ? { schema: content[key]?.schema, found: true } : { found: false };
}
function basicAuthShape(shape) {
  if (isOpaque(shape) && /HTTPBasicAuth$/.test(shape.type || "")) return true;
  return Array.isArray(shape) && shape.length === 2 && shape.every((v) => typeof v === "string" || isTemplate(v) || isOpaque(v) && (v.type == null || v.type === "str"));
}
async function verifyInputContract({ claims, spec }) {
  const rows = ofType(claims, "endpoint").map((ep) => {
    const l = locate("input_contract", spec, ep);
    if (l.row) return l.row;
    const m = l.match, c2 = empty(), pars = parameters(m, spec), sent = requestFields(ep, m);
    c2.unknown.push(...pars.errors);
    if (!ep.request || ep.request_complete !== true) c2.unknown.push("Request extraction is incomplete; required inputs cannot be established.");
    for (const p of pars.values) {
      const location = sent[p.in], key = p.in === "header" ? p.name.toLowerCase() : p.name;
      const val = location.values[key];
      if (val === void 0 || val === null) {
        if (p.required) (location.complete ? c2.bad : c2.unknown).push(`Missing required ${p.in} parameter ${p.name}.`);
      } else if (p.required && location.optional.has(key)) {
        c2.unknown.push(`Required ${p.in} parameter ${p.name} is only sent on some code paths.`);
      } else if (isAbstract(val)) {
        merge(c2, checkValue(val, p.schema, spec, `${p.in}.${p.name}`, true));
      } else {
        const schema = deref(p.schema, spec).value, defaultStyle = ["query", "cookie"].includes(p.in) ? "form" : "simple";
        const style = p.style ?? defaultStyle, explode = p.explode ?? style === "form";
        if (p.content || style !== defaultStyle || schema?.type === "object") c2.unknown.push(`Unsupported parameter serialization: ${p.name}`);
        else if (schema?.type === "array") {
          const items = typeof val === "string" ? explode ? [val] : val.split(",") : Array.isArray(val) && explode ? val : null;
          if (!items) c2.unknown.push(`Parameter ${p.name}: the value's form does not match the declared array serialization (explode=${explode}).`);
          else {
            if (schema.minItems !== void 0 && items.length < schema.minItems || schema.maxItems !== void 0 && items.length > schema.maxItems) c2.bad.push(`${p.in}.${p.name}: invalid array length.`);
            items.forEach((x, i) => merge(c2, checkValue(x, schema.items, spec, `${p.in}.${p.name}[${i}]`, true)));
          }
        } else merge(c2, checkValue(val, p.schema, spec, `${p.in}.${p.name}`, true));
      }
    }
    const authNames = securityNames(spec, m.operation);
    for (const loc of ["query", "header", "cookie"]) {
      if (!sent[loc].complete) c2.unknown.push(`${loc} dictionary has unresolved keys.`);
      const declared = new Set(pars.values.filter((p) => p.in === loc).map((p) => loc === "header" ? p.name.toLowerCase() : p.name));
      for (const key of Object.keys(sent[loc].values)) if (!declared.has(key) && !authNames[loc].has(key)) {
        if (loc === "header") note(c2, `Undeclared header ${key}; acceptance is undocumented`);
        else c2.unknown.push(`Undeclared ${loc} parameter ${key}; acceptance is undocumented.`);
      }
    }
    const auth = ep.request?.auth, authShape = auth?.provided ? shapeOf(auth, "auth") : void 0;
    if (auth?.provided && authShape !== null && !basicAuthShape(authShape)) c2.unknown.push("Custom/dynamic request authentication is outside the supported subset.");
    const rb = deref(m.operation.requestBody, spec);
    const body = ep.request?.json, form = ep.request?.data;
    const bodyShape = body?.provided ? shapeOf(body, "json") : void 0, formShape = form?.provided ? shapeOf(form, "data") : void 0;
    if (body?.provided && bodyShape !== null) {
      const contentType = sent.header.values["content-type"];
      if (contentType !== void 0 && typeof contentType !== "string") c2.unknown.push("Request Content-Type is unresolved.");
      else if (typeof contentType === "string" && contentType.split(";")[0].trim().toLowerCase() !== "application/json") c2.bad.push("JSON body sent with a non-JSON Content-Type.");
    }
    if (form?.provided && formShape !== null) c2.unknown.push("Form/raw body encoding is unsupported.");
    if (m.operation.requestBody) {
      if (rb.error) c2.unknown.push(rb.error);
      else {
        if (rb.value.required && (!body?.provided || bodyShape === null) && !(form?.provided && formShape !== null)) c2.bad.push("Required request body is missing.");
        if (body?.provided && bodyShape !== null) {
          const { schema } = jsonSchemaOf(rb.value.content);
          if (!schema) c2.unknown.push("No JSON request schema available.");
          else if (isAbstract(bodyShape) || bodyShape === void 0) c2.unknown.push("Request body is unresolved.");
          else merge(c2, checkValue(bodyShape, schema, spec, "body"));
        }
      }
    } else if (body?.provided && bodyShape !== null) c2.unknown.push("Code sends a JSON body with no declared request-body contract.");
    return finish("input_contract", c2, spec, `Required inputs, locations and supported value constraints checked for ${ep.call_id} (${m.pathKey}).`);
  });
  return aggregateExtracted("input_contract", claims, rows, "No HTTP calls; no input contract to check.");
}
function schemaView(raw, spec, depth = 0) {
  const v = { properties: {}, required: /* @__PURE__ */ new Set(), additional: void 0, nullable: false, writeOnly: false, problems: [] };
  if (depth > 20) {
    v.problems.push("Schema composition depth limit.");
    return v;
  }
  let s = raw;
  if (isOas31(spec) && s && typeof s === "object" && own(s, "$ref") && Object.keys(s).some((k) => !["$ref", "description", "summary"].includes(k))) {
    const { $ref, ...siblings } = s;
    s = { allOf: [{ $ref }, siblings] };
  }
  const r = deref(s, spec);
  if (r.error) {
    v.problems.push(r.error);
    return v;
  }
  s = r.value;
  const { allOf, oneOf, anyOf, discriminator, ...rest } = s;
  const union = oneOf ?? anyOf;
  const structural = Object.keys(rest).filter((k) => ["properties", "items", "additionalProperties", "required"].includes(k));
  if (union !== void 0 && (structural.length || allOf !== void 0 || !Array.isArray(union))) {
    v.problems.push("Unsupported schema constraint: " + (oneOf !== void 0 ? "oneOf" : "anyOf") + " combined with other structure.");
    return v;
  }
  if (union !== void 0) {
    v.alternatives = union;
    v.nullable = rest.nullable === true || Array.isArray(rest.type) && rest.type.includes("null");
    return v;
  }
  v.problems.push(...schemaProblems(rest, spec));
  v.types = typesOf(rest, spec);
  v.nullable = v.types?.includes("null") ?? false;
  v.writeOnly = rest.writeOnly === true;
  Object.assign(v.properties, rest.properties || {});
  for (const k of rest.required || []) v.required.add(k);
  v.additional = rest.additionalProperties;
  v.items = rest.items;
  if (allOf !== void 0) {
    if (!Array.isArray(allOf)) {
      v.problems.push("Invalid allOf declaration.");
      return v;
    }
    for (const member of allOf) {
      const m = schemaView(member, spec, depth + 1);
      v.problems.push(...m.problems);
      if (m.alternatives) {
        v.problems.push("Unsupported schema constraint: union inside allOf.");
        continue;
      }
      if (m.types) v.types = v.types ? v.types.filter((t2) => m.types.includes(t2) || t2 === "number" && m.types.includes("integer")) : m.types;
      Object.assign(v.properties, m.properties);
      m.required.forEach((k) => v.required.add(k));
      v.items ??= m.items;
      if (m.nullable && (!v.types || v.types.includes("null"))) v.nullable = true;
    }
    if (v.additional === false) v.additional = void 0;
  }
  if (!v.types && Object.keys(v.properties).length) v.types = ["object"];
  return v;
}
function stepInto(view, key, spec, optional) {
  const c2 = empty();
  if (view.problems.length) {
    c2.unknown.push(...view.problems);
    return { c: c2, next: [] };
  }
  if (view.alternatives) {
    const results = view.alternatives.map((a) => stepInto(schemaView(a, spec), key, spec, optional));
    const ok = results.filter((r) => !r.c.bad.length && !r.c.unknown.length);
    if (ok.length === results.length) {
      results.forEach((r) => merge(c2, { bad: [], unknown: [], notes: r.c.notes }));
      return { c: c2, next: results.flatMap((r) => r.next) };
    }
    if (results.every((r) => r.c.bad.length)) {
      c2.bad.push(...new Set(results.flatMap((r) => r.c.bad)));
      return { c: c2, next: [] };
    }
    c2.unknown.push(`Response field ${JSON.stringify(key)} is documented in only some schema alternatives.`);
    return { c: c2, next: [] };
  }
  if (!view.types) {
    c2.unknown.push("Response schema type is unspecified.");
    return { c: c2, next: [] };
  }
  if (view.nullable) note(c2, "a response container on this path can be null");
  if (typeof key === "number" || key === "*" && view.types.includes("array") && !view.types.includes("object")) {
    if (!view.types.includes("array")) {
      c2.bad.push("Array indexing used on a non-array response.");
      return { c: c2, next: [] };
    }
    if (typeof key === "number" && !Number.isInteger(key)) {
      c2.unknown.push("Non-integer response index.");
      return { c: c2, next: [] };
    }
    if (view.items === void 0) {
      c2.unknown.push("Array item schema is unspecified.");
      return { c: c2, next: [] };
    }
    return { c: c2, next: [view.items] };
  }
  if (key === "*") {
    c2.unknown.push("Dynamic response field is unresolved.");
    return { c: c2, next: [] };
  }
  if (!view.types.includes("object")) {
    c2.bad.push(view.types.includes("array") ? `String field ${key} read directly from an array.` : `Field ${key} read from a scalar response.`);
    return { c: c2, next: [] };
  }
  if (!own(view.properties, key)) {
    if (view.additional === false) c2.bad.push(`Response field ${key} is forbidden by the closed schema.`);
    else c2.unknown.push(`Response field ${key} is not documented; schema allows unspecified properties.`);
    return { c: c2, next: [] };
  }
  if (!optional && !view.required.has(key)) note(c2, `response field ${key} is optional in the contract; presence is not guaranteed`);
  const child = schemaView(view.properties[key], spec);
  if (child.writeOnly) c2.unknown.push(`Response field ${key} is writeOnly.`);
  return { c: c2, next: [view.properties[key]] };
}
function checkOutputPath(path, raw, spec, optional = false) {
  const c2 = empty();
  let schemas = [raw];
  for (const [i, key] of path.entries()) {
    const steps = schemas.map((s) => stepInto(schemaView(s, spec), key, spec, optional && i === path.length - 1));
    steps.forEach((s) => merge(c2, s.c));
    if (c2.bad.length || c2.unknown.length) return c2;
    schemas = steps.flatMap((s) => s.next);
  }
  return c2;
}
async function verifyOutputContract({ claims, spec, code }, runPyright, allowPyright = true) {
  const outputs = ofType(claims, "output_field");
  if (!outputs.length) return aggregateExtracted("output_contract", claims, [], "No tracked response-field accesses.");
  const rows = [];
  for (const f of outputs) {
    const ep = ofType(claims, "endpoint").find((e) => e.call_id === f.call_id);
    if (!ep) {
      rows.push(unknown("output_contract", "Response access is not linked to an HTTP operation."));
      continue;
    }
    const l = locate("output_contract", spec, ep);
    if (l.row) {
      rows.push(l.row);
      continue;
    }
    const responses = l.match.operation.responses || {};
    const success = Object.entries(responses).filter(([k]) => /^2\d\d$/.test(k) || k === "2XX");
    if (!success.length) {
      rows.push(unknown("output_contract", "No documented success-response schema; a default/error response is insufficient."));
      continue;
    }
    const checks = success.map(([status, raw]) => {
      const r = deref(raw, spec);
      if (r.error) return { bad: [], unknown: [r.error] };
      const { schema } = jsonSchemaOf(r.value.content);
      if (!schema) return { bad: [], unknown: [`No JSON schema for success status ${status}.`] };
      return checkOutputPath(Array.isArray(f.path) ? f.path : [f.field], schema, spec, f.optional_access === true);
    });
    const combined = empty();
    if (checks.every((c2) => c2.bad.length)) combined.bad.push(...checks.flatMap((c2) => c2.bad));
    else {
      combined.unknown.push(...checks.flatMap((c2) => c2.unknown));
      if (checks.some((c2) => c2.bad.length)) combined.unknown.push("Field validity depends on an unresolved success status.");
    }
    checks.forEach((c2) => {
      if (c2.notes?.length) (combined.notes ||= []).push(...c2.notes);
    });
    rows.push(finish("output_contract", combined, spec, `Response path ${JSON.stringify(f.path || [f.field])} is documented for ${f.call_id} (${l.match.pathKey}).`));
  }
  const verdict = aggregateExtracted("output_contract", claims, rows, "No output checks.");
  if (verdict.state === "unverifiable" && code && runPyright && allowPyright) {
    try {
      const p = parsePyright(await runPyright({ python: code }), code);
      verdict.evidence_detail += "\n" + (p.error ? `Pyright unavailable: ${p.error}` : "Pyright cannot establish untyped JSON response contracts; result remains unverifiable.");
    } catch (e) {
      verdict.evidence_detail += `
Pyright unavailable: ${String(e)}`;
    }
  }
  return verdict;
}
function authCheck(name, scopes, ep, match, spec) {
  const c2 = empty(), resolved = deref(spec.components?.securitySchemes?.[name], spec);
  if (resolved.error) {
    c2.unknown.push(`Security scheme ${name}: ${resolved.error}`);
    return c2;
  }
  const s = resolved.value, sent = requestFields(ep, match);
  let val, complete = false;
  if (Array.isArray(scopes) && scopes.length) note(c2, `required scopes (${scopes.join(", ")}) belong to the ${name} token and cannot be checked statically; the credential is assumed to carry them`);
  if (s.type === "apiKey" && ["header", "query", "cookie"].includes(s.in)) {
    const loc = sent[s.in];
    const key = s.in === "header" ? String(s.name).toLowerCase() : s.name;
    val = loc.values[key];
    complete = loc.complete;
    if (val !== void 0 && loc.optional.has(key)) {
      c2.unknown.push(`Credential ${name} is only sent on some code paths.`);
      return c2;
    }
    if (isAbstract(val)) note(c2, `credential ${name} is placed as documented; its runtime value is not tested`);
  } else if (s.type === "http" && ["bearer", "basic"].includes(s.scheme?.toLowerCase()) || s.type === "oauth2" || s.type === "openIdConnect") {
    const scheme = s.type === "http" ? s.scheme.toLowerCase() : "bearer", label = s.type === "http" ? s.scheme : `${s.type} Bearer token`;
    val = sent.header.values.authorization;
    complete = sent.header.complete;
    if (val !== void 0 && sent.header.optional.has("authorization")) {
      c2.unknown.push(`The ${label} credential is only sent on some code paths.`);
      return c2;
    }
    if (val === void 0 && ep.request?.auth?.provided) {
      if (scheme === "basic" && basicAuthShape(shapeOf(ep.request.auth, "auth"))) return note(c2, `basic credentials are supplied through requests auth; their validity is not tested`);
      c2.unknown.push("Authentication adapter/value could not be established.");
      return c2;
    }
    if (typeof val === "string") {
      if (!SCHEME_PREFIX[scheme].test(val.trim() ? val : "")) c2.bad.push(`Authorization header does not match ${label}.`);
    } else if (isTemplate(val)) {
      const first = val.parts[0];
      if (typeof first !== "string") c2.unknown.push(`The Authorization scheme is a runtime value; ${label} placement cannot be established.`);
      else if (scheme === "bearer" ? !/^Bearer\s+$/i.test(first) && !/^Bearer\s+\S/i.test(first) : !/^Basic\s+/i.test(first)) c2.bad.push(`Authorization header does not match ${label}.`);
      else note(c2, `the ${label} credential is a runtime value; its validity is not tested`);
      return c2;
    } else if (isOpaque(val)) {
      c2.unknown.push(`Credential ${name} has an unresolved runtime value; the ${label} scheme cannot be established.`);
      return c2;
    }
  } else {
    c2.unknown.push(`Unsupported authentication scheme/scopes: ${name} (${s.type}).`);
    return c2;
  }
  if (val === void 0 || val === null) (complete ? c2.bad : c2.unknown).push(`Required credential ${name} is absent from the request.`);
  else if (typeof val === "string" && !val.trim()) c2.bad.push(`Credential ${name} is empty or invalid.`);
  else if (!isAbstract(val) && typeof val !== "string") c2.bad.push(`Credential ${name} is empty or invalid.`);
  return c2;
}
async function verifyContextual({ claims, spec }) {
  const rows = ofType(claims, "endpoint").map((ep) => {
    const l = locate("contextual", spec, ep);
    if (l.row) return l.row;
    const m = l.match, security = m.operation.security ?? spec.security ?? [];
    if (!Array.isArray(security)) return unknown("contextual", "Invalid security requirements.");
    if (m.operation.deprecated) return unknown("contextual", "Operation is deprecated; task-specific acceptability needs review.");
    if (!security.length || security.some((s) => s && typeof s === "object" && !Array.isArray(s) && !Object.keys(s).length)) return result("contextual", "not_applicable", "none", "OpenAPI operation security", "No authentication requirement for this operation. Unused security definitions are not requirements.");
    const alternatives = security.map((requirement) => {
      const c2 = empty();
      if (!requirement || typeof requirement !== "object" || Array.isArray(requirement)) {
        c2.unknown.push("Invalid security alternative.");
        return c2;
      }
      for (const [name, scopes] of Object.entries(requirement)) merge(c2, authCheck(name, scopes, ep, m, spec));
      return c2;
    });
    const satisfied = alternatives.find((c2) => !c2.bad.length && !c2.unknown.length);
    if (satisfied) return finish("contextual", { bad: [], unknown: [], notes: satisfied.notes }, spec, "Required authentication placement and static shape match one security alternative. Credential validity is not tested.");
    if (alternatives.every((c2) => c2.bad.length)) return finish("contextual", { bad: alternatives.flatMap((c2) => c2.bad), unknown: [] }, spec, "");
    return unknown("contextual", alternatives.flatMap((c2) => [...c2.bad, ...c2.unknown]).join("\n"));
  });
  return aggregateExtracted("contextual", claims, rows, "No HTTP calls requiring contextual checks.");
}
var empty, note, merge, own, evidenceOf, isMarker, isOpaque, isTemplate, isAbstract, isMaybe, presentValue, templateText, describe, PY_TO_JSON, isOas31, HOLE, supported, TYPES, INT_FORMATS, JSON_MEDIA, SCHEME_PREFIX;
var init_openApiVerifier = __esm({
  "src/openApiVerifier.ts"() {
    "use strict";
    init_verificationTypes();
    init_pyrightRunner();
    empty = () => ({ bad: [], unknown: [] });
    note = (c2, text3) => {
      (c2.notes ||= []).push(text3);
      return c2;
    };
    merge = (a, b) => {
      a.bad.push(...b.bad);
      a.unknown.push(...b.unknown);
      if (b.notes?.length) (a.notes ||= []).push(...b.notes);
      return a;
    };
    own = (v, k) => v != null && typeof v === "object" && Object.hasOwn(v, k);
    evidenceOf = (spec) => spec && typeof spec === "object" && spec["x-confidence-evidence"] || {};
    isMarker = (v, kind) => v != null && typeof v === "object" && !Array.isArray(v) && v.$ca === kind;
    isOpaque = (v) => isMarker(v, "unknown");
    isTemplate = (v) => isMarker(v, "template");
    isAbstract = (v) => isOpaque(v) || isTemplate(v);
    isMaybe = (v) => isMarker(v, "maybe");
    presentValue = (v) => isMaybe(v) ? v.value : v;
    templateText = (t2) => (t2.parts || []).map((p) => typeof p === "string" ? p : `{${p.hole}}`).join("");
    describe = (v) => isTemplate(v) ? `template "${templateText(v)}"` : isOpaque(v) ? `runtime value ${v.label || ""}`.trim() : JSON.stringify(v);
    PY_TO_JSON = { str: ["string"], int: ["integer", "number"], float: ["number"], bool: ["boolean"], dict: ["object"], list: ["array"], NoneType: ["null"] };
    isOas31 = (spec) => /^3\.1\./.test(spec?.openapi || "");
    HOLE = "\0";
    supported = /* @__PURE__ */ new Set([
      "type",
      "properties",
      "required",
      "items",
      "additionalProperties",
      "enum",
      "nullable",
      "minimum",
      "maximum",
      "exclusiveMinimum",
      "exclusiveMaximum",
      "minLength",
      "maxLength",
      "pattern",
      "minItems",
      "maxItems",
      "uniqueItems",
      "minProperties",
      "maxProperties",
      "multipleOf",
      "title",
      "description",
      "default",
      "example",
      "examples",
      "deprecated",
      "readOnly",
      "writeOnly",
      "xml",
      "externalDocs",
      "format",
      // JSON Schema 2020-12 annotations used by OpenAPI 3.1 documents.
      "const",
      "$schema",
      "$id",
      "$comment",
      "$anchor",
      "contentMediaType",
      "contentEncoding",
      "$defs"
    ]);
    TYPES = ["object", "array", "string", "integer", "number", "boolean"];
    INT_FORMATS = { int32: [-(2 ** 31), 2 ** 31 - 1], int64: [Number.MIN_SAFE_INTEGER, Number.MAX_SAFE_INTEGER] };
    JSON_MEDIA = /^application\/(?:[\w.+-]+\+)?json\s*(?:;.*)?$/i;
    SCHEME_PREFIX = { bearer: /^Bearer\s+\S/i, basic: /^Basic\s+[A-Za-z0-9+/]+=*$/i };
  }
});

// src/verificationPolicy.ts
function computeEwcs({ layer_results, task_id = "candidate", extraction_complete = false, failed_layers = [] }) {
  const acc = new EWCSAccumulator(task_id, extraction_complete, failed_layers);
  for (const r of layer_results) acc.record(r);
  return acc.finalise();
}
function makeDecision(report, correctionAttempts = 0, policy = DEFAULT_POLICY) {
  try {
    if (!report || !Array.isArray(report.contributions)) return "abstain";
    const acc = new EWCSAccumulator(report.task_id);
    for (const c2 of report.contributions) acc.record({ ...c2, evidence_source: "report", evidence_detail: "", hallucination_type: null });
    const checked = acc.finalise();
    if (checked.has_incorrect_layer) return correctionAttempts < 1 ? "correct" : "abstain";
    if (!Array.isArray(report.missing_layers) || report.missing_layers.length || !Array.isArray(report.failed_layers) || report.failed_layers.length || checked.missing_layers.length || checked.ewcs === null || !Number.isFinite(report.ewcs) || report.ewcs !== checked.ewcs) return "abstain";
    if (policy.uncertainty_gate !== false && (report.extraction_complete !== true || checked.unverifiable_layers.length)) return "abstain";
    return checked.ewcs >= policy.deliver_threshold ? "deliver" : checked.ewcs >= policy.flag_threshold ? "deliver_with_flag" : "abstain";
  } catch {
    return "abstain";
  }
}
function presentReport({ code, ewcs_report, decision, policy = DEFAULT_POLICY }) {
  const safeCode = typeof code === "string" ? code : "";
  if (!ewcs_report || typeof ewcs_report !== "object") {
    return {
      report: "### Confidence Agent Report\n\n**Decision:** abstain\n\n**Reason:** Malformed or missing EWCS report.\n\nCode withheld pending successful verification.",
      decision: "abstain",
      code_included: false
    };
  }
  const show = (v) => typeof v === "number" && Number.isFinite(v) ? round(v) : "undefined";
  const checked = makeDecision(ewcs_report, 0, policy);
  const candidateMatches = ewcs_report.candidate_hash === hashCode(safeCode);
  const allowed = candidateMatches && ["deliver", "deliver_with_flag"].includes(checked) && ["deliver", "deliver_with_flag"].includes(decision);
  const actual = allowed ? checked : checked === "correct" && decision !== "abstain" ? "correct" : "abstain";
  const reason = allowed ? null : !candidateMatches ? typeof ewcs_report.candidate_hash !== "string" ? "This score report is not bound to any code (no candidate_hash). Reports assembled from the individual layer tools can be inspected but cannot authorize delivery; only verify_candidate binds a report to the exact code." : "This score report belongs to different code (candidate_hash mismatch). The code must be verified exactly as it will be delivered." : checked === "correct" ? "A layer verified a contradiction; a correction is required." : !["deliver", "deliver_with_flag"].includes(decision) ? `The caller requested ${decision}.` : "The decision policy withheld delivery (see unverifiable layers, extraction and thresholds below).";
  const lines = [
    "### Confidence Agent Report",
    "",
    `**Decision:** ${actual}`,
    ...reason ? [`**Reason:** ${reason}`] : [],
    `**EWCS:** ${ewcs_report.ewcs ?? "undefined (no applicable evidence)"} (signed: ${ewcs_report.signed_score ?? "undefined"}, applicable weight: ${ewcs_report.total_applicable_weight ?? "undefined"})`,
    "",
    "| Layer | State | Tier | Weight | Factor | Positive | Signed |",
    "|---|---|---|---|---|---|---|"
  ];
  for (const c2 of Array.isArray(ewcs_report.contributions) ? ewcs_report.contributions : []) {
    if (!c2 || typeof c2 !== "object") continue;
    lines.push(`| ${c2.layer ?? "?"} | ${c2.state ?? "?"} | ${c2.tier ?? "?"} | ${c2.weight ?? "?"} | ${c2.tier_factor ?? "?"} | ${show(c2.positive_contribution)} | ${show(c2.signed_contribution)} |`);
  }
  lines.push("", "Scope: API-claim and static evidence only. EWCS is not a probability of correctness. Task behavior has not been independently checked by this verifier.");
  lines.push("", `Policy ${POLICY_VERSION}: thresholds ${policy.deliver_threshold}/${policy.flag_threshold}, uncertainty gate ${policy.uncertainty_gate !== false ? "on" : "OFF (exploratory)"}.`);
  if (Array.isArray(ewcs_report.layer_results) && ewcs_report.layer_results.length) {
    lines.push("", "Evidence:", "");
    for (const r of ewcs_report.layer_results) {
      if (!r || typeof r !== "object") continue;
      const detail = typeof r.evidence_detail === "string" ? r.evidence_detail : "(no detail)";
      lines.push(`- ${r.layer ?? "?"}: ${detail.replace(/\n/g, " ")}`);
    }
  }
  if (Array.isArray(ewcs_report.missing_layers) && ewcs_report.missing_layers.length) lines.push("", `Missing layers: ${ewcs_report.missing_layers.join(", ")}`);
  if (Array.isArray(ewcs_report.unverifiable_layers) && ewcs_report.unverifiable_layers.length) lines.push("", `Unverifiable layers: ${ewcs_report.unverifiable_layers.join(", ")}`);
  if (!ewcs_report.extraction_complete) lines.push("", "Extraction was incomplete or failed.");
  if (actual === "deliver_with_flag") lines.push("", "Flag: some checks rely on supporting static or package metadata evidence; the code was not executed.");
  if (allowed) {
    const fence = "`".repeat(Math.max(3, ...(safeCode.match(/`+/g) || []).map((s) => s.length + 1)));
    lines.push("", fence + "python", safeCode, fence);
  } else lines.push("", "Code withheld pending successful verification.");
  return { report: lines.join("\n"), decision: actual, code_included: allowed };
}
var round, EWCSAccumulator, POLICY_VERSION, DEFAULT_POLICY;
var init_verificationPolicy = __esm({
  "src/verificationPolicy.ts"() {
    "use strict";
    init_verificationTypes();
    round = (v) => Math.round(v * 1e4) / 1e4;
    EWCSAccumulator = class {
      constructor(taskId, extractionComplete = false, failed = []) {
        this.taskId = taskId;
        this.extractionComplete = extractionComplete;
        this.failed = failed;
      }
      taskId;
      extractionComplete;
      failed;
      results = /* @__PURE__ */ new Map();
      report = null;
      get isComplete() {
        return this.report !== null;
      }
      record(r) {
        if (this.report) throw new Error("Cannot record after finalise().");
        if (!Object.hasOwn(LAYER_WEIGHTS, r.layer)) throw new Error(`Unknown layer: ${r.layer}`);
        if (this.results.has(r.layer)) throw new Error(`Duplicate layer: ${r.layer}`);
        if (r.weight !== LAYER_WEIGHTS[r.layer]) throw new Error(`Incorrect weight for ${r.layer}`);
        if (!["verified_correct", "verified_incorrect", "unverifiable", "not_applicable"].includes(r.state)) throw new Error(`Invalid state: ${r.state}`);
        if (!Object.hasOwn(TIER_FACTORS, r.tier)) throw new Error(`Invalid tier: ${r.tier}`);
        if (r.state.startsWith("verified_") && r.tier === "none") throw new Error("Verified results require evidence.");
        if (["unverifiable", "not_applicable"].includes(r.state) && r.tier !== "none") throw new Error("Unverified results must use tier none.");
        this.results.set(r.layer, { ...r });
      }
      finalise() {
        if (this.report) return structuredClone(this.report);
        const missing = ALL_LAYERS.filter((l) => !this.results.has(l));
        const rows = ALL_LAYERS.map((l) => this.results.get(l) || result(l, "unverifiable", "none", "controller", "Required layer did not report."));
        const contributions = rows.map((r) => {
          const factor = TIER_FACTORS[r.tier];
          return {
            layer: r.layer,
            state: r.state,
            tier: r.tier,
            weight: r.weight,
            tier_factor: factor,
            positive_contribution: r.state === "verified_correct" ? round(r.weight * factor) : 0,
            signed_contribution: r.state === "verified_correct" ? round(r.weight * factor) : r.state === "verified_incorrect" ? round(-r.weight * factor) : 0
          };
        });
        const applicable = contributions.filter((c2) => c2.state !== "not_applicable");
        const total = applicable.reduce((s, c2) => s + c2.weight, 0), positive = round(applicable.reduce((s, c2) => s + c2.positive_contribution, 0));
        this.report = {
          task_id: this.taskId,
          ewcs: total ? round(positive / total) : null,
          signed_score: total ? round(applicable.reduce((s, c2) => s + c2.signed_contribution, 0) / total) : null,
          has_incorrect_layer: applicable.some((c2) => c2.state === "verified_incorrect"),
          total_applicable_weight: total,
          positive_weight: positive,
          contributions,
          missing_layers: missing,
          extraction_complete: this.extractionComplete,
          failed_layers: [...this.failed],
          unverifiable_layers: rows.filter((r) => r.state === "unverifiable").map((r) => r.layer),
          layer_results: rows
        };
        return structuredClone(this.report);
      }
    };
    POLICY_VERSION = "2026-09-25.1";
    DEFAULT_POLICY = Object.freeze({ uncertainty_gate: true, deliver_threshold: 0.85, flag_threshold: 0.6 });
  }
});

// src/verificationController.ts
async function verifyCandidate(request, deps = {}) {
  const code = request.code, candidate_hash = hashCode(code), snapshot = structuredClone(request.spec), bindings = structuredClone(request.input_bindings || {});
  let extraction;
  try {
    extraction = await (deps.extract || extractClaims)({ code, input_bindings: bindings });
  } catch (e) {
    extraction = { claims: [], complete: false, issues: [], error: String(e) };
  }
  if (!extraction || !Array.isArray(extraction.claims) || typeof extraction.complete !== "boolean") extraction = { claims: [], complete: false, issues: [], error: "Malformed extractor response." };
  if (extraction.candidate_hash && extraction.candidate_hash !== candidate_hash) extraction = { claims: [], complete: false, issues: [], error: "Extraction candidate hash mismatch." };
  if (extraction.error) extraction.complete = false;
  const packages = /* @__PURE__ */ Object.create(null);
  for (const imp of ofType(extraction.claims, "import")) {
    const name = String(imp.library || "").split(".")[0];
    if (imp.stdlib || imp.local || Object.hasOwn(packages, name)) continue;
    try {
      packages[name] = await (deps.lookupPackage || ((name2) => queryPypi({ library_name: name2 })))(name);
    } catch (e) {
      packages[name] = { exists: null, status: "unverifiable", summary: String(e) };
    }
  }
  let pyright = null, pyrightPromise = null;
  const run = deps.runPyright || createPyrightRunner();
  const cached = (p) => {
    if (p.python !== code) throw new Error("Checker must analyze the exact candidate.");
    if (!pyrightPromise) pyrightPromise = run(p).then((r) => {
      pyright = r;
      return r;
    });
    return pyrightPromise;
  };
  const claims = extraction.claims;
  const actions = {
    interface: () => verifyInterface({ claims, pypi_data: packages }),
    identifier: () => verifyIdentifier(code, cached, deps.allowPyright !== false, extraction),
    access_point: () => verifyAccessPoint({ claims, spec: snapshot }),
    input_contract: () => verifyInputContract({ claims, spec: snapshot }),
    output_contract: () => verifyOutputContract({ claims, spec: snapshot, code }, cached, deps.allowPyright !== false),
    contextual: () => verifyContextual({ claims, spec: snapshot })
  };
  const failed = [], layers = [];
  const limits = extractionLimits(extraction);
  for (const layer of ALL_LAYERS) {
    try {
      let r = await actions[layer]();
      if (!r || r.layer !== layer) throw new Error("Missing/mismatched layer result.");
      if (limits.layers.has(layer) && r.state === "not_applicable") r = unknown(layer, "Extraction was incomplete for this layer; absence of relevant claims does not establish inapplicability.");
      layers.push(r);
    } catch (e) {
      failed.push(layer);
      layers.push(unknown(layer, `Required verifier failed: ${String(e)}`));
    }
  }
  const ewcs_report = computeEwcs({ layer_results: layers, task_id: request.task_id, extraction_complete: extraction.complete, failed_layers: failed });
  ewcs_report.candidate_hash = candidate_hash;
  return {
    candidate_hash,
    spec_hash: hashCode(JSON.stringify(snapshot ?? null)),
    bindings_hash: hashCode(JSON.stringify(bindings)),
    extraction,
    layers,
    ewcs_report,
    decision: makeDecision(ewcs_report, 0, deps.policy ?? DEFAULT_POLICY),
    evidence: { packages, pyright }
  };
}
async function runIntervention(request, deps = {}) {
  const frozen = { ...request, spec: structuredClone(request.spec), input_bindings: structuredClone(request.input_bindings || {}) };
  const attempts = [{ code: request.code, verification: await verifyCandidate(frozen, deps) }];
  let correction_error = null;
  if (attempts[0].verification.decision === "correct" && deps.correct) {
    try {
      const revised = await deps.correct({ code: request.code, verification: structuredClone(attempts[0].verification), spec: structuredClone(frozen.spec), input_bindings: structuredClone(frozen.input_bindings) });
      if (typeof revised !== "string" || !revised.trim()) throw new Error("Correction produced no code.");
      attempts.push({ code: revised, verification: await verifyCandidate({ ...frozen, code: revised }, deps) });
    } catch (e) {
      correction_error = String(e);
    }
  }
  const last = attempts[attempts.length - 1], raw = makeDecision(last.verification.ewcs_report, attempts.length - 1, deps.policy ?? DEFAULT_POLICY);
  const decision = raw === "correct" || correction_error ? "abstain" : raw;
  const rendered = presentReport({ code: last.code, ewcs_report: last.verification.ewcs_report, decision, policy: deps.policy ?? DEFAULT_POLICY });
  return {
    decision: rendered.decision,
    delivered_code: rendered.code_included ? last.code : null,
    report: rendered.report,
    attempts,
    correction_attempted: attempts[0].verification.decision === "correct" && !!deps.correct,
    correction_error
  };
}
var init_verificationController = __esm({
  "src/verificationController.ts"() {
    "use strict";
    init_claimExtractor();
    init_packageEvidence();
    init_pyrightRunner();
    init_openApiVerifier();
    init_verificationPolicy();
    init_verificationTypes();
  }
});

// src/bundledReferences.ts
var TOOLBOX_VERSION, BUNDLED_REFERENCES;
var init_bundledReferences = __esm({
  "src/bundledReferences.ts"() {
    "use strict";
    TOOLBOX_VERSION = "1.6.0";
    BUNDLED_REFERENCES = { "jsonplaceholder-posts": { "openapi": "3.0.3", "info": { "title": "JSONPlaceholder posts: reviewed partial reference", "version": "2026-09-24.1" }, "servers": [{ "url": "https://jsonplaceholder.typicode.com" }], "x-confidence-evidence": { "kind": "curated", "partial": true, "source_url": "https://jsonplaceholder.typicode.com/guide/", "source_urls": ["https://jsonplaceholder.typicode.com/guide/", "https://jsonplaceholder.typicode.com/"], "prepared_at": "2026-09-24", "reviewed_at": "2026-09-24", "review_method": "Manual comparison by coding assistant with provider guide and routes page; not provider certification or independent team approval.", "coverage": ["GET /posts without filters", "GET /posts/1"], "note": "Partial secondary reference at tier 2, not provider-published OpenAPI. Example property types are modeled; universal field presence is not asserted. Other operations and supplied undocumented inputs remain unresolved.", "assumptions": ["200 application/json models the documented successful examples; other success/error statuses are not specified.", "Public unauthenticated GET access follows provider examples, not a formal security guarantee.", "Example property types describe the documented examples; they are not a complete provider schema."], "review_document": "examples/JSONPLACEHOLDER_REFERENCE_REVIEW.md" }, "paths": { "/posts": { "get": { "responses": { "200": { "description": "Documented successful JSON response", "content": { "application/json": { "schema": { "type": "array", "items": { "$ref": "#/components/schemas/Post" } } } } } } } }, "/posts/1": { "get": { "responses": { "200": { "description": "Documented successful JSON response", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/Post" } } } } } } } }, "components": { "schemas": { "Post": { "type": "object", "properties": { "id": { "type": "integer" }, "userId": { "type": "integer" }, "title": { "type": "string" }, "body": { "type": "string" } } } } }, "security": [] } };
  }
});

// src/evidenceRegistry.ts
function registryRoot() {
  const candidates = [process.env.CONFIDENCE_EVIDENCE_ROOT, (0, import_path6.resolve)(__dirname, ".."), process.cwd()].filter(Boolean);
  return candidates.find((root) => (0, import_fs3.existsSync)((0, import_path6.join)(root, "evidence", "registry.json"))) ?? null;
}
function templateHead(t2) {
  return Array.isArray(t2?.parts) && typeof t2.parts[0] === "string" ? t2.parts[0] : "";
}
function hostOf(url) {
  return /^https?:\/\/([^/?#:]+)/i.exec(url)?.[1]?.toLowerCase() ?? null;
}
function hostsFromClaims(claims) {
  const hosts = ofType(claims, "endpoint").map((ep) => hostOf(typeof ep.endpoint === "string" ? ep.endpoint : templateHead(ep.endpoint_template)));
  return [...new Set(hosts.filter((h) => !!h))];
}
function hostsFromCode(code) {
  return [...new Set([...code.matchAll(/https?:\/\/([^/'"\s?#:{}]+)/gi)].map((m) => m[1].toLowerCase()))];
}
function selectEvidence(hosts) {
  const root = registryRoot();
  if (!root) return { provider: null, spec: null, hosts, note: "Evidence registry (evidence/registry.json) not found; set CONFIDENCE_EVIDENCE_ROOT to the Toolbox folder." };
  const registry = JSON.parse((0, import_fs3.readFileSync)((0, import_path6.join)(root, "evidence", "registry.json"), "utf8"));
  const matches = Object.entries(registry.providers).filter(([, p]) => hosts.some((h) => p.hosts.includes(h)));
  if (!matches.length) return { provider: null, spec: null, hosts, note: `No frozen evidence for host(s): ${hosts.join(", ") || "(none found)"}.` };
  if (matches.length > 1) return { provider: null, spec: null, hosts, note: `Candidate calls several providers (${matches.map(([n]) => n).join(", ")}); single-provider verification only.` };
  const [provider, entry] = matches[0];
  const path = (0, import_path6.resolve)(root, "evidence", registry.sources_dir, entry.spec);
  if (!(0, import_fs3.existsSync)(path)) return { provider, spec: null, hosts, note: `Frozen snapshot ${entry.spec} is missing at ${path}.` };
  if (!cache.has(path)) cache.set(path, JSON.parse((0, import_fs3.readFileSync)(path, "utf8")));
  const spec = structuredClone(cache.get(path));
  spec["x-confidence-evidence"] = { ...spec["x-confidence-evidence"] || {}, ...entry.overlay, snapshot: entry.spec };
  return { provider, spec, hosts, snapshot: entry.spec, note: `Frozen evidence ${entry.spec} selected for ${provider}.` };
}
function evidenceFor(hosts, supplied) {
  const selected = selectEvidence(hosts);
  if (selected.spec) return { spec: selected.spec, source: selected.note + (supplied != null ? " A model-supplied specification was ignored." : "") };
  const usable = supplied != null && typeof supplied === "object" && !(Object.hasOwn(supplied, "spec") && !Object.hasOwn(supplied, "openapi"));
  return { spec: usable ? supplied : null, source: usable ? "Model-supplied specification (unreviewed; not frozen evidence)." : selected.note };
}
var import_fs3, import_path6, cache;
var init_evidenceRegistry = __esm({
  "src/evidenceRegistry.ts"() {
    "use strict";
    import_fs3 = require("fs");
    import_path6 = require("path");
    init_verificationTypes();
    cache = /* @__PURE__ */ new Map();
  }
});

// src/confidenceAgentTools.ts
function createConfidenceAgentTools(deps) {
  const claims = import_zod.z.array(import_zod.z.record(import_zod.z.any())), spec = import_zod.z.record(import_zod.z.any()).nullable().optional();
  const out = [];
  function add(name, description, parameters2, implementation) {
    out.push((0, import_sdk2.tool)({ name, description, parameters: parameters2, implementation: async (p) => {
      if (!deps.isEnabled) throw new Error("Confidence Agent tools are disabled in plugin settings.");
      try {
        return await implementation(p);
      } catch (e) {
        return { error: String(e) };
      }
    } }));
  }
  const withEvidence = (fn) => async (p) => {
    const { spec: selected, source } = evidenceFor(hostsFromClaims(p.claims || []), p.spec);
    const r = await fn({ ...p, spec: selected });
    return r && typeof r === "object" ? { ...r, evidence_source_selection: source } : r;
  };
  add(
    "verify_candidate",
    "Run all six verifiers, score and report exact candidate API claims. Pass only the code: frozen evidence for JSONPlaceholder, GitHub, Open-Meteo, DummyJSON, REST Countries and Petstore is selected from the host the code calls. Never write or copy a specification. Does not prove task behavior. External controller enforces delivery and one correction.",
    { code: import_zod.z.string(), spec, reference_id: import_zod.z.enum(["jsonplaceholder-posts"]).optional(), input_bindings: import_zod.z.record(import_zod.z.any()).optional(), task_id: import_zod.z.string().optional() },
    async (p) => {
      if (p.reference_id && p.spec != null) throw new Error("Supply reference_id or spec, not both.");
      const selected = p.reference_id ? { spec: structuredClone(BUNDLED_REFERENCES[p.reference_id]), source: `Bundled reference ${p.reference_id}.` } : evidenceFor(hostsFromCode(p.code), p.spec);
      const reference = selected.spec;
      const r = await runIntervention({ ...p, spec: reference }, { runPyright: deps.runPyright, allowPyright: deps.allowPyright, lookupPackage: deps.lookupPackage });
      const v = r.attempts[r.attempts.length - 1].verification;
      return {
        toolbox_version: TOOLBOX_VERSION,
        decision: r.decision,
        report: r.report,
        candidate_hash: v.candidate_hash,
        reference_id: p.reference_id ?? null,
        evidence_selection: selected.source,
        spec_hash: v.spec_hash,
        reference_evidence: reference?.["x-confidence-evidence"] ?? null,
        ewcs_report: v.ewcs_report,
        layers: v.layers,
        extraction_issues: v.extraction.issues
      };
    }
  );
  add("resolve_api_spec", "Discovery only: report whether a JSON OpenAPI 3.0 document exists at common paths, with its source and hash. Does not return the document; verify_candidate selects frozen evidence itself.", { base_url: import_zod.z.string() }, async (p) => {
    const r = await resolveApiSpec(p);
    if (!r.spec) return r;
    const operations = Object.values(r.spec.paths || {}).reduce((n, item) => n + Object.keys(item || {}).filter((k) => ["get", "put", "post", "delete", "patch", "head", "options"].includes(k)).length, 0);
    return {
      found: true,
      source_url: r.source_url,
      retrieved_at: r.retrieved_at,
      content_hash: r.content_hash,
      openapi: r.spec.openapi,
      title: r.spec.info?.title,
      version: r.spec.info?.version,
      operations,
      note: "Summary only. Do not pass a specification to verification tools; call verify_candidate with the code and frozen evidence is selected by host."
    };
  });
  add("query_pypi", "Query package metadata. exists:null/status:unverifiable means lookup failed, not that the package is nonexistent.", { library_name: import_zod.z.string() }, queryPypi);
  add("extract_claims", "Static Python extraction for a documented requests subset. Returns complete/limitations, operation-linked claims and a candidate hash. Runtime input values can be bound explicitly.", { code: import_zod.z.string(), input_bindings: import_zod.z.record(import_zod.z.any()).optional() }, extractClaims);
  add("verify_interface", "Check imports against registry evidence and explicit import/distribution mappings. Missing evidence and registry failures stay unverifiable.", { claims, pypi_data: import_zod.z.record(import_zod.z.any()).optional() }, verifyInterface);
  add("verify_identifier", "Check structured Pyright diagnostics for the exact code. Missing packages/stubs and process failure are unverifiable.", { code: import_zod.z.string() }, (p) => verifyIdentifier(p.code, deps.runPyright, deps.allowPyright));
  add("verify_access_point", "Match server origin/base path, endpoint and HTTP method. Dynamic endpoints and unsupported specs remain unverifiable.", { claims, spec }, withEvidence(verifyAccessPoint));
  add("verify_input_contract", "Check every request separately: required parameters, locations, supported values and JSON bodies. Runtime values are noted, not guessed; unknown keys block verification.", { claims, spec }, withEvidence(verifyInputContract));
  add("verify_output_contract", "Follow response provenance and local references to success schemas. A clean Pyright run never substitutes for JSON response evidence.", { claims, spec, code: import_zod.z.string().optional() }, withEvidence((p) => verifyOutputContract(p, deps.runPyright, deps.allowPyright)));
  add("verify_contextual", "Check operation-level inherited authentication alternatives against actual request arguments. Comments are not authentication.", { claims, spec, code: import_zod.z.string().optional() }, withEvidence(verifyContextual));
  add(
    "compute_ewcs",
    "Diagnostic score with canonical weights; missing checks retain weight and an empty applicable set has ewcs:null. Controller results are authoritative.",
    { layer_results: import_zod.z.array(import_zod.z.record(import_zod.z.any())), task_id: import_zod.z.string().optional(), extraction_complete: import_zod.z.boolean().optional() },
    (p) => Promise.resolve(computeEwcs(p))
  );
  add("make_decision", "Validate all six contributions. Contradiction requests correction; incomplete/unverifiable critical checks abstain before thresholds 0.85/0.60.", { ewcs_report: import_zod.z.record(import_zod.z.any()) }, async (p) => makeDecision(p.ewcs_report));
  add("save_code", "Save a candidate for inspection. This is not verified delivery; use the controller for user-facing output.", { code: import_zod.z.string(), filename: import_zod.z.string() }, async (p) => {
    const base = deps.getWorkingDirectory(), path = (0, import_path7.resolve)(base, p.filename), rel = (0, import_path7.relative)(base, path);
    if (!p.filename.trim() || rel.startsWith("..") || (0, import_path7.isAbsolute)(rel)) throw new Error("Invalid workspace-relative filename.");
    await (0, import_promises3.mkdir)((0, import_path7.dirname)(path), { recursive: true });
    await (0, import_promises3.writeFile)(path, p.code, "utf8");
    return { path };
  });
  add(
    "present_report",
    "Format a score report. Code is withheld for abstain/correct and inconsistent delivery requests. Native chat remains model controlled; use the external controller for enforcement.",
    { code: import_zod.z.string(), ewcs_report: import_zod.z.record(import_zod.z.any()), decision: import_zod.z.enum(["deliver", "deliver_with_flag", "correct", "abstain"]) },
    async (p) => presentReport(p)
  );
  return out;
}
var import_sdk2, import_promises3, import_path7, import_zod;
var init_confidenceAgentTools = __esm({
  "src/confidenceAgentTools.ts"() {
    "use strict";
    import_sdk2 = require("@lmstudio/sdk");
    import_promises3 = require("fs/promises");
    import_path7 = require("path");
    import_zod = require("zod");
    init_claimExtractor();
    init_packageEvidence();
    init_specDiscovery();
    init_pyrightRunner();
    init_openApiVerifier();
    init_verificationPolicy();
    init_verificationController();
    init_bundledReferences();
    init_evidenceRegistry();
    init_verificationTypes();
    init_verificationPolicy();
  }
});

// src/toolsProvider.ts
function validatePath(baseDir, requestedPath) {
  const resolved = (0, import_path8.resolve)(baseDir, requestedPath);
  const rel = (0, import_path8.relative)(baseDir, resolved);
  if (rel.startsWith("..") || (0, import_path8.isAbsolute)(rel)) {
    throw new Error(`Access Denied: Path '${requestedPath}' is outside the workspace.`);
  }
  return resolved;
}
function extractLikelyFilePath(text3) {
  const isPlausiblePath = (value) => {
    const candidate = value.trim();
    if (!candidate) return false;
    if (/[,\r\n]/.test(candidate)) return false;
    if (candidate.includes("=") && !candidate.includes("\\") && !candidate.includes("/")) return false;
    if (/[<>|*?]/.test(candidate)) return false;
    const extensionMatch = candidate.match(/\.([A-Za-z0-9_-]{1,15})$/);
    if (!extensionMatch) return false;
    const extension = extensionMatch[1];
    if (!/[A-Za-z]/.test(extension)) return false;
    return true;
  };
  const patterns = [
    /['"]([A-Za-z]:\\[^'"\r\n]+)['"]/,
    /\b([A-Za-z]:\\[^\s'"]+(?:\.[A-Za-z0-9_-]+)?)\b/,
    /['"]((?:\.{0,2}[\\/])?[^'"\r\n]+\.[A-Za-z0-9_-]+)['"]/
  ];
  for (const pattern of patterns) {
    const match = text3.match(pattern);
    if (!match?.[1]) continue;
    const candidate = match[1].replace(/[),.;]+$/, "").trim();
    if (!isPlausiblePath(candidate)) continue;
    return candidate;
  }
  return null;
}
function cosineSimilarity(vecA, vecB) {
  const dotProduct = vecA.reduce((acc, val, i) => acc + val * vecB[i], 0);
  const magA = Math.sqrt(vecA.reduce((acc, val) => acc + val * val, 0));
  const magB = Math.sqrt(vecB.reduce((acc, val) => acc + val * val, 0));
  if (magA === 0 || magB === 0) {
    return 0;
  }
  return dotProduct / (magA * magB);
}
async function performRagOnText(text3, query, client2, embeddingModelName) {
  const embeddingModel = await client2.embedding.model(embeddingModelName);
  const chunks = text3.split(/\n\s*\n/).filter((chunk) => chunk.trim().length > 20);
  if (chunks.length === 0) {
    return [{ chunk: text3.substring(0, 4e3), score: 1 }];
  }
  const [queryEmbedding] = await embeddingModel.embed([query]);
  const chunkEmbeddings = await embeddingModel.embed(chunks);
  const similarities = chunkEmbeddings.map((chunkEmb, i) => ({
    chunk: chunks[i],
    score: cosineSimilarity(queryEmbedding.embedding, chunkEmb.embedding)
  }));
  similarities.sort((a, b) => b.score - a.score);
  return similarities.slice(0, 5);
}
function getDenoPath() {
  const lmstudioHome2 = findLMStudioHome();
  const utilPath = (0, import_path8.join)(lmstudioHome2, ".internal", "utils");
  const denoPath = (0, import_path8.join)(utilPath, process.platform === "win32" ? "deno.exe" : "deno");
  return denoPath;
}
var import_sdk3, import_child_process3, import_promises4, os3, import_path8, import_zod2, createSafeToolImplementation, isWorkspaceInitialized, toolsProvider;
var init_toolsProvider = __esm({
  "src/toolsProvider.ts"() {
    "use strict";
    import_sdk3 = require("@lmstudio/sdk");
    import_child_process3 = require("child_process");
    import_promises4 = require("fs/promises");
    os3 = __toESM(require("os"));
    import_path8 = require("path");
    import_zod2 = require("zod");
    init_config();
    init_findLMStudioHome();
    init_stateManager();
    init_browserActions();
    init_fuzzySearch();
    init_handoffMessage();
    init_subAgentToolCallParser();
    init_toolCallValidator();
    init_backgroundCommands();
    init_confidenceAgentTools();
    init_pyrightRunner();
    createSafeToolImplementation = (originalImplementation, isEnabled, toolName) => async (params) => {
      if (!isEnabled) {
        throw new Error(`Tool '${toolName}' is disabled in the plugin settings. Please ask the user to enable 'Allow ${toolName.replace(/_/g, " ")}' (or similar) in the settings.`);
      }
      return originalImplementation(params);
    };
    isWorkspaceInitialized = false;
    toolsProvider = async (ctl) => {
      const client2 = ctl.client;
      const pluginConfig = ctl.getPluginConfig(pluginConfigSchematics);
      const defaultWorkspacePath = pluginConfig.get("defaultWorkspacePath");
      const fullState = await getPersistedState(defaultWorkspacePath);
      let currentWorkingDirectory = fullState.currentWorkingDirectory;
      const allowAllCode = pluginConfig.get("allowAllCode");
      let allowJavascript = pluginConfig.get("allowJavascriptExecution");
      let allowPython = pluginConfig.get("allowPythonExecution");
      let allowCpp = pluginConfig.get("allowCppExecution");
      let allowJava = pluginConfig.get("allowJavaExecution");
      let allowPyright = pluginConfig.get("allowPyrightExecution");
      let allowTerminal = pluginConfig.get("allowTerminalExecution");
      let allowShell = pluginConfig.get("allowShellCommandExecution");
      let allowBrowserControl = pluginConfig.get("allowBrowserControl");
      const enableMemory = pluginConfig.get("enableMemory");
      const enableWikipedia = pluginConfig.get("enableWikipediaTool");
      const enableLocalRag = pluginConfig.get("enableLocalRag");
      const enableSecondary = pluginConfig.get("enableSecondaryAgent");
      const enableConfidenceAgentTools = pluginConfig.get("enableConfidenceAgentTools");
      const embeddingModelName = pluginConfig.get("embeddingModel");
      if (allowAllCode) {
        allowJavascript = true;
        allowPython = true;
        allowCpp = true;
        allowJava = true;
        allowPyright = true;
        allowTerminal = true;
        allowShell = true;
        allowBrowserControl = true;
      }
      if (!isWorkspaceInitialized) {
        await ensureWorkspaceExists(currentWorkingDirectory);
        fullState.currentWorkingDirectory = currentWorkingDirectory;
        await savePersistedState(fullState);
        console.log(`Working directory set to: ${currentWorkingDirectory}`);
        isWorkspaceInitialized = true;
      }
      const uiLanguageOverride = pluginConfig.get("uiLanguageOverride");
      if (fullState.uiLanguageOverride !== uiLanguageOverride) {
        fullState.uiLanguageOverride = uiLanguageOverride;
        await savePersistedState(fullState);
        console.log(`[i18n] uiLanguageOverride persisted: "${uiLanguageOverride}". Restart plugin to apply.`);
      }
      const tools = [];
      let browserSession = null;
      const allowGit = pluginConfig.get("allowGitOperations");
      const allowDb = pluginConfig.get("allowDatabaseInspection");
      const allowNotify = pluginConfig.get("allowSystemNotifications");
      const allowGitHubTools = pluginConfig.get("allowGitHubTools");
      if (allowGit) {
        const gitStatusTool = (0, import_sdk3.tool)({
          name: "git_status",
          description: "Get the current git status of the repository.",
          parameters: {},
          implementation: async () => {
            const { simpleGit } = await import("simple-git");
            const git = simpleGit(currentWorkingDirectory);
            try {
              const status = await git.status();
              return status;
            } catch (e) {
              return { error: `Git status failed: ${e instanceof Error ? e.message : String(e)}` };
            }
          }
        });
        tools.push(gitStatusTool);
        const gitDiffTool = (0, import_sdk3.tool)({
          name: "git_diff",
          description: "Get the git diff of the current repository or specific files.",
          parameters: {
            file_path: import_zod2.z.string().optional().describe("Optional: Path to specific file to diff."),
            cached: import_zod2.z.boolean().optional().describe("Optional: Show staged changes only (git diff --cached).")
          },
          implementation: async ({ file_path, cached }) => {
            const { simpleGit } = await import("simple-git");
            const git = simpleGit(currentWorkingDirectory);
            try {
              const args = [];
              if (cached) args.push("--cached");
              if (file_path) args.push(validatePath(currentWorkingDirectory, file_path));
              const diff = await git.diff(args);
              return { diff: diff || "No changes." };
            } catch (e) {
              return { error: `Git diff failed: ${e instanceof Error ? e.message : String(e)}` };
            }
          }
        });
        tools.push(gitDiffTool);
        const gitCommitTool = (0, import_sdk3.tool)({
          name: "git_commit",
          description: "Commit staged changes to the git repository.",
          parameters: {
            message: import_zod2.z.string()
          },
          implementation: async ({ message }) => {
            const { simpleGit } = await import("simple-git");
            const git = simpleGit(currentWorkingDirectory);
            try {
              const result2 = await git.commit(message);
              return { success: true, summary: result2.summary };
            } catch (e) {
              return { error: `Git commit failed: ${e instanceof Error ? e.message : String(e)}` };
            }
          }
        });
        tools.push(gitCommitTool);
        const gitLogTool = (0, import_sdk3.tool)({
          name: "git_log",
          description: "Get recent git commit history.",
          parameters: {
            max_count: import_zod2.z.number().optional().describe("Max number of commits to return (default: 10)")
          },
          implementation: async ({ max_count = 10 }) => {
            const { simpleGit } = await import("simple-git");
            const git = simpleGit(currentWorkingDirectory);
            try {
              const log = await git.log({ maxCount: max_count });
              return { history: log.all };
            } catch (e) {
              return { error: `Git log failed: ${e instanceof Error ? e.message : String(e)}` };
            }
          }
        });
        tools.push(gitLogTool);
        const gitAddTool = (0, import_sdk3.tool)({
          name: "git_add",
          description: "Stage specific files or all changes for the next commit.",
          parameters: {
            paths: import_zod2.z.array(import_zod2.z.string()).optional().describe("Optional: Specific file paths to stage. If omitted, stages all changes.")
          },
          implementation: async ({ paths }) => {
            const { simpleGit } = await import("simple-git");
            const git = simpleGit(currentWorkingDirectory);
            try {
              if (paths && paths.length > 0) {
                const validatedPaths = paths.map((p) => validatePath(currentWorkingDirectory, p));
                await git.add(validatedPaths);
              } else {
                await git.add(".");
              }
              return { success: true, message: "Files staged successfully." };
            } catch (e) {
              return { error: `Git add failed: ${e instanceof Error ? e.message : String(e)}` };
            }
          }
        });
        tools.push(gitAddTool);
        const gitCheckoutTool = (0, import_sdk3.tool)({
          name: "git_checkout",
          description: "Switch to an existing branch or create and switch to a new one.",
          parameters: {
            branch_name: import_zod2.z.string().describe("Name of the branch to checkout."),
            create_new: import_zod2.z.boolean().optional().default(false).describe("If true, creates the branch if it doesn't exist (like git checkout -b).")
          },
          implementation: async ({ branch_name, create_new = false }) => {
            const { simpleGit } = await import("simple-git");
            const git = simpleGit(currentWorkingDirectory);
            try {
              if (create_new) {
                await git.checkout(["-b", branch_name]);
              } else {
                await git.checkout(branch_name);
              }
              return { success: true, message: `Switched to branch '${branch_name}'.` };
            } catch (e) {
              return { error: `Git checkout failed: ${e instanceof Error ? e.message : String(e)}` };
            }
          }
        });
        tools.push(gitCheckoutTool);
      }
      const readDocumentTool = (0, import_sdk3.tool)({
        name: "read_document",
        description: "Read content from PDF or DOCX files.",
        parameters: {
          file_path: import_zod2.z.string()
        },
        implementation: async ({ file_path }) => {
          const fpath = validatePath(currentWorkingDirectory, file_path);
          const ext = fpath.split(".").pop()?.toLowerCase();
          try {
            if (ext === "pdf") {
              if (typeof global.DOMMatrix === "undefined") {
                global.DOMMatrix = class DOMMatrix {
                  constructor(arg) {
                    this.a = 1;
                    this.b = 0;
                    this.c = 0;
                    this.d = 1;
                    this.e = 0;
                    this.f = 0;
                    if (Array.isArray(arg)) {
                      this.a = arg[0];
                      this.b = arg[1];
                      this.c = arg[2];
                      this.d = arg[3];
                      this.e = arg[4];
                      this.f = arg[5];
                    }
                  }
                };
              }
              const { PDFParse } = require("pdf-parse");
              const dataBuffer = await (0, import_promises4.readFile)(fpath);
              const parser = new PDFParse({ data: dataBuffer });
              const textResult = await parser.getText();
              const infoResult = await parser.getInfo();
              await parser.destroy();
              return { content: textResult.text, metadata: infoResult.info };
            } else if (ext === "docx") {
              const mammoth = await import("mammoth");
              const result2 = await mammoth.extractRawText({ path: fpath });
              return { content: result2.value, messages: result2.messages };
            } else {
              return { error: "Unsupported document format. Use read_file for text files." };
            }
          } catch (e) {
            return { error: `Failed to read document: ${e instanceof Error ? e.message : String(e)}` };
          }
        }
      });
      tools.push(readDocumentTool);
      if (allowNotify) {
        const sendNotificationTool = (0, import_sdk3.tool)({
          name: "send_notification",
          description: "Send a system notification to the user.",
          parameters: {
            title: import_zod2.z.string(),
            message: import_zod2.z.string()
          },
          implementation: async ({ title, message }) => {
            const notifier = await import("node-notifier");
            notifier.default.notify({
              title,
              message,
              sound: true,
              wait: false
            });
            return { success: true, message: "Notification sent." };
          }
        });
        tools.push(sendNotificationTool);
      }
      if (allowDb) {
        const queryDatabaseTool = (0, import_sdk3.tool)({
          name: "query_database",
          description: "Execute a read-only query on a SQLite database file.",
          parameters: {
            db_path: import_zod2.z.string(),
            query: import_zod2.z.string()
          },
          implementation: async ({ db_path, query }) => {
            const fpath = validatePath(currentWorkingDirectory, db_path);
            if (/^\s*(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|REPLACE)\b/i.test(query)) {
              return { error: "Only SELECT/read queries are allowed for safety." };
            }
            try {
              const Database = (await import("better-sqlite3")).default;
              const db = new Database(fpath, { readonly: true });
              const stmt = db.prepare(query);
              const results = stmt.all();
              db.close();
              return { results };
            } catch (e) {
              return { error: `Database query failed: ${e instanceof Error ? e.message : String(e)}` };
            }
          }
        });
        tools.push(queryDatabaseTool);
      }
      const analyzeProjectTool = (0, import_sdk3.tool)({
        name: "analyze_project",
        description: "Run project-wide analysis (linting) to find errors and warnings.",
        parameters: {},
        implementation: async () => {
          const packageJsonPath = (0, import_path8.join)(currentWorkingDirectory, "package.json");
          let command = "";
          let type = "unknown";
          try {
            const pkg = JSON.parse(await (0, import_promises4.readFile)(packageJsonPath, "utf-8"));
            if (pkg.scripts && pkg.scripts.lint) {
              command = "npm run lint";
              type = "npm-script";
            } else if (pkg.devDependencies?.eslint || pkg.dependencies?.eslint) {
              command = "npx eslint . --format json";
              type = "eslint";
            }
          } catch (e) {
            const entries = await (0, import_promises4.readdir)(currentWorkingDirectory);
            if (entries.some((f) => f.endsWith(".py"))) {
              command = "pylint .";
              type = "python-lint";
            }
          }
          if (!command) {
            return { error: "Could not detect a supported linter (ESLint script or Python)." };
          }
          try {
            const child = (0, import_child_process3.spawn)(command, {
              shell: true,
              cwd: currentWorkingDirectory,
              timeout: 6e4
            });
            let stdout = "";
            let stderr = "";
            child.stdout.on("data", (d) => stdout += d);
            child.stderr.on("data", (d) => stderr += d);
            await new Promise((resolve5) => child.on("close", resolve5));
            return {
              tool: command,
              type,
              report: (stdout + stderr).substring(0, 1e4)
              // Limit size
            };
          } catch (e) {
            return { error: `Analysis failed: ${e instanceof Error ? e.message : String(e)}` };
          }
        }
      });
      tools.push(analyzeProjectTool);
      const changeDirectoryTool = (0, import_sdk3.tool)({
        name: "change_directory",
        description: import_sdk3.text`
      Change the current working directory.
      Returns the new current working directory.
    `,
        parameters: {
          directory: import_zod2.z.string()
        },
        implementation: async ({ directory }) => {
          const newPath = (0, import_path8.resolve)(currentWorkingDirectory, directory);
          const stats = await (0, import_promises4.stat)(newPath);
          if (!stats.isDirectory()) {
            throw new Error(`Path is not a directory: ${newPath}`);
          }
          currentWorkingDirectory = newPath;
          fullState.currentWorkingDirectory = currentWorkingDirectory;
          await savePersistedState(fullState);
          return {
            previous_directory: (0, import_path8.resolve)(newPath, ".."),
            current_directory: currentWorkingDirectory
          };
        }
      });
      tools.push(changeDirectoryTool);
      const saveMemoryTool = (0, import_sdk3.tool)({
        name: "save_memory",
        description: import_sdk3.text`
      Save a specific piece of information or fact to long-term memory.
      This information will be available in future interactions if memory is enabled.
      Use this for user preferences, important facts, or context that should persist.
    `,
        parameters: {
          fact: import_zod2.z.string().describe("The specific fact or piece of information to remember.")
        },
        implementation: async ({ fact }) => {
          if (!enableMemory) {
            return { error: "Memory is currently disabled in the plugin settings. Please ask the user to enable it." };
          }
          const memoryFile = (0, import_path8.join)(currentWorkingDirectory, "memory.md");
          const timestamp = (/* @__PURE__ */ new Date()).toISOString();
          const entry = `
- [${timestamp}] ${fact}`;
          try {
            await (0, import_promises4.appendFile)(memoryFile, entry, "utf-8");
            return { success: true, message: "Fact saved to memory." };
          } catch (error) {
            try {
              await (0, import_promises4.writeFile)(memoryFile, "# Long-Term Memory\n" + entry, "utf-8");
              return { success: true, message: "Fact saved to memory (new file created)." };
            } catch (writeError) {
              return { error: `Failed to save memory: ${writeError instanceof Error ? writeError.message : String(writeError)}` };
            }
          }
        }
      });
      tools.push(saveMemoryTool);
      const originalRunJavascriptImplementation = async ({ javascript, timeout_seconds }) => {
        const scriptFileName = `temp_script_${Date.now()}.ts`;
        const scriptFilePath = (0, import_path8.join)(currentWorkingDirectory, scriptFileName);
        try {
          await (0, import_promises4.writeFile)(scriptFilePath, javascript, "utf-8");
          const childProcess = (0, import_child_process3.spawn)(
            getDenoPath(),
            [
              "run",
              "--allow-read=.",
              "--allow-write=.",
              "--no-prompt",
              "--deny-net",
              "--deny-env",
              "--deny-sys",
              "--deny-run",
              "--deny-ffi",
              scriptFilePath
            ],
            {
              cwd: currentWorkingDirectory,
              timeout: (timeout_seconds ?? 5) * 1e3,
              // Convert seconds to milliseconds
              stdio: "pipe",
              env: {
                NO_COLOR: "true"
                // Disable color output in Deno
              }
            }
          );
          let stdout = "";
          let stderr = "";
          childProcess.stdout.setEncoding("utf-8");
          childProcess.stderr.setEncoding("utf-8");
          childProcess.stdout.on("data", (data) => {
            stdout += data;
          });
          childProcess.stderr.on("data", (data) => {
            stderr += data;
          });
          await new Promise((resolve5, reject) => {
            childProcess.on("close", (code) => {
              if (code === 0) {
                resolve5();
              } else {
                reject(new Error(`Process exited with code ${code}. Stderr: ${stderr}`));
              }
            });
            childProcess.on("error", (err) => {
              reject(err);
            });
          });
          return {
            stdout: stdout.trim(),
            stderr: stderr.trim()
          };
        } finally {
          await (0, import_promises4.rm)(scriptFilePath, { force: true }).catch(() => {
          });
        }
      };
      const createFileTool = (0, import_sdk3.tool)({
        name: "run_javascript",
        description: import_sdk3.text`
      Run a JavaScript code snippet using deno. You cannot import external modules but you have 
      read/write access to the current working directory.

      Pass the code you wish to run as a string in the 'javascript' parameter.

      By default, the code will timeout in 5 seconds. You can extend this timeout by setting the
      'timeout_seconds' parameter to a higher value in seconds, up to a maximum of 60 seconds.

      You will get the stdout and stderr output of the code execution, thus please print the output
      you wish to return using 'console.log' or 'console.error'.
    `,
        parameters: { javascript: import_zod2.z.string(), timeout_seconds: import_zod2.z.number().min(0.1).max(60).optional() },
        implementation: createSafeToolImplementation(
          originalRunJavascriptImplementation,
          allowJavascript,
          "run_javascript"
        )
      });
      tools.push(createFileTool);
      const originalRunPythonImplementation = async ({ python, timeout_seconds }) => {
        const scriptFileName = `temp_script_${Date.now()}.py`;
        const scriptFilePath = (0, import_path8.join)(currentWorkingDirectory, scriptFileName);
        try {
          await (0, import_promises4.writeFile)(scriptFilePath, python, "utf-8");
          const childProcess = (0, import_child_process3.spawn)(
            "python",
            [
              scriptFilePath
            ],
            {
              cwd: currentWorkingDirectory,
              timeout: (timeout_seconds ?? 5) * 1e3,
              // Convert seconds to milliseconds
              stdio: "pipe"
            }
          );
          let stdout = "";
          let stderr = "";
          childProcess.stdout.setEncoding("utf-8");
          childProcess.stderr.setEncoding("utf-8");
          childProcess.stdout.on("data", (data) => {
            stdout += data;
          });
          childProcess.stderr.on("data", (data) => {
            stderr += data;
          });
          await new Promise((resolve5, reject) => {
            childProcess.on("close", (code) => {
              if (code === 0) {
                resolve5();
              } else {
                reject(new Error(`Process exited with code ${code}. Stderr: ${stderr}`));
              }
            });
            childProcess.on("error", (err) => {
              reject(err);
            });
          });
          return {
            stdout: stdout.trim(),
            stderr: stderr.trim()
          };
        } finally {
          await (0, import_promises4.rm)(scriptFilePath, { force: true }).catch(() => {
          });
        }
      };
      const runPythonTool = (0, import_sdk3.tool)({
        name: "run_python",
        description: import_sdk3.text`
      Run a Python code snippet. You cannot import external modules but you have
      read/write access to the current working directory.

      Pass the code you wish to run as a string in the 'python' parameter.

      By default, the code will timeout in 5 seconds. You can extend this timeout by setting the
      'timeout_seconds' parameter to a higher value in seconds, up to a maximum of 60 seconds.

      You will get the stdout and stderr output of the code execution, thus please print the output
      you wish to return using 'print()'.
    `,
        parameters: { python: import_zod2.z.string(), timeout_seconds: import_zod2.z.number().min(0.1).max(60).optional() },
        implementation: createSafeToolImplementation(
          originalRunPythonImplementation,
          allowPython,
          "run_python"
        )
      });
      tools.push(runPythonTool);
      const runChildProcess = (command, args, options) => new Promise((resolvePromise, rejectPromise) => {
        const child = (0, import_child_process3.spawn)(command, args, {
          cwd: options.cwd,
          timeout: options.timeoutMs,
          stdio: "pipe"
        });
        let stdout = "";
        let stderr = "";
        child.stdout.setEncoding("utf-8");
        child.stderr.setEncoding("utf-8");
        child.stdout.on("data", (data) => {
          stdout += data;
        });
        child.stderr.on("data", (data) => {
          stderr += data;
        });
        child.on("close", (code) => {
          if (code === 0) {
            resolvePromise({ stdout, stderr });
          } else {
            rejectPromise(new Error(`[${options.stageLabel}] exited with code ${code}. Stderr: ${stderr.trim()}`));
          }
        });
        child.on("error", (err) => {
          rejectPromise(new Error(`[${options.stageLabel}] failed to start (is it installed and on PATH?): ${err.message}`));
        });
      });
      const originalRunCppImplementation = async ({ cpp, timeout_seconds }) => {
        const id = `${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
        const sourceFilePath = (0, import_path8.join)(currentWorkingDirectory, `temp_cpp_${id}.cpp`);
        const binaryFilePath = (0, import_path8.join)(currentWorkingDirectory, `temp_cpp_${id}${process.platform === "win32" ? ".exe" : ".out"}`);
        const timeoutMs = (timeout_seconds ?? 5) * 1e3;
        try {
          await (0, import_promises4.writeFile)(sourceFilePath, cpp, "utf-8");
          await runChildProcess(
            "g++",
            ["-std=c++17", "-O2", "-o", binaryFilePath, sourceFilePath],
            { cwd: currentWorkingDirectory, timeoutMs, stageLabel: "compile" }
          );
          const { stdout, stderr } = await runChildProcess(
            binaryFilePath,
            [],
            { cwd: currentWorkingDirectory, timeoutMs, stageLabel: "run" }
          );
          return { stdout: stdout.trim(), stderr: stderr.trim() };
        } finally {
          await (0, import_promises4.rm)(sourceFilePath, { force: true }).catch(() => {
          });
          await (0, import_promises4.rm)(binaryFilePath, { force: true }).catch(() => {
          });
        }
      };
      const runCppTool = (0, import_sdk3.tool)({
        name: "run_cpp",
        description: import_sdk3.text`
      Compile and run a C++ code snippet using g++ (requires g++ to be installed and on PATH).
      You have read/write access to the current working directory, but no external libraries
      beyond the standard library are available.

      Pass the full source code as a string in the 'cpp' parameter. It must contain a main()
      function.

      By default, compiling and running together will timeout in 5 seconds. You can extend this
      by setting 'timeout_seconds' up to a maximum of 60 seconds.

      You will get the stdout and stderr of the compiled program. If compilation fails, the
      compiler's error output is returned instead so you can fix the code and retry.
    `,
        parameters: { cpp: import_zod2.z.string(), timeout_seconds: import_zod2.z.number().min(0.1).max(60).optional() },
        implementation: createSafeToolImplementation(
          originalRunCppImplementation,
          allowCpp,
          "run_cpp"
        )
      });
      tools.push(runCppTool);
      const originalRunJavaImplementation = async ({ java, timeout_seconds }) => {
        const classNameMatch = java.match(/public\s+(?:final\s+|abstract\s+)?class\s+([A-Za-z_$][A-Za-z0-9_$]*)/);
        if (!classNameMatch) {
          throw new Error(
            "Could not find a 'public class <Name>' declaration in the provided Java code. The snippet must define exactly one public class containing a main method."
          );
        }
        const className = classNameMatch[1];
        const id = `${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
        const workDir = (0, import_path8.join)(currentWorkingDirectory, `temp_java_${id}`);
        const sourceFilePath = (0, import_path8.join)(workDir, `${className}.java`);
        const timeoutMs = (timeout_seconds ?? 5) * 1e3;
        try {
          await (0, import_promises4.mkdir)(workDir, { recursive: true });
          await (0, import_promises4.writeFile)(sourceFilePath, java, "utf-8");
          await runChildProcess(
            "javac",
            [sourceFilePath],
            { cwd: workDir, timeoutMs, stageLabel: "compile" }
          );
          const { stdout, stderr } = await runChildProcess(
            "java",
            ["-cp", workDir, className],
            { cwd: workDir, timeoutMs, stageLabel: "run" }
          );
          return { stdout: stdout.trim(), stderr: stderr.trim() };
        } finally {
          await (0, import_promises4.rm)(workDir, { recursive: true, force: true }).catch(() => {
          });
        }
      };
      const runJavaTool = (0, import_sdk3.tool)({
        name: "run_java",
        description: import_sdk3.text`
      Compile and run a Java code snippet using javac/java (requires a JDK to be installed and
      on PATH). You have read/write access to the current working directory, but no external
      dependencies beyond the standard library are available.

      Pass the full source code as a string in the 'java' parameter. It must contain exactly one
      'public class <Name>' with a main method — the class name is detected automatically and
      used as the required filename.

      By default, compiling and running together will timeout in 5 seconds. You can extend this
      by setting 'timeout_seconds' up to a maximum of 60 seconds.

      You will get the stdout and stderr of the program. If compilation fails, the compiler's
      error output is returned instead so you can fix the code and retry.
    `,
        parameters: { java: import_zod2.z.string(), timeout_seconds: import_zod2.z.number().min(0.1).max(60).optional() },
        implementation: createSafeToolImplementation(
          originalRunJavaImplementation,
          allowJava,
          "run_java"
        )
      });
      tools.push(runJavaTool);
      const originalRunPyrightImplementation = createPyrightRunner();
      const runPyrightTool = (0, import_sdk3.tool)({
        name: "run_pyright",
        description: import_sdk3.text`
      Type-check a Python code snippet using the pinned Pyright npm dependency. This only performs static
      analysis — it does NOT execute the code.

      Pass the full source code as a string in the 'python' parameter.

      By default, type-checking will timeout in 15 seconds. You can extend this by setting
      'timeout_seconds' up to a maximum of 60 seconds.

      You will get Pyright's structured JSON diagnostic report as
      stdout, and an 'exit_code': 0 if no issues were found, 1 if type errors were found (fix the
      code and retry), or a higher number if pyright itself hit a configuration problem. Use this
      before run_python to catch type errors without spending an execution cycle.
    `,
        parameters: { python: import_zod2.z.string(), timeout_seconds: import_zod2.z.number().min(0.1).max(60).optional() },
        implementation: createSafeToolImplementation(
          originalRunPyrightImplementation,
          allowPyright,
          "run_pyright"
        )
      });
      tools.push(runPyrightTool);
      const confidenceAgentTools = createConfidenceAgentTools({
        isEnabled: enableConfidenceAgentTools,
        allowPyright,
        getWorkingDirectory: () => currentWorkingDirectory,
        runPyright: originalRunPyrightImplementation
      });
      for (const t2 of confidenceAgentTools) tools.push(t2);
      const saveFileTool = (0, import_sdk3.tool)({
        name: "save_file",
        description: import_sdk3.text`
      Save content to a specified file in the current working directory.
      This tool returns the full path to the saved file. You should then
      output this full path to the user.
    `,
        parameters: {
          file_name: import_zod2.z.string().optional(),
          content: import_zod2.z.string().optional(),
          files: import_zod2.z.array(import_zod2.z.object({ file_name: import_zod2.z.string(), content: import_zod2.z.string() })).optional().describe("For saving multiple files at once. E.g. [{file_name: 'a.txt', content: 'hello'}]")
        },
        implementation: async ({ file_name, content, files }) => {
          const filesToSave = Array.isArray(files) ? files : [];
          if (file_name && content) {
            filesToSave.push({ file_name, content });
          }
          if (filesToSave.length === 0) {
            return { error: "Must provide either file_name and content, or a files array." };
          }
          const savedPaths = [];
          const errors = [];
          for (const file of filesToSave) {
            if (!file.file_name || file.file_name.trim().length === 0) {
              errors.push(`Filename cannot be empty`);
              continue;
            }
            if (file.file_name && /[ \*\?<>|"]/.test(file.file_name)) {
              errors.push("Filename " + file.file_name + " contains invalid characters");
            }
            try {
              const filePath = validatePath(currentWorkingDirectory, file.file_name);
              await (0, import_promises4.mkdir)((0, import_path8.dirname)(filePath), { recursive: true });
              await (0, import_promises4.writeFile)(filePath, file.content, "utf-8");
              savedPaths.push(filePath);
            } catch (e) {
              errors.push(`Failed to save ${file.file_name}: ${e instanceof Error ? e.message : String(e)}`);
            }
          }
          if (errors.length > 0 && savedPaths.length === 0) {
            return { error: errors.join("\n") };
          }
          return {
            success: true,
            paths: savedPaths,
            errors: errors.length > 0 ? errors : void 0
          };
        }
      });
      tools.push(saveFileTool);
      const replaceTextTool = (0, import_sdk3.tool)({
        name: "replace_text_in_file",
        description: import_sdk3.text`
      Replace a specific string in a file with a new string. 
      Useful for making small edits without rewriting the entire file.
      Ensure 'old_string' matches exactly (including whitespace) or the replace will fail.
    `,
        parameters: {
          file_name: import_zod2.z.string(),
          old_string: import_zod2.z.string().describe("The exact text to replace. Must be unique in the file."),
          new_string: import_zod2.z.string().describe("The text to insert in place of old_string.")
        },
        implementation: async ({ file_name, old_string, new_string }) => {
          try {
            if (!old_string || old_string.length === 0) {
              return { error: "old_string cannot be empty" };
            }
            const filePath = validatePath(currentWorkingDirectory, file_name);
            const content = await (0, import_promises4.readFile)(filePath, "utf-8");
            if (!content.includes(old_string)) {
              return { error: "Could not find the exact 'old_string' in the file. Please check whitespace and indentation." };
            }
            const occurrenceCount = content.split(old_string).length - 1;
            if (occurrenceCount > 1) {
              return { error: `Found ${occurrenceCount} occurrences of 'old_string'. Please provide more context (surrounding lines) in 'old_string' to make it unique.` };
            }
            const newContent = content.replace(old_string, new_string);
            await (0, import_promises4.writeFile)(filePath, newContent, "utf-8");
            return { success: true, message: `Successfully replaced text in ${file_name}` };
          } catch (e) {
            return { error: `Failed to replace text: ${e instanceof Error ? e.message : String(e)}` };
          }
        }
      });
      tools.push(replaceTextTool);
      const multiReplaceTextTool = (0, import_sdk3.tool)({
        name: "multi_replace_text",
        description: import_sdk3.text`
      Replace multiple scattered text blocks in a single file safely.
      Each replacement must specify start_line, end_line, old_string, and new_string.
      The old_string must perfectly match what is currently in the file.
    `,
        parameters: {
          file_name: import_zod2.z.string(),
          replacements: import_zod2.z.array(import_zod2.z.object({
            start_line: import_zod2.z.number().int().min(1),
            end_line: import_zod2.z.number().int().min(1),
            old_string: import_zod2.z.string(),
            new_string: import_zod2.z.string()
          })).describe("Array of replacements to make in the file")
        },
        implementation: async ({ file_name, replacements }) => {
          try {
            const filePath = validatePath(currentWorkingDirectory, file_name);
            const content = await (0, import_promises4.readFile)(filePath, "utf-8");
            let lines = content.split("\n");
            let errors = [];
            const sortedReplacements = [...replacements].sort((a, b) => b.start_line - a.start_line);
            for (const rep of sortedReplacements) {
              if (rep.start_line > rep.end_line) {
                errors.push(`Invalid range: start_line ${rep.start_line} > end_line ${rep.end_line}`);
                continue;
              }
              const chunk = lines.slice(rep.start_line - 1, rep.end_line).join("\n");
              if (!chunk.includes(rep.old_string)) {
                errors.push(`Could not find old_string between lines ${rep.start_line}-${rep.end_line}`);
                continue;
              }
              const newChunk = chunk.replace(rep.old_string, rep.new_string);
              const newChunkLines = newChunk.split("\n");
              lines.splice(rep.start_line - 1, rep.end_line - rep.start_line + 1, ...newChunkLines);
            }
            if (errors.length > 0) {
              return { error: "Replacements failed:\n" + errors.join("\n") };
            }
            await (0, import_promises4.writeFile)(filePath, lines.join("\n"), "utf-8");
            return { success: true, message: `Applied ${replacements.length} replacements to ${file_name}` };
          } catch (e) {
            return { error: `Failed to multi-replace: ${e instanceof Error ? e.message : String(e)}` };
          }
        }
      });
      tools.push(multiReplaceTextTool);
      const searchDirectoryTool = (0, import_sdk3.tool)({
        name: "search_directory",
        description: import_sdk3.text`
      Search an entire directory for a regex pattern (like grep).
      Returns matching file paths and line numbers.
    `,
        parameters: {
          directory_path: import_zod2.z.string().optional().describe("Directory to search. Defaults to workspace root."),
          pattern: import_zod2.z.string().describe("Regex pattern or string to search for"),
          use_regex: import_zod2.z.boolean().optional().default(false)
        },
        implementation: async ({ directory_path, pattern, use_regex }) => {
          try {
            const targetDir = directory_path ? validatePath(currentWorkingDirectory, directory_path) : currentWorkingDirectory;
            const regex = new RegExp(use_regex ? pattern : pattern.replace(/[.*+?^${}()|[\]\\]/g, "\\  tools.push(replaceTextTool);"), "g");
            const results = [];
            let searchedCount = 0;
            async function search(dir) {
              const files = await (0, import_promises4.readdir)(dir);
              for (const file of files) {
                if (file === "node_modules" || file === ".git" || file.startsWith(".")) continue;
                const fullPath = (0, import_path8.join)(dir, file);
                const st = await (0, import_promises4.stat)(fullPath);
                if (st.isDirectory()) {
                  await search(fullPath);
                } else if (st.isFile()) {
                  if (st.size > 2e6) continue;
                  try {
                    const content = await (0, import_promises4.readFile)(fullPath, "utf-8");
                    if (content.includes("\0")) continue;
                    const lines = content.split("\n");
                    for (let i = 0; i < lines.length; i++) {
                      if (lines[i].match(regex)) {
                        results.push(`${(0, import_path8.relative)(currentWorkingDirectory, fullPath)}:${i + 1} => ${lines[i].trim()}`);
                        if (results.length >= 100) return;
                      }
                    }
                    searchedCount++;
                  } catch (e) {
                  }
                }
              }
            }
            await search(targetDir);
            if (results.length === 0) return { message: `No matches found. Searched ${searchedCount} files.` };
            return { matches: results, message: `Found ${results.length} matches across ${searchedCount} files searched.` };
          } catch (e) {
            return { error: `Search failed: ${e instanceof Error ? e.message : String(e)}` };
          }
        }
      });
      tools.push(searchDirectoryTool);
      const runBackgroundCommandTool = (0, import_sdk3.tool)({
        name: "run_background_command",
        description: import_sdk3.text`
      Starts a long-running process in the background. The process is not blocked, allowing you to do other things.
      You MUST provide a timeout (max 10 hours) and a descriptive name.
    `,
        parameters: {
          command: import_zod2.z.string(),
          timeout_hours: import_zod2.z.number().max(10).describe("MANDATORY: How long the process is allowed to run before being killed."),
          name: import_zod2.z.string().describe("MANDATORY: A short, descriptive name for the background task (e.g. 'Vite Dev Server')")
        },
        implementation: async ({ command, timeout_hours, name }) => {
          try {
            if (!timeout_hours) return { error: "timeout_hours is MANDATORY" };
            if (!name) return { error: "name is MANDATORY" };
            const timeoutMs = timeout_hours * 60 * 60 * 1e3;
            const id = generateId();
            const isWindows = os3.platform() === "win32";
            const shellCmd = isWindows ? "cmd.exe" : "sh";
            const shellArgs = isWindows ? ["/c", command] : ["-c", command];
            const proc = (0, import_child_process3.spawn)(shellCmd, shellArgs, { cwd: currentWorkingDirectory });
            const bgCmd = {
              id,
              name,
              startTime: Date.now(),
              process: proc,
              timeoutMs,
              stdout: "",
              stderr: "",
              status: "running"
            };
            proc.stdout.on("data", (data) => {
              bgCmd.stdout += data.toString();
              if (bgCmd.stdout.length > 5e4) bgCmd.stdout = bgCmd.stdout.slice(-5e4);
            });
            proc.stderr.on("data", (data) => {
              bgCmd.stderr += data.toString();
              if (bgCmd.stderr.length > 5e4) bgCmd.stderr = bgCmd.stderr.slice(-5e4);
            });
            proc.on("close", (code) => {
              bgCmd.status = bgCmd.status === "cancelled" || bgCmd.status === "timeout" ? bgCmd.status : "completed";
              bgCmd.exitCode = code;
              if (bgCmd.timeoutHandle) clearTimeout(bgCmd.timeoutHandle);
            });
            proc.on("error", (err) => {
              bgCmd.status = "error";
              bgCmd.stderr += `
Error: ${err.message}`;
            });
            bgCmd.timeoutHandle = setTimeout(() => {
              if (bgCmd.status === "running") {
                bgCmd.status = "timeout";
                proc.kill("SIGKILL");
              }
            }, timeoutMs);
            backgroundCommands.set(id, bgCmd);
            await new Promise((resolve5) => setTimeout(resolve5, 500));
            return {
              id,
              status: bgCmd.status,
              message: `Command launched. Use check_background_command with ID ${id} to poll output.`,
              initial_stdout: bgCmd.stdout.slice(-1e3),
              initial_stderr: bgCmd.stderr.slice(-1e3)
            };
          } catch (e) {
            return { error: `Failed to launch: ${e instanceof Error ? e.message : String(e)}` };
          }
        }
      });
      tools.push(runBackgroundCommandTool);
      const checkBackgroundCommandTool = (0, import_sdk3.tool)({
        name: "check_background_command",
        description: "Check the status, stdout, and stderr of a running or completed background command.",
        parameters: {
          id: import_zod2.z.string()
        },
        implementation: async ({ id }) => {
          const bgCmd = backgroundCommands.get(id);
          if (!bgCmd) return { error: `No background command found with ID ${id}` };
          return {
            id: bgCmd.id,
            name: bgCmd.name,
            status: bgCmd.status,
            duration_seconds: Math.floor((Date.now() - bgCmd.startTime) / 1e3),
            stdout_tail: bgCmd.stdout.slice(-2e3),
            // last 2000 chars
            stderr_tail: bgCmd.stderr.slice(-2e3),
            exitCode: bgCmd.exitCode
          };
        }
      });
      tools.push(checkBackgroundCommandTool);
      const cancelBackgroundCommandTool = (0, import_sdk3.tool)({
        name: "cancel_background_command",
        description: "Kills a running background command.",
        parameters: {
          id: import_zod2.z.string()
        },
        implementation: async ({ id }) => {
          const bgCmd = backgroundCommands.get(id);
          if (!bgCmd) return { error: `No background command found with ID ${id}` };
          if (bgCmd.status !== "running") return { message: `Command is already ${bgCmd.status}` };
          bgCmd.status = "cancelled";
          bgCmd.process.kill("SIGKILL");
          if (bgCmd.timeoutHandle) clearTimeout(bgCmd.timeoutHandle);
          return { success: true, message: `Command ${id} killed.` };
        }
      });
      tools.push(cancelBackgroundCommandTool);
      const listDirectoryTool = (0, import_sdk3.tool)({
        name: "list_directory",
        description: "List the files and directories in the current working directory or a specified subdirectory.",
        parameters: {
          path: import_zod2.z.string().optional().describe("The path to the directory to list. Defaults to current working directory.")
        },
        implementation: async ({ path }) => {
          const targetPath = path ? validatePath(currentWorkingDirectory, path) : currentWorkingDirectory;
          const files = await (0, import_promises4.readdir)(targetPath);
          return {
            files
          };
        }
      });
      tools.push(listDirectoryTool);
      const readFileTool = (0, import_sdk3.tool)({
        name: "read_file",
        description: "Read the content of a file in the current working directory.",
        parameters: {
          file_name: import_zod2.z.string()
        },
        implementation: async ({ file_name }) => {
          const filePath = validatePath(currentWorkingDirectory, file_name);
          const stats = await (0, import_promises4.stat)(filePath);
          if (stats.size > 1e7) {
            return { error: "File too large (>10MB)" };
          }
          const buffer = await (0, import_promises4.readFile)(filePath);
          const checkBuffer = buffer.subarray(0, Math.min(buffer.length, 1024));
          if (checkBuffer.includes(0)) {
            return { error: "File appears to be binary and cannot be read as text." };
          }
          const content = buffer.toString("utf-8");
          return {
            content
          };
        }
      });
      tools.push(readFileTool);
      const originalExecuteCommandImplementation = async ({ command, input, timeout_seconds }) => {
        const childProcess = (0, import_child_process3.spawn)(command, [], {
          cwd: currentWorkingDirectory,
          shell: true,
          timeout: (timeout_seconds ?? 5) * 1e3,
          stdio: "pipe"
        });
        if (input) {
          childProcess.stdin.write(input);
          childProcess.stdin.end();
        } else {
          childProcess.stdin.end();
        }
        let stdout = "";
        let stderr = "";
        childProcess.stdout.setEncoding("utf-8");
        childProcess.stderr.setEncoding("utf-8");
        childProcess.stdout.on("data", (data) => {
          stdout += data;
        });
        childProcess.stderr.on("data", (data) => {
          stderr += data;
        });
        await new Promise((resolve5, reject) => {
          childProcess.on("close", (code) => {
            if (code === 0) {
              resolve5();
            } else {
              reject(new Error(`Process exited with code ${code}. Stderr: ${stderr}`));
            }
          });
          childProcess.on("error", (err) => {
            reject(err);
          });
        });
        return {
          stdout: stdout.trim(),
          stderr: stderr.trim()
        };
      };
      const executeCommandTool = (0, import_sdk3.tool)({
        name: "execute_command",
        description: import_sdk3.text`
      Execute a shell command in the current working directory.
      Returns the stdout and stderr output of the command.
      You can optionally provide input to be piped to the command's stdin.

      IMPORTANT: The host operating system is '${process.platform}'. 
      If the OS is 'win32' (Windows), do NOT use 'bash' or 'sh' commands unless you are certain WSL is available.
      Instead, use standard Windows 'cmd' or 'powershell' syntax.
    `,
        parameters: {
          command: import_zod2.z.string(),
          input: import_zod2.z.string().optional().describe("Input text to pipe to the command's stdin."),
          timeout_seconds: import_zod2.z.number().min(0.1).max(60).optional().describe("Timeout in seconds (default: 5, max: 60)")
        },
        implementation: createSafeToolImplementation(
          originalExecuteCommandImplementation,
          allowShell,
          "execute_command"
        )
      });
      tools.push(executeCommandTool);
      const makeDirectoryTool = (0, import_sdk3.tool)({
        name: "make_directory",
        description: "Create a new directory in the current working directory.",
        parameters: {
          directory_name: import_zod2.z.string()
        },
        implementation: async ({ directory_name }) => {
          const dirPath = validatePath(currentWorkingDirectory, directory_name);
          await (0, import_promises4.mkdir)(dirPath, { recursive: true });
          return {
            success: true,
            path: dirPath
          };
        }
      });
      tools.push(makeDirectoryTool);
      const deletePathTool = (0, import_sdk3.tool)({
        name: "delete_path",
        description: "Delete a file or directory in the current working directory. Be careful!",
        parameters: {
          path: import_zod2.z.string()
        },
        implementation: async ({ path }) => {
          const targetPath = validatePath(currentWorkingDirectory, path);
          await (0, import_promises4.rm)(targetPath, { recursive: true, force: true });
          return {
            success: true,
            path: targetPath
          };
        }
      });
      tools.push(deletePathTool);
      const deleteFilesByPatternTool = (0, import_sdk3.tool)({
        name: "delete_files_by_pattern",
        description: "Delete multiple files in the current directory that match a regex pattern.",
        parameters: {
          pattern: import_zod2.z.string().describe("Regex pattern to match filenames (e.g., '^auto_gen_.*\\.txt$')")
        },
        implementation: async ({ pattern }) => {
          try {
            if (pattern.length > 100) {
              return { error: "Pattern too complex (max 100 characters)" };
            }
            const regex = new RegExp(pattern);
            const start = Date.now();
            regex.test("safe_test_string_for_redos_check_1234567890_safe_test_string_for_redos_check_1234567890");
            if (Date.now() - start > 100) {
              return { error: "Pattern is too complex or slow (ReDoS protection)." };
            }
            const files = await (0, import_promises4.readdir)(currentWorkingDirectory);
            const deleted = [];
            for (const file of files) {
              if (regex.test(file)) {
                await (0, import_promises4.rm)((0, import_path8.join)(currentWorkingDirectory, file), { force: true });
                deleted.push(file);
              }
            }
            return { deleted_count: deleted.length, deleted_files: deleted };
          } catch (e) {
            return { error: `Failed to delete files: ${e instanceof Error ? e.message : String(e)}` };
          }
        }
      });
      tools.push(deleteFilesByPatternTool);
      const originalRunInTerminalImplementation = async ({ command }) => {
        if (process.platform === "win32") {
          const escapedDir = currentWorkingDirectory.replace(/"/g, '""');
          const escapedCmd = command.replace(/"/g, '""');
          const shellCommand = `start "" /D "${escapedDir}" cmd.exe /k "${escapedCmd}"`;
          const child = (0, import_child_process3.spawn)("cmd.exe", ["/c", shellCommand], {
            detached: true,
            stdio: "ignore",
            windowsHide: false,
            windowsVerbatimArguments: true
          });
          child.unref();
        } else {
          if (process.platform === "darwin") {
            const safeCmd = command.replace(/\\/g, "\\\\").replace(/"/g, '\\"');
            const safeCwd = currentWorkingDirectory.replace(/\\/g, "\\\\").replace(/"/g, '\\"');
            const appleScript = `
          tell application "Terminal"
            do script "cd \\"${safeCwd}\\" && ${safeCmd}"
            activate
          end tell
        `;
            const child = (0, import_child_process3.spawn)("osascript", ["-e", appleScript], { detached: true, stdio: "ignore" });
            child.unref();
          } else {
            const safeCwd = currentWorkingDirectory.replace(/'/g, "'\\''");
            const safeCmd = command.replace(/'/g, "'\\''");
            const bashScript = `cd '${safeCwd}' && ${safeCmd}; bash`;
            const child = (0, import_child_process3.spawn)("x-terminal-emulator", ["-e", "bash", "-c", bashScript], {
              detached: true,
              stdio: "ignore"
            });
            child.on("error", (e) => {
              const child2 = (0, import_child_process3.spawn)("gnome-terminal", ["--", "bash", "-c", bashScript], {
                detached: true,
                stdio: "ignore"
              });
              child2.unref();
            });
            child.unref();
          }
        }
        return {
          success: true,
          message: "Terminal window launched. Please check your taskbar."
        };
      };
      const runInTerminalTool = (0, import_sdk3.tool)({
        name: "run_in_terminal",
        description: import_sdk3.text`
      Launch a command in a new, separate interactive terminal window. 
      Use this for scripts that require user interaction (input/output) or to open a shell in a specific directory.
      (Currently optimized for Windows).
    `,
        parameters: {
          command: import_zod2.z.string()
        },
        implementation: createSafeToolImplementation(
          originalRunInTerminalImplementation,
          allowTerminal,
          "run_in_terminal"
        )
      });
      tools.push(runInTerminalTool);
      const webSearchTool = (0, import_sdk3.tool)({
        name: "web_search",
        description: "Search the web using multiple providers (DuckDuckGo, Google, Bing). Uses no-key, no-Chrome providers first, then browser providers as fallback.",
        parameters: {
          query: import_zod2.z.string(),
          providers: import_zod2.z.array(import_zod2.z.enum(["duckduckgo-api", "duckduckgo-fetch", "duckduckgo-html", "google", "bing"])).optional().describe("Optional: List of specific providers. If omitted, fallback chain is: DDG Fetch (no Chrome) -> DDG API -> DDG browser -> Google -> Bing.")
        },
        implementation: async ({ query, providers }) => {
          const results = [];
          const errors = [];
          const logs = [];
          const decodeHtmlEntities = (value) => value.replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&apos;/g, "'").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&nbsp;/g, " ").replace(/&amp;/g, "&");
          const stripHtml = (value) => decodeHtmlEntities(value).replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
          const normalizeDuckDuckGoLink = (link) => {
            const decoded = decodeHtmlEntities(link);
            const absolute = decoded.startsWith("//") ? `https:${decoded}` : decoded.startsWith("/") ? `https://duckduckgo.com${decoded}` : decoded;
            try {
              const parsed = new URL(absolute);
              const redirect = parsed.searchParams.get("uddg");
              if (redirect) {
                return decodeURIComponent(redirect);
              }
            } catch {
            }
            return absolute;
          };
          const parseDuckDuckGoHtml = (html, provider) => {
            const parsedResults = [];
            const titleRegex = /<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/gi;
            let match;
            while ((match = titleRegex.exec(html)) !== null) {
              const link = normalizeDuckDuckGoLink(match[1]);
              const title = stripHtml(match[2]);
              const nearbyHtml = html.slice(match.index, Math.min(html.length, match.index + 1800));
              const snippetMatch = nearbyHtml.match(/class="result__snippet"[^>]*>([\s\S]*?)<\/(?:a|div)>/i);
              const snippet = snippetMatch ? stripHtml(snippetMatch[1]) : "";
              if (title && link) {
                parsedResults.push({ title, link, snippet, provider });
              }
              if (parsedResults.length >= 10) break;
            }
            return parsedResults;
          };
          let sharedBrowser = null;
          const getBrowser = async () => {
            if (!sharedBrowser) {
              const puppeteer = await import("puppeteer");
              sharedBrowser = await puppeteer.launch({
                headless: true,
                args: ["--no-sandbox", "--disable-setuid-sandbox"]
              });
            }
            return sharedBrowser;
          };
          const searchFunctions = {
            "duckduckgo-api": async (q) => {
              const { search, SafeSearchType } = await import("duck-duck-scrape");
              let attempt = 0;
              let lastError = null;
              while (attempt < 2) {
                try {
                  const r = await search(q, { safeSearch: SafeSearchType.OFF });
                  if (r.results && r.results.length > 0) {
                    return r.results.slice(0, 10).map((result2) => ({
                      title: result2.title,
                      link: result2.url,
                      snippet: result2.description,
                      provider: "duckduckgo-api"
                    }));
                  }
                  break;
                } catch (e) {
                  lastError = e;
                  attempt++;
                  await new Promise((res) => setTimeout(res, 1e3));
                }
              }
              if (lastError) {
                throw lastError;
              }
              throw new Error("DuckDuckGo API returned no results");
            },
            "duckduckgo-fetch": async (q) => {
              const response = await fetch(`https://html.duckduckgo.com/html/?q=${encodeURIComponent(q)}`, {
                headers: {
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                  "Accept-Language": "en-US,en;q=0.9"
                }
              });
              if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
              }
              const html = await response.text();
              const extracted = parseDuckDuckGoHtml(html, "duckduckgo-fetch");
              if (extracted.length > 0) return extracted;
              throw new Error("No results parsed from DuckDuckGo HTML");
            },
            "duckduckgo-html": async (q) => {
              const browser = await getBrowser();
              try {
                const page = await browser.newPage();
                await page.goto(`https://html.duckduckgo.com/html/?q=${encodeURIComponent(q)}`, { waitUntil: "networkidle2", timeout: 15e3 });
                const html = await page.content();
                const extracted = parseDuckDuckGoHtml(html, "duckduckgo-html");
                if (extracted.length > 0) return extracted;
                throw new Error("No results found");
              } finally {
                await browser.close();
              }
            },
            "google": async (q) => {
              const browser = await getBrowser();
              try {
                const page = await browser.newPage();
                await page.goto(`https://www.google.com/search?q=${encodeURIComponent(q)}`, { waitUntil: "networkidle2", timeout: 15e3 });
                const extracted = await page.evaluate(() => {
                  const items = document.querySelectorAll("div.g");
                  const data = [];
                  for (const item of items) {
                    const titleEl = item.querySelector("h3");
                    const linkEl = item.querySelector("a");
                    const snippetEl = item.querySelector('div[style*="-webkit-line-clamp"]') || item.querySelector("div.VwiC3b");
                    if (titleEl && linkEl) {
                      data.push({
                        title: titleEl.innerText,
                        link: linkEl.getAttribute("href") || "",
                        snippet: snippetEl ? snippetEl.innerText : "",
                        provider: "google"
                      });
                    }
                  }
                  return data;
                });
                if (extracted.length > 0) return extracted.slice(0, 10);
                throw new Error("No results found");
              } finally {
                await browser.close();
              }
            },
            "bing": async (q) => {
              const browser = await getBrowser();
              try {
                const page = await browser.newPage();
                await page.goto(`https://www.bing.com/search?q=${encodeURIComponent(q)}`, { waitUntil: "networkidle2", timeout: 15e3 });
                const extracted = await page.evaluate(() => {
                  const items = document.querySelectorAll("li.b_algo");
                  const data = [];
                  for (const item of items) {
                    const titleEl = item.querySelector("h2 a");
                    const linkEl = item.querySelector("h2 a");
                    const snippetEl = item.querySelector("p");
                    if (titleEl && linkEl) {
                      data.push({
                        title: titleEl.innerText,
                        link: linkEl.getAttribute("href") || "",
                        snippet: snippetEl ? snippetEl.innerText : "",
                        provider: "bing"
                      });
                    }
                  }
                  return data;
                });
                if (extracted.length > 0) return extracted.slice(0, 10);
                throw new Error("No results found");
              } finally {
                await browser.close();
              }
            }
          };
          if (providers && providers.length > 0) {
            for (const providerKey of providers) {
              try {
                logs.push(`[Manual] Attempting ${providerKey}...`);
                const pResults = await searchFunctions[providerKey](query);
                results.push(...pResults);
                logs.push(`[Manual] Success: ${providerKey} found ${pResults.length} results.`);
              } catch (e) {
                const errMsg = e instanceof Error ? e.message : String(e);
                errors.push(`${providerKey}: ${errMsg}`);
                logs.push(`[Manual] Failed: ${providerKey} - ${errMsg}`);
              }
            }
          } else {
            const chain = ["duckduckgo-fetch", "duckduckgo-api", "duckduckgo-html", "google", "bing"];
            const browserProviders = ["duckduckgo-html", "google", "bing"];
            let chromeUnavailable = false;
            for (let i = 0; i < chain.length; i++) {
              const providerKey = chain[i];
              if (chromeUnavailable && browserProviders.includes(providerKey)) {
                logs.push(`[Fallback Chain] Skipping ${providerKey}: Chrome not available on this system.`);
                continue;
              }
              const nextProvider = chain[i + 1];
              try {
                logs.push(`[Fallback Chain] Attempting ${providerKey}...`);
                const pResults = await searchFunctions[providerKey](query);
                results.push(...pResults);
                logs.push(`[Fallback Chain] Success: ${providerKey} found ${pResults.length} results. Stopping chain.`);
                break;
              } catch (e) {
                const errMsg = e instanceof Error ? e.message : String(e);
                errors.push(`${providerKey}: ${errMsg}`);
                if (/chrome|chromium/i.test(errMsg) && browserProviders.includes(providerKey)) {
                  chromeUnavailable = true;
                  logs.push(`[Fallback Chain] Failed: ${providerKey} - Chrome not available. Skipping all browser-based providers.`);
                } else {
                  const nextMsg = nextProvider ? `Falling back to ${nextProvider}...` : "No more providers.";
                  logs.push(`[Fallback Chain] Failed: ${providerKey} - ${errMsg}. ${nextMsg}`);
                }
              }
            }
          }
          if (results.length === 0) {
            return {
              error: "All attempted search providers failed.",
              attempts: errors,
              trace: logs
            };
          }
          const seenLinks = /* @__PURE__ */ new Set();
          const dedupedResults = results.filter((r) => {
            const key = r.link.trim();
            if (!key || seenLinks.has(key)) return false;
            seenLinks.add(key);
            return true;
          });
          return {
            results: dedupedResults,
            meta: {
              total_found: dedupedResults.length,
              providers_used: [...new Set(dedupedResults.map((r) => r.provider))],
              no_api_key_required: true,
              trace: logs
            }
          };
        }
      });
      tools.push(webSearchTool);
      const moveFileTool = (0, import_sdk3.tool)({
        name: "move_file",
        description: "Move or rename a file or directory.",
        parameters: {
          source: import_zod2.z.string(),
          destination: import_zod2.z.string()
        },
        implementation: async ({ source, destination }) => {
          const sourcePath = validatePath(currentWorkingDirectory, source);
          const destPath = validatePath(currentWorkingDirectory, destination);
          await (0, import_promises4.rename)(sourcePath, destPath);
          return {
            success: true,
            from: sourcePath,
            to: destPath
          };
        }
      });
      tools.push(moveFileTool);
      const copyFileTool = (0, import_sdk3.tool)({
        name: "copy_file",
        description: "Copy a file to a new location.",
        parameters: {
          source: import_zod2.z.string(),
          destination: import_zod2.z.string()
        },
        implementation: async ({ source, destination }) => {
          const sourcePath = validatePath(currentWorkingDirectory, source);
          const destPath = validatePath(currentWorkingDirectory, destination);
          await (0, import_promises4.copyFile)(sourcePath, destPath);
          return {
            success: true,
            from: sourcePath,
            to: destPath
          };
        }
      });
      tools.push(copyFileTool);
      const fetchWebContentTool = (0, import_sdk3.tool)({
        name: "fetch_web_content",
        description: "Fetch the clean, text-based content of a webpage URL.",
        parameters: {
          url: import_zod2.z.string()
        },
        implementation: async ({ url }) => {
          try {
            const response = await fetch(url);
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
            let text3 = await response.text();
            const result2 = {
              url,
              status: response.status
            };
            const titleMatch = text3.match(/<title[^>]*>([^<]+)<\/title>/i);
            if (titleMatch) result2.title = titleMatch[1];
            const { compile } = await import("html-to-text");
            const compiledConvert = compile({
              wordwrap: false,
              selectors: [
                { selector: "a", options: { ignoreHref: true } },
                { selector: "img", format: "skip" }
              ]
            });
            text3 = compiledConvert(text3);
            result2.content = text3.substring(0, 4e4) + (text3.length > 4e4 ? "... (truncated)" : "");
            return result2;
          } catch (error) {
            return {
              error: `Failed to fetch URL: ${error instanceof Error ? error.message : String(error)}`
            };
          }
        }
      });
      tools.push(fetchWebContentTool);
      const ragWebContentTool = (0, import_sdk3.tool)({
        name: "rag_web_content",
        description: "Fetch content from a URL, and then use RAG to find and return only the text chunks most relevant to a specific query.",
        parameters: {
          url: import_zod2.z.string(),
          query: import_zod2.z.string()
        },
        implementation: async ({ url, query }) => {
          try {
            const response = await fetch(url);
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
            let text3 = await response.text();
            const { compile } = await import("html-to-text");
            const compiledConvert = compile({
              wordwrap: false,
              selectors: [
                { selector: "a", options: { ignoreHref: true } },
                { selector: "img", format: "skip" }
              ]
            });
            text3 = compiledConvert(text3);
            if (text3.length === 0) {
              return { error: "Could not extract any text from the URL." };
            }
            if (!client2) {
              return { error: "LM Studio Client is not available. RAG features require the client to be initialized." };
            }
            const ragResults = await performRagOnText(text3, query, client2, embeddingModelName);
            return {
              url,
              query,
              relevant_chunks: ragResults
            };
          } catch (error) {
            return { error: `Failed during RAG web search: ${error instanceof Error ? error.message : String(error)}` };
          }
        }
      });
      tools.push(ragWebContentTool);
      const getSystemInfoTool = (0, import_sdk3.tool)({
        name: "get_system_info",
        description: "Get information about the system (OS, CPU, Memory).",
        parameters: {},
        implementation: async () => {
          return {
            platform: os3.platform(),
            arch: os3.arch(),
            release: os3.release(),
            hostname: os3.hostname(),
            total_memory: os3.totalmem(),
            free_memory: os3.freemem(),
            cpus: os3.cpus().length,
            node_version: process.version
          };
        }
      });
      tools.push(getSystemInfoTool);
      const findFilesTool = (0, import_sdk3.tool)({
        name: "find_files",
        description: "Find files recursively in the current directory matching a name pattern.",
        parameters: {
          pattern: import_zod2.z.string().describe("Substring to match in filename (case-insensitive)"),
          max_depth: import_zod2.z.number().optional().describe("Maximum depth to search (default: 5)")
        },
        implementation: async ({ pattern, max_depth }) => {
          const depthLimit = max_depth ?? 5;
          const foundFiles = [];
          const lowerPattern = pattern.toLowerCase();
          async function scan(dir, currentDepth) {
            if (currentDepth > depthLimit) return;
            try {
              const entries = await (0, import_promises4.readdir)(dir, { withFileTypes: true });
              for (const entry of entries) {
                if (["node_modules", ".git", "dist", ".lmstudio"].includes(entry.name)) continue;
                const fullPath = (0, import_path8.join)(dir, entry.name);
                if (entry.isDirectory()) {
                  await scan(fullPath, currentDepth + 1);
                } else if (entry.isFile()) {
                  if (entry.name.toLowerCase().includes(lowerPattern)) {
                    foundFiles.push(fullPath);
                  }
                }
              }
            } catch (e) {
            }
          }
          await scan(currentWorkingDirectory, 0);
          return {
            found_files: foundFiles.slice(0, 100),
            // Limit results
            count: foundFiles.length
          };
        }
      });
      tools.push(findFilesTool);
      const fuzzyFindLocalFilesTool = (0, import_sdk3.tool)({
        name: "fuzzy_find_local_files",
        description: "Fuzzy find local files by path/name similarity using Levenshtein scoring.",
        parameters: {
          query: import_zod2.z.string().describe("Search query to match against file names/paths."),
          path: import_zod2.z.string().optional().describe("Sub-directory to search in (default: current directory)."),
          max_results: import_zod2.z.number().int().min(1).max(20).optional().describe("Max results to return (default: 5).")
        },
        implementation: async ({ query, path = ".", max_results = 5 }) => {
          try {
            const targetDir = validatePath(currentWorkingDirectory, path);
            const entries = await (0, import_promises4.readdir)(targetDir, { recursive: true, withFileTypes: true });
            const files = entries.filter((entry) => entry.isFile()).map((entry) => {
              const fullPath = (0, import_path8.join)(entry.path, entry.name);
              const relativePath = (0, import_path8.relative)(targetDir, fullPath);
              return relativePath.replace(/\\/g, "/");
            });
            const ranked = rankFuzzyMatches(query, files, max_results);
            return {
              query,
              path: targetDir,
              results: ranked.map((item) => ({
                path: item.value,
                score: item.score
              }))
            };
          } catch (error) {
            return { error: `Fuzzy file search failed: ${error instanceof Error ? error.message : String(error)}` };
          }
        }
      });
      tools.push(fuzzyFindLocalFilesTool);
      const getFileMetadataTool = (0, import_sdk3.tool)({
        name: "get_file_metadata",
        description: "Get metadata (size, dates) for a specific file.",
        parameters: {
          path: import_zod2.z.string()
        },
        implementation: async ({ path }) => {
          try {
            const targetPath = validatePath(currentWorkingDirectory, path);
            const stats = await (0, import_promises4.stat)(targetPath);
            return {
              path: targetPath,
              size: stats.size,
              created: stats.birthtime,
              modified: stats.mtime,
              is_directory: stats.isDirectory(),
              is_file: stats.isFile()
            };
          } catch (error) {
            return { error: `Failed to get metadata: ${error instanceof Error ? error.message : String(error)}` };
          }
        }
      });
      tools.push(getFileMetadataTool);
      const readClipboardTool = (0, import_sdk3.tool)({
        name: "read_clipboard",
        description: "Read text content from the system clipboard.",
        parameters: {},
        implementation: async () => {
          let command = "";
          let args = [];
          if (process.platform === "win32") {
            command = "powershell";
            args = ["-command", "Get-Clipboard"];
          } else if (process.platform === "darwin") {
            command = "pbpaste";
          } else {
            command = "xclip";
            args = ["-selection", "clipboard", "-o"];
          }
          return Promise.race([
            new Promise((resolve5) => {
              const child = (0, import_child_process3.spawn)(command, args);
              let output = "";
              let error = "";
              child.stdout.on("data", (data) => output += data.toString());
              child.stderr.on("data", (data) => error += data.toString());
              child.on("close", (code) => {
                if (code === 0) {
                  resolve5({ content: output.trim() });
                } else {
                  resolve5({ error: `Failed to read clipboard. Exit code: ${code}. Error: ${error}` });
                }
              });
              child.on("error", (err) => {
                resolve5({ error: `Failed to spawn clipboard command: ${err.message}` });
              });
            }),
            new Promise(
              (_, reject) => setTimeout(() => reject(new Error("Clipboard operation timeout")), 5e3)
            )
          ]).catch((err) => ({ error: err.message }));
        }
      });
      tools.push(readClipboardTool);
      const writeClipboardTool = (0, import_sdk3.tool)({
        name: "write_clipboard",
        description: "Write text content to the system clipboard.",
        parameters: {
          content: import_zod2.z.string()
        },
        implementation: async ({ content }) => {
          let command = "";
          let args = [];
          let input = content;
          if (process.platform === "win32") {
            command = "powershell";
            const base64Content = Buffer.from(content, "utf8").toString("base64");
            args = ["-command", `$str = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('${base64Content}')); Set-Clipboard -Value $str`];
            input = "";
          } else if (process.platform === "darwin") {
            command = "pbcopy";
          } else {
            command = "xclip";
            args = ["-selection", "clipboard", "-i"];
          }
          return Promise.race([
            new Promise((resolve5) => {
              const child = (0, import_child_process3.spawn)(command, args, { stdio: ["pipe", "ignore", "pipe"] });
              if (input && process.platform !== "win32") {
                child.stdin.write(input);
                child.stdin.end();
              } else if (process.platform === "win32") {
                child.stdin.end();
              }
              let error = "";
              child.stderr.on("data", (data) => error += data.toString());
              child.on("close", (code) => {
                if (code === 0) {
                  resolve5({ success: true });
                } else {
                  resolve5({ error: `Failed to write to clipboard. Exit code: ${code}. Error: ${error}` });
                }
              });
              child.on("error", (err) => {
                resolve5({ error: `Failed to spawn clipboard command: ${err.message}` });
              });
            }),
            new Promise(
              (_, reject) => setTimeout(() => reject(new Error("Clipboard operation timeout")), 5e3)
            )
          ]).catch((err) => ({ error: err.message }));
        }
      });
      tools.push(writeClipboardTool);
      const openFileTool = (0, import_sdk3.tool)({
        name: "open_file",
        description: "Open a file or URL in the system's default application. Use this to preview images, PDFs, or open web pages.",
        parameters: {
          target: import_zod2.z.string().describe("File path or URL")
        },
        implementation: async ({ target }) => {
          let targetToOpen = target;
          if (!target.startsWith("http://") && !target.startsWith("https://")) {
            targetToOpen = validatePath(currentWorkingDirectory, target);
          }
          const open = (await import("open")).default;
          await open(targetToOpen);
          return { success: true, message: `Opened ${targetToOpen}` };
        }
      });
      tools.push(openFileTool);
      const previewHtmlTool = (0, import_sdk3.tool)({
        name: "preview_html",
        description: "Render and preview HTML content in the system's default browser. Useful for visualizing code or UIs.",
        parameters: {
          html_content: import_zod2.z.string(),
          file_name: import_zod2.z.string().optional().describe("Optional filename (default: preview.html)")
        },
        implementation: async ({ html_content, file_name }) => {
          const name = file_name || `preview_${Date.now()}.html`;
          const filePath = validatePath(currentWorkingDirectory, name);
          await (0, import_promises4.writeFile)(filePath, html_content, "utf-8");
          const open = (await import("open")).default;
          await open(filePath);
          return { success: true, path: filePath, message: "HTML preview launched in browser." };
        }
      });
      tools.push(previewHtmlTool);
      const browserActionSchema = import_zod2.z.object({
        type: import_zod2.z.enum(["wait_for_selector", "wait", "click", "type", "press", "select", "hover", "scroll", "evaluate"]),
        selector: import_zod2.z.string().optional().describe("CSS selector used by selector-based actions."),
        text: import_zod2.z.string().optional().describe("Text payload for type action."),
        value: import_zod2.z.string().optional().describe("Value payload for select action."),
        key: import_zod2.z.string().optional().describe("Keyboard key for press action (e.g., Enter, Tab)."),
        milliseconds: import_zod2.z.number().int().min(0).max(3e4).optional().describe("Delay in milliseconds for wait action."),
        x: import_zod2.z.number().optional().describe("Horizontal scroll delta for scroll action."),
        y: import_zod2.z.number().optional().describe("Vertical scroll delta for scroll action."),
        script: import_zod2.z.string().optional().describe("JavaScript snippet for evaluate action (executed in page context).")
      });
      const browserSessionOpenTool = (0, import_sdk3.tool)({
        name: "browser_session_open",
        description: "Open a persistent browser session (single active page), navigate to URL, and return page text for context.",
        parameters: {
          url: import_zod2.z.string(),
          wait_for_selector: import_zod2.z.string().optional().describe("Optional selector to wait for after navigation."),
          include_page_text: import_zod2.z.boolean().optional().describe("If true (default), returns full page text content after opening.")
        },
        implementation: createSafeToolImplementation(async ({ url, wait_for_selector, include_page_text = true }) => {
          try {
            if (browserSession) {
              await browserSession.browser.close().catch(() => {
              });
              browserSession = null;
            }
            const puppeteer = await import("puppeteer");
            const browser = await puppeteer.launch({
              headless: true,
              args: ["--no-sandbox", "--disable-setuid-sandbox"]
            });
            const page = await browser.newPage();
            await page.goto(url, { waitUntil: "networkidle0", timeout: 3e4 });
            if (wait_for_selector) {
              await page.waitForSelector(wait_for_selector, { timeout: 15e3 });
            }
            browserSession = {
              browser,
              page,
              currentUrl: page.url()
            };
            const pageText = include_page_text ? await page.evaluate(() => document.body.innerText || "") : void 0;
            return {
              success: true,
              session_active: true,
              url: page.url(),
              title: await page.title(),
              text_content: pageText,
              text_length: pageText ? pageText.length : 0,
              message: "Browser session opened."
            };
          } catch (error) {
            return { error: `Failed to open browser session: ${error instanceof Error ? error.message : String(error)}` };
          }
        }, allowBrowserControl, "browser_control")
      });
      tools.push(browserSessionOpenTool);
      const browserSessionControlTool = (0, import_sdk3.tool)({
        name: "browser_session_control",
        description: "Control the active persistent browser session. Supports actions, page reading, screenshot capture, and fuzzy finding in-page text/selectors.",
        parameters: {
          actions: import_zod2.z.array(browserActionSchema).optional().describe("Optional scripted browser actions to execute on the active page."),
          read_page: import_zod2.z.boolean().optional().describe("If true (default), returns page metadata. Full text is returned only on URL change or when full_read=true."),
          full_read: import_zod2.z.boolean().optional().describe("If true, forces full page text output even when URL has not changed."),
          screenshot_path: import_zod2.z.string().optional().describe("Optional screenshot output path."),
          full_page_screenshot: import_zod2.z.boolean().optional().describe("If true, captures full page screenshot."),
          fuzzy_find: import_zod2.z.string().optional().describe("Optional fuzzy-find query for in-page content/selectors."),
          max_results: import_zod2.z.number().int().min(1).max(20).optional().describe("Max fuzzy results to return (default: 5).")
        },
        implementation: createSafeToolImplementation(async ({ actions, read_page = true, full_read = false, screenshot_path, full_page_screenshot, fuzzy_find, max_results = 5 }) => {
          if (!browserSession) {
            return { error: "No active browser session. Call 'browser_session_open' first." };
          }
          try {
            const beforeUrl = browserSession.page.url();
            const actionLog = await executeBrowserActions(browserSession.page, actions || []);
            const afterUrl = browserSession.page.url();
            const urlChanged = beforeUrl !== afterUrl;
            browserSession.currentUrl = afterUrl;
            let screenshotSaved = false;
            if (screenshot_path) {
              const screenshotFilePath = validatePath(currentWorkingDirectory, screenshot_path);
              await browserSession.page.screenshot({ path: screenshotFilePath, fullPage: full_page_screenshot ?? false });
              screenshotSaved = true;
            }
            let pageSnapshot = void 0;
            if (read_page) {
              const title = await browserSession.page.title();
              if (urlChanged || full_read) {
                const textContent = await browserSession.page.evaluate(() => document.body.innerText || "");
                pageSnapshot = {
                  url: afterUrl,
                  title,
                  text_content: textContent,
                  text_length: textContent.length
                };
              } else {
                pageSnapshot = {
                  url: afterUrl,
                  title,
                  note: "Full page text omitted (URL unchanged). Set full_read=true to force full output."
                };
              }
            }
            let fuzzyResults = [];
            if (typeof fuzzy_find === "string" && fuzzy_find.trim()) {
              const candidates = await browserSession.page.evaluate(() => {
                const dedup = /* @__PURE__ */ new Map();
                const nodes = document.querySelectorAll("a,button,input,textarea,select,[role='button'],[aria-label],h1,h2,h3,h4,h5,h6,p,span");
                const clean = (value) => value.replace(/\s+/g, " ").trim();
                const classSelector = (el) => {
                  const classes = Array.from(el.classList).slice(0, 2).map((c2) => c2.replace(/[^a-zA-Z0-9_-]/g, ""));
                  return classes.length > 0 ? `.${classes.join(".")}` : "";
                };
                const buildSelector = (el) => {
                  if (el.id) return `#${el.id}`;
                  const name = el.getAttribute("name");
                  if (name) return `${el.tagName.toLowerCase()}[name="${name.replace(/\\/g, "\\\\").replace(/"/g, '\\"')}"]`;
                  return `${el.tagName.toLowerCase()}${classSelector(el)}`;
                };
                for (const node of nodes) {
                  const element = node;
                  const text3 = clean(
                    element.innerText || element.value || element.getAttribute("aria-label") || ""
                  );
                  if (!text3) continue;
                  const selector = buildSelector(element);
                  const key = `${text3}||${selector}`;
                  if (!dedup.has(key)) {
                    dedup.set(key, { text: text3.substring(0, 200), selector });
                  }
                  if (dedup.size >= 400) break;
                }
                return Array.from(dedup.values());
              });
              const ranked = candidates.map((candidate) => ({
                ...candidate,
                score: Math.max(
                  rankFuzzyMatches(fuzzy_find, [candidate.text], 1)[0]?.score ?? 0,
                  rankFuzzyMatches(fuzzy_find, [candidate.selector], 1)[0]?.score ?? 0
                )
              })).sort((a, b) => b.score - a.score).slice(0, max_results);
              fuzzyResults = ranked.map((item) => ({
                text: item.text,
                selector: item.selector,
                score: item.score
              }));
            }
            return {
              success: true,
              session_active: true,
              actions_executed: actionLog,
              screenshot_saved: screenshotSaved,
              url_changed: urlChanged,
              url_change_notice: urlChanged ? `Url changed to -> [${afterUrl}]` : void 0,
              page: pageSnapshot,
              fuzzy_find_results: fuzzyResults
            };
          } catch (error) {
            return { error: `Browser session control failed: ${error instanceof Error ? error.message : String(error)}` };
          }
        }, allowBrowserControl, "browser_control")
      });
      tools.push(browserSessionControlTool);
      const browserSessionCloseTool = (0, import_sdk3.tool)({
        name: "browser_session_close",
        description: "Close the active persistent browser session.",
        parameters: {},
        implementation: createSafeToolImplementation(async () => {
          if (!browserSession) {
            return { success: true, session_active: false, message: "No active browser session." };
          }
          try {
            await browserSession.browser.close();
            browserSession = null;
            return { success: true, session_active: false, message: "Browser session closed." };
          } catch (error) {
            return { error: `Failed to close browser session: ${error instanceof Error ? error.message : String(error)}` };
          }
        }, allowBrowserControl, "browser_control")
      });
      tools.push(browserSessionCloseTool);
      const browserOpenPageTool = (0, import_sdk3.tool)({
        name: "browser_open_page",
        description: "Open a webpage in a headless browser (Puppeteer), render it once, and return content. One-shot only; do not use for multi-step navigation.",
        parameters: {
          url: import_zod2.z.string(),
          screenshot_path: import_zod2.z.string().optional().describe("Path to save a screenshot (e.g., 'screenshot.png')."),
          wait_for_selector: import_zod2.z.string().optional().describe("CSS selector to wait for before returning."),
          full_page_screenshot: import_zod2.z.boolean().optional().describe("If true, captures the full page when taking a screenshot."),
          actions: import_zod2.z.array(browserActionSchema).optional().describe("Optional scripted browser steps to run after navigation.")
        },
        implementation: createSafeToolImplementation(async ({ url, screenshot_path, wait_for_selector, full_page_screenshot, actions }) => {
          let browser;
          try {
            const puppeteer = await import("puppeteer");
            browser = await puppeteer.launch({
              headless: true,
              args: ["--no-sandbox", "--disable-setuid-sandbox"]
            });
            const page = await browser.newPage();
            try {
              await page.goto(url, { waitUntil: "networkidle0", timeout: 3e4 });
              if (wait_for_selector) {
                await page.waitForSelector(wait_for_selector, { timeout: 1e4 });
              }
              const beforeActionUrl = page.url();
              const action_log = await executeBrowserActions(page, actions || []);
              const currentUrl = page.url();
              const urlChanged = currentUrl !== beforeActionUrl;
              const title = await page.title();
              const textContent = await page.evaluate(() => document.body.innerText || "");
              let screenshot_saved = false;
              if (screenshot_path) {
                const screenshotFilePath = validatePath(currentWorkingDirectory, screenshot_path);
                await page.screenshot({ path: screenshotFilePath, fullPage: full_page_screenshot ?? false });
                screenshot_saved = true;
              }
              return {
                url: currentUrl,
                title,
                text_content: textContent.substring(0, 5e3),
                screenshot_saved,
                actions_executed: action_log,
                url_changed: urlChanged,
                url_change_notice: urlChanged ? `Url changed to -> [${currentUrl}]` : void 0
              };
            } finally {
              await browser.close();
            }
          } catch (error) {
            if (browser) {
              await browser.close().catch(() => {
              });
            }
            return { error: `Browser operation failed: ${error instanceof Error ? error.message : String(error)}` };
          }
        }, allowBrowserControl, "browser_control")
      });
      tools.push(browserOpenPageTool);
      const runTestCommandTool = (0, import_sdk3.tool)({
        name: "run_test_command",
        description: "Execute a test command (like 'npm test') and return the results. Specialized for capturing test output.",
        parameters: {
          command: import_zod2.z.string().describe("The test command to run (e.g., 'npm test', 'pytest').")
        },
        implementation: async ({ command }) => {
          return new Promise((resolve5) => {
            const parts = command.split(" ");
            const cmd = parts[0];
            const args = parts.slice(1);
            const child = (0, import_child_process3.spawn)(cmd, args, {
              cwd: currentWorkingDirectory,
              shell: true,
              env: { ...process.env, CI: "true" }
            });
            let stdout = "";
            let stderr = "";
            child.stdout.on("data", (data) => {
              stdout += data.toString();
            });
            child.stderr.on("data", (data) => {
              stderr += data.toString();
            });
            child.on("close", (code) => {
              resolve5({
                command,
                exit_code: code,
                stdout: stdout.trim(),
                stderr: stderr.trim(),
                passed: code === 0
              });
            });
            child.on("error", (err) => {
              resolve5({
                command,
                error: err.message,
                passed: false
              });
            });
          });
        }
      });
      tools.push(runTestCommandTool);
      const wikipediaSearchTool = (0, import_sdk3.tool)({
        name: "wikipedia_search",
        description: "Search Wikipedia for a given query and return page summaries.",
        parameters: {
          query: import_zod2.z.string(),
          lang: import_zod2.z.string().optional().describe("Language code (default: en)")
        },
        implementation: createSafeToolImplementation(
          async ({ query, lang = "en" }) => {
            try {
              const searchUrl = `https://${lang}.wikipedia.org/w/api.php?action=query&list=search&srsearch=${encodeURIComponent(query)}&format=json`;
              const searchResponse = await fetch(searchUrl);
              const searchData = await searchResponse.json();
              if (!searchData.query || !searchData.query.search || searchData.query.search.length === 0) {
                return { results: "No Wikipedia articles found." };
              }
              const results = [];
              for (const item of searchData.query.search.slice(0, 3)) {
                const pageUrl = `https://${lang}.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&explaintext&pageids=${item.pageid}&format=json`;
                const pageResponse = await fetch(pageUrl);
                const pageData = await pageResponse.json();
                const page = pageData.query.pages[item.pageid];
                results.push({
                  title: item.title,
                  summary: page.extract.substring(0, 2e3) + (page.extract.length > 2e3 ? "..." : ""),
                  url: `https://${lang}.wikipedia.org/wiki/${encodeURIComponent(item.title.replace(/ /g, "_"))}`
                });
              }
              return { results };
            } catch (error) {
              return { error: `Wikipedia search failed: ${error instanceof Error ? error.message : String(error)}` };
            }
          },
          enableWikipedia,
          "wikipedia_search"
        )
      });
      tools.push(wikipediaSearchTool);
      const ragLocalFilesTool = (0, import_sdk3.tool)({
        name: "rag_local_files",
        description: "Perform RAG (Retrieval-Augmented Generation) on files in the current workspace. Use this to find code snippets or information within local files relevant to a query.",
        parameters: {
          query: import_zod2.z.string(),
          path: import_zod2.z.string().optional().describe("Sub-directory to limit search (default: current working directory)"),
          file_pattern: import_zod2.z.string().optional().describe("File pattern to include (e.g. '.ts', 'src/'). Default: all text files.")
        },
        implementation: createSafeToolImplementation(
          async ({ query, path = ".", file_pattern = "" }) => {
            try {
              if (!client2) return { error: "LM Studio Client unavailable." };
              const targetDir = validatePath(currentWorkingDirectory, path);
              const entries = await (0, import_promises4.readdir)(targetDir, { recursive: true, withFileTypes: true });
              const textFiles = entries.filter((e) => e.isFile() && !e.name.match(/\.(png|jpg|jpeg|gif|ico|exe|dll|bin)$/i));
              const filteredFiles = file_pattern ? textFiles.filter((e) => e.name.includes(file_pattern) || (0, import_path8.join)(e.parentPath, e.name).includes(file_pattern)) : textFiles;
              const filesToScan = filteredFiles.slice(0, 50);
              let allChunks = [];
              const embeddingModel = await client2.embedding.model(embeddingModelName);
              const [queryEmbedding] = await embeddingModel.embed([query]);
              for (const file of filesToScan) {
                try {
                  const fullPath = (0, import_path8.join)(file.parentPath, file.name);
                  const content = await (0, import_promises4.readFile)(fullPath, "utf-8");
                  const chunks = content.split(/\n\s*\n/).filter((c2) => c2.trim().length > 20);
                  if (chunks.length === 0) continue;
                  const chunkEmbeddings = await embeddingModel.embed(chunks);
                  chunks.forEach((chunk, i) => {
                    const score = cosineSimilarity(queryEmbedding.embedding, chunkEmbeddings[i].embedding);
                    if (score > 0.4) {
                      allChunks.push({ chunk, score, file: file.name });
                    }
                  });
                } catch (e) {
                }
              }
              allChunks.sort((a, b) => b.score - a.score);
              return {
                query,
                results: allChunks.slice(0, 10).map((c2) => ({
                  file: c2.file,
                  score: c2.score.toFixed(3),
                  content: c2.chunk
                }))
              };
            } catch (error) {
              return { error: `Local RAG failed: ${error instanceof Error ? error.message : String(error)}` };
            }
          },
          enableLocalRag,
          "rag_local_files"
        )
      });
      tools.push(ragLocalFilesTool);
      const consultSecondaryAgentTool = (0, import_sdk3.tool)({
        name: "consult_secondary_agent",
        description: "Delegate a task to a secondary agent. IMPORTANT: If the task is 'coding' or 'writing files', the secondary agent will AUTOMATICALLY CREATE AND SAVE the files to the disk. You do NOT need to save them yourself. The tool returns a list of generated files. Trust this list.",
        parameters: {
          task: import_zod2.z.string(),
          agent_role: import_zod2.z.string().optional().describe("Key from 'Sub-Agent Profiles' config (e.g., 'coder'). Default: 'general'."),
          context: import_zod2.z.string().optional().describe("Additional context or data for the agent."),
          allow_tools: import_zod2.z.boolean().optional().describe("If true, the secondary agent can use tools like Web Search (DuckDuckGo, Wikipedia), File System (Read/List), and Code Execution (if enabled in settings). Default: false.")
        },
        implementation: createSafeToolImplementation(
          async ({ task, agent_role = "general", context = "", allow_tools = false }) => {
            let endpoint = pluginConfig.get("secondaryAgentEndpoint");
            let modelId = pluginConfig.get("secondaryModelId");
            const useMainModel = pluginConfig.get("useMainModelForSubAgent");
            let handoffMessage = void 0;
            let finalResponse = "";
            if (useMainModel) {
              endpoint = "http://localhost:1234/v1";
              modelId = "local-model";
            }
            const subAgentProfilesStr = pluginConfig.get("subAgentProfiles");
            const debugMode = pluginConfig.get("enableDebugMode");
            const subAgentDebugLogging = pluginConfig.get("enableSubAgentDebugLogging");
            const autoSave = pluginConfig.get("subAgentAutoSave");
            const showFullCode = pluginConfig.get("showFullCodeOutput");
            const allowFileSystem = pluginConfig.get("subAgentAllowFileSystem");
            const allowWeb = pluginConfig.get("subAgentAllowWeb");
            const allowCode = pluginConfig.get("subAgentAllowCode");
            const allowSubAgentBrowserControl = pluginConfig.get("subAgentAllowBrowserControl");
            if (!enableSecondary) return { error: "Secondary agent is disabled in settings." };
            const runAgentLoop = async (role, taskPrompt, contextData, loopLimit = 8, forceTools = false, currentWorkingDirectory2) => {
              let currentSystemPrompt = "You are a helpful assistant.";
              const instructionsPath = (0, import_path8.join)(currentWorkingDirectory2, "SUB_AGENT_INSTRUCTIONS.md");
              try {
                const instructions = await (0, import_promises4.readFile)(instructionsPath, "utf-8");
                if (instructions.trim()) currentSystemPrompt = instructions;
              } catch (e) {
              }
              const infoPath = (0, import_path8.join)(currentWorkingDirectory2, "beledarian_info.md");
              try {
                const projectInfo = await (0, import_promises4.readFile)(infoPath, "utf-8");
                if (projectInfo.trim()) {
                  currentSystemPrompt += `

## ? Current Project Info (beledarian_info.md)
${projectInfo}
`;
                }
              } catch (e) {
              }
              currentSystemPrompt += `

## ? Current Workspace
Your current working directory is: 

${currentWorkingDirectory2}
Always assume relative paths are from this directory.`;
              try {
                const profiles = JSON.parse(subAgentProfilesStr);
                if (profiles[role]) {
                  currentSystemPrompt += `

## Your Persona
${profiles[role]}`;
                } else if (role === "reviewer") {
                  currentSystemPrompt += `

## Your Persona
You are a Senior Code Reviewer. Your job is to analyze code, find bugs, security issues, or logic errors, and FIX them.

IMPORTANT: To fix a file, you MUST use the 'save_file' tool with the complete, corrected content. DO NOT use 'container.exec' or diff formats. Just overwrite the file with the fixed version using 'save_file'.`;
                }
              } catch (jsonErr) {
              }
              let toolsReminder = "";
              const toolsEnabled = allow_tools || forceTools;
              if (toolsEnabled) {
                const allowedTools = [];
                if (allowFileSystem) allowedTools.push("read_file", "list_directory", "save_file", "replace_text_in_file", "delete_files_by_pattern", "rag_local_files", "fuzzy_find_local_files", "search_file_content");
                if (allowWeb) allowedTools.push("wikipedia_search", "web_search", "duckduckgo_search", "fetch_web_content", "rag_web_content");
                if (allowWeb && allowSubAgentBrowserControl && allowBrowserControl) allowedTools.push("browser_session_open", "browser_session_control", "browser_session_close");
                if (allowCode) allowedTools.push("run_python", "run_javascript");
                if (allowedTools.length > 0) {
                  const toolsList = allowedTools.join(", ");
                  currentSystemPrompt += `

## Allowed Tools
You have access to the following tools via JSON output: ${toolsList}.
Refer to the "Tool Usage" section above for the JSON format.
`;
                  toolsReminder = `

[SYSTEM REMINDER: You have access to tools: ${toolsList}. If you need information you don't have, USE A TOOL. Do not refuse. Format tool calls exactly as: {"tool": "tool_name", "args": {"arg_name": "value"}}]`;
                }
                if (allowWeb && allowSubAgentBrowserControl && allowBrowserControl) {
                  currentSystemPrompt += `

## Browser Navigation Rule
For multi-step browsing/navigation, you MUST use browser_session_open -> browser_session_control -> browser_session_close.
Use browser_open_page only for one-shot page reads.`;
                }
              }
              currentSystemPrompt += `

## Optional Handoff Message
If you want the main agent to relay your findings, include either:
1) [HANDOFF_MESSAGE]...[/HANDOFF_MESSAGE]
OR
2) JSON with a \`handoff_message\` field (optionally with \`response\` or \`final_response\`).`;
              currentSystemPrompt += `

## Task Completion & Early Exit
If you have successfully completed your task, output 'TASK_COMPLETED'.
If you cannot complete the task (e.g., due to system limitations, missing files, or inaccessible paths), output 'TASK_FAILED' to abort early.`;
              const msgList = [
                { role: "system", content: currentSystemPrompt },
                { role: "user", content: `Task: ${taskPrompt}

Context: ${contextData}${toolsReminder}` }
              ];
              let loops = 0;
              let noToolCallCount = 0;
              let executedToolCallCount = 0;
              let finalContent = "";
              let filesModified = [];
              let handoffMessage2 = "";
              const maxSubAgentToolOutputChars = 3e4;
              const suggestedReadPath = allowFileSystem ? extractLikelyFilePath(`${taskPrompt}
${contextData}`) : null;
              while (loops < loopLimit) {
                try {
                  const response = await fetch(`${endpoint}/chat/completions`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                      model: modelId,
                      messages: msgList,
                      temperature: 0.7,
                      stream: false
                    })
                  });
                  if (!response.ok) {
                    const errorBody = await response.text().catch(() => "");
                    const compactErrorBody = errorBody.replace(/\s+/g, " ").trim().substring(0, 600);
                    if (subAgentDebugLogging) {
                      console.log(`[Sub-Agent] API error status=${response.status} body=${compactErrorBody}`);
                    }
                    const details = compactErrorBody ? ` - ${compactErrorBody}` : "";
                    return { error: `API Error: ${response.status}${details}`, filesModified };
                  }
                  const data = await response.json();
                  const message = data?.choices?.[0]?.message;
                  const parsedMessage = parseSubAgentResponseMessage(message);
                  const content = parsedMessage.content;
                  let toolCall = parsedMessage.toolCall;
                  if (subAgentDebugLogging) {
                    const rawContent = (typeof message === "string" ? message : JSON.stringify(message)) ?? "";
                    console.log(`[Sub-Agent] RAW content received: ${rawContent.substring(0, 1e3)}...`);
                    const preview = content.substring(0, 200);
                    console.log(`[Sub-Agent] Parse result source=${parsedMessage.toolCallSource} hasToolCall=${Boolean(toolCall)} preview=${preview}`);
                  }
                  finalContent = content;
                  if (!toolsEnabled) {
                    const extracted = extractHandoffMessage(content);
                    const looksLikePureToolCall = extracted.response.trimStart().startsWith("{") && parsedMessage.toolCall !== null && extracted.response.trim().length < 500;
                    const safeResponse = looksLikePureToolCall ? "[Sub-agent did not produce a prose response. It attempted a tool call but tools are disabled for this invocation.]" : extracted.response;
                    return { response: safeResponse, filesModified, handoff_message: extracted.handoffMessage };
                  }
                  const trimmed = content.trim();
                  if (!toolCall && trimmed) {
                    const refusalKeywords = [
                      "i cannot browse",
                      "i don't have access",
                      "i can't access",
                      "unable to browse",
                      "real-time news",
                      "no internet access",
                      "as an ai",
                      "i do not have the ability",
                      "cannot access the internet"
                    ];
                    if (refusalKeywords.some((kw) => trimmed.toLowerCase().includes(kw))) {
                      msgList.push({ role: "assistant", content });
                      msgList.push({ role: "system", content: "SYSTEM ERROR: You HAVE access to tools. USE THEM." });
                      loops++;
                      continue;
                    }
                  }
                  if (toolCall && toolCall.tool) {
                    noToolCallCount = 0;
                    executedToolCallCount++;
                    msgList.push({ role: "assistant", content });
                    let toolResult = "";
                    let toolValidationError = null;
                    const validateRequiredParams = (toolName, requiredParams, providedArgs = {}) => {
                      const missing = requiredParams.filter((p) => !(p in providedArgs));
                      if (missing.length > 0) {
                        const availableKeys = Object.keys(providedArgs).join(", ") || "none";
                        return `Tool '${toolName}' requires parameters: [${requiredParams.join(", ")}]. Missing: [${missing.join(", ")}]. Provided keys: ${availableKeys}.`;
                      }
                      return null;
                    };
                    try {
                      const args = toolCall.args || {};
                      toolValidationError = validateToolCall(toolCall.tool, args);
                      if (toolValidationError) {
                        toolResult = `TOOL_VALIDATION_ERROR: ${toolValidationError}`;
                      } else {
                        if (allowFileSystem) {
                          if (toolCall.tool === "read_file" && toolCall.args?.file_name) {
                            const fpath = validatePath(currentWorkingDirectory2, toolCall.args.file_name);
                            const readContent = await (0, import_promises4.readFile)(fpath, "utf-8");
                            toolResult = readContent.length > maxSubAgentToolOutputChars ? `${readContent.substring(0, maxSubAgentToolOutputChars)}
... (truncated ${readContent.length - maxSubAgentToolOutputChars} chars)` : readContent;
                          } else if (toolCall.tool === "list_directory") {
                            const files = await (0, import_promises4.readdir)(currentWorkingDirectory2);
                            toolResult = JSON.stringify(files);
                          } else if (toolCall.tool === "save_file") {
                            if (Array.isArray(toolCall.args?.files)) {
                              const savedList = [];
                              for (const fileObj of toolCall.args.files) {
                                const fName = fileObj.file_name || fileObj.name || fileObj.path;
                                const fContent = fileObj.content || fileObj.data;
                                if (fName && fContent) {
                                  try {
                                    const fpath = validatePath(currentWorkingDirectory2, fName);
                                    await (0, import_promises4.mkdir)((0, import_path8.dirname)(fpath), { recursive: true });
                                    await (0, import_promises4.writeFile)(fpath, fContent, "utf-8");
                                    filesModified.push(fName);
                                    savedList.push(fName);
                                  } catch (err) {
                                  }
                                }
                              }
                              toolResult = savedList.length > 0 ? `Success: Saved ${savedList.length} files: ${savedList.join(", ")}` : "Error: No valid files found in batch.";
                            } else {
                              const fileName = toolCall.args?.file_name || toolCall.args?.name || toolCall.args?.path;
                              const content2 = toolCall.args?.content || toolCall.args?.data;
                              if (fileName && content2) {
                                const fpath = validatePath(currentWorkingDirectory2, fileName);
                                await (0, import_promises4.mkdir)((0, import_path8.dirname)(fpath), { recursive: true });
                                await (0, import_promises4.writeFile)(fpath, content2, "utf-8");
                                toolResult = `Success: File saved to ${fpath}`;
                                filesModified.push(fileName);
                              } else {
                                toolResult = "Error: Missing 'file_name' (or 'name', 'path') or 'content' (or 'data') arguments.";
                              }
                            }
                          } else if (toolCall.tool === "replace_text_in_file" && toolCall.args?.file_name && toolCall.args?.old_string && toolCall.args?.new_string) {
                            const fpath = validatePath(currentWorkingDirectory2, toolCall.args.file_name);
                            const content2 = await (0, import_promises4.readFile)(fpath, "utf-8");
                            if (!content2.includes(toolCall.args.old_string)) {
                              toolResult = "Error: 'old_string' not found exactly.";
                            } else {
                              const count = content2.split(toolCall.args.old_string).length - 1;
                              if (count > 1) {
                                toolResult = `Error: Found ${count} occurrences. Be more specific.`;
                              } else {
                                await (0, import_promises4.writeFile)(fpath, content2.replace(toolCall.args.old_string, toolCall.args.new_string), "utf-8");
                                toolResult = "Success: Text replaced.";
                                filesModified.push(toolCall.args.file_name);
                              }
                            }
                          } else if (toolCall.tool === "delete_files_by_pattern" && toolCall.args?.pattern) {
                            if (toolCall.args.pattern.length > 100) throw new Error("Pattern too complex");
                            const regex = new RegExp(toolCall.args.pattern);
                            const start = Date.now();
                            regex.test("safe_test_string_for_redos_check_1234567890_safe_test_string_for_redos_check_1234567890");
                            if (Date.now() - start > 100) throw new Error("Pattern too complex/slow");
                            const files = await (0, import_promises4.readdir)(currentWorkingDirectory2);
                            const deleted = [];
                            for (const file of files) {
                              if (regex.test(file)) {
                                const fpath = validatePath(currentWorkingDirectory2, file);
                                await (0, import_promises4.rm)(fpath, { force: true });
                                deleted.push(file);
                              }
                            }
                            toolResult = `Deleted ${deleted.length} files: ${deleted.join(", ")}`;
                          } else if (toolCall.tool === "rag_local_files") {
                            toolResult = "Local RAG available (mocked for refactor).";
                          } else if (toolCall.tool === "fuzzy_find_local_files" && toolCall.args?.query) {
                            const targetDir = validatePath(currentWorkingDirectory2, toolCall.args?.path || ".");
                            const maxResults = Math.min(Math.max(Number(toolCall.args?.max_results ?? 5), 1), 20);
                            const entries = await (0, import_promises4.readdir)(targetDir, { recursive: true, withFileTypes: true });
                            const files = entries.filter((entry) => entry.isFile()).map((entry) => (0, import_path8.relative)(targetDir, (0, import_path8.join)(entry.path, entry.name)).replace(/\\/g, "/"));
                            const ranked = rankFuzzyMatches(toolCall.args.query, files, maxResults);
                            toolResult = JSON.stringify(ranked.map((item) => ({ path: item.value, score: item.score })));
                          }
                        }
                        if (allowWeb && !toolResult) {
                          if (toolCall.tool === "wikipedia_search") toolResult = "Wiki Search (mocked)";
                          else if (toolCall.tool === "web_search" || toolCall.tool === "duckduckgo_search") {
                            const { search, SafeSearchType } = await import("duck-duck-scrape");
                            const r = await search(toolCall.args.query, { safeSearch: SafeSearchType.OFF });
                            toolResult = JSON.stringify(r.results.slice(0, 3));
                          } else if (toolCall.tool === "fetch_web_content" && toolCall.args?.url) {
                            const res = await fetch(toolCall.args.url);
                            toolResult = (await res.text()).substring(0, 5e3);
                          } else if (allowSubAgentBrowserControl && allowBrowserControl && toolCall.tool === "browser_session_open" && toolCall.args?.url) {
                            if (browserSession) {
                              await browserSession.browser.close().catch(() => {
                              });
                              browserSession = null;
                            }
                            const puppeteer = await import("puppeteer");
                            const browser = await puppeteer.launch({
                              headless: true,
                              args: ["--no-sandbox", "--disable-setuid-sandbox"]
                            });
                            const page = await browser.newPage();
                            await page.goto(toolCall.args.url, { waitUntil: "networkidle0", timeout: 3e4 });
                            if (toolCall.args.wait_for_selector) {
                              await page.waitForSelector(toolCall.args.wait_for_selector, { timeout: 15e3 });
                            }
                            browserSession = { browser, page, currentUrl: page.url() };
                            const includePageText = toolCall.args.include_page_text !== false;
                            const pageText = includePageText ? await page.evaluate(() => document.body.innerText || "") : void 0;
                            toolResult = JSON.stringify({
                              session_active: true,
                              url: page.url(),
                              title: await page.title(),
                              text_content: pageText,
                              text_length: pageText ? pageText.length : 0
                            });
                          } else if (allowSubAgentBrowserControl && allowBrowserControl && toolCall.tool === "browser_session_control") {
                            if (!browserSession) {
                              toolResult = "Error: No active browser session.";
                            } else {
                              const beforeUrl = browserSession.page.url();
                              const actionLog = await executeBrowserActions(browserSession.page, toolCall.args?.actions || []);
                              const afterUrl = browserSession.page.url();
                              const urlChanged = beforeUrl !== afterUrl;
                              browserSession.currentUrl = afterUrl;
                              let fuzzyResults = [];
                              if (toolCall.args?.fuzzy_find) {
                                const maxResults = Math.min(Math.max(Number(toolCall.args?.max_results ?? 5), 1), 20);
                                const candidates = await browserSession.page.evaluate(() => {
                                  const dedup = /* @__PURE__ */ new Map();
                                  const nodes = document.querySelectorAll("a,button,input,textarea,select,[role='button'],[aria-label],h1,h2,h3,h4,h5,h6,p,span");
                                  const clean = (value) => value.replace(/\s+/g, " ").trim();
                                  const classSelector = (el) => {
                                    const classes = Array.from(el.classList).slice(0, 2).map((c2) => c2.replace(/[^a-zA-Z0-9_-]/g, ""));
                                    return classes.length > 0 ? `.${classes.join(".")}` : "";
                                  };
                                  const buildSelector = (el) => {
                                    if (el.id) return `#${el.id}`;
                                    const name = el.getAttribute("name");
                                    if (name) return `${el.tagName.toLowerCase()}[name="${CSS.escape(name)}"]`;
                                    return `${el.tagName.toLowerCase()}${classSelector(el)}`;
                                  };
                                  for (const node of nodes) {
                                    const element = node;
                                    const text3 = clean(
                                      element.innerText || element.value || element.getAttribute("aria-label") || ""
                                    );
                                    if (!text3) continue;
                                    const selector = buildSelector(element);
                                    const key = `${text3}||${selector}`;
                                    if (!dedup.has(key)) dedup.set(key, { text: text3.substring(0, 200), selector });
                                    if (dedup.size >= 400) break;
                                  }
                                  return Array.from(dedup.values());
                                });
                                fuzzyResults = candidates.map((candidate) => ({
                                  ...candidate,
                                  score: Math.max(
                                    rankFuzzyMatches(toolCall.args.fuzzy_find, [candidate.text], 1)[0]?.score ?? 0,
                                    rankFuzzyMatches(toolCall.args.fuzzy_find, [candidate.selector], 1)[0]?.score ?? 0
                                  )
                                })).sort((a, b) => b.score - a.score).slice(0, maxResults);
                              }
                              const output = {
                                session_active: true,
                                actions_executed: actionLog,
                                url: afterUrl,
                                url_changed: urlChanged,
                                url_change_notice: urlChanged ? `Url changed to -> [${afterUrl}]` : void 0,
                                fuzzy_find_results: fuzzyResults
                              };
                              if (toolCall.args?.read_page !== false) {
                                const fullRead = toolCall.args?.full_read === true;
                                output.title = await browserSession.page.title();
                                if (urlChanged || fullRead) {
                                  const textContent = await browserSession.page.evaluate(() => document.body.innerText || "");
                                  output.text_content = textContent;
                                  output.text_length = textContent.length;
                                } else {
                                  output.note = "Full page text omitted (URL unchanged). Set full_read=true to force full output.";
                                }
                              }
                              if (toolCall.args?.screenshot_path) {
                                const screenshotFilePath = validatePath(currentWorkingDirectory2, toolCall.args.screenshot_path);
                                await browserSession.page.screenshot({ path: screenshotFilePath, fullPage: !!toolCall.args?.full_page_screenshot });
                                output.screenshot_saved = true;
                              }
                              toolResult = JSON.stringify(output);
                            }
                          } else if (allowSubAgentBrowserControl && allowBrowserControl && toolCall.tool === "browser_session_close") {
                            if (browserSession) {
                              await browserSession.browser.close().catch(() => {
                              });
                              browserSession = null;
                            }
                            toolResult = JSON.stringify({ session_active: false, message: "Browser session closed." });
                          }
                        }
                        if (allowCode && !toolResult) {
                          if (toolCall.tool === "run_python") {
                            const res = await originalRunPythonImplementation({ python: toolCall.args.python });
                            toolResult = res.stderr ? `Error: ${res.stderr}` : res.stdout;
                          }
                        }
                        if (!toolResult) toolResult = "Error: Tool not found/allowed.";
                      }
                    } catch (err) {
                      toolResult = `Error: ${err.message}`;
                    }
                    msgList.push({ role: "user", content: `Tool Output: ${toolResult}` });
                    loops++;
                  } else {
                    const shouldAutoFallbackRead = toolsEnabled && allowFileSystem && executedToolCallCount === 0 && noToolCallCount === 0 && typeof suggestedReadPath === "string" && suggestedReadPath.length > 0;
                    if (shouldAutoFallbackRead) {
                      try {
                        const autoReadPath = validatePath(currentWorkingDirectory2, suggestedReadPath);
                        const autoReadStats = await (0, import_promises4.stat)(autoReadPath);
                        if (!autoReadStats.isFile()) {
                          throw new Error(`Not a file: ${autoReadPath}`);
                        }
                        const autoReadContent = await (0, import_promises4.readFile)(autoReadPath, "utf-8");
                        const boundedContent = autoReadContent.length > 3e4 ? `${autoReadContent.substring(0, 3e4)}
... (truncated)` : autoReadContent;
                        if (trimmed.length > 0) {
                          msgList.push({ role: "assistant", content });
                        }
                        msgList.push({
                          role: "user",
                          content: `Tool Output: AUTO_FALLBACK read_file(${suggestedReadPath})
${boundedContent}`
                        });
                        executedToolCallCount++;
                        loops++;
                        continue;
                      } catch (error) {
                        if (subAgentDebugLogging) {
                          console.log(`[Sub-Agent] Auto fallback read_file failed: ${error instanceof Error ? error.message : String(error)}`);
                        }
                        try {
                          const autoFiles = await (0, import_promises4.readdir)(currentWorkingDirectory2);
                          const limitedFiles = autoFiles.slice(0, 200);
                          if (trimmed.length > 0) {
                            msgList.push({ role: "assistant", content });
                          }
                          msgList.push({
                            role: "user",
                            content: `Tool Output: AUTO_FALLBACK list_directory(.)
${JSON.stringify(limitedFiles)}`
                          });
                          executedToolCallCount++;
                          loops++;
                          continue;
                        } catch {
                        }
                      }
                    }
                    const planningLikeText = /(?:\bI(?:'ll| will)\b|\blet me\b|\bnext\b|\bfirst\b)/i.test(trimmed);
                    const shouldTreatAsFinalResponse = trimmed.length >= 120 && !planningLikeText;
                    noToolCallCount++;
                    if (content.includes("TASK_COMPLETED") || content.includes("TASK_FAILED") || shouldTreatAsFinalResponse || noToolCallCount >= 3 || loops >= loopLimit - 1) {
                      break;
                    }
                    if (content.trim().length > 0) {
                      msgList.push({ role: "assistant", content });
                    }
                    let reminder = "SYSTEM NOTICE: You did not call a tool. If you are finished, output 'TASK_COMPLETED'. If you cannot complete the task, output 'TASK_FAILED'. If not, USE A TOOL now and return a single JSON tool-call object only (no prose).";
                    if (toolsEnabled) {
                      if (allowFileSystem && suggestedReadPath && noToolCallCount <= 3) {
                        const escapedPath = suggestedReadPath.replace(/\\/g, "\\\\").replace(/"/g, '\\"');
                        reminder += `
Suggested next step: {"tool":"read_file","args":{"file_name":"${escapedPath}"}}`;
                      } else if (allowFileSystem && noToolCallCount <= 3) {
                        reminder += `
Suggested next step: {"tool":"list_directory","args":{}}`;
                      }
                    }
                    msgList.push({ role: "system", content: reminder });
                    loops++;
                  }
                } catch (err) {
                  return { error: err.message, filesModified };
                }
                if (msgList.length > 20) {
                  const systemMsg = msgList[0];
                  const recentMsgs = msgList.slice(-18);
                  msgList.length = 0;
                  msgList.push(systemMsg, ...recentMsgs);
                }
              }
              if (finalContent) {
                const extracted = extractHandoffMessage(finalContent);
                finalContent = extracted.response;
                handoffMessage2 = extracted.handoffMessage || "";
              }
              if (autoSave && allowFileSystem && finalContent) {
                const codeBlockRegex = /```\s*(\w+)?\s*([\s\S]*?)```/g;
                const matches = Array.from(finalContent.matchAll(codeBlockRegex));
                const processedFiles = /* @__PURE__ */ new Set();
                for (let i = matches.length - 1; i >= 0; i--) {
                  const match = matches[i];
                  const fullBlock = match[0];
                  const lang = (match[1] || "txt").toLowerCase();
                  const code = match[2];
                  const index = match.index || 0;
                  let handledAsBatch = false;
                  if (lang === "json") {
                    try {
                      const parsed = JSON.parse(code);
                      if (Array.isArray(parsed)) {
                        let extractedCount = 0;
                        for (const item of parsed) {
                          const fName = item.path || item.file_name || item.name;
                          const fContent = item.content || item.data || item.code;
                          if (fName && typeof fName === "string" && fContent && typeof fContent === "string") {
                            const fpath = validatePath(currentWorkingDirectory2, fName);
                            await (0, import_promises4.mkdir)((0, import_path8.dirname)(fpath), { recursive: true });
                            await (0, import_promises4.writeFile)(fpath, fContent, "utf-8");
                            filesModified.push(fName);
                            processedFiles.add(fName);
                            extractedCount++;
                          }
                        }
                        if (extractedCount > 0) {
                          handledAsBatch = true;
                          const replacement = `
[System: Successfully extracted and saved ${extractedCount} files from JSON block.]
`;
                          finalContent = finalContent.slice(0, index) + replacement + finalContent.slice(index + fullBlock.length);
                        }
                      }
                    } catch (e) {
                    }
                  }
                  if (!handledAsBatch && code.trim().length > 50) {
                    const lookback = finalContent.substring(Math.max(0, index - 500), index);
                    const nameMatch = lookback.match(/(?:`|\*\*|###|filename:|file:)[\s\S]*?([\w\-\/\\.]+\.(?:tsx|ts|jsx|js|html|css|json|md|py|sh|java|rs|go|sql|yaml|yml|c|cpp|h|hpp|txt))/i);
                    let fileName = "";
                    if (nameMatch) {
                      fileName = nameMatch[1].trim();
                    }
                    if (!fileName) {
                      const firstLine = code.split("\n")[0].trim();
                      const commentMatch = firstLine.match(/^(?:\/\/|#|<!--|;)\s*(?:filename:|file:)?\s*([\w\-\/\\.]+\.(?:tsx|ts|jsx|js|html|css|json|md|py|sh|java|rs|go|sql|yaml|yml|c|cpp|h|hpp|txt))/i);
                      if (commentMatch) {
                        fileName = commentMatch[1].trim();
                      }
                    }
                    const isShell = ["bash", "sh", "cmd", "powershell", "console", "zsh", "terminal"].includes(lang);
                    if (isShell && !fileName) {
                      continue;
                    }
                    if (!fileName) {
                      continue;
                    }
                    if (processedFiles.has(fileName)) {
                      continue;
                    }
                    const fpath = (0, import_path8.join)(currentWorkingDirectory2, fileName);
                    try {
                      await (0, import_promises4.mkdir)((0, import_path8.dirname)(fpath), { recursive: true });
                      await (0, import_promises4.writeFile)(fpath, code, "utf-8");
                      filesModified.push(fileName);
                      processedFiles.add(fileName);
                      const replacement = `
[System: File '${fileName}' created successfully.]
`;
                      finalContent = finalContent.slice(0, index) + replacement + finalContent.slice(index + fullBlock.length);
                    } catch (e) {
                      console.error(`Failed to auto-save file ${fileName}:`, e);
                    }
                  }
                }
              }
              if (filesModified.length > 0 && allowFileSystem) {
                const infoPath2 = (0, import_path8.join)(currentWorkingDirectory2, "beledarian_info.md");
                const timestamp = (/* @__PURE__ */ new Date()).toISOString();
                const logEntry = `
- **[${timestamp}]** Task: "${taskPrompt.substring(0, 50)}..." | Modified: ${filesModified.join(", ")}`;
                try {
                  await (0, import_promises4.appendFile)(infoPath2, logEntry, "utf-8");
                } catch (e) {
                  try {
                    await (0, import_promises4.writeFile)(infoPath2, `# Project History
${logEntry}`, "utf-8");
                  } catch (e2) {
                  }
                }
              }
              return { response: finalContent, filesModified, handoff_message: handoffMessage2 || void 0 };
            };
            const primaryResult = await runAgentLoop(agent_role, task, context, 8, false, currentWorkingDirectory);
            if (primaryResult.error) return { error: primaryResult.error };
            finalResponse = primaryResult.response || "";
            handoffMessage = primaryResult.handoff_message;
            const generatedFiles = [...primaryResult.filesModified];
            if (debugMode && primaryResult.filesModified.length > 0) {
              const filesToCheck = primaryResult.filesModified.join(", ");
              const debugTask = `Review the code in these files: ${filesToCheck}. Check for bugs, syntax errors, or logic flaws. If you find any, use 'save_file' to FIX them. If they are correct, confirm it.`;
              let debugContext = "Here is the content of the created files:\n";
              for (const f of primaryResult.filesModified) {
                try {
                  const c2 = await (0, import_promises4.readFile)((0, import_path8.join)(currentWorkingDirectory, f), "utf-8");
                  debugContext += `
--- ${f} ---
${c2}
`;
                } catch (e) {
                }
              }
              const debugResult = await runAgentLoop("reviewer", debugTask, debugContext, 5, true, currentWorkingDirectory);
              finalResponse += "\n\n--- Auto-Debug Report ---\n" + (debugResult.response || "Debug pass completed.");
              if (debugResult.filesModified.length > 0) {
                finalResponse += `
(The reviewer fixed these files: ${debugResult.filesModified.join(", ")})`;
              }
              if (!handoffMessage && debugResult.handoff_message) {
                handoffMessage = debugResult.handoff_message;
              }
            }
            if (primaryResult.filesModified.length > 0) {
              const fullPaths = primaryResult.filesModified.map((f) => {
                if ((0, import_path8.isAbsolute)(f)) return f;
                return (0, import_path8.join)(currentWorkingDirectory, f);
              });
              finalResponse += `

[GENERATED_FILES]: ${fullPaths.join(", ")}`;
              if (showFullCode) {
                finalResponse += `

### Generated Code Content:
`;
                for (const f of primaryResult.filesModified) {
                  try {
                    const fpath = (0, import_path8.isAbsolute)(f) ? f : (0, import_path8.join)(currentWorkingDirectory, f);
                    const content = await (0, import_promises4.readFile)(fpath, "utf-8");
                    const ext = f.split(".").pop() || "txt";
                    finalResponse += `
**${f}**
\`\`\`${ext}
${content}
\`\`\`
`;
                  } catch (e) {
                  }
                }
              }
            }
            if (!showFullCode && primaryResult.filesModified.length > 0) {
              finalResponse = finalResponse.replace(/```[\s\S]*?```/g, "\n[System: Code Block Hidden for Brevity. The code has been handled/saved by the sub-agent. Do NOT request it again. Proceed.]\n");
            }
            return { response: finalResponse, generated_files: generatedFiles, handoff_message: handoffMessage };
          },
          enableSecondary,
          "consult_secondary_agent"
        )
      });
      tools.push(consultSecondaryAgentTool);
      const insertAtLineTool = (0, import_sdk3.tool)({
        name: "insert_at_line",
        description: import_sdk3.text`
      Insert content at a specific line number in a file. 
      The line_number is 1-indexed (line 1 is the first line).
      Existing content at that line and below will be pushed down.
    `,
        parameters: {
          file_name: import_zod2.z.string(),
          line_number: import_zod2.z.number().int().min(1).describe("The line number to insert at (1-indexed)"),
          content_to_insert: import_zod2.z.string().describe("The text content to insert at the specified line")
        },
        implementation: async ({ file_name, line_number, content_to_insert }) => {
          try {
            const filePath = validatePath(currentWorkingDirectory, file_name);
            let content = "";
            try {
              content = await (0, import_promises4.readFile)(filePath, "utf-8");
            } catch {
              if (line_number !== 1) {
                return { error: `File '${file_name}' does not exist. Can only insert at line 1 in a new file.` };
              }
            }
            const lines = content.split("\n");
            const insertIndex = Math.min(line_number - 1, lines.length);
            lines.splice(insertIndex, 0, content_to_insert);
            await (0, import_promises4.writeFile)(filePath, lines.join("\n"), "utf-8");
            return {
              success: true,
              message: `Inserted ${content_to_insert.split("\n").length} line(s) at line ${line_number} in ${file_name}`,
              new_line_count: lines.length
            };
          } catch (e) {
            return { error: `Failed to insert text: ${e instanceof Error ? e.message : String(e)}` };
          }
        }
      });
      tools.push(insertAtLineTool);
      const appendFileTool = (0, import_sdk3.tool)({
        name: "append_file",
        description: import_sdk3.text`
      Append content to the end of a file. 
      If the file doesn't exist, it will be created.
      Useful for adding logs, entries, or building files incrementally.
    `,
        parameters: {
          file_name: import_zod2.z.string(),
          content: import_zod2.z.string().describe("The text content to append to the file")
        },
        implementation: async ({ file_name, content }) => {
          try {
            const filePath = validatePath(currentWorkingDirectory, file_name);
            await (0, import_promises4.mkdir)((0, import_path8.dirname)(filePath), { recursive: true });
            await (0, import_promises4.appendFile)(filePath, content, "utf-8");
            return {
              success: true,
              message: `Content appended to ${file_name}`
            };
          } catch (e) {
            return { error: `Failed to append to file: ${e instanceof Error ? e.message : String(e)}` };
          }
        }
      });
      tools.push(appendFileTool);
      const readFileRangeTool = (0, import_sdk3.tool)({
        name: "read_file_range",
        description: import_sdk3.text`
      Read a specific range of lines from a file. 
      Returns the content with line numbers for easy reference.
      Line numbers are 1-indexed (line 1 is the first line).
    `,
        parameters: {
          file_name: import_zod2.z.string(),
          start_line: import_zod2.z.number().int().min(1).describe("Starting line number (1-indexed)"),
          end_line: import_zod2.z.number().int().min(1).describe("Ending line number (1-indexed, inclusive)")
        },
        implementation: async ({ file_name, start_line, end_line }) => {
          try {
            const filePath = validatePath(currentWorkingDirectory, file_name);
            const content = await (0, import_promises4.readFile)(filePath, "utf-8");
            const lines = content.split("\n");
            if (start_line > lines.length) {
              return { error: `Start line ${start_line} is beyond the end of the file (${lines.length} lines)` };
            }
            const actualEndLine = Math.min(end_line, lines.length);
            const selectedLines = lines.slice(start_line - 1, actualEndLine);
            const numberedContent = selectedLines.map(
              (line, idx) => `${start_line + idx}: ${line}`
            ).join("\n");
            return {
              file_name,
              start_line,
              end_line: actualEndLine,
              line_count: selectedLines.length,
              content_with_line_numbers: numberedContent
            };
          } catch (e) {
            return { error: `Failed to read file range: ${e instanceof Error ? e.message : String(e)}` };
          }
        }
      });
      tools.push(readFileRangeTool);
      const searchInFileTool = (0, import_sdk3.tool)({
        name: "search_in_file",
        description: import_sdk3.text`
      Search for a pattern within a single file (grep-like functionality).
      Returns matching lines with their line numbers.
      The pattern can be a simple substring or a regex pattern.
    `,
        parameters: {
          file_name: import_zod2.z.string(),
          pattern: import_zod2.z.string().describe("Search pattern (substring or regex)"),
          case_sensitive: import_zod2.z.boolean().optional().default(false).describe("Whether the search is case-sensitive (default: false)"),
          use_regex: import_zod2.z.boolean().optional().default(false).describe("Whether to treat pattern as a regex (default: false, treats as literal substring)")
        },
        implementation: async ({ file_name, pattern, case_sensitive = false, use_regex = false }) => {
          try {
            const filePath = validatePath(currentWorkingDirectory, file_name);
            const content = await (0, import_promises4.readFile)(filePath, "utf-8");
            const lines = content.split("\n");
            let matches = [];
            for (let i = 0; i < lines.length; i++) {
              let line = lines[i];
              let searchPattern = pattern;
              if (!case_sensitive) {
                line = line.toLowerCase();
                searchPattern = pattern.toLowerCase();
              }
              let isMatch = false;
              if (use_regex) {
                try {
                  const regex = new RegExp(searchPattern);
                  isMatch = regex.test(line);
                } catch (e) {
                  return { error: `Invalid regex pattern: ${e instanceof Error ? e.message : String(e)}` };
                }
              } else {
                isMatch = line.includes(searchPattern);
              }
              if (isMatch) {
                matches.push({
                  line_number: i + 1,
                  content: lines[i]
                });
              }
            }
            return {
              file_name,
              pattern,
              match_count: matches.length,
              matches: matches.slice(0, 100),
              note: matches.length > 100 ? `Showing first 100 of ${matches.length} matches` : void 0
            };
          } catch (e) {
            return { error: `Failed to search file: ${e instanceof Error ? e.message : String(e)}` };
          }
        }
      });
      tools.push(searchInFileTool);
      const deleteLinesInFileTool = (0, import_sdk3.tool)({
        name: "delete_lines_in_file",
        description: import_sdk3.text`
      Delete a specific line or range of lines from a file.
      Line numbers are 1-indexed (line 1 is the first line).
      If end_line is omitted, only start_line will be deleted.
    `,
        parameters: {
          file_name: import_zod2.z.string(),
          start_line: import_zod2.z.number().int().min(1).describe("The starting line number to delete (1-indexed)"),
          end_line: import_zod2.z.number().int().min(1).optional().describe("Optional: The ending line number to delete (inclusive). If omitted, only deletes start_line.")
        },
        implementation: async ({ file_name, start_line, end_line }) => {
          try {
            const filePath = validatePath(currentWorkingDirectory, file_name);
            let content = "";
            try {
              content = await (0, import_promises4.readFile)(filePath, "utf-8");
            } catch {
              return { error: `File '${file_name}' does not exist.` };
            }
            const lines = content.split("\n");
            const actualEndLine = end_line ?? start_line;
            if (start_line > lines.length) {
              return { error: `Start line ${start_line} is beyond the end of the file (${lines.length} lines)` };
            }
            const deleteCount = Math.min(actualEndLine - start_line + 1, lines.length - start_line + 1);
            if (deleteCount <= 0) {
              return { error: `Invalid line range. End line must be >= Start line.` };
            }
            lines.splice(start_line - 1, deleteCount);
            await (0, import_promises4.writeFile)(filePath, lines.join("\n"), "utf-8");
            return {
              success: true,
              message: `Deleted ${deleteCount} line(s) (lines ${start_line}-${actualEndLine}) from ${file_name}`,
              new_line_count: lines.length
            };
          } catch (e) {
            return { error: `Failed to delete lines: ${e instanceof Error ? e.message : String(e)}` };
          }
        }
      });
      tools.push(deleteLinesInFileTool);
      if (allowGitHubTools) {
        const checkGhInstalled = async () => {
          try {
            const cmd = process.platform === "win32" ? "where gh" : "which gh";
            const child = (0, import_child_process3.spawn)(cmd, [], { shell: true });
            await new Promise((resolve5) => child.on("close", resolve5));
            return true;
          } catch (e) {
            return "GitHub CLI ('gh') is not installed. Please ask the user to install it from https://cli.github.com/";
          }
        };
        const ghAuthTool = (0, import_sdk3.tool)({
          name: "gh_auth",
          description: "Check GitHub authentication status. If not authenticated, opens a terminal window for the user to sign in.",
          parameters: {},
          implementation: async () => {
            const isInstalled = await checkGhInstalled();
            if (typeof isInstalled === "string") return { error: isInstalled };
            try {
              const statusChild = (0, import_child_process3.spawn)("gh auth status", [], { shell: true });
              let stderr = "";
              statusChild.stderr.on("data", (d) => stderr += d);
              await new Promise((resolve5) => statusChild.on("close", resolve5));
              if (statusChild.exitCode === 0) {
                return { success: true, message: "Already authenticated with GitHub." };
              } else {
                const escapedDir = currentWorkingDirectory.replace(/"/g, '""');
                const shellCommand = `start "" /D "${escapedDir}" cmd.exe /k "gh auth login --git-protocol=https & exit"`;
                (0, import_child_process3.spawn)("cmd.exe", ["/c", shellCommand], { detached: true, stdio: "ignore" });
                return { success: true, message: "Opened a terminal window for GitHub authentication. Please sign in there." };
              }
            } catch (e) {
              return { error: `Auth check failed: ${e instanceof Error ? e.message : String(e)}` };
            }
          }
        });
        tools.push(ghAuthTool);
        const ghCreateIssueTool = (0, import_sdk3.tool)({
          name: "gh_create_issue",
          description: "Create a new GitHub issue in the current repository.",
          parameters: {
            title: import_zod2.z.string(),
            body: import_zod2.z.string().optional(),
            labels: import_zod2.z.array(import_zod2.z.string()).optional()
          },
          implementation: async ({ title, body, labels }) => {
            const isInstalled = await checkGhInstalled();
            if (typeof isInstalled === "string") return { error: isInstalled };
            try {
              let tempFilePath = "";
              const ghArgs = ["issue", "create", "--title", title];
              if (body) {
                tempFilePath = (0, import_path8.join)(currentWorkingDirectory, `gh_issue_body_${Date.now()}.md`);
                await (0, import_promises4.writeFile)(tempFilePath, body, "utf-8");
                ghArgs.push("--body-file", tempFilePath);
              }
              if (labels) {
                for (const label of labels) {
                  ghArgs.push("-l", label);
                }
              }
              const child = (0, import_child_process3.spawn)("gh", ghArgs);
              let stdout = "", stderr = "";
              child.stdout.on("data", (d) => stdout += d);
              child.stderr.on("data", (d) => stderr += d);
              await new Promise((resolve5) => child.on("close", resolve5));
              if (tempFilePath) await (0, import_promises4.rm)(tempFilePath, { force: true });
              if (child.exitCode === 0) return { success: true, url: stdout.trim() };
              return { error: `Failed to create issue: ${stderr}` };
            } catch (e) {
              return { error: `Create issue failed: ${e instanceof Error ? e.message : String(e)}` };
            }
          }
        });
        tools.push(ghCreateIssueTool);
        const ghListIssuesTool = (0, import_sdk3.tool)({
          name: "gh_list_issues",
          description: "List issues in the current repository.",
          parameters: {
            state: import_zod2.z.enum(["open", "closed"]).optional().default("open"),
            labels: import_zod2.z.array(import_zod2.z.string()).optional(),
            limit: import_zod2.z.number().min(1).max(50).optional().default(10)
          },
          implementation: async ({ state, labels, limit }) => {
            const isInstalled = await checkGhInstalled();
            if (typeof isInstalled === "string") return { error: isInstalled };
            try {
              const ghArgs = ["issue", "list", "--state", state, "--limit", String(limit), "--json", "number,title,state,url,labels"];
              if (labels) {
                for (const label of labels) {
                  ghArgs.push("-l", label);
                }
              }
              const child = (0, import_child_process3.spawn)("gh", ghArgs);
              let stdout = "", stderr = "";
              child.stdout.on("data", (d) => stdout += d);
              child.stderr.on("data", (d) => stderr += d);
              await new Promise((resolve5) => child.on("close", resolve5));
              if (child.exitCode === 0) {
                try {
                  return { issues: JSON.parse(stdout) };
                } catch {
                  return { error: "Failed to parse issue list output" };
                }
              }
              return { error: `List issues failed: ${stderr}` };
            } catch (e) {
              return { error: `List issues failed: ${e instanceof Error ? e.message : String(e)}` };
            }
          }
        });
        tools.push(ghListIssuesTool);
        const ghViewCommentsTool = (0, import_sdk3.tool)({
          name: "gh_view_comments",
          description: "View comments on a specific issue or pull request.",
          parameters: {
            number: import_zod2.z.number().describe("The issue or PR number"),
            type: import_zod2.z.enum(["issue", "pr"]).default("issue").describe("Whether it's an issue or a pull request")
          },
          implementation: async ({ number, type }) => {
            const isInstalled = await checkGhInstalled();
            if (typeof isInstalled === "string") return { error: isInstalled };
            try {
              const ghArgs = type === "issue" ? ["issue", "view", String(number), "--json", "comments"] : ["pr", "view", String(number), "--json", "comments"];
              const child = (0, import_child_process3.spawn)("gh", ghArgs);
              let stdout = "", stderr = "";
              child.stdout.on("data", (d) => stdout += d);
              child.stderr.on("data", (d) => stderr += d);
              await new Promise((resolve5) => child.on("close", resolve5));
              if (child.exitCode === 0) {
                try {
                  const data = JSON.parse(stdout);
                  return { comments: data.comments || [] };
                } catch {
                  return { raw_output: stdout };
                }
              }
              return { error: `View comments failed: ${stderr}` };
            } catch (e) {
              return { error: `View comments failed: ${e instanceof Error ? e.message : String(e)}` };
            }
          }
        });
        tools.push(ghViewCommentsTool);
        const ghCreatePrTool = (0, import_sdk3.tool)({
          name: "gh_create_pr",
          description: "Create a new pull request in the current repository.",
          parameters: {
            title: import_zod2.z.string(),
            body: import_zod2.z.string().optional(),
            head_branch: import_zod2.z.string().describe("The branch containing your changes"),
            base_branch: import_zod2.z.string().default("main").describe("The branch you want to merge into (e.g., main, master)")
          },
          implementation: async ({ title, body, head_branch, base_branch }) => {
            const isInstalled = await checkGhInstalled();
            if (typeof isInstalled === "string") return { error: isInstalled };
            try {
              let tempFilePath = "";
              const ghArgs = ["pr", "create", "--title", title, "--head", head_branch, "--base", base_branch];
              if (body) {
                tempFilePath = (0, import_path8.join)(currentWorkingDirectory, `gh_pr_body_${Date.now()}.md`);
                await (0, import_promises4.writeFile)(tempFilePath, body, "utf-8");
                ghArgs.push("--body-file", tempFilePath);
              }
              const child = (0, import_child_process3.spawn)("gh", ghArgs);
              let stdout = "", stderr = "";
              child.stdout.on("data", (d) => stdout += d);
              child.stderr.on("data", (d) => stderr += d);
              await new Promise((resolve5) => child.on("close", resolve5));
              if (tempFilePath) await (0, import_promises4.rm)(tempFilePath, { force: true });
              if (child.exitCode === 0) return { success: true, url: stdout.trim() };
              return { error: `Failed to create PR: ${stderr}` };
            } catch (e) {
              return { error: `Create PR failed: ${e instanceof Error ? e.message : String(e)}` };
            }
          }
        });
        tools.push(ghCreatePrTool);
        const ghListPrsTool = (0, import_sdk3.tool)({
          name: "gh_list_prs",
          description: "List pull requests in the current repository.",
          parameters: {
            state: import_zod2.z.enum(["open", "closed"]).optional().default("open"),
            limit: import_zod2.z.number().min(1).max(50).optional().default(10)
          },
          implementation: async ({ state, limit }) => {
            const isInstalled = await checkGhInstalled();
            if (typeof isInstalled === "string") return { error: isInstalled };
            try {
              const ghArgs = ["pr", "list", "--state", state, "--limit", String(limit), "--json", "number,title,state,url,headRefName,baseRefName"];
              const child = (0, import_child_process3.spawn)("gh", ghArgs);
              let stdout = "", stderr = "";
              child.stdout.on("data", (d) => stdout += d);
              child.stderr.on("data", (d) => stderr += d);
              await new Promise((resolve5) => child.on("close", resolve5));
              if (child.exitCode === 0) {
                try {
                  return { pull_requests: JSON.parse(stdout) };
                } catch {
                  return { error: "Failed to parse PR list output" };
                }
              }
              return { error: `List PRs failed: ${stderr}` };
            } catch (e) {
              return { error: `List PRs failed: ${e instanceof Error ? e.message : String(e)}` };
            }
          }
        });
        tools.push(ghListPrsTool);
        const ghViewPrDiffTool = (0, import_sdk3.tool)({
          name: "gh_view_pr_diff",
          description: "Fetch the diff/patch of a specific pull request.",
          parameters: {
            number: import_zod2.z.number().describe("The PR number")
          },
          implementation: async ({ number }) => {
            const isInstalled = await checkGhInstalled();
            if (typeof isInstalled === "string") return { error: isInstalled };
            try {
              const ghArgs = ["pr", "diff", String(number)];
              const child = (0, import_child_process3.spawn)("gh", ghArgs);
              let stdout = "", stderr = "";
              child.stdout.on("data", (d) => stdout += d);
              child.stderr.on("data", (d) => stderr += d);
              await new Promise((resolve5) => child.on("close", resolve5));
              if (child.exitCode === 0) {
                return { diff: stdout.substring(0, 5e4) + (stdout.length > 5e4 ? "\n... (truncated)" : "") };
              }
              return { error: `Fetch PR diff failed: ${stderr}` };
            } catch (e) {
              return { error: `Fetch PR diff failed: ${e instanceof Error ? e.message : String(e)}` };
            }
          }
        });
        tools.push(ghViewPrDiffTool);
        const ghPushTool = (0, import_sdk3.tool)({
          name: "gh_push",
          description: "Push local commits to the remote GitHub repository.",
          parameters: {
            branch: import_zod2.z.string().optional().describe("Optional: The branch to push. Defaults to current branch.")
          },
          implementation: async ({ branch }) => {
            const isInstalled = await checkGhInstalled();
            if (typeof isInstalled === "string") return { error: isInstalled };
            try {
              const gitArgs = ["push", "origin"];
              if (branch) gitArgs.push(branch);
              const child = (0, import_child_process3.spawn)("git", gitArgs);
              let stdout = "", stderr = "";
              child.stdout.on("data", (d) => stdout += d);
              child.stderr.on("data", (d) => stderr += d);
              await new Promise((resolve5) => child.on("close", resolve5));
              if (child.exitCode === 0) return { success: true, message: "Pushed successfully." };
              return { error: `Git push failed: ${stderr}` };
            } catch (e) {
              return { error: `Git push failed: ${e instanceof Error ? e.message : String(e)}` };
            }
          }
        });
        tools.push(ghPushTool);
      }
      const casualTools = /* @__PURE__ */ new Set([
        // File ops
        "change_directory",
        "list_directory",
        "read_file",
        "read_file_range",
        "save_file",
        "create_file",
        "move_file",
        "copy_file",
        "delete_path",
        "delete_files_by_pattern",
        "make_directory",
        "find_files",
        "fuzzy_find_local_files",
        "get_file_metadata",
        "search_file_content",
        "search_in_file",
        "search_directory",
        // File editing
        "replace_text_in_file",
        "multi_replace_text",
        "insert_at_line",
        "append_file",
        "delete_lines_in_file",
        // Web / RAG
        "web_search",
        "fetch_web_content",
        "wikipedia_search",
        "rag_web_content",
        "rag_local_files",
        // System / utility
        "get_system_info",
        "read_clipboard",
        "write_clipboard",
        "open_file_or_url",
        "preview_html",
        "read_document",
        "save_memory",
        "send_notification"
      ]);
      tools.sort((a, b) => {
        const aCasual = casualTools.has(a.name);
        const bCasual = casualTools.has(b.name);
        if (aCasual && !bCasual) return -1;
        if (!aCasual && bCasual) return 1;
        return a.name.localeCompare(b.name);
      });
      return tools;
    };
  }
});

// src/toolsDocumentation.ts
var TOOLS_DOCUMENTATION, TOOLS_DOCUMENTATION_LITE;
var init_toolsDocumentation = __esm({
  "src/toolsDocumentation.ts"() {
    "use strict";
    TOOLS_DOCUMENTATION = [
      "# System Instructions: Local Development Assistant",
      "",
      "You are an AI assistant with direct access to the user's local file system and development environment via a suite of tools. Your goal is to help the user complete tasks efficiently and safely.",
      "",
      "##  Core Workflow",
      "Tailor your approach to the task at hand. Not every task requires exploring the full project:",
      "- **For software development tasks** (writing/modifying code, debugging, refactoring):",
      "  1. **Explore:** List files (`list_directory`) to understand the project structure.",
      "  2. **Read:** Read relevant files (`search_in_file` and `read_file_range`) to understand the context/codebase before making changes.",
      "  3. **Plan:** Formulate a plan based on the file contents.",
      "  4. **Execute:** Use the appropriate tools to carry out your plan.",
      "  5. **Verify:** Check your work (e.g., run tests, read back files) to ensure correctness.",
      "- **For simple/utility tasks** (changing directories, opening files, saving a known file, getting system info):",
      "  - Simply perform the requested action without elaborate exploration.",
      "- **For information retrieval** (research, web search, file search):",
      "  - Go directly to the appropriate search/retrieval tool.",
      "",
      "##  Strategic File Handling",
      "- **CRITICAL - Never Read Entire Files Unnecessarily:** Reading full files wastes precious context window and slows down responses. ALWAYS use targeted reading strategies:",
      "  1. **Search First:** Use `search_in_file` to find the exact line numbers containing what you need.",
      "  2. **Read Only What You Need:** Use `read_file_range(start_line, end_line)` to read just those specific lines (\xB15-10 lines for context).",
      "  3. **Only as Last Resort:** Use `read_file` only when the file is known to be small (<50 lines) or you genuinely need the full content.",
      "- **Safe Edits (Recommended):** Use `insert_at_line` for adding code or comments. It is much safer than `replace_text_in_file` because it doesn't fail on whitespace mismatches and guarantees insertion at a specific location.",
      "- **Incremental Builds:** Use `append_file` to add logs, entries, or build files incrementally without overwriting existing content.",
      "- **Search Strategy:",
      "  - *Exact string match (single file):* Use `search_in_file`. **This is your primary search tool.**",
      "  - *Find files by name:* Use `find_files` with glob patterns (e.g., `**/*.ts`).",
      "  - *Fuzzy filename search:* Use `fuzzy_find_local_files` when you're unsure of the exact path.",
      "  - *Semantic/Code search across files:* Use `rag_local_files`. **Preferred over shell grep for code understanding.**",
      '  - *Avoid Shell Grep:* Do NOT use `execute_command("grep ...")` \u2014 dedicated tools provide better context, line numbers, and integration.',
      "",
      "##  Tool Reference",
      "",
      "###  File System",
      "- `list_directory(path?)`: Lists files/folders in the current directory or a specific path. **Use this often.**",
      "- `read_file(file_name)`: Reads the content of a text file.",
      "- `read_file_range(file_name, start_line, end_line)`: Reads a specific range of lines (1-indexed). **Highly recommended for large files to save context window.**",
      "- `save_file(file_name, content)`: Creates or completely overwrites a file.",
      "- `insert_at_line(file_name, line_number, content_to_insert)`: Inserts text at a specific line number. Existing content is pushed down. **Safer than replace_text_in_file.**",
      "- `append_file(file_name, content)`: Appends content to the end of a file (creates if missing).",
      "- `replace_text_in_file(file_name, old_string, new_string)`: Replaces specific text in a file. *Warning: Fails if whitespace/indentation doesn't match exactly.*",
      "- `search_in_file(file_name, pattern, case_sensitive?, use_regex?)`: Searches for a substring or regex within a single file and returns matching line numbers.",
      "- `make_directory(directory_name)`: Creates a new directory path.",
      "- `move_file(source, destination)`: Moves or renames a file/directory.",
      "- `copy_file(source, destination)`: Copies a file.",
      "- `delete_path(path)`: **DESTRUCTIVE!** Permanently deletes a file or directory.",
      "- `delete_files_by_pattern(pattern)`: Deletes multiple files matching a regex (e.g. `^temp_.*`).",
      "- `delete_lines_in_file(file_name, start_line, end_line?)`: Deletes a specific line or range of lines from a file (1-indexed).",
      "- `find_files(pattern)`: Finds files matching a glob pattern (e.g., `**/*.ts`).",
      "- `fuzzy_find_local_files(query, path?, max_results?)`: Fuzzy-find file paths/names using Levenshtein similarity.",
      "- `get_file_metadata(file_name)`: Gets size and modification dates.",
      "- `change_directory(directory)`: Changes the working directory for future commands. **Use this to navigate to subdirectories and gain file system access within different parts of the workspace.**",
      "",
      "###  Git & Version Control",
      "- `git_status()`: View modified files.",
      "- `git_diff(file_path?, cached?)`: See changes in detail.",
      "- `git_commit(message)`: Commit staged changes.",
      "- `git_log(max_count?)`: View commit history.",
      "- `git_add(paths?)`: Stage specific files or all changes for the next commit.",
      "- `git_checkout(branch_name, create_new?)`: Switch to an existing branch or create and switch to a new one.",
      "",
      "###  Advanced File Tools",
      "- `read_document(file_path)`: Parse text from .pdf or .docx files.",
      "- `analyze_project()`: Run configured linters (ESLint, Pylint) to find code issues.",
      "- `query_database(db_path, query)`: Run READ-ONLY SQL queries on SQLite databases.",
      "- `send_notification(title, message)`: Show a desktop notification (useful for long tasks).",
      "",
      "###  Execution & Terminal",
      "- `execute_command(command, input?)`: Runs a shell command in the *background*. **Use only when no dedicated tool exists** (e.g., build scripts, package managers). Returns stdout/stderr.",
      "- `run_in_terminal(command)`: Opens a **visible, interactive** terminal window. Use for long-running servers or scripts requiring user interaction.",
      "- `run_test_command(command)`: Specific wrapper for running tests (e.g., `npm test`).",
      "- `run_javascript(javascript)`: Executes a sandboxed JS/TS snippet (via Deno). **Prefer dedicated tools over running arbitrary code.**",
      "- `run_python(python)`: Executes a Python script (requires system Python). **Prefer dedicated tools over running arbitrary code.**",
      "- `run_cpp(cpp, timeout_seconds?)`: Compiles (g++, requires g++ on PATH) and runs a C++ snippet with a `main()`. Returns stdout/stderr, or compiler errors on failure. **Prefer dedicated tools over running arbitrary code.**",
      "- `run_java(java, timeout_seconds?)`: Compiles (javac, requires a JDK on PATH) and runs a Java snippet. Must contain exactly one `public class <Name>` with a main method \u2014 the class name is auto-detected. Returns stdout/stderr, or compiler errors on failure. **Prefer dedicated tools over running arbitrary code.**",
      "- `run_pyright(python, timeout_seconds?)`: Type-checks (Pyright, requires pyright on PATH) a Python snippet WITHOUT executing it. Returns the diagnostic report and an `exit_code` (0 = no issues, 1 = type errors found). Use before `run_python` to catch type errors without spending an execution cycle.",
      "",
      "###  Web & Research",
      '- `web_search(query, providers?)`: Performs a web search. By default, uses a no-key fallback chain: DuckDuckGo API -> DuckDuckGo HTML fetch -> DuckDuckGo Puppeteer -> Google -> Bing. You can optionally specify providers such as `["duckduckgo-fetch", "google"]`.',
      "- `wikipedia_search(query)`: Searches Wikipedia and returns article summaries.",
      "- `fetch_web_content(url)`: Scrapes the text content of a webpage.",
      "- `rag_web_content(url, query)`: Fetches a page and returns *only* snippets relevant to your query. Best for long docs.",
      "- `rag_local_files(query, path?)`: Semantic search over local files in your workspace. Use to find code or info.",
      "- **Navigation Policy:** For any multi-step browser workflow, you MUST use `browser_session_open` -> `browser_session_control` -> `browser_session_close`. Use `browser_open_page` only for one-shot page reads.",
      "- `browser_session_open(url, wait_for_selector?, include_page_text?)`: Opens a persistent browser session (one active page) and can return full page text at open time.",
      "- `browser_session_control(actions?, read_page?, full_read?, screenshot_path?, full_page_screenshot?, fuzzy_find?, max_results?)`: Reuses the active page for automation, page reading, screenshots, and in-page fuzzy find. Full text is returned on URL change or when `full_read=true`.",
      "- **Click Workaround:** If selector clicks fail on dynamic pages, use an `evaluate` action to find a target by text and call `.click()`, then set `full_read=true` to capture the resulting page state.",
      '- **Minimal Workaround Example:** `browser_session_control({ "actions":[{ "type":"evaluate", "script":"const link=[...document.querySelectorAll(\\\\"a\\\\")].find(a=>a.textContent?.includes(\\"LICENSE\\")); if(link) link.click();" }], "full_read": true })`',
      "- `browser_session_close()`: Closes the active persistent browser session.",
      "- `browser_open_page(url, screenshot_path?, wait_for_selector?, full_page_screenshot?, actions?)`: Stateless one-shot browser render with optional scripted actions (`wait_for_selector`, `wait`, `click`, `type`, `press`, `select`, `hover`, `scroll`, `evaluate`). Do NOT use for multi-step navigation.",
      "",
      "###  System & Utility",
      "- `read_clipboard()`: Reads text from the system clipboard.",
      "- `write_clipboard(text)`: Writes text to the system clipboard.",
      "- `get_system_info()`: Returns OS, CPU, and Memory details.",
      "- `open_file(path)`: Opens a file or URL in the default system application.",
      "- `preview_html(html_content)`: Opens a local HTML preview in the browser.",
      "",
      "###  Agents & Memory",
      "- `save_memory(text)`: Saves a fact/preference to `memory.md`. Use this to remember user preferences, project conventions, or specific instructions across sessions.",
      '- `consult_secondary_agent(task, agent_role?)`: Delegate a task to a specialized Sub-Agent. **Use this for complex coding tasks or research.**\n    - The Sub-Agent will automatically CREATE and SAVE files. You do NOT need to save them yourself.\n    - Supports optional structured handoff via `[HANDOFF_MESSAGE]...[/HANDOFF_MESSAGE]` or JSON `handoff_message`.\n    - Sub-agent browser automation tools are only exposed when `Sub-Agent: Allow Web Search`, `Sub-Agent: Allow Browser Control`, and global `Allow Browser Control` are enabled.\n    - **IMPORTANT:** If the tool output says `[System: Code Block Hidden for Brevity...]`, this is a **SUCCESS** message. It means the file has been written to disk. **DO NOT** complain about "hidden code" or ask for the full content again. Simply proceed by verifying the files exist using `list_directory` or `read_file`. Trust the `[GENERATED_FILES]` list.',
      "",
      "##  Tool Selection Priority",
      "- **ALWAYS prefer dedicated tools over generic execution:**",
      '  - *File operations:* Use `read_file_range`, `save_file`, `replace_text_in_file`, `insert_at_line`, `append_file`, `delete_lines_in_file`, `search_in_file` \u2014 NOT `execute_command("cat ...")` or Python/JS file I/O.',
      '  - *Search & grep:* Use `search_in_file`, `find_files`, `rag_local_files` \u2014 NOT `execute_command("grep ...")`.',
      '  - *Git operations:* Use `git_status`, `git_diff`, `git_commit` \u2014 NOT `execute_command("git ...")` (except for advanced git commands not covered by tools).',
      '  - *Web requests:* Use `web_search`, `fetch_web_content` \u2014 NOT `run_python("requests.get(...)")` or `execute_command("curl ...")`.',
      "- **WHY?** Dedicated tools are:",
      "  - More reliable and provide structured output with line numbers/context",
      "  - Safer (built-in validation, no shell injection risks)",
      "  - Faster (no process spawning overhead)",
      "  - Better integrated with the system (proper error handling, context awareness)",
      "- **ONLY use `execute_command`, `run_python`, `run_javascript`, `run_cpp`, `run_java`, or `run_pyright` when:**",
      "  - No dedicated tool exists for the task",
      "  - You need to run build scripts, tests, or package managers (`npm install`, `pytest`, etc.)",
      "  - The task requires complex system-level operations not available through tools",
      "",
      "##  Best Practices",
      "- **Safety:** You are operating on a real machine. Be *extremely* careful with `delete_path` and `execute_command`.",
      "- **Context:** NEVER read entire files unnecessarily. Always use `search_in_file` + `read_file_range` to target only the lines you need.",
      "- **Formatting:** Always use Markdown code blocks for code generation. Use single backticks for file paths.",
      '- **Git:** Use dedicated `git_*` tools (`git_status`, `git_diff`, `git_commit`) for version control. Only use `execute_command("git ...")` for advanced commands not covered by tools.',
      "",
      "## Safety Settings",
      'Tools capable of execution/automation (Python, JavaScript, Shell, Terminal, Browser Control) are controlled by "Allow" toggles in the plugin settings.',
      '- **Disabled (Default):** The tool is completely blocked. If you need to use it, ask the user to enable the specific "Allow [X]" setting.',
      "- **Enabled:** The tool executes immediately without confirmation.",
      "",
      "##  GitHub Management Protocol",
      "When managing GitHub repositories via `gh` o `git` Tools:",
      "- **Identity:** Always state in the body of your PR that the PR was created or assisted by you (Beledarian_LM_Studio_Toolbox agent).",
      "- **Testing:** Add regression tests if useful and run them (`npm test`) to verify fixes before creating PRs.",
      "- **Auth Flow:** If `gh auth status` fails, ask the user if you should start an authentication flow."
    ].join("\n");
    TOOLS_DOCUMENTATION_LITE = [
      "# System: Local Assistant",
      "",
      "You are an AI assistant with filesystem access. Help the user efficiently. Match your approach to the task:",
      "",
      "## Workflow",
      "- **Dev tasks:** Explore (`list_directory`) \u2192 Read (`search_in_file`/`read_file_range`) \u2192 Plan \u2192 Execute \u2192 Verify.",
      "- **Simple tasks:** Perform the action directly. Do not list directories or read files unnecessarily.",
      "- **Search tasks:** Use search/retrieval tools directly.",
      "",
      "## Key Tools",
      "- `list_directory`, `read_file`, `read_file_range`, `search_in_file`, `save_file`, `replace_text_in_file`, `insert_at_line`, `append_file`, `delete_lines_in_file`",
      "- `make_directory`, `move_file`, `copy_file`, `delete_path`, `find_files`, `fuzzy_find_local_files`",
      "- `web_search`, `fetch_web_content`, `wikipedia_search`, `rag_local_files`, `rag_web_content`",
      "- `execute_command` (shell), `run_in_terminal` (visible), `run_python`, `run_javascript`, `run_cpp`, `run_java`, `run_pyright`",
      "- `git_status`, `git_diff`, `git_commit`, `git_add`, `git_log`, `git_checkout`",
      "- `consult_secondary_agent` \u2014 delegate complex tasks",
      "- `read_document` (pdf/docx), `get_system_info`, `read_clipboard`, `write_clipboard`, `open_file_or_url`, `preview_html`, `save_memory`",
      "",
      "## Rules",
      "- Use dedicated tools over shell commands when available.",
      "- Never read entire files unnecessarily \u2014 use `search_in_file` + `read_file_range`.",
      "- Be careful with `delete_path` and destructive operations.",
      "- Safety toggles in plugin settings control execution tools."
    ].join("\n");
  }
});

// src/promptPreprocessor.ts
function getSubAgentDocsCandidatePaths(currentWorkingDirectory) {
  return [
    (0, import_path9.join)((0, import_path9.dirname)(__dirname), "subagent_docs.md"),
    (0, import_path9.join)((0, import_path9.dirname)(__dirname), "instructions", "subagent_docs.md"),
    (0, import_path9.join)(currentWorkingDirectory, "instructions", "subagent_docs.md"),
    (0, import_path9.join)(currentWorkingDirectory, "subagent_docs.md")
  ];
}
async function promptPreprocessor(ctl, userMessage) {
  const userPrompt = userMessage.getText();
  const history = await ctl.pullHistory();
  let isFirstTurn = false;
  if (Array.isArray(history)) {
    isFirstTurn = history.length === 0;
  } else if ("messages" in history && Array.isArray(history.messages)) {
    isFirstTurn = history.messages.length === 0;
  } else if ("length" in history && typeof history.length === "number") {
    isFirstTurn = history.length === 0;
  } else {
    isFirstTurn = true;
  }
  history.append(userMessage);
  const newFiles = userMessage.getFiles(ctl.client).filter((f) => f.type !== "image");
  const files = history.getAllFiles(ctl.client).filter((f) => f.type !== "image");
  let processingResult = null;
  if (newFiles.length > 0) {
    const strategy = await chooseContextInjectionStrategy(ctl, userPrompt, newFiles);
    if (strategy === "inject-full-content") {
      processingResult = await prepareDocumentContextInjection(ctl, userMessage);
    } else if (strategy === "retrieval") {
      processingResult = await prepareRetrievalResultsContextInjection(ctl, userPrompt, files);
    }
  } else if (files.length > 0) {
    processingResult = await prepareRetrievalResultsContextInjection(ctl, userPrompt, files);
  }
  let currentContent;
  if (processingResult) {
    if (typeof processingResult === "string") {
      currentContent = processingResult;
    } else {
      currentContent = processingResult.getText();
    }
  } else {
    currentContent = userPrompt;
  }
  const pluginConfig = ctl.getPluginConfig(pluginConfigSchematics);
  const defaultWorkspacePath = pluginConfig.get("defaultWorkspacePath");
  const frequency = pluginConfig.get("subAgentFrequency");
  const debugMode = pluginConfig.get("enableDebugMode");
  const messageLanguage = pluginConfig.get("messageLanguage");
  const rt = getDict(messageLanguage).runtime;
  const uiLanguageOverride = pluginConfig.get("uiLanguageOverride");
  try {
    const state2 = await getPersistedState(defaultWorkspacePath);
    if (state2.uiLanguageOverride !== uiLanguageOverride) {
      state2.uiLanguageOverride = uiLanguageOverride;
      await savePersistedState(state2);
      ctl.debug(`[i18n] uiLanguageOverride saved: "${uiLanguageOverride}". Restart the plugin to apply the new UI language.`);
    }
  } catch (e) {
    ctl.debug("[i18n] Failed to persist uiLanguageOverride.", e);
  }
  const planMode = pluginConfig.get("planMode");
  let planHint = "";
  if (planMode === "always") {
    planHint = rt.planHintAlways;
  } else if (planMode === "when_useful") {
    planHint = rt.planHintWhenUseful;
  }
  let delegationHint = "";
  if (frequency === "always") {
    delegationHint = rt.delegationHintAlways;
  } else if (frequency === "when_useful") {
    delegationHint = rt.delegationHintWhenUseful;
    if (debugMode) {
      delegationHint += rt.delegationHintWhenUsefulDebug;
    }
  } else if (frequency === "hard_tasks") {
    delegationHint = rt.delegationHintHardTasks;
  }
  if (delegationHint && pluginConfig.get("enableSecondaryAgent")) {
    currentContent += delegationHint;
  }
  if (planHint) {
    currentContent += planHint;
  }
  const enableSecondary = pluginConfig.get("enableSecondaryAgent");
  const state = await getPersistedState(defaultWorkspacePath);
  if (isFirstTurn) {
    state.subAgentDocsInjected = false;
    await savePersistedState(state);
  }
  if (enableSecondary && !state.subAgentDocsInjected) {
    const { currentWorkingDirectory } = state;
    const candidatePaths = getSubAgentDocsCandidatePaths(currentWorkingDirectory);
    let docsInjected = false;
    for (const subAgentDocsPath of candidatePaths) {
      try {
        const docsContent = await (0, import_promises5.readFile)(subAgentDocsPath, "utf-8");
        if (docsContent && docsContent.trim().length > 0) {
          currentContent += `

---

${docsContent}

---

`;
          ctl.debug(`subagent_docs.md injected into context from: ${subAgentDocsPath}`);
          state.subAgentDocsInjected = true;
          await savePersistedState(state);
          docsInjected = true;
          break;
        }
      } catch (e) {
      }
    }
    if (!docsInjected) {
      ctl.debug("subagent_docs.md not found or failed to load from plugin/workspace paths. Skipping injection.");
    }
  }
  if (isFirstTurn) {
    const simpleSystemPrompt = pluginConfig.get("simpleSystemPrompt");
    let injectionContent = simpleSystemPrompt ? TOOLS_DOCUMENTATION_LITE : TOOLS_DOCUMENTATION;
    try {
      const { currentWorkingDirectory } = state;
      const candidateStartupPaths = [
        (0, import_path9.join)(currentWorkingDirectory, ".beledarian", "startup.md"),
        (0, import_path9.join)(currentWorkingDirectory, "instructions", "startup.md"),
        (0, import_path9.join)(currentWorkingDirectory, "startup.md")
      ];
      let startupContent = "";
      let usedStartupPath = "";
      for (const startupPath of candidateStartupPaths) {
        try {
          startupContent = await (0, import_promises5.readFile)(startupPath, "utf-8");
          usedStartupPath = (0, import_path9.dirname)(startupPath);
          ctl.debug(`startup.md loaded from: ${startupPath}`);
          break;
        } catch (e) {
        }
      }
      if (startupContent) {
        const filesToRead = startupContent.split("\n").map((f) => f.trim()).filter((f) => f);
        for (const file of filesToRead) {
          const candidateFilePaths = [
            (0, import_path9.join)(usedStartupPath, file),
            (0, import_path9.join)(currentWorkingDirectory, file)
          ];
          let loaded = false;
          for (const filePath of candidateFilePaths) {
            try {
              const fileContent = await (0, import_promises5.readFile)(filePath, "utf-8");
              if (fileContent.trim().length > 0) {
                injectionContent = `

---

${fileContent}

---

${injectionContent}`;
                ctl.debug(`${file} loaded and injected into context from ${filePath}.`);
                loaded = true;
                break;
              }
            } catch (e) {
            }
          }
          if (!loaded) {
            ctl.debug(`Failed to load ${file} from startup.md.`);
          }
        }
      }
    } catch (e) {
      ctl.debug("No startup.md file found or failed to load.");
    }
    currentContent = `${injectionContent}

---

${currentContent}`;
  }
  if (currentContent !== userPrompt) {
    return currentContent;
  }
  try {
    state.messageCount++;
    await savePersistedState(state);
  } catch (e) {
    ctl.debug("Failed to update message count or memory.", e);
  }
  return userMessage;
}
async function prepareRetrievalResultsContextInjection(ctl, originalUserPrompt, files) {
  const pluginConfig = ctl.getPluginConfig(pluginConfigSchematics);
  const retrievalLimit = pluginConfig.get("retrievalLimit");
  const retrievalAffinityThreshold = pluginConfig.get("retrievalAffinityThreshold");
  const statusSteps = /* @__PURE__ */ new Map();
  const rtRetrieve = getDict(
    ctl.getPluginConfig(pluginConfigSchematics).get("messageLanguage")
  ).runtime;
  const retrievingStatus = ctl.createStatus({
    status: "loading",
    text: rtRetrieve.statusLoadingEmbeddingModel
  });
  const model = await ctl.client.embedding.model("nomic-ai/nomic-embed-text-v1.5-GGUF", {
    signal: ctl.abortSignal
  });
  retrievingStatus.setState({
    status: "loading",
    text: rtRetrieve.statusRetrievingCitations
  });
  const result2 = await ctl.client.files.retrieve(originalUserPrompt, files, {
    embeddingModel: model,
    // Affinity threshold: 0.6 not implemented in SDK retrieve options directly usually, 
    // but we filter below.
    limit: retrievalLimit,
    signal: ctl.abortSignal,
    onFileProcessList(filesToProcess) {
      for (const file of filesToProcess) {
        statusSteps.set(
          file,
          retrievingStatus.addSubStatus({
            status: "waiting",
            text: `Process ${file.name} for retrieval`
          })
        );
      }
    },
    onFileProcessingStart(file) {
      statusSteps.get(file).setState({ status: "loading", text: `Processing ${file.name} for retrieval` });
    },
    onFileProcessingEnd(file) {
      statusSteps.get(file).setState({ status: "done", text: `Processed ${file.name} for retrieval` });
    },
    onFileProcessingStepProgress(file, step, progressInStep) {
      const verb = step === "loading" ? "Loading" : step === "chunking" ? "Chunking" : "Embedding";
      statusSteps.get(file).setState({
        status: "loading",
        text: `${verb} ${file.name} for retrieval (${(progressInStep * 100).toFixed(1)}%)`
      });
    }
  });
  result2.entries = result2.entries.filter((entry) => entry.score > retrievalAffinityThreshold);
  let processedContent = "";
  const numRetrievals = result2.entries.length;
  if (numRetrievals > 0) {
    retrievingStatus.setState({
      status: "done",
      text: rtRetrieve.statusRetrievedCitations(numRetrievals)
    });
    ctl.debug("Retrieval results", result2);
    processedContent += rtRetrieve.citationPrefix;
    let citationNumber = 1;
    result2.entries.forEach((result3) => {
      const completeText = result3.content;
      processedContent += rtRetrieve.citationEntry(citationNumber, completeText);
      citationNumber++;
    });
    await ctl.addCitations(result2);
    processedContent += rtRetrieve.citationSuffix(originalUserPrompt);
  } else {
    retrievingStatus.setState({
      status: "canceled",
      text: rtRetrieve.statusNoRelevantCitations
    });
    ctl.debug("No relevant citations found for user query");
    processedContent = rtRetrieve.noRelevantCitationsNote + `

User Query:

${originalUserPrompt}`;
  }
  ctl.debug("Processed content", processedContent);
  return processedContent;
}
async function prepareDocumentContextInjection(ctl, input) {
  const documentInjectionSnippets = /* @__PURE__ */ new Map();
  const files = input.consumeFiles(ctl.client, (file) => file.type !== "image");
  for (const file of files) {
    const { content } = await ctl.client.files.parseDocument(file, {
      signal: ctl.abortSignal
    });
    ctl.debug(import_sdk4.text`
      Strategy: inject-full-content. Injecting full content of file '${file}' into the
      context. Length: ${content.length}.
    `);
    documentInjectionSnippets.set(file, content);
  }
  let formattedFinalUserPrompt = "";
  const rtDoc = getDict(
    ctl.getPluginConfig(pluginConfigSchematics).get("messageLanguage")
  ).runtime;
  if (documentInjectionSnippets.size > 0) {
    formattedFinalUserPrompt += rtDoc.documentInjectionHeader;
    for (const [fileHandle, snippet] of documentInjectionSnippets) {
      formattedFinalUserPrompt += rtDoc.documentInjectionFileBlock(fileHandle.name, snippet);
    }
    formattedFinalUserPrompt += rtDoc.documentInjectionSuffix(input.getText());
  }
  input.replaceText(formattedFinalUserPrompt);
  return input;
}
async function measureContextWindow(ctx, model) {
  const currentContextFormatted = await model.applyPromptTemplate(ctx);
  const totalTokensInContext = await model.countTokens(currentContextFormatted);
  const modelContextLength = await model.getContextLength();
  const modelRemainingContextLength = modelContextLength - totalTokensInContext;
  const contextOccupiedPercent = totalTokensInContext / modelContextLength * 100;
  return {
    totalTokensInContext,
    modelContextLength,
    modelRemainingContextLength,
    contextOccupiedPercent
  };
}
async function chooseContextInjectionStrategy(ctl, originalUserPrompt, files) {
  const rtStrategy = getDict(
    ctl.getPluginConfig(pluginConfigSchematics).get("messageLanguage")
  ).runtime;
  const status = ctl.createStatus({
    status: "loading",
    text: rtStrategy.statusDecidingStrategy
  });
  const model = await ctl.client.llm.model();
  const ctx = await ctl.pullHistory();
  const {
    totalTokensInContext,
    modelContextLength,
    modelRemainingContextLength,
    contextOccupiedPercent
  } = await measureContextWindow(ctx, model);
  ctl.debug(
    `Context measurement result:

	Total tokens in context: ${totalTokensInContext}
	Model context length: ${modelContextLength}
	Model remaining context length: ${modelRemainingContextLength}
	Context occupied percent: ${contextOccupiedPercent.toFixed(2)}%
`
  );
  let totalFileTokenCount = 0;
  let totalReadTime = 0;
  let totalTokenizeTime = 0;
  for (const file of files) {
    const startTime = performance.now();
    const loadingStatus = status.addSubStatus({
      status: "loading",
      text: rtStrategy.statusLoadingParser(file.name)
    });
    let actionProgressing = "Reading";
    let parserIndicator = "";
    const { content } = await ctl.client.files.parseDocument(file, {
      signal: ctl.abortSignal,
      onParserLoaded: (parser) => {
        loadingStatus.setState({
          status: "loading",
          text: `${parser.library} loaded for ${file.name}...`
        });
        if (parser.library !== "builtIn") {
          actionProgressing = "Parsing";
          parserIndicator = ` with ${parser.library}`;
        }
      },
      onProgress: (progress) => {
        loadingStatus.setState({
          status: "loading",
          text: `${actionProgressing} file ${file.name}${parserIndicator}... (${(progress * 100).toFixed(2)}%)`
        });
      }
    });
    loadingStatus.remove();
    totalReadTime += performance.now() - startTime;
    const startTokenizeTime = performance.now();
    totalFileTokenCount += await model.countTokens(content);
    totalTokenizeTime += performance.now() - startTokenizeTime;
    if (totalFileTokenCount > modelRemainingContextLength) {
      break;
    }
  }
  ctl.debug(`Total file read time: ${totalReadTime.toFixed(2)} ms`);
  ctl.debug(`Total tokenize time: ${totalTokenizeTime.toFixed(2)} ms`);
  ctl.debug(`Original User Prompt: ${originalUserPrompt}`);
  const userPromptTokenCount = (await model.tokenize(originalUserPrompt)).length;
  const totalFilePlusPromptTokenCount = totalFileTokenCount + userPromptTokenCount;
  const contextOccupiedFraction = contextOccupiedPercent / 100;
  const targetContextUsePercent = 0.7;
  const targetContextUsage = targetContextUsePercent * (1 - contextOccupiedFraction);
  const availableContextTokens = Math.floor(modelRemainingContextLength * targetContextUsage);
  ctl.debug("Strategy Calculation:");
  ctl.debug(`	Total Tokens in All Files: ${totalFileTokenCount}`);
  ctl.debug(`	Total Tokens in User Prompt: ${userPromptTokenCount}`);
  ctl.debug(`	Model Context Remaining: ${modelRemainingContextLength} tokens`);
  ctl.debug(`	Context Occupied: ${contextOccupiedPercent.toFixed(2)}%`);
  ctl.debug(`	Available Tokens: ${availableContextTokens}
`);
  if (totalFilePlusPromptTokenCount > availableContextTokens) {
    const chosenStrategy2 = "retrieval";
    ctl.debug(
      `Chosen context injection strategy: '${chosenStrategy2}'. Total file + prompt token count: ${totalFilePlusPromptTokenCount} > ${targetContextUsage * 100}% * available context tokens: ${availableContextTokens}`
    );
    status.setState({
      status: "done",
      text: rtStrategy.statusStrategyChosen(chosenStrategy2, "Retrieval is optimal for the size of content provided")
    });
    return chosenStrategy2;
  }
  const chosenStrategy = "inject-full-content";
  status.setState({
    status: "done",
    text: rtStrategy.statusStrategyChosen(chosenStrategy, "All content can fit into the context")
  });
  return chosenStrategy;
}
var import_sdk4, import_promises5, import_path9;
var init_promptPreprocessor = __esm({
  "src/promptPreprocessor.ts"() {
    "use strict";
    import_sdk4 = require("@lmstudio/sdk");
    import_promises5 = require("fs/promises");
    import_path9 = require("path");
    init_config();
    init_toolsDocumentation();
    init_stateManager();
    init_i18n();
  }
});

// src/index.ts
var src_exports = {};
__export(src_exports, {
  main: () => main
});
async function main(context) {
  context.withConfigSchematics(pluginConfigSchematics);
  context.withToolsProvider(toolsProvider);
  context.withPromptPreprocessor(promptPreprocessor);
}
var init_src = __esm({
  "src/index.ts"() {
    "use strict";
    init_toolsProvider();
    init_promptPreprocessor();
    init_config();
  }
});

// .lmstudio/entry.ts
var import_sdk5 = require("@lmstudio/sdk");
var clientIdentifier = process.env.LMS_PLUGIN_CLIENT_IDENTIFIER;
var clientPasskey = process.env.LMS_PLUGIN_CLIENT_PASSKEY;
var baseUrl = process.env.LMS_PLUGIN_BASE_URL;
var client = new import_sdk5.LMStudioClient({
  clientIdentifier,
  clientPasskey,
  baseUrl
});
globalThis.__LMS_PLUGIN_CONTEXT = true;
var predictionLoopHandlerSet = false;
var promptPreprocessorSet = false;
var configSchematicsSet = false;
var globalConfigSchematicsSet = false;
var toolsProviderSet = false;
var generatorSet = false;
var selfRegistrationHost = client.plugins.getSelfRegistrationHost();
var pluginContext = {
  withPredictionLoopHandler: (generate) => {
    if (predictionLoopHandlerSet) {
      throw new Error("PredictionLoopHandler already registered");
    }
    if (toolsProviderSet) {
      throw new Error("PredictionLoopHandler cannot be used with a tools provider");
    }
    predictionLoopHandlerSet = true;
    selfRegistrationHost.setPredictionLoopHandler(generate);
    return pluginContext;
  },
  withPromptPreprocessor: (preprocess) => {
    if (promptPreprocessorSet) {
      throw new Error("PromptPreprocessor already registered");
    }
    promptPreprocessorSet = true;
    selfRegistrationHost.setPromptPreprocessor(preprocess);
    return pluginContext;
  },
  withConfigSchematics: (configSchematics) => {
    if (configSchematicsSet) {
      throw new Error("Config schematics already registered");
    }
    configSchematicsSet = true;
    selfRegistrationHost.setConfigSchematics(configSchematics);
    return pluginContext;
  },
  withGlobalConfigSchematics: (globalConfigSchematics) => {
    if (globalConfigSchematicsSet) {
      throw new Error("Global config schematics already registered");
    }
    globalConfigSchematicsSet = true;
    selfRegistrationHost.setGlobalConfigSchematics(globalConfigSchematics);
    return pluginContext;
  },
  withToolsProvider: (toolsProvider2) => {
    if (toolsProviderSet) {
      throw new Error("Tools provider already registered");
    }
    if (predictionLoopHandlerSet) {
      throw new Error("Tools provider cannot be used with a predictionLoopHandler");
    }
    toolsProviderSet = true;
    selfRegistrationHost.setToolsProvider(toolsProvider2);
    return pluginContext;
  },
  withGenerator: (generator) => {
    if (generatorSet) {
      throw new Error("Generator already registered");
    }
    generatorSet = true;
    selfRegistrationHost.setGenerator(generator);
    return pluginContext;
  }
};
Promise.resolve().then(() => (init_src(), src_exports)).then(async (module2) => {
  return await module2.main(pluginContext);
}).then(() => {
  selfRegistrationHost.initCompleted();
}).catch((error) => {
  console.error("Failed to execute the main function of the plugin.");
  console.error(error);
});
