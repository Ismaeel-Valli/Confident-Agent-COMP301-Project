"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ofType = exports.hashCode = exports.TIER_FACTORS = exports.ALL_LAYERS = exports.LAYER_WEIGHTS = void 0;
exports.result = result;
exports.unknown = unknown;
exports.aggregate = aggregate;
exports.aggregateExtracted = aggregateExtracted;
const crypto_1 = require("crypto");
exports.LAYER_WEIGHTS = { interface: 3, identifier: 3, access_point: 4, input_contract: 2, output_contract: 1, contextual: 2 };
exports.ALL_LAYERS = Object.keys(exports.LAYER_WEIGHTS);
exports.TIER_FACTORS = { tier_1: 1, tier_2: 0.8, tier_3: 0.9, tier_4: 0.5, none: 0 };
const hashCode = (code) => (0, crypto_1.createHash)('sha256').update(code).digest('hex');
exports.hashCode = hashCode;
function result(layer, state, tier, source, detail, kind = null) {
    return { layer, state, tier, weight: exports.LAYER_WEIGHTS[layer], evidence_source: source, evidence_detail: detail, hallucination_type: kind };
}
function unknown(layer, detail) { return result(layer, 'unverifiable', 'none', 'verification', detail); }
function aggregate(layer, rows, emptyReason) {
    const applicable = rows.filter(r => r.state !== 'not_applicable');
    if (!applicable.length)
        return result(layer, 'not_applicable', 'none', 'extraction / specification', rows.length ? rows.map(r => r.evidence_detail).join('\n') : emptyReason);
    const incorrect = applicable.filter(r => r.state === 'verified_incorrect');
    const unresolved = applicable.filter(r => r.state === 'unverifiable');
    const selected = incorrect.length ? incorrect.sort((a, b) => exports.TIER_FACTORS[b.tier] - exports.TIER_FACTORS[a.tier])[0]
        : unresolved.length ? unresolved[0] : applicable.sort((a, b) => exports.TIER_FACTORS[a.tier] - exports.TIER_FACTORS[b.tier])[0];
    return { ...selected, evidence_detail: rows.map(r => r.evidence_detail).join('\n'), claim_ids: rows.flatMap(r => r.claim_ids || []) };
}
const ofType = (claims, type) => claims.filter(c => c.type === type);
exports.ofType = ofType;
function aggregateExtracted(layer, claims, rows, emptyReason) {
    const r = aggregate(layer, rows, emptyReason);
    const relevant = { interface: ['import'], identifier: ['method_call'], access_point: ['endpoint'], input_contract: ['endpoint', 'input_field'], output_contract: ['output_field'], contextual: ['endpoint', 'input_field'] };
    r.claim_ids = claims.filter(c => relevant[layer].includes(c.type) && typeof c.id === 'string').map(c => c.id);
    if (claims.some(c => c.type === 'extraction_issue') && ['verified_correct', 'not_applicable'].includes(r.state)) {
        // Registry evidence for explicit imports is independent of whether response flow is
        // supported. Retain that evidence; do not claim that the import inventory is exhaustive.
        // The controller's extraction_complete gate still prohibits delivery.
        if (layer === 'interface' && r.state === 'verified_correct') {
            return { ...r, evidence_detail: r.evidence_detail + '\nEvidence covers the extracted imports only. Extraction is incomplete; additional claims may be missing and delivery remains blocked.' };
        }
        return unknown(layer, 'Extraction is incomplete; unsupported claims may be missing. ' + r.evidence_detail);
    }
    return r;
}
//# sourceMappingURL=verificationTypes.js.map