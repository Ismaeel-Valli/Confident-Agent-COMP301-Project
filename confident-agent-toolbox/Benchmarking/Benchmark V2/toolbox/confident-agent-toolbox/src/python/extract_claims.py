"""Conservative static extraction. Never imports or executes the candidate.

Values are abstract. A value is either a statically known Python literal
(str/int/float/bool/None, a dict with string keys, a list), an Opaque runtime
value (optionally with a statically evident Python type), or a Template: a
string whose literal parts are known and whose holes are runtime values, such
as f"https://host/users/{user_id}". Unknown values are never guessed, and a
container that is changed in a way the analysis cannot follow becomes Opaque
rather than keeping a stale value.

Each extraction issue lists the verification layers whose claim inventory it
can make incomplete ("affects"). Other layers keep their evidence.
"""
import ast
import builtins
import io
import json
import string
import sys
import tokenize
import types
import urllib.parse

payload = json.load(sys.stdin)
code = payload.get('code', '')
bindings = payload.get('input_bindings', {}) or {}

ALL = ['interface', 'identifier', 'access_point', 'input_contract', 'output_contract', 'contextual']
API = ['access_point', 'input_contract', 'output_contract', 'contextual']
REQUEST = ['input_contract', 'contextual']
RESPONSE = ['output_contract']
IDENTIFIER = ['identifier']

HTTP = {'get', 'post', 'put', 'patch', 'delete', 'head', 'options'}
# requests.<verb>(url, <positional>...) as defined by requests.api.
POSITIONAL = {'get': ['params'], 'post': ['data', 'json'], 'put': ['data'], 'patch': ['data'],
              'delete': [], 'head': [], 'options': [], 'request': []}
REQUEST_KWARGS = {'url', 'method', 'params', 'json', 'data', 'headers', 'cookies', 'auth',
                  'timeout', 'allow_redirects', 'verify', 'stream', 'proxies', 'cert'}
OTHER_HTTP_CLIENTS = ('httpx.', 'aiohttp.', 'urllib.request.', 'urllib3.', 'http.client.', 'pycurl.')
# Calls that neither mutate their arguments nor perform HTTP requests.
PURE = {
    'print', 'len', 'str', 'int', 'float', 'bool', 'bytes', 'bytearray', 'complex', 'frozenset',
    'object', 'slice', 'memoryview', 'format', 'isinstance', 'issubclass', 'hasattr', 'callable',
    'type', 'id', 'repr', 'hash', 'dir', 'list', 'dict', 'set', 'tuple', 'range', 'enumerate',
    'zip', 'iter', 'next', 'reversed', 'sorted', 'min', 'max', 'sum', 'abs', 'round', 'pow',
    'divmod', 'bin', 'hex', 'oct', 'chr', 'ord', 'any', 'all', 'super', 'property',
    'classmethod', 'staticmethod',
    'json.dumps', 'json.loads', 'json.dump', 'os.getenv', 'os.environ.get',
    'urllib.parse.quote', 'urllib.parse.quote_plus', 'urllib.parse.unquote',
    'urllib.parse.urlencode', 'urllib.parse.urljoin', 'urllib.parse.urlparse',
    'time.sleep', 'time.time', 'sys.exit', 'logging.debug', 'logging.info', 'logging.warning',
    'logging.error', 'logging.exception', 'logging.critical', 'logging.getLogger',
    'datetime.datetime.now', 'datetime.date.today',
}
BUILTIN_EXCEPTIONS = {n for n in dir(builtins) if n.endswith(('Error', 'Exception', 'Warning', 'Exit', 'Interrupt'))}
MUTATORS = {'update', 'setdefault', 'pop', 'popitem', 'clear', 'append', 'extend', 'insert', 'remove', 'sort', 'reverse'}
DYNAMIC_CODE = {'getattr', 'setattr', 'delattr', 'eval', 'exec', 'compile', '__import__', 'globals', 'importlib.import_module'}

claims, issues, unused_parameters = [], [], []


class Opaque:
    """A runtime value. type is a statically evident Python type name, if any."""
    __slots__ = ('label', 'type')

    def __init__(self, label='', type_=None):
        self.label, self.type = label, type_

    def __eq__(self, other):
        return isinstance(other, Opaque) and other.label == self.label and other.type == self.type

    __hash__ = None


class Template:
    """A string with known literal parts and Opaque holes."""
    __slots__ = ('parts',)

    def __init__(self, parts):
        self.parts = tuple(parts)

    def __eq__(self, other):
        return isinstance(other, Template) and other.parts == self.parts

    __hash__ = None


AMBIGUOUS = object()  # provenance that differs across control-flow paths
MISSING = object()


def make_string(parts):
    """Normalise parts (str, Template, Opaque) into a str or a Template."""
    flat = []
    for part in parts:
        if isinstance(part, Template):
            flat.extend(part.parts)
        elif isinstance(part, str):
            flat.append(part)
        else:
            flat.append(part if isinstance(part, Opaque) else Opaque(str(part)))
    merged = []
    for part in flat:
        if isinstance(part, str) and merged and isinstance(merged[-1], str):
            merged[-1] += part
        elif part != '':
            merged.append(part)
    if all(isinstance(p, str) for p in merged):
        return ''.join(merged)
    return Template(merged)


def label(node):
    try:
        text = ast.unparse(node)
    except Exception:  # pragma: no cover - defensive
        text = type(node).__name__
    return text if len(text) <= 80 else text[:77] + '...'


def issue(node, reason, affects=None):
    item = {'line': getattr(node, 'lineno', 0), 'reason': reason, 'affects': list(affects or ALL)}
    if not any(i['line'] == item['line'] and i['reason'] == reason for i in issues):
        issues.append(item)


def add(node, kind, **fields):
    result = {'id': 'claim_%s' % (len(claims) + 1), 'type': kind, 'line': getattr(node, 'lineno', 0), **fields}
    claims.append(result)
    return result


def known(value):
    if isinstance(value, (Opaque, Template)):
        return False
    if isinstance(value, dict):
        return all(known(v) for v in value.values())
    if isinstance(value, (list, tuple)):
        return all(known(v) for v in value)
    return True


def public(value):
    return encode(value) if known(value) else None


def encode(value):
    """JSON form of an abstract value; unknown parts are explicit markers."""
    if isinstance(value, Opaque):
        return {'$ca': 'unknown', 'label': value.label, 'type': value.type}
    if isinstance(value, Template):
        return {'$ca': 'template', 'parts': [p if isinstance(p, str) else {'hole': p.label} for p in value.parts]}
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return {'$ca': 'unknown', 'label': repr(value)[:80], 'type': type(value).__name__}


