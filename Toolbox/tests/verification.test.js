const {test}=require('node:test');
const assert=require('node:assert/strict');
const {extractClaims}=require('../dist/claimExtractor');
const {queryPypi,verifyInterface}=require('../dist/packageEvidence');
const {verifyAccessPoint,verifyInputContract,verifyOutputContract,verifyContextual,checkValue}=require('../dist/openApiVerifier');
const {verifyIdentifier,createPyrightRunner,parsePyright}=require('../dist/pyrightRunner');
const {computeEwcs,makeDecision,presentReport,EWCSAccumulator}=require('../dist/verificationPolicy');
const {verifyCandidate,runIntervention}=require('../dist/verificationController');
const {ALL_LAYERS,result,hashCode}=require('../dist/verificationTypes');
const {createConfidenceAgentTools}=require('../dist/confidenceAgentTools');
const clone=x=>structuredClone(x);
const fixture=require('./fixtures/api.json');
const valid=`import requests\nr = requests.get("https://api.example.test/v1/users/1", params={"limit": 2})\ndata = r.json()\nprint(data["name"])`;
const pypi={exists:true,status:'found',distribution:'requests',latest_version:'2.32.5'};
const pyright=(diags=[],exit=diags.some(d=>d.severity==='error')?1:0)=>({stdout:JSON.stringify({version:'test',generalDiagnostics:diags,summary:{filesAnalyzed:1,errorCount:diags.filter(d=>d.severity==='error').length,warningCount:diags.filter(d=>d.severity==='warning').length}}),stderr:'',exit_code:exit});
const deps={runPyright:async()=>pyright(),lookupPackage:async()=>pypi};
const extracted=async code=>{const r=await extractClaims({code});assert.equal(r.error,undefined);return r;};
const check=async(fn,code,spec=fixture)=>fn({claims:(await extracted(code)).claims,spec,code});
const goodLayers=()=>ALL_LAYERS.map(l=>result(l,'verified_correct','tier_1','test','checked'));

