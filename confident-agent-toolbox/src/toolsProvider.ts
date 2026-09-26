import { text, tool, type Tool, type ToolsProvider } from '@lmstudio/sdk';
import { mkdir } from 'fs/promises';
import { homedir } from 'os';
import { isAbsolute, join, resolve } from 'path';
import { z } from 'zod';
import { pluginConfigSchematics } from './config';
import { createConfidenceAgentTools } from './confidenceAgentTools';
import { createPyrightRunner, type RunPyright } from './pyrightRunner';

export const DEFAULT_WORKSPACE = join(homedir(), 'confident-agent-workspace');

/** Expands %VAR% (Windows style) and resolves relative paths against the default workspace. */
export function resolveWorkspace(configured: string): string {
  const raw = configured.trim().replace(/%([^%]+)%/g, (match, name: string) => process.env[name] ?? match);
  if (!raw) return DEFAULT_WORKSPACE;
  return isAbsolute(raw) ? raw : resolve(DEFAULT_WORKSPACE, raw);
}

export function createPyrightTool(runPyright: RunPyright, allowPyright: boolean): Tool {
  return tool({
    name: 'run_pyright',
    description: text`
      Type-check a Python snippet with the pinned Pyright checker. Static analysis only: the code is
      NOT executed. Returns Pyright's structured JSON diagnostics, the exit code (0 no errors,
      1 type errors, higher values for checker or configuration failures), the checker version and
      the candidate hash. verify_candidate already runs Pyright; use this only for inspection.
    `,
    parameters: { python: z.string(), timeout_seconds: z.number().min(0.1).max(60).optional() },
    implementation: async params => {
      if (!allowPyright) throw new Error("Tool 'run_pyright' is disabled in the plugin settings (Allow Pyright).");
      return runPyright(params);
    },
  });
}

export const toolsProvider: ToolsProvider = async ctl => {
  const config = ctl.getPluginConfig(pluginConfigSchematics);
  // The claim extractor and the Pyright runner read CONFIDENCE_PYTHON; the plugin setting takes precedence.
  const python = config.get('pythonExecutable').trim();
  if (python) process.env.CONFIDENCE_PYTHON = python;
  const workspace = resolveWorkspace(config.get('workspacePath'));
  await mkdir(workspace, { recursive: true });
  const allowPyright = config.get('allowPyrightExecution');
  const runPyright = createPyrightRunner();
  const tools: Tool[] = [createPyrightTool(runPyright, allowPyright)];
  if (config.get('enableConfidenceAgentTools')) {
    tools.push(...createConfidenceAgentTools({ isEnabled: true, allowPyright, getWorkingDirectory: () => workspace, runPyright }));
  }
  return tools;
};
