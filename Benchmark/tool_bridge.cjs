#!/usr/bin/env node
/**
 * Runs one Confidence Agent toolbox tool call for run_benchmark.py.
 *
 *   node tool_bridge.cjs <toolbox dir> [--package-evidence FILE] --describe
 *   node tool_bridge.cjs <toolbox dir> [--package-evidence FILE] < request.json
 *
 * request.json: {"name": "...", "arguments": {...}}. The result is printed as one JSON
 * document. The tool is the same implementation the LM Studio plugin exposes; it analyses
 * the candidate statically (claim extraction, Pyright, frozen OpenAPI evidence) and never
 * executes it.
 *
 * --package-evidence: frozen PyPI metadata keyed by import name (for example the toolbox's
 * examples/evidence/requests-pypi-pilot.json). Imports it covers are answered from the file,
 * so the interface layer does not depend on the network during a run; any other import is
 * looked up live, with retries.
 */
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');

const argv = process.argv.slice(2);
const toolbox = path.resolve(argv[0] || '');
const evidenceArg = argv.indexOf('--package-evidence');
const evidenceFile = evidenceArg >= 0 ? argv[evidenceArg + 1] : null;

let tools;
try {
  const { createConfidenceAgentTools } = require(path.join(toolbox, 'dist', 'confidenceAgentTools'));
  const { createPyrightRunner } = require(path.join(toolbox, 'dist', 'pyrightRunner'));
  const { queryPypi } = require(path.join(toolbox, 'dist', 'packageEvidence'));
  const frozen = evidenceFile ? JSON.parse(fs.readFileSync(evidenceFile, 'utf8')) : {};
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const lookupPackage = async name => {
    if (Object.hasOwn(frozen, name)) return structuredClone(frozen[name]);
    let evidence;
    for (let attempt = 1; attempt <= 3; attempt++) {
      evidence = await queryPypi({ library_name: name });
      if (evidence.status !== 'unverifiable') return evidence;
      if (attempt < 3) await sleep(1000 * attempt);
    }
    return evidence;
  };
  tools = createConfidenceAgentTools({ isEnabled: true, allowPyright: true, getWorkingDirectory: () => os.tmpdir(),
    runPyright: createPyrightRunner(), lookupPackage });
} catch (e) {
  console.log(JSON.stringify({ error: `Toolbox not loadable from ${toolbox}: ${e.message}` }));
  process.exit(0);
}
const find = name => tools.find(t => t.name === name);

if (argv.includes('--describe')) {
  const t = find('verify_candidate');
  console.log(JSON.stringify({ name: t.name, description: t.description }));
  process.exit(0);
}

let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => { input += chunk; });
process.stdin.on('end', async () => {
  try {
    const { name, arguments: args } = JSON.parse(input);
    const t = find(name);
    const result = t ? await t.implementation(args || {}) : { error: `Unknown tool ${name}.` };
    console.log(JSON.stringify(result));
  } catch (e) {
    console.log(JSON.stringify({ error: String(e && e.message || e) }));
  }
});
