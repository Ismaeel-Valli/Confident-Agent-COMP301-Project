"""Runs one candidate `solve(inputs)` in this (child) process with a recording stand-in for
the `requests` library, and prints what it did. Started by evaluate_benchmark.py as
`python -I -S sandbox_harness.py` with the job as JSON on stdin; never imported.

Nothing leaves the machine: `requests` is replaced by a recorder that returns a response
built from the documented response schema, sockets, subprocesses and file writes are
blocked, and `time.sleep` returns at once. This keeps honest model output from reaching the
network or the disk; it is not a security boundary against deliberately hostile code.

Output: one line `@@RESULT@@<json>` with the requests made, the response fields read, the
return value or exception, and whether a non-existent `requests` API was used.
"""
import builtins
import copy
import json
import sys
import traceback
import types

JOB = json.loads(sys.stdin.read())
REQUESTS: list = []
READS: list = []       # [request index, path, "documented" | "undocumented" | "open"]
LIBRARY_ERRORS: list = []  # uses of requests APIs that do not exist
UNSUPPORTED: list = []     # real requests APIs this stand-in does not implement

# Public names of the real library (requests 2.32), so a real-but-unimplemented name is
# told apart from an invented one.
REAL_TOP = {"ConnectTimeout", "ConnectionError", "DependencyWarning", "FileModeWarning", "HTTPError", "JSONDecodeError",
            "NullHandler", "PreparedRequest", "ReadTimeout", "Request", "RequestException", "RequestsDependencyWarning",
            "Response", "Session", "Timeout", "TooManyRedirects", "URLRequired", "adapters", "api", "auth", "certs",
            "chardet_version", "charset_normalizer_version", "check_compatibility", "codes", "compat", "cookies", "delete",
            "exceptions", "get", "head", "hooks", "logging", "models", "options", "packages", "patch", "post", "put",
            "request", "session", "sessions", "ssl", "status_codes", "structures", "urllib3", "utils", "warnings",
            "__version__", "__title__", "__build__", "__author__", "__license__", "__copyright__", "__cake__",
            "__description__", "__url__", "__author_email__"}
REAL_RESPONSE = {"apparent_encoding", "close", "content", "is_permanent_redirect", "is_redirect", "iter_content",
                 "iter_lines", "json", "links", "next", "ok", "raise_for_status", "text", "status_code", "headers", "raw",
                 "url", "encoding", "history", "reason", "cookies", "elapsed", "request", "connection"}
REAL_SESSION = {"close", "delete", "get", "get_adapter", "get_redirect_target", "head", "merge_environment_settings",
                "mount", "options", "patch", "post", "prepare_request", "put", "rebuild_auth", "rebuild_method",
                "rebuild_proxies", "request", "resolve_redirects", "send", "should_strip_auth", "headers", "auth",
                "proxies", "hooks", "params", "stream", "verify", "cert", "max_redirects", "trust_env", "cookies",
                "adapters"}
REQUEST_KWARGS = {"params", "data", "headers", "cookies", "files", "auth", "timeout", "allow_redirects", "proxies",
                  "hooks", "stream", "verify", "cert", "json"}


class SandboxUnsupported(Exception):
    """A real requests feature this stand-in does not model."""


class HallucinatedLibraryAPI(AttributeError):
    """A requests attribute that does not exist in the real library."""


def missing(kind: str, name: str, real: set):
    if name in real:
        UNSUPPORTED.append(f"{kind}.{name}")
        raise SandboxUnsupported(f"{kind}.{name} is not modelled by the evaluation sandbox")
    LIBRARY_ERRORS.append(f"{kind}.{name}")
    raise HallucinatedLibraryAPI(f"module 'requests' has no attribute '{name}'" if kind == "requests"
                                 else f"'{kind}' object has no attribute '{name}'")


# ---------------------------------------------------------------- response bodies
class Node:
    """Mixin for recorded response values: every key read is logged with whether the
    documented schema has it."""
    def _init(self, path, request_index, open_):
        self._path, self._req, self._open = path, request_index, open_

    def _read(self, key, present):
        status = "documented" if present else ("open" if self._open else "undocumented")
        READS.append([self._req, self._path + [key if isinstance(key, (str, int)) else str(key)], status])


