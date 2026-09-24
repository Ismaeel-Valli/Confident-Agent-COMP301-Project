import { type LayerResult, type Extraction } from './verificationTypes';
export interface Diagnostic {
    severity: string;
    message: string;
    rule?: string;
    range?: any;
    file?: string;
}
export interface PyrightResult {
    stdout: string;
    stderr: string;
    exit_code: number | null;
    signal?: string | null;
    timed_out?: boolean;
    error?: string;
    candidate_hash?: string;
    python_executable?: string;
    checker_version?: string;
    diagnostics?: Diagnostic[];
    summary?: Record<string, any>;
}
export type RunPyright = (p: {
    python: string;
    timeout_seconds?: number;
}) => Promise<PyrightResult>;
export declare function createPyrightRunner(): RunPyright;
export declare function parsePyright(r: PyrightResult, code: string): {
    diagnostics: Diagnostic[];
    error?: string;
};
export declare function verifyIdentifier(code: string, runPyright: RunPyright, allowPyright?: boolean, extraction?: Extraction): Promise<LayerResult>;
//# sourceMappingURL=pyrightRunner.d.ts.map