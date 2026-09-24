import { type ChatMessage, type PromptPreprocessorController } from "@lmstudio/sdk";
export declare function getSubAgentDocsCandidatePaths(currentWorkingDirectory: string): string[];
export declare function promptPreprocessor(ctl: PromptPreprocessorController, userMessage: ChatMessage): Promise<string | ChatMessage>;
//# sourceMappingURL=promptPreprocessor.d.ts.map