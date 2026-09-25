import { catalog } from '../catalog';
import { makeTool, validatePath, type Context } from '../runtime';
/** LM Studio diagnostic tools. Use the external controller for enforced final delivery. */
import { type Tool } from '@lmstudio/sdk';
import { mkdir, writeFile } from 'fs/promises';
import { dirname, isAbsolute, relative } from 'path';
import { z } from 'zod';
import { extractClaims } from './claimExtractor';
import { queryPypi, verifyInterface } from './packageEvidence';
import { resolveApiSpec } from './specDiscovery';
import { verifyIdentifier, RunPyright } from './pyrightRunner';
import { verifyAccessPoint, verifyInputContract, verifyOutputContract, verifyContextual } from './openApiVerifier';
import { computeEwcs, makeDecision, presentReport, EWCSReport } from './verificationPolicy';
import { runIntervention } from './verificationController';
import { LayerResult } from './verificationTypes';
import { BUNDLED_REFERENCES, TOOLBOX_VERSION } from './bundledReferences';

export * from './verificationTypes';
export { EWCSAccumulator } from './verificationPolicy';
export type { EWCSReport, LayerContribution } from './verificationPolicy';

export interface ConfidenceAgentToolsDeps {
  isEnabled: boolean;
  allowPyright: boolean;
  context: Context;
  getWorkingDirectory: () => string;
  runPyright: RunPyright;
}

// --- Shared Zod schemas -----------------------------------------------

const contributionSchema = z.object({
  layer: z.string(),
  state: z.string(),
  tier: z.string(),
  weight: z.number(),
  tier_factor: z.number(),
  positive_contribution: z.number(),
  signed_contribution: z.number(),
});

const layerResultSchema = z.object({
  layer: z.string(),
  state: z.string(),
  tier: z.string(),
  weight: z.number(),
  evidence_source: z.string(),
  evidence_detail: z.string(),
  hallucination_type: z.string().nullable(),
  claim_ids: z.array(z.string()).optional(),
});

const ewcsReportSchema = z.object({
  task_id: z.string(),
  ewcs: z.number().nullable(),
  signed_score: z.number().nullable(),
  has_incorrect_layer: z.boolean(),
  total_applicable_weight: z.number(),
  positive_weight: z.number(),
  contributions: z.array(contributionSchema),
  missing_layers: z.array(z.string()),
  extraction_complete: z.boolean(),
  failed_layers: z.array(z.string()),
  unverifiable_layers: z.array(z.string()),
  candidate_hash: z.string().optional(),
  layer_results: z.array(layerResultSchema).optional(),
});

// --- Tool factory -----------------------------------------------------

