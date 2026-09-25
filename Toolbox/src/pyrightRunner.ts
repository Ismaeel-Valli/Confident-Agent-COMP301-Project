import { spawn } from 'child_process';
import { mkdtemp, writeFile, rm } from 'fs/promises';
import { tmpdir } from 'os';
import { join } from 'path';
import { hashCode, type LayerResult, type Extraction, result, unknown } from './verificationTypes';
import { extractClaims } from './claimExtractor';
export interface Diagnostic { severity: string; message: string; rule?: string; range?: any; file?: string; }
export interface PyrightResult {
  stdout: string; stderr: string; exit_code: number | null; signal?: string | null;
  timed_out?: boolean; error?: string; candidate_hash?: string; python_executable?: string;
  checker_version?: string; diagnostics?: Diagnostic[]; summary?: Record<string, any>;
}
export type RunPyright = (p: {python: string; timeout_seconds?: number}) => Promise<PyrightResult>;
async function launch(command: string, args: string[], timeout: number) {
  return new Promise<PyrightResult>(resolve => {
    const child = spawn(command, args, {stdio:'pipe', timeout});
    let stdout = '', stderr = '';
    child.stdout.setEncoding('utf8'); child.stderr.setEncoding('utf8');
    child.stdout.on('data', d => { stdout += d; }); child.stderr.on('data', d => { stderr += d; });
    child.on('error', e => resolve({stdout, stderr, exit_code:null, error:e.message}));
    child.on('close', (code, signal) => resolve({stdout, stderr, exit_code:code, signal, timed_out:signal === 'SIGTERM'}));
    child.stdin.end();
  });
}
export function createPyrightRunner(): RunPyright {
  return async ({python, timeout_seconds = 20}) => {
    const candidate_hash = hashCode(python);
    const env = await launch(process.env.CONFIDENCE_PYTHON || 'python', ['-c', 'import sys; print(sys.executable)'], 10000);
    if (env.exit_code !== 0 || !env.stdout.trim()) return {...env, candidate_hash, error:'Could not resolve the verification Python environment.'};
    const directory = await mkdtemp(join(tmpdir(), 'confidence-pyright-'));
    try {
      const path = join(directory,'candidate.py');
      await writeFile(path, python, 'utf8');
      const config = join(directory,'pyrightconfig.json');
      await writeFile(config, JSON.stringify({typeCheckingMode:'strict', pythonVersion:'3.12', include:['candidate.py'],
        reportMissingTypeStubs:'warning', reportUnknownVariableType:'warning', reportUnknownMemberType:'warning',
        reportUnknownArgumentType:'warning', reportUnknownParameterType:'warning', reportUnknownLambdaType:'warning'}));
      // Launch the pinned npm CLI via Node on Windows and POSIX; no .cmd shell dependency.
      const r = await launch(process.execPath, [require.resolve('pyright/index.js'), '--outputjson', '--project', config,
        '--pythonpath', env.stdout.trim(), path], Math.min(60, Math.max(0.1, timeout_seconds)) * 1000);
      const metadata = {candidate_hash, python_executable:env.stdout.trim()};
      try {
        const json = JSON.parse(r.stdout);
        return {...r,...metadata, checker_version:json.version, diagnostics:json.generalDiagnostics, summary:json.summary};
      } catch { return {...r,...metadata, error:r.error || 'Pyright returned no valid JSON diagnostics.'}; }
    } catch (e) {
      return {stdout:'',stderr:'',exit_code:null,candidate_hash,error:String(e)};
    } finally { await rm(directory,{recursive:true,force:true}); }
  };
}
export function parsePyright(r: PyrightResult, code: string): {diagnostics: Diagnostic[]; error?: string} {
  if (r.error || r.timed_out || r.signal || ![0,1].includes(r.exit_code as number)) return {diagnostics:[],error:r.error || `Pyright process failed (${r.exit_code ?? r.signal}). ${r.stderr}`};
  if (r.candidate_hash && r.candidate_hash !== hashCode(code)) return {diagnostics:[],error:'Pyright result belongs to a different candidate.'};
  try {
    const data = JSON.parse(r.stdout);
    if (!Array.isArray(data.generalDiagnostics) || !data.summary || data.summary.filesAnalyzed < 1 ||
        !Number.isInteger(data.summary.errorCount) || data.summary.errorCount < 0 ||
        data.generalDiagnostics.some((d:any) => typeof d.message !== 'string' || !['error','warning','information'].includes(d.severity))) throw new Error();
    const errors = data.generalDiagnostics.filter((d:Diagnostic) => d.severity === 'error').length;
    if (errors !== data.summary.errorCount || (r.exit_code === 0 && errors > 0) || (r.exit_code === 1 && errors === 0)) throw new Error();
    return {diagnostics:data.generalDiagnostics};
  } catch { return {diagnostics:[],error:'Missing, malformed or inconsistent Pyright JSON output.'}; }
}
export async function verifyIdentifier(code: string, runPyright: RunPyright, allowPyright = true, extraction?: Extraction): Promise<LayerResult> {
  if (!allowPyright) return unknown('identifier','Pyright is disabled.');
  if (!code.trim()) return unknown('identifier','No candidate supplied.');
  try {
    const parsed = parsePyright(await runPyright({python:code}), code);
    if (parsed.error) return unknown('identifier', parsed.error);
    const contradictionRules = new Set(['reportUndefinedVariable','reportAttributeAccessIssue','reportCallIssue',
      'reportArgumentType','reportAssignmentType','reportReturnType','reportOperatorIssue','reportIndexIssue',
      'reportRedeclaration','reportUnboundVariable','reportPossiblyUnboundVariable']);
    const annotationRules = new Set(['reportUnknownParameterType', 'reportMissingParameterType']);
    let unused:NonNullable<Extraction['unused_parameters']> = [];
    if (parsed.diagnostics.some(d => annotationRules.has(d.rule || ''))) {
      const context = extraction || await extractClaims({code});
      if (!context.error && context.candidate_hash === hashCode(code)) unused = context.unused_parameters || [];
    }
    const ignoredAnnotations = parsed.diagnostics.filter(d => annotationRules.has(d.rule || '') && unused.some(p =>
      d.range?.start?.line === p.line && Number.isInteger(d.range?.start?.character) &&
      d.range.start.character >= p.start_character && d.range.start.character < p.end_character));
    const relevant = parsed.diagnostics.filter(d => !/^report(?:Unused|Unnecessary)/.test(d.rule || '') && !ignoredAnnotations.includes(d));
    const incorrect = relevant.filter(d => d.severity === 'error' && (!d.rule || contradictionRules.has(d.rule)));
    if (incorrect.length) return result('identifier','verified_incorrect','tier_4','Pyright structured diagnostics',
      incorrect.map(d => `${d.rule || 'syntax/type error'}: ${d.message}`).join('\n'),'static_identifier_or_type_error');
    // Only errors are blocking. Warnings about missing annotations or unknown
    // types describe completeness, not identifier correctness. The extractor
    // separately tracks unused parameters, and a function whose parameters
    // have no annotations still has well-defined identifiers.
    const blocking = relevant.filter(d => d.severity === 'error');
    if (blocking.length) return unknown('identifier',
      'Incomplete static evidence: ' + blocking.map(d => `${d.rule}: ${d.message}`).join('\n'));
    return result('identifier','verified_correct','tier_4','Pyright structured diagnostics',
      'No blocking identifier/type diagnostics in the configured environment. Unused/unnecessary-code and missing-annotation notices do not establish an API error. This does not establish REST contracts or task behavior.' +
      (ignoredAnnotations.length ? '\nNonblocking annotation diagnostics for AST-confirmed unused parameters: ' + ignoredAnnotations.map(d=>`${d.rule}: ${d.message}`).join('; ') : ''));
  } catch (e) { return unknown('identifier',`Pyright failed: ${String(e)}`); }
}