// Sections 5-7.
const TS = '../../../Findings/Statistical Analysis/tempstats/charts/';
const RF = '../../../Findings/Statistical Analysis/tempstats/report_figures/charts/';
const DG = 'figures/';

module.exports = [
  // -------------------------------------------------------------- 5
  { t: 'h1', text: '5 Baseline Evaluation' },
  { t: 'p', text: 'The experiment uses one model served one way: Qwen3.5-9B (GGUF) in LM Studio, at temperature 0.2 without a fixed seed, with reasoning off and a 30,208-token context. Both conditions receive the identical prompt file; the baseline system prompt asks only for the code in one Python block. The experiment was run three times, with the Q4_K_M, Q6_K and Q8_0 quantizations of the same weights, between 30 September and 3 October 2026 (full configuration in Appendix B.4).' },
  { t: 'table', key: 'baseline', caption: 'Baseline: class of the code delivered to the user (990 tasks per run, pilot excluded).', cols: [2.4, 1.3, 1.3, 1.3],
    header: ['Class', 'Q4_K_M', 'Q6_K', 'Q8_0'], align: [null, 'r', 'r', 'r'],
    rows: [
      ['Correct', '247 (24.9%)', '365 (36.9%)', '341 (34.4%)'],
      ['A: API hallucination', '513 (51.8%)', '503 (50.8%)', '546 (55.2%)'],
      ['B: valid call, wrong task', '79 (8.0%)', '56 (5.7%)', '58 (5.9%)'],
      ['Runtime failure or no code', '151 (15.3%)', '66 (6.7%)', '45 (4.5%)'],
    ] },
  { t: 'p', text: 'Between 51% and 55% of baseline answers contained an API hallucination at every quantization ({tab:baseline}): the rate reflects what the model knows, not its numerical precision, while the lower quantization pays in ordinary programming errors instead. Most baseline hallucinations (1,303 of 1,562 across the three runs) are a wrong host, version or base path, and {fig:cutoff} shows where they come from. These are errors the model cannot detect by introspection, and that a frozen specification detects deterministically.' },
  { t: 'bullets', items: [
    '**Retired versions.** 78% of Petstore answers called the Swagger 2 host `petstore.swagger.io/v2`, which dominates tutorials; 63% of REST Countries answers called the deprecated `restcountries.com/v3.1`.',
    '**Extrapolated versions.** Told "REST Countries v5", the model invented `restcountries.com/v5.1/...` in 35% of answers; only 4 of 447 reached the real host.',
    '**Sibling confusion.** 45% of DummyJSON answers called JSONPlaceholder. Where the model\'s knowledge is current (JSONPlaceholder, GitHub), the host was almost always right.',
  ] },
  { t: 'fig', key: 'cutoff', file: RF + 'R03_training_cutoff_versions.png', width: 500, caption: 'Which API host and version each baseline answer called (three runs pooled). The model reproduces versions from its training data and extrapolates versions it has never seen.' },

  // -------------------------------------------------------------- 6
  { t: 'h1', text: '6 Confident Agent Architecture and Design' },
  { t: 'h2', text: '6.1 Architecture overview' },
  { t: 'p', text: 'The organising principle comes from the course\'s Trust-by-Design notes: generation alone must not confer authority on an output (Vorster, 2026a; pattern mapping in Appendix C.1). The model proposes code, a deterministic tool judges it against external evidence, and the tool, not the model, decides what may be released ({fig:components}). The toolbox runs as an LM Studio tools provider or, in the experiment, through a Node.js bridge with the same `verify_candidate` implementation; the evaluator shares no code with it.' },
  { t: 'fig', key: 'components', file: DG + 'D02_deployment_components.png', width: 500, caption: 'Deployment and component view (UML). All components run on one workstation; the evaluator is independent of the toolbox.' },
  { t: 'p', text: 'We attached verification as an **in-loop tool through function calling** rather than as a post-hoc controller, an MCP server or a multi-agent pipeline (Appendix C.2), because the package a developer would run is a model, a system prompt and one tool. The model then controls the conversation and may skip or repeat steps, so three safeguards keep the delivery decision with the tool: the benchmark scores the tool\'s decision on the last verified candidate, the tool\'s report embeds the candidate\'s SHA-256, and every protocol deviation is recorded.' },
  { t: 'h2', text: '6.2 Claims, layers and evidence' },
  { t: 'p', text: 'The extractor parses the candidate with Python\'s `ast` module (it never runs it); values that exist only at run time become typed holes, so `f"https://api.github.com/orgs/{org}"` is matched against OpenAPI path templates. Six layers then check the claims, each against one kind of evidence (weights in brackets):' },
  { t: 'bullets', items: [
    '**L1 Interface (3):** imported modules exist. **L2 Identifier (3):** Pyright 1.1.414 finds no undefined name, attribute or call.',
    '**L3 Access point (4):** host, base path, path and method match a declared operation of the frozen specification.',
    '**L4 Input contract (2)**, **L5 Output contract (1)** and **L6 Contextual (2):** parameters and request body, response fields read, and security requirements match the operation.',
  ] },
  { t: 'p', text: 'Each layer returns one verdict (verified correct, verified incorrect, unverifiable or not applicable) with an evidence tier. The evidence is the same frozen, hashed snapshots as the dataset, **selected by the host the candidate itself calls**; the model never supplies a specification. A host without frozen evidence makes layers 3 to 6 unverifiable, so an invented host cannot be "verified". Dynamic specification discovery was rejected because a live specification can change between runs and four of the six APIs publish none (Appendix C.5).' },
  { t: 'h2', text: '6.3 The Evidence-Weighted Confidence Score' },
  { t: 'p', text: 'The EWCS is the proportion of the applicable verification weight supported by positive evidence. With A the applicable layers, w_l a layer\'s weight, t_l the factor of its evidence tier and c_l = 1 if it is verified correct (0 otherwise):' },
  { t: 'eq', name: 'ewcs' },
  { t: 'p', text: 'The weights convert a severity ranking of the layers with the rank-sum rule (Stillwell, Seaver and Edwards, 1981; Barron and Barrett, 1996); a wrong access point ranks first because nothing downstream can then be right. Tier factors discount weaker evidence: 1.0 for a provider\'s specification, 0.8 for a curated specification or registry record, 0.5 for a clean Pyright run, 0 for none. The highest attainable scores are therefore known in advance: only fully modelled official specifications can reach 0.85, and curated ones cannot exceed 0.74 (Appendix C.6). The EWCS measures **evidence coverage, not the probability that the code is correct**.' },
  { t: 'h2', text: '6.4 The decision policy: score, constraints and gate' },
  { t: 'p', text: 'The policy ({fig:activity}) applies three ordered rules, and the first two do not consult the score:' },
  { t: 'numbers', ref: 'numbers1', items: [
    '**Safety constraint.** If any layer is verified incorrect, the code is not released: on a first candidate the agent may correct it once and must have the new code verified; on a second it abstains.',
    '**Uncertainty gate.** If any applicable layer is unverifiable, failed to run or had incomplete extraction, the agent abstains.',
    '**Thresholds.** Otherwise EWCS ≥ 0.85 delivers, 0.60 ≤ EWCS < 0.85 delivers with a flag, and a lower score abstains.',
  ] },
  { t: 'fig', key: 'activity', file: DG + 'D05_activity_decision.png', width: 290, caption: 'Activity diagram (UML) of the decision policy. Hard rules precede the score; the renderer releases code only when its hash matches the verified candidate.' },
  { t: 'p', text: 'The design thus has three parts that are easily conflated. The **confidence score** (EWCS) summarises how much evidence supports a candidate. The **hard verification constraints**, the safety constraint and the uncertainty gate, decide whether code may be released at all. The **decision policy** composes them in a fixed order, so the score is consulted only for candidates the constraints already allow. A candidate that passes the gate has every applicable layer verified and so scores at least 0.65, which means the 0.60 threshold can never bind: in this design the score decides only whether delivered code carries a flag (confirmed empirically in Section 8.4).' },

  // -------------------------------------------------------------- 7
  { t: 'h1', text: '7 Experimental Methodology' },
  { t: 'h2', text: '7.1 Design, and the structure of the observations' },
  { t: 'p', text: 'The experiment is a **paired, within-task comparison**: each of the 990 scored tasks is answered by the same model with the same settings in the baseline and in the intervention condition, and the primary outcome is whether class A code reached the user (pipeline in Appendix B.5).' },
  { t: 'p', text: 'It was run three times, under the Q4_K_M, Q6_K and Q8_0 quantizations, which gives **2,970 task pairs**. These are **not three independent replications**: each run uses the same 990 tasks and prompts and the same model apart from numerical precision, so a task\'s outcomes are strongly correlated across runs. Whether the baseline hallucinated on a task agrees between quantizations with κ = 0.69–0.74, and 412 tasks hallucinated in all three runs while 363 hallucinated in none (Appendix D.10). Within a run each task was sampled once per condition, and tasks are grouped into 141 operation families and six APIs. We therefore test each run separately on its 990 pairs, treat agreement across the runs as evidence of **robustness to quantization** rather than replication, use pooled figures only descriptively, and allow for the families with a cluster bootstrap.' },
  { t: 'p', text: 'The intervention is a **package**: the Confident Agent prompt (which prescribes the workflow and names the hosts with frozen evidence), the verification tool, one correction and abstention. Each condition generates its own code, because the prompt also shapes the first answer. The experiment therefore measures the **combined architecture** and was not designed to separate its components; Section 8.2 reports what the recorded data can and cannot say about them.' },
  { t: 'h2', text: '7.2 Procedure and measurements' },
  { t: 'p', text: 'In the **baseline**, the code block of the model\'s single reply is what the user receives. In the **intervention**, the model may call `verify_candidate`; the harness stores each candidate byte for byte with the tool\'s result. The prompt allows one correction, and only if a layer is verified incorrect; after four turns, a fixed message asks for the tool\'s report. What reaches the user is the code the tool delivered on the last verified candidate. For every task and condition we record the delivered code\'s class, the verifier\'s decision, EWCS and layer states, corrections and protocol deviations, three behaviour checks, time, tokens, and GPU and CPU energy priced at R4.1109 per kWh including VAT (eThekwini Municipality, 2026; Appendix B.6).' },
  { t: 'h2', text: '7.3 Independent evaluation and manual review' },
  { t: 'p', text: 'The grader must not trust the agent\'s own verdict (Vorster, 2026c), so the evaluator shares no code with the toolbox and uses a different method. It executes each candidate in an isolated process with the task\'s test inputs and a recording stand-in for `requests` that sends nothing, which yields the exact requests and every response field read. It runs each candidate against a success, an empty and an error response for the behaviour checks, and compares the requests with the expected request and the pinned specification (Appendix B.7). It scored all 1,000 reference solutions correct before scoring any model output.' },
  { t: 'p', text: 'Names that a curated specification does not list left **396 undetermined candidates**: 46 had reached the user and 350 had been withheld. Each open question was answered once from the provider\'s documentation or harmless live read requests and recorded as a rule (Appendix I). The first review was AI-assisted; a group member independently reviewed the 46 decisive candidates and agreed on 43 (Cohen\'s κ = 0.88), and the group settled the three disagreements as correct, which changes no hallucination figure.' },
  { t: 'h2', text: '7.4 Pre-registration and statistical analysis' },
  { t: 'p', text: 'Scoring rules, outcomes and tests were fixed in an evaluation plan on 27 September 2026, before benchmark run 2, and later changes were logged (Appendix B.9). The primary test is the exact two-sided McNemar test within each run (McNemar, 1947), α = 0.05, with Holm\'s correction across the three runs (Holm, 1979). Differences carry 95% bootstrap intervals over tasks and over the 141 operation families (Efron and Tibshirani, 1993). Subgroups are descriptive; costs use the Wilcoxon signed-rank test (Wilcoxon, 1945), the EWCS the ROC area, and agreement Cohen\'s κ (Cohen, 1960; full plan in Appendix B.10).' },
];
