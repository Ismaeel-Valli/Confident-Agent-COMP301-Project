"""Generate reproducible, source-grounded DRAFT tasks without an LLM or API calls.

Only documented features are varied; IDs and example values do not create new
scenarios. Every generated record remains pending independent human review.
"""
import argparse
import copy
import hashlib
import itertools
import json
import random
import re
from collections import Counter, defaultdict, deque
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
DATE = "2026-09-21"
TARGETS = {"JSONPlaceholder": 150, "GitHub": 250, "Open-Meteo": 150,
           "DummyJSON": 150, "REST Countries": 150, "Petstore": 150}
CODES = dict(zip(TARGETS, ["JP", "GH", "OM", "DJ", "RC", "PS"]))
FILES = {"JSONPlaceholder": ["jsonplaceholder.curated.openapi.json"],
         "GitHub": ["github.openapi.json"],
         "Open-Meteo": [f"openmeteo-{n}.openapi.json" for n in ["forecast", "air-quality", "marine"]],
         "DummyJSON": ["dummyjson.curated.openapi.json"],
         "REST Countries": ["restcountries.curated.openapi.json"],
         "Petstore": ["petstore.openapi.json"]}

# These operations use ordinary JSON/HTTP contracts. More complex GitHub
# operations are intentionally left out of this first generator.
GH_PATHS = {
    '/user', '/users/{username}', '/users/{username}/repos', '/user/repos',
    '/orgs/{org}', '/orgs/{org}/repos', '/repos/{owner}/{repo}',
    '/repos/{owner}/{repo}/issues', '/repos/{owner}/{repo}/issues/{issue_number}',
    '/repos/{owner}/{repo}/issues/{issue_number}/comments',
    '/repos/{owner}/{repo}/issues/comments/{comment_id}',
    '/repos/{owner}/{repo}/labels', '/repos/{owner}/{repo}/labels/{name}',
    '/repos/{owner}/{repo}/milestones', '/repos/{owner}/{repo}/milestones/{milestone_number}',
    '/repos/{owner}/{repo}/pulls', '/repos/{owner}/{repo}/pulls/{pull_number}',
    '/repos/{owner}/{repo}/pulls/{pull_number}/commits',
    '/repos/{owner}/{repo}/pulls/{pull_number}/files',
    '/repos/{owner}/{repo}/commits', '/repos/{owner}/{repo}/commits/{ref}',
    '/repos/{owner}/{repo}/contributors', '/repos/{owner}/{repo}/languages',
    '/repos/{owner}/{repo}/tags', '/repos/{owner}/{repo}/branches',
    '/repos/{owner}/{repo}/branches/{branch}',
    '/repos/{owner}/{repo}/releases', '/repos/{owner}/{repo}/releases/{release_id}',
    '/repos/{owner}/{repo}/releases/latest',
    '/repos/{owner}/{repo}/forks', '/repos/{owner}/{repo}/stargazers',
    '/users/{username}/followers', '/users/{username}/following',
    '/user/following/{username}', '/user/starred/{owner}/{repo}',
    '/users/{username}/starred', '/repos/{owner}/{repo}/subscribers',
}
GH_OPTIONAL_BODY = {
    'name', 'description', 'homepage', 'private', 'auto_init', 'has_issues', 'has_wiki',
    'has_projects', 'has_discussions', 'delete_branch_on_merge', 'title', 'body',
    'state', 'labels', 'assignees', 'color', 'new_name', 'due_on', 'draft',
    'prerelease', 'target_commitish', 'maintainer_can_modify', 'base', 'head',
    'tag_name', 'make_latest', 'generate_release_notes',
}
GH_QUERY = {'page', 'per_page', 'state', 'sort', 'direction', 'type', 'visibility',
            'affiliation', 'since', 'until', 'creator', 'assignee', 'labels', 'head',
            'base', 'sha', 'path', 'author', 'committer', 'anon'}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


