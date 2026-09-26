import { Claim, LayerName, LayerResult, EvidenceTier, ofType, result, unknown, aggregateExtracted } from './verificationTypes';
import { RunPyright, parsePyright } from './pyrightRunner';
/**
 * bad: supported contradictions. unknown: unresolved critical checks.
 * notes: noncritical limits (runtime input values, optional presence, undeclared
 * headers). Notes are reported but do not change the check state.
 */
type Check = {bad: string[]; unknown: string[]; notes?: string[]};
const empty = (): Check => ({bad:[], unknown:[]});
const note = (c:Check, text:string) => { (c.notes ||= []).push(text); return c; };
const merge = (a:Check,b:Check) => { a.bad.push(...b.bad); a.unknown.push(...b.unknown); if (b.notes?.length) (a.notes ||= []).push(...b.notes); return a; };
const own = (v:any,k:string) => v != null && typeof v === 'object' && Object.hasOwn(v,k);
const evidenceOf = (spec:any) => (spec && typeof spec === 'object' && spec['x-confidence-evidence']) || {};
function tier(spec:any): EvidenceTier { return evidenceOf(spec).kind === 'curated' ? 'tier_2' : 'tier_1'; }
function finish(layer:LayerName,c:Check,spec:any,success:string): LayerResult {
  const notes = c.notes?.length ? '\nNoncritical: ' + [...new Set(c.notes)].join('; ') : '';
  if (c.bad.length) return result(layer,'verified_incorrect',tier(spec),'OpenAPI contract',c.bad.join('\n') + notes,'contract_violation');
  if (c.unknown.length) return unknown(layer,c.unknown.join('\n') + notes);
  return result(layer,'verified_correct',tier(spec),'OpenAPI contract',success + notes);
}

// ---------------------------------------------------------------- abstract values
// The extractor encodes runtime values as {$ca:'unknown'} and partially known strings
// as {$ca:'template', parts:[string | {hole}]}. Everything else is a concrete JSON value.
const isMarker = (v:any, kind:string) => v != null && typeof v === 'object' && !Array.isArray(v) && v.$ca === kind;
const isOpaque = (v:any) => isMarker(v,'unknown');
const isTemplate = (v:any) => isMarker(v,'template');
const isAbstract = (v:any) => isOpaque(v) || isTemplate(v);
function concrete(v:any):boolean {
  if (isAbstract(v)) return false;
  if (Array.isArray(v)) return v.every(concrete);
  if (v && typeof v === 'object') return Object.values(v).every(concrete);
  return true;
}
const templateText = (t:any) => (t.parts || []).map((p:any) => typeof p === 'string' ? p : `{${p.hole}}`).join('');
const describe = (v:any) => isTemplate(v) ? `template "${templateText(v)}"` : isOpaque(v) ? `runtime value ${v.label || ''}`.trim() : JSON.stringify(v);
/** Shape of a request container or field, tolerating claims from older extractors. */
function shapeOf(entry:any, fallbackLabel:string):any {
  if (entry == null) return undefined;
  if (own(entry,'shape')) return entry.shape;
  if (entry.known) return entry.value;
  if (entry.keys_known && entry.fields) return Object.fromEntries(Object.entries(entry.fields).map(([k,v]:[string,any]) => [k, shapeOf(v,k)]));
  return {$ca:'unknown', label:fallbackLabel, type:null};
}
const PY_TO_JSON: Record<string,string[]> = {str:['string'], int:['integer','number'], float:['number'], bool:['boolean'], dict:['object'], list:['array'], NoneType:['null']};

