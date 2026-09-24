export declare const LAYER_WEIGHTS: {
    readonly interface: 3;
    readonly identifier: 3;
    readonly access_point: 4;
    readonly input_contract: 2;
    readonly output_contract: 1;
    readonly contextual: 2;
};
export type LayerName = keyof typeof LAYER_WEIGHTS;
export declare const ALL_LAYERS: LayerName[];
export declare const TIER_FACTORS: {
    readonly tier_1: 1;
    readonly tier_2: 0.8;
    readonly tier_3: 0.9;
    readonly tier_4: 0.5;
    readonly none: 0;
};
export type EvidenceTier = keyof typeof TIER_FACTORS;
export type VerificationState = 'verified_correct' | 'verified_incorrect' | 'unverifiable' | 'not_applicable';
export type Decision = 'deliver' | 'deliver_with_flag' | 'correct' | 'abstain';
export type Claim = Record<string, any>;
export interface LayerResult {
    layer: LayerName;
    state: VerificationState;
    tier: EvidenceTier;
    weight: number;
    evidence_source: string;
    evidence_detail: string;
    hallucination_type: string | null;
    claim_ids?: string[];
}
export interface Extraction {
    claims: Claim[];
    complete: boolean;
    issues: Array<{
        line: number;
        reason: string;
    }>;
    error?: string;
    candidate_hash?: string;
    unused_parameters?: Array<{
        name: string;
        line: number;
        start_character: number;
        end_character: number;
    }>;
}
export declare const hashCode: (code: string) => string;
export declare function result(layer: LayerName, state: VerificationState, tier: EvidenceTier, source: string, detail: string, kind?: string | null): LayerResult;
export declare function unknown(layer: LayerName, detail: string): LayerResult;
export declare function aggregate(layer: LayerName, rows: LayerResult[], emptyReason: string): LayerResult;
export declare const ofType: (claims: Claim[], type: string) => Claim[];
export declare function aggregateExtracted(layer: LayerName, claims: Claim[], rows: LayerResult[], emptyReason: string): LayerResult;
//# sourceMappingURL=verificationTypes.d.ts.map