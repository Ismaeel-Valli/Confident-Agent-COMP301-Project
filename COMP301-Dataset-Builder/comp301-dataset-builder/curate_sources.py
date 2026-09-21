"""Build explicitly partial OpenAPI contracts from the documented examples.

These three specifications are researcher-authored. Source URLs and coverage
limits are embedded; absence from these subsets is not evidence of invalidity.
"""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / "sources"


def scalar(kind, description="", example=None):
    result = {"type": kind}
    if description:
        result["description"] = description
    if example is not None:
        result["example"] = example
    return result


def obj(properties):
    return {"type": "object", "properties": properties}


def param(name, location, kind, description, example=None, required=False, **schema):
    return {"name": name, "in": location, "required": required or location == "path",
            "description": description, "schema": {**scalar(kind, example=example), **schema}}


def document(name, base, url):
    return {"openapi": "3.0.3", "info": {"title": name + " - curated subset",
            "version": "draft-2026-09-21", "description": "Researcher-authored, documentation-derived subset; independent human review pending."},
            "servers": [{"url": base}], "paths": {},
            "x-source-docs": url, "x-source-kind": "documentation_derived",
            "x-coverage": "Partial. Unlisted operations/fields are not automatically invalid. Example fields are not asserted to be universally required."}


def operation(doc, path, method, summary, parameters=(), body=None, response=None,
              core=(), allowed=None, source=None):
    op = {"summary": summary, "operationId": method + '_' + path.strip('/').replace('/', '_'),
          "parameters": list(copy.deepcopy(parameters)), "security": [],
          "responses": {"2XX": {"description": "Successful JSON response; exact status may vary by operation.",
                        "content": {"application/json": {"schema": response or {}}}}},
          "x-task-core-fields": list(core), "x-source-docs": source or doc["x-source-docs"]}
    if body is not None:
        op["requestBody"] = {"content": {"application/json": {"schema": body}}}
    if allowed is not None:
        op["x-task-allowed-query"] = allowed
    doc["paths"].setdefault(path, {})[method] = op
    return op


def jsonplaceholder():
    d = document("JSONPlaceholder", "https://jsonplaceholder.typicode.com", "https://jsonplaceholder.typicode.com/guide/")
    resources = {
        "posts": {"title": scalar("string"), "body": scalar("string"), "userId": scalar("integer")},
        "comments": {"name": scalar("string"), "email": scalar("string"), "body": scalar("string"), "postId": scalar("integer")},
        "albums": {"title": scalar("string"), "userId": scalar("integer")},
        "photos": {"title": scalar("string"), "url": scalar("string"), "thumbnailUrl": scalar("string"), "albumId": scalar("integer")},
        "todos": {"title": scalar("string"), "completed": scalar("boolean"), "userId": scalar("integer")},
        "users": {"name": scalar("string"), "username": scalar("string"), "email": scalar("string"), "phone": scalar("string"), "website": scalar("string")},
    }
    for name, fields in resources.items():
        singular = name[:-1] if name != "people" else "person"
        response = obj({"id": scalar("integer"), **fields})
        path = '/' + name
        ids = [param("id", "path", "integer", f"Identifier of the {singular}", 1)]
        filters = [param(n, "query", s["type"], f"Filter by {n}", 1)
                   for n, s in fields.items() if n.endswith("Id")]
        operation(d, path, "get", f"Retrieve the {name}", filters,
                  response={"type": "array", "items": response})
        operation(d, path + '/{id}', "get", f"Retrieve a {singular} by identifier", ids, response=response)
        operation(d, path, "post", f"Submit a new {singular}", body=obj(fields), response=response,
                  core=list(fields)[:1])
        operation(d, path + '/{id}', "put", f"Replace a {singular} record with the supplied data", ids,
                  body=obj(fields), response=response, core=list(fields))
        operation(d, path + '/{id}', "patch", f"Change selected fields of a {singular}", ids,
                  body=obj(fields), response=response)
        operation(d, path + '/{id}', "delete", f"Delete a {singular} by identifier", ids, response={"type": "object"})
    d["x-source-evidence"] = ["https://jsonplaceholder.typicode.com/guide/", "https://jsonplaceholder.typicode.com/"]
    d["x-response-note"] = "Only selected resource fields are modeled. Mutable fields other than the guide's post example need explicit team review. Writes are simulated by the service."
    return d


