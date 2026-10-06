import { createConfigSchematics } from '@lmstudio/sdk';

/** Plugin settings shown in LM Studio. Keys match the previous toolbox where the setting still exists. */
export const pluginConfigSchematics = createConfigSchematics()
  .field('enableConfidenceAgentTools', 'boolean', {
    displayName: 'Confident Agent tools',
    subtitle: 'Expose verify_candidate and the inspection tools (claim extraction, six layer checks, scoring and report).',
  }, true)
  .field('allowPyrightExecution', 'boolean', {
    displayName: 'Allow Pyright',
    subtitle: 'Run the pinned Pyright checker on candidate code. Static analysis only: candidate code is never executed. Required for the identifier layer.',
  }, true)
  .field('pythonExecutable', 'string', {
    displayName: 'Verification Python',
    subtitle: 'Interpreter for claim extraction and Pyright import resolution, e.g. C:\\...\\confident-agent-toolbox\\.venv\\Scripts\\python.exe. Empty uses the CONFIDENCE_PYTHON environment variable, then python.',
  }, '')
  .field('workspacePath', 'string', {
    displayName: 'save_code folder',
    subtitle: 'Folder where save_code writes files. Empty uses %USERPROFILE%\\confident-agent-workspace.',
  }, '')
  .build();
