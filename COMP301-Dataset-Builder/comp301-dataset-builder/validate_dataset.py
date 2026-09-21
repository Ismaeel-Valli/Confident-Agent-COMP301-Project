"""Check task records against pinned specifications, without executing code.

The tiny AST reader supports our reference template only. It is not the
experimental verifier and must not be used to grade arbitrary LLM programs.
"""
import argparse
import ast
import copy
import hashlib
import json
import re
import warnings
from collections import Counter
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote

with warnings.catch_warnings():
    warnings.simplefilter('ignore', DeprecationWarning)
    from jsonschema import Draft4Validator, FormatChecker, RefResolver

ROOT = Path(__file__).resolve().parent
FIELDS = {'task_id': str, 'language': str, 'natural_language_instruction': str,
          'api_specification': dict, 'ground_truth': dict, 'test_case': dict, 'metadata': dict}


@lru_cache(maxsize=32)
def source(path):
    data = Path(path).read_bytes()
    return json.loads(data), hashlib.sha256(data).hexdigest()


def resolve(doc, value):
    seen = set()
    while isinstance(value, dict) and '$ref' in value:
        ref = value['$ref']
        if not ref.startswith('#/') or ref in seen:
            raise ValueError('Unsupported reference ' + ref)
        seen.add(ref)
        node = doc
        for part in ref[2:].split('/'):
            node = node[part.replace('~1', '/').replace('~0', '~')]
        value = {**node, **{k: v for k, v in value.items() if k != '$ref'}}
    return value


def schema_errors(doc, schema, value):
    validator = Draft4Validator(schema, resolver=RefResolver.from_schema(doc), format_checker=FormatChecker())
    return [f'{"/".join(map(str, e.path)) or "value"}: {e.message}' for e in validator.iter_errors(value)]


def wire(value, p):
    if isinstance(value, list):
        items = [str(x).lower() if isinstance(x, bool) else str(x) for x in value]
        return items if p.get('explode', True) else ','.join(items)
    return str(value).lower() if isinstance(value, bool) else str(value)


class TemplateReader:
    """Symbolically read an allowlisted syntax subset. No eval/exec/import."""
    def __init__(self, inputs):
        self.values = {'inputs': copy.deepcopy(inputs)}

    def expr(self, node):
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):
            return self.values[node.id]
        if isinstance(node, ast.Dict):
            return {self.expr(k): self.expr(v) for k, v in zip(node.keys, node.values)}
        if isinstance(node, (ast.List, ast.Tuple)):
            return [self.expr(x) for x in node.elts]
        if isinstance(node, ast.Subscript):
            return self.expr(node.value)[self.expr(node.slice)]
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            return self.expr(node.left) + self.expr(node.right)
        if isinstance(node, ast.GeneratorExp):
            if len(node.generators) != 1:
                raise ValueError('Unsupported generator')
            gen = node.generators[0]
            if gen.ifs or gen.is_async or not isinstance(gen.target, ast.Name):
                raise ValueError('Unsupported generator')
            out = []
            old = dict(self.values)
            for item in self.expr(gen.iter):
                self.values[gen.target.id] = item
                out.append(self.expr(node.elt))
            self.values = old
            return out
        if isinstance(node, ast.Call):
            args = [self.expr(x) for x in node.args]
            kwargs = {x.arg: self.expr(x.value) for x in node.keywords}
            if isinstance(node.func, ast.Name):
                if node.func.id == 'str' and len(args) == 1 and not kwargs:
                    return str(args[0])
                if node.func.id == 'quote':
                    return quote(*args, **kwargs)
            if isinstance(node.func, ast.Attribute):
                receiver = self.expr(node.func.value)
                if not isinstance(receiver, str):
                    raise ValueError('Only string methods are allowed here')
                if node.func.attr == 'replace':
                    return receiver.replace(*args, **kwargs)
                if node.func.attr == 'lower' and not args and not kwargs:
                    return receiver.lower()
                if node.func.attr == 'join':
                    return receiver.join(*args, **kwargs)
        raise ValueError('Unsupported template expression: ' + ast.dump(node)[:160])

    def request(self, code):
        tree = ast.parse(code)
        functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'solve']
        if len(functions) != 1:
            raise ValueError('Expected exactly one solve function')
        for statement in functions[0].body:
            if not isinstance(statement, ast.Assign) or len(statement.targets) != 1:
                raise ValueError('Unexpected statement before HTTP request')
            value = statement.value
            if isinstance(value, ast.Call) and isinstance(value.func, ast.Attribute) and isinstance(value.func.value, ast.Name) and value.func.value.id == 'requests' and value.func.attr == 'request':
                args = [self.expr(x) for x in value.args]
                kw = {x.arg: self.expr(x.value) for x in value.keywords}
                if len(args) != 2:
                    raise ValueError('Expected method and URL')
                return {'method': args[0], 'url': args[1], 'query': kw.get('params', {}),
                        'headers': kw.get('headers', {}), 'json_body': kw.get('json')}
            evaluated = self.expr(value)
            target = statement.targets[0]
            if isinstance(target, ast.Name):
                self.values[target.id] = evaluated
            elif isinstance(target, ast.Subscript):
                self.expr(target.value)[self.expr(target.slice)] = evaluated
            else:
                raise ValueError('Unsupported assignment target')
        raise ValueError('No HTTP request found')


