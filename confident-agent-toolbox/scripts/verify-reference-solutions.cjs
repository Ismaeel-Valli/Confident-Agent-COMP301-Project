#!/usr/bin/env node
/**
 * Verifier regression check over the benchmark's reference solutions.
 *
 * Engineering validation only: reference code is the evaluator's artefact and is
 * used here as a known-valid candidate set, plus deliberately mutated variants
 * that must never be delivered. These results are not hallucination measurements
 * and must not be reported as such. Evidence is selected from the host named in
 * the candidate code (never from task metadata) via evidence/registry.json.
 *
 * Usage (after `npm run build`):
 *   node scripts/verify-reference-solutions.cjs [--dataset PATH] [--per-api 25|0] [--mutants]
 *     [--pyright off] [--jobs 6] [--out verification-runs/references.json]
 */
const fs = require('node:fs');
const path = require('node:path');
const { parseArgs } = require('node:util');
const { verifyCandidate } = require('../dist/verificationController');
const { createPyrightRunner } = require('../dist/pyrightRunner');

const root = path.join(__dirname, '..');
const { values } = parseArgs({ options: {
  dataset: { type: 'string', default: path.join(root, '../COMP301-Dataset-Builder/comp301-dataset-builder/output/rest_api_tasks_v1_DRAFT.jsonl') },
  'per-api': { type: 'string', default: '25' }, mutants: { type: 'boolean', default: false },
  pyright: { type: 'string', default: 'on' }, jobs: { type: 'string', default: '6' },
  'package-evidence': { type: 'string', default: path.join(root, 'examples/evidence/requests-pypi-pilot.json') },
  out: { type: 'string', default: path.join(root, 'verification-runs', `references-${Date.now()}.json`) },
} });

