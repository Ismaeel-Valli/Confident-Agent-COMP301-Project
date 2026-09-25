/** LM Studio diagnostic tools. Use the external controller for enforced final delivery. */
import { tool, type Tool } from '@lmstudio/sdk';
import { mkdir, writeFile } from 'fs/promises';
import { dirname, isAbsolute, relative, resolve } from 'path';
import { z } from 'zod';
import { extractClaims } from './claimExtractor';
import { queryPypi, verifyInterface } from './packageEvidence';
import { resolveApiSpec } from './specDiscovery';
import { verifyIdentifier, RunPyright } from './pyrightRunner';
import { verifyAccessPoint, verifyInputContract, verifyOutputContract, verifyContextual } from './openApiVerifier';
import { computeEwcs, makeDecision, presentReport, EWCSReport } from './verificationPolicy';
import { runIntervention } from './verificationController';
import { LayerResult } from './verificationTypes';
import { BUNDLED_REFERENCES, TOOLBOX_VERSION } from './bundledReferences';
import { evidenceFor, hostsFromClaims, hostsFromCode } from './evidenceRegistry';
export * from './verificationTypes';
export { EWCSAccumulator } from './verificationPolicy';
export type { EWCSReport, LayerContribution } from './verificationPolicy';
export interface ConfidenceAgentToolsDeps {isEnabled:boolean;allowPyright:boolean;getWorkingDirectory:()=>string;runPyright:RunPyright;}
export function createConfidenceAgentTools(deps:ConfidenceAgentToolsDeps):Tool[] {
  const claims=z.array(z.record(z.any())), spec=z.record(z.any()).nullable().optional();
  const out:Tool[]=[];
  function add(name:string,description:string,parameters:Record<string,z.ZodTypeAny>,implementation:(p:any)=>Promise<any>) {
    out.push(tool({name,description,parameters,implementation:async (p:any)=> {
      if(!deps.isEnabled)throw new Error('Confidence Agent tools are disabled in plugin settings.');
      try {return await implementation(p);} catch(e) {return {error:String(e)};}
    }}));
  }
  // Layer tools resolve frozen evidence from the claims' hosts; a model-supplied spec is used only for unknown hosts.
  const withEvidence=(fn:(p:any)=>Promise<any>)=>async (p:any)=> {
    const {spec:selected,source}=evidenceFor(hostsFromClaims(p.claims || []),p.spec);
    const r=await fn({...p,spec:selected});
    return r && typeof r==='object' ? {...r,evidence_source_selection:source} : r;
  };
  add('verify_candidate','Run all six verifiers, score and report exact candidate API claims. Pass only the code: frozen evidence for JSONPlaceholder, GitHub, Open-Meteo, DummyJSON, REST Countries and Petstore is selected from the host the code calls. Never write or copy a specification. Does not prove task behavior. External controller enforces delivery and one correction.',
    {code:z.string(),spec,reference_id:z.enum(['jsonplaceholder-posts']).optional(),input_bindings:z.record(z.any()).optional(),task_id:z.string().optional()},async p=> {
      if (p.reference_id && p.spec != null) throw new Error('Supply reference_id or spec, not both.');
      const selected = p.reference_id ? {spec:structuredClone(BUNDLED_REFERENCES[p.reference_id]),source:`Bundled reference ${p.reference_id}.`} : evidenceFor(hostsFromCode(p.code),p.spec);
      const reference = selected.spec;
      const r=await runIntervention({...p,spec:reference},{runPyright:deps.runPyright,allowPyright:deps.allowPyright});
      const v=r.attempts[r.attempts.length-1].verification;
      return {toolbox_version:TOOLBOX_VERSION,decision:r.decision,report:r.report,candidate_hash:v.candidate_hash,
        reference_id:p.reference_id ?? null,evidence_selection:selected.source,spec_hash:v.spec_hash,reference_evidence:reference?.['x-confidence-evidence'] ?? null,
        ewcs_report:v.ewcs_report,layers:v.layers,extraction_issues:v.extraction.issues};
    });
  // Returns a summary only. The full document is never placed in the chat: it floods a small
  // model's context (a Petstore pilot run stopped after the spec was pasted three times),
  // and verification selects frozen evidence itself.
  add('resolve_api_spec','Discovery only: report whether a JSON OpenAPI 3.0 document exists at common paths, with its source and hash. Does not return the document; verify_candidate selects frozen evidence itself.',{base_url:z.string()},async p=> {
    const r:any=await resolveApiSpec(p);
    if (!r.spec) return r;
    const operations=Object.values<any>(r.spec.paths || {}).reduce((n,item)=>n+Object.keys(item || {}).filter(k=>['get','put','post','delete','patch','head','options'].includes(k)).length,0);
    return {found:true,source_url:r.source_url,retrieved_at:r.retrieved_at,content_hash:r.content_hash,openapi:r.spec.openapi,title:r.spec.info?.title,version:r.spec.info?.version,operations,
      note:'Summary only. Do not pass a specification to verification tools; call verify_candidate with the code and frozen evidence is selected by host.'};
  });
  add('query_pypi','Query package metadata. exists:null/status:unverifiable means lookup failed, not that the package is nonexistent.',{library_name:z.string()},queryPypi);
  add('extract_claims','Static Python extraction for a documented requests subset. Returns complete/limitations, operation-linked claims and a candidate hash. Runtime input values can be bound explicitly.',{code:z.string(),input_bindings:z.record(z.any()).optional()},extractClaims);
  add('verify_interface','Check imports against registry evidence and explicit import/distribution mappings. Missing evidence and registry failures stay unverifiable.',{claims,pypi_data:z.record(z.any()).optional()},verifyInterface);
  add('verify_identifier','Check structured Pyright diagnostics for the exact code. Missing packages/stubs and process failure are unverifiable.',{code:z.string()},p=>verifyIdentifier(p.code,deps.runPyright,deps.allowPyright));
  add('verify_access_point','Match server origin/base path, endpoint and HTTP method. Dynamic endpoints and unsupported specs remain unverifiable.',{claims,spec},withEvidence(verifyAccessPoint));
  add('verify_input_contract','Check every request separately: required parameters, locations, supported values and JSON bodies. Runtime values are noted, not guessed; unknown keys block verification.',{claims,spec},withEvidence(verifyInputContract));
  add('verify_output_contract','Follow response provenance and local references to success schemas. A clean Pyright run never substitutes for JSON response evidence.',{claims,spec,code:z.string().optional()},withEvidence(p=>verifyOutputContract(p,deps.runPyright,deps.allowPyright)));
  add('verify_contextual','Check operation-level inherited authentication alternatives against actual request arguments. Comments are not authentication.',{claims,spec,code:z.string().optional()},withEvidence(verifyContextual));
  add('compute_ewcs','Diagnostic score with canonical weights; missing checks retain weight and an empty applicable set has ewcs:null. Controller results are authoritative.',
    {layer_results:z.array(z.record(z.any())),task_id:z.string().optional(),extraction_complete:z.boolean().optional()},p=>Promise.resolve(computeEwcs(p as {layer_results:LayerResult[]})));
  add('make_decision','Validate all six contributions. Contradiction requests correction; incomplete/unverifiable critical checks abstain before thresholds 0.85/0.60.',{ewcs_report:z.record(z.any())},async p=>makeDecision(p.ewcs_report as EWCSReport));
  add('save_code','Save a candidate for inspection. This is not verified delivery; use the controller for user-facing output.',{code:z.string(),filename:z.string()},async p=> {
    const base=deps.getWorkingDirectory(),path=resolve(base,p.filename),rel=relative(base,path);
    if(!p.filename.trim() || rel.startsWith('..') || isAbsolute(rel))throw new Error('Invalid workspace-relative filename.');
    await mkdir(dirname(path),{recursive:true});await writeFile(path,p.code,'utf8');return {path};
  });
  add('present_report','Format a score report. Code is withheld for abstain/correct and inconsistent delivery requests. Native chat remains model controlled; use the external controller for enforcement.',
    {code:z.string(),ewcs_report:z.record(z.any()),decision:z.enum(['deliver','deliver_with_flag','correct','abstain'])},async p=>presentReport(p));
  return out;
}