def dummyjson():
    d = document("DummyJSON", "https://dummyjson.com", "https://dummyjson.com/docs")
    resources = {
        "products": {"title": scalar("string"), "description": scalar("string"), "price": scalar("number"), "category": scalar("string"), "brand": scalar("string"), "stock": scalar("integer")},
        "users": {"firstName": scalar("string"), "lastName": scalar("string"), "age": scalar("integer"), "email": scalar("string"), "phone": scalar("string"), "username": scalar("string")},
        "posts": {"title": scalar("string"), "body": scalar("string"), "userId": scalar("integer")},
        "todos": {"todo": scalar("string"), "completed": scalar("boolean"), "userId": scalar("integer")},
    }
    for name, fields in resources.items():
        source = 'https://dummyjson.com/docs/' + name
        singular = name[:-1]
        response = obj({"id": scalar("integer"), **fields})
        envelope = obj({name: {"type": "array", "items": response}, "total": scalar("integer"), "skip": scalar("integer"), "limit": scalar("integer")})
        ids = [param("id", "path", "integer", f"Identifier of the {singular}", 1)]
        pagination = [param("limit", "query", "integer", "Maximum number of results", 10, minimum=0),
                      param("skip", "query", "integer", "Number of results to skip", 0, minimum=0),
                      param("select", "query", "string", "Fields to return, separated by commas", ','.join(list(fields)[:2]))]
        if name in ("products", "users", "posts"):
            pagination += [param("sortBy", "query", "string", "Field used for ordering", list(fields)[0]),
                           param("order", "query", "string", "Ordering direction", "asc", enum=["asc", "desc"])]
        path = '/' + name
        operation(d, path, "get", f"Retrieve one page of {name}", pagination, response=envelope, source=source)
        operation(d, path + '/{id}', "get", f"Retrieve a {singular} by identifier", ids, response=response, source=source)
        if name != "todos":
            operation(d, path + '/search', "get", f"Search {name} using a search term",
                      [param("q", "query", "string", "Search term", "phone" if name == 'products' else 'example', required=True)], response=envelope, source=source)
        core = list(fields) if name in ("posts", "todos") else list(fields)[:1]
        operation(d, path + '/add', "post", f"Submit a new {singular}", body=obj(fields), response=response, core=core, source=source)
        for method in ("put", "patch"):
            operation(d, path + '/{id}', method, f"Update selected fields of a {singular}", ids,
                      body=obj(fields), response=response, source=source)
        operation(d, path + '/{id}', "delete", f"Delete a {singular} by identifier", ids,
                  response=obj({**response['properties'], 'isDeleted': scalar('boolean'), 'deletedOn': scalar('string')}), source=source)
    d["x-response-note"] = "Examples define a partial field vocabulary, not an exhaustive schema or mandatory-field list. Writes are simulated. Cart operations are omitted because their documentation contains conflicting field names."
    return d


def restcountries():
    d = document("REST Countries", "https://api.restcountries.com", "https://restcountries.com/docs/countries")
    d['info']['version'] = 'v5-curated-2026-09-21'
    d['components'] = {'securitySchemes': {'api_key': {'type': 'http', 'scheme': 'bearer', 'description': 'API key sent using the documented bearer-header form.'}}}
    common = [param('limit', 'query', 'integer', 'Maximum number of results', 10, minimum=1, maximum=100),
              param('offset', 'query', 'integer', 'Number of results to skip', 0, minimum=0),
              param('response_fields', 'query', 'string', 'Return only these country attributes', 'names.common,codes.alpha_2'),
              param('response_fields_omit', 'query', 'string', 'Exclude these country attributes', 'names.translations')]
    q = param('q', 'query', 'string', 'Search term', 'can', minLength=1)
    response = obj({'data': obj({'objects': {'type': 'array', 'items': {'type': 'object'}}, 'meta': {'type': 'object'}})})
    operation(d, '/countries/v5', 'get', 'Retrieve one page of countries', common + [q], response=response)
    for aggregate, meaning in [('name', 'country names'), ('code', 'country codes')]:
        required_q = copy.deepcopy(q); required_q['required'] = True
        operation(d, '/countries/v5/' + aggregate, 'get', 'Search ' + meaning,
                  common + [required_q], response=response)
    properties = ['codes.alpha_2', 'codes.alpha_3', 'names.common', 'region', 'subregion',
                  'borders', 'currencies', 'calling_codes', 'capitals', 'landlocked', 'memberships.eu']
    operation(d, '/countries/v5/{property}/{value}', 'get', 'Look up countries by an exact property value',
              [param('property', 'path', 'string', 'Country attribute used for matching', 'names.common', enum=properties),
               param('value', 'path', 'string', 'Value to match exactly', 'Canada')] + common + [q], response=response)
    for item in d['paths'].values():
        for op in item.values():
            op['security'] = [{'api_key': []}]
            op['x-auth-source'] = 'https://restcountries.com/docs#authentication'
    d['x-version-note'] = 'Targets the documented v5 API at api.restcountries.com; do not mix with historical v3.1 endpoints.'
    return d


def main():
    for name, build in [('jsonplaceholder', jsonplaceholder), ('dummyjson', dummyjson), ('restcountries', restcountries)]:
        path = SOURCES / (name + '.curated.openapi.json')
        path.write_text(json.dumps(build(), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(path.name)


if __name__ == '__main__':
    main()