def validate_record(record, root=ROOT):
    errors = []
    if not isinstance(record, dict):
        return ['Record must be an object']
    if set(record) != set(FIELDS):
        errors.append('Record must have exactly the seven top-level fields')
    for key, kind in FIELDS.items():
        if not isinstance(record.get(key), kind):
            errors.append('Missing or invalid field ' + key)
    if errors:
        return errors
    if record['language'] != 'python':
        errors.append('Language must be python')
    if not record['task_id'] or not record['natural_language_instruction'].strip():
        errors.append('Task ID and instruction must be nonempty')
    a = record['api_specification']; test = record['test_case']; m = record['metadata']
    try:
        path = (root / a['source_file']).resolve()
        if root.resolve() not in path.parents:
            return errors + ['Source path escapes the project']
        doc, sha = source(str(path))
        if sha != a['source_sha256']:
            errors.append('Source hash mismatch')
        item = doc['paths'][a['endpoint']]
        op = resolve(doc, item[a['method'].lower()])
        servers = op.get('servers') or item.get('servers') or doc.get('servers') or [{'url': 'https://api.github.com'}]
        valid_bases = [(('https://petstore3.swagger.io' + s['url']) if s['url'].startswith('/') else s['url']).rstrip('/') for s in servers]
        if a['base_url'] not in valid_bases:
            errors.append('Base URL is not supported by the pinned specification')
        raw_params = [resolve(doc, x) for x in item.get('parameters', []) + op.get('parameters', [])]
        params = {(p['in'], p['name']): p for p in raw_params}
        selected = m['scenario']['parameters']; fixed = m['scenario']['fixed']
        bindings = {(b['location'], b['parameter']): b['input_key'] for b in m['input_bindings']}
        required = {p['name'] for p in params.values() if p.get('required') or p['in'] == 'path'}
        if required - set(selected):
            errors.append('Missing required parameters: ' + repr(sorted(required - set(selected))))
        if set(selected) - {p['name'] for p in params.values()}:
            errors.append('Selected an undocumented parameter')
        documented = {(p['in'], p['name']) for p in a['parameters']}
        if documented != set(params):
            errors.append('Copied API parameters differ from source')
        for copied in a['parameters']:
            original = params.get((copied['in'], copied['name']))
            if original and (copied.get('schema') != original.get('schema') or copied.get('required', False) != original.get('required', False)):
                errors.append('Copied parameter rule differs from source: ' + copied['name'])
        expected_url = a['base_url'] + a['endpoint']
        expected_query, expected_headers = {}, {}
        for key, p in params.items():
            name = p['name']
            if name not in selected:
                continue
            value = fixed[name] if name in fixed else test['inputs'][bindings[key]]
            errors.extend('Parameter ' + name + ': ' + e for e in schema_errors(doc, p.get('schema', {}), value))
            if p['in'] == 'path':
                expected_url = expected_url.replace('{' + name + '}', quote(str(value), safe='/' if p.get('x-multi-segment') else ''))
            elif p['in'] == 'query':
                expected_query[name] = wire(value, p)
            else:
                expected_headers[name] = wire(value, p)
        req = test['expected_request']
        if req['method'] != a['method'] or req['url'] != expected_url:
            errors.append('Expected request method or URL differs from source contract and inputs')
        if req['query'] != expected_query:
            errors.append('Expected query differs from documented parameter mapping')
        body = resolve(doc, op.get('requestBody', {}))
        body_schema = body.get('content', {}).get('application/json', {}).get('schema')
        if (a.get('request_body') or {}).get('schema') != body_schema:
            errors.append('Copied request-body schema differs from source')
        if req['json_body'] is not None:
            if body_schema is None:
                errors.append('JSON body is not documented')
            else:
                errors.extend('Body: ' + e for e in schema_errors(doc, body_schema, req['json_body']))
                names = set(m['scenario']['body_fields'])
                if names != set(req['json_body']):
                    errors.append('Request body fields differ from task requirements')
                for n in names:
                    if req['json_body'][n] != test['inputs'][bindings[('body', n)]]:
                        errors.append('Body input mismatch for ' + n)
        elif body.get('required'):
            errors.append('Required body is missing')
        auth = a['auth']
        if auth:
            if req['headers'].get(auth['header']) != auth['prefix'] + test['inputs']['credential']:
                errors.append('Credential header mapping is incorrect')
        for k, v in expected_headers.items():
            if req['headers'].get(k) != v:
                errors.append('Required/documented header mismatch: ' + k)
        code = record['ground_truth']['code']
        derived = TemplateReader(test['inputs']).request(code)
        if derived != req:
            differences = [k for k in req if req[k] != derived.get(k)]
            errors.append('Reference code disagrees with expected request: ' + ', '.join(differences))
        tree = ast.parse(code)
        if not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'raise_for_status' for n in ast.walk(tree)):
            errors.append('Reference code lacks HTTP-error handling')
        projection = m['scenario']['projection']
        last = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'solve').body[-1]
        expected_return = 'response.status_code' if m['scenario']['output_mode'] == 'status' else f'data.get({projection!r})' if projection else 'data'
        if not isinstance(last, ast.Return) or ast.dump(last.value) != ast.dump(ast.parse(expected_return, mode='eval').body):
            errors.append('Reference return does not match requested output')
        # No answers, endpoint paths or transport method instructions in prompts.
        instruction = record['natural_language_instruction']
        if a['base_url'] in instruction or a['endpoint'] in instruction or re.search(r'\brequests\.(get|post|put|patch|delete|request|Session)\b', instruction):
            errors.append('Instruction leaks an endpoint or a library call')
    except Exception as exc:
        errors.append(type(exc).__name__ + ': ' + str(exc)[:600])
    return errors


