const {build}=require('esbuild');
build({entryPoints:['.lmstudio/entry.ts'],outfile:'.lmstudio/dev.js',bundle:true,platform:'node',format:'cjs',target:'node22',packages:'external',logLevel:'info'}).catch(()=>process.exit(1));
