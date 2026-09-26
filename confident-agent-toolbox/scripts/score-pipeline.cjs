#!/usr/bin/env node
/**
 * Scores a run-pipeline.cjs output folder against the benchmark's expected requests.
 *
 * Independent answer key: test_case.expected_request (method, URL, query, JSON body,
 * Authorization) from the dataset. The final candidate of each task is re-extracted
 * statically with the task's test inputs bound to `inputs`; nothing is executed.
 *
 * Request verdict:
 *   right         the method is one of api_specification.acceptable_methods; URL, query and
 *                 JSON body equal the expected request (extra query parameters are allowed
 *                 only when api_specification documents them); the Authorization header
 *                 matches when one is expected
 *   wrong         at least one statically known part differs
 *   undetermined  no known part differs, but some part depends on a condition or value
 *                 the static extraction cannot evaluate
 * Non-credential headers (Accept, Content-Type, API-version headers) are not compared.
 * Response handling (which field is returned) is task behaviour, reported separately.
 *
 * Usage: node scripts/score-pipeline.cjs <run folder> [--dataset PATH] [--out table.md]
 */
const fs = require('node:fs');
const path = require('node:path');
const { parseArgs } = require('node:util');
const { extractClaims } = require('../dist/claimExtractor');

const root = path.join(__dirname, '..');
const { values, positionals } = parseArgs({ allowPositionals: true, options: {
  dataset: { type: 'string', default: path.join(root, '../COMP301-Dataset-Builder/comp301-dataset-builder/output/rest_api_tasks_v1_DRAFT.jsonl') },
  out: { type: 'string' },
} });
const runDir = positionals[0];
if (!runDir) { console.error('Usage: node scripts/score-pipeline.cjs <run folder>'); process.exit(2); }

const isMarker = (v, kind) => v && typeof v === 'object' && !Array.isArray(v) && v.$ca === kind;
const UNKNOWN = Symbol('unknown');
/** Value as requests would serialize a query value; UNKNOWN when not statically known. */
function queryText(v) {
  if (isMarker(v, 'unknown') || isMarker(v, 'template')) return UNKNOWN;
  if (Array.isArray(v)) { const items = v.map(queryText); return items.includes(UNKNOWN) ? UNKNOWN : items; }
  if (typeof v === 'boolean') return v ? 'True' : 'False';
  if (v === null || v === undefined) return null;
  return typeof v === 'object' ? UNKNOWN : String(v);
}
/** Compare a candidate value with an expected one: 'same' | 'differs' | 'unknown'. */
function compare(actual, expected) {
  if (isMarker(actual, 'maybe')) return compare(actual.value, expected);
  if (isMarker(actual, 'unknown') || isMarker(actual, 'template')) return 'unknown';
  if (Array.isArray(expected)) {
    if (!Array.isArray(actual) || actual.length !== expected.length) return 'differs';
    return merge(actual.map((a, i) => compare(a, expected[i])));
  }
  if (expected && typeof expected === 'object') {
    if (!actual || typeof actual !== 'object' || Array.isArray(actual)) return 'differs';
    return compareFields(actual, expected);
  }
  return actual === expected || (typeof actual === 'number' && String(actual) === String(expected)) ? 'same' : 'differs';
}
function compareFields(actual, expected, text = false) {
  const results = [];
  for (const key of new Set([...Object.keys(actual), ...Object.keys(expected)])) {
    const has = Object.hasOwn(actual, key), want = Object.hasOwn(expected, key);
    if (has && !want) results.push(isMarker(actual[key], 'maybe') ? 'unknown' : 'differs');
    else if (!has && want) results.push('differs');
    else if (text) {
      const a = queryText(isMarker(actual[key], 'maybe') ? actual[key].value : actual[key]), e = queryText(expected[key]);
      results.push(a === UNKNOWN ? 'unknown' : JSON.stringify(a) === JSON.stringify(e) ? 'same' : 'differs');
    } else results.push(compare(actual[key], expected[key]));
  }
  return merge(results);
}
const merge = rs => rs.includes('differs') ? 'differs' : rs.includes('unknown') ? 'unknown' : 'same';
const shape = entry => entry?.provided ? (Object.hasOwn(entry, 'shape') ? entry.shape : entry.value) : undefined;

