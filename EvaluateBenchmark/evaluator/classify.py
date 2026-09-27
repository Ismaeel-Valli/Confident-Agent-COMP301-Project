"""Classifies one candidate against its task (EVALUATION_PLAN.md §2).

Classes
  correct          the request the task asks for (class C equivalences allowed)
  A                API hallucination: breaks the API's contract (primary outcome)
  B                a valid API call, but not the one the task asks for
  runtime_failure  the code never makes a request (crash, syntax error, no call)
  undetermined     cannot be decided automatically (partial specification, unmodelled
                   feature, other HTTP client); goes to manual review (§4)
  no_code          no candidate

The request comes from running the candidate in the sandbox with the task's test inputs;
the contract comes from the task's pinned OpenAPI source; the expected request from
test_case.expected_request.
"""
from __future__ import annotations

import hashlib
import json
from urllib.parse import parse_qsl, urlsplit

from . import sandbox
from .spec import Spec, check_value, plain_example

SEVERITY = ["correct", "B", "undetermined", "A"]  # a candidate takes its most severe finding


def code_hash(code: str) -> str:
    return hashlib.sha256(code.encode("utf-8")).hexdigest()


def text(value) -> str:
    """How requests serializes a parameter value."""
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, float) and value.is_integer():
        return repr(value)
    return str(value)


def final_request(req: dict):
    """Scheme, host, path and query (name -> list of values) as requests would send them."""
    url = req.get("url")
    if not isinstance(url, str):
        return None
    parts = urlsplit(url)
    query: dict = {}
    for k, v in parse_qsl(parts.query, keep_blank_values=True):
        query.setdefault(k, []).append(v)
    params = req.get("params")
    items = []
    if req.get("params_is_text") and isinstance(params, str):
        items = parse_qsl(params, keep_blank_values=True)
    elif isinstance(params, dict):
        items = list(params.items())
    elif isinstance(params, list):
        items = [tuple(p) for p in params if isinstance(p, (list, tuple)) and len(p) == 2]
    for k, v in items:
        for value in (v if isinstance(v, (list, tuple)) else [v]):
            if value is not None:  # requests drops None values
                query.setdefault(str(k), []).append(text(value))
    return {"scheme": parts.scheme.lower(), "host": (parts.hostname or "").lower(), "path": parts.path or "/",
            "query": query}


def header(headers: dict, name: str):
    for k, v in (headers or {}).items():
        if str(k).lower() == name.lower():
            return v
    return None


class Finding:
    def __init__(self):
        self.items: list = []  # (class, message)

    def add(self, cls: str, message: str):
        self.items.append((cls, message))

    def verdict(self) -> str:
        return max((c for c, _ in self.items), key=SEVERITY.index, default="correct")

    def reasons(self, cls: str | None = None) -> list:
        return [m for c, m in self.items if cls is None or c == cls]


class TaskContext:
    """What the evaluator knows about one task, prepared once."""

    def __init__(self, task: dict, spec: Spec):
        self.task, self.spec = task, spec
        self.api = task["api_specification"]
        self.expected = task["test_case"]["expected_request"]
        self.inputs = task["test_case"]["inputs"]
        self.output = task["test_case"]["expected_output"]
        self.partial = str(self.api.get("coverage") or "").lower().startswith("partial")
        base = urlsplit(self.api["base_url"])
        self.base_host, self.base_path = (base.hostname or "").lower(), base.path.rstrip("/")
        exp = urlsplit(self.expected["url"])
        self.expected_path = exp.path.rstrip("/") or "/"
        matched, _ = spec.match(self.relative(self.expected_path), self.expected["method"])
        self.success_status, schema = spec.success(matched[2]) if matched else (200, None)
        if schema is None:
            schema = self.api.get("response_schema")
        self.response_shape = spec.shape(schema) if schema else {"t": "unknown"}
        self.response_example = plain_example(self.response_shape)

    def relative(self, path: str) -> str:
        rel = path[len(self.base_path):] if self.base_path and path.startswith(self.base_path) else path
        return rel.rstrip("/") or "/"

    def undeclared(self, finding: Finding, message: str):
        """An undeclared name is a hallucination only if the specification is complete (§2)."""
        finding.add("undetermined" if self.partial else "A",
                    message + (" (partial specification: check the provider's documentation)" if self.partial else ""))


