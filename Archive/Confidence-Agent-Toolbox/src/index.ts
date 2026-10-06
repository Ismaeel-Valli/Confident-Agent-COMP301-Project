import { type PluginContext, type ToolsProvider, type Tool } from '@lmstudio/sdk';
import { mkdir, readFile, writeFile, stat } from 'fs/promises';
import { join, resolve } from 'path';
import { homedir } from 'os';
import { createHash } from 'crypto';
import { z } from 'zod';
import { pluginConfigSchematics } from './config';
import { catalog } from './catalog';
import { makeTool, type Context } from './runtime';
import { createFilesystemTools } from './filesystem/tools';
import { createWebTools } from './web/tools';
import { createDocumentationTool } from './web/documentation';
import { createExecutionTools } from './execution';
import { createMemoryTools } from './memory';
import { createConfidenceAgentTools } from './confidence/confidenceAgentTools';
import { createPyrightRunner } from './confidence/pyrightRunner';
export function createToolbox(ctx:Context):Tool[]{
 const tool=makeTool(ctx),web=createWebTools(ctx);
 const runPyright=createPyrightRunner(ctx.pythonExecutable);
 const all=[...createFilesystemTools(ctx),...web,createDocumentationTool(ctx,web),...createExecutionTools(ctx),...createMemoryTools(ctx),
  ...createConfidenceAgentTools({isEnabled:true,allowPyright:ctx.enabled('run_pyright'),context:ctx,getWorkingDirectory:()=>ctx.cwd,
    runPyright:async p=>{if(!ctx.enabled('run_pyright'))throw new Error('run_pyright is disabled.');return runPyright(p);}}),
  tool({name:'change_directory',description:catalog.change_directory.description,parameters:{directory:z.string()},implementation:async({directory})=>{
   const previous_directory=ctx.cwd,newPath=resolve(ctx.cwd,directory);
   if(!(await stat(newPath)).isDirectory())throw new Error('Not a directory: '+newPath);
   await ctx.setDirectory(newPath);return {previous_directory,current_directory:ctx.cwd};
  }})];
 return all.filter(t=>ctx.enabled(t.name));
}
export const toolsProvider:ToolsProvider=async ctl=>{
 const config=ctl.getPluginConfig(pluginConfigSchematics);
 const configured=config.get('workspacePath').trim().replace(/%([^%]+)%/g,(_,key)=>process.env[key]||`%${key}%`);
 const workspace=resolve(configured||join(homedir(),'confidence-agent-workspace'));
 await mkdir(workspace,{recursive:true});
 const stateDirectory=join(homedir(),'.confidence-agent-toolbox',createHash('sha256').update(workspace).digest('hex').slice(0,16));
 const statePath=join(stateDirectory,'state.json');
 let cwd=workspace;
 try {const saved=JSON.parse(await readFile(statePath,'utf8'));if(typeof saved.cwd==='string'&&(await stat(saved.cwd)).isDirectory())cwd=saved.cwd;}catch{}
 const ctx:Context={cwd,workspace,stateDirectory,pythonExecutable:config.get('pythonExecutable').trim()||'python',embeddingModel:config.get('embeddingModel'),client:(ctl as any).client,
  enabled:name=>name in catalog&&(config.get as any)(`enable_${name}`)===true,
  setDirectory:async directory=>{await mkdir(stateDirectory,{recursive:true});await writeFile(statePath,JSON.stringify({cwd:directory}),'utf8');ctx.cwd=directory;}};
 return createToolbox(ctx);
};
export async function main(context:PluginContext){context.withConfigSchematics(pluginConfigSchematics).withToolsProvider(toolsProvider);}
