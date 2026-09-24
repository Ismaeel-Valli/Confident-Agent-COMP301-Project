/** LM Studio diagnostic tools. Use the external controller for enforced final delivery. */
import { type Tool } from '@lmstudio/sdk';
import { RunPyright } from './pyrightRunner';
export * from './verificationTypes';
export { EWCSAccumulator } from './verificationPolicy';
export type { EWCSReport, LayerContribution } from './verificationPolicy';
export interface ConfidenceAgentToolsDeps {
    isEnabled: boolean;
    allowPyright: boolean;
    getWorkingDirectory: () => string;
    runPyright: RunPyright;
}
export declare function createConfidenceAgentTools(deps: ConfidenceAgentToolsDeps): Tool[];
//# sourceMappingURL=confidenceAgentTools.d.ts.map