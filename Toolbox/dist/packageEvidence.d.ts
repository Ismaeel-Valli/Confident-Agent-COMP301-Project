import { Claim, LayerResult } from './verificationTypes';
export interface PackageEvidence {
    exists: boolean | null;
    status: 'found' | 'not_found' | 'unverifiable';
    latest_version?: string;
    summary?: string;
    source_url?: string;
    retrieved_at?: string;
    import_name?: string;
    distribution?: string;
}
export declare const IMPORT_DISTRIBUTIONS: Record<string, string>;
export declare function queryPypi({ library_name }: {
    library_name: string;
}, fetcher?: typeof fetch): Promise<PackageEvidence>;
export declare function verifyInterface({ claims, pypi_data }: {
    claims: Claim[];
    pypi_data?: Record<string, PackageEvidence>;
}): Promise<LayerResult>;
//# sourceMappingURL=packageEvidence.d.ts.map