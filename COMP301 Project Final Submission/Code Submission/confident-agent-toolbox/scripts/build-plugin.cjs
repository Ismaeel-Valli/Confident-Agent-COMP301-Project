const { build } = require('esbuild');
const path = require('node:path');
const root = path.join(__dirname,'..');
build({entryPoints:[path.join(root,'.lmstudio/entry.ts')],outfile:path.join(root,'.lmstudio/dev.js'),bundle:true,platform:'node',format:'cjs',target:'node22',packages:'external',logLevel:'info'}).catch(()=>process.exit(1));