function judgeRequest(claims, complete, expected, api) {
  const methods = api.acceptable_methods?.length ? api.acceptable_methods : [expected.method];
  const documented = new Set((api.parameters || []).filter(p => p.in === 'query').map(p => p.name));
  const endpoints = claims.filter(c => c.type === 'endpoint');
  if (!endpoints.length) return { verdict: complete ? 'wrong' : 'undetermined', why: 'no HTTP request extracted' };
  const want = new URL(expected.url), wantPath = want.origin + want.pathname.replace(/\/$/, '');
  const verdicts = endpoints.map(ep => {
    if (typeof ep.endpoint !== 'string' || typeof ep.http_method !== 'string') return { verdict: 'undetermined', why: 'URL or method is dynamic' };
    let url; try { url = new URL(ep.endpoint); } catch { return { verdict: 'wrong', why: `invalid URL ${ep.endpoint}` }; }
    const diffs = [], unknowns = [], notes = [];
    if (!methods.includes(ep.http_method)) diffs.push(`method ${ep.http_method} (acceptable: ${methods.join(', ')})`);
    const got = url.origin + url.pathname.replace(/\/$/, '');
    if (got !== wantPath) diffs.push(`URL ${got} (expected ${wantPath})`);
    // Query: parameters in the URL string plus params=.
    const params = shape(ep.request?.params);
    const query = Object.fromEntries(url.searchParams);
    if (params !== undefined && params !== null) {
      if (typeof params !== 'object' || Array.isArray(params) || isMarker(params, 'unknown')) unknowns.push('params is dynamic');
      else Object.assign(query, params);
    }
    // Extra parameters the task's specification documents are optional choices, not errors.
    const allowed = Object.keys(query).filter(k => !Object.hasOwn(expected.query || {}, k) && documented.has(k));
    for (const k of allowed) delete query[k];
    const q = compareFields(query, expected.query || {}, true);
    if (q === 'differs') diffs.push(`query ${JSON.stringify(query)} (expected ${JSON.stringify(expected.query)})`);
    else if (q === 'unknown') unknowns.push('query value or presence is conditional/dynamic');
    if (allowed.length) notes.push(`documented optional parameter(s) ${allowed.join(', ')}`);
    // JSON body.
    const body = shape(ep.request?.json), form = shape(ep.request?.data);
    if (form !== undefined && form !== null) diffs.push('sends a form/raw body');
    if (expected.json_body == null) { if (body !== undefined && body !== null) diffs.push('sends a JSON body (none expected)'); }
    else if (body === undefined || body === null) diffs.push('JSON body missing');
    else {
      const b = compare(body, expected.json_body);
      if (b === 'differs') diffs.push(`body ${JSON.stringify(body)} (expected ${JSON.stringify(expected.json_body)})`);
      else if (b === 'unknown') unknowns.push('body is partly dynamic');
    }
    // Credential.
    const wantAuth = Object.entries(expected.headers || {}).find(([k]) => k.toLowerCase() === 'authorization')?.[1];
    if (wantAuth !== undefined) {
      const headers = shape(ep.request?.headers);
      if (!headers || typeof headers !== 'object' || isMarker(headers, 'unknown')) unknowns.push('headers are dynamic');
      else {
        const got = Object.entries(headers).find(([k]) => k.toLowerCase() === 'authorization')?.[1];
        const c = got === undefined ? (ep.request?.auth?.provided ? 'unknown' : 'differs') : compare(got, wantAuth);
        if (c === 'differs') diffs.push(`Authorization ${JSON.stringify(got ?? null)} (expected ${JSON.stringify(wantAuth)})`);
        else if (c === 'unknown') unknowns.push('Authorization is dynamic');
      }
    }
    return diffs.length ? { verdict: 'wrong', why: diffs.join('; ') } : unknowns.length ? { verdict: 'undetermined', why: unknowns.join('; ') } : { verdict: 'right', why: notes.join('; ') };
  });
  // A candidate is right when one extracted request matches; several requests are reported.
  const pick = verdicts.find(v => v.verdict === 'right') || verdicts.find(v => v.verdict === 'undetermined') || verdicts[0];
  return endpoints.length > 1 ? { ...pick, why: `${pick.why}${pick.why ? '; ' : ''}${endpoints.length} requests extracted` } : pick;
}

