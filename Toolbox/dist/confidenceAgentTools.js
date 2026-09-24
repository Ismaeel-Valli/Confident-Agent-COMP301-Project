"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.EWCSAccumulator = void 0;
exports.createConfidenceAgentTools = createConfidenceAgentTools;
/** LM Studio diagnostic tools. Use the external controller for enforced final delivery. */
const sdk_1 = require("@lmstudio/sdk");
const promises_1 = require("fs/promises");
const path_1 = require("path");
const zod_1 = require("zod");
const claimExtractor_1 = require("./claimExtractor");
const packageEvidence_1 = require("./packageEvidence");
const specDiscovery_1 = require("./specDiscovery");
const pyrightRunner_1 = require("./pyrightRunner");
const openApiVerifier_1 = require("./openApiVerifier");
const verificationPolicy_1 = require("./verificationPolicy");
const verificationController_1 = require("./verificationController");
const bundledReferences_1 = require("./bundledReferences");
__exportStar(require("./verificationTypes"), exports);
var verificationPolicy_2 = require("./verificationPolicy");
Object.defineProperty(exports, "EWCSAccumulator", { enumerable: true, get: function () { return verificationPolicy_2.EWCSAccumulator; } });
function createConfidenceAgentTools(deps) {
    const claims = zod_1.z.array(zod_1.z.record(zod_1.z.any())), spec = zod_1.z.record(zod_1.z.any()).nullable().optional();
    const out = [];
    function add(name, description, parameters, implementation) {
        out.push((0, sdk_1.tool)({ name, description, parameters, implementation: async (p) => {
                if (!deps.isEnabled)
                    throw new Error('Confidence Agent tools are disabled in plugin settings.');
                try {
                    return await implementation(p);
                }
                catch (e) {
                    return { error: String(e) };
                }
            } }));
    }
    add('verify_candidate', 'Run all six verifiers, score and report exact candidate API claims. For JSONPlaceholder GET /posts or /posts/1 use reference_id=jsonplaceholder-posts; otherwise supply reviewed spec or null. Does not prove task behavior. External controller enforces delivery and one correction.', { code: zod_1.z.string(), spec, reference_id: zod_1.z.enum(['jsonplaceholder-posts']).optional(), input_bindings: zod_1.z.record(zod_1.z.any()).optional(), task_id: zod_1.z.string().optional() }, async (p) => {
        if (p.reference_id && p.spec != null)
            throw new Error('Supply reference_id or spec, not both.');
        const reference = p.reference_id ? structuredClone(bundledReferences_1.BUNDLED_REFERENCES[p.reference_id]) : p.spec ?? null;
        const r = await (0, verificationController_1.runIntervention)({ ...p, spec: reference }, { runPyright: deps.runPyright, allowPyright: deps.allowPyright });
        const v = r.attempts[r.attempts.length - 1].verification;
        return { toolbox_version: bundledReferences_1.TOOLBOX_VERSION, decision: r.decision, report: r.report, candidate_hash: v.candidate_hash,
            reference_id: p.reference_id ?? null, spec_hash: v.spec_hash, reference_evidence: reference?.['x-confidence-evidence'] ?? null,
            ewcs_report: v.ewcs_report, layers: v.layers, extraction_issues: v.extraction.issues };
    });
    add('resolve_api_spec', 'Discover a JSON OpenAPI 3.0 contract and provenance; unresolved discovery returns spec:null. Review and freeze a snapshot for experiments.', { base_url: zod_1.z.string() }, specDiscovery_1.resolveApiSpec);
    add('query_pypi', 'Query package metadata. exists:null/status:unverifiable means lookup failed, not that the package is nonexistent.', { library_name: zod_1.z.string() }, packageEvidence_1.queryPypi);
    add('extract_claims', 'Static Python extraction for a documented requests subset. Returns complete/limitations, operation-linked claims and a candidate hash. Runtime input values can be bound explicitly.', { code: zod_1.z.string(), input_bindings: zod_1.z.record(zod_1.z.any()).optional() }, claimExtractor_1.extractClaims);
    add('verify_interface', 'Check imports against registry evidence and explicit import/distribution mappings. Missing evidence and registry failures stay unverifiable.', { claims, pypi_data: zod_1.z.record(zod_1.z.any()).optional() }, packageEvidence_1.verifyInterface);
    add('verify_identifier', 'Check structured Pyright diagnostics for the exact code. Missing packages/stubs and process failure are unverifiable.', { code: zod_1.z.string() }, p => (0, pyrightRunner_1.verifyIdentifier)(p.code, deps.runPyright, deps.allowPyright));
    add('verify_access_point', 'Match server origin/base path, endpoint and HTTP method. Dynamic endpoints and unsupported specs remain unverifiable.', { claims, spec }, openApiVerifier_1.verifyAccessPoint);
    add('verify_input_contract', 'Check every request separately: required parameters, locations, supported values and JSON bodies. Unknown values block verification.', { claims, spec }, openApiVerifier_1.verifyInputContract);
    add('verify_output_contract', 'Follow response provenance and local references to success schemas. A clean Pyright run never substitutes for JSON response evidence.', { claims, spec, code: zod_1.z.string().optional() }, p => (0, openApiVerifier_1.verifyOutputContract)(p, deps.runPyright, deps.allowPyright));
    add('verify_contextual', 'Check operation-level inherited authentication alternatives against actual request arguments. Comments are not authentication.', { claims, spec, code: zod_1.z.string().optional() }, openApiVerifier_1.verifyContextual);
    add('compute_ewcs', 'Diagnostic score with canonical weights; missing checks retain weight and an empty applicable set has ewcs:null. Controller results are authoritative.', { layer_results: zod_1.z.array(zod_1.z.record(zod_1.z.any())), task_id: zod_1.z.string().optional(), extraction_complete: zod_1.z.boolean().optional() }, p => Promise.resolve((0, verificationPolicy_1.computeEwcs)(p)));
    add('make_decision', 'Validate all six contributions. Contradiction requests correction; incomplete/unverifiable critical checks abstain before thresholds 0.85/0.60.', { ewcs_report: zod_1.z.record(zod_1.z.any()) }, async (p) => (0, verificationPolicy_1.makeDecision)(p.ewcs_report));
    add('save_code', 'Save a candidate for inspection. This is not verified delivery; use the controller for user-facing output.', { code: zod_1.z.string(), filename: zod_1.z.string() }, async (p) => {
        const base = deps.getWorkingDirectory(), path = (0, path_1.resolve)(base, p.filename), rel = (0, path_1.relative)(base, path);
        if (!p.filename.trim() || rel.startsWith('..') || (0, path_1.isAbsolute)(rel))
            throw new Error('Invalid workspace-relative filename.');
        await (0, promises_1.mkdir)((0, path_1.dirname)(path), { recursive: true });
        await (0, promises_1.writeFile)(path, p.code, 'utf8');
        return { path };
    });
    add('present_report', 'Format a score report. Code is withheld for abstain/correct and inconsistent delivery requests. Native chat remains model controlled; use the external controller for enforcement.', { code: zod_1.z.string(), ewcs_report: zod_1.z.record(zod_1.z.any()), decision: zod_1.z.enum(['deliver', 'deliver_with_flag', 'correct', 'abstain']) }, async (p) => (0, verificationPolicy_1.presentReport)(p));
    return out;
}
//# sourceMappingURL=confidenceAgentTools.js.map