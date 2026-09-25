import { type Tool } from '@lmstudio/sdk';
import { z } from 'zod';
import { createHash } from 'crypto';
import { makeTool, type Context } from '../runtime';
import { catalog } from '../catalog';
const domains={jsonplaceholder:'jsonplaceholder.typicode.com',github:'docs.github.com',openmeteo:'open-meteo.com',dummyjson:'dummyjson.com',restcountries:'restcountries.com',petstore:'petstore3.swagger.io'};
export function createDocumentationTool(ctx:Context,web:Tool[]):Tool {
 return makeTool(ctx)({name:'lookup_documentation',description:catalog.lookup_documentation.description,
 parameters:{api:z.enum(['jsonplaceholder','github','openmeteo','dummyjson','restcountries','petstore']),api_version:z.string().optional(),query:z.string().optional()},
 implementation:async({api,api_version,query},callContext)=>{
  for(const name of ['web_search','fetch_web_content'])if(!ctx.enabled(name))throw new Error(`Required tool '${name}' is disabled.`);
  const invoke=async(name:string,args:any)=>{const selected=web.find(t=>t.name===name);if(!selected||!('implementation' in selected))throw new Error('Unavailable tool: '+name);return selected.implementation(args,callContext);};
  const domain=domains[api],searchQuery=`site:${domain} ${api} ${api_version||''} ${query||'API documentation'}`;
  const search=await invoke('web_search',{query:searchQuery});
  const found=(search.results||[]).map((r:any)=>r.link||r.url).filter((url:any)=>{try {const h=new URL(url).hostname;return h===domain||h.endsWith('.'+domain);}catch{return false;}});
  const urls=[...new Set<string>(found)].slice(0,3);if(!urls.length)urls.push(`https://${domain}/`);
  const pages=[];
  for(const url of urls){const page=await invoke('fetch_web_content',{url});pages.push({...page,retrieved_at:new Date().toISOString(),sha256:typeof page.content==='string'?createHash('sha256').update(page.content).digest('hex'):null,review_required:true});}
  return {api,requested_api_version:api_version||null,query:searchQuery,search,pages,notes:['Retrieved text and search results are unreviewed evidence. They do not establish an API version or change layer verdicts, tiers or EWCS. Supply a reviewed OpenAPI contract explicitly to verification.']};
 }});
}
