import { type Tool } from '@lmstudio/sdk';
import { z } from 'zod';
import { spawn } from 'child_process';
import { mkdtemp, writeFile, rm } from 'fs/promises';
import { join } from 'path';
import * as os from 'os';
import { makeTool, type Context } from './runtime';
import { catalog } from './catalog';
import { createPyrightRunner } from './confidence/pyrightRunner';
export function createExecutionTools(ctx:Context):Tool[]{
 const tool=makeTool(ctx);
 return [tool({name:'run_python',description:catalog.run_python.description,
  parameters:{python:z.string(),timeout_seconds:z.number().min(0.1).max(120).optional()},
  implementation:async({python,timeout_seconds=15})=>{
   const dir=await mkdtemp(join(ctx.cwd,'.python-'));
   try {
    const file=join(dir,'candidate.py');await writeFile(file,python,'utf8');
    return await new Promise(resolve=>{
     const child=spawn(ctx.pythonExecutable,[file],{cwd:ctx.cwd,stdio:'pipe',timeout:timeout_seconds*1000});
     let stdout='',stderr='',truncated=false;
     const capture=(old:string,chunk:Buffer)=>{const next=old+chunk.toString();if(next.length>1000000)truncated=true;return next.slice(0,1000000);};
     child.stdout.on('data',d=>stdout=capture(stdout,d));child.stderr.on('data',d=>stderr=capture(stderr,d));
     child.on('error',e=>resolve({stdout,stderr,error:e.message,exit_code:null}));
     child.on('close',(exit_code,signal)=>resolve({stdout,stderr,exit_code,signal,timed_out:signal==='SIGTERM',truncated}));
     child.stdin.end();
    });
   } finally {await rm(dir,{recursive:true,force:true});}
  }}),
  tool({name:'run_pyright',description:catalog.run_pyright.description,
   parameters:{python:z.string(),timeout_seconds:z.number().min(0.1).max(60).optional()},implementation:createPyrightRunner(ctx.pythonExecutable)}),
  tool({name:'get_system_info',description:catalog.get_system_info.description,parameters:{},implementation:async()=>({platform:os.platform(),architecture:os.arch(),release:os.release(),cpu:os.cpus()[0]?.model,memory_total:os.totalmem(),memory_free:os.freemem(),node:process.version,working_directory:ctx.cwd,python:ctx.pythonExecutable})})];
}
