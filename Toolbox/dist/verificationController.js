"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.verifyCandidate = verifyCandidate;
exports.runIntervention = runIntervention;
const claimExtractor_1 = require("./claimExtractor");
const packageEvidence_1 = require("./packageEvidence");
const pyrightRunner_1 = require("./pyrightRunner");
const openApiVerifier_1 = require("./openApiVerifier");
const verificationPolicy_1 = require("./verificationPolicy");
const verificationTypes_1 = require("./verificationTypes");
async function verifyCandidate(request, deps = {}) {
    const code = request.code, candidate_hash = (0, verificationTypes_1.hashCode)(code), snapshot = structuredClone(request.spec), bindings = structuredClone(request.input_bindings || {});
    let extraction;
    try {
        extraction = await (deps.extract || claimExtractor_1.extractClaims)({ code, input_bindings: bindings });
    }
    catch (e) {
        extraction = { claims: [], complete: false, issues: [], error: String(e) };
    }
    if (!extraction || !Array.isArray(extraction.claims) || typeof extraction.complete !== 'boolean')
        extraction = { claims: [], complete: false, issues: [], error: 'Malformed extractor response.' };
    if (extraction.candidate_hash && extraction.candidate_hash !== candidate_hash)
        extraction = { claims: [], complete: false, issues: [], error: 'Extraction candidate hash mismatch.' };
    if (extraction.error)
        extraction.complete = false;
    const packages = Object.create(null);
    for (const imp of (0, verificationTypes_1.ofType)(extraction.claims, 'import')) {
        const name = String(imp.library || '').split('.')[0];
        if (imp.stdlib || imp.local || Object.hasOwn(packages, name))
            continue;
        try {
            packages[name] = await (deps.lookupPackage || (name => (0, packageEvidence_1.queryPypi)({ library_name: name })))(name);
        }
        catch (e) {
            packages[name] = { exists: null, status: 'unverifiable', summary: String(e) };
        }
    }
    let pyright = null, pyrightPromise = null;
    const run = deps.runPyright || (0, pyrightRunner_1.createPyrightRunner)();
    const cached = (p) => {
        if (p.python !== code)
            throw new Error('Checker must analyze the exact candidate.');
        if (!pyrightPromise)
            pyrightPromise = run(p).then(r => { pyright = r; return r; });
        return pyrightPromise;
    };
    const claims = extraction.claims;
    const actions = {
        interface: () => (0, packageEvidence_1.verifyInterface)({ claims, pypi_data: packages }), identifier: () => (0, pyrightRunner_1.verifyIdentifier)(code, cached, deps.allowPyright !== false, extraction),
        access_point: () => (0, openApiVerifier_1.verifyAccessPoint)({ claims, spec: snapshot }), input_contract: () => (0, openApiVerifier_1.verifyInputContract)({ claims, spec: snapshot }),
        output_contract: () => (0, openApiVerifier_1.verifyOutputContract)({ claims, spec: snapshot, code }, cached, deps.allowPyright !== false),
        contextual: () => (0, openApiVerifier_1.verifyContextual)({ claims, spec: snapshot })
    };
    const failed = [], layers = [];
    for (const layer of verificationTypes_1.ALL_LAYERS) {
        try {
            let r = await actions[layer]();
            if (!r || r.layer !== layer)
                throw new Error('Missing/mismatched layer result.');
            if (!extraction.complete && r.state === 'not_applicable')
                r = (0, verificationTypes_1.unknown)(layer, 'Extraction was incomplete; absence of relevant claims does not establish inapplicability.');
            layers.push(r);
        }
        catch (e) {
            failed.push(layer);
            layers.push((0, verificationTypes_1.unknown)(layer, `Required verifier failed: ${String(e)}`));
        }
    }
    const ewcs_report = (0, verificationPolicy_1.computeEwcs)({ layer_results: layers, task_id: request.task_id, extraction_complete: extraction.complete, failed_layers: failed });
    ewcs_report.candidate_hash = candidate_hash;
    return { candidate_hash, spec_hash: (0, verificationTypes_1.hashCode)(JSON.stringify(snapshot ?? null)), bindings_hash: (0, verificationTypes_1.hashCode)(JSON.stringify(bindings)), extraction, layers, ewcs_report,
        decision: (0, verificationPolicy_1.makeDecision)(ewcs_report), evidence: { packages, pyright } };
}
async function runIntervention(request, deps = {}) {
    // Freeze task evidence across the single correction attempt.
    const frozen = { ...request, spec: structuredClone(request.spec), input_bindings: structuredClone(request.input_bindings || {}) };
    const attempts = [{ code: request.code, verification: await verifyCandidate(frozen, deps) }];
    let correction_error = null;
    if (attempts[0].verification.decision === 'correct' && deps.correct) {
        try {
            const revised = await deps.correct({ code: request.code, verification: structuredClone(attempts[0].verification), spec: structuredClone(frozen.spec), input_bindings: structuredClone(frozen.input_bindings) });
            if (typeof revised !== 'string' || !revised.trim())
                throw new Error('Correction produced no code.');
            attempts.push({ code: revised, verification: await verifyCandidate({ ...frozen, code: revised }, deps) });
        }
        catch (e) {
            correction_error = String(e);
        }
    }
    const last = attempts[attempts.length - 1], raw = (0, verificationPolicy_1.makeDecision)(last.verification.ewcs_report, attempts.length - 1);
    const decision = raw === 'correct' || correction_error ? 'abstain' : raw;
    const rendered = (0, verificationPolicy_1.presentReport)({ code: last.code, ewcs_report: last.verification.ewcs_report, decision });
    return { decision: rendered.decision, delivered_code: rendered.code_included ? last.code : null, report: rendered.report, attempts,
        correction_attempted: attempts[0].verification.decision === 'correct' && !!deps.correct, correction_error };
}
//# sourceMappingURL=verificationController.js.map