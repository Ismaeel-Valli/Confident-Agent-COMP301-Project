const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const {spawnSync}=require('node:child_process');
const {extractClaims}=require('../dist/claimExtractor');
const {verifyInterface}=require('../dist/packageEvidence');
const {verifyIdentifier,createPyrightRunner}=require('../dist/pyrightRunner');
const {verifyCandidate,runIntervention}=require('../dist/verificationController');
const {verifyAccessPoint,verifyOutputContract}=require('../dist/openApiVerifier');
const {BUNDLED_REFERENCES,TOOLBOX_VERSION}=require('../dist/bundledReferences');
const spec=require('../examples/jsonplaceholder-posts.openapi.json');
const packages=require('../examples/evidence/requests-pypi-pilot.json');
const code=fs.readFileSync('examples/jsonplaceholder-solve.py','utf8');
const original=fs.readFileSync('tests/fixtures/pilot-return-none.py','utf8');
const lookupPackage=async name=>packages[name]; // Captured evidence, no live registry test.
const clean=async()=>({stdout:JSON.stringify({generalDiagnostics:[],summary:{filesAnalyzed:1,errorCount:0}}),stderr:'',exit_code:0});

test('ordinary empty-body and status guards retain complete extraction for both pilot candidates',async()=>{
 for(const candidate of [code,original]){
  const r=await extractClaims({code:candidate});
  assert.equal(r.complete,true,JSON.stringify(r.issues));
  assert.equal(r.claims.filter(c=>c.type==='endpoint').length,1);
 }
});
test('response guard branches preserve operation-linked output fields',async()=>{
 const candidate='import requests\nr=requests.get("https://jsonplaceholder.typicode.com/posts/1")\ndef f():\n    if r.content:\n        data=r.json()\n        return data.get("title")\n    else:\n        return None';
 const r=await extractClaims({code:candidate});assert.equal(r.complete,true,JSON.stringify(r.issues));
 const output=r.claims.find(c=>c.type==='output_field');assert.equal(output.field,'title');
 assert.equal(output.call_id,r.claims.find(c=>c.type==='endpoint').call_id);
 assert.equal((await verifyOutputContract({claims:r.claims,spec})).state,'verified_correct');
});
test('response-only conditional expressions are supported',async()=>{
 const candidate='import requests\ndef f():\n    r=requests.get("https://jsonplaceholder.typicode.com/posts")\n    return r.json() if r.content else None';
 assert.equal((await extractClaims({code:candidate})).complete,true);
});
// Branches are joined rather than treated as unsupported. The safety properties are
// asserted directly: no stale values, conflicting response provenance is flagged
// for the output layer, and reads after a guard stay linked to their operation.
test('branch effects never leave stale values or unlinked response reads',async()=>{
 const {verifyInputContract}=require('../dist/openApiVerifier');
 const prefix='import requests\nr=requests.get("https://jsonplaceholder.typicode.com/posts")\n';
 const dynamic=await extractClaims({code:prefix+'if r.content:\n    url="https://other.test/"\nrequests.get(url)'});
 assert.equal(dynamic.complete,false);assert.equal(dynamic.claims.filter(c=>c.type==='endpoint'&&c.resolved===false).length,1);
 const ambiguous=await extractClaims({code:prefix+'if r.content:\n    r=requests.get("https://other.test/")\nprint(r.json()["title"])'});
 assert.equal(ambiguous.complete,false);assert.ok(ambiguous.issues.every(i=>i.affects.join()==='output_contract'),JSON.stringify(ambiguous.issues));
 assert.equal(ambiguous.claims.filter(c=>c.type==='output_field').length,0);
 const headers=await extractClaims({code:prefix+'headers={"Accept":"x"}\nif r.content:\n    headers.update(runtime_headers)\nrequests.get("https://jsonplaceholder.typicode.com/posts",headers=headers)'});
 assert.equal(headers.claims.filter(c=>c.type==='endpoint').pop().request.headers.keys_known,false);
 assert.equal((await verifyInputContract({claims:headers.claims,spec})).state,'unverifiable');
 for(const tail of ['if r.content:\n    data=r.json()\nprint(data["missing"])','x=r.json() if inputs["flag"] else None\nprint(x["missing"])']){
  const out=await extractClaims({code:prefix+tail});
  assert.equal(out.claims.find(c=>c.type==='output_field').field,'missing',tail);
  assert.equal((await verifyOutputContract({claims:out.claims,spec})).state,'verified_incorrect',tail); // string field on the posts array
 }
 assert.equal((await extractClaims({code:prefix+'if r.content:\n    raise custom_exception()'})).complete,true);
});
test('requests inside conditions are extracted as ordinary claims',async()=>{
 const r=await extractClaims({code:'import requests\nif requests.get("https://other.test/").status_code == 200:\n    print("x")'});
 assert.equal(r.complete,true);assert.equal(r.claims.filter(c=>c.type==='endpoint').length,1);
});
test('incomplete extraction preserves established import evidence but blocks delivery',async()=>{
 const candidate=code+'\nclass Helper:\n    pass\n';
 const r=await verifyCandidate({code:candidate,spec},{lookupPackage,runPyright:clean});
 assert.equal(r.layers.find(r=>r.layer==='interface').state,'verified_correct');
 assert.match(r.layers.find(r=>r.layer==='interface').evidence_detail,/extracted imports only/);
 assert.equal(r.extraction.complete,false);assert.equal(r.decision,'abstain');assert.ok(r.ewcs_report.positive_weight>0);
 const final=await runIntervention({code:candidate,spec},{lookupPackage,runPyright:clean});assert.equal(final.delivered_code,null);
});
test('incomplete extraction never makes an empty import inventory not-applicable',async()=>{
 const r=await extractClaims({code:'exec(runtime_code)'});
 assert.equal((await verifyInterface({claims:r.claims})).state,'unverifiable');
});
test('truncated PyPI metadata identifies the missing distribution',async()=>{
 const r=await extractClaims({code});const datum={...packages.requests};delete datum.distribution;
 const result=await verifyInterface({claims:r.claims,pypi_data:{requests:datum}});
 assert.equal(result.state,'unverifiable');assert.match(result.evidence_detail,/distribution=\(missing\)/);
 assert.equal((await verifyInterface({claims:r.claims,pypi_data:packages})).state,'verified_correct');
});
test('discovery wrappers produce actionable errors without becoming specifications',async()=>{
 const r=await extractClaims({code});const layer=await verifyAccessPoint({claims:r.claims,spec:{spec:null,source_url:null}});
 assert.equal(layer.state,'unverifiable');assert.match(layer.evidence_detail,/wrapper/);
});
// Pyright runs in standard mode. Annotation completeness is not identifier evidence,
// so untyped benchmark functions such as solve(inputs) are not left unresolved.
test('real pinned Pyright verifies the pilot and untyped parameters in standard mode',async()=>{
 const result=await verifyIdentifier(code,createPyrightRunner());
 assert.equal(result.state,'verified_correct',result.evidence_detail);assert.match(result.evidence_detail,/standard mode/);
 for(const candidate of ['def f(inputs):\n    return inputs["url"]','def f(inputs):\n    def inner():\n        return inputs\n    return inner()']){
  const r=await verifyIdentifier(candidate,createPyrightRunner());assert.equal(r.state,'verified_correct',r.evidence_detail);
 }
});
test('real Pyright separates API identifier errors from general Python diagnostics',async()=>{
 const invented=await verifyIdentifier('import requests\nrequests.fetch_json("https://jsonplaceholder.typicode.com/posts")',createPyrightRunner());
 assert.equal(invented.state,'verified_incorrect',invented.evidence_detail);assert.match(invented.evidence_detail,/reportAttributeAccessIssue/);
 const response=await verifyIdentifier('import requests\nr = requests.get("https://jsonplaceholder.typicode.com/posts")\nprint(r.json_data)',createPyrightRunner());
 assert.equal(response.state,'verified_incorrect',response.evidence_detail);
 const general=await verifyIdentifier('def f(x: int) -> str:\n    return x',createPyrightRunner());
 assert.equal(general.state,'verified_correct',general.evidence_detail);assert.match(general.evidence_detail,/General Python diagnostics/);
});
test('unused-parameter ranges are scope-specific and reflection is conservative',async()=>{
 const r=await extractClaims({code:'def f(inputs):\n    return 1\ndef g(inputs):\n    return inputs\ndef h(inputs):\n    return locals()'});
 assert.equal(r.unused_parameters.length,1);assert.equal(r.unused_parameters[0].line,0);
});
// A documented optional field is permitted by the contract (report section 6.7), so the
// field claim is verified; non-guaranteed presence is reported as a noncritical note.
test('reviewed snapshot: optional documented fields verify with a note; unmodeled filters stay unknown',async()=>{
 assert.equal(spec.components.schemas.Post.required,undefined);
 const direct=await extractClaims({code:'import requests\nr=requests.get("https://jsonplaceholder.typicode.com/posts/1")\nprint(r.json()["title"])'});
 const layer=await verifyOutputContract({claims:direct.claims,spec});
 assert.equal(layer.state,'verified_correct');assert.match(layer.evidence_detail,/optional in the contract/);
 const ghost=await extractClaims({code:'import requests\nr=requests.get("https://jsonplaceholder.typicode.com/posts/1")\nprint(r.json()["ghost"])'});
 assert.equal((await verifyOutputContract({claims:ghost.claims,spec})).state,'unverifiable');
 const {verifyInputContract}=require('../dist/openApiVerifier');
 const filtered=await extractClaims({code:'import requests\nrequests.get("https://jsonplaceholder.typicode.com/posts",params={"userId":1})'});
 assert.equal((await verifyInputContract({claims:filtered.claims,spec})).state,'unverifiable');
});
test('bundled native reference matches the reviewed file and release',()=>{
 assert.deepEqual(BUNDLED_REFERENCES['jsonplaceholder-posts'],spec);assert.equal(TOOLBOX_VERSION,require('../package.json').version);
});
test('native verify_candidate loads the reference and carries complete package evidence internally',async t=>{
 const {createConfidenceAgentTools}=require('../dist/confidenceAgentTools');
 const {hashCode}=require('../dist/verificationTypes');let lookups=0;
 t.mock.method(globalThis,'fetch',async url=>{
  lookups++;assert.equal(url,packages.requests.source_url);
  return new Response(JSON.stringify({info:{name:'requests',version:packages.requests.latest_version,summary:packages.requests.summary}}));
 });
 const tool=createConfidenceAgentTools({isEnabled:true,allowPyright:true,getWorkingDirectory:()=>process.cwd(),runPyright:createPyrightRunner()}).find(t=>t.name==='verify_candidate');
 const parameters={code,reference_id:'jsonplaceholder-posts'};
 tool.checkParameters(parameters);
 const r=await tool.implementation(parameters);
 assert.equal(r.toolbox_version,require('../package.json').version);assert.equal(r.reference_id,'jsonplaceholder-posts');
 assert.equal(r.spec_hash,hashCode(JSON.stringify(spec)));assert.equal(lookups,1);
 assert.equal(r.decision,'deliver_with_flag',JSON.stringify(r.layers));assert.equal(r.ewcs_report.ewcs,0.725);
 const conflict=await tool.implementation({...parameters,spec});assert.match(conflict.error,/not both/);
});
test('corrected pilot runs through the real checker/controller with frozen evidence',async()=>{
 const r=await runIntervention({code,spec},{lookupPackage});const v=r.attempts[0].verification;
 assert.equal(v.extraction.complete,true);assert.equal(v.ewcs_report.ewcs,0.725);assert.equal(r.decision,'deliver_with_flag',JSON.stringify(v.layers));
 assert.equal(r.delivered_code,code);assert.match(r.report,/Task behavior has not been independently checked/);
 const missing=await runIntervention({code,spec:null},{lookupPackage});assert.equal(missing.decision,'abstain');assert.equal(missing.delivered_code,null);
});
test('independent mocked behavior checks reject the pilot bug and accept the reference',{skip:process.env.RUN_BEHAVIOR_EVAL!=='1' && 'executes shipped fixtures (one model-generated); set RUN_BEHAVIOR_EVAL=1 to run'},()=>{
 const r=spawnSync(process.env.CONFIDENCE_PYTHON || 'python',['evaluation/jsonplaceholder_behavior.py'],{encoding:'utf8',timeout:20000});
 assert.equal(r.status,0,r.stderr);const report=JSON.parse(r.stdout);
 assert.equal(report.fixtures.corrected_reference.passed,11);assert.equal(report.fixtures.corrected_reference.total,11);
 assert.equal(report.fixtures.original_pilot.all_passed,false);
 for(const name of ['populated_200','empty_body_200','empty_body_204','populated_201','empty_json_array']){
  assert.equal(report.fixtures.original_pilot.cases.find(c=>c.case===name).passed,false,name);
 }
});
