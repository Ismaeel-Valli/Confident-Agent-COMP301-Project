import { Claim, LayerName, LayerResult, EvidenceTier, ofType, result, unknown, aggregateExtracted } from './verificationTypes';
import { RunPyright, parsePyright } from './pyrightRunner';
type Check = {bad: string[]; unknown: string[]};
const empty = (): Check => ({bad:[], unknown:[]});
const merge = (a:Check,b:Check) => { a.bad.push(...b.bad); a.unknown.push(...b.unknown); return a; };
const own = (v:any,k:string) => v != null && Object.hasOwn(v,k);
function tier(spec:any): EvidenceTier { return spec?.['x-confidence-evidence']?.kind === 'curated' ? 'tier_2' : 'tier_1'; }
function finish(layer:LayerName,c:Check,spec:any,success:string): LayerResult {
  if (c.bad.length) return result(layer,'verified_incorrect',tier(spec),'OpenAPI contract',c.bad.join('\n'),'contract_violation');
  if (c.unknown.length) return unknown(layer,c.unknown.join('\n'));
  return result(layer,'verified_correct',tier(spec),'OpenAPI contract',success);
}
export function deref(value:any,spec:any): {value?:any;error?:string} {
  const seen = new Set<string>();
  while (value && typeof value === 'object' && own(value,'$ref')) {
    const ref = value.$ref;
    if (typeof ref !== 'string' || !ref.startsWith('#/')) return {error:'External or invalid $ref is unsupported.'};
    if (seen.has(ref)) return {error:'Cyclic reference is unresolved.'};
    seen.add(ref);
    let target:any = spec;
    for (const key of ref.slice(2).split('/').map((k:string) => k.replace(/~1/g,'/').replace(/~0/g,'~'))) {
      if (!own(target,key)) return {error:`Unresolved reference ${ref}`};
      target = target[key];
    }
    // OpenAPI 3.0 ignores siblings of a Reference Object.
    value = target;
  }
  if (!value || typeof value !== 'object' || Array.isArray(value)) return {error:'Missing or unsupported schema/object.'};
  return {value};
}
function specProblem(spec:any): string | undefined {
  if (!spec) return 'No API specification available.';
  if (own(spec, 'spec') && !own(spec, 'openapi')) return 'Received a discovery-result wrapper. Pass its spec field (the OpenAPI document or null), or use a bundled reference with verify_candidate.';
  if (!/^3\.0\./.test(spec.openapi || '')) return 'Only OpenAPI 3.0.x contracts are currently supported.';
  if (!spec.paths || typeof spec.paths !== 'object' || Array.isArray(spec.paths)) return 'Specification has no valid paths map.';
}
export interface Operation {pathKey:string; operation:any; pathItem:any; params:Record<string,string>; url:URL;}
export function findOperation(spec:any, endpoint:Claim): {match?:Operation;bad?:string;unknown?:string} {
  const problem = specProblem(spec);
  if (problem) return {unknown:problem};
  if (endpoint.resolved === false || typeof endpoint.endpoint !== 'string' || typeof endpoint.http_method !== 'string') return {unknown:'Endpoint or method is dynamic/unresolved.'};
  let url:URL;
  try { url = new URL(endpoint.endpoint); } catch { return {unknown:'An absolute endpoint URL is required to establish the server.'}; }
  if (!['http:','https:'].includes(url.protocol)) return {bad:'The request does not use an HTTP(S) URL.'};
  if (url.username || url.password) return {unknown:'Credentials embedded in URLs are outside supported authentication analysis.'};
  let serverKnown = false, serverMatches = false, uncertainServer = false;
  const matches:Operation[] = [];
  for (const pathKey of Object.keys(spec.paths).sort((a,b) => Number(a.includes('{')) - Number(b.includes('{')))) {
    const item = deref(spec.paths[pathKey],spec);
    if (item.error) { uncertainServer = true; continue; }
    const pathItem = item.value, operation = pathItem[endpoint.http_method.toLowerCase()];
    const servers = operation?.servers ?? pathItem.servers ?? spec.servers;
    if (!Array.isArray(servers) || !servers.length) { uncertainServer = true; continue; }
    for (const server of servers) {
      if (typeof server.url !== 'string' || server.url.includes('{')) { uncertainServer = true; continue; }
      let base:URL;
      try { base = new URL(server.url); } catch { uncertainServer = true; continue; }
      serverKnown = true;
      if (base.origin !== url.origin) continue;
      const prefix = base.pathname.replace(/\/$/,'');
      if (url.pathname !== prefix && !url.pathname.startsWith(prefix + '/')) continue;
      serverMatches = true;
      const path = url.pathname.slice(prefix.length) || '/';
      const keys:string[] = [];
      const regex = '^' + pathKey.split('/').map(segment => {
        const m = /^\{([^}]+)\}$/.exec(segment);
        if (m) { keys.push(m[1]); return '([^/]+)'; }
        return segment.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
      }).join('/') + '$';
      const m = new RegExp(regex).exec(path);
      if (!m || !operation || typeof operation !== 'object') continue;
      let params:Record<string,string>;
      try { params = Object.fromEntries(keys.map((k,i) => [k,decodeURIComponent(m[i+1])])); }
      catch { return {unknown:'Invalid percent-encoding in the path.'}; }
      matches.push({pathKey,operation,pathItem,params,url});
    }
  }
  if (matches.length) {
    const exact = matches.filter(m => !m.pathKey.includes('{'));
    const selected = exact.length ? exact : matches;
    if (new Set(selected.map(m => m.pathKey)).size > 1) return {unknown:'Ambiguous templated path match.'};
    return {match:selected[0]};
  }
  if (!serverKnown || uncertainServer) return {unknown:'Server identity or operation could not be resolved from the specification.'};
  if (!serverMatches) return {bad:`Endpoint origin/base path does not match the declared API servers: ${url.origin}${url.pathname}`};
  if (spec['x-confidence-evidence']?.partial) return {unknown:'Operation is outside the curated reference subset.'};
  return {bad:`No declared operation matches ${endpoint.http_method} ${url.pathname}.`};
}
const supported = new Set(['type','properties','required','items','additionalProperties','enum','nullable','minimum','maximum','exclusiveMinimum','exclusiveMaximum','minLength','maxLength','pattern','minItems','maxItems','uniqueItems','minProperties','maxProperties','multipleOf','title','description','default','example','examples','deprecated','readOnly','writeOnly','xml','externalDocs']);
function schemaProblems(schema:any):string[] {
  const errors = Object.keys(schema).filter(k => !supported.has(k) && !k.startsWith('x-')).map(k => `Unsupported schema constraint: ${k}`);
  if (schema.required !== undefined && (!Array.isArray(schema.required) || schema.required.some((x:any)=>typeof x !== 'string'))) errors.push('Invalid required declaration.');
  if (schema.enum !== undefined && !Array.isArray(schema.enum)) errors.push('Invalid enum declaration.');
  if (schema.type !== undefined && !['object','array','string','integer','number','boolean'].includes(schema.type)) errors.push('Unsupported schema type.');
  if (schema.properties !== undefined && (!schema.properties || typeof schema.properties !== 'object' || Array.isArray(schema.properties))) errors.push('Invalid properties declaration.');
  for (const key of ['nullable','uniqueItems','exclusiveMinimum','exclusiveMaximum','readOnly','writeOnly']) if (schema[key] !== undefined && typeof schema[key] !== 'boolean') errors.push('Invalid '+key+' declaration.');
  for (const key of ['minimum','maximum','multipleOf','minLength','maxLength','minItems','maxItems','minProperties','maxProperties']) if (schema[key] !== undefined && (typeof schema[key] !== 'number' || !Number.isFinite(schema[key]))) errors.push('Invalid '+key+' declaration.');
  return errors;
}
export function checkValue(value:any,raw:any,spec:any,label:string,serialized=false,depth=0):Check {
  const c=empty();
  if (depth>30) {c.unknown.push(`${label}: schema depth limit`);return c;}
  const resolved=deref(raw,spec);
  if (resolved.error) {c.unknown.push(`${label}: ${resolved.error}`);return c;}
  const s=resolved.value;
  c.unknown.push(...schemaProblems(s).map(x=>`${label}: ${x}`));
  if (c.unknown.length) return c;
  if (value===null && s.nullable===true) return c;
  let v=value;
  if (serialized && typeof v==='string') {
    if ((s.type==='integer' || s.type==='number') && /^-?(?:0|[1-9]\d*)(?:\.\d+)?$/.test(v)) v=Number(v);
    if (s.type==='boolean' && ['true','false'].includes(v)) v=v==='true';
  }
  const type=s.type;
  const valid = type==='string' ? typeof v==='string' : type==='integer' ? Number.isInteger(v) : type==='number' ? typeof v==='number' && Number.isFinite(v)
    : type==='boolean' ? typeof v==='boolean' : type==='array' ? Array.isArray(v) : type==='object' ? v!==null && typeof v==='object' && !Array.isArray(v) : false;
  if (!type) {c.unknown.push(`${label}: schema type is unspecified.`);return c;}
  else if (!valid) {c.bad.push(`${label}: expected ${type}.`);return c;}
  if (Array.isArray(s.enum) && !s.enum.some((x:any)=>JSON.stringify(x)===JSON.stringify(v))) c.bad.push(`${label}: value is outside enum.`);
  if (typeof v==='number') {
    if (s.minimum!==undefined && (s.exclusiveMinimum ? v<=s.minimum : v<s.minimum)) c.bad.push(`${label}: below minimum.`);
    if (s.maximum!==undefined && (s.exclusiveMaximum ? v>=s.maximum : v>s.maximum)) c.bad.push(`${label}: above maximum.`);
    if (s.multipleOf!==undefined && (s.multipleOf<=0 || Math.abs(v/s.multipleOf-Math.round(v/s.multipleOf))>1e-9)) c.bad.push(`${label}: violates multipleOf.`);
  }
  if (typeof v==='string') {
    const length=[...v].length;
    if (s.minLength!==undefined && length<s.minLength || s.maxLength!==undefined && length>s.maxLength) c.bad.push(`${label}: invalid string length.`);
    if (typeof s.pattern==='string') {
      try {if (!new RegExp(s.pattern,'u').test(v)) c.bad.push(`${label}: pattern mismatch.`);} catch {c.unknown.push(`${label}: unsupported regular expression.`);}
    }
  }
  if (Array.isArray(v)) {
    if (s.minItems!==undefined && v.length<s.minItems || s.maxItems!==undefined && v.length>s.maxItems) c.bad.push(`${label}: invalid array length.`);
    if (s.uniqueItems && new Set(v.map(x=>JSON.stringify(x))).size!==v.length) c.bad.push(`${label}: items are not unique.`);
    v.forEach((x,i)=>merge(c,checkValue(x,s.items,spec,`${label}[${i}]`,false,depth+1)));
  } else if (v && typeof v==='object') {
    if (s.minProperties!==undefined && Object.keys(v).length<s.minProperties || s.maxProperties!==undefined && Object.keys(v).length>s.maxProperties) c.bad.push(`${label}: invalid property count.`);
    for (const required of s.required || []) if (!own(v,required) && !deref(s.properties?.[required],spec).value?.readOnly) c.bad.push(`${label}: missing required property ${required}.`);
    for (const [key,val] of Object.entries(v)) {
      if (own(s.properties,key)) {
        if (deref(s.properties[key],spec).value?.readOnly) c.bad.push(`${label}.${key}: readOnly property sent in request.`);
        merge(c,checkValue(val,s.properties[key],spec,`${label}.${key}`,false,depth+1));
      } else if (s.additionalProperties===false) c.bad.push(`${label}: undeclared property ${key}.`);
      else if (typeof s.additionalProperties==='object') merge(c,checkValue(val,s.additionalProperties,spec,`${label}.${key}`,false,depth+1));
    }
  }
  return c;
}
function locate(layer:LayerName,spec:any,ep:Claim):{match?:Operation;row?:LayerResult} {
  const found=findOperation(spec,ep);
  if (found.match) return {match:found.match};
  return {row:found.bad && layer==='access_point' ? finish(layer,{bad:[found.bad],unknown:[]},spec,'') : unknown(layer,found.unknown || found.bad || 'Operation unresolved.')};
}
export async function verifyAccessPoint({claims,spec}:{claims:Claim[];spec:any}) {
  return aggregateExtracted('access_point',claims,ofType(claims,'endpoint').map(ep=> {
    const l=locate('access_point',spec,ep);
    return l.row || result('access_point','verified_correct',tier(spec),'OpenAPI servers + path + method',`${ep.http_method} ${ep.endpoint} matches the declared server and operation.`);
  }),'No HTTP calls in the supported extraction.');
}
function parameters(match:Operation,spec:any):{values:any[];errors:string[]} {
  const map=new Map<string,any>(), errors:string[]=[];
  for (const list of [match.pathItem.parameters,match.operation.parameters]) {
    if (list!==undefined && !Array.isArray(list)) {errors.push('Invalid parameter declaration.');continue;}
    for (const raw of list || []) {
      const p=deref(raw,spec);
      if (p.error) {errors.push(p.error);continue;}
      if (typeof p.value.name!=='string' || !['path','query','header','cookie'].includes(p.value.in)) {errors.push('Invalid parameter name/location.');continue;}
      const key=p.value.in+':'+(p.value.in==='header'?p.value.name.toLowerCase():p.value.name);
      map.set(key,p.value);
    }
  }
  return {values:[...map.values()],errors};
}
function fields(ep:Claim,via:string):{values:Record<string,{known:boolean;value:any}>;complete:boolean} {
  const container=ep.request?.[via];
  if (!container) return {values:{},complete:ep.request_complete===true};
  if (container.known && container.value===null) return {values:{},complete:true};
  if (!container.keys_known) return {values:{},complete:false};
  const values:Record<string,{known:boolean;value:any}>=Object.create(null);
  for (const [k,v] of Object.entries(container.fields || {}) as Array<[string,any]>) values[via==='headers'?k.toLowerCase():k]=v;
  return {values,complete:true};
}
function requestFields(ep:Claim,match:Operation) {
  const query=fields(ep,'params');
  for (const [key,value] of match.url.searchParams) {
    if (own(query.values,key)) query.complete=false; // duplicate serialization not guessed
    else query.values[key]={known:true,value};
  }
  return {query,header:fields(ep,'headers'),cookie:fields(ep,'cookies'),path:{values:Object.fromEntries(Object.entries(match.params).map(([k,v])=>[k,{known:true,value:v}])),complete:true}};
}
function securityNames(spec:any,operation:any):Record<string,Set<string>> {
  const names:Record<string,Set<string>>={header:new Set(['authorization','content-type','accept','user-agent']),query:new Set(),cookie:new Set()};
  const requirements=operation.security ?? spec.security ?? [];
  const requiredNames=new Set((Array.isArray(requirements)?requirements:[]).flatMap(r=>Object.keys(r || {})));
  for (const [name,raw] of Object.entries(spec.components?.securitySchemes || {})) {
    if (!requiredNames.has(name)) continue;
    const s=deref(raw,spec).value;
    if (s?.type==='apiKey' && names[s.in] && typeof s.name==='string') names[s.in].add(s.in==='header'?s.name.toLowerCase():s.name);
  }
  return names;
}
export async function verifyInputContract({claims,spec}:{claims:Claim[];spec:any}) {
  const rows=ofType(claims,'endpoint').map(ep=> {
    const l=locate('input_contract',spec,ep); if (l.row) return l.row;
    const m=l.match!, c=empty(), pars=parameters(m,spec), sent=requestFields(ep,m);
    c.unknown.push(...pars.errors);
    if (!ep.request || ep.request_complete!==true) c.unknown.push('Request extraction is incomplete; required inputs cannot be established.');
    for (const p of pars.values) {
      const location=sent[p.in as keyof typeof sent], key=p.in==='header'?p.name.toLowerCase():p.name;
      const val=location.values[key];
      if (!val || val.known && val.value===null) {
        if (p.required) (location.complete ? c.bad : c.unknown).push(`Missing required ${p.in} parameter ${p.name}.`);
      } else if (!val.known) c.unknown.push(`Value of ${p.in} parameter ${p.name} is unresolved.`);
      else {
        if (p.content || p.style && p.style !== (['query','cookie'].includes(p.in)?'form':'simple') || p.schema?.type==='array' || p.schema?.type==='object') c.unknown.push(`Unsupported parameter serialization: ${p.name}`);
        merge(c,checkValue(val.value,p.schema,spec,`${p.in}.${p.name}`,true));
      }
    }
    const authNames=securityNames(spec,m.operation);
    for (const loc of ['query','header','cookie'] as const) {
      if (!sent[loc].complete) c.unknown.push(`${loc} dictionary has unresolved keys.`);
      const declared=new Set(pars.values.filter(p=>p.in===loc).map(p=>loc==='header'?p.name.toLowerCase():p.name));
      for (const key of Object.keys(sent[loc].values)) if (!declared.has(key) && !authNames[loc].has(key)) {
        // OpenAPI does not forbid extra query/header/cookie parameters by default.
        c.unknown.push(`Undeclared ${loc} parameter ${key}; acceptance is undocumented.`);
      }
    }
    const auth=ep.request?.auth;
    if (auth?.provided && !(auth.known && (auth.value===null || Array.isArray(auth.value) && auth.value.length===2 && auth.value.every((v:any)=>typeof v==='string')))) c.unknown.push('Custom/dynamic request authentication is outside the supported subset.');
    const rb=deref(m.operation.requestBody,spec);
    const body=ep.request?.json, form=ep.request?.data;
    if (body?.provided && (!body.known || body.value!==null)) {
      const contentType=sent.header.values['content-type'];
      if (contentType && !contentType.known) c.unknown.push('Request Content-Type is unresolved.');
      else if (contentType && (typeof contentType.value!=='string' || contentType.value.split(';')[0].trim().toLowerCase()!=='application/json')) c.bad.push('JSON body sent with a non-JSON Content-Type.');
    }
    if (form?.provided && !(form.known && form.value===null)) c.unknown.push('Form/raw body encoding is unsupported.');
    if (m.operation.requestBody) {
      if (rb.error) c.unknown.push(rb.error);
      else {
        if (rb.value.required && (!body?.provided || body.known && body.value===null) && !form?.provided) c.bad.push('Required request body is missing.');
        if (body?.provided && body.value!==null) {
          const schema=rb.value.content?.['application/json']?.schema;
          if (!schema) c.unknown.push('No JSON request schema available.');
          else if (!body.known) c.unknown.push('Request body includes unresolved values.');
          else merge(c,checkValue(body.value,schema,spec,'body'));
        } else if (body?.provided && !body.known) c.unknown.push('Request body is unresolved.');
      }
    } else if (body?.provided && (!body.known || body.value!==null)) c.unknown.push('Code sends a JSON body with no declared request-body contract.');
    return finish('input_contract',c,spec,`Required inputs, locations and supported value constraints checked for ${ep.call_id}.`);
  });
  return aggregateExtracted('input_contract',claims,rows,'No HTTP calls; no input contract to check.');
}
function checkOutputPath(path:any[],raw:any,spec:any,optional=false):Check {
  const c=empty(); let schema=raw;
  for (const key of path) {
    const r=deref(schema,spec);
    if (r.error) {c.unknown.push(r.error);return c;}
    schema=r.value;
    c.unknown.push(...schemaProblems(schema));
    if (c.unknown.length) return c;
    if (!schema.type) {c.unknown.push('Response schema type is unspecified.');return c;}
    if (schema.nullable) c.unknown.push('Response container can be null.');
    if (typeof key==='number') {
      if (schema.type!=='array') {c.bad.push('Array indexing used on a non-array response.');return c;}
      if (!Number.isInteger(key)) {c.unknown.push('Non-integer response index.');return c;}
      // Existence of a particular array element is not established by its item schema.
      schema=schema.items;
    } else if (key==='*') {c.unknown.push('Dynamic response field is unresolved.');return c;}
    else {
      if (schema.type==='array') {c.bad.push(`String field ${key} read directly from an array.`);return c;}
      if (schema.type && schema.type!=='object') {c.bad.push(`Field ${key} read from a scalar response.`);return c;}
      if (!own(schema.properties,key)) {
        if (schema.additionalProperties===false) c.bad.push(`Response field ${key} is forbidden by the closed schema.`);
        else c.unknown.push(`Response field ${key} is not documented; schema allows unspecified properties.`);
        return c;
      }
      if (!optional && !(schema.required || []).includes(key)) c.unknown.push(`Response field ${key} is optional; presence is not guaranteed.`);
      schema=schema.properties[key];
      if (schema.writeOnly) c.unknown.push(`Response field ${key} is writeOnly.`);
    }
  }
  return c;
}
export async function verifyOutputContract({claims,spec,code}:{claims:Claim[];spec:any;code?:string},runPyright?:RunPyright,allowPyright=true) {
  const outputs=ofType(claims,'output_field');
  if (!outputs.length) return aggregateExtracted('output_contract',claims,[],'No tracked response-field accesses.');
  const rows:LayerResult[]=[];
  for (const f of outputs) {
    const ep=ofType(claims,'endpoint').find(e=>e.call_id===f.call_id);
    if (!ep) {rows.push(unknown('output_contract','Response access is not linked to an HTTP operation.'));continue;}
    const l=locate('output_contract',spec,ep);
    if (l.row) {rows.push(l.row);continue;}
    const responses=l.match!.operation.responses || {};
    const success=Object.entries(responses).filter(([k])=>/^2\d\d$/.test(k) || k==='2XX');
    if (!success.length) {rows.push(unknown('output_contract','No documented success-response schema; a default/error response is insufficient.'));continue;}
    const checks=success.map(([status,raw])=> {
      const r=deref(raw,spec);
      if (r.error) return {bad:[],unknown:[r.error]};
      const schema=r.value.content?.['application/json']?.schema;
      if (!schema) return {bad:[],unknown:[`No JSON schema for success status ${status}.`]};
      return checkOutputPath(Array.isArray(f.path)?f.path:[f.field],schema,spec,f.optional_access===true);
    });
    const combined=empty();
    if (checks.every(c=>c.bad.length)) combined.bad.push(...checks.flatMap(c=>c.bad));
    else {
      combined.unknown.push(...checks.flatMap(c=>c.unknown));
      if (checks.some(c=>c.bad.length)) combined.unknown.push('Field validity depends on an unresolved success status.');
    }
    rows.push(finish('output_contract',combined,spec,`Response path ${JSON.stringify(f.path || [f.field])} is documented for ${f.call_id}.`));
  }
  const verdict=aggregateExtracted('output_contract',claims,rows,'No output checks.');
  if (verdict.state==='unverifiable' && code && runPyright && allowPyright) {
    try {
      const p=parsePyright(await runPyright({python:code}),code);
      verdict.evidence_detail+='\n'+(p.error?`Pyright unavailable: ${p.error}`:'Pyright cannot establish untyped JSON response contracts; result remains unverifiable.');
    } catch(e) {verdict.evidence_detail+=`\nPyright unavailable: ${String(e)}`;}
  }
  return verdict;
}
function authCheck(name:string,scopes:any,ep:Claim,match:Operation,spec:any):Check {
  const c=empty(), resolved=deref(spec.components?.securitySchemes?.[name],spec);
  if (resolved.error) {c.unknown.push(`Security scheme ${name}: ${resolved.error}`);return c;}
  const s=resolved.value, sent=requestFields(ep,match);
  let val:any, complete=false;
  if (s.type==='apiKey' && ['header','query','cookie'].includes(s.in)) {
    const loc=sent[s.in as 'header'|'query'|'cookie'];
    val=loc.values[s.in==='header'?String(s.name).toLowerCase():s.name]; complete=loc.complete;
  } else if (s.type==='http' && ['bearer','basic'].includes(s.scheme?.toLowerCase())) {
    val=sent.header.values.authorization;complete=sent.header.complete;
    if (!val && ep.request?.auth?.provided) {
      const a=ep.request.auth;
      if (s.scheme.toLowerCase()==='basic' && a.known && Array.isArray(a.value) && a.value.length===2 && a.value.every((x:any)=>typeof x==='string'&&x.length)) return c;
      c.unknown.push('Authentication adapter/value could not be established.');return c;
    }
    if (val?.known && typeof val.value==='string' && !(s.scheme.toLowerCase()==='bearer'?/^Bearer\s+\S+$/i:/^Basic\s+[A-Za-z0-9+/]+=*$/i).test(val.value)) c.bad.push(`Authorization header does not match ${s.scheme}.`);
  } else {c.unknown.push(`Unsupported authentication scheme/scopes: ${name} (${s.type}).`);return c;}
  if (Array.isArray(scopes) && scopes.length) c.unknown.push('Required OAuth scopes cannot be established statically.');
  if (!val) (complete?c.bad:c.unknown).push(`Required credential ${name} is absent from the request.`);
  else if (!val.known) c.unknown.push(`Credential ${name} has an unresolved runtime value.`);
  else if (typeof val.value!=='string' || !val.value.trim()) c.bad.push(`Credential ${name} is empty or invalid.`);
  return c;
}
export async function verifyContextual({claims,spec}:{claims:Claim[];spec:any;code?:string}) {
  const rows=ofType(claims,'endpoint').map(ep=> {
    const l=locate('contextual',spec,ep);if(l.row)return l.row;
    const m=l.match!, security=m.operation.security ?? spec.security ?? [];
    if (!Array.isArray(security)) return unknown('contextual','Invalid security requirements.');
    if (m.operation.deprecated) return unknown('contextual','Operation is deprecated; task-specific acceptability needs review.');
    if (!security.length || security.some(s=>s && typeof s==='object' && !Array.isArray(s) && !Object.keys(s).length)) return result('contextual','not_applicable','none','OpenAPI operation security','No authentication requirement for this operation. Unused security definitions are not requirements.');
    const alternatives=security.map(requirement=> {
      const c=empty();
      if (!requirement || typeof requirement!=='object' || Array.isArray(requirement)) {c.unknown.push('Invalid security alternative.');return c;}
      for (const [name,scopes] of Object.entries(requirement)) merge(c,authCheck(name,scopes,ep,m,spec));
      return c;
    });
    if (alternatives.some(c=>!c.bad.length && !c.unknown.length)) return finish('contextual',empty(),spec,'Required authentication placement and static shape match one security alternative. Credential validity is not tested.');
    if (alternatives.every(c=>c.bad.length)) return finish('contextual',{bad:alternatives.flatMap(c=>c.bad),unknown:[]},spec,'');
    return unknown('contextual',alternatives.flatMap(c=>[...c.bad,...c.unknown]).join('\n'));
  });
  return aggregateExtracted('contextual',claims,rows,'No HTTP calls requiring contextual checks.');
}
