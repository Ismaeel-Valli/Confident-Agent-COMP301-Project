export type ParsedToolCall = {
    tool: string;
    args: Record<string, any>;
};
export type ParsedSubAgentMessage = {
    content: string;
    toolCall: ParsedToolCall | null;
    toolCallSource: "tool_calls" | "content" | "reasoning" | "none";
};
export declare function parseSubAgentResponseMessage(message: unknown): ParsedSubAgentMessage;
//# sourceMappingURL=subAgentToolCallParser.d.ts.map