export function createConfidenceAgentTools(deps: ConfidenceAgentToolsDeps): Tool[] {
  const tool = makeTool(deps.context);
  const claims = z.array(z.record(z.any()));
  const spec = z.record(z.any()).nullable().optional();
  const out: Tool[] = [];

  function add(
    name: string,
    description: string,
    parameters: Record<string, z.ZodTypeAny>,
    implementation: (p: any) => Promise<any>,
  ) {
    out.push(
      tool({
        name,
        description,
        parameters,
        implementation: async (p: any) => {
          if (!deps.isEnabled) throw new Error('Confidence Agent tools are disabled in plugin settings.');
          try {
            return await implementation(p);
          } catch (e) {
            return { error: String(e) };
          }
        },
      }),
    );
  }

  // --- verify_candidate -------------------------------------------------

  add(
    'verify_candidate',
    catalog.verify_candidate.description,
    {
      code: z.string(),
      spec,
      reference_id: z.enum(['jsonplaceholder-posts']).optional(),
      input_bindings: z.record(z.any()).optional(),
      task_id: z.string().optional(),
    },
    async (p) => {
      const required = [
        'extract_claims',
        'query_pypi',
        'verify_interface',
        'verify_identifier',
        'verify_access_point',
        'verify_input_contract',
        'verify_output_contract',
        'verify_contextual',
        'compute_ewcs',
        'make_decision',
        'present_report',
        'run_pyright',
      ];
      const disabled = required.filter((name) => !deps.context.enabled(name));
      if (disabled.length) throw new Error('Required tools are disabled: ' + disabled.join(', '));

      // Validation: exactly one of reference_id or spec must be supplied.
      const hasReference = typeof p.reference_id === 'string' && p.reference_id.length > 0;
      const hasSpec = p.spec != null;
      if (!hasReference && !hasSpec) {
        throw new Error(
          'verify_candidate requires either reference_id (a bundled reference id, e.g. "jsonplaceholder-posts") ' +
            'or spec (an OpenAPI 3.0 document). Neither was supplied. Call list_api_references to see available ' +
            'bundled references, or resolve_api_spec to fetch a spec first.',
        );
      }
      if (hasReference && hasSpec) {
        throw new Error('Supply reference_id or spec, not both.');
      }

      const reference = hasReference ? structuredClone(BUNDLED_REFERENCES[p.reference_id]) : p.spec ?? null;

      const r = await runIntervention(
        { ...p, spec: reference },
        {
          runPyright: deps.runPyright,
          allowPyright: deps.allowPyright,
          extract: (p) => extractClaims({ ...p, pythonExecutable: deps.context.pythonExecutable }),
        },
      );

      const v = r.attempts[r.attempts.length - 1].verification;
      return {
        toolbox_version: TOOLBOX_VERSION,
        decision: r.decision,
        report: r.report,
        candidate_hash: v.candidate_hash,
        reference_id: p.reference_id ?? null,
        spec_hash: v.spec_hash,
        ewcs_report: v.ewcs_report,
        layers: v.layers,
        extraction_issues: v.extraction.issues,
      };
    },
  );

  // --- spec + package lookup -------------------------------------------

  add('resolve_api_spec', catalog.resolve_api_spec.description, { base_url: z.string() }, resolveApiSpec);
  add('query_pypi', catalog.query_pypi.description, { library_name: z.string() }, queryPypi);

  // --- individual layer tools (debugging) ------------------------------

  add(
    'extract_claims',
    catalog.extract_claims.description,
    { code: z.string(), input_bindings: z.record(z.any()).optional() },
    (p) => extractClaims({ ...p, pythonExecutable: deps.context.pythonExecutable }),
  );
  add('verify_interface', catalog.verify_interface.description, { claims, pypi_data: z.record(z.any()).optional() }, verifyInterface);
  add('verify_identifier', catalog.verify_identifier.description, { code: z.string() }, (p) =>
    verifyIdentifier(p.code, deps.runPyright, deps.allowPyright),
  );
  add('verify_access_point', catalog.verify_access_point.description, { claims, spec }, verifyAccessPoint);
  add('verify_input_contract', catalog.verify_input_contract.description, { claims, spec }, verifyInputContract);
  add('verify_output_contract', catalog.verify_output_contract.description, { claims, spec, code: z.string().optional() }, (p) =>
    verifyOutputContract(p, deps.runPyright, deps.allowPyright),
  );
  add('verify_contextual', catalog.verify_contextual.description, { claims, spec, code: z.string().optional() }, verifyContextual);

  // --- scoring + decision ----------------------------------------------

  add(
    'compute_ewcs',
    catalog.compute_ewcs.description,
    {
      layer_results: z.array(z.record(z.any())),
      task_id: z.string().optional(),
      extraction_complete: z.boolean().optional(),
    },
    (p) => Promise.resolve(computeEwcs(p as { layer_results: LayerResult[] })),
  );
  add('make_decision', catalog.make_decision.description, { ewcs_report: z.record(z.any()) }, async (p) =>
    makeDecision(p.ewcs_report as EWCSReport),
  );

  // --- delivery --------------------------------------------------------

  add(
    'save_code',
    catalog.save_code.description,
    { code: z.string(), filename: z.string() },
    async (p) => {
      const base = deps.getWorkingDirectory();
      const path = validatePath(base, p.filename);
      const rel = relative(base, path);
      if (!p.filename.trim() || rel.startsWith('..') || isAbsolute(rel)) throw new Error('Invalid workspace-relative filename.');
      await mkdir(dirname(path), { recursive: true });
      await writeFile(path, p.code, 'utf8');
      return { path };
    },
  );

  add(
    'present_report',
    catalog.present_report.description,
    {
      code: z.string(),
      ewcs_report: ewcsReportSchema,
      decision: z.enum(['deliver', 'deliver_with_flag', 'correct', 'abstain']),
    },
    async (p) => presentReport(p),
  );

  // --- reference listing -----------------------------------------------

  add('list_api_references', catalog.list_api_references.description, {}, async () => ({
    toolbox_version: TOOLBOX_VERSION,
    references: Object.entries(BUNDLED_REFERENCES).map(([id, spec]: [string, any]) => ({
      id,
      info: spec.info,
      evidence: spec['x-confidence-evidence'],
    })),
  }));

  return out;
}