if (!fs.existsSync(values.dataset)) {
  console.error(`Dataset not found: ${values.dataset}
Pass --dataset path/to/rest_api_tasks_v1_DRAFT.jsonl (from COMP301-Dataset-Builder).`);
  process.exit(2);
}
const registry = JSON.parse(fs.readFileSync(path.join(root, 'evidence/registry.json'), 'utf8'));
const sourcesDir = path.resolve(root, 'evidence', registry.sources_dir);
const specCache = new Map();
function evidenceFor(code) {
  const host = /https?:\/\/([^/'"\s?#{]+)/.exec(code)?.[1];
  const entry = Object.entries(registry.providers).find(([, p]) => p.hosts.includes(host));
  if (!entry) return { provider: null, spec: null };
  const [provider, p] = entry;
  if (!specCache.has(provider)) {
    const spec = JSON.parse(fs.readFileSync(path.join(sourcesDir, p.spec), 'utf8'));
    spec['x-confidence-evidence'] = { ...(spec['x-confidence-evidence'] || {}), ...p.overlay, snapshot: p.spec };
    specCache.set(provider, spec);
  }
  return { provider, spec: specCache.get(provider) };
}

const tasks = fs.readFileSync(values.dataset, 'utf8').split('\n').filter(Boolean).map(l => JSON.parse(l));
const perApi = Number(values['per-api']);
const byApi = new Map();
for (const t of tasks) { const k = t.api_specification.api_name; if (!byApi.has(k)) byApi.set(k, []); byApi.get(k).push(t); }
const selected = [];
for (const list of byApi.values()) {
  if (!perApi) { selected.push(...list); continue; }
  const stride = Math.max(1, Math.floor(list.length / perApi));
  for (let i = 0; i < list.length && selected.filter(s => s.api_specification.api_name === list[0].api_specification.api_name).length < perApi; i += stride) selected.push(list[i]);
}

const METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'];
function mutants(task, spec) {
  const code = task.ground_truth.code, base = task.api_specification.base_url, out = [];
  if (code.includes(base)) {
    out.push({ kind: 'invented_path', code: code.replace(base, base + '/zz-invented-segment') });
    out.push({ kind: 'wrong_host', code: code.replace(new URL(base).host, 'api.invented-host.example') });
  }
  const declared = Object.keys(spec?.paths?.[task.api_specification.endpoint] || {}).map(m => m.toUpperCase());
  const method = METHODS.find(m => !declared.includes(m));
  const current = task.api_specification.method;
  if (method && code.includes(`requests.request('${current}'`)) out.push({ kind: 'undeclared_method', code: code.replace(`requests.request('${current}'`, `requests.request('${method}'`) });
  return out;
}

const packages = JSON.parse(fs.readFileSync(values['package-evidence'], 'utf8'));
const deps = {
  lookupPackage: async name => structuredClone(packages[name] || { exists: null, status: 'unverifiable', summary: 'Import absent from frozen package evidence.' }),
  runPyright: values.pyright === 'off' ? async () => ({ stdout: '', stderr: '', exit_code: null, error: 'Pyright disabled for this run.' }) : createPyrightRunner(),
};

async function verify(task, kind, code) {
  const { provider, spec } = evidenceFor(code);
  const v = await verifyCandidate({ code, spec, task_id: `${task.task_id}:${kind}` }, deps);
  return { task_id: task.task_id, api: task.api_specification.api_name, kind, provider, ewcs: v.ewcs_report.ewcs, decision: v.decision,
    extraction_complete: v.extraction.complete, issues: v.extraction.issues.map(i => i.reason),
    layers: v.layers.map(l => ({ layer: l.layer, state: l.state, tier: l.tier, detail: l.evidence_detail })) };
}

(async () => {
  const jobs = [];
  for (const t of selected) {
    jobs.push([t, 'reference', t.ground_truth.code]);
    if (values.mutants) for (const m of mutants(t, evidenceFor(t.ground_truth.code).spec)) jobs.push([t, m.kind, m.code]);
  }
  const results = []; let next = 0;
  await Promise.all(Array.from({ length: Number(values.jobs) }, async () => { while (next < jobs.length) { const j = jobs[next++]; results.push(await verify(...j)); } }));
  results.sort((a, b) => (a.task_id + a.kind).localeCompare(b.task_id + b.kind));
  fs.mkdirSync(path.dirname(values.out), { recursive: true });
  fs.writeFileSync(values.out, JSON.stringify(results, null, 1));

  const short = { verified_correct: 'OK', verified_incorrect: 'BAD', unverifiable: 'UNV', not_applicable: 'N/A' };
  const count = (rows, f) => rows.reduce((m, r) => { const k = f(r); m[k] = (m[k] || 0) + 1; return m; }, {});
  const refs = results.filter(r => r.kind === 'reference');
  console.log(`Reference solutions: ${refs.length} (pyright ${values.pyright})`);
  for (const api of [...new Set(refs.map(r => r.api)), 'ALL']) {
    const rows = refs.filter(r => api === 'ALL' || r.api === api);
    const mean = rows.reduce((s, r) => s + (r.ewcs ?? 0), 0) / rows.length;
    console.log(`  ${api.padEnd(16)} n=${String(rows.length).padStart(4)} meanEWCS=${mean.toFixed(3)} decisions=${JSON.stringify(count(rows, r => r.decision))}`);
    console.log(`  ${''.padEnd(16)} ` + ['interface', 'identifier', 'access_point', 'input_contract', 'output_contract', 'contextual']
      .map(l => `${l.slice(0, 6)} ${Object.entries(count(rows, r => short[r.layers.find(x => x.layer === l).state])).map(([k, v]) => k + ':' + v).join(',')}`).join(' | '));
  }
  const reasons = {};
  for (const r of refs) for (const l of r.layers) if (l.state === 'unverifiable' || l.state === 'verified_incorrect') {
    const k = `${l.layer} ${short[l.state]}: ${l.detail.split('\n')[0].slice(0, 140)}`; reasons[k] = (reasons[k] || 0) + 1;
  }
  const top = Object.entries(reasons).sort((a, b) => b[1] - a[1]).slice(0, 15);
  if (top.length) { console.log('\nMost frequent unresolved/contradicted reference checks:'); for (const [k, v] of top) console.log(`  ${String(v).padStart(4)}  ${k}`); }
  if (values.mutants) {
    console.log('\nMutants (must never be delivered):');
    for (const kind of [...new Set(results.filter(r => r.kind !== 'reference').map(r => r.kind))]) {
      const rows = results.filter(r => r.kind === kind);
      const delivered = rows.filter(r => r.decision.startsWith('deliver'));
      console.log(`  ${kind.padEnd(18)} n=${String(rows.length).padStart(4)} decisions=${JSON.stringify(count(rows, r => r.decision))}${delivered.length ? '  DELIVERED: ' + delivered.map(r => r.task_id).join(',') : ''}`);
    }
  }
  console.log(`\nSaved: ${values.out}`);
})().catch(e => { console.error(e); process.exitCode = 1; });
