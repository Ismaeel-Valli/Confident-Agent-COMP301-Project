import { type Tool } from '@lmstudio/sdk';
import { z } from 'zod';
import { readFile, writeFile, mkdir, rename } from 'fs/promises';
import { join } from 'path';
import { randomUUID } from 'crypto';
import { makeTool, type Context } from './runtime';
import { catalog } from './catalog';
type Entry={id:string;created_at:string;fact:string};
const queues=new Map<string,Promise<unknown>>();
export function createMemoryTools(ctx:Context):Tool[]{
 const tool=makeTool(ctx),file=join(ctx.stateDirectory,'memory.json');
 const read=async():Promise<Entry[]>=>{try{return JSON.parse(await readFile(file,'utf8'));}catch(e:any){if(e.code==='ENOENT')return [];throw e;}};
 const mutate=(fn:(entries:Entry[])=>any)=>{
  const next=(queues.get(file)||Promise.resolve()).catch(()=>{}).then(async()=>{
   const entries=await read(),result=fn(entries);await mkdir(ctx.stateDirectory,{recursive:true});
   const temp=file+'.'+randomUUID()+'.tmp';await writeFile(temp,JSON.stringify(entries,null,2),'utf8');await rename(temp,file);return result;
  });queues.set(file,next);return next;
 };
 return [tool({name:'save_memory',description:catalog.save_memory.description,parameters:{fact:z.string().min(1).max(10000)},implementation:async({fact})=>mutate(entries=>{const entry={id:randomUUID(),created_at:new Date().toISOString(),fact};entries.push(entry);return entry;})}),
 tool({name:'read_memory',description:catalog.read_memory.description,parameters:{},implementation:async()=>({entries:await read()})}),
 tool({name:'search_memory',description:catalog.search_memory.description,parameters:{query:z.string()},implementation:async({query})=>({entries:(await read()).filter(e=>e.fact.toLowerCase().includes(query.toLowerCase()))})}),
 tool({name:'delete_memory',description:catalog.delete_memory.description,parameters:{id:z.string()},implementation:async({id})=>mutate(entries=>{const index=entries.findIndex(e=>e.id===id);if(index<0)return {deleted:false};entries.splice(index,1);return {deleted:true};})})];
}
