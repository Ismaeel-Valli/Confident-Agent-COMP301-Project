export declare function levenshteinDistance(a: string, b: string): number;
export declare function computeFuzzyScore(query: string, candidate: string): number;
export declare function rankFuzzyMatches(query: string, candidates: string[], limit?: number): Array<{
    value: string;
    score: number;
}>;
//# sourceMappingURL=fuzzySearch.d.ts.map