// ---------------------------------------------------------------- specification
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
    // OpenAPI 3.0 ignores siblings of a Reference Object; 3.1 schema siblings are merged by schemaView.
    value = target;
  }
  if (!value || typeof value !== 'object' || Array.isArray(value)) return {error:'Missing or unsupported schema/object.'};
  return {value};
}
const isOas31 = (spec:any) => /^3\.1\./.test(spec?.openapi || '');
function rootServers(spec:any):any[] {
  if (Array.isArray(spec.servers) && spec.servers.length) return spec.servers;
  const overlay = evidenceOf(spec).servers;
  return Array.isArray(overlay) ? overlay : [];
}
function specProblem(spec:any): string | undefined {
  if (!spec) return 'No API specification available.';
  // Discovery-result wrapper: {spec, source_url, ...} rather than the spec itself.
  if (own(spec, 'spec') && !own(spec, 'openapi')) return 'Received a discovery-result wrapper. Pass its spec field (the OpenAPI document or null), or use a bundled reference with verify_candidate.';
  // A PyPI datum accidentally passed in place of a spec.
  if (own(spec, 'distribution') || own(spec, 'import_name')) return 'Received a PyPI package datum, not an OpenAPI spec. Pass the spec field from resolve_api_spec (the OpenAPI document) or null.';
  // A discovery note accidentally passed in place of a spec.
  if (own(spec, 'note') && !own(spec, 'openapi')) return 'Received a discovery note, not an OpenAPI document. Pass the spec field from resolve_api_spec or null.';
  if (own(spec,'swagger')) return 'Swagger/OpenAPI 2.0 documents are not read as OpenAPI 3.x; convert and review them first.';
  if (!/^3\.[01]\./.test(spec.openapi || '')) return 'Only OpenAPI 3.0.x and 3.1.x contracts are supported.';
  if (!spec.paths || typeof spec.paths !== 'object' || Array.isArray(spec.paths)) return 'Specification has no valid paths map.';
  if (!rootServers(spec).length) return 'Specification has no servers array. A spec without a server URL cannot resolve endpoint origins. Supply a reviewed snapshot whose x-confidence-evidence.servers cites the official base URL.';
}
/** Absolute base URLs for a server list, expanding variables and resolving relative URLs. */
function serverBases(spec:any, servers:any[]):{bases:URL[];uncertain:boolean} {
  const bases:URL[] = []; let uncertain = false;
  const documentUrl = evidenceOf(spec).document_url;
  for (const server of servers) {
    if (!server || typeof server.url !== 'string') { uncertain = true; continue; }
    let urls = [server.url];
    for (const [name] of server.url.matchAll(/\{([^}]+)\}/g)) {
      const variable = server.variables?.[name.slice(1,-1)];
      if (!variable || typeof variable.default !== 'string') { uncertain = true; urls = []; break; }
      const options = Array.isArray(variable.enum) && variable.enum.length ? variable.enum : [variable.default];
      urls = urls.flatMap(u => options.map((o:string) => u.replace(name, o)));
    }
    for (const u of urls) {
      try { bases.push(documentUrl ? new URL(u, documentUrl) : new URL(u)); }
      catch { uncertain = true; }
    }
  }
  return {bases, uncertain};
}

