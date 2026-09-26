// Plugin surface: which tools the model can see, settings, and the retained Pyright tool.
const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const os=require('node:os');
const path=require('node:path');
const {toolsProvider,resolveWorkspace,DEFAULT_WORKSPACE}=require('../dist/toolsProvider');

const VERIFICATION_TOOLS=['verify_candidate','resolve_api_spec','query_pypi','extract_claims','verify_interface','verify_identifier',
  'verify_access_point','verify_input_contract','verify_output_contract','verify_contextual','compute_ewcs','make_decision','save_code','present_report'];
const workspace=fs.mkdtempSync(path.join(os.tmpdir(),'cat-workspace-'));
const provider=overrides=>toolsProvider({getPluginConfig:()=>({get:key=>({enableConfidenceAgentTools:true,allowPyrightExecution:true,
  pythonExecutable:'',workspacePath:workspace,...overrides})[key]})});

test('the model sees exactly run_pyright and the verification tools',async()=>{
 const names=(await provider()).map(t=>t.name).sort();
 assert.deepEqual(names,['run_pyright',...VERIFICATION_TOOLS].sort());
 for(const removed of ['run_python','run_javascript','run_cpp','run_java','execute_command','run_in_terminal','save_file','read_file',
   'replace_text_in_file','list_directory','change_directory','web_search','fetch_web_content','browser_open_page','consult_secondary_agent',
   'save_memory','git_status','send_notification','wikipedia_search','rag_local_files'])assert.ok(!names.includes(removed),removed);
});
test('disabling the verification tools leaves only run_pyright',async()=>{
 assert.deepEqual((await provider({enableConfidenceAgentTools:false})).map(t=>t.name),['run_pyright']);
});
test('run_pyright returns structured diagnostics from the pinned checker without executing code',async()=>{
 const run=(await provider()).find(t=>t.name==='run_pyright');
 const marker=path.join(workspace,'must-not-exist.txt');
 const r=await run.implementation({python:`open(${JSON.stringify(marker)}, "w").write("x")\nprint(undefined_name)`});
 assert.equal(r.checker_version,'1.1.414');assert.equal(r.exit_code,1);
 assert.ok(r.diagnostics.some(d=>d.rule==='reportUndefinedVariable'),JSON.stringify(r.diagnostics));
 assert.equal(fs.existsSync(marker),false,'candidate code must never run');
});
test('Allow Pyright off blocks run_pyright and leaves the identifier layer unverifiable',async()=>{
 const tools=await provider({allowPyrightExecution:false});
 await assert.rejects(tools.find(t=>t.name==='run_pyright').implementation({python:'x = 1'}),/disabled/);
 const r=await tools.find(t=>t.name==='verify_identifier').implementation({code:'x = 1'});
 assert.equal(r.state,'unverifiable');
});
test('save_code writes inside the configured workspace only',async()=>{
 const save=(await provider()).find(t=>t.name==='save_code');
 const r=await save.implementation({code:'x = 1\n',filename:'candidate.py'});
 assert.equal(path.dirname(r.path),workspace);
 const outside=await save.implementation({code:'x',filename:'../escape.py'});
 assert.match(outside.error,/Invalid workspace-relative filename/);
});
test('workspace setting expands %VAR% and defaults outside any Beledarian folder',()=>{
 assert.equal(resolveWorkspace(''),DEFAULT_WORKSPACE);
 process.env.CAT_TEST_DIR=workspace;assert.equal(resolveWorkspace('%CAT_TEST_DIR%'),workspace);
 assert.ok(!/beledarian/i.test(DEFAULT_WORKSPACE));
});
