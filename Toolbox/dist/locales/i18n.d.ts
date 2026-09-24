/**
 * i18n.ts — Central internationalization engine for the Beledarians LM Studio Toolbox plugin.
 *
 * Implements the "Dual-Layer Language Mechanism":
 *   Layer 1 (Config UI)   — detected once at startup from OS locale; immutable per SDK constraints.
 *   Layer 2 (Runtime)     — read dynamically per-turn from the user-selectable "messageLanguage" field.
 *
 * Supported locales: "en", "zh-CN", "zh-TW", "de"
 */
import type { LocaleDict } from "./types";
/** The canonical locale IDs this plugin exposes to users (Layer 2 dropdown). */
export declare const SUPPORTED_LOCALE_IDS: ReadonlyArray<string>;
/**
 * Detect the host operating system's language/locale string.
 *
 * Priority:
 *  1. Native `Intl.DateTimeFormat().resolvedOptions().locale` (reliable on Windows & macOS)
 *  2. POSIX environment variables — fallback for headless Linux / llmster daemon deployments
 *     where the Intl API may report a generic "C" or "POSIX" locale.
 */
export declare function detectSystemLanguage(): string;
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
export declare function resolveLocale(raw: string): string;
/**
 * Return the locale dictionary for the given locale ID.
 * Falls back to English if the locale is unknown.
 */
export declare function getDict(locale?: string): LocaleDict;
/**
 * Convenience: detect + resolve + return the dictionary in one call.
 * Used by config.ts during Layer 1 (static boot-time) initialization.
 *
 * Priority:
 *  1. Persisted `uiLanguageOverride` from state file (set by user in config)
 *  2. OS locale detection (Intl + POSIX env vars)
 */
export declare function getSystemDict(): {
    dict: LocaleDict;
    resolvedLocale: string;
};
//# sourceMappingURL=i18n.d.ts.map