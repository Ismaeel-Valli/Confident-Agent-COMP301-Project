export declare function resolveApiSpec({ base_url }: {
    base_url: string;
}): Promise<{
    spec: null;
    source_url: null;
    note: string;
    retrieved_at?: undefined;
    content_hash?: undefined;
    review_required?: undefined;
} | {
    spec: any;
    source_url: string;
    retrieved_at: string;
    content_hash: string;
    review_required: boolean;
    note?: undefined;
}>;
//# sourceMappingURL=specDiscovery.d.ts.map