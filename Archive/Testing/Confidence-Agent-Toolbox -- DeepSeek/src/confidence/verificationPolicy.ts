import { ALL_LAYERS, LAYER_WEIGHTS, TIER_FACTORS, LayerName, LayerResult, Decision, result, hashCode } from './verificationTypes';

export interface LayerContribution extends Pick<LayerResult, 'layer' | 'state' | 'tier' | 'weight'> {
  tier_factor: number; positive_contribution: number; signed_contribution: number;
}

export interface EWCSReport {
  task_id: string; ewcs: number | null; signed_score: number | null; has_incorrect_layer: boolean;
  total_applicable_weight: number; positive_weight: number; contributions: LayerContribution[];
  missing_layers: LayerName[]; extraction_complete: boolean; failed_layers: LayerName[];
  unverifiable_layers: LayerName[]; candidate_hash?: string;
  layer_results?: LayerResult[];
}

const round = (v: unknown): number | string => {
  if (typeof v !== 'number' || !Number.isFinite(v)) return 'undefined';
  return Math.round(v * 10000) / 10000;
};

export class EWCSAccumulator {
  private results = new Map<LayerName, LayerResult>();
  private report: EWCSReport | null = null;
  constructor(private taskId: string, private extractionComplete = false, private failed: LayerName[] = []) {}
  get isComplete() { return this.report !== null; }
  record(r: LayerResult) {
    if (this.report) throw new Error('Cannot record after finalise().');
    if (!Object.hasOwn(LAYER_WEIGHTS, r.layer)) throw new Error(`Unknown layer: ${r.layer}`);
    if (this.results.has(r.layer)) throw new Error(`Duplicate layer: ${r.layer}`);
    if (r.weight !== LAYER_WEIGHTS[r.layer]) throw new Error(`Incorrect weight for ${r.layer}`);
    if (!['verified_correct', 'verified_incorrect', 'unverifiable', 'not_applicable'].includes(r.state)) throw new Error(`Invalid state: ${r.state}`);
    if (!Object.hasOwn(TIER_FACTORS, r.tier)) throw new Error(`Invalid tier: ${r.tier}`);
    if (r.state.startsWith('verified_') && r.tier === 'none') throw new Error('Verified results require evidence.');
    if (['unverifiable', 'not_applicable'].includes(r.state) && r.tier !== 'none') throw new Error('Unverified results must use tier none.');
    this.results.set(r.layer, { ...r });
  }
  finalise(): EWCSReport {
    if (this.report) return structuredClone(this.report);
    const missing = ALL_LAYERS.filter(l => !this.results.has(l));
    const rows = ALL_LAYERS.map(l => this.results.get(l) || result(l, 'unverifiable', 'none', 'controller', 'Required layer did not report.'));
    const contributions: LayerContribution[] = rows.map(r => {
      const factor = TIER_FACTORS[r.tier];
      return { layer:r.layer, state:r.state, tier:r.tier, weight:r.weight, tier_factor:factor,
        positive_contribution: r.state === 'verified_correct' ? round(r.weight * factor) as number : 0,
        signed_contribution: r.state === 'verified_correct' ? round(r.weight * factor) as number : r.state === 'verified_incorrect' ? round(-r.weight * factor) as number : 0 };
    });
    const applicable = contributions.filter(c => c.state !== 'not_applicable');
    const total = applicable.reduce((s,c) => s+c.weight,0), positive = (round(applicable.reduce((s,c) => s+c.positive_contribution,0)) as number);
    this.report = { task_id:this.taskId, ewcs:total ? round(positive/total) as number : null,
      signed_score:total ? round(applicable.reduce((s,c) => s+c.signed_contribution,0)/total) as number : null,
      has_incorrect_layer:applicable.some(c => c.state === 'verified_incorrect'), total_applicable_weight:total,
      positive_weight:positive, contributions, missing_layers:missing, extraction_complete:this.extractionComplete,
      failed_layers:[...this.failed], unverifiable_layers:rows.filter(r => r.state === 'unverifiable').map(r => r.layer), layer_results:rows };
    return structuredClone(this.report);
  }
}

export function computeEwcs({layer_results, task_id = 'candidate', extraction_complete = false, failed_layers = []}:
  {layer_results: LayerResult[]; task_id?: string; extraction_complete?: boolean; failed_layers?: LayerName[]}): EWCSReport {
  const acc = new EWCSAccumulator(task_id, extraction_complete, failed_layers);
  for (const r of layer_results) acc.record(r);
  return acc.finalise();
}

/**
 * Decision policy (progress report section 8.1), applied in order:
 * 1. any contradiction -> correct (once), then abstain;
 * 2. missing/failed verifiers, incomplete extraction or an unresolved
 *    delivery-critical check -> abstain (the uncertainty gate);
 * 3. EWCS thresholds.
 * Layer states carry critical checks only; noncritical limits are notes in the
 * evidence and never make a layer unverifiable. Disabling the gate is only for
 * labelled exploratory sensitivity runs.
 */
export interface DecisionPolicy {uncertainty_gate: boolean; deliver_threshold: number; flag_threshold: number;}
export const POLICY_VERSION = '2026-09-25.1';
export const DEFAULT_POLICY: DecisionPolicy = Object.freeze({uncertainty_gate: true, deliver_threshold: 0.85, flag_threshold: 0.60});

