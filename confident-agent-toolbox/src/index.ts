import { type PluginContext } from '@lmstudio/sdk';
import { pluginConfigSchematics } from './config';
import { toolsProvider } from './toolsProvider';

/** LM Studio plugin entry: settings and the verification tools only. No prompt preprocessing. */
export async function main(context: PluginContext) {
  context.withConfigSchematics(pluginConfigSchematics);
  context.withToolsProvider(toolsProvider);
}
