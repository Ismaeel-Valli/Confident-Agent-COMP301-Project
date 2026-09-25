import { hashCode } from './verificationTypes';
export async function resolveApiSpec({base_url}:{base_url:string}) {
  let base:URL;
  try {base=new URL(base_url);} catch {return {spec:null,source_url:null,note:'Invalid absolute URL.'};}
  if (!['https:','http:'].includes(base.protocol)) return {spec:null,source_url:null,note:'Only HTTP(S) discovery is supported.'};
  const direct=/\.json(?:$|\?)/i.test(base_url) || /openapi|swagger|api-docs/i.test(base.pathname);
  const candidates=direct?[base_url]:['/openapi.json','/swagger.json','/v3/api-docs'].map(p=>base_url.replace(/\/$/,'')+p);
  for(const url of candidates) {
    try {
      const r=await fetch(url,{signal:AbortSignal.timeout(5000)});
      if(!r.ok)continue;
      const raw=await r.text(), spec=JSON.parse(raw);
      if(!/^3\.0\./.test(spec.openapi || '') || !spec.paths)continue;
      // Discovery metadata is retained; the experiment should use a reviewed local snapshot.
      return {spec,source_url:r.url || url,retrieved_at:new Date().toISOString(),content_hash:hashCode(raw),review_required:true};
    } catch { /* Retain uncertainty, never invent a contract. */ }
  }
  return {spec:null,source_url:null,note:'No supported JSON OpenAPI 3.0 contract resolved. Supply a reviewed snapshot; YAML/Swagger 2/OpenAPI 3.1 are not silently interpreted as 3.0.'};
}