export function makeDecision(report: EWCSReport, correctionAttempts = 0, policy: DecisionPolicy = DEFAULT_POLICY): Decision {
  // Recompute from contributions; never trust model-supplied score/flags.
  try {
    if (!report || !Array.isArray(report.contributions)) return 'abstain';
    const acc = new EWCSAccumulator(report.task_id);
    for (const c of report.contributions) acc.record({ ...c, evidence_source:'report', evidence_detail:'', hallucination_type:null });
    const checked = acc.finalise();
    // Safety constraint first: any contradiction forces correction.
    if (checked.has_incorrect_layer) return correctionAttempts < 1 ? 'correct' : 'abstain';
    // System integrity checks: missing or failed layers indicate a verifier
    // did not run, not that the code is uncertain. These still force abstention.
    if (!Array.isArray(report.missing_layers) || report.missing_layers.length ||
      !Array.isArray(report.failed_layers) || report.failed_layers.length || checked.missing_layers.length ||
      checked.ewcs === null || !Number.isFinite(report.ewcs) || report.ewcs !== checked.ewcs) return 'abstain';
    // Rule 2: a score cannot outweigh an unresolved critical check or missing claims.
    if (policy.uncertainty_gate !== false && (report.extraction_complete !== true || checked.unverifiable_layers.length)) return 'abstain';
    return checked.ewcs >= policy.deliver_threshold ? 'deliver' : checked.ewcs >= policy.flag_threshold ? 'deliver_with_flag' : 'abstain';
  } catch { return 'abstain'; }
}

export function presentReport({code, ewcs_report, decision, policy = DEFAULT_POLICY}: {code: string; ewcs_report: EWCSReport; decision: Decision; policy?: DecisionPolicy}) {
  // Guards for malformed tool input.
  const safeCode = typeof code === 'string' ? code : '';
  if (!ewcs_report || typeof ewcs_report !== 'object') {
    return {
      report: '### Confidence Agent Report\n\n**Decision:** abstain\n\n**Reason:** Malformed or missing EWCS report.\n\nCode withheld pending successful verification.',
      decision: 'abstain' as Decision,
      code_included: false,
    };
  }
  const show = (v: unknown) => typeof v === 'number' && Number.isFinite(v) ? round(v) : 'undefined';
  // A caller cannot override a restrictive decision by supplying 'deliver'.
  const checked = makeDecision(ewcs_report, 0, policy);
  const candidateMatches = ewcs_report.candidate_hash === hashCode(safeCode);
  const allowed = candidateMatches && ['deliver','deliver_with_flag'].includes(checked) && ['deliver','deliver_with_flag'].includes(decision);
  const actual = allowed ? checked : checked === 'correct' && decision !== 'abstain' ? 'correct' : 'abstain';
  const lines = ['### Confidence Agent Report', '', `**Decision:** ${actual}`, `**EWCS:** ${ewcs_report.ewcs ?? 'undefined (no applicable evidence)'} (signed: ${ewcs_report.signed_score ?? 'undefined'}, applicable weight: ${ewcs_report.total_applicable_weight ?? 'undefined'})`, '',
    '| Layer | State | Tier | Weight | Factor | Positive | Signed |', '|---|---|---|---|---|---|---|'];
  for (const c of Array.isArray(ewcs_report.contributions) ? ewcs_report.contributions : []) {
    if (!c || typeof c !== 'object') continue;
    lines.push(`| ${c.layer ?? '?'} | ${c.state ?? '?'} | ${c.tier ?? '?'} | ${c.weight ?? '?'} | ${c.tier_factor ?? '?'} | ${show(c.positive_contribution)} | ${show(c.signed_contribution)} |`);
  }
  lines.push('', 'Scope: API-claim and static evidence only. EWCS is not a probability of correctness. Task behavior has not been independently checked by this verifier.');
  lines.push('', `Policy ${POLICY_VERSION}: thresholds ${policy.deliver_threshold}/${policy.flag_threshold}, uncertainty gate ${policy.uncertainty_gate !== false ? 'on' : 'OFF (exploratory)'}.`);
  if (Array.isArray(ewcs_report.layer_results) && ewcs_report.layer_results.length) {
    lines.push('', 'Evidence:', '');
    for (const r of ewcs_report.layer_results) {
      if (!r || typeof r !== 'object') continue;
      const detail = typeof r.evidence_detail === 'string' ? r.evidence_detail : '(no detail)';
      lines.push(`- ${r.layer ?? '?'}: ${detail.replace(/\n/g, ' ')}`);
    }
  }
  if (Array.isArray(ewcs_report.missing_layers) && ewcs_report.missing_layers.length) lines.push('', `Missing layers: ${ewcs_report.missing_layers.join(', ')}`);
  if (Array.isArray(ewcs_report.unverifiable_layers) && ewcs_report.unverifiable_layers.length) lines.push('', `Unverifiable layers: ${ewcs_report.unverifiable_layers.join(', ')}`);
  if (!ewcs_report.extraction_complete) lines.push('', 'Extraction was incomplete or failed.');
  if (actual === 'deliver_with_flag') lines.push('', 'Flag: some checks rely on supporting static or package metadata evidence; the code was not executed.');
  if (allowed) {
    const fence = '`'.repeat(Math.max(3, ...((safeCode.match(/`+/g) || []).map(s => s.length + 1))));
    lines.push('', fence + 'python', safeCode, fence);
  } else lines.push('', 'Code withheld pending successful verification.');
  return { report:lines.join('\n'), decision:actual, code_included:allowed };
}