@lru_cache(maxsize=32)
def source_digest(filename):
    return hashlib.sha256((ROOT / 'sources' / filename).read_bytes()).hexdigest()


def resolve(doc, node):
    result = copy.deepcopy(node)
    seen = set()
    while isinstance(result, dict) and '$ref' in result:
        ref = result['$ref']
        if not ref.startswith('#/') or ref in seen:
            raise ValueError('Unsupported or recursive direct reference: ' + ref)
        seen.add(ref)
        target = doc
        for part in ref[2:].split('/'):
            target = target[part.replace('~1', '/').replace('~0', '~')]
        result = {**copy.deepcopy(target), **{k: v for k, v in result.items() if k != '$ref'}}
    return result


def shape(doc, schema):
    s = resolve(doc, schema)
    if 'allOf' in s:
        props, required = dict(s.get('properties', {})), list(s.get('required', []))
        for child in s['allOf']:
            c = shape(doc, child)
            props.update(c.get('properties', {})); required.extend(c.get('required', []))
        s.update(type='object', properties=props, required=sorted(set(required)))
    return s


def example(doc, schema, name='', depth=0):
    if depth > 10:
        raise ValueError('Input schema is too deeply nested')
    s = shape(doc, schema)
    if s.get('enum'):
        return copy.deepcopy(next((x for x in s['enum'] if x is not None), s['enum'][0]))
    for key in ['example', 'default']:
        if key in s and s[key] is not None:
            return copy.deepcopy(s[key])
    for key in ['oneOf', 'anyOf']:
        if key in s:
            return example(doc, s[key][0], name, depth + 1)
    kind = s.get('type', 'object' if 'properties' in s else 'string')
    if kind == 'object':
        props = s.get('properties', {})
        names = list(s.get('required', []))
        if not names and props:
            names = [next(iter(props))]
        return {k: example(doc, props[k], k, depth + 1) for k in names if k in props}
    if kind == 'array':
        return [example(doc, s.get('items', {}), name, depth + 1) for _ in range(max(1, s.get('minItems', 0)))]
    if kind == 'boolean':
        return True
    if kind in ['integer', 'number']:
        value = max(1, s.get('minimum', 1))
        if 'maximum' in s:
            value = min(value, s['maximum'])
        return int(value) if kind == 'integer' else float(value)
    known = {'owner': 'example-owner', 'repo': 'example-repository', 'org': 'example-org',
             'username': 'example-user', 'head': 'feature-branch', 'base': 'main',
             'ref': 'main', 'branch': 'main', 'sha': 'a' * 40, 'color': 'a1b2c3',
             'tag_name': 'v1.0.0', 'email': 'researcher@example.test',
             'latitude': '-29.9', 'longitude': '31.2', 'timezone': 'auto',
             'due_on': '2026-10-01T00:00:00Z', 'website': 'https://example.test',
             'url': 'https://example.test/image.png', 'thumbnailUrl': 'https://example.test/thumb.png',
             'photoUrls': 'https://example.test/pet.png'}
    if s.get('format') == 'date-time':
        return '2026-09-21T00:00:00Z'
    if s.get('format') == 'date':
        return '2026-09-21'
    value = known.get(name, 'example-' + re.sub(r'[^a-zA-Z0-9-]', '-', name or 'value'))
    if len(value) < s.get('minLength', 0):
        value += 'x' * (s['minLength'] - len(value))
    if 'maxLength' in s:
        value = value[:s['maxLength']]
    return value


def subsets(required, optional, max_optional=4):
    for size in range(min(len(optional), max_optional) + 1):
        for choice in itertools.combinations(optional, size):
            yield list(required) + list(choice)


