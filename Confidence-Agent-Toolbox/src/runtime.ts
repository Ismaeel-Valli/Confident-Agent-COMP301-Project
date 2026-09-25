import { tool as sdkTool, type LMStudioClient } from '@lmstudio/sdk';
import { resolve, relative, isAbsolute, dirname } from 'path';
import { existsSync, realpathSync } from 'fs';
import { catalog } from './catalog';
export interface Context {
  cwd: string;
  workspace: string;
  stateDirectory: string;
  pythonExecutable: string;
  embeddingModel: string;
  client: LMStudioClient;
  enabled: (name:string)=>boolean;
  setDirectory: (directory:string)=>Promise<void>;
}
export function validatePath(base:string,requested:string):string {
  const target=resolve(base,requested);
  const inside=(parent:string,child:string)=>{const rel=relative(parent,child);return rel!== '..'&&!rel.startsWith('..'+require('path').sep)&&!isAbsolute(rel);};
  if(!inside(resolve(base),target))throw new Error('Path is outside the working directory.');
  // Check existing ancestors too, so symlinked directories cannot bypass the boundary.
  let ancestor=target;
  while(!existsSync(ancestor)&&dirname(ancestor)!==ancestor)ancestor=dirname(ancestor);
  if(!inside(realpathSync(base),realpathSync(ancestor)))throw new Error('Path resolves outside the working directory through a symbolic link.');
  return target;
}
export function makeTool(ctx:Context):typeof sdkTool {
  return ((definition:any)=>sdkTool({...definition,description:(catalog as any)[definition.name]?.description||definition.description,
    implementation:async (...args:any[])=>{
      if(!ctx.enabled(definition.name))throw new Error(`Tool '${definition.name}' is disabled in plugin settings.`);
      return definition.implementation(...args);
    }})) as typeof sdkTool;
}
export const safeImplementation=<P,R>(fn:(params:P)=>Promise<R>,enabled:boolean,name:string)=>async(params:P):Promise<R>=>{
  if(!enabled)throw new Error(`Tool '${name}' is disabled.`);
  return fn(params);
};
