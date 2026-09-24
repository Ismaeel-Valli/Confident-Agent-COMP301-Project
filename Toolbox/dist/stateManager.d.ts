export interface PluginState {
    currentWorkingDirectory: string;
    messageCount: number;
    dontAskToCompress: boolean;
    subAgentDocsInjected: boolean;
    /** Locale ID to use for Layer 1 (Config UI) on next plugin restart. "auto" = OS detection. */
    uiLanguageOverride: string;
}
export declare function getPersistedState(configuredWorkspacePath?: string): Promise<PluginState>;
export declare function savePersistedState(state: PluginState): Promise<void>;
export declare function ensureWorkspaceExists(path: string): Promise<void>;
//# sourceMappingURL=stateManager.d.ts.map