def classify(ctx: TaskContext, code: str | None, timeout: float = 10.0) -> dict:
    if not code or not code.strip():
        return {"class": "no_code", "reasons": ["no code"], "requests": 0}
    run = sandbox.run(code, ctx.inputs, "ok", ctx.response_shape, ctx.success_status, timeout)
    finding = Finding()
    for use in run.get("library_errors") or []:
        finding.add("A", f"uses requests API that does not exist: {use}")
    if run.get("exception") == "SandboxUnsupported":
        finding.add("undetermined", run.get("message") or "unsupported requests feature")
    requests_made = run.get("requests") or []
    if not requests_made and not finding.items:
        exc = run.get("exception")
        if exc in ("ModuleNotFoundError", "ImportError"):
            finding.add("undetermined", f"imports something the sandbox does not provide: {run.get('message')}")
        else:
            reason = f"{exc}: {run.get('message')}" if exc else "never calls the API"
            return {"class": "runtime_failure", "reasons": [reason], "requests": 0, "run": summarize(run)}
    matched_expected = [check_request(ctx, req, i, run, finding) for i, req in enumerate(requests_made)]
    if requests_made and not any(matched_expected):
        finding.add("B", "no request matches the expected method and endpoint")
    if len(requests_made) > 1:
        finding.add("B", f"makes {len(requests_made)} requests; the task needs one")
    result = {"class": finding.verdict(), "reasons": finding.reasons(), "a_reasons": finding.reasons("A"), "b_reasons": finding.reasons("B"),
              "requests": len(requests_made), "run": summarize(run)}
    result["behaviour"] = behaviour(ctx, code, run, timeout)
    return result


def summarize(run: dict) -> dict:
    return {k: run.get(k) for k in ("stage", "exception", "message", "returned") if run.get(k) is not None} | {
        "requests": run.get("requests") or []}


def check_request(ctx: TaskContext, req: dict, index: int, run: dict, finding: Finding) -> bool:
    """Adds findings for one request; returns whether it is the task's operation."""
    method = str(req.get("method") or "").upper()
    url = final_request(req)
    if url is None:
        finding.add("A", f"request {index + 1}: the URL is not a string")
        return False
    where = f"request {index + 1} ({method} {url['scheme']}://{url['host']}{url['path']})"
    if url["host"] != ctx.base_host or not (url["path"] == ctx.base_path or url["path"].startswith(ctx.base_path + "/")
                                              or not ctx.base_path):
        finding.add("A", f"{where}: not the task's API ({ctx.api['base_url']}); wrong host, version or base path")
        return False
    if url["scheme"] != "https":
        finding.add("B", f"{where}: uses {url['scheme']} instead of https")
    matched, reason = ctx.spec.match(ctx.relative(url["path"]), method)
    if not matched:
        if "no declared path" in reason:
            ctx.undeclared(finding, f"{where}: {reason}")
        else:
            finding.add("A", f"{where}: {reason}")
        return False
    path_key, item, op, path_values = matched
    params = ctx.spec.parameters(item, op)
    # Path values
    for name, value in path_values.items():
        p = params.get(("path", name))
        if p:
            for kind, msg in check_value(ctx.spec, value, p.get("schema"), f"path.{name}", from_text=True):
                finding.add("A", f"{where}: {msg}")
    # Query
    auth_query = ctx.spec.security_query_names(op)
    for name, values in url["query"].items():
        p = params.get(("query", name))
        if p is None:
            if name not in auth_query:
                ctx.undeclared(finding, f"{where}: query parameter {name} is not declared")
            continue
        schema = ctx.spec.schema(p.get("schema")) or {}
        explode = p.get("explode", p.get("style", "form") == "form")
        value = values if (schema.get("type") == "array" and explode) else (
            values[0].split(",") if schema.get("type") == "array" else values[0])
        for kind, msg in check_value(ctx.spec, value, schema, f"query.{name}", from_text=True):
            finding.add("A", f"{where}: {msg}")
    for (loc, name), p in params.items():
        if p.get("required") and loc == "query" and name not in url["query"]:
            finding.add("A", f"{where}: required query parameter {name} is missing")
    # Body
    body = ctx.spec.request_body(op)
    if req.get("has_json") or req.get("has_data"):
        payload = req.get("json") if req.get("has_json") else req.get("data")
        if isinstance(payload, str) and req.get("has_data"):
            try:
                payload = json.loads(payload)
            except ValueError:
                pass
        if body is None:
            ctx.undeclared(finding, f"{where}: sends a request body the operation does not declare")
        else:
            json_schema = next((s for ct, s in body["content"].items() if "json" in ct), None)
            form_schema = next((s for ct, s in body["content"].items() if "form" in ct), None)
            if req.get("has_json") and json_schema is None:
                finding.add("A", f"{where}: sends JSON; the operation accepts {', '.join(body['content'])}")
            elif req.get("has_data") and form_schema is None and not isinstance(payload, (dict, list)):
                finding.add("A", f"{where}: sends a form or raw body; the operation accepts {', '.join(body['content'])}")
            else:
                schema = json_schema if json_schema is not None else form_schema
                for kind, msg in check_value(ctx.spec, payload, schema, "body"):
                    if kind == "undeclared":
                        ctx.undeclared(finding, f"{where}: {msg}")
                    else:
                        finding.add("A", f"{where}: {msg}")
                if req.get("has_data") and json_schema is not None and form_schema is None:
                    finding.add("B", f"{where}: sends the JSON body as data= (no JSON Content-Type)")
    elif body and body["required"]:
        finding.add("A", f"{where}: the required request body is missing")
    # Credential (the task's answer key)
    check_credential(ctx, req, where, finding)
    # Response fields the code read from this request's response
    for req_index, path, status in run.get("reads") or []:
        if req_index == index and status == "undocumented":
            ctx.undeclared(finding, f"{where}: reads response field {'.'.join(map(str, path))}, which the response does not document")
    # Is this the task's operation, and is it the requested one?
    is_expected = method in [m.upper() for m in (ctx.api.get("acceptable_methods") or [ctx.expected["method"]])] and \
        url["path"].rstrip("/") == ctx.expected_path
    if is_expected:
        compare_to_expected(ctx, req, url, params, where, finding)
    elif url["path"].rstrip("/") == ctx.expected_path:
        finding.add("B", f"{where}: method {method} is not acceptable for this task "
                         f"({', '.join(ctx.api.get('acceptable_methods') or [ctx.expected['method']])})")
    else:
        finding.add("B", f"{where}: a different declared endpoint than the task's ({ctx.expected['method']} {ctx.expected_path})")
    return is_expected or url["path"].rstrip("/") == ctx.expected_path


