import { Claim, LayerResult } from './verificationTypes';
import { RunPyright } from './pyrightRunner';
type Check = {
    bad: string[];
    unknown: string[];
};
export declare function deref(value: any, spec: any): {
    value?: any;
    error?: string;
};
export interface Operation {
    pathKey: string;
    operation: any;
    pathItem: any;
    params: Record<string, string>;
    url: URL;
}
export declare function findOperation(spec: any, endpoint: Claim): {
    match?: Operation;
    bad?: string;
    unknown?: string;
};
export declare function checkValue(value: any, raw: any, spec: any, label: string, serialized?: boolean, depth?: number): Check;
export declare function verifyAccessPoint({ claims, spec }: {
    claims: Claim[];
    spec: any;
}): Promise<LayerResult>;
export declare function verifyInputContract({ claims, spec }: {
    claims: Claim[];
    spec: any;
}): Promise<LayerResult>;
export declare function verifyOutputContract({ claims, spec, code }: {
    claims: Claim[];
    spec: any;
    code?: string;
}, runPyright?: RunPyright, allowPyright?: boolean): Promise<LayerResult>;
export declare function verifyContextual({ claims, spec }: {
    claims: Claim[];
    spec: any;
    code?: string;
}): Promise<LayerResult>;
export {};
//# sourceMappingURL=openApiVerifier.d.ts.map