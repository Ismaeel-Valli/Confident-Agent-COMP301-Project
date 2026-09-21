"""Create a reproducible 10% review queue and a plain-language coverage report."""
import csv
import hashlib
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

from build_dataset import TARGETS

ROOT = Path(__file__).resolve().parent


def main():
    existing = ROOT / 'review/review_100.csv'
    if existing.exists():
        with existing.open(encoding='utf-8-sig', newline='') as f:
            previous = list(csv.DictReader(f))
        if any(r.get('decision', 'PENDING') != 'PENDING' or r.get('reviewer') or r.get('notes') for r in previous):
            raise SystemExit('Existing review annotations found. Back up or move review/review_100.csv before generating a new queue.')
    records = [json.loads(s) for s in (ROOT / 'output/rest_api_tasks_v1_DRAFT.jsonl').read_text(encoding='utf-8').splitlines()]
    audit = json.loads((ROOT / 'output/validation_report.json').read_text())
    rng = random.Random(301)
    review = []
    for api, count in TARGETS.items():
        candidates = [r for r in records if r['metadata']['api_name'] == api]
        review.extend(rng.sample(candidates, count // 10))
    folder = ROOT / 'review'; folder.mkdir(exist_ok=True)
    (folder / 'review_100.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in review), encoding='utf-8')
    fields = ['task_id', 'scenario_fingerprint', 'api', 'method', 'endpoint', 'source_docs', 'instruction',
              'source_contract_correct', 'prompt_unambiguous', 'reference_code_correct',
              'test_case_correct', 'alternative_valid_calls_considered', 'difficulty_label_checked',
              'decision', 'reviewer', 'review_date', 'notes']
    with (folder / 'review_100.csv').open('w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for r in review:
            w.writerow({'task_id': r['task_id'], 'scenario_fingerprint': r['metadata']['scenario_fingerprint'], 'api': r['metadata']['api_name'],
                        'method': r['api_specification']['method'], 'endpoint': r['api_specification']['endpoint'],
                        'source_docs': r['metadata']['source_docs'], 'instruction': r['natural_language_instruction'],
                        'decision': 'PENDING'})
    # Source groups, rather than row-level random splits, prevent related variants
    # from appearing in both development and final evaluation data.
    family_counts = Counter(r['metadata']['operation_family_id'] for r in records)
    with (folder / 'operation_families.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['family_id', 'api', 'method', 'endpoint', 'task_count'])
        seen = set()
        for r in records:
            family = r['metadata']['operation_family_id']
            if family not in seen:
                seen.add(family); w.writerow([family, r['metadata']['api_name'], r['api_specification']['method'], r['api_specification']['endpoint'], family_counts[family]])
    methods = audit['http_methods']; difficulties = audit['difficulty_heuristic']
    comparisons = [('GET total (list/single/search)', 600, methods.get('GET', 0)),
                   ('POST', 150, methods.get('POST', 0)),
                   ('PUT/PATCH', 150, methods.get('PUT', 0) + methods.get('PATCH', 0)),
                   ('DELETE', 100, methods.get('DELETE', 0)),
                   ('Easy (heuristic)', 400, difficulties.get('easy', 0)),
                   ('Medium (heuristic)', 400, difficulties.get('medium', 0)),
                   ('Hard (heuristic)', 200, difficulties.get('hard', 0))]
    auth = audit['authentication']
    comparisons += [('No credential', 550, auth.get('none', 0)), ('API key', 150, auth.get('api_key', 0)),
                    ('Bearer token', 200, auth.get('bearer', 0)), ('OAuth2 token', 100, auth.get('oauth2', 0))]
    report = ['# Dataset audit', '', '**Status: DRAFT. Automated integrity checks pass; human review and report-distribution alignment remain open.**', '',
              '## Actual API composition', '', '| API | Target | Generated | Operation families |', '|---|---:|---:|---:|']
    for api, target in TARGETS.items():
        report.append(f'| {api} | {target} | {audit["api_counts"][api]} | {audit["operation_families"][api]} |')
    report += ['', 'The 1,000 tasks include related variants of the same operations. Changing only an ID or rewording a prompt does not create a new generated scenario. Some scenarios vary only the requested response field; those remain in the same operation family.', '',
               '## Differences from Progress Report 2', '', '| Measure | Report target (approx.) | Actual draft |', '|---|---:|---:|']
    for label, target, actual in comparisons:
        report.append(f'| {label} | {target} | {actual} |')
    report += ['', 'The generator guarantees the six API totals. It does not claim to satisfy the proposed operation, difficulty or authentication balance. GET list/single/search subcategories also need a reviewed classification. Do not relabel tasks just to hit a percentage. Add/select genuinely appropriate operations and scenarios, or document an agreed revision to the report.', '',
        'Difficulty currently uses an explicit heuristic: easy has at most two selected parameters/body fields and no credential; hard has at least seven; remaining tasks are medium. This is not a measured difficulty estimate. OAuth2 here means use of an already-issued token; there is no OAuth login flow.', '',
        '## Source and correctness limits', '',
        '- GitHub, Petstore and Open-Meteo use downloaded provider OpenAPI descriptions. JSONPlaceholder, DummyJSON and REST Countries use clearly marked documentation-derived partial specifications.',
        '- Review the three curated specifications before treating them as answer keys. Example fields do not establish mandatory fields, exhaustive parameter lists or all valid alternatives. Some mutable-field choices are proposals requiring source review.',
        '- REST Countries targets the current documented v5 interface. Petstore targets the OpenAPI 3 service. Do not mix historical API versions into their grading rules.',
        '- A reference request is one valid implementation candidate. Do not require exact Python text or reject an alternative documented route/method that satisfies the task. DummyJSON updates record PUT and PATCH as acceptable alternatives.',
        '- A missing entry in a partial source is insufficient evidence for VERIFIED_INCORRECT. Preserve UNVERIFIABLE where the evidence is incomplete.',
        '- The fixtures describe inputs and expected HTTP requests. Expected outputs describe decoded JSON/optional fields/empty responses; these are not live API payloads. No credentials, endpoint calls from generated code, account state or service responses were evaluated.',
        '- The template AST checker is an authoring integrity tool. It cannot grade arbitrary LLM code. Build the experimental evaluator independently and audit its labels against original sources.', '',
        '## Before the final experiment', '',
        '1. Review source curation and all distinct operation families, including prose-only conditions and response fields.',
        '2. Complete the supplied 100-task stratified random review; expand review if systematic errors appear. The CSV is an empty review queue, not a claim of completed review.',
        '3. Resolve the distribution differences above and freeze the dataset, sources, settings and approved labels.',
        '4. Keep development/pilot examples and their related operation families out of a held-out final test. The included pilot deliberately overlaps this draft; it is for development only. The draft has no final train/test split.',
        '5. Generate each initial model answer once and reuse it for the paired baseline/intervention comparison. Give the model the prompt-only record; keep task-specific reference answers out of its context.',
        '6. Report operation-family correlation and consider grouped analysis rather than treating every related variant as independent evidence.', '']
    (ROOT / 'DATASET_AUDIT.md').write_text('\n'.join(report), encoding='utf-8')
    gate = {'release_ready': False, 'task_count': len(records), 'api_count_targets_met': dict(Counter(r['metadata']['api_name'] for r in records)) == TARGETS,
            'automated_integrity_checks_passed': audit['status'] == 'automated_checks_passed',
            'human_review_completed': False, 'review_queue_size': len(review),
            'operation_distribution_matches_report': False, 'difficulty_distribution_matches_report': False,
            'issues': ['Independent source and reference review pending', 'Operation/difficulty/authentication distributions differ from the report',
                       'Pilot overlap must be removed from a held-out final evaluation set', 'Independent experimental evaluator not implemented']}
    (ROOT / 'output/release_status.json').write_text(json.dumps(gate, indent=2) + '\n')
    print('Created a 100-task review queue, operation-family index and dataset audit.')


if __name__ == '__main__':
    main()
