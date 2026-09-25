import { existsSync, readFileSync } from 'fs';
import { join, resolve } from 'path';
import { type Claim, ofType } from './verificationTypes';
/**
 * Frozen public evidence selected from evidence/registry.json by the host the
 * candidate calls. The model never supplies or copies specifications: evidence
 * routed through the model cannot be trusted (it can be truncated, confused
 * with other tool results or invented).
 */
export interface EvidenceSelection {provider:string|null; spec:any|null; hosts:string[]; snapshot?:string; note:string}
const cache = new Map<string,any>();
function registryRoot():string|null {
  const candidates = [process.env.CONFIDENCE_EVIDENCE_ROOT, resolve(__dirname,'..'), process.cwd()].filter(Boolean) as string[];
  return candidates.find(root => existsSync(join(root,'evidence','registry.json'))) ?? null;
}
function templateHead(t:any):string { return Array.isArray(t?.parts) && typeof t.parts[0] === 'string' ? t.parts[0] : ''; }
function hostOf(url:string):string|null { return /^https?:\/\/([^/?#:]+)/i.exec(url)?.[1]?.toLowerCase() ?? null; }
/** Hosts named by extracted endpoint claims (literal URLs or template origins). */
export function hostsFromClaims(claims:Claim[]):string[] {
  const hosts = ofType(claims,'endpoint').map(ep => hostOf(typeof ep.endpoint === 'string' ? ep.endpoint : templateHead(ep.endpoint_template)));
  return [...new Set(hosts.filter((h):h is string => !!h))];
}
/** Hosts named in source text; used before extraction has run. */
export function hostsFromCode(code:string):string[] {
  return [...new Set([...code.matchAll(/https?:\/\/([^/'"\s?#:{}]+)/gi)].map(m => m[1].toLowerCase()))];
}
export function selectEvidence(hosts:string[]):EvidenceSelection {
  const root = registryRoot();
  if (!root) return {provider:null,spec:null,hosts,note:'Evidence registry (evidence/registry.json) not found; set CONFIDENCE_EVIDENCE_ROOT to the Toolbox folder.'};
  const registry = JSON.parse(readFileSync(join(root,'evidence','registry.json'),'utf8'));
  const matches = Object.entries<any>(registry.providers).filter(([,p]) => hosts.some(h => p.hosts.includes(h)));
  if (!matches.length) return {provider:null,spec:null,hosts,note:`No frozen evidence for host(s): ${hosts.join(', ') || '(none found)'}.`};
  if (matches.length > 1) return {provider:null,spec:null,hosts,note:`Candidate calls several providers (${matches.map(([n])=>n).join(', ')}); single-provider verification only.`};
  const [provider, entry] = matches[0];
  const path = resolve(root,'evidence',registry.sources_dir,entry.spec);
  if (!existsSync(path)) return {provider,spec:null,hosts,note:`Frozen snapshot ${entry.spec} is missing at ${path}.`};
  if (!cache.has(path)) cache.set(path, JSON.parse(readFileSync(path,'utf8')));
  const spec = structuredClone(cache.get(path));
  spec['x-confidence-evidence'] = {...(spec['x-confidence-evidence'] || {}), ...entry.overlay, snapshot:entry.spec};
  return {provider,spec,hosts,snapshot:entry.spec,note:`Frozen evidence ${entry.spec} selected for ${provider}.`};
}
/**
 * Use frozen evidence for known hosts. A model-supplied spec is only accepted when
 * no frozen evidence exists for the host, and is then reported as unreviewed.
 */
export function evidenceFor(hosts:string[], supplied:any):{spec:any; source:string} {
  const selected = selectEvidence(hosts);
  if (selected.spec) return {spec:selected.spec, source:selected.note + (supplied != null ? ' A model-supplied specification was ignored.' : '')};
  const usable = supplied != null && typeof supplied === 'object' && !(Object.hasOwn(supplied,'spec') && !Object.hasOwn(supplied,'openapi'));
  return {spec:usable ? supplied : null, source:usable ? 'Model-supplied specification (unreviewed; not frozen evidence).' : selected.note};
}