def operations(api):
    for filename in FILES[api]:
        doc = json.loads((ROOT / 'sources' / filename).read_text(encoding='utf-8'))
        for path, item in doc['paths'].items():
            if api == 'GitHub' and path not in GH_PATHS:
                continue
            for method, raw in item.items():
                if method not in ['get', 'post', 'put', 'patch', 'delete'] or raw.get('deprecated'):
                    continue
                if api == 'DummyJSON' and method == 'put':
                    continue  # PUT and PATCH have equivalent documented update behavior.
                # Session semantics and binary transfer need a separate adapter.
                if api == 'Petstore' and (path.startswith('/user') or 'uploadImage' in path):
                    continue
                op = resolve(doc, raw)
                server = (op.get('servers') or item.get('servers') or doc.get('servers') or [{'url': 'https://api.github.com'}])[0]['url']
                if server.startswith('/'):
                    server = 'https://petstore3.swagger.io' + server
                params = [resolve(doc, p) for p in item.get('parameters', []) + op.get('parameters', [])]
                merged = {(p['in'], p['name']): p for p in params}
                params = list(merged.values())
                if any(p['in'] not in ['path', 'query', 'header'] for p in params):
                    continue
                body = resolve(doc, op.get('requestBody', {}))
                body_schema = body.get('content', {}).get('application/json', {}).get('schema')
                if body.get('required') and body_schema is None:
                    continue
                if body_schema is not None and shape(doc, body_schema).get('type', 'object') != 'object':
                    continue
                success = next((str(k) for k in op['responses'] if str(k).startswith('2')), None)
                if success is None:
                    continue
                response = resolve(doc, op['responses'][success])
                response_schema = response.get('content', {}).get('application/json', {}).get('schema', {})
                yield {'api': api, 'file': filename, 'doc': doc, 'path': path, 'method': method.upper(),
                       'op': op, 'base': server.rstrip('/'), 'parameters': params,
                       'body_schema': body_schema, 'response_schema': response_schema,
                       'has_json_response': 'application/json' in response.get('content', {}),
                       'success_status': success, 'family': digest([api, filename, path, method])[:16]}


def aliases(name, location):
    special = {'id': 'resource_id', 'owner': 'repository_owner', 'repo': 'repository_name',
               'org': 'organization', 'per_page': 'page_size', 'limit': 'result_limit',
               'skip': 'results_to_skip', 'offset': 'results_to_skip', 'q': 'search_text',
               'response_fields': 'included_attributes', 'response_fields_omit': 'excluded_attributes',
               'select': 'included_fields', 'sortBy': 'sort_field', 'order': 'sort_direction',
               'photoUrls': 'photo_links', 'userId': 'user_identifier', 'postId': 'post_identifier',
               'petId': 'pet_identifier', 'orderId': 'order_identifier', 'user_id': 'user_identifier'}
    # Names describe function inputs without revealing path/query/body placement.
    return ('new_' if location == 'body' else '') + special.get(name, re.sub(r'[^a-zA-Z0-9_]', '_', name))


def auth_for(o):
    if o['api'] == 'GitHub':
        return {'type': 'bearer', 'header': 'Authorization', 'prefix': 'Bearer ',
                'required_by_api': None, 'required_by_task': True,
                'source': 'https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api',
                'note': 'Caller supplies an appropriate token; permissions/resource state are assumed. Auth requirement is not fully encoded by this OpenAPI document.'}
    security = o['op'].get('security', o['doc'].get('security', []))
    if not security:
        return None
    selected = next((s for s in security if 'api_key' in s), security[0])
    name = next(iter(selected))
    s = o['doc']['components']['securitySchemes'][name]
    if s['type'] == 'apiKey':
        if s['in'] != 'header':
            raise ValueError('This adapter only implements header API keys')
        return {'type': 'api_key', 'header': s['name'], 'prefix': '', 'required_by_api': True,
                'required_by_task': True, 'scheme_name': name, 'scopes': selected[name]}
    return {'type': 'oauth2' if s['type'] == 'oauth2' else 'api_key', 'header': 'Authorization',
            'prefix': 'Bearer ', 'required_by_api': True, 'required_by_task': True,
            'scheme_name': name, 'scopes': selected[name],
            'note': 'A valid credential is supplied by the caller; this task does not obtain or verify credentials.'}


