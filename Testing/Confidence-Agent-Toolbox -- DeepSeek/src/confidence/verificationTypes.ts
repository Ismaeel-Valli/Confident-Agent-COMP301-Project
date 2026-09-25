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
export interface UnusedParameter {
  name: string;
  line: number;
  start_character: number;
  end_character: number;
}
export interface Extraction {
  claims: Claim[];
  complete: boolean;
  issues: Array<{line: number; reason: string; affects?: string[]}>;
  unused_parameters?: UnusedParameter[];
  error?: string;
  candidate_hash?: string;
}
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

/**
 * Layers whose claim inventory an extraction limitation can make incomplete.
 * Each extractor issue names the layers it affects; an issue without that
 * information, or an extraction error, conservatively affects every layer.
 */
export function extractionLimits(source: Claim[] | Extraction): {layers: Set<LayerName>; reasons: string[]} {
  const layers = new Set<LayerName>(), reasons: string[] = [];
  const records: Array<{issues?: any[]; error?: any}> = Array.isArray(source)
    ? source.filter(c => c.type === 'extraction_issue')
    : (source.error || !source.complete ? [{issues: source.issues, error: source.error ?? (source.issues?.length ? undefined : 'Extraction incomplete.')}] : []);
  for (const record of records) {
    if (record.error) { ALL_LAYERS.forEach(l => layers.add(l)); reasons.push(String(record.error)); }
    for (const i of record.issues || []) {
      const affects = Array.isArray(i?.affects) && i.affects.length ? i.affects : ALL_LAYERS;
      for (const l of affects) if ((ALL_LAYERS as string[]).includes(l)) layers.add(l as LayerName);
      reasons.push(`line ${i?.line ?? '?'}: ${i?.reason ?? 'unsupported construct'}`);
    }
    if (!record.error && !(record.issues || []).length) ALL_LAYERS.forEach(l => layers.add(l));
  }
  return {layers, reasons};
}

export function aggregateExtracted(layer: LayerName, claims: Claim[], rows: LayerResult[], emptyReason: string): LayerResult {
  const r = aggregate(layer, rows, emptyReason);
  const relevant: Record<LayerName,string[]> = {interface:['import'],identifier:['method_call'],access_point:['endpoint'],input_contract:['endpoint','input_field'],output_contract:['output_field'],contextual:['endpoint','input_field']};
  r.claim_ids = claims.filter(c=>relevant[layer].includes(c.type) && typeof c.id==='string').map(c=>c.id);
  const limits = extractionLimits(claims);
  // A limitation that can hide claims of this layer means neither a positive
  // result nor "nothing to check" is established. Contradictions still stand.
  if (limits.layers.has(layer) && (r.state === 'verified_correct' || r.state === 'not_applicable')) {
    return {...unknown(layer, `Extraction is incomplete for this layer; unsupported claims may be missing (${limits.reasons.join('; ')}). ` + r.evidence_detail), claim_ids: r.claim_ids};
  }
  if (limits.reasons.length && !limits.layers.has(layer)) {
    r.evidence_detail += `\nExtraction limitations elsewhere do not affect this layer; evidence covers the extracted ${layer === 'interface' ? 'imports' : 'claims'} only.`;
  }
  return r;
}