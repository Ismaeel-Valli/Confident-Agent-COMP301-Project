import { createHash } from 'crypto';
export const LAYER_WEIGHTS = { interface: 3, identifier: 3, access_point: 4, input_contract: 2, output_contract: 1, contextual: 2 } as const;
export type LayerName = keyof typeof LAYER_WEIGHTS;
export const ALL_LAYERS = Object.keys(LAYER_WEIGHTS) as LayerName[];
export const TIER_FACTORS = { tier_1: 1, tier_2: 0.8, tier_3: 0.9, tier_4: 0.5, none: 0 } as const;
export type EvidenceTier = keyof typeof TIER_FACTORS;
export type VerificationState = 'verified_correct' | 'verified_incorrect' | 'unverifiable' | 'not_applicable';
export type Decision = 'deliver' | 'deliver_with_flag' | 'correct' | 'abstain';
export type Claim = Record<string, any>;
export interface LayerResult {
  layer: LayerName; state: VerificationState; tier: EvidenceTier; weight: number;
  evidence_source: string; evidence_detail: string; hallucination_type: string | null;
  claim_ids?: string[];
}
export interface Extraction { claims: Claim[]; complete: boolean; issues: Array<{line: number; reason: string}>; error?: string; candidate_hash?: string;
  unused_parameters?: Array<{name:string;line:number;start_character:number;end_character:number}>; }
export const hashCode = (code: string) => createHash('sha256').update(code).digest('hex');
export function result(layer: LayerName, state: VerificationState, tier: EvidenceTier, source: string, detail: string, kind: string | null = null): LayerResult {
  return { layer, state, tier, weight: LAYER_WEIGHTS[layer], evidence_source: source, evidence_detail: detail, hallucination_type: kind };
}
export function unknown(layer: LayerName, detail: string): LayerResult { return result(layer, 'unverifiable', 'none', 'verification', detail); }
export function aggregate(layer: LayerName, rows: LayerResult[], emptyReason: string): LayerResult {
  const applicable = rows.filter(r => r.state !== 'not_applicable');
  if (!applicable.length) return result(layer, 'not_applicable', 'none', 'extraction / specification', rows.length ? rows.map(r=>r.evidence_detail).join('\n') : emptyReason);
  const incorrect = applicable.filter(r => r.state === 'verified_incorrect');
  const unresolved = applicable.filter(r => r.state === 'unverifiable');
  const selected = incorrect.length ? incorrect.sort((a,b) => TIER_FACTORS[b.tier] - TIER_FACTORS[a.tier])[0]
    : unresolved.length ? unresolved[0] : applicable.sort((a,b) => TIER_FACTORS[a.tier] - TIER_FACTORS[b.tier])[0];
  return { ...selected, evidence_detail: rows.map(r => r.evidence_detail).join('\n'), claim_ids: rows.flatMap(r => r.claim_ids || []) };
}
export const ofType = (claims: Claim[], type: string) => claims.filter(c => c.type === type);

export function aggregateExtracted(layer: LayerName, claims: Claim[], rows: LayerResult[], emptyReason: string): LayerResult {
  const r = aggregate(layer, rows, emptyReason);
  const relevant: Record<LayerName,string[]> = {interface:['import'],identifier:['method_call'],access_point:['endpoint'],input_contract:['endpoint','input_field'],output_contract:['output_field'],contextual:['endpoint','input_field']};
  r.claim_ids = claims.filter(c=>relevant[layer].includes(c.type) && typeof c.id==='string').map(c=>c.id);
  if (claims.some(c => c.type === 'extraction_issue') && ['verified_correct','not_applicable'].includes(r.state)) {
    // Registry evidence for explicit imports is independent of whether response flow is
    // supported. Retain that evidence; do not claim that the import inventory is exhaustive.
    // The controller's extraction_complete gate still prohibits delivery.
    if (layer === 'interface' && r.state === 'verified_correct') {
      return {...r, evidence_detail:r.evidence_detail + '\nEvidence covers the extracted imports only. Extraction is incomplete; additional claims may be missing and delivery remains blocked.'};
    }
    return unknown(layer, 'Extraction is incomplete; unsupported claims may be missing. ' + r.evidence_detail);
  }
  return r;
}
