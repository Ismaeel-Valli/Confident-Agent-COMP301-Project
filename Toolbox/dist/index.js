"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.main = main;
const toolsProvider_1 = require("./toolsProvider");
const promptPreprocessor_1 = require("./promptPreprocessor");
const config_1 = require("./config");
async function main(context) {
    // Register the configuration schematics.
    context.withConfigSchematics(config_1.pluginConfigSchematics);
    // Register the tools provider.
    context.withToolsProvider(toolsProvider_1.toolsProvider);
    // Register the prompt preprocessor to inject documentation on startup.
    context.withPromptPreprocessor(promptPreprocessor_1.promptPreprocessor);
}
//# sourceMappingURL=index.js.map