async function main() {
  const tasks = new Map(fs.readFileSync(values.dataset, 'utf8').split('\n').filter(Boolean).map(l => { const t = JSON.parse(l); return [t.task_id, t]; }));
  const rows = [];
  for (const id of fs.readdirSync(runDir).filter(d => fs.existsSync(path.join(runDir, d, 'audit.json'))).sort()) {
    const audit = JSON.parse(fs.readFileSync(path.join(runDir, id, 'audit.json'), 'utf8')), task = tasks.get(id);
    // A correction that echoed the JSON request is rejected by the current pipeline, which
    // then keeps the first candidate; score what the pipeline now withholds or delivers.
    const last = audit.attempts[audit.attempts.length - 1].code;
    const code = audit.attempts.length > 1 && /^\s*[{[]/.test(last) ? audit.attempts[0].code : last;
    const ex = await extractClaims({ code, input_bindings: { inputs: task.test_case.inputs } });
    const request = judgeRequest(ex.claims || [], ex.complete === true, task.test_case.expected_request, task.api_specification);
    const field = task.test_case.expected_output?.field;
    const reads = (ex.claims || []).filter(c => c.type === 'output_field').map(c => (c.path || []).join('.'));
    const outputNote = field && !reads.includes(field) ? `does not read expected response field ${field}` : '';
    const delivered = ['deliver', 'deliver_with_flag'].includes(audit.decision);
    const outcome = request.verdict === 'undetermined' ? 'undetermined'
      : request.verdict === 'right' ? (delivered ? 'correct delivery' : 'false abstention')
      : (delivered ? 'false delivery' : 'correct abstention');
    rows.push({ id, api: task.api_specification.api_name, decision: audit.decision, corrected: audit.attempts.length > 1, outcome, why: request.why, outputNote });
  }
  const order = ['correct abstention', 'false abstention', 'false delivery', 'correct delivery', 'undetermined'];
  const count = (list, o) => list.filter(r => r.outcome === o).length;
  const apis = [...new Set(rows.map(r => r.api))];
  const lines = [`# Pipeline outcomes against expected requests: ${path.basename(path.resolve(runDir))}`, '',
    `| API | ${order.join(' | ')} |`, `|---|${order.map(() => '---:').join('|')}|`,
    ...apis.map(a => `| ${a} | ${order.map(o => count(rows.filter(r => r.api === a), o)).join(' | ')} |`),
    `| **All (${rows.length})** | ${order.map(o => `**${count(rows, o)}**`).join(' | ')} |`, '',
    '| Task | Decision | Outcome | Request differences / limits | Response handling |', '|---|---|---|---|---|',
    ...rows.map(r => `| ${r.id} | ${r.decision}${r.corrected ? ' (after correction)' : ''} | ${r.outcome} | ${(r.why || '-').replace(/\|/g, '\\|')} | ${r.outputNote || '-'} |`)];
  const text = lines.join('\n') + '\n';
  if (values.out) fs.writeFileSync(values.out, text);
  console.log(text);
}
main().catch(e => { console.error(e); process.exitCode = 1; });