def preset_options(o):
    if o['api'] == 'Open-Meteo':
        # Specific requested measurements are semantic choices, not swapped IDs.
        names = {
            '/v1/forecast': ['temperature_2m', 'relative_humidity_2m', 'precipitation', 'wind_speed_10m', 'cloud_cover'],
            '/v1/air-quality': ['pm10', 'pm2_5', 'carbon_monoxide', 'nitrogen_dioxide', 'ozone'],
            '/v1/marine': ['wave_height', 'wave_direction', 'wave_period', 'wind_wave_height', 'swell_wave_height'],
        }[o['path']]
        measures = [[x] for x in names] + [list(x) for x in itertools.combinations(names, 2)]
        for metrics in measures:
            for extras in [{}, {'timezone': 'auto'}, {'forecast_days': 3}, {'timezone': 'auto', 'forecast_days': 3}]:
                yield {'hourly': metrics, **extras}
    elif o['api'] == 'REST Countries' and '{property}' in o['path']:
        for p in next(p for p in o['parameters'] if p['name'] == 'property')['schema']['enum']:
            yield {'property': p}
    else:
        yield {}


def scenarios(o):
    params = o['parameters']
    mandatory = [p['name'] for p in params if p.get('required')]
    optional = [p['name'] for p in params if not p.get('required') and p['in'] == 'query']
    if o['api'] == 'GitHub':
        optional = [n for n in optional if n in GH_QUERY]
    if o['api'] == 'Open-Meteo':
        optional = []
    b = shape(o['doc'], o['body_schema']) if o['body_schema'] is not None else {}
    props = b.get('properties', {})
    required_fields = list(dict.fromkeys(b.get('required', []) + o['op'].get('x-task-core-fields', [])))
    # Documented business intent can need more fields than the JSON schema.
    if o['api'] == 'GitHub' and o['path'].endswith('/pulls') and o['method'] == 'POST':
        required_fields = list(dict.fromkeys(required_fields + ['title', 'head', 'base']))
    if o['api'] == 'Petstore' and o['path'] == '/store/order' and o['method'] == 'POST':
        required_fields = list(dict.fromkeys(required_fields + ['petId', 'quantity']))
    if o['api'] == 'Petstore' and o['path'] == '/pet' and o['method'] == 'PUT':
        required_fields = list(dict.fromkeys(required_fields + ['id']))
    optional_fields = [k for k, v in props.items() if k not in required_fields and not resolve(o['doc'], v).get('readOnly')]
    if o['api'] == 'GitHub':
        optional_fields = [k for k in optional_fields if k in GH_OPTIONAL_BODY]
    response = shape(o['doc'], o['response_schema'])
    projections = [None]
    # Response variants are explicitly recorded as the same operation family.
    if o['api'] in ['Petstore', 'JSONPlaceholder', 'DummyJSON'] and response.get('type') == 'object':
        projections += [k for k in ['id', 'name', 'title', 'status', 'isDeleted'] if k in response.get('properties', {})]
    for fixed in preset_options(o):
        for chosen in subsets(mandatory, optional, 3):
            chosen = list(dict.fromkeys(chosen + list(fixed)))
            if o['api'] == 'Petstore' and o['path'] == '/pet/{petId}' and o['method'] == 'POST' and not {'name', 'status'}.intersection(chosen):
                continue
            if 'order' in chosen and 'sortBy' not in chosen:
                continue
            if 'direction' in chosen and 'sort' not in chosen:
                continue
            if o['api'] == 'REST Countries' and 'response_fields' in chosen and 'response_fields_omit' in chosen:
                continue
            if o['api'] == 'REST Countries' and '{value}' in o['path'] and 'q' in chosen:
                continue  # avoid unintentionally contradictory synthetic filters
            for fields in subsets(required_fields, optional_fields, 4):
                if o['body_schema'] is not None and not fields:
                    continue
                for projection in projections:
                    yield {'parameters': sorted(chosen), 'body_fields': sorted(fields),
                           'fixed': fixed, 'projection': projection,
                           'output_mode': 'json' if o['has_json_response'] else 'status'}