class DictNode(dict, Node):
    def __getitem__(self, key):
        present = dict.__contains__(self, key)
        self._read(key, present)
        if present:
            return dict.__getitem__(self, key)
        if self._open:
            return build({"t": "unknown"}, self._path + [key], self._req)
        raise KeyError(key)

    def get(self, key, default=None):
        present = dict.__contains__(self, key)
        self._read(key, present)
        return dict.__getitem__(self, key) if present else default


class ListNode(list, Node):
    def __getitem__(self, index):
        if isinstance(index, slice):
            return list.__getitem__(self, index)
        self._read("[]", True)
        return list.__getitem__(self, index)


class OpenNode(dict, Node):
    """A value whose schema is unknown: reads are recorded as 'open' and return more of the same."""
    def __getitem__(self, key):
        self._read(key, False)
        return OpenNode._make(self._path + [key], self._req)

    def get(self, key, default=None):
        self._read(key, False)
        return default

    @staticmethod
    def _make(path, req):
        node = OpenNode()
        node._init(path, req, True)
        return node


def build(shape, path, req):
    kind = shape.get("t")
    if kind == "object":
        node = DictNode()
        node._init(path, req, bool(shape.get("open")))
        for key, sub in (shape.get("props") or {}).items():
            dict.__setitem__(node, key, build(sub, path + [key], req))
        return node
    if kind == "array":
        node = ListNode()
        node._init(path, req, False)
        list.append(node, build(shape.get("items") or {"t": "unknown"}, path + ["[]"], req))
        return node
    if kind == "value":
        return copy.deepcopy(shape.get("v"))
    return OpenNode._make(path, req)


def plain(value, depth=0):
    """A JSON-able copy of a value built from response nodes."""
    if depth > 20:
        return "<deep>"
    if isinstance(value, dict):
        return {str(k): plain(dict.__getitem__(value, k), depth + 1) for k in dict.keys(value)}
    if isinstance(value, (list, tuple)):
        return [plain(v, depth + 1) for v in (list.__iter__(value) if isinstance(value, list) else value)]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, bytes):
        return value.decode("utf-8", "replace")
    return f"<{type(value).__name__}>"


# ---------------------------------------------------------------- stand-in library
class CaseInsensitiveDict(dict):
    def __init__(self, data=None, **kw):
        super().__init__()
        self.update(data or {}, **kw)

    def __setitem__(self, k, v):
        for existing in list(self.keys()):
            if isinstance(existing, str) and isinstance(k, str) and existing.lower() == k.lower():
                dict.__delitem__(self, existing)
        dict.__setitem__(self, k, v)

    def __getitem__(self, k):
        for existing in self.keys():
            if isinstance(existing, str) and isinstance(k, str) and existing.lower() == k.lower():
                return dict.__getitem__(self, existing)
        raise KeyError(k)

    def get(self, k, default=None):
        try:
            return self[k]
        except KeyError:
            return default

    def __contains__(self, k):
        return any(isinstance(e, str) and isinstance(k, str) and e.lower() == k.lower() for e in self.keys())

    def update(self, other=None, **kw):
        for k, v in (dict(other or {}) | kw).items():
            self[k] = v

    def copy(self):
        return CaseInsensitiveDict(dict(self))