def type_of(value):
    if isinstance(value, Opaque):
        return value.type
    if isinstance(value, Template):
        return 'str'
    return type(value).__name__


def origin_known(url):
    """True when a Template's scheme and host are literal."""
    if not isinstance(url, Template) or not url.parts or not isinstance(url.parts[0], str):
        return False
    head = url.parts[0]
    if '://' not in head:
        return False
    rest = head.split('://', 1)[1]
    return any(c in rest for c in '/?#') and rest.split('/')[0].split('?')[0] != ''


def copy_value(value):
    if isinstance(value, dict):
        return {k: copy_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [copy_value(v) for v in value]
    return value


def assigned_names(nodes):
    """Names (re)bound or mutated anywhere inside the statements."""
    names = set()
    for stmt in nodes:
        for n in ast.walk(stmt):
            if isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
                names.add(n.id)
            elif isinstance(n, (ast.Subscript, ast.Attribute)) and isinstance(n.ctx, (ast.Store, ast.Del)):
                root = n
                while isinstance(root, (ast.Subscript, ast.Attribute)):
                    root = root.value
                if isinstance(root, ast.Name):
                    names.add(root.id)
            elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in MUTATORS \
                    and isinstance(n.func.value, ast.Name):
                names.add(n.func.value.id)
            elif isinstance(n, (ast.Global, ast.Nonlocal)):
                names.update(n.names)
    return names


class Context:
    def __init__(self):
        self.calls = {}           # id(ast.Call) -> call_id for HTTP requests
        self.functions = {}       # module-level function name -> FunctionInfo
        self.module = None        # module-level Analyzer


class FunctionInfo:
    def __init__(self, node):
        self.node, self.done, self.running, self.summary = node, False, False, None


CTX = Context()


class Analyzer:
    def __init__(self, env=None, imports=None, provenance=None, local_functions=None):
        self.env = dict(env or {})
        self.imports = dict(imports or {})
        self.prov = dict(provenance or {})
        self.local_functions = dict(local_functions or {})
        self.returns = []

    # ------------------------------------------------------------------ state
    def fork(self):
        child = Analyzer(self.env, self.imports, self.prov, self.local_functions)
        return child

    def collect(self, *branches):
        for b in branches:
            if b is not None and b is not self:
                self.returns.extend(b.returns)
                b.returns = []

    def join(self, branches, node):
        """Merge the end states of the branches that fall through."""
        live = [b for b in branches if b is not None]
        if not live:
            return
        if len(live) == 1:
            only = live[0]
            self.env, self.prov, self.imports = dict(only.env), dict(only.prov), dict(only.imports)
            self.local_functions = dict(only.local_functions)
            return
        env, prov = {}, {}
        for name in set().union(*(b.env.keys() for b in live)):
            values = [b.env.get(name, MISSING) for b in live]
            first = values[0]
            if first is not MISSING and all(v is not MISSING and v == first for v in values[1:]):
                env[name] = first
            else:
                types = {type_of(v) for v in values if v is not MISSING}
                env[name] = Opaque(name, types.pop() if len(types) == 1 and MISSING not in values else None)
        for name in set().union(*(b.prov.keys() for b in live)):
            tracked = [b.prov.get(name) for b in live if b.prov.get(name) is not None]
            if any(t is AMBIGUOUS for t in tracked) or any(t != tracked[0] for t in tracked[1:]):
                prov[name] = AMBIGUOUS
                issue(node, 'Response provenance of %s differs across branches; field accesses cannot be linked to one operation.' % name, RESPONSE)
            else:
                # May-alias: fields read later are checked against the response they may come from.
                prov[name] = tracked[0]
        self.env, self.prov = env, prov
        self.imports = dict(live[0].imports)
        for b in live[1:]:
            for k in list(self.imports):
                if b.imports.get(k) != self.imports[k]:
                    self.imports.pop(k)

    def havoc(self, names, keep_provenance=True):
        for name in names:
            self.env[name] = Opaque(name)
            self.imports.pop(name, None)
            if not keep_provenance:
                self.prov.pop(name, None)

    # ------------------------------------------------------------- resolution
    def qualified(self, node):
        if isinstance(node, ast.Name):
            if node.id in self.env and node.id not in self.imports:
                return ''
            return self.imports.get(node.id, node.id)
        if isinstance(node, ast.Attribute):
            base = self.qualified(node.value)
            return base + '.' + node.attr if base else ''
        return ''

    def function_info(self, name):
        info = self.local_functions.get(name)
        if info is None and name not in self.env and name not in self.imports:
            info = CTX.functions.get(name)
        return info

    def ensure_analyzed(self, info):
        if info.done or info.running:
            return
        module = CTX.module
        self.analyze_function(info, module.env if module else self.env, module.imports if module else self.imports, module.prov if module else self.prov)

    def analyze_function(self, info, env, imports, provenance=None):
        """Analyze a body once; globals/closure values and response provenance are visible."""
        node = info.node
        info.running = True
        child = Analyzer(env, imports, provenance, self.local_functions)
        all_args = node.args.posonlyargs + node.args.args + node.args.kwonlyargs
        extra = [a for a in (node.args.vararg, node.args.kwarg) if a is not None]
        for arg in all_args + extra:
            child.env[arg.arg] = copy_value(bindings[arg.arg]) if arg.arg in bindings else Opaque(arg.arg)
            child.imports.pop(arg.arg, None)
            child.prov.pop(arg.arg, None)
        record_unused_parameters(node, all_args)
        if isinstance(node, ast.AsyncFunctionDef):
            issue(node, 'Async functions are outside the supported extraction subset.', API)
        child.statements(node.body)
        tracked = [r for r in child.returns if r is not None]
        if any(r is AMBIGUOUS for r in tracked) or any(r != tracked[0] for r in tracked[1:]):
            info.summary = AMBIGUOUS
            issue(node, 'Function %s returns data from different operations.' % node.name, RESPONSE)
        else:
            info.summary = tracked[0] if tracked else None
        info.running, info.done = False, True

    # ------------------------------------------------------------ evaluation
    def value(self, node):
        if node is None:
            return None
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):
            if node.id in self.env:
                return self.env[node.id]
            return Opaque(node.id)
        if isinstance(node, ast.Dict):
            result = {}
            for k, v in zip(node.keys, node.values):
                if k is None:
                    spread = self.value(v)
                    if isinstance(spread, dict):
                        result.update(spread)
                        continue
                    return Opaque(label(node), 'dict')
                key = self.value(k)
                if not isinstance(key, str):
                    return Opaque(label(node), 'dict')
                result[key] = self.value(v)
            return result
        if isinstance(node, (ast.List, ast.Tuple)):
            if any(isinstance(e, ast.Starred) for e in node.elts):
                return Opaque(label(node), 'list')
            return [self.value(v) for v in node.elts]
        if isinstance(node, ast.Subscript):
            obj, key = self.value(node.value), self.value(node.slice)
            if isinstance(obj, (dict, list, str)) and known(key) and not isinstance(node.slice, ast.Slice):
                try:
                    return obj[key]
                except (KeyError, IndexError, TypeError):
                    pass
            return Opaque(label(node))
        if isinstance(node, ast.BinOp):
            left, right = self.value(node.left), self.value(node.right)
            if isinstance(node.op, ast.Add):
                if isinstance(left, (str, Template)) or isinstance(right, (str, Template)):
                    if isinstance(left, (int, float, bool, list, dict)) or isinstance(right, (int, float, bool, list, dict)):
                        return Opaque(label(node))  # a TypeError at runtime; not a URL
                    return make_string([left, right])
            if isinstance(node.op, ast.Mod) and isinstance(left, str) and known(right):
                try:
                    return left % (tuple(right) if isinstance(right, list) else right)
                except (TypeError, ValueError, KeyError):
                    return Opaque(label(node), 'str')
            if known(left) and known(right) and isinstance(left, (int, float)) and isinstance(right, (int, float)):
                try:
                    return eval_binop(node.op, left, right)
                except Exception:
                    pass
            if isinstance(left, (str, Template)) and isinstance(node.op, ast.Mod):
                return Opaque(label(node), 'str')
            return Opaque(label(node))
        if isinstance(node, ast.JoinedStr):
            parts = []
            for part in node.values:
                if isinstance(part, ast.Constant):
                    parts.append(part.value)
                elif isinstance(part, ast.FormattedValue):
                    val = self.value(part.value)
                    plain = part.format_spec is None and part.conversion == -1
                    if plain and isinstance(val, (str, Template)):
                        parts.append(val)
                    elif plain and (val is None or isinstance(val, (int, float, bool))):
                        parts.append(str(val))
                    else:
                        parts.append(Opaque(label(part.value), 'str'))
            return make_string(parts)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            v = self.value(node.operand)
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                return -v if isinstance(node.op, ast.USub) else v
            return Opaque(label(node))
        if isinstance(node, ast.IfExp):
            a, b = self.value(node.body), self.value(node.orelse)
            return a if a == b else Opaque(label(node), type_of(a) if type_of(a) == type_of(b) else None)
        if isinstance(node, ast.NamedExpr):
            return self.value(node.value)
        if isinstance(node, ast.Compare):
            return Opaque(label(node), 'bool')
        if isinstance(node, (ast.ListComp, ast.GeneratorExp)):
            return Opaque(label(node), 'list')
        if isinstance(node, ast.DictComp):
            return Opaque(label(node), 'dict')
        if isinstance(node, ast.Call):
            return self.call_value(node)
        return Opaque(label(node))

    def call_value(self, node):
        """Pure evaluation of a call's result. Side effects are handled by scan()."""
        if id(node) in CTX.calls:
            return Opaque(label(node), 'requests.Response')
        name = self.qualified(node.func)
        args = [self.value(a) for a in node.args]
        kwargs = {kw.arg: self.value(kw.value) for kw in node.keywords if kw.arg}
        if name == 'str' and len(args) == 1:
            v = args[0]
            if isinstance(v, (str, Template)):
                return v
            if known(v) and isinstance(v, (int, float, bool)) or v is None:
                return str(v)
            return Opaque(label(node.args[0]), 'str')
        if name in ('int', 'float', 'bool') and len(args) == 1:
            if known(args[0]):
                try:
                    return {'int': int, 'float': float, 'bool': bool}[name](args[0])
                except (TypeError, ValueError):
                    pass
            return Opaque(label(node), name)
        if name in ('requests.Session', 'requests.session', 'requests.sessions.Session'):
            return Opaque(label(node), 'requests.Session')
        if name in ('requests.auth.HTTPBasicAuth', 'requests.HTTPBasicAuth'):
            return Opaque(label(node), 'requests.auth.HTTPBasicAuth')
        if name == 'len':
            return Opaque(label(node), 'int')
        if name == 'dict' and not args:
            return kwargs if all(kw.arg for kw in node.keywords) else Opaque(label(node), 'dict')
        if name in ('urllib.parse.quote', 'urllib.parse.quote_plus', 'requests.utils.quote'):
            if args and isinstance(args[0], str):
                safe = kwargs.get('safe', args[1] if len(args) > 1 else '/')
                fn = urllib.parse.quote_plus if name.endswith('quote_plus') else urllib.parse.quote
                return fn(args[0], safe=safe) if isinstance(safe, str) else Opaque(label(node), 'str')
            return Opaque(label(node.args[0]) if node.args else label(node), 'str')
        if name == 'urllib.parse.urlencode' and args and known(args[0]):
            try:
                return urllib.parse.urlencode(args[0])
            except (TypeError, ValueError):
                return Opaque(label(node), 'str')
        if name == 'urllib.parse.urljoin' and len(args) == 2 and all(isinstance(a, str) for a in args):
            return urllib.parse.urljoin(args[0], args[1])
        if name in ('os.getenv', 'os.environ.get'):
            return Opaque(label(node), 'str' if len(args) > 1 and isinstance(args[1], str) else None)
        if name in ('json.dumps',):
            return Opaque(label(node), 'str')
        if isinstance(node.func, ast.Attribute):
            receiver = self.value(node.func.value)
            method = node.func.attr
            if isinstance(receiver, dict) and method == 'get' and args and isinstance(args[0], str):
                return receiver.get(args[0], args[1] if len(args) > 1 else kwargs.get('default'))
            if isinstance(receiver, dict) and method == 'copy':
                return dict(receiver)
            if isinstance(receiver, str):
                return self.string_method(node, receiver, method, args, kwargs)
            if isinstance(receiver, Template):
                return self.template_method(node, receiver, method, args)
        return Opaque(label(node))

    def string_method(self, node, receiver, method, args, kwargs):
        if method == 'replace' and len(args) >= 2 and isinstance(args[0], str) and args[0]:
            if isinstance(args[1], str):
                return receiver.replace(args[0], args[1])
            pieces = receiver.split(args[0])
            parts = [pieces[0]]
            for piece in pieces[1:]:
                parts.extend([args[1] if isinstance(args[1], (Template, Opaque)) else Opaque(label(node.args[1]), 'str'), piece])
            return make_string(parts)
        if method == 'format':
            return self.format_string(node, receiver, args, kwargs)
        if method in ('strip', 'rstrip', 'lstrip', 'lower', 'upper', 'title', 'capitalize') and all(isinstance(a, str) for a in args):
            return getattr(receiver, method)(*args)
        if method == 'join' and len(args) == 1 and isinstance(args[0], list) and all(isinstance(a, str) for a in args[0]):
            return receiver.join(args[0])
        if method in ('join', 'replace', 'format', 'strip', 'rstrip', 'lstrip', 'lower', 'upper'):
            return Opaque(label(node), 'str')
        return Opaque(label(node))

    def template_method(self, node, receiver, method, args):
        if method == 'replace' and len(args) >= 2 and isinstance(args[0], str) and args[0]:
            parts = []
            for part in receiver.parts:
                if isinstance(part, str) and args[0] in part:
                    pieces = part.split(args[0])
                    parts.append(pieces[0])
                    for piece in pieces[1:]:
                        parts.extend([args[1] if isinstance(args[1], (str, Template, Opaque)) else Opaque(label(node.args[1]), 'str'), piece])
                else:
                    parts.append(part)
            return make_string(parts)
        if method in ('rstrip', 'strip') and receiver.parts and isinstance(receiver.parts[-1], str) and all(isinstance(a, str) for a in args):
            return make_string(list(receiver.parts[:-1]) + [receiver.parts[-1].rstrip(*args)]) if method == 'rstrip' else Opaque(label(node), 'str')
        return Opaque(label(node), 'str')

    def format_string(self, node, template, args, kwargs):
        parts, auto = [], 0
        try:
            for literal, field, spec, conversion in string.Formatter().parse(template):
                parts.append(literal)
                if field is None:
                    continue
                if field == '':
                    key, auto = auto, auto + 1
                elif field.isdigit():
                    key = int(field)
                else:
                    key = field
                if isinstance(key, int):
                    val = args[key] if key < len(args) else Opaque(label(node), 'str')
                elif key.isidentifier():
                    val = kwargs.get(key, Opaque(key, 'str'))
                else:
                    val = Opaque(key, 'str')
                if spec or conversion or not (isinstance(val, (str, Template)) or known(val) and isinstance(val, (int, float, bool))):
                    val = Opaque(field or str(key), 'str')
                parts.append(val if isinstance(val, (str, Template, Opaque)) else str(val))
        except (ValueError, IndexError):
            return Opaque(label(node), 'str')
        return make_string(parts)

    # ------------------------------------------------------------ provenance
    def origin(self, node):
        """(call_id, None) for a raw Response, (call_id, path) for decoded JSON data."""
        if isinstance(node, ast.Name):
            return self.prov.get(node.id)
        if isinstance(node, ast.NamedExpr):
            return self.origin(node.value)
        if isinstance(node, ast.Call):
            if id(node) in CTX.calls:
                return (CTX.calls[id(node)], None)
            if isinstance(node.func, ast.Attribute):
                source = self.origin(node.func.value)
                attr = node.func.attr
                if source is AMBIGUOUS:
                    return AMBIGUOUS if attr in ('json', 'get', 'copy') else None
                if source and source[1] is None and attr == 'json':
                    return (source[0], [])
                if source and source[1] is not None and attr == 'get' and node.args:
                    key = self.value(node.args[0])
                    return (source[0], source[1] + [key if isinstance(key, str) else '*'])
                if source and source[1] is not None and attr == 'copy':
                    return source
            if isinstance(node.func, ast.Name):
                if node.func.id in ('list', 'sorted', 'reversed', 'dict', 'tuple') and len(node.args) == 1:
                    return self.origin(node.args[0])
                info = self.function_info(node.func.id)
                if info is not None:
                    self.ensure_analyzed(info)
                    return info.summary
            return None
        if isinstance(node, ast.Subscript):
            source = self.origin(node.value)
            if source is AMBIGUOUS:
                return AMBIGUOUS
            if source and source[1] is not None:
                if isinstance(node.slice, ast.Slice):
                    return source
                key = self.value(node.slice)
                if isinstance(key, bool) or not isinstance(key, (str, int)):
                    return (source[0], source[1] + ['*'])
                return (source[0], source[1] + [key])
            return None
        if isinstance(node, ast.IfExp):
            return self.merge_origins([self.origin(node.body), self.origin(node.orelse)], node)
        if isinstance(node, ast.BoolOp):
            return self.merge_origins([self.origin(v) for v in node.values], node)
        return None

    def merge_origins(self, origins, node):
        tracked = [o for o in origins if o is not None]
        if not tracked:
            return None
        if any(o is AMBIGUOUS for o in tracked) or any(o != tracked[0] for o in tracked[1:]):
            issue(node, 'Expression may hold data from different operations.', RESPONSE)
            return AMBIGUOUS
        return tracked[0]

    # --------------------------------------------------------------- scanning
    def scan(self, node):
        if node is None:
            return
        if isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)):
            self.comprehension(node)
            return
        if isinstance(node, ast.Lambda):
            child = self.fork()
            for arg in node.args.posonlyargs + node.args.args + node.args.kwonlyargs:
                child.env[arg.arg] = Opaque(arg.arg)
                child.prov.pop(arg.arg, None)
            child.scan(node.body)
            return
        if isinstance(node, ast.Await):
            issue(node, 'Await expressions are outside the supported extraction subset.', API)
        for child in ast.iter_child_nodes(node):
            self.scan(child)
        if isinstance(node, ast.NamedExpr):
            self.assign(node.target, node.value)
        if isinstance(node, ast.Subscript) and isinstance(node.ctx, ast.Load):
            source = self.origin(node)
            if source is AMBIGUOUS:
                issue(node, 'Response field read from data with ambiguous provenance.', RESPONSE)
            elif source and source[1]:
                add(node, 'output_field', call_id=source[0], field=source[1][-1], path=source[1])
        if isinstance(node, ast.Call):
            self.call(node)

    def comprehension(self, node):
        child = self.fork()
        for gen in node.generators:
            child.scan(gen.iter)
            source = child.origin(gen.iter)
            child.bind_iteration(gen.target, gen.iter, source)
            for cond in gen.ifs:
                child.scan(cond)
        if isinstance(node, ast.DictComp):
            child.scan(node.key)
            child.scan(node.value)
        else:
            child.scan(node.elt)

    def bind_iteration(self, target, iterator, source):
        """Bind a for/comprehension target, retaining response-item provenance."""
        items_call = isinstance(iterator, ast.Call) and isinstance(iterator.func, ast.Attribute) \
            and iterator.func.attr in ('items', 'values', 'keys') and not iterator.args
        if items_call:
            base = self.origin(iterator.func.value)
            if base is AMBIGUOUS:
                issue(iterator, 'Iteration over data with ambiguous provenance.', RESPONSE)
                base = None
            names = target.elts if isinstance(target, ast.Tuple) else [target]
            for i, t in enumerate(names):
                if isinstance(t, ast.Name):
                    self.env[t.id] = Opaque(t.id)
                    self.imports.pop(t.id, None)
                    is_value = iterator.func.attr == 'values' or (iterator.func.attr == 'items' and i == 1)
                    if base and base[1] is not None and is_value:
                        self.prov[t.id] = (base[0], base[1] + ['*'])
                    else:
                        self.prov.pop(t.id, None)
                else:
                    self.assign(t, None)
            return
        if isinstance(iterator, ast.Call) and isinstance(iterator.func, ast.Name) and iterator.func.id == 'enumerate' \
                and iterator.args and isinstance(target, ast.Tuple) and len(target.elts) == 2:
            inner = self.origin(iterator.args[0])
            self.bind_iteration(target.elts[0], ast.Constant(0), None)
            self.bind_iteration(target.elts[1], iterator.args[0], inner)
            return
        if source is AMBIGUOUS:
            issue(iterator, 'Iteration over data with ambiguous provenance.', RESPONSE)
            source = None
        if isinstance(target, ast.Name):
            self.env[target.id] = Opaque(target.id)
            self.imports.pop(target.id, None)
            if source and source[1] is not None:
                self.prov[target.id] = (source[0], source[1] + [0])
            else:
                self.prov.pop(target.id, None)
        else:
            if source and source[1] is not None:
                issue(target, 'Destructuring items of a response is outside the supported subset.', RESPONSE)
            for n in ast.walk(target):
                if isinstance(n, ast.Name):
                    self.env[n.id] = Opaque(n.id)
                    self.prov.pop(n.id, None)

    def call(self, node):
        name = self.qualified(node.func)
        method = name[len('requests.'):] if name.startswith('requests.') else ''
        if method.startswith('api.'):
            method = method[4:]
        if name == 'requests' or name.startswith('requests.'):
            add(node, 'method_call', library='requests', method=name[len('requests.'):] if name.startswith('requests.') else '')
        if method in HTTP or method == 'request':
            self.http(node, method)
            return
        if name in DYNAMIC_CODE or (isinstance(node.func, ast.Name) and node.func.id in DYNAMIC_CODE and node.func.id not in self.env):
            issue(node, 'Dynamic code or attribute access is unsupported.', ALL)
            return
        if name.startswith(OTHER_HTTP_CLIENTS):
            issue(node, 'Only direct requests calls are supported; other HTTP clients are unresolved: ' + name, API)
            return
        if name.startswith('requests.'):
            return  # exceptions, auth helpers, adapters and utilities: recorded, no HTTP claim
        if name:  # a callable resolved by name: module function, import or builtin
            if isinstance(node.func, ast.Name):
                info = self.function_info(node.func.id)
                if info is not None:
                    self.ensure_analyzed(info)
                    for arg in list(node.args) + [kw.value for kw in node.keywords]:
                        source = self.origin(arg)
                        if source is AMBIGUOUS or source and source[1] is not None:
                            issue(node, 'Response data is passed into user-defined function %s; field accesses inside it are not linked.' % node.func.id, RESPONSE)
                    self.havoc_arguments(node)
                    return
            if name in PURE or name in BUILTIN_EXCEPTIONS or name.split('.')[-1] in BUILTIN_EXCEPTIONS:
                return
            self.havoc_arguments(node)
            for arg in node.args:
                if isinstance(arg, ast.Lambda) and any(self.origin(a) is not None for a in node.args if a is not arg):
                    issue(node, 'A lambda applied to response data is outside the supported subset.', RESPONSE)
            return
        if isinstance(node.func, ast.Attribute):
            self.method_call(node)
            return
        self.havoc_arguments(node)

    def havoc_arguments(self, node):
        """An unknown callee may mutate container arguments; forget their contents."""
        for arg in list(node.args) + [kw.value for kw in node.keywords]:
            if isinstance(arg, ast.Starred):
                arg = arg.value
            if isinstance(arg, ast.Name) and isinstance(self.env.get(arg.id), (dict, list)):
                self.env[arg.id] = Opaque(arg.id, type_of(self.env[arg.id]))

    def method_call(self, node):
        receiver_node, attr = node.func.value, node.func.attr
        source = self.origin(receiver_node)
        if source is AMBIGUOUS:
            if attr == 'get':
                issue(node, 'Response field read from data with ambiguous provenance.', RESPONSE)
            return
        if source is not None:
            if source[1] is None:  # raw Response
                if attr == 'json' and (node.args or node.keywords):
                    issue(node, 'Custom JSON decoding arguments can change response shape.', RESPONSE)
                return
            if attr == 'get' and node.args:
                add(node, 'output_field', call_id=source[0], field=self.origin(node)[1][-1], path=self.origin(node)[1], optional_access=True)
            elif attr == 'pop' and node.args:
                key = self.value(node.args[0])
                path = source[1] + [key if isinstance(key, str) else '*']
                add(node, 'output_field', call_id=source[0], field=path[-1], path=path, optional_access=len(node.args) > 1)
                self.forget_response_data(receiver_node, node)
            elif attr in MUTATORS:
                self.forget_response_data(receiver_node, node)
            return
        receiver = self.value(receiver_node)
        if isinstance(receiver_node, ast.Name) and receiver_node.id in self.env and attr in MUTATORS:
            self.mutate(receiver_node.id, attr, node)
            return
        if attr in HTTP or attr == 'request':
            if isinstance(receiver, Opaque) and receiver.type == 'requests.Session':
                issue(node, 'Session-based requests are outside the supported subset.', API)
            elif isinstance(receiver, (Opaque, Template)) and not self.qualified(receiver_node):
                if attr != 'get' or self.looks_like_request(node):
                    issue(node, 'Unresolved HTTP-like call receiver: ' + label(node.func), API)
        if not self.qualified(receiver_node) and not isinstance(receiver, (str, Template, dict)):
            self.havoc_arguments(node)

    def looks_like_request(self, node):
        if any(kw.arg in REQUEST_KWARGS - {'url'} for kw in node.keywords):
            return True
        if node.args:
            first = self.value(node.args[0])
            text = first if isinstance(first, str) else first.parts[0] if isinstance(first, Template) and isinstance(first.parts[0], str) else ''
            return text.startswith(('http://', 'https://', '/'))
        return False

    def forget_response_data(self, receiver_node, node):
        issue(node, 'Response data is mutated; later field reads may not come from the API.', RESPONSE)
        if isinstance(receiver_node, ast.Name):
            self.prov[receiver_node.id] = AMBIGUOUS

    def mutate(self, name, attr, node):
        """Apply a container mutation (copy-on-write) or forget the container."""
        current = self.env[name]
        args = [self.value(a) for a in node.args]
        kwargs = {kw.arg: self.value(kw.value) for kw in node.keywords if kw.arg}
        new = MISSING
        if isinstance(current, dict):
            if attr == 'update' and not any(kw.arg is None for kw in node.keywords):
                if not args or (len(args) == 1 and isinstance(args[0], dict)):
                    new = {**current, **(args[0] if args else {}), **kwargs}
            elif attr == 'setdefault' and args and isinstance(args[0], str):
                new = dict(current)
                new.setdefault(args[0], args[1] if len(args) > 1 else None)
            elif attr == 'pop' and args and isinstance(args[0], str):
                new = {k: v for k, v in current.items() if k != args[0]}
            elif attr == 'clear':
                new = {}
        elif isinstance(current, list):
            if attr == 'append' and len(args) == 1:
                new = current + [args[0]]
            elif attr == 'extend' and len(args) == 1 and isinstance(args[0], list):
                new = current + list(args[0])
            elif attr == 'clear':
                new = []
        if new is MISSING:
            new = Opaque(name, type_of(current))
        self.set_container(name, new)

    def set_container(self, name, new):
        old = self.env.get(name)
        for other, value in list(self.env.items()):
            if other != name and value is old and isinstance(old, (dict, list)):
                self.env[other] = new  # keep aliases consistent
            elif other != name and isinstance(value, (dict, list)) and contains(value, old):
                self.env[other] = Opaque(other, type_of(value))
        self.env[name] = new

    def http(self, node, method):
        args = list(node.args)
        kwargs = {kw.arg: kw.value for kw in node.keywords if kw.arg}
        expanded = any(kw.arg is None for kw in node.keywords)
        if expanded:
            issue(node, 'Expanded request keyword arguments are unsupported.', API)
        if method == 'request':
            method_node = kwargs.get('method') or (args.pop(0) if args else None)
            method_value = self.value(method_node)
        else:
            method_value = method.upper()
        url_node = kwargs.get('url') or (args.pop(0) if args else None)
        url = self.value(url_node)
        for key, val in zip(POSITIONAL.get(method, []), args):
            if key in kwargs:
                issue(node, 'Duplicate request argument.', REQUEST)
            kwargs[key] = val
        if len(args) > len(POSITIONAL.get(method, [])):
            issue(node, 'Unsupported positional request arguments.', REQUEST)
        call_id = 'call_%s_%s' % (node.lineno, node.col_offset)
        CTX.calls[id(node)] = call_id
        request = {}
        for via in ('params', 'json', 'data', 'headers', 'cookies', 'auth'):
            if via in kwargs:
                value = self.value(kwargs[via])
                request[via] = {'provided': True, 'known': known(value), 'value': public(value),
                                'keys_known': isinstance(value, dict), 'shape': encode(value),
                                'fields': {k: {'known': known(v), 'value': public(v), 'shape': encode(v)} for k, v in value.items()} if isinstance(value, dict) else {}}
                if isinstance(value, dict):
                    for field, val in value.items():
                        add(node, 'input_field', call_id=call_id, field=field, via=via, known=known(val), value=public(val))
        method_ok = isinstance(method_value, str) and method_value.upper() in {m.upper() for m in HTTP}
        url_ok = isinstance(url, str) or origin_known(url)
        if not url_ok or not method_ok:
            issue(node, 'Dynamic endpoint or HTTP method requires explicit input_bindings.', API)
        add(node, 'endpoint', call_id=call_id, endpoint=url if isinstance(url, str) else None,
            endpoint_template=encode(url) if isinstance(url, Template) else None,
            http_method=method_value.upper() if isinstance(method_value, str) else None,
            resolved=url_ok and method_ok, request=request, request_complete=not expanded)
        if 'verify' in kwargs and self.value(kwargs['verify']) is False:
            issue(node, 'TLS verification disabled; outside supported verification scope.', ['contextual'])
        if 'files' in kwargs:
            issue(node, 'Multipart file uploads are outside the supported request subset.', REQUEST)
        if any(k not in REQUEST_KWARGS | {'files'} for k in kwargs):
            issue(node, 'Unsupported requests keyword argument.', REQUEST)

    # -------------------------------------------------------------- binding
    def assign(self, target, node, value=MISSING):
        if value is MISSING:
            value = self.value(node) if node is not None else Opaque(label(target))
        if isinstance(target, ast.Name):
            self.env[target.id] = value
            self.imports.pop(target.id, None)
            self.local_functions.pop(target.id, None)
            source = self.origin(node) if node is not None else None
            if source is not None:
                self.prov[target.id] = source
            else:
                self.prov.pop(target.id, None)
        elif isinstance(target, (ast.Tuple, ast.List)):
            elts = target.elts
            if node is not None and isinstance(node, (ast.Tuple, ast.List)) and len(node.elts) == len(elts) \
                    and not any(isinstance(e, ast.Starred) for e in elts + node.elts):
                values = [self.value(e) for e in node.elts]
                for t, n, v in zip(elts, node.elts, values):
                    self.assign(t, n, v)
                return
            source = self.origin(node) if node is not None else None
            if source is AMBIGUOUS or source and source[1] is not None:
                issue(target, 'Destructuring response data is outside the supported subset.', RESPONSE)
            for t in elts:
                self.assign(t.value if isinstance(t, ast.Starred) else t, None, Opaque(label(t)))
        elif isinstance(target, ast.Subscript):
            self.assign_item(target, value)
        elif isinstance(target, ast.Attribute):
            root = target
            while isinstance(root, (ast.Attribute, ast.Subscript)):
                root = root.value
            if isinstance(root, ast.Name) and isinstance(self.env.get(root.id), (dict, list)):
                self.set_container(root.id, Opaque(root.id, type_of(self.env[root.id])))
        elif isinstance(target, ast.Starred):
            self.assign(target.value, None, Opaque(label(target)))

    def assign_item(self, target, value):
        """d[k] = v on a tracked container (copy-on-write); otherwise forget the container."""
        chain = []
        node = target
        while isinstance(node, ast.Subscript):
            chain.append(node.slice)
            node = node.value
        if not isinstance(node, ast.Name):
            return
        name = node.id
        source = self.prov.get(name)
        if source is not None and name not in self.env or source is not None and not isinstance(self.env.get(name), (dict, list)):
            self.forget_response_data(node, target)
            return
        keys = [self.value(k) for k in reversed(chain)]
        root = self.env.get(name)

        def update(container, path):
            if not path:
                return value
            key = path[0]
            if isinstance(container, dict) and isinstance(key, str):
                new = dict(container)
                new[key] = update(container.get(key, {}) if len(path) > 1 else None, path[1:])
                return new
            if isinstance(container, list) and isinstance(key, int) and -len(container) <= key < len(container):
                new = list(container)
                new[key] = update(container[key], path[1:])
                return new
            return MISSING

        new = update(root, keys) if isinstance(root, (dict, list)) else MISSING
        if new is MISSING or contains_missing(new):
            new = Opaque(name, type_of(root) if root is not None else None)
        if name in self.env or isinstance(new, (dict, list)):
            self.set_container(name, new)

    # ------------------------------------------------------------ statements
    def statements(self, statements):
        """Analyze a block; return True when it cannot fall through."""
        for node in statements:
            if self.statement(node):
                return True
        return False

    def statement(self, node):
        if isinstance(node, ast.Import):
            for alias in node.names:
                self.imports[alias.asname or alias.name.split('.')[0]] = alias.name if alias.asname else alias.name.split('.')[0]
                self.env.pop(alias.asname or alias.name.split('.')[0], None)
                top = alias.name.split('.')[0]
                add(node, 'import', library=alias.name, stdlib=top in getattr(sys, 'stdlib_module_names', set()), local=False)
            return False
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ''
            for alias in node.names:
                if alias.name == '*':
                    issue(node, 'Wildcard import is unsupported.', ALL)
                else:
                    self.imports[alias.asname or alias.name] = (mod + '.' if mod else '') + alias.name
                    self.env.pop(alias.asname or alias.name, None)
                add(node, 'import', library=mod, stdlib=mod.split('.')[0] in getattr(sys, 'stdlib_module_names', set()), local=node.level > 0)
            return False
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for decorator in node.decorator_list:
                self.scan(decorator)
            self.env.pop(node.name, None)
            self.imports.pop(node.name, None)
            self.prov.pop(node.name, None)
            registered = CTX.functions.get(node.name)
            if self is CTX.module and registered is not None and registered.node is node:
                return False  # analyzed on first call, or at module end with final globals
            info = FunctionInfo(node)
            self.local_functions[node.name] = info
            self.analyze_function(info, self.env, self.imports, self.prov)
            return False
        if isinstance(node, ast.ClassDef):
            issue(node, 'Classes are outside the supported extraction subset.', API)
            for stmt in node.body:
                if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    self.analyze_function(FunctionInfo(stmt), self.env, self.imports, self.prov)
            self.env.pop(node.name, None)
            return False
        if isinstance(node, ast.Assign):
            self.scan(node.value)
            value = self.value(node.value)
            for target in node.targets:
                self.scan_target(target)
                self.assign(target, node.value, value)
            return False
        if isinstance(node, ast.AnnAssign):
            if node.value is not None:
                self.scan(node.value)
                self.scan_target(node.target)
                self.assign(node.target, node.value)
            return False
        if isinstance(node, ast.AugAssign):
            self.scan(node.value)
            self.scan_target(node.target)
            if isinstance(node.target, ast.Name):
                combined = ast.BinOp(left=ast.Name(id=node.target.id, ctx=ast.Load()), op=node.op, right=node.value)
                ast.copy_location(combined, node)
                value = self.value(combined)
                if self.prov.get(node.target.id) is not None:
                    self.forget_response_data(node.target, node)
                self.env[node.target.id] = value
                self.imports.pop(node.target.id, None)
            else:
                self.assign(node.target, None, Opaque(label(node.target)))
            return False
        if isinstance(node, (ast.Expr,)):
            self.scan(node.value)
            return False
        if isinstance(node, ast.Return):
            self.scan(node.value)
            if node.value is not None:
                self.returns.append(self.origin(node.value))
            return True
        if isinstance(node, ast.Raise):
            self.scan(node.exc)
            self.scan(node.cause)
            return True
        if isinstance(node, (ast.Break, ast.Continue)):
            return True
        if isinstance(node, ast.Pass):
            return False
        if isinstance(node, ast.If):
            self.scan(node.test)
            body, orelse = self.fork(), self.fork()
            body_ends = body.statements(node.body)
            else_ends = orelse.statements(node.orelse)
            self.collect(body, orelse)
            self.join([None if body_ends else body, None if else_ends else orelse], node)
            return body_ends and else_ends
        if isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
            if isinstance(node, ast.AsyncFor):
                issue(node, 'Async iteration is outside the supported extraction subset.', API)
            self.loop(node)
            return False
        if isinstance(node, (ast.Try, getattr(ast, 'TryStar', ast.Try))):
            return self.try_statement(node)
        if isinstance(node, (ast.With, ast.AsyncWith)):
            if isinstance(node, ast.AsyncWith):
                issue(node, 'Async context managers are outside the supported extraction subset.', API)
            for item in node.items:
                self.scan(item.context_expr)
                if item.optional_vars is not None:
                    source = self.origin(item.context_expr)
                    name = self.qualified(item.context_expr.func) if isinstance(item.context_expr, ast.Call) else ''
                    typed = Opaque(label(item.optional_vars), 'requests.Session' if name in ('requests.Session', 'requests.session') else None)
                    self.assign(item.optional_vars, None, typed)
                    if isinstance(item.optional_vars, ast.Name) and source is not None:
                        self.prov[item.optional_vars.id] = source
            return self.statements(node.body)
        if isinstance(node, ast.Delete):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.env.pop(target.id, None)
                    self.prov.pop(target.id, None)
                elif isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name) and isinstance(self.env.get(target.value.id), dict):
                    key = self.value(target.slice)
                    current = self.env[target.value.id]
                    self.set_container(target.value.id, {k: v for k, v in current.items() if k != key} if isinstance(key, str) else Opaque(target.value.id, 'dict'))
                elif isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name) and self.prov.get(target.value.id) is not None:
                    self.forget_response_data(target.value, node)
            return False
        if isinstance(node, ast.Assert):
            self.scan(node.test)
            self.scan(node.msg)
            return False
        if isinstance(node, (ast.Global, ast.Nonlocal)):
            issue(node, 'global/nonlocal rebinding is outside the supported extraction subset.', API)
            self.havoc(node.names, keep_provenance=False)
            return False
        if isinstance(node, getattr(ast, 'Match', ())):
            issue(node, 'Match statements are outside the supported extraction subset.', API)
            self.scan(node.subject)
            branches = []
            for case in node.cases:
                branch = self.fork()
                ends = branch.statements(case.body)
                self.collect(branch)
                branches.append(None if ends else branch)
            self.join(branches + [self.fork()], node)
            return False
        if isinstance(node, getattr(ast, 'TypeAlias', ())):
            return False
        issue(node, 'Unsupported statement: ' + type(node).__name__, API)
        return False

    def scan_target(self, target):
        """Scan index expressions in an assignment target without recording field reads."""
        if isinstance(target, ast.Subscript):
            self.scan_target(target.value)
            self.scan(target.slice)
        elif isinstance(target, ast.Attribute):
            self.scan_target(target.value)
        elif isinstance(target, (ast.Tuple, ast.List)):
            for t in target.elts:
                self.scan_target(t)

    def loop(self, node):
        body_nodes = node.body + node.orelse
        changed = assigned_names(body_nodes)
        if isinstance(node, (ast.For, ast.AsyncFor)):
            self.scan(node.iter)
            changed |= {n.id for n in ast.walk(node.target) if isinstance(n, ast.Name)}
        before = {name: self.prov.get(name) for name in changed}
        # Any iteration may see values from an earlier iteration: forget changed values.
        for name in changed:
            if name in self.env:
                self.env[name] = Opaque(name, type_of(self.env[name]))
        if isinstance(node, ast.While):
            self.scan(node.test)
        entry = self.fork()
        body = self.fork()
        if isinstance(node, (ast.For, ast.AsyncFor)):
            body.bind_iteration(node.target, node.iter, self.origin(node.iter))
        body.statements(node.body)
        self.collect(body)
        for name in changed:
            start, end = before.get(name), body.prov.get(name)
            if start is not None and end is not None and start != end:
                issue(node, 'Response provenance of %s changes across loop iterations.' % name, RESPONSE)
                body.prov[name] = AMBIGUOUS
        self.join([entry, body], node)
        if node.orelse:
            self.statements(node.orelse)

    def try_statement(self, node):
        before = self.fork()
        body = self.fork()
        body_ends = body.statements(node.body)
        changed = assigned_names(node.body)
        ends = []
        if not body_ends:
            else_ends = body.statements(node.orelse) if node.orelse else False
            ends.append(None if else_ends else body)
        self.collect(body)
        for handler in node.handlers:
            h = before.fork()
            # A handler may start after any prefix of the body ran.
            for name in changed:
                if name in h.env or name in body.env:
                    h.env[name] = Opaque(name)
                if body.prov.get(name) is not None and h.prov.get(name) != body.prov.get(name):
                    h.prov[name] = body.prov[name] if h.prov.get(name) is None else AMBIGUOUS
            if handler.name:
                h.env[handler.name] = Opaque(handler.name)
                h.prov.pop(handler.name, None)
            handler_ends = h.statements(handler.body)
            self.collect(h)
            ends.append(None if handler_ends else h)
        reachable = any(e is not None for e in ends)
        self.join(ends if reachable else [before], node)
        final_ends = self.statements(node.finalbody) if node.finalbody else False
        return final_ends or not reachable