def serialize_value(value, p):
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, list):
        if p.get('explode', True):
            return [str(x).lower() if isinstance(x, bool) else str(x) for x in value]
        return ','.join(str(x).lower() if isinstance(x, bool) else str(x) for x in value)
    return str(value)


def code_for(o, scenario, bindings, auth):
    lines = ['import requests', 'from urllib.parse import quote', '', '', 'def solve(inputs):',
             f'    url = {o["base"] + o["path"]!r}', '    params = {}', '    headers = {}']
    if o['api'] == 'GitHub':
        lines.append("    headers['Accept'] = 'application/vnd.github+json'")
        lines.append("    headers['X-GitHub-Api-Version'] = '2026-03-10'")
    else:
        lines.append("    headers['Accept'] = 'application/json'")
    if auth:
        lines.append(f'    headers[{auth["header"]!r}] = {auth["prefix"]!r} + inputs["credential"]')
    for p in o['parameters']:
        n = p['name']
        if n not in scenario['parameters']:
            continue
        expr = repr(scenario['fixed'][n]) if n in scenario['fixed'] else f'inputs[{bindings[(p["in"], n)]!r}]'
        s = shape(o['doc'], p.get('schema', {}))
        if p['in'] == 'path':
            # GitHub explicitly marks some slash-containing path values.
            safe = '/' if p.get('x-multi-segment') else ''
            lines.append(f'    url = url.replace({"{" + n + "}"!r}, quote(str({expr}), safe={safe!r}))')
        else:
            if s.get('type') == 'array' and not p.get('explode', True):
                expr = f'",".join(str(value) for value in {expr})'
            elif s.get('type') == 'boolean':
                expr = f'str({expr}).lower()'
            elif s.get('type') != 'array':
                expr = f'str({expr})'
            lines.append(f'    {"params" if p["in"] == "query" else "headers"}[{n!r}] = {expr}')
    if o['body_schema'] is not None:
        fields = ', '.join(f'{n!r}: inputs[{bindings[("body", n)]!r}]' for n in scenario['body_fields'])
        lines.append('    payload = {' + fields + '}')
        body_arg = ', json=payload'
    else:
        body_arg = ''
    lines += [f'    response = requests.request({o["method"]!r}, url, params=params, headers=headers{body_arg}, timeout=20)',
              '    response.raise_for_status()']
    if scenario['output_mode'] == 'status':
        return '\n'.join(lines + ['    return response.status_code']) + '\n'
    lines += [
              '    if response.status_code == 204 or not response.content:', '        return None',
              '    data = response.json()']
    lines.append(f'    return data.get({scenario["projection"]!r})' if scenario['projection'] else '    return data')
    return '\n'.join(lines) + '\n'


