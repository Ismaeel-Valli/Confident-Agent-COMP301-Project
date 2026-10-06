import { spawn } from 'child_process';
import { EXTRACTION_SCRIPT } from './extractorScript';
import { type Extraction, hashCode } from './verificationTypes';
const BOOTSTRAP = "import sys, json; exec(compile(json.loads(sys.stdin.readline()), '<extract_claims>', 'exec'))";
export async function extractClaims({ code, input_bindings = {}, pythonExecutable = process.env.CONFIDENCE_PYTHON || 'python' }: {code: string; input_bindings?: Record<string, any>; pythonExecutable?:string}): Promise<Extraction> {
  const failed = (error: string): Extraction => ({ claims: [], complete: false, issues: [], error, candidate_hash: hashCode(code) });
  if (!code.trim()) return failed('No candidate code supplied.');
  return new Promise(resolve => {
    // The script travels on stdin (first line, JSON-encoded): Windows limits command lines to 32,767 characters.
    const child = spawn(pythonExecutable, ['-c', BOOTSTRAP], { stdio: 'pipe', timeout: 10000 });
    let stdout = '', stderr = '';
    child.stdout.setEncoding('utf8'); child.stderr.setEncoding('utf8');
    child.stdout.on('data', d => { stdout += d; }); child.stderr.on('data', d => { stderr += d; });
    child.on('error', e => resolve(failed(`Python extraction could not start: ${e.message}`)));
    child.stdin.on('error', () => {});
    child.on('close', (exitCode, signal) => {
      if (exitCode !== 0 || signal) return resolve(failed(`Extraction failed (${exitCode ?? signal}): ${stderr}`));
      try {
        const data = JSON.parse(stdout);
        if (!Array.isArray(data.claims) || typeof data.complete !== 'boolean' || !Array.isArray(data.issues)) throw new Error('Invalid extractor result');
        if (!data.complete) data.claims.push({id:'extraction_limitations',type:'extraction_issue',issues:data.issues,error:data.error});
        resolve({ ...data, candidate_hash: hashCode(code) });
      } catch { resolve(failed(`Invalid extraction output: ${stderr || stdout.slice(0, 200)}`)); }
    });
    child.stdin.end(JSON.stringify(EXTRACTION_SCRIPT) + '\n' + JSON.stringify({ code, input_bindings }));
  });
}
