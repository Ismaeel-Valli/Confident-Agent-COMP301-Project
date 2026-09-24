"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.extractHandoffMessage = extractHandoffMessage;
function extractHandoffMessage(rawContent) {
    const markerRegex = /\[HANDOFF_MESSAGE\]([\s\S]*?)\[\/HANDOFF_MESSAGE\]/i;
    const markerMatch = rawContent.match(markerRegex);
    if (markerMatch) {
        const handoff = markerMatch[1].trim();
        const response = rawContent.replace(markerRegex, "").trim();
        return {
            response,
            handoffMessage: handoff || undefined,
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
            if (!parsed || typeof parsed !== "object")
                continue;
            const handoff = typeof parsed.handoff_message === "string"
                ? parsed.handoff_message.trim()
                : "";
            if (!handoff)
                continue;
            const explicitResponse = typeof parsed.response === "string"
                ? parsed.response.trim()
                : typeof parsed.final_response === "string"
                    ? parsed.final_response.trim()
                    : "";
            let response = explicitResponse;
            if (!response && candidate.fullMatch) {
                response = rawContent.replace(candidate.fullMatch, "").trim();
            }
            if (!response && !candidate.fullMatch) {
                response = "";
            }
            return {
                response,
                handoffMessage: handoff,
            };
        }
        catch {
            // Not valid JSON; continue scanning.
        }
    }
    return { response: rawContent };
}
//# sourceMappingURL=handoffMessage.js.map