def task_for(o, scenario):
    doc = o['doc']; inputs = {}; bindings = {}; requirements = []; request = {'method': o['method'], 'url': o['base'] + o['path'], 'query': {}, 'headers': {}, 'json_body': None}
    source_hash = source_digest(o['file'])
    auth = auth_for(o)
    request['headers']['Accept'] = 'application/vnd.github+json' if o['api'] == 'GitHub' else 'application/json'
    if o['api'] == 'GitHub':
        request['headers']['X-GitHub-Api-Version'] = '2026-03-10'
    if auth:
        inputs['credential'] = 'EXAMPLE_CREDENTIAL_NOT_REAL'
        request['headers'][auth['header']] = auth['prefix'] + inputs['credential']
    for p in o['parameters']:
        name = p['name']
        if name not in scenario['parameters']:
            continue
        value = scenario['fixed'].get(name) if name in scenario['fixed'] else example(doc, p.get('schema', {}), name)
        if o['api'] == 'REST Countries' and name == 'value':
            value = {'codes.alpha_2': 'CA', 'codes.alpha_3': 'CAN', 'names.common': 'Canada', 'region': 'Europe',
                     'subregion': 'Northern Europe', 'borders': 'CAN', 'currencies': 'CAD', 'calling_codes': '44',
                     'capitals': 'Tokyo', 'landlocked': 'true', 'memberships.eu': 'true'}[scenario['fixed']['property']]
        alias = aliases(name, p['in']); bindings[(p['in'], name)] = alias
        if name not in scenario['fixed']:
            inputs[alias] = value
            meaning = p.get('description', name).split('\n')[0]
            # Long official prose stays in the source file, not the user prompt.
            meaning = re.sub(r'[`*]', '', meaning)
            meaning = re.sub(r'\[([^]]+)\]\([^)]*\)', r'\1', meaning)
            meaning = meaning.split('. ')[0][:180]
            requirements.append(f'{alias}: {meaning or name}')
        if p['in'] == 'path':
            request['url'] = request['url'].replace('{' + name + '}', quote(str(value), safe='/' if p.get('x-multi-segment') else ''))
        else:
            request['query' if p['in'] == 'query' else 'headers'][name] = serialize_value(value, p)
    if o['body_schema'] is not None:
        props = shape(doc, o['body_schema']).get('properties', {})
        request['json_body'] = {}
        for name in scenario['body_fields']:
            alias = aliases(name, 'body'); bindings[('body', name)] = alias
            inputs[alias] = example(doc, props[name], name)
            request['json_body'][name] = inputs[alias]
            field_label = re.sub(r'([a-z])([A-Z])', r'\1 \2', name).replace('_', ' ')
            requirements.append(f'{alias}: value for the {field_label} attribute')
    summary = o['op'].get('summary', 'Perform the documented operation').rstrip('.')
    if o['api'] == 'Open-Meteo':
        pretty = {'pm2_5': 'fine particulate matter (PM2.5)', 'pm10': 'particulate matter (PM10)',
                  'temperature_2m': 'temperature at two metres', 'relative_humidity_2m': 'relative humidity at two metres',
                  'wind_speed_10m': 'wind speed at ten metres'}
        measures = ', '.join(pretty.get(x, x.replace('_', ' ')) for x in scenario['fixed']['hourly'])
        summary = f'Retrieve hourly {measures} from the {"weather forecast" if "forecast" in o["path"] else "air quality forecast" if "air-quality" in o["path"] else "marine forecast"} service'
        if 'timezone' in scenario['fixed']:
            summary += ', using the location\'s automatically determined time zone'
        if 'forecast_days' in scenario['fixed']:
            summary += ', covering three forecast days'
    if o['api'] == 'REST Countries' and 'property' in scenario['fixed']:
        labels = {'codes.alpha_2': 'two-letter ISO country code', 'codes.alpha_3': 'three-letter ISO country code',
                  'names.common': 'common country name', 'region': 'region', 'subregion': 'subregion',
                  'borders': 'bordering country code', 'currencies': 'currency code', 'calling_codes': 'calling code',
                  'capitals': 'capital city', 'landlocked': 'landlocked status', 'memberships.eu': 'EU membership status'}
        summary = 'Look up countries by an exact match on their ' + labels[scenario['fixed']['property']]
    api_name = {'REST Countries': 'REST Countries v5', 'Petstore': 'Swagger Petstore (OpenAPI 3 service)',
                'GitHub': 'GitHub REST API version 2026-03-10', 'Open-Meteo': 'Open-Meteo public API'}.get(o['api'], o['api'])
    prompt = f'Write a Python function solve(inputs) for {api_name}. {summary}. '
    if requirements:
        prompt += 'The inputs dictionary provides: ' + '; '.join(requirements) + '. '
    if auth:
        prompt += 'Use the caller-supplied credential in inputs["credential"], assumed to have the necessary permissions. '
    if scenario['output_mode'] == 'status':
        prompt += 'Return the successful HTTP status code. '
    elif scenario['projection']:
        prompt += f'Return only the response\'s {scenario["projection"]} value, or None if that attribute is absent. '
    else:
        prompt += 'Return the decoded JSON response. '
    if scenario['output_mode'] == 'json':
        prompt += 'Return None for a successful empty response. '
    prompt += 'Raise an exception for an unsuccessful HTTP response. Assume referenced resources and accounts exist. Do not execute the function.'
    signature = [o['api'], o['file'], o['path'], o['method'], scenario]
    count = len(scenario['parameters']) + len(scenario['body_fields'])
    difficulty = 'easy' if count <= 2 and not auth else 'hard' if count >= 7 else 'medium'
    source_docs = o['op'].get('x-source-docs') or o['op'].get('externalDocs', {}).get('url') or o['doc'].get('x-source-docs')
    if not source_docs:
        source_docs = {'Petstore': 'https://petstore3.swagger.io/', 'Open-Meteo': 'https://open-meteo.com/en/docs'}[o['api']]
    code = code_for(o, scenario, bindings, auth)
    params = [{**copy.deepcopy(p), 'type': shape(doc, p.get('schema', {})).get('type')} for p in o['parameters']]
    return {
        'task_id': '', 'language': 'python', 'natural_language_instruction': prompt,
        'api_specification': {'api_name': o['api'], 'base_url': o['base'], 'endpoint': o['path'], 'method': o['method'],
            'acceptable_methods': ['PUT', 'PATCH'] if o['api'] == 'DummyJSON' and o['method'] == 'PATCH' else [o['method']],
            'parameters': params, 'headers': [{'name': k, 'value': v} for k, v in request['headers'].items() if k != (auth or {}).get('header')],
            'request_body': {'content_type': 'application/json', 'schema': o['body_schema']} if o['body_schema'] is not None else None,
            'response_schema': o['response_schema'], 'auth': auth,
            'source_file': 'sources/' + o['file'], 'source_sha256': source_hash,
            'source_pointer': '/paths/' + o['path'].replace('~', '~0').replace('/', '~1') + '/' + o['method'].lower(),
            'openapi_url': None if 'curated' in o['file'] else next((m['url'] for m in json.loads((ROOT/'sources/manifest.json').read_text()) if m['file'] == o['file'] or m['file'] == o['file'].replace('.openapi.json', '.yml')), None),
            'coverage': o['doc'].get('x-coverage', 'Provider specification; coverage limitations and non-schema conditions still apply.')},
        'ground_truth': {'code': code, 'expected_behavior': summary,
            'verified_by': 'deterministic_source_template; automated_checks_pending', 'verification_date': DATE,
            'review_status': 'pending_human_review'},
        'test_case': {'inputs': inputs, 'expected_request': request,
            'expected_output': {'kind': 'http_status_code' if scenario['output_mode'] == 'status' else 'optional_response_field' if scenario['projection'] else 'decoded_json_or_none',
                'field': scenario['projection'], 'empty_response': 'return_status_code' if scenario['output_mode'] == 'status' else None,
                'response_schema_source': 'api_specification.response_schema'},
            'evaluation_mode': 'static_contract', 'fixture_origin': 'synthetic_inputs_no_live_resource_claims'},
        'metadata': {'api_name': o['api'], 'category': 'create' if o['method'] == 'POST' else 'update' if o['method'] in ['PUT', 'PATCH'] else 'delete' if o['method'] == 'DELETE' else 'search_filter' if 'search' in summary.lower() or 'q' in scenario['parameters'] else 'read',
            'difficulty': difficulty, 'difficulty_status': 'heuristic_pending_review',
            'source_openapi': 'sources/' + o['file'], 'source_docs': source_docs,
            'created_date': DATE, 'reviewed_by': None, 'review_status': 'pending_human_review',
            'tags': ['rest', 'python', o['method'].lower()], 'generation_method': 'source_driven_templates',
            'operation_family_id': o['family'], 'scenario_fingerprint': digest(signature),
            'scenario': scenario, 'input_bindings': [{'location': loc, 'parameter': name, 'input_key': alias} for (loc, name), alias in bindings.items()],
            'source_kind': 'documentation_derived' if 'curated' in o['file'] else 'provider_openapi',
            'split': 'unassigned_draft',
            'assumptions': ['Valid existing resources and appropriate account permissions are supplied.',
                            'Credentials are caller inputs; credential validity cannot be checked statically.',
                            'Missing entries in partial specifications are not proof of a hallucination.']}}