test('missing layers retain weight and cannot authorize delivery',()=>{
 const r=computeEwcs({extraction_complete:true,layer_results:[result('access_point','verified_correct','tier_1','spec','checked')]});
 assert.equal(r.total_applicable_weight,15);assert.equal(r.ewcs,0.2667);assert.equal(r.missing_layers.length,5);assert.equal(makeDecision(r),'abstain');
});
test('uncertainty gates override a high score, contradictions allow one correction',()=>{
 const layers=goodLayers();layers[4]=result('output_contract','unverifiable','none','none','unknown');
 const r=computeEwcs({extraction_complete:true,layer_results:layers});assert.ok(r.ewcs>.85);assert.equal(makeDecision(r),'abstain');
 layers[4]=result('output_contract','verified_incorrect','tier_1','spec','bad');
 const bad=computeEwcs({extraction_complete:true,layer_results:layers});assert.equal(makeDecision(bad),'correct');assert.equal(makeDecision(bad,1),'abstain');
 assert.equal(makeDecision({...computeEwcs({extraction_complete:true,layer_results:goodLayers()}),extraction_complete:false}),'abstain');
});
test('empty applicable set is explicitly undefined',()=>{
 const r=computeEwcs({extraction_complete:true,layer_results:ALL_LAYERS.map(l=>result(l,'not_applicable','none','test','no claims'))});
 assert.equal(r.ewcs,null);assert.equal(r.signed_score,null);assert.equal(makeDecision(r),'abstain');
});
test('locked worked example stays 0.4875 and contributions are rounded',()=>{
 const layers=ALL_LAYERS.map(l=>result(l,'not_applicable','none','test','not used'));
 layers[0]=result('interface','verified_correct','tier_2','test','checked');layers[1]=result('identifier','verified_correct','tier_4','test','checked');layers[5]=result('contextual','unverifiable','none','test','unknown');
 const r=computeEwcs({extraction_complete:true,layer_results:layers});assert.equal(r.total_applicable_weight,8);assert.equal(r.ewcs,0.4875);assert.equal(r.contributions[0].positive_contribution,2.4);
});
test('invalid state/tier/weight/duplicates rejected; finalise is immutable and idempotent',()=>{
 for(const change of [{state:'fake'},{tier:'fake'},{weight:0},{tier:'none'}])assert.throws(()=>computeEwcs({extraction_complete:true,layer_results:[{...goodLayers()[0],...change}]}));
 assert.throws(()=>computeEwcs({extraction_complete:true,layer_results:[goodLayers()[0],goodLayers()[0]]}));
 const acc=new EWCSAccumulator('t');goodLayers().forEach(r=>acc.record(r));const r=acc.finalise();r.ewcs=0;assert.equal(acc.finalise().ewcs,1);assert.throws(()=>acc.record(goodLayers()[0]));
 assert.equal(makeDecision({ewcs:1,has_incorrect_layer:false}),'abstain');
});
test('abstain/correct/mismatched candidate reports never include source',()=>{
 const code='SECRET_CANDIDATE_SENTINEL',r=computeEwcs({extraction_complete:true,layer_results:goodLayers()});r.candidate_hash=hashCode(code);
 for(const decision of ['abstain','correct'])assert.ok(!presentReport({code,ewcs_report:r,decision}).report.includes(code));
 assert.ok(!presentReport({code:'OTHER_SECRET',ewcs_report:r,decision:'deliver'}).report.includes('OTHER_SECRET'));
 assert.ok(presentReport({code,ewcs_report:r,decision:'deliver'}).report.includes(code));
});
test('input dictionary reads are not response-field claims; dynamic endpoint retained',async()=>{
 const r=await extracted('import requests\ndef f(inputs):\n    url = inputs["url"]\n    params = inputs["query_params"]\n    return requests.get(url, params=params)');
 assert.equal(r.claims.filter(c=>c.type==='output_field').length,0);assert.equal(r.claims.filter(c=>c.type==='endpoint').length,1);assert.equal(r.complete,false);
 assert.equal((await verifyAccessPoint({claims:r.claims,spec:fixture})).state,'unverifiable');
 assert.equal((await verifyInputContract({claims:r.claims,spec:fixture})).state,'unverifiable');
});
test('literal variables, imported client aliases and parameter dictionaries resolve',async()=>{
 const r=await extracted('from requests import get as fetch\nurl="https://api.example.test/v1/users/1"\np={"limit":2}\nr=fetch(url,params=p)\nprint(r.json()["name"])');
 assert.equal(r.complete,true);const ep=r.claims.find(c=>c.type==='endpoint');assert.equal(ep.endpoint,'https://api.example.test/v1/users/1');assert.equal(ep.request.params.value.limit,2);
 assert.equal(r.claims.find(c=>c.type==='output_field').call_id,ep.call_id);
});
test('explicit runtime bindings resolve a parameterized URL without executing it',async()=>{
 const code='import requests\ndef f(inputs):\n    url=inputs["url"]\n    params=inputs["query_params"]\n    return requests.get(url,params=params).json()["name"]';
 const r=await extractClaims({code,input_bindings:{inputs:{url:'https://api.example.test/v1/users/1',query_params:{limit:2}}}});
 assert.equal(r.complete,true);assert.equal((await verifyInputContract({claims:r.claims,spec:fixture})).state,'verified_correct');
});
test('unsupported session/branch/mutation and syntax errors are explicitly incomplete',async()=>{
 for(const code of ['import requests\ns=requests.Session()\ns.get("https://api.example.test/v1/posts")','if True:\n    print(1)','d={}\nd.update({"x":1})','def ('])assert.equal((await extractClaims({code})).complete,false);
});
test('extraction never executes candidate side effects',async()=>{
 const r=await extracted('raise RuntimeError("MUST_NOT_EXECUTE")');assert.equal(r.complete,true);assert.equal(r.error,undefined);
});
test('network/server/JSON failures remain unverifiable package evidence',async()=>{
 for(const response of [async()=>{throw Error('offline')},async()=>new Response('',{status:503}),async()=>new Response('bad',{status:200}),async()=>new Response('{}',{status:200})]){
  const r=await queryPypi({library_name:'requests'},response);assert.equal(r.exists,null);assert.equal(r.status,'unverifiable');
  assert.equal((await verifyInterface({claims:[{type:'import',library:'requests'}],pypi_data:{requests:r}})).state,'unverifiable');
 }
});
test('registry 404 cannot prove a local/private import nonexistent; import aliases mapped',async()=>{
 const r=await queryPypi({library_name:'private_module'},async()=>new Response('',{status:404}));assert.equal(r.status,'not_found');
 assert.equal((await verifyInterface({claims:[{type:'import',library:'private_module'}],pypi_data:{private_module:r}})).state,'unverifiable');
 let url;const p=await queryPypi({library_name:'PIL'},async u=>{url=u;return new Response(JSON.stringify({info:{name:'Pillow',version:'1'}}));});
 assert.ok(url.includes('/Pillow/'));assert.equal(p.distribution,'Pillow');
});
test('stdlib imports do not need a PyPI distribution',async()=>{
 const r=await extracted('import json\nprint(json.dumps({"x":1}))');
 assert.equal((await verifyInterface({claims:r.claims})).state,'verified_correct');
});
test('Pyright process/configuration failures and malformed successful output cannot pass',async()=>{
 for(const r of [{stdout:'',stderr:'config',exit_code:3},{stdout:'',stderr:'',exit_code:null},{stdout:'',stderr:'',exit_code:0}, {...pyright(),timed_out:true}]){
  assert.equal((await verifyIdentifier(valid,async()=>r)).state,'unverifiable');
  const claims=(await extracted(valid)).claims;
  assert.equal((await verifyOutputContract({claims,spec:null,code:valid},async()=>r)).state,'unverifiable');
 }
});
test('clean Pyright output cannot establish untyped JSON response fields',async()=>{
 assert.equal((await verifyOutputContract({claims:(await extracted(valid)).claims,spec:null,code:valid},deps.runPyright)).state,'unverifiable');
});
test('structured undefined identifiers are incorrect; missing installations are unknown',async()=>{
 const bad=pyright([{severity:'error',rule:'reportUndefinedVariable',message:'"undefined_name" is not defined'}]);
 assert.equal((await verifyIdentifier('print(undefined_name)',async()=>bad)).state,'verified_incorrect');
 const missing=pyright([{severity:'error',rule:'reportMissingImports',message:'Import could not be resolved'}]);
 assert.equal((await verifyIdentifier('import foo',async()=>missing)).state,'unverifiable');
 assert.ok(parsePyright({...pyright(),candidate_hash:'wrong'},valid).error);
});
test('server origin and base path are checked, including operation server overrides',async()=>{
 for(const url of ['https://other.example/v1/users/1','https://api.example.test/users/1'])assert.equal((await check(verifyAccessPoint,valid.replace('https://api.example.test/v1/users/1',url))).state,'verified_incorrect');
 const s=clone(fixture);s.paths['/users/{id}'].get.servers=[{url:'https://other.example/v2'}];
 assert.equal((await check(verifyAccessPoint,valid.replace('https://api.example.test/v1/users/1','https://other.example/v2/users/1'),s)).state,'verified_correct');
});
test('invented endpoint and wrong HTTP method are detected',async()=>{
 assert.equal((await check(verifyAccessPoint,valid.replace('/users/1','/invented'))).state,'verified_incorrect');
 assert.equal((await check(verifyAccessPoint,valid.replace('requests.get','requests.delete'))).state,'verified_incorrect');
});
test('missing required input, wrong location, wrong type, range and path value are detected',async()=>{
 for(const code of [valid.replace(', params={"limit": 2}',''),valid.replace('params=','headers='),valid.replace('"limit": 2','"limit": "bad"'),valid.replace('"limit": 2','"limit": 99'),valid.replace('/users/1','/users/nope')]){
  assert.equal((await check(verifyInputContract,code)).state,'verified_incorrect',code);
 }
 assert.equal((await check(verifyInputContract,valid)).state,'verified_correct');
});
test('URL query values, path-level required parameters and operation overrides are honored',async()=>{
 assert.equal((await check(verifyInputContract,valid.replace('/users/1','/users/1?limit=2').replace(', params={"limit": 2}',''))).state,'verified_correct');
 const s=clone(fixture);s.paths['/users/{id}'].parameters.push({name:'limit',in:'query',required:true,schema:{type:'string'}});
 assert.equal((await check(verifyInputContract,valid,s)).state,'verified_correct');
});
test('unknown value and unsupported request serialization cannot pass',async()=>{
 assert.equal((await check(verifyInputContract,valid.replace('"limit": 2','"limit": runtime_limit'))).state,'unverifiable');
 assert.equal((await check(verifyInputContract,valid.replace('params={"limit": 2}','params=unknown_dict'))).state,'unverifiable');
});
test('body references, required properties, enum and additionalProperties enforced',async()=>{
 const prefix='import requests\nr=requests.post("https://api.example.test/v1/submit"';
 for(const body of [')',',json={})',',json={"name":"ok","kind":"z"})',',json={"name":"ok","invented":1})'])assert.equal((await check(verifyInputContract,prefix+body)).state,'verified_incorrect');
 assert.equal((await check(verifyInputContract,prefix+',json={"name":"ok","kind":"a"})')).state,'verified_correct');
 const s=clone(fixture);s.components.schemas.Body=s.paths['/submit'].post.requestBody.content['application/json'].schema;s.paths['/submit'].post.requestBody.content['application/json'].schema={$ref:'#/components/schemas/Body'};
 assert.equal((await check(verifyInputContract,prefix+',json={"name":"ok"})',s)).state,'verified_correct');
});
test('multiple requests are checked against their own parameters and response schemas',async()=>{
 const code=valid+'\np=requests.get("https://api.example.test/v1/posts")\nprint(p.json()[0]["title"])';
 assert.equal((await check(verifyInputContract,code)).state,'verified_correct');assert.equal((await check(verifyOutputContract,code)).state,'verified_correct');
 assert.equal((await check(verifyOutputContract,code.replace('["title"]','["name"]'))).state,'verified_incorrect');
});
test('array and nested response provenance, aliases and local references work',async()=>{
 const code='import requests\nr=requests.get("https://api.example.test/v1/posts")\na=r.json()\nb=a\nfor post in b:\n    print(post["title"])';
 assert.equal((await check(verifyOutputContract,code)).state,'verified_correct');
 assert.equal((await check(verifyOutputContract,code.replace('["title"]','["ghost"]'))).state,'verified_incorrect');
});
test('open schema omissions, external references, unions and ambiguous success responses remain unknown',async()=>{
 const open=clone(fixture);delete open.components.schemas.User.additionalProperties;
 assert.equal((await check(verifyOutputContract,valid.replace('["name"]','["ghost"]'),open)).state,'unverifiable');
 const ext=clone(fixture);ext.components.schemas.User={$ref:'https://example.test/schema.json'};
 assert.equal((await check(verifyOutputContract,valid,ext)).state,'unverifiable');
 const union=clone(fixture);union.components.schemas.User.oneOf=[{type:'object'}];assert.equal((await check(verifyOutputContract,valid,union)).state,'unverifiable');
 const status=clone(fixture);status.paths['/users/{id}'].get.responses['204']={description:'empty'};assert.equal((await check(verifyOutputContract,valid,status)).state,'unverifiable');
});
test('unsupported format/composition never silently passes values',()=>{
 assert.ok(checkValue('x',{type:'string',format:'uuid'},fixture,'v').unknown.length);
 assert.ok(checkValue(1,{type:'integer',oneOf:[{minimum:5}]},fixture,'v').unknown.length);
});
test('comments do not satisfy authentication; actual matching request credentials do',async()=>{
 const s=clone(fixture);s.security=[{token:[]}];
 assert.equal((await check(verifyContextual,valid+'\n# TODO add bearer authentication',s)).state,'verified_incorrect');
 const code=valid.replace('params={"limit": 2}','params={"limit": 2},headers={"Authorization":"Bearer test-token"}');
 assert.equal((await check(verifyContextual,code,s)).state,'verified_correct');
 assert.equal((await check(verifyContextual,code.replace('Bearer test-token','Basic abc'),s)).state,'verified_incorrect');
 assert.equal((await check(verifyContextual,code.replace('"Bearer test-token"','token'),s)).state,'unverifiable');
});
test('security definitions alone impose no requirement; operation overrides and OR/AND respected',async()=>{
 assert.equal((await check(verifyContextual,valid)).state,'not_applicable');
 const s=clone(fixture);s.security=[{token:[]}];s.paths['/users/{id}'].get.security=[];
 assert.equal((await check(verifyContextual,valid,s)).state,'not_applicable');
 s.paths['/users/{id}'].get.security=[{token:[]},{key:[]}];
 const code=valid.replace('"limit": 2','"limit": 2, "key":"abc"');assert.equal((await check(verifyContextual,code,s)).state,'verified_correct');
 s.paths['/users/{id}'].get.security=[{token:[],key:[]}];assert.equal((await check(verifyContextual,code,s)).state,'verified_incorrect');
});
test('controller preserves six real results, hashes candidate and reuses one checker run',async()=>{
 let calls=0;const r=await verifyCandidate({code:valid,spec:fixture},{...deps,runPyright:async()=>{calls++;return pyright();}});
 assert.equal(calls,1);assert.equal(r.layers.length,6);assert.equal(r.candidate_hash,hashCode(valid));assert.equal(r.decision,'deliver_with_flag');assert.equal(r.ewcs_report.ewcs,0.8385);
});
test('incomplete extraction/disabled checker/failed retrieval cannot deliver',async()=>{
 for(const d of [{...deps,allowPyright:false},{...deps,lookupPackage:async()=>{throw Error('offline')}},{...deps,extract:async()=>{throw Error('crash')}}])assert.equal((await runIntervention({code:valid,spec:fixture},d)).decision,'abstain');
 const r=await runIntervention({code:'import requests\ns=requests.Session()\ns.get("https://api.example.test/v1/posts")',spec:fixture},deps);
 assert.equal(r.decision,'abstain');assert.ok(!r.report.includes('requests.Session'));
});
test('one correction is reverified; a second bad candidate is withheld',async()=>{
 let calls=0;const r=await runIntervention({code:valid.replace('"limit": 2','"limit": 99'),spec:fixture},{...deps,correct:async()=>{calls++;return valid.replace('"limit": 2','"limit": 100');}});
 assert.equal(calls,1);assert.equal(r.attempts.length,2);assert.equal(r.decision,'abstain');assert.equal(r.delivered_code,null);assert.ok(!r.report.includes('requests.get'));
});
test('successful correction is checked before delivery and baseline retained unchanged',async()=>{
 const bad=valid.replace('"limit": 2','"limit": 99');const r=await runIntervention({code:bad,spec:fixture},{...deps,correct:async()=>valid});
 assert.equal(r.decision,'deliver_with_flag');assert.equal(r.delivered_code,valid);assert.equal(r.attempts[0].code,bad);assert.equal(r.attempts[1].verification.candidate_hash,hashCode(valid));
});
test('correction failure abstains without leaking candidate in report',async()=>{
 const r=await runIntervention({code:valid.replace('"limit": 2','"limit": 99'),spec:fixture},{...deps,correct:async()=>{throw Error('model offline')}});
 assert.equal(r.decision,'abstain');assert.ok(r.correction_error);assert.ok(!r.report.includes('requests.get'));
});
test('plugin retains named tools and exposes the complete verification path',()=>{
 const tools=createConfidenceAgentTools({isEnabled:true,allowPyright:true,getWorkingDirectory:()=>process.cwd(),runPyright:deps.runPyright});
 for(const name of ['verify_candidate','verify_identifier','compute_ewcs','present_report'])assert.ok(tools.some(t=>t.name===name));
});
test('real pinned Pyright catches undefined name and checks a valid literal requests candidate',async()=>{
 const run=createPyrightRunner();
 const bad=await verifyIdentifier('print(undefined_name)',run);assert.equal(bad.state,'verified_incorrect',bad.evidence_detail);assert.match(bad.evidence_detail,/reportUndefinedVariable/);
 const r=await runIntervention({code:valid,spec:fixture},{lookupPackage:deps.lookupPackage,runPyright:run});
 assert.equal(r.decision,'deliver_with_flag',JSON.stringify(r.attempts[0].verification.layers));
 assert.equal(r.attempts[0].verification.evidence.pyright.checker_version,'1.1.414');
});
test('unspecified extraction evidence and unsupported schema semantics never authorize delivery',()=>{
 assert.equal(makeDecision(computeEwcs({layer_results:goodLayers()})),'abstain');
 const c=checkValue(5,{properties:{x:{type:'string'}}},fixture,'input');assert.equal(c.bad.length,0);assert.ok(c.unknown.length);
 const union=checkValue('ok',{type:'integer',oneOf:[{type:'string'}]},fixture,'input');assert.equal(union.bad.length,0);assert.ok(union.unknown.length);
});
test('standalone layer tools retain unsupported-extraction uncertainty',async()=>{
 const r=await extracted('import requests\ns=requests.Session()\nr=s.get("https://api.example.test/v1/posts")\nprint(r.json()[0]["ghost"])');
 for(const fn of [verifyAccessPoint,verifyInputContract,verifyOutputContract,verifyContextual])assert.equal((await fn({claims:r.claims,spec:fixture})).state,'unverifiable');
});
test('checker suppression, unsupported requests methods and custom JSON decoding remain incomplete',async()=>{
 for(const code of ['# pyright: reportAttributeAccessIssue=false\nimport requests\nrequests.not_real()',valid+'\n# type: ignore',valid.replace('r.json()','r.json(object_hook=hook)')])assert.equal((await extracted(code)).complete,false);
});
test('unknown undeclared bodies/auth and conflicting content types cannot pass',async()=>{
 assert.equal((await check(verifyInputContract,valid.replace('params={"limit": 2}','params={"limit": 2}, json=runtime_body'))).state,'unverifiable');
 assert.equal((await check(verifyInputContract,valid.replace('params={"limit": 2}','params={"limit": 2}, auth=runtime_auth'))).state,'unverifiable');
 const code='import requests\nr=requests.post("https://api.example.test/v1/submit",json={"name":"ok"},headers={"Content-Type":"text/plain"})';
 assert.equal((await check(verifyInputContract,code)).state,'verified_incorrect');
});
test('readOnly required response properties are not required in request bodies',()=>{
 const schema={type:'object',required:['id','name'],properties:{id:{type:'integer',readOnly:true},name:{type:'string'}}};
 assert.deepEqual(checkValue({name:'ok'},schema,fixture,'body'),{bad:[],unknown:[]});
 assert.ok(checkValue({id:1,name:'ok'},schema,fixture,'body').bad.length);
});
test('CLI controls a real checker plus an OpenAI-compatible correction request and preserves the trace',async()=>{
 const {createServer}=require('node:http');const fs=require('node:fs/promises');const os=require('node:os');const path=require('node:path');const {spawn}=require('node:child_process');
 const dir=await fs.mkdtemp(path.join(os.tmpdir(),'ca-cli-test-'));let calls=0,request;
 const server=createServer((req,res)=>{let text='';req.on('data',d=>text+=d);req.on('end',()=>{calls++;request=JSON.parse(text);res.writeHead(200,{'Content-Type':'application/json'});res.end(JSON.stringify({choices:[{finish_reason:'stop',message:{content:'```python\n'+valid+'\n```'}}]}));});});
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 try {
  const bad=valid.replace('"limit": 2','"limit": 99');await fs.writeFile(path.join(dir,'candidate.py'),bad);
  await fs.writeFile(path.join(dir,'packages.json'),JSON.stringify({requests:pypi}));
  const out=path.join(dir,'run');
  const run=await new Promise(resolve=>{const child=spawn(process.execPath,['dist/verificationCli.js','--code',path.join(dir,'candidate.py'),'--spec','tests/fixtures/api.json','--package-evidence',path.join(dir,'packages.json'),'--out-dir',out,'--model','qwen-test-stub','--endpoint',`http://127.0.0.1:${server.address().port}/v1`],{env:process.env});let stdout='',stderr='';child.stdout.on('data',d=>stdout+=d);child.stderr.on('data',d=>stderr+=d);child.on('close',code=>resolve({code,stdout,stderr}));});
  assert.equal(run.code,0,run.stderr);assert.equal(calls,1);assert.equal(request.model,'qwen-test-stub');assert.equal(request.stream,false);
  const audit=JSON.parse(await fs.readFile(path.join(out,'audit.json'),'utf8'));
  assert.equal(audit.decision,'deliver_with_flag');assert.equal(audit.attempts.length,2);assert.equal(audit.attempts[0].code,bad);assert.equal(await fs.readFile(path.join(out,'delivered.py'),'utf8'),valid);
  assert.ok(!run.stdout.includes('"limit": 99'));
 } finally {await new Promise(resolve=>server.close(resolve));await fs.rm(dir,{recursive:true,force:true});}
});
test('shipped parameterized example is verifiable with task bindings and real Pyright',async()=>{
 const fs=require('node:fs/promises');const code=await fs.readFile('examples/jsonplaceholder-parameterized.py','utf8');
 const spec=JSON.parse(await fs.readFile('examples/jsonplaceholder-posts.openapi.json','utf8'));
 const input_bindings=JSON.parse(await fs.readFile('examples/inputs.json','utf8'));
 const r=await runIntervention({code,spec,input_bindings},{lookupPackage:deps.lookupPackage});
 assert.equal(r.decision,'deliver_with_flag',JSON.stringify(r.attempts[0].verification.layers));
 assert.equal(r.delivered_code,code);
 const unbound=await runIntervention({code,spec},{lookupPackage:deps.lookupPackage});
 assert.equal(unbound.decision,'abstain');assert.equal(unbound.delivered_code,null);
});
test('style-only diagnostics are not false contradictions and missing annotations remain uncertainty',async()=>{
 const unused=pyright([{severity:'error',rule:'reportUnusedImport',message:'Import is not accessed'}]);
 assert.equal((await verifyIdentifier('import json',async()=>unused)).state,'verified_correct');
 const missing=pyright([{severity:'error',rule:'reportMissingParameterType',message:'Parameter annotation missing'}]);
 assert.equal((await verifyIdentifier('def f(x):\n    return x',async()=>missing)).state,'unverifiable');
});
