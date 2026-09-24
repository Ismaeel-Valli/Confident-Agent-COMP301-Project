"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.getPersistedState = getPersistedState;
exports.savePersistedState = savePersistedState;
exports.ensureWorkspaceExists = ensureWorkspaceExists;
const promises_1 = require("fs/promises");
const path_1 = require("path");
const os = __importStar(require("os"));
const CONFIG_FILE_NAME = ".plugin_state.json";
const DEFAULT_DIR = (0, path_1.join)(os.homedir(), ".beledarians-llm-toolbox", "workspace");
function resolveWorkspaceDirectory(configuredWorkspacePath) {
    const raw = (configuredWorkspacePath ?? "").trim();
    if (!raw)
        return DEFAULT_DIR;
    // Support Windows-style env vars in config values (e.g. %USERPROFILE%\projects\workspace)
    const expanded = raw.replace(/%([^%]+)%/g, (_match, varName) => process.env[varName] ?? `%${varName}%`);
    return (0, path_1.isAbsolute)(expanded) ? expanded : (0, path_1.resolve)(DEFAULT_DIR, expanded);
}
async function getPersistedState(configuredWorkspacePath) {
    const configuredDirectory = resolveWorkspaceDirectory(configuredWorkspacePath);
    try {
        const statePath = (0, path_1.join)(os.homedir(), ".beledarians-llm-toolbox", CONFIG_FILE_NAME);
        const content = await (0, promises_1.readFile)(statePath, "utf-8");
        const state = JSON.parse(content);
        return {
            // configuredDirectory is a startup default/fallback, not a forced override
            currentWorkingDirectory: state.currentWorkingDirectory ?? configuredDirectory,
            messageCount: state.messageCount ?? 0,
            dontAskToCompress: state.dontAskToCompress ?? false,
            subAgentDocsInjected: state.subAgentDocsInjected ?? false,
            uiLanguageOverride: state.uiLanguageOverride ?? "auto",
        };
    }
    catch (error) {
        return {
            currentWorkingDirectory: configuredDirectory,
            messageCount: 0,
            dontAskToCompress: false,
            subAgentDocsInjected: false,
            uiLanguageOverride: "auto",
        };
    }
}
async function savePersistedState(state) {
    try {
        const statePath = (0, path_1.join)(os.homedir(), ".beledarians-llm-toolbox", CONFIG_FILE_NAME);
        const dir = (0, path_1.join)(os.homedir(), ".beledarians-llm-toolbox");
        await (0, promises_1.mkdir)(dir, { recursive: true });
        await (0, promises_1.writeFile)(statePath, JSON.stringify(state, null, 2), "utf-8");
    }
    catch (error) {
        console.error("Failed to save plugin state:", error);
    }
}
async function ensureWorkspaceExists(path) {
    try {
        await (0, promises_1.mkdir)(path, { recursive: true });
    }
    catch (error) {
        console.error(`Failed to create/access directory ${path}`, error);
    }
}
//# sourceMappingURL=stateManager.js.map