def generate(counts):
    from validate_dataset import validate_record
    records, rejected = [], []
    for api, wanted in counts.items():
        # Round robin across operations prevents one large body schema dominating.
        queues = deque((o, iter(scenarios(o))) for o in operations(api))
        selected, seen = [], set()
        while queues and len(selected) < wanted:
            o, candidates = queues.popleft()
            try:
                scenario = next(candidates)
            except StopIteration:
                continue
            queues.append((o, candidates))
            try:
                record = task_for(o, scenario)
                record['task_id'] = f'REST_PY_{CODES[api]}_{len(selected)+1:04d}'
                issues = validate_record(record, ROOT)
                if issues:
                    raise ValueError('; '.join(issues[:3]))
                if record['metadata']['scenario_fingerprint'] in seen:
                    continue
                seen.add(record['metadata']['scenario_fingerprint'])
                record['ground_truth']['verified_by'] = 'source_contract_checks_and_static_reference_request_check; human_review_pending'
                selected.append(record)
            except (ValueError, KeyError, TypeError, StopIteration) as exc:
                rejected.append({'api': api, 'operation': o['method'] + ' ' + o['path'], 'scenario': scenario, 'reason': str(exc)[:1000]})
        if len(selected) != wanted:
            raise RuntimeError(f'{api}: only {len(selected)} acceptable scenarios for target {wanted}; do not pad with duplicates. Rejections: {rejected[-3:]}')
        records.extend(selected)
        print(f'{api}: {len(selected)} records across {len(set(t["metadata"]["operation_family_id"] for t in selected))} operation families')
    return records, rejected


