#!/usr/bin/env node
/**
 * Runs one Confidence Agent toolbox tool call for run_benchmark.py.
 *
 *   node tool_bridge.cjs <toolbox dir> --describe      prints {name, description} of verify_candidate
 *   node tool_bridge.cjs <toolbox dir> < request.json   request: {"name": "...", "arguments": {...}}
 *
 * The tool is the same implementation the LM Studio plugin exposes. It analyses the
 * candidate statically (claim extraction, Pyright, frozen OpenAPI evidence); the
 * candidate is never executed. The result is printed as one JSON document.
 */
const path = require('node:path');
const os = require('node:os');

const toolbox = path.resolve(process.argv[2] || '');
let tools;
try {
  const { createConfidenceAgentTools } = require(path.join(toolbox, 'dist', 'confidenceAgentTools'));
  const { createPyrightRunner } = require(path.join(toolbox, 'dist', 'pyrightRunner'));
  tools = createConfidenceAgentTools({ isEnabled: true, allowPyright: true, getWorkingDirectory: () => os.tmpdir(), runPyright: createPyrightRunner() });
} catch (e) {
  console.log(JSON.stringify({ error: `Toolbox not loadable from ${toolbox}: ${e.message}` }));
  process.exit(0);
}
const find = name => tools.find(t => t.name === name);

if (process.argv.includes('--describe')) {
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