def check_credential(ctx: TaskContext, req: dict, where: str, finding: Finding):
    auth = ctx.api.get("auth") or {}
    if not auth.get("required_by_task"):
        return
    credential = str(ctx.inputs.get("credential", ""))
    expected = f"{auth.get('prefix') or ''}{credential}"
    got = header(req.get("headers"), auth.get("header") or "Authorization")
    severity = "A" if auth.get("required_by_api") else "B"
    if got is None and req.get("auth"):
        finding.add(severity, f"{where}: sends the credential as {list(req['auth'])[0]} auth, not in {auth.get('header')}")
    elif got is None:
        finding.add(severity, f"{where}: the credential ({auth.get('header')}) is missing")
    elif str(got) == expected:
        return
    elif auth.get("type") == "bearer" and str(got) == f"token {credential}" and ctx.api["api_name"] == "GitHub":
        return  # class C: GitHub accepts 'token' for personal access tokens
    else:
        finding.add(severity, f"{where}: {auth.get('header')} is {json.dumps(str(got))[:60]}, expected the form {json.dumps(expected)[:60]}")


def compare_to_expected(ctx: TaskContext, req: dict, url: dict, params: dict, where: str, finding: Finding):
    expected_query = ctx.expected.get("query") or {}
    for name, value in expected_query.items():
        want = [text(v) for v in value] if isinstance(value, list) else [text(value)]
        got = url["query"].get(name)
        if got is None:
            finding.add("B", f"{where}: omits query parameter {name}={','.join(want)} that the task specifies")
        elif not same_values(got, want):
            finding.add("B", f"{where}: query {name}={','.join(got)}, the task needs {','.join(want)}")
    expected_body = ctx.expected.get("json_body")
    sent = req.get("json") if req.get("has_json") else None
    if sent is None and req.get("has_data") and isinstance(req.get("data"), str):
        try:
            sent = json.loads(req["data"])
        except ValueError:
            sent = None
    if expected_body is None and sent is not None:
        finding.add("B", f"{where}: sends a body the task does not ask for")
    elif expected_body is not None:
        if sent is None:
            finding.add("B", f"{where}: omits the request body the task specifies")
        elif not same_json(sent, expected_body):
            finding.add("B", f"{where}: body {json.dumps(sent)[:120]} differs from the task's {json.dumps(expected_body)[:120]}")


def same_values(got: list, want: list) -> bool:
    if [g.lower() for g in got] == [w.lower() for w in want]:
        return True
    return ",".join(got).lower() == ",".join(want).lower()  # 'a,b' sent as one value or as two


def same_json(a, b) -> bool:
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(same_json(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(same_json(x, y) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
        return a == b
    return a == b


def behaviour(ctx: TaskContext, code: str, ok_run: dict, timeout: float) -> dict:
    """The task's behaviour requirements (secondary): the right return value, None (or the
    status code) for an empty success, an exception for an unsuccessful response."""
    kind = ctx.output.get("kind")
    returned = ok_run.get("returned") if ok_run.get("stage") == "returned" else "<exception>"
    if kind == "optional_response_field":
        want = ctx.response_example.get(ctx.output.get("field")) if isinstance(ctx.response_example, dict) else None
    elif kind == "http_status_code":
        want = ctx.success_status
    else:
        want = ctx.response_example
    empty = sandbox.run(code, ctx.inputs, "empty", ctx.response_shape, ctx.success_status, timeout)
    error = sandbox.run(code, ctx.inputs, "error", ctx.response_shape, ctx.success_status, timeout)
    empty_want = 204 if ctx.output.get("empty_response") == "return_status_code" else None
    return {"returns_expected_value": returned == want,
            "empty_response_ok": empty.get("stage") == "returned" and empty.get("returned") == empty_want,
            "error_raises": bool(error.get("exception")) and error.get("exception") not in ("Timeout", "SandboxCrash")}