def _exceptions():
    m = types.ModuleType("requests.exceptions")

    class RequestException(IOError):
        def __init__(self, *args, **kwargs):
            self.response = kwargs.pop("response", None)
            self.request = kwargs.pop("request", None)
            super().__init__(*args, **kwargs)

    class InvalidJSONError(RequestException):
        pass

    class JSONDecodeError(InvalidJSONError, json.JSONDecodeError):
        def __init__(self, *args, **kwargs):
            json.JSONDecodeError.__init__(self, *(args or ("Expecting value", "", 0)))
            InvalidJSONError.__init__(self, *self.args, **kwargs)

    names = {"RequestException": RequestException, "InvalidJSONError": InvalidJSONError, "JSONDecodeError": JSONDecodeError}
    bases = [("HTTPError", (RequestException,)), ("ConnectionError", (RequestException,)),
             ("ProxyError", ("ConnectionError",)), ("SSLError", ("ConnectionError",)), ("Timeout", (RequestException,)),
             ("ConnectTimeout", ("ConnectionError", "Timeout")), ("ReadTimeout", ("Timeout",)),
             ("URLRequired", (RequestException,)), ("TooManyRedirects", (RequestException,)),
             ("MissingSchema", (RequestException, ValueError)), ("InvalidSchema", (RequestException, ValueError)),
             ("InvalidURL", (RequestException, ValueError)), ("InvalidHeader", (RequestException, ValueError)),
             ("InvalidProxyURL", ("InvalidURL",)), ("ChunkedEncodingError", (RequestException,)),
             ("ContentDecodingError", (RequestException,)), ("StreamConsumedError", (RequestException, TypeError)),
             ("RetryError", (RequestException,)), ("UnrewindableBodyError", (RequestException,)),
             ("BaseHTTPError", (Exception,))]
    for name, parents in bases:
        names[name] = type(name, tuple(names[p] if isinstance(p, str) else p for p in parents), {})
    for w in ("RequestsWarning", "FileModeWarning", "RequestsDependencyWarning"):
        names[w] = type(w, (Warning,), {})
    names["CompatJSONDecodeError"] = json.JSONDecodeError
    for k, v in names.items():
        setattr(m, k, v)
    return m


EXC = _exceptions()
STATUS = {"continue": 100, "ok": 200, "okay": 200, "all_ok": 200, "created": 201, "accepted": 202, "no_content": 204,
          "moved_permanently": 301, "found": 302, "not_modified": 304, "bad_request": 400, "unauthorized": 401,
          "forbidden": 403, "not_found": 404, "method_not_allowed": 405, "conflict": 409, "gone": 410,
          "unprocessable_entity": 422, "too_many_requests": 429, "internal_server_error": 500, "bad_gateway": 502,
          "service_unavailable": 503, "gateway_timeout": 504}