def write_jsonl(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in records), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pilot', action='store_true', help='Generate a 10-task check batch, two tasks from four APIs and one from two.')
    parser.add_argument('--output', default='output', help='Destination directory, relative to this project.')
    args = parser.parse_args()
    counts = {'JSONPlaceholder': 2, 'GitHub': 2, 'Open-Meteo': 2, 'DummyJSON': 2, 'REST Countries': 1, 'Petstore': 1} if args.pilot else TARGETS
    records, rejected = generate(counts)
    out = ROOT / args.output
    master_name = 'rest_api_tasks_pilot.jsonl' if args.pilot else 'rest_api_tasks_v1_DRAFT.jsonl'
    prompt_name = 'rest_api_prompts_pilot.jsonl' if args.pilot else 'rest_api_prompts_v1_DRAFT.jsonl'
    write_jsonl(out / master_name, records)
    write_jsonl(out / prompt_name, [{k: r[k] for k in ['task_id', 'language', 'natural_language_instruction']} for r in records])
    (out / ('pilot_rejections.json' if args.pilot else 'generation_rejections.json')).write_text(json.dumps(rejected, indent=2) + '\n')
    print(f'Wrote {len(records)} DRAFT tasks to {out}. All remain pending human review.')


if __name__ == '__main__':
    main()
