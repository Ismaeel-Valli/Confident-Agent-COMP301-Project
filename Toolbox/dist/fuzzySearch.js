"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.levenshteinDistance = levenshteinDistance;
exports.computeFuzzyScore = computeFuzzyScore;
exports.rankFuzzyMatches = rankFuzzyMatches;
function normalize(input) {
    return input.toLowerCase().replace(/\s+/g, " ").trim();
}
function levenshteinDistance(a, b) {
    const left = normalize(a);
    const right = normalize(b);
    const m = left.length;
    const n = right.length;
    if (m === 0)
        return n;
    if (n === 0)
        return m;
    const prev = new Array(n + 1);
    const curr = new Array(n + 1);
    for (let j = 0; j <= n; j++)
        prev[j] = j;
    for (let i = 1; i <= m; i++) {
        curr[0] = i;
        for (let j = 1; j <= n; j++) {
            const cost = left[i - 1] === right[j - 1] ? 0 : 1;
            curr[j] = Math.min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost);
        }
        for (let j = 0; j <= n; j++)
            prev[j] = curr[j];
    }
    return prev[n];
}
function computeFuzzyScore(query, candidate) {
    const q = normalize(query);
    const c = normalize(candidate);
    if (!q || !c)
        return 0;
    if (q === c)
        return 1;
    if (c.includes(q)) {
        const coverage = q.length / c.length;
        return Math.min(1, 0.85 + coverage * 0.15);
    }
    const distance = levenshteinDistance(q, c);
    const maxLen = Math.max(q.length, c.length);
    return Math.max(0, 1 - distance / maxLen);
}
function rankFuzzyMatches(query, candidates, limit = 5) {
    const ranked = candidates
        .map(value => ({ value, score: computeFuzzyScore(query, value) }))
        .sort((a, b) => b.score - a.score || a.value.length - b.value.length)
        .slice(0, limit);
    return ranked;
}
//# sourceMappingURL=fuzzySearch.js.map