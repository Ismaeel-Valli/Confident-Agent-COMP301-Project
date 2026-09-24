import { LayerName, LayerResult, Decision } from './verificationTypes';
export interface LayerContribution extends Pick<LayerResult, 'layer' | 'state' | 'tier' | 'weight'> {
    tier_factor: number;
    positive_contribution: number;
    signed_contribution: number;
}
export interface EWCSReport {
    task_id: string;
    ewcs: number | null;
    signed_score: number | null;
    has_incorrect_layer: boolean;
    total_applicable_weight: number;
    positive_weight: number;
    contributions: LayerContribution[];
    missing_layers: LayerName[];
    extraction_complete: boolean;
    failed_layers: LayerName[];
    unverifiable_layers: LayerName[];
    candidate_hash?: string;
    layer_results?: LayerResult[];
}
export declare class EWCSAccumulator {
    private taskId;
    private extractionComplete;
    private failed;
    private results;
    private report;
    constructor(taskId: string, extractionComplete?: boolean, failed?: LayerName[]);
    get isComplete(): boolean;
    record(r: LayerResult): void;
    finalise(): EWCSReport;
}
export declare function computeEwcs({ layer_results, task_id, extraction_complete, failed_layers }: {
    layer_results: LayerResult[];
    task_id?: string;
    extraction_complete?: boolean;
    failed_layers?: LayerName[];
}): EWCSReport;
export declare function makeDecision(report: EWCSReport, correctionAttempts?: number): Decision;
export declare function presentReport({ code, ewcs_report, decision }: {
    code: string;
    ewcs_report: EWCSReport;
    decision: Decision;
}): {
    report: string;
    decision: Decision;
    code_included: boolean;
};
//# sourceMappingURL=verificationPolicy.d.ts.map