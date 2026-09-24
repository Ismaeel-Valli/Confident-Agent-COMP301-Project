import { ChildProcess } from "child_process";
export interface BackgroundCommand {
    id: string;
    name: string;
    startTime: number;
    process: ChildProcess;
    timeoutMs: number;
    stdout: string;
    stderr: string;
    status: "running" | "completed" | "error" | "cancelled" | "timeout";
    exitCode?: number | null;
    timeoutHandle?: NodeJS.Timeout;
}
export declare const backgroundCommands: Map<string, BackgroundCommand>;
export declare function getRunningCommandsStatus(): string;
export declare function generateId(): string;
//# sourceMappingURL=backgroundCommands.d.ts.map