class Codes(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError(name)


class Response:
    def __init__(self, status, body, index, method, url):
        self.status_code = status
        self.headers = CaseInsensitiveDict({"Content-Type": "application/json"} if body is not None else {})
        self.url, self.reason, self.encoding = url, {200: "OK", 201: "Created", 204: "No Content", 500: "Internal Server Error"}.get(status, ""), "utf-8"
        self.history, self.cookies, self.elapsed, self.request = [], {}, None, types.SimpleNamespace(method=method, url=url, headers={})
        self._body, self._index = body, index

    def __getattr__(self, name):
        missing("Response", name, REAL_RESPONSE)

    @property
    def ok(self):
        return self.status_code < 400

    @property
    def content(self):
        return b"" if self._body is None else json.dumps(plain(self._body)).encode()

    @property
    def text(self):
        return self.content.decode()

    def json(self, **kwargs):
        if self._body is None:
            raise EXC.JSONDecodeError("Expecting value", "", 0)
        return self._body

    def raise_for_status(self):
        if self.status_code >= 400:
            raise EXC.HTTPError(f"{self.status_code} Server Error: {self.reason} for url: {self.url}", response=self)

    def close(self):
        pass

    def iter_content(self, chunk_size=1, decode_unicode=False):
        yield self.content

    def iter_lines(self, *a, **k):
        yield from self.content.splitlines()

    def __bool__(self):
        return self.ok

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def _auth_value(auth):
    if auth is None:
        return None
    if isinstance(auth, (tuple, list)) and len(auth) == 2:
        return {"basic": [plain(auth[0]), plain(auth[1])]}
    if isinstance(auth, AUTH.HTTPBasicAuth):
        return {"basic": [plain(auth.username), plain(auth.password)]}
    return {"custom": type(auth).__name__}


def _send(method, url, kwargs, defaults=None):
    unknown = set(kwargs) - REQUEST_KWARGS
    if unknown:
        LIBRARY_ERRORS.append("request(" + ", ".join(sorted(unknown)) + "=)")
        raise TypeError(f"request() got an unexpected keyword argument '{sorted(unknown)[0]}'")
    defaults = defaults or {}
    headers = CaseInsensitiveDict(defaults.get("headers") or {})
    headers.update(kwargs.get("headers") or {})
    params = kwargs.get("params")
    if defaults.get("params") and isinstance(params, (dict, type(None))):
        params = {**defaults["params"], **(params or {})}
    auth = kwargs.get("auth") if kwargs.get("auth") is not None else defaults.get("auth")
    index = len(REQUESTS)
    REQUESTS.append({"method": str(method).upper(), "url": plain(url),
                     "params": plain(params) if not isinstance(params, (str, bytes)) else plain(params),
                     "params_is_text": isinstance(params, (str, bytes)),
                     "json": plain(kwargs.get("json")), "has_json": kwargs.get("json") is not None,
                     "data": plain(kwargs.get("data")), "has_data": kwargs.get("data") is not None,
                     "headers": {str(k): plain(v) for k, v in dict(headers).items()},
                     "auth": _auth_value(auth), "has_files": kwargs.get("files") is not None,
                     "cookies": plain(kwargs.get("cookies"))})
    scenario = JOB["scenario"]
    if scenario == "empty":
        return Response(204, None, index, method, url)
    if scenario == "error":
        body = DictNode()
        body._init([], index, True)
        dict.__setitem__(body, "message", "Internal Server Error")
        return Response(500, body, index, method, url)
    return Response(JOB.get("success_status") or 200, build(JOB["response_shape"], [], index), index, method, url)


def _verb(method, positional):
    def call(url, *args, **kwargs):
        if len(args) > len(positional):
            raise TypeError(f"{method.lower()}() takes at most {len(positional) + 1} positional arguments")
        kwargs.update(dict(zip(positional, args)))
        return _send(method, url, kwargs)
    call.__name__ = method.lower()
    return call


class Session:
    def __init__(self):
        self.headers = CaseInsensitiveDict({"User-Agent": "python-requests/2.32.5", "Accept": "*/*"})
        self.auth, self.params, self.cookies, self.proxies, self.hooks = None, {}, {}, {}, {"response": []}
        self.verify, self.stream, self.cert, self.max_redirects, self.trust_env, self.adapters = True, False, None, 30, True, {}

    def __getattr__(self, name):
        missing("Session", name, REAL_SESSION)

    def request(self, method, url, *args, **kwargs):
        names = ["params", "data", "headers", "cookies", "files", "auth", "timeout", "allow_redirects", "proxies",
                 "hooks", "stream", "verify", "cert", "json"]
        kwargs.update(dict(zip(names, args)))
        return _send(method, url, kwargs, {"headers": self.headers, "params": self.params, "auth": self.auth})

    def get(self, url, **kw):
        return self.request("GET", url, **kw)

    def options(self, url, **kw):
        return self.request("OPTIONS", url, **kw)

    def head(self, url, **kw):
        return self.request("HEAD", url, **kw)

    def post(self, url, data=None, json=None, **kw):
        return self.request("POST", url, data=data, json=json, **kw)

    def put(self, url, data=None, **kw):
        return self.request("PUT", url, data=data, **kw)

    def patch(self, url, data=None, **kw):
        return self.request("PATCH", url, data=data, **kw)

    def delete(self, url, **kw):
        return self.request("DELETE", url, **kw)

    def mount(self, prefix, adapter):
        self.adapters[prefix] = adapter

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def _auth_module():
    m = types.ModuleType("requests.auth")

    class AuthBase:
        def __call__(self, r):
            return r

    class HTTPBasicAuth(AuthBase):
        def __init__(self, username, password):
            self.username, self.password = username, password

    class HTTPDigestAuth(HTTPBasicAuth):
        pass

    class HTTPProxyAuth(HTTPBasicAuth):
        pass

    m.AuthBase, m.HTTPBasicAuth, m.HTTPDigestAuth, m.HTTPProxyAuth = AuthBase, HTTPBasicAuth, HTTPDigestAuth, HTTPProxyAuth
    return m


AUTH = _auth_module()


class RequestsModule(types.ModuleType):
    def __getattr__(self, name):
        missing("requests", name, REAL_TOP)


def install_requests():
    r = RequestsModule("requests")
    r.__version__ = "2.32.5"
    r.request = lambda method, url, *a, **k: _send(method, url, {**dict(zip(["params", "data", "headers", "cookies", "files", "auth", "timeout", "allow_redirects", "proxies", "hooks", "stream", "verify", "cert", "json"], a)), **k})
    r.get = _verb("GET", ["params"])
    r.options = _verb("OPTIONS", [])
    r.head = _verb("HEAD", [])
    r.post = _verb("POST", ["data", "json"])
    r.put = _verb("PUT", ["data"])
    r.patch = _verb("PATCH", ["data"])
    r.delete = _verb("DELETE", [])
    r.Session, r.session, r.Response = Session, Session, Response
    r.exceptions, r.auth = EXC, AUTH
    for name in ("RequestException", "HTTPError", "ConnectionError", "Timeout", "ConnectTimeout", "ReadTimeout",
                 "TooManyRedirects", "URLRequired", "JSONDecodeError"):
        setattr(r, name, getattr(EXC, name))
    r.codes = Codes(STATUS)
    structures = types.ModuleType("requests.structures")
    structures.CaseInsensitiveDict = CaseInsensitiveDict
    r.structures = structures
    adapters = types.ModuleType("requests.adapters")
    adapters.HTTPAdapter = type("HTTPAdapter", (), {"__init__": lambda self, *a, **k: None})
    r.adapters = adapters
    sys.modules.update({"requests": r, "requests.exceptions": EXC, "requests.auth": AUTH,
                        "requests.structures": structures, "requests.adapters": adapters})


# ---------------------------------------------------------------- confinement
def confine():
    import os
    import shutil
    import socket
    import subprocess
    import time
    import urllib.request
    import http.client

    def deny(*a, **k):
        raise PermissionError("blocked by the evaluation sandbox")

    socket.socket = deny
    socket.create_connection = deny
    urllib.request.urlopen = deny
    http.client.HTTPConnection = deny
    http.client.HTTPSConnection = deny
    for name in ("Popen", "run", "call", "check_call", "check_output"):
        setattr(subprocess, name, deny)
    for name in ("system", "popen", "remove", "unlink", "rmdir", "removedirs", "rename", "replace", "kill"):
        if hasattr(os, name):
            setattr(os, name, deny)
    shutil.rmtree = deny
    real_open = builtins.open

    def safe_open(file, mode="r", *a, **k):
        if any(c in str(mode) for c in "wax+"):
            raise PermissionError("file writes are blocked by the evaluation sandbox")
        return real_open(file, mode, *a, **k)
    builtins.open = safe_open
    time.sleep = lambda *a, **k: None


# ---------------------------------------------------------------- run
def main():
    out = sys.stdout
    install_requests()
    confine()
    result = {"stage": "compile"}
    namespace = {"__name__": "candidate"}
    try:
        code = compile(JOB["code"], "<candidate>", "exec")
        result["stage"] = "import"
        exec(code, namespace)
        solve = namespace.get("solve")
        if not callable(solve):
            raise NameError("the candidate defines no solve() function")
        result["stage"] = "call"
        value = solve(copy.deepcopy(JOB["inputs"]))
        result.update({"stage": "returned", "returned": plain(value), "returned_type": type(value).__name__})
    except SandboxUnsupported as e:
        result.update({"exception": "SandboxUnsupported", "message": str(e)})
    except BaseException as e:  # noqa: BLE001 - everything the candidate does is recorded
        tb = traceback.extract_tb(e.__traceback__)
        in_candidate = [f for f in tb if f.filename == "<candidate>"]
        result.update({"exception": type(e).__name__, "message": str(e)[:500],
                       "line": in_candidate[-1].lineno if in_candidate else None,
                       "requests_exception": type(e).__module__ == "requests.exceptions" or isinstance(e, EXC.RequestException)})
    result.update({"requests": REQUESTS, "reads": READS, "library_errors": LIBRARY_ERRORS, "unsupported": UNSUPPORTED})
    out.write("@@RESULT@@" + json.dumps(result, default=str) + "\n")
    out.flush()


main()
