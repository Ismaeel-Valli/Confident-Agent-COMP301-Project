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
const round = (v: number) => Math.round(v * 10000) / 10000;
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
        positive_contribution: r.state === 'verified_correct' ? round(r.weight * factor) : 0,
        signed_contribution: r.state === 'verified_correct' ? round(r.weight * factor) : r.state === 'verified_incorrect' ? round(-r.weight * factor) : 0 };
    });
    const applicable = contributions.filter(c => c.state !== 'not_applicable');
    const total = applicable.reduce((s,c) => s+c.weight,0), positive = round(applicable.reduce((s,c) => s+c.positive_contribution,0));
    this.report = { task_id:this.taskId, ewcs:total ? round(positive/total) : null,
      signed_score:total ? round(applicable.reduce((s,c) => s+c.signed_contribution,0)/total) : null,
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
export function makeDecision(report: EWCSReport, correctionAttempts = 0): Decision {
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
    // Unverifiable layers and incomplete extraction are findings, not
    // system failures. They already reduce the EWCS via the denominator.
    // The thresholds now decide, not a hard gate.
    return checked.ewcs >= 0.85 ? 'deliver' : checked.ewcs >= 0.60 ? 'deliver_with_flag' : 'abstain';
  } catch { return 'abstain'; }
}
export function presentReport({code, ewcs_report, decision}: {code: string; ewcs_report: EWCSReport; decision: Decision}) {
  // A caller cannot override a restrictive decision by supplying 'deliver'.
  const checked = makeDecision(ewcs_report);
  const candidateMatches = ewcs_report.candidate_hash === hashCode(code);
  const allowed = candidateMatches && ['deliver','deliver_with_flag'].includes(checked) && ['deliver','deliver_with_flag'].includes(decision);
  const actual = allowed ? checked : checked === 'correct' && decision !== 'abstain' ? 'correct' : 'abstain';
  const lines = ['### Confidence Agent Report', '', `**Decision:** ${actual}`, `**EWCS:** ${ewcs_report.ewcs ?? 'undefined (no applicable evidence)'} (signed: ${ewcs_report.signed_score ?? 'undefined'}, applicable weight: ${ewcs_report.total_applicable_weight})`, '',
    '| Layer | State | Tier | Weight | Factor | Positive | Signed |', '|---|---|---|---|---|---|---|'];
  for (const c of ewcs_report.contributions || []) lines.push(`| ${c.layer} | ${c.state} | ${c.tier} | ${c.weight} | ${c.tier_factor} | ${round(c.positive_contribution)} | ${round(c.signed_contribution)} |`);
  lines.push('', 'Scope: API-claim and static evidence only. EWCS is not a probability of correctness. Task behavior has not been independently checked by this verifier.');
  if (ewcs_report.layer_results?.length) {
    lines.push('', 'Evidence:', '');
    for (const r of ewcs_report.layer_results) lines.push(`- ${r.layer}: ${r.evidence_detail.replace(/\n/g, ' ')}`);
  }
  if (ewcs_report.missing_layers?.length) lines.push('', `Missing layers: ${ewcs_report.missing_layers.join(', ')}`);
  if (ewcs_report.unverifiable_layers?.length) lines.push('', `Unverifiable layers: ${ewcs_report.unverifiable_layers.join(', ')}`);
  if (!ewcs_report.extraction_complete) lines.push('', 'Extraction was incomplete or failed.');
  if (actual === 'deliver_with_flag') lines.push('', 'Flag: some checks rely on supporting static or package metadata evidence; the code was not executed.');
  if (allowed) {
    // Use a fence longer than any candidate run of backticks.
    const fence = '`'.repeat(Math.max(3, ...((code.match(/`+/g) || []).map(s => s.length + 1))));
    lines.push('', fence + 'python', code, fence);
  } else lines.push('', 'Code withheld pending successful verification.');
  return { report:lines.join('\n'), decision:actual, code_included:allowed };
}