def audit(records, root=ROOT):
    ids, fingerprints, prompts = set(), set(), set()
    failures = []
    for record in records:
        issues = validate_record(record, root)
        for key, seen in [('task_id', ids), ('natural_language_instruction', prompts)]:
            value = record[key]
            if value in seen:
                issues.append('Duplicate ' + key)
            seen.add(value)
        fp = record['metadata']['scenario_fingerprint']
        if fp in fingerprints:
            issues.append('Duplicate semantic scenario fingerprint')
        fingerprints.add(fp)
        if issues:
            failures.append({'task_id': record['task_id'], 'issues': issues})
    counts = Counter(r['metadata']['api_name'] for r in records)
    return {'status': 'automated_checks_passed' if not failures else 'failed',
            'task_count': len(records), 'api_counts': dict(counts),
            'http_methods': dict(Counter(r['api_specification']['method'] for r in records)),
            'categories': dict(Counter(r['metadata']['category'] for r in records)),
            'difficulty_heuristic': dict(Counter(r['metadata']['difficulty'] for r in records)),
            'authentication': dict(Counter((r['api_specification']['auth'] or {}).get('type', 'none') for r in records)),
            'operation_families': {api: len({r['metadata']['operation_family_id'] for r in records if r['metadata']['api_name'] == api}) for api in counts},
            'failure_count': len(failures), 'failures': failures,
            'human_review_status': 'pending', 'live_api_execution': False,
            'checks': ['seven-field structure', 'unique task IDs/prompts/scenarios', 'pinned source hashes',
                       'source endpoint/method existence', 'required parameters', 'input JSON schemas',
                       'query and path serialization', 'reference code request via a restricted AST reader',
                       'reference output mode', 'prompt endpoint/library-call leakage'],
            'limits': ['This validator only understands our reference template; it is not an independent experimental evaluator.',
                       'Source documentation can omit conditions; passing schema checks does not establish complete semantic correctness.',
                       'Correlated variants share operation families; 1,000 records are not 1,000 independent API operations.',
                       'Difficulty, operation mix and authentication proportions must be reviewed against Progress Report 2.',
                       'No live response content, credentials, resource existence, account permissions or LLM outputs were evaluated.']}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('dataset', nargs='?', default='output/rest_api_tasks_v1_DRAFT.jsonl')
    p.add_argument('--report', default='output/validation_report.json')
    p.add_argument('--prompts', help='Also check exact prompt-only export')
    args = p.parse_args()
    records = [json.loads(line) for line in (ROOT / args.dataset).read_text(encoding='utf-8').splitlines() if line.strip()]
    report = audit(records)
    if args.prompts:
        prompts = [json.loads(line) for line in (ROOT / args.prompts).read_text(encoding='utf-8').splitlines() if line.strip()]
        expected = [{k: r[k] for k in ['task_id', 'language', 'natural_language_instruction']} for r in records]
        report['prompt_export_matches'] = prompts == expected
        if prompts != expected:
            report['status'] = 'failed'; report['failure_count'] += 1
            report['failures'].append({'task_id': None, 'issues': ['Prompt export differs from master projection']})
    target = ROOT / args.report; target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ['status', 'task_count', 'api_counts', 'failure_count']}, indent=2))
    if report['failure_count']:
        print(json.dumps(report['failures'][:4], indent=2))
        raise SystemExit(1)


if __name__ == '__main__':
    main()
