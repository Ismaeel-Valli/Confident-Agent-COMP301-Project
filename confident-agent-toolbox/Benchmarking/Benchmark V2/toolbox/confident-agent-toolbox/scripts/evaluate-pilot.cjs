const {spawnSync}=require('node:child_process');
const {join}=require('node:path');
const r=spawnSync(process.env.CONFIDENCE_PYTHON || 'python',[join(__dirname,'../evaluation/jsonplaceholder_behavior.py')],{stdio:'inherit'});
if(r.error) console.error(r.error.message);
process.exitCode=r.status ?? 1;
