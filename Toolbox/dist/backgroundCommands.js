"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.backgroundCommands = void 0;
exports.getRunningCommandsStatus = getRunningCommandsStatus;
exports.generateId = generateId;
const crypto_1 = require("crypto");
exports.backgroundCommands = new Map();
function getRunningCommandsStatus() {
    const running = Array.from(exports.backgroundCommands.values()).filter(c => c.status === "running");
    if (running.length === 0)
        return "";
    const now = Date.now();
    let statusStr = "Currently running background commands (Do not forget these are running!):\n";
    for (const cmd of running) {
        const durationSecs = Math.floor((now - cmd.startTime) / 1000);
        const durationStr = durationSecs > 60
            ? `${Math.floor(durationSecs / 60)}m ${durationSecs % 60}s`
            : `${durationSecs}s`;
        statusStr += `- ID: ${cmd.id} | Name: "${cmd.name}" | Duration: ${durationStr} | Timeout in: ${Math.floor((cmd.timeoutMs - (now - cmd.startTime)) / 1000)}s\n`;
    }
    return statusStr;
}
function generateId() {
    return (0, crypto_1.randomBytes)(8).toString("hex");
}
//# sourceMappingURL=backgroundCommands.js.map