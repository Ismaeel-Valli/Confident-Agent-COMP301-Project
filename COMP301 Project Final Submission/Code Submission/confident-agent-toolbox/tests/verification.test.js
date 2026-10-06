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
test('unsupported sessions and syntax errors are explicitly incomplete',async()=>{
 for(const code of ['import requests\ns=requests.Session()\ns.get("https://api.example.test/v1/posts")','def ('])assert.equal((await extractClaims({code})).complete,false);
});
test('branches and tracked mutations are followed; unfollowable mutations make values unknown, never stale',async()=>{
 const tracked=await extracted('import requests\nd={}\nd.update({"x":1})\nd["y"]=2\nif True:\n    print(1)\nrequests.get("https://api.example.test/v1/posts",params=d)');
 assert.equal(tracked.complete,true);assert.deepEqual(tracked.claims.find(c=>c.type==='endpoint').request.params.value,{x:1,y:2});
 const lost=await extracted('import requests\nd={"limit":2}\nadd_defaults(d)\nrequests.get("https://api.example.test/v1/users/1",params=d)');
 assert.equal(lost.claims.find(c=>c.type==='endpoint').request.params.keys_known,false);
 assert.equal((await verifyInputContract({claims:lost.claims,spec:fixture})).state,'unverifiable');
});
// Regression for the all-zero dataset scores: the benchmark reference template builds
// headers/params by subscript assignment, fills the path with url.replace(quote(...))
// and guards empty bodies. Every layer must be established, not zeroed.
const datasetTemplate=`import requests
from urllib.parse import quote


def solve(inputs):
    url = 'https://api.example.test/v1/users/{id}'
    params = {}
    headers = {}
    headers['Accept'] = 'application/json'
    params['limit'] = 2
    url = url.replace('{id}', quote(str(inputs['user_id']), safe=''))
    response = requests.request('GET', url, params=params, headers=headers, timeout=20)
    response.raise_for_status()
    if response.status_code == 204 or not response.content:
        return None
    data = response.json()
    return data.get('name')
`;
test('dataset reference template verifies every layer; a dropped required input is contradicted',async()=>{
 const r=await verifyCandidate({code:datasetTemplate,spec:fixture},deps);
 assert.equal(r.extraction.complete,true,JSON.stringify(r.extraction.issues));
 assert.deepEqual(r.layers.map(l=>l.state),['verified_correct','verified_correct','verified_correct','verified_correct','verified_correct','not_applicable']);
 assert.equal(r.ewcs_report.ewcs,0.8385);assert.equal(r.decision,'deliver_with_flag');
 const mutant=await verifyCandidate({code:datasetTemplate.replace("    params['limit'] = 2\n",''),spec:fixture},deps);
 assert.equal(mutant.layers.find(l=>l.layer==='input_contract').state,'verified_incorrect');assert.equal(mutant.decision,'correct');
});
test('parameterized URL templates match path templates without runtime values',async()=>{
 const r=await extracted('import requests\ndef f(user_id):\n    r=requests.get(f"https://api.example.test/v1/users/{user_id}",params={"limit":2})\n    return r.json()["name"]');
 assert.equal(r.complete,true);
 for(const fn of [verifyAccessPoint,verifyInputContract,verifyOutputContract])assert.equal((await fn({claims:r.claims,spec:fixture})).state,'verified_correct',fn.name);
 const wrong=await extracted('import requests\ndef f(user_id):\n    return requests.get(f"https://api.example.test/v1/accounts/{user_id}")');
 assert.equal((await verifyAccessPoint({claims:wrong.claims,spec:fixture})).state,'verified_incorrect');
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
// A runtime input value makes no static claim about its content: its constraints are a
// noncritical note. Unknown keys, and statically typed mismatches, still decide the layer.
test('runtime input values are noted; unknown keys and typed mismatches still decide',async()=>{
 const runtime=await check(verifyInputContract,valid.replace('"limit": 2','"limit": runtime_limit'));
 assert.equal(runtime.state,'verified_correct');assert.match(runtime.evidence_detail,/not statically known/);
 assert.equal((await check(verifyInputContract,valid.replace('params={"limit": 2}','params=unknown_dict'))).state,'unverifiable');
 assert.equal((await check(verifyInputContract,'import requests\nr=requests.post("https://api.example.test/v1/submit",json={"name":len(items)})')).state,'verified_incorrect');
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
// Pilot chat runs scored layers 3-6 as zero because no specification ever reached the
// verifier (resolve_api_spec finds none; the model passed wrappers, PyPI data or an
// invented spec). The plugin now selects frozen evidence from the called host.
test('plugin selects frozen evidence by host; model-supplied specs are ignored for known hosts',async t=>{
 t.mock.method(globalThis,'fetch',async()=>new Response(JSON.stringify({info:{name:'requests',version:'2.34.2',summary:'x'}})));
 const tools=createConfidenceAgentTools({isEnabled:true,allowPyright:true,getWorkingDirectory:()=>process.cwd(),runPyright:deps.runPyright});
 const verify=tools.find(x=>x.name==='verify_candidate');
 const code='import requests\n\ndef solve(inputs):\n    resource_id = inputs.get("resource_id")\n    response = requests.get(f"https://dummyjson.com/products/{resource_id}")\n    response.raise_for_status()\n    return response.json()["title"]\n';
 const r=await verify.implementation({code});
 assert.match(r.evidence_selection,/DummyJSON/);
 assert.deepEqual(r.layers.slice(2,5).map(l=>l.state),['verified_correct','verified_correct','verified_correct'],JSON.stringify(r.layers));
 const invented=await verify.implementation({code:code.replace('["title"]','["product"]')});
 // The curated DummyJSON schema is open, so an undocumented field cannot be contradicted: it stays unresolved and is withheld.
 assert.equal(invented.layers.find(l=>l.layer==='output_contract').state,'unverifiable');assert.equal(invented.decision,'abstain');
 const claims=(await extracted(code)).claims;
 const fake={openapi:'3.0.0',info:{title:'invented',version:'1'},servers:[{url:'https://dummyjson.com'}],paths:{}};
 const ap=await tools.find(x=>x.name==='verify_access_point').implementation({claims,spec:fake});
 assert.equal(ap.state,'verified_correct');assert.match(ap.evidence_source_selection,/ignored/);
});
// Pilot run: a chat assembled the score from the layer tools, then present_report withheld
// the code and the model misread it as a threshold failure. The report now states the reason.
test('present_report explains when a report is not bound to the code',()=>{
 const r=computeEwcs({extraction_complete:true,layer_results:goodLayers()});
 assert.match(presentReport({code:'x',ewcs_report:r,decision:'deliver'}).report,/not bound to any code/);
 r.candidate_hash=hashCode('other');
 assert.match(presentReport({code:'x',ewcs_report:r,decision:'deliver'}).report,/different code/);
});
// OAuth2 scopes belong to the token, not the code: placement and scheme are checked,
// scopes are reported as a noncritical note (decision 6 in SCORING_FIXES.md).
test('OAuth2 bearer placement is verified; scopes are noted, not gated',async()=>{
 const s=clone(fixture);s.components.securitySchemes.oauth={type:'oauth2',flows:{implicit:{authorizationUrl:'https://api.example.test/oauth',scopes:{'read:users':'read'}}}};
 s.paths['/users/{id}'].get.security=[{oauth:['read:users']}];
 const call=h=>`import requests\ndef f(inputs):\n    return requests.get("https://api.example.test/v1/users/1", params={"limit": 2}, headers=${h})`;
 const ok=await check(verifyContextual,call('{"Authorization": f"Bearer {inputs[\'credential\']}"}'),s);
 assert.equal(ok.state,'verified_correct',ok.evidence_detail);assert.match(ok.evidence_detail,/scopes \(read:users\)/);
 assert.equal((await check(verifyContextual,call('{"Authorization": f"token {inputs[\'credential\']}"}'),s)).state,'verified_incorrect');
 assert.equal((await check(verifyContextual,call('{"Accept": "application/json"}'),s)).state,'verified_incorrect');
});
test('comma-separated array query parameters are checked item by item',async()=>{
 const s=clone(fixture);s.paths['/posts'].get.parameters=[{name:'fields',in:'query',explode:false,schema:{type:'array',items:{type:'string',enum:['title','body']}}}];
 const call=q=>`import requests\nrequests.get("https://api.example.test/v1/posts", params={"fields": "${q}"})`;
 assert.equal((await check(verifyInputContract,call('title,body'),s)).state,'verified_correct');
 assert.equal((await check(verifyInputContract,call('title'),s)).state,'verified_correct');
 assert.equal((await check(verifyInputContract,call('title,pm10'),s)).state,'verified_incorrect');
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
test('style-only and general Python diagnostics are not API contradictions',async()=>{
 const unused=pyright([{severity:'error',rule:'reportUnusedImport',message:'Import is not accessed'}]);
 assert.equal((await verifyIdentifier('import json',async()=>unused)).state,'verified_correct');
 const missing=pyright([{severity:'error',rule:'reportMissingParameterType',message:'Parameter annotation missing',range:{start:{line:0,character:6}}}]);
 const r=await verifyIdentifier('def f(x):\n    return x',async()=>missing);
 assert.equal(r.state,'verified_correct');assert.match(r.evidence_detail,/General Python diagnostics/);
 const api=pyright([{severity:'error',rule:'reportArgumentType',message:'bad argument',range:{start:{line:1,character:0}}}]);
 assert.equal((await verifyIdentifier('import requests\nrequests.get(1)',async()=>api)).state,'verified_incorrect');
});

// Entries set inside an if (optional parameters, conditional credentials) and branch-dependent
// return values were reported as "unresolved keys" / "different operations" (pilot run 2026-09-26).
const optSpec={openapi:'3.0.3',info:{title:'optional entries',version:'1'},servers:[{url:'https://api.example.test'}],
 components:{securitySchemes:{key:{type:'apiKey',in:'header',name:'X-Key'}}},
 paths:{'/items':{get:{security:[{key:[]}],parameters:[{name:'q',in:'query',required:true,schema:{type:'string'}},{name:'limit',in:'query',schema:{type:'integer'}}],
  responses:{'200':{description:'ok',content:{'application/json':{schema:{type:'object',properties:{id:{type:'integer'},user:{type:'object',properties:{id:{type:'integer'}}}}}}}}}}}}};
const optCode=(setup,headers='{"X-Key": inputs["key"]}')=>`import requests\ndef solve(inputs):\n    params = {}\n    headers = ${headers}\n${setup}\n    r = requests.get("https://api.example.test/items", params=params, headers=headers)\n    r.raise_for_status()\n    return r.json()\n`;
test('an optional parameter added inside an if is checked by name, not treated as unresolved',async()=>{
 const ok=await check(verifyInputContract,optCode('    params["q"] = "x"\n    if "limit" in inputs:\n        params["limit"] = inputs["limit"]'),optSpec);
 assert.equal(ok.state,'verified_correct',ok.evidence_detail);
 const invented=await check(verifyInputContract,optCode('    params["q"] = "x"\n    if "fields" in inputs:\n        params["fields"] = inputs["fields"]'),optSpec);
 assert.equal(invented.state,'unverifiable');assert.match(invented.evidence_detail,/Undeclared query parameter fields/);assert.doesNotMatch(invented.evidence_detail,/unresolved keys/);
});
test('a required parameter or credential sent on some paths only is not established',async()=>{
 const q=await check(verifyInputContract,optCode('    if "q" in inputs:\n        params["q"] = inputs["q"]'),optSpec);
 assert.equal(q.state,'unverifiable');assert.match(q.evidence_detail,/Required query parameter q is only sent on some code paths/);
 const key=await check(verifyContextual,optCode('    params["q"] = "x"\n    if "key" in inputs:\n        headers["X-Key"] = inputs["key"]','{}'),optSpec);
 assert.equal(key.state,'unverifiable');assert.match(key.evidence_detail,/only sent on some code paths/);
});
test('different fields returned on different branches do not limit extraction',async()=>{
 const code='import requests\ndef solve(inputs):\n    r = requests.get("https://api.example.test/items", params={"q": "x"}, headers={"X-Key": inputs["key"]})\n    data = r.json()\n    if "id" in data:\n        return data["id"]\n    elif "user" in data:\n        return data["user"]["id"]\n    return None\n';
 const r=await extracted(code);assert.equal(r.complete,true,JSON.stringify(r.issues));
 const out=await check(verifyOutputContract,code,optSpec);assert.equal(out.state,'verified_correct',out.evidence_detail);
 // A caller that reads fields from such a result still cannot link them to one response path.
 const caller='import requests\ndef get(inputs):\n    data = requests.get("https://api.example.test/items", params={"q": "x"}).json()\n    if inputs:\n        return data["id"]\n    return data["user"]\ndef solve(inputs):\n    return get(inputs)["id"]\n';
 const c=await extractClaims({code:caller});assert.equal(c.complete,false);assert.ok(c.issues.some(i=>/ambiguous provenance/.test(i.reason)),JSON.stringify(c.issues));
});

// Benchmark run 1 (2026-09-27): "name" sent where the label API declares "new_name" was delivered,
// because an undeclared body field in a silent (open) schema was only a note.
const bodySpec=extra=>({openapi:'3.0.3',info:{title:'body fields',version:'1'},servers:[{url:'https://api.example.test'}],
 paths:{'/labels/{name}':{patch:{parameters:[{name:'name',in:'path',required:true,schema:{type:'string'}}],
  requestBody:{content:{'application/json':{schema:{type:'object',properties:{new_name:{type:'string'},color:{type:'string'}},...extra}}}},
  responses:{'200':{description:'ok'}}}}}});
const bodyCode='import requests\ndef solve(inputs):\n    r = requests.patch("https://api.example.test/labels/bug", json={"name": inputs["new"]})\n    r.raise_for_status()\n    return r.json()\n';
test('an undeclared request-body field is unresolved unless the schema explicitly allows extras',async()=>{
 const silent=await check(verifyInputContract,bodyCode,bodySpec({}));
 assert.equal(silent.state,'unverifiable');assert.match(silent.evidence_detail,/body: property name is not declared; acceptance is undocumented/);
 const allowed=await check(verifyInputContract,bodyCode,bodySpec({additionalProperties:true}));
 assert.equal(allowed.state,'verified_correct',allowed.evidence_detail);assert.match(allowed.evidence_detail,/explicitly allows additional properties/);
 const closed=await check(verifyInputContract,bodyCode,bodySpec({additionalProperties:false}));
 assert.equal(closed.state,'verified_incorrect');
});
