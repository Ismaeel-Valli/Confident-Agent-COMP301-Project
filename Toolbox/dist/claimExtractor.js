"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.extractClaims = extractClaims;
const child_process_1 = require("child_process");
const extractorScript_1 = require("./extractorScript");
const verificationTypes_1 = require("./verificationTypes");
async function extractClaims({ code, input_bindings = {} }) {
    const failed = (error) => ({ claims: [], complete: false, issues: [], error, candidate_hash: (0, verificationTypes_1.hashCode)(code) });
    if (!code.trim())
        return failed('No candidate code supplied.');
    return new Promise(resolve => {
        const child = (0, child_process_1.spawn)(process.env.CONFIDENCE_PYTHON || 'python', ['-c', extractorScript_1.EXTRACTION_SCRIPT], { stdio: 'pipe', timeout: 10000 });
        let stdout = '', stderr = '';
        child.stdout.setEncoding('utf8');
        child.stderr.setEncoding('utf8');
        child.stdout.on('data', d => { stdout += d; });
        child.stderr.on('data', d => { stderr += d; });
        child.on('error', e => resolve(failed(`Python extraction could not start: ${e.message}`)));
        child.stdin.on('error', () => { });
        child.on('close', (exitCode, signal) => {
            if (exitCode !== 0 || signal)
                return resolve(failed(`Extraction failed (${exitCode ?? signal}): ${stderr}`));
            try {
                const data = JSON.parse(stdout);
                if (!Array.isArray(data.claims) || typeof data.complete !== 'boolean' || !Array.isArray(data.issues))
                    throw new Error('Invalid extractor result');
                if (!data.complete)
                    data.claims.push({ id: 'extraction_limitations', type: 'extraction_issue', issues: data.issues, error: data.error });
                resolve({ ...data, candidate_hash: (0, verificationTypes_1.hashCode)(code) });
            }
            catch {
                resolve(failed(`Invalid extraction output: ${stderr || stdout.slice(0, 200)}`));
            }
        });
        child.stdin.end(JSON.stringify({ code, input_bindings }));
    });
}
//# sourceMappingURL=claimExtractor.js.map