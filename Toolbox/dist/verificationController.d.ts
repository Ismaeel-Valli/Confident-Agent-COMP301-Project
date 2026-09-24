import { PackageEvidence } from './packageEvidence';
import { RunPyright, PyrightResult } from './pyrightRunner';
import { EWCSReport } from './verificationPolicy';
import { Extraction, LayerResult, Decision } from './verificationTypes';
export interface VerificationRequest {
    code: string;
    spec: any;
    input_bindings?: Record<string, any>;
    task_id?: string;
}
export interface VerificationDeps {
    runPyright?: RunPyright;
    allowPyright?: boolean;
    lookupPackage?: (name: string) => Promise<PackageEvidence>;
    extract?: (p: {
        code: string;
        input_bindings?: Record<string, any>;
    }) => Promise<Extraction>;
}
export interface Verification {
    candidate_hash: string;
    spec_hash: string;
    bindings_hash: string;
    extraction: Extraction;
    layers: LayerResult[];
    ewcs_report: EWCSReport;
    decision: Decision;
    evidence: {
        packages: Record<string, PackageEvidence>;
        pyright: PyrightResult | null;
    };
}
export declare function verifyCandidate(request: VerificationRequest, deps?: VerificationDeps): Promise<Verification>;
export interface Attempt {
    code: string;
    verification: Verification;
}
export declare function runIntervention(request: VerificationRequest, deps?: VerificationDeps & {
    correct?: (context: {
        code: string;
        verification: Verification;
        spec: any;
        input_bindings: Record<string, any>;
    }) => Promise<string>;
}): Promise<{
    decision: Decision;
    delivered_code: string | null;
    report: string;
    attempts: Attempt[];
    correction_attempted: boolean;
    correction_error: string | null;
}>;
//# sourceMappingURL=verificationController.d.ts.map