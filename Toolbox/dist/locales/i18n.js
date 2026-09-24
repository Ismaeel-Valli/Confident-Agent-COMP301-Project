"use strict";
/**
 * i18n.ts — Central internationalization engine for the Beledarians LM Studio Toolbox plugin.
 *
 * Implements the "Dual-Layer Language Mechanism":
 *   Layer 1 (Config UI)   — detected once at startup from OS locale; immutable per SDK constraints.
 *   Layer 2 (Runtime)     — read dynamically per-turn from the user-selectable "messageLanguage" field.
 *
 * Supported locales: "en", "zh-CN", "zh-TW", "de"
 */
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
exports.SUPPORTED_LOCALE_IDS = void 0;
exports.detectSystemLanguage = detectSystemLanguage;
exports.resolveLocale = resolveLocale;
exports.getDict = getDict;
exports.getSystemDict = getSystemDict;
const en_1 = require("./en");
const zh_CN_1 = require("./zh-CN");
const zh_TW_1 = require("./zh-TW");
const de_1 = require("./de");
const fs_1 = require("fs");
const path_1 = require("path");
const os = __importStar(require("os"));
// ─────────────────────────────────────────────────────────────
// Registry
// ─────────────────────────────────────────────────────────────
const LOCALES = {
    en: en_1.en,
    "zh-CN": zh_CN_1.zhCN,
    "zh-TW": zh_TW_1.zhTW,
    de: de_1.de,
};
/** The canonical locale IDs this plugin exposes to users (Layer 2 dropdown). */
exports.SUPPORTED_LOCALE_IDS = Object.keys(LOCALES);
// ─────────────────────────────────────────────────────────────
// Persisted Override (synchronous boot-time read)
// ─────────────────────────────────────────────────────────────
/**
 * Reads the plugin state file synchronously to check for a persisted
 * `uiLanguageOverride`. This must be synchronous because it is called
 * during module evaluation, before withConfigSchematics() runs.
 *
 * Returns the override locale ID (e.g. "zh-CN") or "auto" / "" if none set.
 */
function readPersistedLocaleOverride() {
    try {
        const statePath = (0, path_1.join)(os.homedir(), ".beledarians-llm-toolbox", ".plugin_state.json");
        const raw = (0, fs_1.readFileSync)(statePath, "utf-8");
        const state = JSON.parse(raw);
        const override = state?.uiLanguageOverride;
        if (typeof override === "string" && override && override !== "auto") {
            return override;
        }
    }
    catch {
        // File doesn't exist yet or is malformed — fall through to OS detection
    }
    return "";
}
// ─────────────────────────────────────────────────────────────
// Detection
// ─────────────────────────────────────────────────────────────
/**
 * Detect the host operating system's language/locale string.
 *
 * Priority:
 *  1. Native `Intl.DateTimeFormat().resolvedOptions().locale` (reliable on Windows & macOS)
 *  2. POSIX environment variables — fallback for headless Linux / llmster daemon deployments
 *     where the Intl API may report a generic "C" or "POSIX" locale.
 */
function detectSystemLanguage() {
    // 1. Native Intl API
    try {
        const intlLocale = Intl.DateTimeFormat().resolvedOptions().locale;
        if (intlLocale && intlLocale !== "C" && intlLocale !== "POSIX" && intlLocale.length > 1) {
            return intlLocale;
        }
    }
    catch {
        // Intl not available in this environment — fall through
    }
    // 2. POSIX environment variable chain
    const posixVars = ["LC_ALL", "LANGUAGE", "LANG"];
    for (const envVar of posixVars) {
        const raw = process.env[envVar];
        if (raw && raw.length > 1 && raw !== "C" && raw !== "POSIX") {
            // Strip encoding suffix, e.g. "zh_CN.UTF-8" → "zh_CN"
            return raw.split(".")[0].replace(/_/g, "-");
        }
    }
    // 3. Safe default
    return "en";
}
// ─────────────────────────────────────────────────────────────
// Resolution (heuristic mapping → canonical locale ID)
// ─────────────────────────────────────────────────────────────
/**
 * Map a raw locale string (from Intl or env vars) to one of the plugin's supported locale IDs.
 *
 * Heuristic order matters — check more-specific variants before general prefixes.
 *
 * Sinophone routing:
 *   zh-TW, zh-HK, zh-MO, zh-Hant → "zh-TW"
 *   zh-CN, zh-Hans, zh-SG, zh     → "zh-CN"
 *
 * Germanic routing:
 *   de-*, de → "de"
 */
function resolveLocale(raw) {
    if (!raw || typeof raw !== "string")
        return "en";
    const tag = raw.toLowerCase();
    // ── Chinese – Traditional ──────────────────────────────────
    if (tag.startsWith("zh-tw") ||
        tag.startsWith("zh-hk") ||
        tag.startsWith("zh-mo") ||
        tag.startsWith("zh-hant") ||
        tag === "zh_tw" ||
        tag === "zh_hk") {
        return "zh-TW";
    }
    // ── Chinese – Simplified ───────────────────────────────────
    if (tag.startsWith("zh-cn") ||
        tag.startsWith("zh-hans") ||
        tag.startsWith("zh-sg") ||
        tag === "zh_cn" ||
        tag === "zh") {
        return "zh-CN";
    }
    // ── German ─────────────────────────────────────────────────
    if (tag.startsWith("de")) {
        return "de";
    }
    // ── Default ────────────────────────────────────────────────
    return "en";
}
// ─────────────────────────────────────────────────────────────
// Lookup
// ─────────────────────────────────────────────────────────────
/**
 * Return the locale dictionary for the given locale ID.
 * Falls back to English if the locale is unknown.
 */
function getDict(locale) {
    if (locale && LOCALES[locale]) {
        return LOCALES[locale];
    }
    return en_1.en;
}
/**
 * Convenience: detect + resolve + return the dictionary in one call.
 * Used by config.ts during Layer 1 (static boot-time) initialization.
 *
 * Priority:
 *  1. Persisted `uiLanguageOverride` from state file (set by user in config)
 *  2. OS locale detection (Intl + POSIX env vars)
 */
function getSystemDict() {
    // 1. Check for a persisted override written on a previous turn
    const persistedOverride = readPersistedLocaleOverride();
    if (persistedOverride) {
        const resolvedLocale = resolveLocale(persistedOverride);
        return { dict: getDict(resolvedLocale), resolvedLocale };
    }
    // 2. Fall back to OS detection
    const raw = detectSystemLanguage();
    const resolvedLocale = resolveLocale(raw);
    return { dict: getDict(resolvedLocale), resolvedLocale };
}
//# sourceMappingURL=i18n.js.map