// ---------------------------------------------------------------- request targets
type Segment = {lit:string} | {hole:string} | {mixed:any[]};
interface Target {origin?:string; segments?:Segment[]; query:{values:Record<string,any>;complete:boolean}; display:string; problem?:string}
const HOLE = '\u0000';
function parseTarget(ep:Claim):Target {
  const empty = {values:{},complete:true};
  if (typeof ep.endpoint === 'string') {
    let url:URL;
    try { url = new URL(ep.endpoint); } catch { return {query:empty,display:ep.endpoint,problem:'An absolute endpoint URL is required to establish the server.'}; }
    if (!['http:','https:'].includes(url.protocol)) return {query:empty,display:ep.endpoint,problem:'bad-protocol'};
    if (url.username || url.password) return {query:empty,display:ep.endpoint,problem:'Credentials embedded in URLs are outside supported authentication analysis.'};
    const values:Record<string,any> = Object.create(null); let complete = true;
    for (const [k,v] of url.searchParams) { if (own(values,k)) complete = false; else values[k] = v; }
    const segments = url.pathname.split('/').slice(1).map(s => { try { return {lit:decodeURIComponent(s)}; } catch { return {mixed:[s]}; } });
    return {origin:url.origin, segments, query:{values,complete}, display:`${url.origin}${url.pathname}`};
  }
  if (!isTemplate(ep.endpoint_template)) return {query:empty,display:'(dynamic)',problem:'Endpoint or method is dynamic/unresolved.'};
  const parts:any[] = ep.endpoint_template.parts, holes:string[] = [];
  const rendered = parts.map(p => typeof p === 'string' ? p.replace(/\u0000/g,'') : (holes.push(p.hole), HOLE)).join('');
  const display = templateText(ep.endpoint_template);
  const m = /^(https?):\/\/([^/?#\u0000]+)(?=$|[/?#])/i.exec(rendered);
  if (!m) return {query:empty,display,problem:'The endpoint origin is a runtime value; the server cannot be established.'};
  let origin:string;
  try { const u = new URL(m[0]); if (u.username || u.password) return {query:empty,display,problem:'Credentials embedded in URLs are outside supported authentication analysis.'}; origin = u.origin; }
  catch { return {query:empty,display,problem:'Invalid endpoint origin.'}; }
  let rest = rendered.slice(m[0].length).split('#')[0];
  const q = rest.indexOf('?');
  const pathText = q >= 0 ? rest.slice(0,q) : rest, queryText = q >= 0 ? rest.slice(q+1) : '';
  let holeIndex = 0;
  const fragment = (text:string):any => {
    // Rebuild a template value from rendered text, consuming holes in order.
    const pieces:any[] = [];
    text.split(HOLE).forEach((lit,i,all) => { if (lit) pieces.push(lit); if (i < all.length-1) pieces.push({hole:holes[holeIndex++] ?? 'value'}); });
    if (pieces.length === 1 && typeof pieces[0] !== 'string') return {$ca:'unknown', label:pieces[0].hole, type:'str'};
    return pieces.every(p => typeof p === 'string') ? pieces.join('') : {$ca:'template', parts:pieces};
  };
  const segments:Segment[] = (pathText || '/').split('/').slice(1).map(seg => {
    if (!seg.includes(HOLE)) { try { return {lit:decodeURIComponent(seg)}; } catch { return {mixed:[seg]}; } }
    const value = fragment(seg);
    return isOpaque(value) ? {hole:value.label} : {mixed:value.parts};
  });
  const values:Record<string,any> = Object.create(null); let complete = true;
  for (const pair of queryText ? queryText.split('&') : []) {
    const eq = pair.indexOf('='), key = eq >= 0 ? pair.slice(0,eq) : pair, raw = eq >= 0 ? pair.slice(eq+1) : '';
    if (key.includes(HOLE)) { complete = false; fragment(key); fragment(raw); continue; }
    let name:string; try { name = decodeURIComponent(key.replace(/\+/g,' ')); } catch { complete = false; continue; }
    const value = raw.includes(HOLE) ? fragment(raw) : (() => { try { return decodeURIComponent(raw.replace(/\+/g,' ')); } catch { return raw; } })();
    if (own(values,name)) complete = false; else values[name] = value;
  }
  return {origin, segments, query:{values,complete}, display};
}

export interface Operation {pathKey:string; operation:any; pathItem:any; params:Record<string,any>; query:{values:Record<string,any>;complete:boolean}; display:string;}
export function findOperation(spec:any, endpoint:Claim): {match?:Operation;bad?:string;unknown?:string} {
  const problem = specProblem(spec);
  if (problem) return {unknown:problem};
  if (endpoint.resolved === false || typeof endpoint.http_method !== 'string' || (typeof endpoint.endpoint !== 'string' && !isTemplate(endpoint.endpoint_template)))
    return {unknown:'Endpoint or method is dynamic/unresolved.'};
  const target = parseTarget(endpoint);
  if (target.problem === 'bad-protocol') return {bad:'The request does not use an HTTP(S) URL.'};
  if (target.problem || !target.segments) return {unknown:target.problem || 'Endpoint unresolved.'};
  let serverKnown = false, serverMatches = false, uncertainServer = false, prefixUnresolved = false;
  const matches:Operation[] = [];
  for (const pathKey of Object.keys(spec.paths)) {
    const item = deref(spec.paths[pathKey],spec);
    if (item.error) { uncertainServer = true; continue; }
    const pathItem = item.value, operation = pathItem[endpoint.http_method.toLowerCase()];
    const servers = operation?.servers ?? pathItem.servers ?? rootServers(spec);
    if (!Array.isArray(servers) || !servers.length) { uncertainServer = true; continue; }
    const {bases, uncertain} = serverBases(spec, servers);
    if (uncertain) uncertainServer = true;
    for (const base of bases) {
      serverKnown = true;
      if (base.origin !== target.origin) continue;
      const prefix = base.pathname.split('/').filter(Boolean).map(s => { try { return decodeURIComponent(s); } catch { return s; } });
      const segs = target.segments;
      const head = segs.slice(0, prefix.length);
      if (head.some(s => !('lit' in s))) { prefixUnresolved = true; continue; }
      if (segs.length < prefix.length || head.some((s,i) => (s as any).lit !== prefix[i])) continue;
      serverMatches = true;
      let rest = segs.slice(prefix.length);
      if (rest.length === 1 && 'lit' in rest[0] && rest[0].lit === '' ) rest = [];
      const keys = pathKey.split('/').slice(1);
      if (pathKey === '/') keys.length = 0;
      if (keys.length !== rest.length || !operation || typeof operation !== 'object') continue;
      const params:Record<string,any> = Object.create(null);
      let ok = true;
      keys.forEach((key,i) => {
        if (!ok) return;
        const seg = rest[i], whole = /^\{([^}]+)\}$/.exec(key);
        if (whole) {
          if ('lit' in seg) params[whole[1]] = seg.lit;
          else if ('hole' in seg) params[whole[1]] = {$ca:'unknown', label:seg.hole, type:'str'};
          else params[whole[1]] = {$ca:'template', parts:seg.mixed};
          return;
        }
        if (!key.includes('{')) { ok = 'lit' in seg && seg.lit === key; return; }
        // Partial-segment template, e.g. {id}.json: only literal code segments can be matched.
        if (!('lit' in seg)) { ok = false; return; }
        const names:string[] = [];
        const regex = new RegExp('^' + key.split(/(\{[^}]+\})/).map(p => { const n = /^\{([^}]+)\}$/.exec(p); if (n) { names.push(n[1]); return '([^/]+)'; } return p.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'); }).join('') + '$');
        const m = regex.exec(seg.lit);
        if (!m) { ok = false; return; }
        names.forEach((n,j) => { params[n] = m[j+1]; });
      });
      if (ok) matches.push({pathKey,operation,pathItem,params,query:target.query,display:target.display});
    }
  }
  if (matches.length) {
    const exact = matches.filter(m => !m.pathKey.includes('{'));
    const selected = exact.length ? exact : matches;
    if (new Set(selected.map(m => m.pathKey)).size > 1) return {unknown:'Ambiguous templated path match.'};
    return {match:selected[0]};
  }
  if (prefixUnresolved) return {unknown:'The server base path of the endpoint is a runtime value.'};
  if (!serverKnown || uncertainServer) return {unknown:'Server identity or operation could not be resolved from the specification.'};
  if (!serverMatches) return {bad:`Endpoint origin/base path does not match the declared API servers: ${target.display}`};
  if (evidenceOf(spec).partial) return {unknown:'Operation is outside the curated reference subset.'};
  return {bad:`No declared operation matches ${endpoint.http_method} ${target.display}.`};
}

// ---------------------------------------------------------------- schema values
const supported = new Set(['type','properties','required','items','additionalProperties','enum','nullable','minimum','maximum','exclusiveMinimum','exclusiveMaximum','minLength','maxLength','pattern','minItems','maxItems','uniqueItems','minProperties','maxProperties','multipleOf','title','description','default','example','examples','deprecated','readOnly','writeOnly','xml','externalDocs','format',
  // JSON Schema 2020-12 annotations used by OpenAPI 3.1 documents.
  'const','$schema','$id','$comment','$anchor','contentMediaType','contentEncoding','$defs']);
const TYPES = ['object','array','string','integer','number','boolean'];
function typesOf(s:any, spec:any):string[]|undefined {
  if (s.type === undefined) return undefined;
  const list = Array.isArray(s.type) ? s.type : [s.type];
  return s.nullable === true ? [...list, 'null'] : list;
}
function schemaProblems(schema:any, spec?:any):string[] {
  const errors = Object.keys(schema).filter(k => !supported.has(k) && !k.startsWith('x-')).map(k => `Unsupported schema constraint: ${k}`);
  if (schema.required !== undefined && (!Array.isArray(schema.required) || schema.required.some((x:any)=>typeof x !== 'string'))) errors.push('Invalid required declaration.');
  if (schema.enum !== undefined && !Array.isArray(schema.enum)) errors.push('Invalid enum declaration.');
  if (schema.type !== undefined) {
    const list = Array.isArray(schema.type) && (spec === undefined || isOas31(spec)) ? schema.type : [schema.type];
    if (!list.length || list.some((t:any) => !TYPES.includes(t) && !(t === 'null' && Array.isArray(schema.type)))) errors.push('Unsupported schema type.');
  }
  if (schema.properties !== undefined && (!schema.properties || typeof schema.properties !== 'object' || Array.isArray(schema.properties))) errors.push('Invalid properties declaration.');
  for (const key of ['nullable','uniqueItems','readOnly','writeOnly']) if (schema[key] !== undefined && typeof schema[key] !== 'boolean') errors.push('Invalid '+key+' declaration.');
  for (const key of ['exclusiveMinimum','exclusiveMaximum']) if (schema[key] !== undefined && typeof schema[key] !== 'boolean' && (typeof schema[key] !== 'number' || !Number.isFinite(schema[key]))) errors.push('Invalid '+key+' declaration.');
  for (const key of ['minimum','maximum','multipleOf','minLength','maxLength','minItems','maxItems','minProperties','maxProperties']) if (schema[key] !== undefined && (typeof schema[key] !== 'number' || !Number.isFinite(schema[key]))) errors.push('Invalid '+key+' declaration.');
  return errors;
}
const INT_FORMATS: Record<string,[number,number]> = {int32:[-(2**31), 2**31-1], int64:[Number.MIN_SAFE_INTEGER, Number.MAX_SAFE_INTEGER]};
export function checkValue(value:any,raw:any,spec:any,label:string,serialized=false,depth=0):Check {
  const c=empty();
  if (depth>30) {c.unknown.push(`${label}: schema depth limit`);return c;}
  const resolved=deref(raw,spec);
  if (resolved.error) {c.unknown.push(`${label}: ${resolved.error}`);return c;}
  const s=resolved.value;
  c.unknown.push(...schemaProblems(s, spec).map(x=>`${label}: ${x}`));
  if (c.unknown.length) return c;
  const types = typesOf(s, spec);
  if (isAbstract(value)) {
    // A runtime value: the code makes no static claim about its content.
    const pyType = isTemplate(value) ? 'str' : value.type;
    const jsonTypes = pyType ? PY_TO_JSON[pyType] : undefined;
    if (!serialized && types && jsonTypes && !jsonTypes.some(t => types.includes(t))) c.bad.push(`${label}: a Python ${pyType} value is sent where the contract expects ${types.join('/')}.`);
    else note(c, `${label}: ${describe(value)} is not statically known; its value constraints are not checked`);
    return c;
  }
  if (value===null && types?.includes('null')) return c;
  let v=value;
  if (serialized && typeof v==='string' && types) {
    if ((types.includes('integer') || types.includes('number')) && !types.includes('string') && /^-?(?:0|[1-9]\d*)(?:\.\d+)?$/.test(v)) v=Number(v);
    if (types.includes('boolean') && !types.includes('string') && ['true','false'].includes(v)) v=v==='true';
  }
  if (!types) {c.unknown.push(`${label}: schema type is unspecified.`);return c;}
  const matchesType = (type:string) => type==='string' ? typeof v==='string' : type==='integer' ? Number.isInteger(v) : type==='number' ? typeof v==='number' && Number.isFinite(v)
    : type==='boolean' ? typeof v==='boolean' : type==='array' ? Array.isArray(v) : type==='object' ? v!==null && typeof v==='object' && !Array.isArray(v) : type==='null' ? v===null : false;
  if (!types.some(matchesType)) {c.bad.push(`${label}: expected ${types.join('/')}.`);return c;}
  if (s.const!==undefined && JSON.stringify(s.const)!==JSON.stringify(v)) c.bad.push(`${label}: value differs from const.`);
  if (Array.isArray(s.enum) && !s.enum.some((x:any)=>JSON.stringify(x)===JSON.stringify(v))) c.bad.push(`${label}: value is outside enum.`);
  if (typeof s.format==='string' && v!==null) {
    if (INT_FORMATS[s.format] && typeof v==='number') { const [lo,hi]=INT_FORMATS[s.format]; if (v<lo || v>hi) c.bad.push(`${label}: outside ${s.format} range.`); }
    else if (!['float','double','int32','int64'].includes(s.format) || typeof v!=='number') c.unknown.push(`${label}: format ${s.format} is not validated.`);
  }
  if (typeof v==='number') {
    const exMin = typeof s.exclusiveMinimum==='number' ? s.exclusiveMinimum : s.exclusiveMinimum===true ? s.minimum : undefined;
    const exMax = typeof s.exclusiveMaximum==='number' ? s.exclusiveMaximum : s.exclusiveMaximum===true ? s.maximum : undefined;
    if (exMin!==undefined && v<=exMin || s.minimum!==undefined && s.exclusiveMinimum!==true && v<s.minimum) c.bad.push(`${label}: below minimum.`);
    if (exMax!==undefined && v>=exMax || s.maximum!==undefined && s.exclusiveMaximum!==true && v>s.maximum) c.bad.push(`${label}: above maximum.`);
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
    if (s.uniqueItems && concrete(v) && new Set(v.map(x=>JSON.stringify(x))).size!==v.length) c.bad.push(`${label}: items are not unique.`);
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
      else note(c, `${label}: property ${key} is not declared; the schema allows additional properties`);
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
    if (l.row) return l.row;
    const m=l.match!, templated = typeof ep.endpoint !== 'string';
    return result('access_point','verified_correct',tier(spec),'OpenAPI servers + path + method',`${ep.http_method} ${m.display} matches the declared server and operation ${ep.http_method} ${m.pathKey}.` +
      (templated ? '\nNoncritical: runtime path values are assumed to stay within one path segment.' : ''));
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
type Sent = {values:Record<string,any>;complete:boolean};
function fields(ep:Claim,via:string):Sent {
  const container=ep.request?.[via];
  if (!container) return {values:{},complete:ep.request_complete===true};
  const shape=shapeOf(container,via);
  if (shape===null) return {values:{},complete:true};
  if (!shape || typeof shape!=='object' || Array.isArray(shape) || isAbstract(shape)) return {values:{},complete:false};
  const values:Record<string,any>=Object.create(null);
  for (const [k,v] of Object.entries(shape)) values[via==='headers'?k.toLowerCase():k]=v;
  return {values,complete:true};
}
function requestFields(ep:Claim,match:Operation) {
  const query=fields(ep,'params');
  for (const [key,value] of Object.entries(match.query.values)) {
    if (own(query.values,key)) query.complete=false; // duplicate serialization not guessed
    else query.values[key]=value;
  }
  if (!match.query.complete) query.complete=false;
  return {query,header:fields(ep,'headers'),cookie:fields(ep,'cookies'),path:{values:match.params,complete:true}};
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
const JSON_MEDIA = /^application\/(?:[\w.+-]+\+)?json\s*(?:;.*)?$/i;
function jsonSchemaOf(content:any):{schema?:any;found:boolean} {
  if (!content || typeof content!=='object') return {found:false};
  const key=Object.keys(content).find(k=>JSON_MEDIA.test(k));
  return key ? {schema:content[key]?.schema,found:true} : {found:false};
}
function basicAuthShape(shape:any):boolean {
  if (isOpaque(shape) && /HTTPBasicAuth$/.test(shape.type || '')) return true;
  return Array.isArray(shape) && shape.length===2 && shape.every((v:any)=>typeof v==='string' || isTemplate(v) || isOpaque(v) && (v.type==null || v.type==='str'));
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
      if (val===undefined || val===null) {
        if (p.required) (location.complete ? c.bad : c.unknown).push(`Missing required ${p.in} parameter ${p.name}.`);
      } else if (isAbstract(val)) {
        merge(c,checkValue(val,p.schema,spec,`${p.in}.${p.name}`,true));
      } else {
        const schema=deref(p.schema,spec).value, defaultStyle=['query','cookie'].includes(p.in)?'form':'simple';
        const style=p.style ?? defaultStyle, explode=p.explode ?? style==='form';
        if (p.content || style!==defaultStyle || schema?.type==='object') c.unknown.push(`Unsupported parameter serialization: ${p.name}`);
        else if (schema?.type==='array') {
          // form + explode:false is one comma-separated value; explode:true repeats the key per item.
          const items=typeof val==='string' ? (explode ? [val] : val.split(',')) : Array.isArray(val) && explode ? val : null;
          if (!items) c.unknown.push(`Parameter ${p.name}: the value's form does not match the declared array serialization (explode=${explode}).`);
          else {
            if (schema.minItems!==undefined && items.length<schema.minItems || schema.maxItems!==undefined && items.length>schema.maxItems) c.bad.push(`${p.in}.${p.name}: invalid array length.`);
            items.forEach((x:any,i:number)=>merge(c,checkValue(x,schema.items,spec,`${p.in}.${p.name}[${i}]`,true)));
          }
        } else merge(c,checkValue(val,p.schema,spec,`${p.in}.${p.name}`,true));
      }
    }
    const authNames=securityNames(spec,m.operation);
    for (const loc of ['query','header','cookie'] as const) {
      if (!sent[loc].complete) c.unknown.push(`${loc} dictionary has unresolved keys.`);
      const declared=new Set(pars.values.filter(p=>p.in===loc).map(p=>loc==='header'?p.name.toLowerCase():p.name));
      for (const key of Object.keys(sent[loc].values)) if (!declared.has(key) && !authNames[loc].has(key)) {
        // OpenAPI does not forbid extra inputs. An undeclared query parameter may be a
        // hallucinated filter, so it stays unresolved; extra headers are ordinarily ignored.
        if (loc==='header') note(c,`Undeclared header ${key}; acceptance is undocumented`);
        else c.unknown.push(`Undeclared ${loc} parameter ${key}; acceptance is undocumented.`);
      }
    }
    const auth=ep.request?.auth, authShape=auth?.provided ? shapeOf(auth,'auth') : undefined;
    if (auth?.provided && authShape!==null && !basicAuthShape(authShape)) c.unknown.push('Custom/dynamic request authentication is outside the supported subset.');
    const rb=deref(m.operation.requestBody,spec);
    const body=ep.request?.json, form=ep.request?.data;
    const bodyShape=body?.provided ? shapeOf(body,'json') : undefined, formShape=form?.provided ? shapeOf(form,'data') : undefined;
    if (body?.provided && bodyShape!==null) {
      const contentType=sent.header.values['content-type'];
      if (contentType!==undefined && typeof contentType!=='string') c.unknown.push('Request Content-Type is unresolved.');
      else if (typeof contentType==='string' && contentType.split(';')[0].trim().toLowerCase()!=='application/json') c.bad.push('JSON body sent with a non-JSON Content-Type.');
    }
    if (form?.provided && formShape!==null) c.unknown.push('Form/raw body encoding is unsupported.');
    if (m.operation.requestBody) {
      if (rb.error) c.unknown.push(rb.error);
      else {
        if (rb.value.required && (!body?.provided || bodyShape===null) && !(form?.provided && formShape!==null)) c.bad.push('Required request body is missing.');
        if (body?.provided && bodyShape!==null) {
          const {schema}=jsonSchemaOf(rb.value.content);
          if (!schema) c.unknown.push('No JSON request schema available.');
          else if (isAbstract(bodyShape) || bodyShape===undefined) c.unknown.push('Request body is unresolved.');
          else merge(c,checkValue(bodyShape,schema,spec,'body'));
        }
      }
    } else if (body?.provided && bodyShape!==null) c.unknown.push('Code sends a JSON body with no declared request-body contract.');
    return finish('input_contract',c,spec,`Required inputs, locations and supported value constraints checked for ${ep.call_id} (${m.pathKey}).`);
  });
  return aggregateExtracted('input_contract',claims,rows,'No HTTP calls; no input contract to check.');
}

// ---------------------------------------------------------------- response schemas
interface View {types?:string[]; properties:Record<string,any>; required:Set<string>; additional:any; items?:any; nullable:boolean; writeOnly:boolean; alternatives?:any[]; problems:string[]}
/** A normalised view of a response schema: $ref resolved, allOf merged, pure unions expanded. */
function schemaView(raw:any,spec:any,depth=0):View {
  const v:View={properties:{},required:new Set(),additional:undefined,nullable:false,writeOnly:false,problems:[]};
  if (depth>20) {v.problems.push('Schema composition depth limit.');return v;}
  let s=raw;
  if (isOas31(spec) && s && typeof s==='object' && own(s,'$ref') && Object.keys(s).some(k=>!['$ref','description','summary'].includes(k))) {
    const {$ref,...siblings}=s; s={allOf:[{$ref},siblings]};
  }
  const r=deref(s,spec);
  if (r.error) {v.problems.push(r.error);return v;}
  s=r.value;
  const {allOf,oneOf,anyOf,discriminator,...rest}=s;
  const union=oneOf ?? anyOf;
  const structural=Object.keys(rest).filter(k=>['properties','items','additionalProperties','required'].includes(k));
  if (union!==undefined && (structural.length || allOf!==undefined || !Array.isArray(union))) {
    v.problems.push('Unsupported schema constraint: '+(oneOf!==undefined?'oneOf':'anyOf')+' combined with other structure.');
    return v;
  }
  if (union!==undefined) {
    v.alternatives=union;
    v.nullable=rest.nullable===true || (Array.isArray(rest.type) && rest.type.includes('null'));
    return v;
  }
  v.problems.push(...schemaProblems(rest,spec));
  v.types=typesOf(rest,spec);
  v.nullable=v.types?.includes('null') ?? false;
  v.writeOnly=rest.writeOnly===true;
  Object.assign(v.properties,rest.properties || {});
  for (const k of rest.required || []) v.required.add(k);
  v.additional=rest.additionalProperties;
  v.items=rest.items;
  if (allOf!==undefined) {
    if (!Array.isArray(allOf)) {v.problems.push('Invalid allOf declaration.');return v;}
    for (const member of allOf) {
      const m=schemaView(member,spec,depth+1);
      v.problems.push(...m.problems);
      if (m.alternatives) {v.problems.push('Unsupported schema constraint: union inside allOf.');continue;}
      if (m.types) v.types=v.types ? v.types.filter(t=>m.types!.includes(t) || t==='number' && m.types!.includes('integer')) : m.types;
      Object.assign(v.properties,m.properties);
      m.required.forEach(k=>v.required.add(k));
      v.items ??= m.items;
      if (m.nullable && (!v.types || v.types.includes('null'))) v.nullable=true;
    }
    // additionalProperties inside allOf members only sees that member's properties; treat the merge as open.
    if (v.additional===false) v.additional=undefined;
  }
  if (!v.types && Object.keys(v.properties).length) v.types=['object'];
  return v;
}
type Step = {c:Check; next:any[]};
function stepInto(view:View,key:any,spec:any,optional:boolean):Step {
  const c=empty();
  if (view.problems.length) {c.unknown.push(...view.problems);return {c,next:[]};}
  if (view.alternatives) {
    const results=view.alternatives.map(a=>stepInto(schemaView(a,spec),key,spec,optional));
    const ok=results.filter(r=>!r.c.bad.length && !r.c.unknown.length);
    if (ok.length===results.length) { results.forEach(r=>merge(c,{bad:[],unknown:[],notes:r.c.notes})); return {c,next:results.flatMap(r=>r.next)}; }
    if (results.every(r=>r.c.bad.length)) {c.bad.push(...new Set(results.flatMap(r=>r.c.bad)));return {c,next:[]};}
    c.unknown.push(`Response field ${JSON.stringify(key)} is documented in only some schema alternatives.`);
    return {c,next:[]};
  }
  if (!view.types) {c.unknown.push('Response schema type is unspecified.');return {c,next:[]};}
  if (view.nullable) note(c,'a response container on this path can be null');
  if (typeof key==='number' || key==='*' && view.types.includes('array') && !view.types.includes('object')) {
    if (!view.types.includes('array')) {c.bad.push('Array indexing used on a non-array response.');return {c,next:[]};}
    if (typeof key==='number' && !Number.isInteger(key)) {c.unknown.push('Non-integer response index.');return {c,next:[]};}
    // Existence of a particular array element is not established by its item schema.
    if (view.items===undefined) {c.unknown.push('Array item schema is unspecified.');return {c,next:[]};}
    return {c,next:[view.items]};
  }
  if (key==='*') {c.unknown.push('Dynamic response field is unresolved.');return {c,next:[]};}
  if (!view.types.includes('object')) {
    c.bad.push(view.types.includes('array') ? `String field ${key} read directly from an array.` : `Field ${key} read from a scalar response.`);
    return {c,next:[]};
  }
  if (!own(view.properties,key)) {
    if (view.additional===false) c.bad.push(`Response field ${key} is forbidden by the closed schema.`);
    else c.unknown.push(`Response field ${key} is not documented; schema allows unspecified properties.`);
    return {c,next:[]};
  }
  // The field is documented. Presence is a robustness question, not an API-claim contradiction.
  if (!optional && !view.required.has(key)) note(c,`response field ${key} is optional in the contract; presence is not guaranteed`);
  const child=schemaView(view.properties[key],spec);
  if (child.writeOnly) c.unknown.push(`Response field ${key} is writeOnly.`);
  return {c,next:[view.properties[key]]};
}
function checkOutputPath(path:any[],raw:any,spec:any,optional=false):Check {
  const c=empty(); let schemas=[raw];
  for (const [i,key] of path.entries()) {
    const steps=schemas.map(s=>stepInto(schemaView(s,spec),key,spec,optional && i===path.length-1));
    steps.forEach(s=>merge(c,s.c));
    if (c.bad.length || c.unknown.length) return c;
    schemas=steps.flatMap(s=>s.next);
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
      if (r.error) return {bad:[],unknown:[r.error]} as Check;
      const {schema}=jsonSchemaOf(r.value.content);
      if (!schema) return {bad:[],unknown:[`No JSON schema for success status ${status}.`]} as Check;
      return checkOutputPath(Array.isArray(f.path)?f.path:[f.field],schema,spec,f.optional_access===true);
    });
    const combined=empty();
    if (checks.every(c=>c.bad.length)) combined.bad.push(...checks.flatMap(c=>c.bad));
    else {
      combined.unknown.push(...checks.flatMap(c=>c.unknown));
      if (checks.some(c=>c.bad.length)) combined.unknown.push('Field validity depends on an unresolved success status.');
    }
    checks.forEach(c=>{ if (c.notes?.length) (combined.notes ||= []).push(...c.notes); });
    rows.push(finish('output_contract',combined,spec,`Response path ${JSON.stringify(f.path || [f.field])} is documented for ${f.call_id} (${l.match!.pathKey}).`));
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

// ---------------------------------------------------------------- authentication
const SCHEME_PREFIX:Record<string,RegExp>={bearer:/^Bearer\s+\S/i, basic:/^Basic\s+[A-Za-z0-9+/]+=*$/i};
function authCheck(name:string,scopes:any,ep:Claim,match:Operation,spec:any):Check {
  const c=empty(), resolved=deref(spec.components?.securitySchemes?.[name],spec);
  if (resolved.error) {c.unknown.push(`Security scheme ${name}: ${resolved.error}`);return c;}
  const s=resolved.value, sent=requestFields(ep,match);
  let val:any, complete=false;
  // Scopes are granted to the token, not expressed by the code: report them, do not gate on them
  // (decision 6 in SCORING_FIXES.md), just as credential validity is not tested.
  if (Array.isArray(scopes) && scopes.length) note(c,`required scopes (${scopes.join(', ')}) belong to the ${name} token and cannot be checked statically; the credential is assumed to carry them`);
  if (s.type==='apiKey' && ['header','query','cookie'].includes(s.in)) {
    const loc=sent[s.in as 'header'|'query'|'cookie'];
    val=loc.values[s.in==='header'?String(s.name).toLowerCase():s.name]; complete=loc.complete;
    if (isAbstract(val)) note(c,`credential ${name} is placed as documented; its runtime value is not tested`);
  } else if (s.type==='http' && ['bearer','basic'].includes(s.scheme?.toLowerCase()) || s.type==='oauth2' || s.type==='openIdConnect') {
    // OAuth2 and OpenID Connect access tokens are sent as Bearer tokens (RFC 6750).
    const scheme=s.type==='http' ? s.scheme.toLowerCase() : 'bearer', label=s.type==='http' ? s.scheme : `${s.type} Bearer token`;
    val=sent.header.values.authorization;complete=sent.header.complete;
    if (val===undefined && ep.request?.auth?.provided) {
      if (scheme==='basic' && basicAuthShape(shapeOf(ep.request.auth,'auth'))) return note(c,`basic credentials are supplied through requests auth; their validity is not tested`);
      c.unknown.push('Authentication adapter/value could not be established.');return c;
    }
    if (typeof val==='string') {
      if (!SCHEME_PREFIX[scheme].test(val.trim() ? val : '')) c.bad.push(`Authorization header does not match ${label}.`);
    } else if (isTemplate(val)) {
      // The literal prefix of a template such as "Bearer {token}" establishes the scheme.
      const first=val.parts[0];
      if (typeof first!=='string') c.unknown.push(`The Authorization scheme is a runtime value; ${label} placement cannot be established.`);
      else if (scheme==='bearer' ? !/^Bearer\s+$/i.test(first) && !/^Bearer\s+\S/i.test(first) : !/^Basic\s+/i.test(first)) c.bad.push(`Authorization header does not match ${label}.`);
      else note(c,`the ${label} credential is a runtime value; its validity is not tested`);
      return c;
    } else if (isOpaque(val)) {
      c.unknown.push(`Credential ${name} has an unresolved runtime value; the ${label} scheme cannot be established.`);return c;
    }
  } else {c.unknown.push(`Unsupported authentication scheme/scopes: ${name} (${s.type}).`);return c;}
  if (val===undefined || val===null) (complete?c.bad:c.unknown).push(`Required credential ${name} is absent from the request.`);
  else if (typeof val==='string' && !val.trim()) c.bad.push(`Credential ${name} is empty or invalid.`);
  else if (!isAbstract(val) && typeof val!=='string') c.bad.push(`Credential ${name} is empty or invalid.`);
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
    const satisfied=alternatives.find(c=>!c.bad.length && !c.unknown.length);
    if (satisfied) return finish('contextual',{bad:[],unknown:[],notes:satisfied.notes},spec,'Required authentication placement and static shape match one security alternative. Credential validity is not tested.');
    if (alternatives.every(c=>c.bad.length)) return finish('contextual',{bad:alternatives.flatMap(c=>c.bad),unknown:[]},spec,'');
    return unknown('contextual',alternatives.flatMap(c=>[...c.bad,...c.unknown]).join('\n'));
  });
  return aggregateExtracted('contextual',claims,rows,'No HTTP calls requiring contextual checks.');
}
