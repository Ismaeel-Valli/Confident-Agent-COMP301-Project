import { extractClaims } from './claimExtractor';
import { verifyInterface, queryPypi, PackageEvidence } from './packageEvidence';
import { createPyrightRunner, verifyIdentifier, RunPyright, PyrightResult } from './pyrightRunner';
import { verifyAccessPoint, verifyInputContract, verifyOutputContract, verifyContextual } from './openApiVerifier';
import { computeEwcs, makeDecision, presentReport, EWCSReport, DecisionPolicy, DEFAULT_POLICY } from './verificationPolicy';
import { ALL_LAYERS, Claim, Extraction, LayerName, LayerResult, Decision, hashCode, ofType, unknown, extractionLimits } from './verificationTypes';
export interface VerificationRequest {code:string;spec:any;input_bindings?:Record<string,any>;task_id?:string;}
export interface VerificationDeps {runPyright?:RunPyright;allowPyright?:boolean;lookupPackage?:(name:string)=>Promise<PackageEvidence>;extract?:(p:{code:string;input_bindings?:Record<string,any>})=>Promise<Extraction>;policy?:DecisionPolicy;}
export interface Verification {
  candidate_hash:string; spec_hash:string; bindings_hash:string; extraction:Extraction;
  layers:LayerResult[]; ewcs_report:EWCSReport; decision:Decision;
  evidence:{packages:Record<string,PackageEvidence>;pyright:PyrightResult|null};
}
export async function verifyCandidate(request:VerificationRequest,deps:VerificationDeps={}):Promise<Verification> {
  const code=request.code, candidate_hash=hashCode(code), snapshot=structuredClone(request.spec), bindings=structuredClone(request.input_bindings || {});
  let extraction:Extraction;
  try {extraction=await (deps.extract || extractClaims)({code,input_bindings:bindings});}
  catch(e) {extraction={claims:[],complete:false,issues:[],error:String(e)};}
  if (!extraction || !Array.isArray(extraction.claims) || typeof extraction.complete!=='boolean') extraction={claims:[],complete:false,issues:[],error:'Malformed extractor response.'};
  if(extraction.candidate_hash && extraction.candidate_hash!==candidate_hash) extraction={claims:[],complete:false,issues:[],error:'Extraction candidate hash mismatch.'};
  if(extraction.error) extraction.complete=false;
  const packages:Record<string,PackageEvidence>=Object.create(null);
  for(const imp of ofType(extraction.claims,'import')) {
    const name=String(imp.library || '').split('.')[0];
    if(imp.stdlib || imp.local || Object.hasOwn(packages,name))continue;
    try {packages[name]=await (deps.lookupPackage || (name=>queryPypi({library_name:name})))(name);}
    catch(e) {packages[name]={exists:null,status:'unverifiable',summary:String(e)};}
  }
  let pyright:PyrightResult|null=null, pyrightPromise:Promise<PyrightResult>|null=null;
  const run=deps.runPyright || createPyrightRunner();
  const cached:RunPyright=(p)=> {
    if(p.python!==code) throw new Error('Checker must analyze the exact candidate.');
    if(!pyrightPromise) pyrightPromise=run(p).then(r=>{pyright=r;return r;});
    return pyrightPromise;
  };
  const claims=extraction.claims;
  const actions:Record<LayerName,()=>Promise<LayerResult>>={
    interface:()=>verifyInterface({claims,pypi_data:packages}), identifier:()=>verifyIdentifier(code,cached,deps.allowPyright!==false,extraction),
    access_point:()=>verifyAccessPoint({claims,spec:snapshot}), input_contract:()=>verifyInputContract({claims,spec:snapshot}),
    output_contract:()=>verifyOutputContract({claims,spec:snapshot,code},cached,deps.allowPyright!==false),
    contextual:()=>verifyContextual({claims,spec:snapshot})
  };
  const failed:LayerName[]=[],layers:LayerResult[]=[];
  const limits=extractionLimits(extraction);
  for(const layer of ALL_LAYERS) {
    try {
      let r=await actions[layer]();
      if(!r || r.layer!==layer) throw new Error('Missing/mismatched layer result.');
      if(limits.layers.has(layer) && r.state==='not_applicable') r=unknown(layer,'Extraction was incomplete for this layer; absence of relevant claims does not establish inapplicability.');
      layers.push(r);
    } catch(e) {failed.push(layer);layers.push(unknown(layer,`Required verifier failed: ${String(e)}`));}
  }
  const ewcs_report=computeEwcs({layer_results:layers,task_id:request.task_id,extraction_complete:extraction.complete,failed_layers:failed});
  ewcs_report.candidate_hash=candidate_hash;
  return {candidate_hash,spec_hash:hashCode(JSON.stringify(snapshot ?? null)),bindings_hash:hashCode(JSON.stringify(bindings)),extraction,layers,ewcs_report,
    decision:makeDecision(ewcs_report,0,deps.policy ?? DEFAULT_POLICY),evidence:{packages,pyright}};
}
export interface Attempt {code:string;verification:Verification;}
export async function runIntervention(request:VerificationRequest,deps:VerificationDeps & {
  correct?:(context:{code:string;verification:Verification;spec:any;input_bindings:Record<string,any>})=>Promise<string>;
}={}) {
  // Freeze task evidence across the single correction attempt.
  const frozen={...request,spec:structuredClone(request.spec),input_bindings:structuredClone(request.input_bindings || {})};
  const attempts:Attempt[]=[{code:request.code,verification:await verifyCandidate(frozen,deps)}];
  let correction_error:string|null=null;
  if(attempts[0].verification.decision==='correct' && deps.correct) {
    try {
      const revised=await deps.correct({code:request.code,verification:structuredClone(attempts[0].verification),spec:structuredClone(frozen.spec),input_bindings:structuredClone(frozen.input_bindings)});
      if(typeof revised!=='string' || !revised.trim()) throw new Error('Correction produced no code.');
      attempts.push({code:revised,verification:await verifyCandidate({...frozen,code:revised},deps)});
    } catch(e) {correction_error=String(e);}
  }
  const last=attempts[attempts.length-1], raw=makeDecision(last.verification.ewcs_report,attempts.length-1,deps.policy ?? DEFAULT_POLICY);
  const decision:Decision=raw==='correct' || correction_error?'abstain':raw;
  const rendered=presentReport({code:last.code,ewcs_report:last.verification.ewcs_report,decision,policy:deps.policy ?? DEFAULT_POLICY});
  return {decision:rendered.decision,delivered_code:rendered.code_included?last.code:null,report:rendered.report,attempts,
    correction_attempted:attempts[0].verification.decision==='correct' && !!deps.correct,correction_error};
}