def contains(container, target):
    if container is target:
        return True
    if isinstance(container, dict):
        return any(contains(v, target) for v in container.values())
    if isinstance(container, list):
        return any(contains(v, target) for v in container)
    return False


def contains_missing(value):
    if value is MISSING:
        return True
    if isinstance(value, dict):
        return any(contains_missing(v) for v in value.values())
    if isinstance(value, list):
        return any(contains_missing(v) for v in value)
    return False


def eval_binop(op, left, right):
    if isinstance(op, ast.Add):
        return left + right
    if isinstance(op, ast.Sub):
        return left - right
    if isinstance(op, ast.Mult):
        return left * right
    if isinstance(op, ast.Div):
        return left / right
    if isinstance(op, ast.FloorDiv):
        return left // right
    if isinstance(op, ast.Mod):
        return left % right
    raise ValueError('unsupported')


def record_unused_parameters(node, all_args):
    referenced = set()
    reflective = False
    for stmt in node.body:
        for descendant in ast.walk(stmt):
            if isinstance(descendant, ast.Name):
                referenced.add(descendant.id)
                if descendant.id in ('locals', 'vars'):
                    reflective = True
    if reflective:
        return
    for arg in all_args:
        if arg.arg in ('self', 'cls') or arg.arg in referenced:
            continue
        # Pyright ranges are 0-indexed lines; ast lines are 1-indexed.
        unused_parameters.append({'name': arg.arg, 'line': arg.lineno - 1,
                                  'start_character': arg.col_offset, 'end_character': arg.col_offset + len(arg.arg)})


def prepass(tree):
    """Register module-level functions so calls resolve before definitions."""
    counts = {}
    for stmt in tree.body:
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
            counts[stmt.name] = counts.get(stmt.name, 0) + 1
    for stmt in tree.body:
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)) and counts[stmt.name] == 1:
            CTX.functions[stmt.name] = FunctionInfo(stmt)


try:
    tree = ast.parse(code)
    for token in tokenize.generate_tokens(io.StringIO(code).readline):
        if token.type == tokenize.COMMENT and ('pyright:' in token.string.lower() or 'type: ignore' in token.string.lower()):
            issue(types.SimpleNamespace(lineno=token.start[0]), 'Candidate contains checker suppression/configuration directives.', IDENTIFIER)
    module = Analyzer()
    CTX.module = module
    prepass(tree)
    module.statements(tree.body)
    for info in list(CTX.functions.values()):
        if not info.done:
            module.analyze_function(info, module.env, module.imports, module.prov)
    print(json.dumps({
        'claims': claims,
        'complete': not issues,
        'issues': issues,
        'unused_parameters': unused_parameters,
    }))
except (SyntaxError, ValueError) as e:
    print(json.dumps({'claims': [], 'complete': False, 'issues': [], 'unused_parameters': [], 'error': str(e)}))
