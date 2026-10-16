// Front matter and sections 1-4.
const TS = '../../../Findings/Statistical Analysis/tempstats/charts/';
const RF = '../../../Findings/Statistical Analysis/tempstats/report_figures/charts/';
const DG = 'figures/';

module.exports = [
  // ============================================================== TITLE PAGE
  { t: 'section', kind: 'title' },
  { t: 'title', text: 'COMP301', size: 40, bold: true, color: '1F3864', before: 900 },
  { t: 'title', text: 'Software Design', size: 32, after: 300 },
  { t: 'title', text: 'Confidence Agent', size: 30, after: 300 },
  { t: 'title', text: 'Static Verification of REST API', size: 44, bold: true, color: '1F3864' },
  { t: 'title', text: 'Hallucinations in LLM-Generated Code', size: 44, bold: true, color: '1F3864', after: 300 },
  { t: 'title', text: 'Final Report', size: 34, after: 1400 },
  { t: 'title', text: 'An investigation into how thoughtful software design can improve the trustworthiness', size: 24 },
  { t: 'title', text: 'of AI systems through benchmark design, experimental methodology,', size: 24 },
  { t: 'title', text: 'validation architectures, and evidence-based evaluation.', size: 24, after: 1200 },
  { t: 'title', text: 'by The Skeptics', size: 28, bold: true, after: 300 },
  { t: 'title', text: 'University of KwaZulu-Natal', size: 26 },

  // ============================================================== FRONT MATTER
  { t: 'section', kind: 'front' },
  { t: 'fronth', text: 'Project Formalities' },
  { t: 'p', text: '**Domain:** Static Verification of API Hallucinations in LLM-Generated Code' },
  { t: 'p', text: '**Group Name:** The Skeptics' },
  { t: 'p', text: '**Group Members:**' },
  { t: 'members', rows: [['Jawad Kachbal', '223037045'], ['Joshua Blom', '224039813'], ['Mahomed Valli Mahomed', '224005878'], ['Andiswa Hlengwa', '221002430'], ['Abiel Govender', '224058851']] },
  { t: 'fronth', text: 'Abstract', pageBreak: true },
  { t: 'p', text: 'Large language models write plausible code that calls web APIs which do not exist, at versions that were retired, with parameters the provider never documented. This report investigates whether a **Confident Agent** can stop such REST API hallucinations from reaching the user. The agent pairs a local model (Qwen3.5-9B served by LM Studio) with a prompt and a tool that verifies every API claim in a candidate program against **frozen, hashed OpenAPI specifications** across six layers, scores the evidence with an **Evidence-Weighted Confidence Score (EWCS)**, and applies a decision policy that delivers, flags, corrects once, or withholds the code.' },
  { t: 'p', text: 'We built a frozen benchmark of 1,000 Python tasks over six public REST APIs and answered each of the 990 scored tasks twice, once with the plain model and once with the Confident Agent. The experiment was run under three quantizations of the same model (Q4_K_M, Q6_K and Q8_0): 2,970 task pairs that repeat the same 990 tasks, not three independent replications. An evaluator that shares no code with the agent executed every candidate in a sandbox against the answer key. In each run the share of tasks whose delivered code contained an API hallucination fell from **50.8–55.2% to 1.6–2.3%** (exact McNemar p < 10⁻¹²⁹, Holm-adjusted), while correct code reaching the user rose from **24.9–36.9% to 50.4–51.5%**. These figures measure the combined intervention of prompt, verification, one correction and abstention, not the contribution of each part; the agent\'s first candidates, written under its prompt but before verification, still hallucinated in 46.7–48.9% of tasks, against 50.8–55.2% for the baseline.' },
  { t: 'p', text: 'Release is governed by hard verification constraints, not by the confidence score: re-scoring every decision under the five planned weighting schemes changes only whether delivered code carries a flag, never what is withheld. Safety has costs: abstention on 38–40% of tasks, including almost every REST Countries task, and about **six times the time and energy** (37–48 s and R10.51–R14.87 of electricity per 1,000 prompts at the Durban Central tariff, against 6–7 s and R1.95–R2.42). Verification establishes conformance to the API contract, not that the code does what the user asked: only 19–23% of the agent\'s delivered programs met all three task-behaviour checks.' },
  { t: 'p', text: '**Keywords:** LLM hallucination, REST API, OpenAPI, static verification, confidence estimation, abstention, McNemar test, energy cost.' },
  { t: 'fronth', text: 'Table of Contents', pageBreak: true },
  { t: 'toc' },
  { t: 'fronth', text: 'List of Figures', pageBreak: true },
  { t: 'tof' },
  { t: 'fronth', text: 'List of Tables', pageBreak: true },
  { t: 'tot' },

  // ============================================================== MAIN
  { t: 'section', kind: 'main' },
  // -------------------------------------------------------------- 1
  { t: 'h1', text: '1 Introduction' },
  { t: 'h2', text: '1.1 Motivation' },
  { t: 'p', text: 'Developers now ask language models for integration code as routinely as they search documentation, and a large share of the answers call an API that is wrong in a way the developer cannot see: a renamed endpoint, a retired host, a parameter that never existed. The COMP301 brief frames the remedy as a design problem: *a Confident Agent is not one that is always correct; it is one that knows when it should not be trusted* (University of KwaZulu-Natal, 2026). We treat that statement as a testable claim. We hold the model fixed, add an explicit verification architecture around it, and measure with an independent judge whether fewer hallucinated API calls reach the user, how many correct answers are lost, and what the checking costs.' },
  { t: 'p', text: 'We chose software APIs, after abandoning an education setting in which web access made the intended traps trivial (The Skeptics, 2026a), because they offer an **authoritative, machine-readable specification** against which a claim can be checked without trusting the model (Vorster, 2026c). Progress Report Two fixed the design (The Skeptics, 2026b); Appendix E lists where this report supersedes it.' },
  { t: 'h2', text: '1.2 Contributions' },
  { t: 'bullets', items: [
    '**A frozen benchmark** of 1,000 Python tasks over six public REST APIs, with an executable answer key (Section 4).',
    '**The Confident Agent toolbox**: six-layer verification against frozen evidence, a confidence score and a decision policy with hard constraints (Section 6).',
    '**A paired experiment** on 990 tasks under three quantizations, judged by an independent sandboxed evaluator, with a pre-registered analysis plan and a cost analysis in Rand (Sections 7–9).',
    '**An architectural finding**: release decisions can be governed by explicit verification constraints rather than by the model\'s judgement or a confidence threshold (Sections 6.4 and 8.4).',
  ] },
  { t: 'p', text: 'Supporting details and analyses are in the appendices; Appendix A summarises the supplementary charts on one A3 page.' },

  // -------------------------------------------------------------- 2
  { t: 'h1', text: '2 Research Question and Hypotheses' },
  { t: 'note', text: '**Research question.** Can an LLM-based code-generation agent that verifies the REST API claims in its own code against frozen, authoritative specifications reduce the unacceptable API hallucinations that reach the user, compared with the same model without verification, while abstaining when verification is inconclusive, and at what cost?' },
  { t: 'p', text: '*Reaching the user* places the harm at delivery: a hallucinated candidate that the agent withholds is not a failure, but one that it delivers is. *Frozen, authoritative specifications* distinguishes the approach from self-verification by the same model, which can rationalise its own errors (Vorster, 2026a), and *abstaining* makes refusal a measured outcome rather than a hidden one.' },
  { t: 'note', text: '**H1 (primary).** Agent-based validation equipped with explicit, evidence-based confidence estimation significantly reduces the proportion of tasks in which code containing an API hallucination (class A, Section 3.1) reaches the user, compared with the equivalent baseline model. Test: exact two-sided McNemar test on paired tasks within each quantization run, α = 0.05, Holm-adjusted across the three runs.' },
  { t: 'bullets', items: [
    '**H2 (correctness is preserved).** The proportion of tasks in which correct code reaches the user does not decrease. A verifier that refused everything would fail H2.',
    '**H3 (the confidence metric discriminates).** Among final candidates, correct code receives a higher EWCS than hallucinated code (ROC area above 0.5). We do not claim the EWCS is a calibrated probability.',
    '**H4 (the cost is measurable).** Time, tokens and energy per prompt increase; we estimate the ratios and their price rather than test their direction.',
  ] },
  { t: 'p', text: 'We report **incorrect acceptance** (hallucinated code is delivered) and **incorrect rejection** (correct code is withheld) separately, and a reduction in hallucinations bought only through blanket refusal would count as a negative result.' },

  // -------------------------------------------------------------- 3
  { t: 'h1', text: '3 Application Domain and Definitions' },
  { t: 'h2', text: '3.1 Hallucination and API hallucination' },
  { t: 'p', text: 'A hallucination is generated content that is fluent and plausible but unfaithful to, or unsupported by, the source or the world (Ji et al., 2023; Huang et al., 2025); for code it includes invented packages (Spracklen et al., 2025), non-existent functions and wrong API usage (Liu et al., 2024; Patil et al., 2023). Our working definition is: **an LLM hallucination is content that appears plausible and confident but is incorrect, fabricated, or unsupported by verified ground truth.**' },
  { t: 'p', text: 'A claim about a **REST API** (Fielding, 2000) in code has six parts, which map onto our verification layers: the library imported, the identifier called, the access point (host, path and method), the input contract, the output contract, and the required context such as authentication. An **OpenAPI** document declares these parts in machine-readable form (OpenAPI Initiative, 2021), so a claim such as `GET https://api.github.com/orgs/{org}` can be checked deterministically without running the code. An **API hallucination** is a claim verified to be incorrect against such an authoritative source. *Cannot be verified* does not mean *false*: of the four states a claim can have (verified correct, verified incorrect, unverifiable, not applicable), only the second is a hallucination, and the third is a reason to abstain. The independent evaluator classifies delivered code as in {tab:classes} (taxonomy mapping in Appendix B.1).' },
  { t: 'table', key: 'classes', caption: 'Classes used to score the code that reaches the user (evaluation plan §2).', cols: [1.3, 4.4, 1.6],
    header: ['Class', 'Meaning and examples', 'Counts as'],
    rows: [
      ['**A** API hallucination', 'Breaks the API contract: wrong host, version or base path; undeclared path, method, parameter or field; missing required part or credential; wrong value type; undocumented response field.', 'Primary outcome'],
      ['**B** task-fidelity error', 'A valid API call that is not the one the task asked for (another endpoint, method, value or body).', 'Secondary outcome'],
      ['Correct (incl. **C** equivalent)', 'The expected request, allowing a closed list of equivalences (e.g. `token X` for `Bearer X`).', 'Correct'],
      ['Runtime failure', 'The code makes no request: syntax error, crash or no call.', 'Error'],
      ['Undetermined', 'A name a partial specification does not list; resolved by manual review.', 'Resolved'],
    ] },
  { t: 'h2', text: '3.2 Scope, and why external evidence is needed' },
  { t: 'p', text: 'We study **Python with `requests`** and **REST APIs with OpenAPI contracts**. Verification is **static**: the agent never executes generated code, because model output may be destructive, a verdict would depend on a live service on a particular day, and execution would need real credentials, which the benchmark must not contain (Vorster, 2026c). A model\'s knowledge is a snapshot that ends at a cut-off and over-represents what was common on the web (Cheng et al., 2024), while public APIs keep changing. The model therefore tends to write the API that was popular in its training data, with no internal signal that it is stale (Section 5). Only evidence from outside the model can detect this, which is why the agent is anchored to frozen, current specifications.' },

  // -------------------------------------------------------------- 4
  { t: 'h1', text: '4 Benchmark Design and Justification' },
  { t: 'h2', text: '4.1 Requirements and APIs' },
  { t: 'p', text: 'The brief asks for a representative, objective and reproducible benchmark; the lecturer added that ground truth must be frozen and hashed, credentials must be placeholders, and curated specifications must be labelled (Vorster, 2026c). The benchmark uses six public REST APIs spanning no authentication, API keys, Bearer tokens and OAuth2 ({tab:apis}). Each task carries an exact expected request, so correctness is decided by comparing requests; every specification is referenced by its SHA-256 hash; no task contains a real credential; and the dataset is generated by a deterministic script, not by a language model (Appendix B.2).' },
  { t: 'table', key: 'apis', caption: 'APIs in the benchmark and the provenance of their evidence (retrieved 21 September 2026).', cols: [1.5, 0.7, 0.8, 2.8, 0.6, 1.3],
    header: ['API', 'Tasks', 'Families', 'Ground-truth source', 'Tier', 'Authentication'],
    align: [null, 'r', 'r', null, 'c', null],
    rows: [
      ['GitHub REST', '250', '65', 'Official OpenAPI, full document (819 paths)', '1', 'Bearer token'],
      ['Swagger Petstore', '150', '11', 'Official OpenAPI 3 document', '1', 'API key / OAuth2'],
      ['Open-Meteo', '150', '3', 'Official OpenAPI (forecast, air quality, marine)', '1', 'None'],
      ['JSONPlaceholder', '150', '36', 'Curated partial specification from the official guide', '2', 'None'],
      ['DummyJSON', '150', '23', 'Curated partial specification from the documentation', '2', 'None'],
      ['REST Countries v5', '150', '4', 'Curated partial specification from the v5 documentation', '2', 'API key (Bearer)'],
    ],
    note: 'Tier 1 = provider-published specification; tier 2 = researcher-curated partial specification, labelled as such. Total: 1,000 tasks in 142 operation families.' },
  { t: 'p', text: 'For three APIs no adequate official OpenAPI document exists, so we built small specifications from the cited documentation and labelled them as researcher-authored. A name such a specification does not list is not proof that it does not exist, so the evaluator marks it undetermined for manual review (Section 7.3). REST Countries recently moved to an authenticated v5 interface on a new host; we kept it because it is exactly the case in which a model\'s training data is out of date.' },
  { t: 'h2', text: '4.2 Tasks and the answer key' },
  { t: 'p', text: 'The generator builds each task from a checked template for a documented operation; related variants share an **operation family** (141 among the scored tasks) so the analysis can allow for their correlation. Prompts name the API and describe the operation and its inputs, but never give the URL, method or parameter names, and never mention hallucination. Each asks for a function `solve(inputs)` and states how to handle an empty response and an error, which gives behaviour checks beyond API correctness (Appendix F). The 990 scored tasks are 494 reads, 232 creates, 197 updates, 37 searches and 30 deletes; their proportions differ from the targets of Progress Report Two, and we report subgroups rather than relabel tasks (Appendix B.3).' },
  { t: 'p', text: 'The task file is the answer key. Before any model output was scored, the evaluator\'s **self-check** executed all 1,000 reference solutions and classified every one correct. The planned two-reviewer human review of a stratified 100-task sample of the answer key was not completed (Section 10.1). Every task is answerable, so the benchmark measures the natural hallucination rate on ordinary requests but cannot reward a correct refusal. Ten pilot tasks used to develop the agent are excluded from every statistic.' },
];
