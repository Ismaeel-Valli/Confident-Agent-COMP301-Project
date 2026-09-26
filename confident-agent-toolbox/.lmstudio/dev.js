"use strict";
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __esm = (fn, res, err) => function __init() {
  if (err) throw err[0];
  try {
    return fn && (res = (0, fn[__getOwnPropNames(fn)[0]])(fn = 0)), res;
  } catch (e) {
    throw err = [e], e;
  }
};
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));

// src/config.ts
var import_sdk, pluginConfigSchematics;
var init_config = __esm({
  "src/config.ts"() {
    "use strict";
    import_sdk = require("@lmstudio/sdk");
    pluginConfigSchematics = (0, import_sdk.createConfigSchematics)().field("enableConfidenceAgentTools", "boolean", {
      displayName: "Confident Agent tools",
      subtitle: "Expose verify_candidate and the inspection tools (claim extraction, six layer checks, scoring and report)."
    }, true).field("allowPyrightExecution", "boolean", {
      displayName: "Allow Pyright",
      subtitle: "Run the pinned Pyright checker on candidate code. Static analysis only: candidate code is never executed. Required for the identifier layer."
    }, true).field("pythonExecutable", "string", {
      displayName: "Verification Python",
      subtitle: "Interpreter for claim extraction and Pyright import resolution, e.g. C:\\...\\confident-agent-toolbox\\.venv\\Scripts\\python.exe. Empty uses the CONFIDENCE_PYTHON environment variable, then python."
    }, "").field("workspacePath", "string", {
      displayName: "save_code folder",
      subtitle: "Folder where save_code writes files. Empty uses %USERPROFILE%\\confident-agent-workspace."
    }, "").build();
  }
});

// src/extractorScript.ts
var EXTRACTION_SCRIPT;
var init_extractorScript = __esm({
  "src/extractorScript.ts"() {
    "use strict";
    EXTRACTION_SCRIPT = `"""Conservative static extraction. Never imports or executes the candidate.\r
\r
Values are abstract. A value is either a statically known Python literal\r
(str/int/float/bool/None, a dict with string keys, a list), an Opaque runtime\r
value (optionally with a statically evident Python type), or a Template: a\r
string whose literal parts are known and whose holes are runtime values, such\r
as f"https://host/users/{user_id}". Unknown values are never guessed, and a\r
container that is changed in a way the analysis cannot follow becomes Opaque\r
rather than keeping a stale value.\r
\r
Each extraction issue lists the verification layers whose claim inventory it\r
can make incomplete ("affects"). Other layers keep their evidence.\r
"""\r
import ast\r
import builtins\r
import io\r
import json\r
import string\r
import sys\r
import tokenize\r
import types\r
import urllib.parse\r
\r
payload = json.load(sys.stdin)\r
code = payload.get('code', '')\r
bindings = payload.get('input_bindings', {}) or {}\r
\r
ALL = ['interface', 'identifier', 'access_point', 'input_contract', 'output_contract', 'contextual']\r
API = ['access_point', 'input_contract', 'output_contract', 'contextual']\r
REQUEST = ['input_contract', 'contextual']\r
RESPONSE = ['output_contract']\r
IDENTIFIER = ['identifier']\r
\r
HTTP = {'get', 'post', 'put', 'patch', 'delete', 'head', 'options'}\r
# requests.<verb>(url, <positional>...) as defined by requests.api.\r
POSITIONAL = {'get': ['params'], 'post': ['data', 'json'], 'put': ['data'], 'patch': ['data'],\r
              'delete': [], 'head': [], 'options': [], 'request': []}\r
REQUEST_KWARGS = {'url', 'method', 'params', 'json', 'data', 'headers', 'cookies', 'auth',\r
                  'timeout', 'allow_redirects', 'verify', 'stream', 'proxies', 'cert'}\r
OTHER_HTTP_CLIENTS = ('httpx.', 'aiohttp.', 'urllib.request.', 'urllib3.', 'http.client.', 'pycurl.')\r
# Calls that neither mutate their arguments nor perform HTTP requests.\r
PURE = {\r
    'print', 'len', 'str', 'int', 'float', 'bool', 'bytes', 'bytearray', 'complex', 'frozenset',\r
    'object', 'slice', 'memoryview', 'format', 'isinstance', 'issubclass', 'hasattr', 'callable',\r
    'type', 'id', 'repr', 'hash', 'dir', 'list', 'dict', 'set', 'tuple', 'range', 'enumerate',\r
    'zip', 'iter', 'next', 'reversed', 'sorted', 'min', 'max', 'sum', 'abs', 'round', 'pow',\r
    'divmod', 'bin', 'hex', 'oct', 'chr', 'ord', 'any', 'all', 'super', 'property',\r
    'classmethod', 'staticmethod',\r
    'json.dumps', 'json.loads', 'json.dump', 'os.getenv', 'os.environ.get',\r
    'urllib.parse.quote', 'urllib.parse.quote_plus', 'urllib.parse.unquote',\r
    'urllib.parse.urlencode', 'urllib.parse.urljoin', 'urllib.parse.urlparse',\r
    'time.sleep', 'time.time', 'sys.exit', 'logging.debug', 'logging.info', 'logging.warning',\r
    'logging.error', 'logging.exception', 'logging.critical', 'logging.getLogger',\r
    'datetime.datetime.now', 'datetime.date.today',\r
}\r
BUILTIN_EXCEPTIONS = {n for n in dir(builtins) if n.endswith(('Error', 'Exception', 'Warning', 'Exit', 'Interrupt'))}\r
MUTATORS = {'update', 'setdefault', 'pop', 'popitem', 'clear', 'append', 'extend', 'insert', 'remove', 'sort', 'reverse'}\r
DYNAMIC_CODE = {'getattr', 'setattr', 'delattr', 'eval', 'exec', 'compile', '__import__', 'globals', 'importlib.import_module'}\r
\r
claims, issues, unused_parameters = [], [], []\r
\r
\r
class Opaque:\r
    """A runtime value. type is a statically evident Python type name, if any."""\r
    __slots__ = ('label', 'type')\r
\r
    def __init__(self, label='', type_=None):\r
        self.label, self.type = label, type_\r
\r
    def __eq__(self, other):\r
        return isinstance(other, Opaque) and other.label == self.label and other.type == self.type\r
\r
    __hash__ = None\r
\r
\r
class Template:\r
    """A string with known literal parts and Opaque holes."""\r
    __slots__ = ('parts',)\r
\r
    def __init__(self, parts):\r
        self.parts = tuple(parts)\r
\r
    def __eq__(self, other):\r
        return isinstance(other, Template) and other.parts == self.parts\r
\r
    __hash__ = None\r
\r
\r
AMBIGUOUS = object()  # provenance that differs across control-flow paths\r
MISSING = object()\r
\r
\r
def make_string(parts):\r
    """Normalise parts (str, Template, Opaque) into a str or a Template."""\r
    flat = []\r
    for part in parts:\r
        if isinstance(part, Template):\r
            flat.extend(part.parts)\r
        elif isinstance(part, str):\r
            flat.append(part)\r
        else:\r
            flat.append(part if isinstance(part, Opaque) else Opaque(str(part)))\r
    merged = []\r
    for part in flat:\r
        if isinstance(part, str) and merged and isinstance(merged[-1], str):\r
            merged[-1] += part\r
        elif part != '':\r
            merged.append(part)\r
    if all(isinstance(p, str) for p in merged):\r
        return ''.join(merged)\r
    return Template(merged)\r
\r
\r
def label(node):\r
    try:\r
        text = ast.unparse(node)\r
    except Exception:  # pragma: no cover - defensive\r
        text = type(node).__name__\r
    return text if len(text) <= 80 else text[:77] + '...'\r
\r
\r
def issue(node, reason, affects=None):\r
    item = {'line': getattr(node, 'lineno', 0), 'reason': reason, 'affects': list(affects or ALL)}\r
    if not any(i['line'] == item['line'] and i['reason'] == reason for i in issues):\r
        issues.append(item)\r
\r
\r
def add(node, kind, **fields):\r
    result = {'id': 'claim_%s' % (len(claims) + 1), 'type': kind, 'line': getattr(node, 'lineno', 0), **fields}\r
    claims.append(result)\r
    return result\r
\r
\r
def known(value):\r
    if isinstance(value, (Opaque, Template)):\r
        return False\r
    if isinstance(value, dict):\r
        return all(known(v) for v in value.values())\r
    if isinstance(value, (list, tuple)):\r
        return all(known(v) for v in value)\r
    return True\r
\r
\r
def public(value):\r
    return encode(value) if known(value) else None\r
\r
\r
def encode(value):\r
    """JSON form of an abstract value; unknown parts are explicit markers."""\r
    if isinstance(value, Opaque):\r
        return {'$ca': 'unknown', 'label': value.label, 'type': value.type}\r
    if isinstance(value, Template):\r
        return {'$ca': 'template', 'parts': [p if isinstance(p, str) else {'hole': p.label} for p in value.parts]}\r
    if isinstance(value, dict):\r
        return {k: encode(v) for k, v in value.items()}\r
    if isinstance(value, (list, tuple)):\r
        return [encode(v) for v in value]\r
    if isinstance(value, (str, int, float, bool)) or value is None:\r
        return value\r
    return {'$ca': 'unknown', 'label': repr(value)[:80], 'type': type(value).__name__}\r
\r
\r
def type_of(value):\r
    if isinstance(value, Opaque):\r
        return value.type\r
    if isinstance(value, Template):\r
        return 'str'\r
    return type(value).__name__\r
\r
\r
def origin_known(url):\r
    """True when a Template's scheme and host are literal."""\r
    if not isinstance(url, Template) or not url.parts or not isinstance(url.parts[0], str):\r
        return False\r
    head = url.parts[0]\r
    if '://' not in head:\r
        return False\r
    rest = head.split('://', 1)[1]\r
    return any(c in rest for c in '/?#') and rest.split('/')[0].split('?')[0] != ''\r
\r
\r
def copy_value(value):\r
    if isinstance(value, dict):\r
        return {k: copy_value(v) for k, v in value.items()}\r
    if isinstance(value, list):\r
        return [copy_value(v) for v in value]\r
    return value\r
\r
\r
def assigned_names(nodes):\r
    """Names (re)bound or mutated anywhere inside the statements."""\r
    names = set()\r
    for stmt in nodes:\r
        for n in ast.walk(stmt):\r
            if isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):\r
                names.add(n.id)\r
            elif isinstance(n, (ast.Subscript, ast.Attribute)) and isinstance(n.ctx, (ast.Store, ast.Del)):\r
                root = n\r
                while isinstance(root, (ast.Subscript, ast.Attribute)):\r
                    root = root.value\r
                if isinstance(root, ast.Name):\r
                    names.add(root.id)\r
            elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in MUTATORS \\\r
                    and isinstance(n.func.value, ast.Name):\r
                names.add(n.func.value.id)\r
            elif isinstance(n, (ast.Global, ast.Nonlocal)):\r
                names.update(n.names)\r
    return names\r
\r
\r
class Context:\r
    def __init__(self):\r
        self.calls = {}           # id(ast.Call) -> call_id for HTTP requests\r
        self.functions = {}       # module-level function name -> FunctionInfo\r
        self.module = None        # module-level Analyzer\r
\r
\r
class FunctionInfo:\r
    def __init__(self, node):\r
        self.node, self.done, self.running, self.summary = node, False, False, None\r
\r
\r
CTX = Context()\r
\r
\r
class Analyzer:\r
    def __init__(self, env=None, imports=None, provenance=None, local_functions=None):\r
        self.env = dict(env or {})\r
        self.imports = dict(imports or {})\r
        self.prov = dict(provenance or {})\r
        self.local_functions = dict(local_functions or {})\r
        self.returns = []\r
\r
    # ------------------------------------------------------------------ state\r
    def fork(self):\r
        child = Analyzer(self.env, self.imports, self.prov, self.local_functions)\r
        return child\r
\r
    def collect(self, *branches):\r
        for b in branches:\r
            if b is not None and b is not self:\r
                self.returns.extend(b.returns)\r
                b.returns = []\r
\r
    def join(self, branches, node):\r
        """Merge the end states of the branches that fall through."""\r
        live = [b for b in branches if b is not None]\r
        if not live:\r
            return\r
        if len(live) == 1:\r
            only = live[0]\r
            self.env, self.prov, self.imports = dict(only.env), dict(only.prov), dict(only.imports)\r
            self.local_functions = dict(only.local_functions)\r
            return\r
        env, prov = {}, {}\r
        for name in set().union(*(b.env.keys() for b in live)):\r
            values = [b.env.get(name, MISSING) for b in live]\r
            first = values[0]\r
            if first is not MISSING and all(v is not MISSING and v == first for v in values[1:]):\r
                env[name] = first\r
            else:\r
                types = {type_of(v) for v in values if v is not MISSING}\r
                env[name] = Opaque(name, types.pop() if len(types) == 1 and MISSING not in values else None)\r
        for name in set().union(*(b.prov.keys() for b in live)):\r
            tracked = [b.prov.get(name) for b in live if b.prov.get(name) is not None]\r
            if any(t is AMBIGUOUS for t in tracked) or any(t != tracked[0] for t in tracked[1:]):\r
                prov[name] = AMBIGUOUS\r
                issue(node, 'Response provenance of %s differs across branches; field accesses cannot be linked to one operation.' % name, RESPONSE)\r
            else:\r
                # May-alias: fields read later are checked against the response they may come from.\r
                prov[name] = tracked[0]\r
        self.env, self.prov = env, prov\r
        self.imports = dict(live[0].imports)\r
        for b in live[1:]:\r
            for k in list(self.imports):\r
                if b.imports.get(k) != self.imports[k]:\r
                    self.imports.pop(k)\r
\r
    def havoc(self, names, keep_provenance=True):\r
        for name in names:\r
            self.env[name] = Opaque(name)\r
            self.imports.pop(name, None)\r
            if not keep_provenance:\r
                self.prov.pop(name, None)\r
\r
    # ------------------------------------------------------------- resolution\r
    def qualified(self, node):\r
        if isinstance(node, ast.Name):\r
            if node.id in self.env and node.id not in self.imports:\r
                return ''\r
            return self.imports.get(node.id, node.id)\r
        if isinstance(node, ast.Attribute):\r
            base = self.qualified(node.value)\r
            return base + '.' + node.attr if base else ''\r
        return ''\r
\r
    def function_info(self, name):\r
        info = self.local_functions.get(name)\r
        if info is None and name not in self.env and name not in self.imports:\r
            info = CTX.functions.get(name)\r
        return info\r
\r
    def ensure_analyzed(self, info):\r
        if info.done or info.running:\r
            return\r
        module = CTX.module\r
        self.analyze_function(info, module.env if module else self.env, module.imports if module else self.imports, module.prov if module else self.prov)\r
\r
    def analyze_function(self, info, env, imports, provenance=None):\r
        """Analyze a body once; globals/closure values and response provenance are visible."""\r
        node = info.node\r
        info.running = True\r
        child = Analyzer(env, imports, provenance, self.local_functions)\r
        all_args = node.args.posonlyargs + node.args.args + node.args.kwonlyargs\r
        extra = [a for a in (node.args.vararg, node.args.kwarg) if a is not None]\r
        for arg in all_args + extra:\r
            child.env[arg.arg] = copy_value(bindings[arg.arg]) if arg.arg in bindings else Opaque(arg.arg)\r
            child.imports.pop(arg.arg, None)\r
            child.prov.pop(arg.arg, None)\r
        record_unused_parameters(node, all_args)\r
        if isinstance(node, ast.AsyncFunctionDef):\r
            issue(node, 'Async functions are outside the supported extraction subset.', API)\r
        child.statements(node.body)\r
        tracked = [r for r in child.returns if r is not None]\r
        if any(r is AMBIGUOUS for r in tracked) or any(r != tracked[0] for r in tracked[1:]):\r
            info.summary = AMBIGUOUS\r
            issue(node, 'Function %s returns data from different operations.' % node.name, RESPONSE)\r
        else:\r
            info.summary = tracked[0] if tracked else None\r
        info.running, info.done = False, True\r
\r
    # ------------------------------------------------------------ evaluation\r
    def value(self, node):\r
        if node is None:\r
            return None\r
        if isinstance(node, ast.Constant):\r
            return node.value\r
        if isinstance(node, ast.Name):\r
            if node.id in self.env:\r
                return self.env[node.id]\r
            return Opaque(node.id)\r
        if isinstance(node, ast.Dict):\r
            result = {}\r
            for k, v in zip(node.keys, node.values):\r
                if k is None:\r
                    spread = self.value(v)\r
                    if isinstance(spread, dict):\r
                        result.update(spread)\r
                        continue\r
                    return Opaque(label(node), 'dict')\r
                key = self.value(k)\r
                if not isinstance(key, str):\r
                    return Opaque(label(node), 'dict')\r
                result[key] = self.value(v)\r
            return result\r
        if isinstance(node, (ast.List, ast.Tuple)):\r
            if any(isinstance(e, ast.Starred) for e in node.elts):\r
                return Opaque(label(node), 'list')\r
            return [self.value(v) for v in node.elts]\r
        if isinstance(node, ast.Subscript):\r
            obj, key = self.value(node.value), self.value(node.slice)\r
            if isinstance(obj, (dict, list, str)) and known(key) and not isinstance(node.slice, ast.Slice):\r
                try:\r
                    return obj[key]\r
                except (KeyError, IndexError, TypeError):\r
                    pass\r
            return Opaque(label(node))\r
        if isinstance(node, ast.BinOp):\r
            left, right = self.value(node.left), self.value(node.right)\r
            if isinstance(node.op, ast.Add):\r
                if isinstance(left, (str, Template)) or isinstance(right, (str, Template)):\r
                    if isinstance(left, (int, float, bool, list, dict)) or isinstance(right, (int, float, bool, list, dict)):\r
                        return Opaque(label(node))  # a TypeError at runtime; not a URL\r
                    return make_string([left, right])\r
            if isinstance(node.op, ast.Mod) and isinstance(left, str) and known(right):\r
                try:\r
                    return left % (tuple(right) if isinstance(right, list) else right)\r
                except (TypeError, ValueError, KeyError):\r
                    return Opaque(label(node), 'str')\r
            if known(left) and known(right) and isinstance(left, (int, float)) and isinstance(right, (int, float)):\r
                try:\r
                    return eval_binop(node.op, left, right)\r
                except Exception:\r
                    pass\r
            if isinstance(left, (str, Template)) and isinstance(node.op, ast.Mod):\r
                return Opaque(label(node), 'str')\r
            return Opaque(label(node))\r
        if isinstance(node, ast.JoinedStr):\r
            parts = []\r
            for part in node.values:\r
                if isinstance(part, ast.Constant):\r
                    parts.append(part.value)\r
                elif isinstance(part, ast.FormattedValue):\r
                    val = self.value(part.value)\r
                    plain = part.format_spec is None and part.conversion == -1\r
                    if plain and isinstance(val, (str, Template)):\r
                        parts.append(val)\r
                    elif plain and (val is None or isinstance(val, (int, float, bool))):\r
                        parts.append(str(val))\r
                    else:\r
                        parts.append(Opaque(label(part.value), 'str'))\r
            return make_string(parts)\r
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):\r
            v = self.value(node.operand)\r
            if isinstance(v, (int, float)) and not isinstance(v, bool):\r
                return -v if isinstance(node.op, ast.USub) else v\r
            return Opaque(label(node))\r
        if isinstance(node, ast.IfExp):\r
            a, b = self.value(node.body), self.value(node.orelse)\r
            return a if a == b else Opaque(label(node), type_of(a) if type_of(a) == type_of(b) else None)\r
        if isinstance(node, ast.NamedExpr):\r
            return self.value(node.value)\r
        if isinstance(node, ast.Compare):\r
            return Opaque(label(node), 'bool')\r
        if isinstance(node, (ast.ListComp, ast.GeneratorExp)):\r
            return Opaque(label(node), 'list')\r
        if isinstance(node, ast.DictComp):\r
            return Opaque(label(node), 'dict')\r
        if isinstance(node, ast.Call):\r
            return self.call_value(node)\r
        return Opaque(label(node))\r
\r
    def call_value(self, node):\r
        """Pure evaluation of a call's result. Side effects are handled by scan()."""\r
        if id(node) in CTX.calls:\r
            return Opaque(label(node), 'requests.Response')\r
        name = self.qualified(node.func)\r
        args = [self.value(a) for a in node.args]\r
        kwargs = {kw.arg: self.value(kw.value) for kw in node.keywords if kw.arg}\r
        if name == 'str' and len(args) == 1:\r
            v = args[0]\r
            if isinstance(v, (str, Template)):\r
                return v\r
            if known(v) and isinstance(v, (int, float, bool)) or v is None:\r
                return str(v)\r
            return Opaque(label(node.args[0]), 'str')\r
        if name in ('int', 'float', 'bool') and len(args) == 1:\r
            if known(args[0]):\r
                try:\r
                    return {'int': int, 'float': float, 'bool': bool}[name](args[0])\r
                except (TypeError, ValueError):\r
                    pass\r
            return Opaque(label(node), name)\r
        if name in ('requests.Session', 'requests.session', 'requests.sessions.Session'):\r
            return Opaque(label(node), 'requests.Session')\r
        if name in ('requests.auth.HTTPBasicAuth', 'requests.HTTPBasicAuth'):\r
            return Opaque(label(node), 'requests.auth.HTTPBasicAuth')\r
        if name == 'len':\r
            return Opaque(label(node), 'int')\r
        if name == 'dict' and not args:\r
            return kwargs if all(kw.arg for kw in node.keywords) else Opaque(label(node), 'dict')\r
        if name in ('urllib.parse.quote', 'urllib.parse.quote_plus', 'requests.utils.quote'):\r
            if args and isinstance(args[0], str):\r
                safe = kwargs.get('safe', args[1] if len(args) > 1 else '/')\r
                fn = urllib.parse.quote_plus if name.endswith('quote_plus') else urllib.parse.quote\r
                return fn(args[0], safe=safe) if isinstance(safe, str) else Opaque(label(node), 'str')\r
            return Opaque(label(node.args[0]) if node.args else label(node), 'str')\r
        if name == 'urllib.parse.urlencode' and args and known(args[0]):\r
            try:\r
                return urllib.parse.urlencode(args[0])\r
            except (TypeError, ValueError):\r
                return Opaque(label(node), 'str')\r
        if name == 'urllib.parse.urljoin' and len(args) == 2 and all(isinstance(a, str) for a in args):\r
            return urllib.parse.urljoin(args[0], args[1])\r
        if name in ('os.getenv', 'os.environ.get'):\r
            return Opaque(label(node), 'str' if len(args) > 1 and isinstance(args[1], str) else None)\r
        if name in ('json.dumps',):\r
            return Opaque(label(node), 'str')\r
        if isinstance(node.func, ast.Attribute):\r
            receiver = self.value(node.func.value)\r
            method = node.func.attr\r
            if isinstance(receiver, dict) and method == 'get' and args and isinstance(args[0], str):\r
                return receiver.get(args[0], args[1] if len(args) > 1 else kwargs.get('default'))\r
            if isinstance(receiver, dict) and method == 'copy':\r
                return dict(receiver)\r
            if isinstance(receiver, str):\r
                return self.string_method(node, receiver, method, args, kwargs)\r
            if isinstance(receiver, Template):\r
                return self.template_method(node, receiver, method, args)\r
        return Opaque(label(node))\r
\r
    def string_method(self, node, receiver, method, args, kwargs):\r
        if method == 'replace' and len(args) >= 2 and isinstance(args[0], str) and args[0]:\r
            if isinstance(args[1], str):\r
                return receiver.replace(args[0], args[1])\r
            pieces = receiver.split(args[0])\r
            parts = [pieces[0]]\r
            for piece in pieces[1:]:\r
                parts.extend([args[1] if isinstance(args[1], (Template, Opaque)) else Opaque(label(node.args[1]), 'str'), piece])\r
            return make_string(parts)\r
        if method == 'format':\r
            return self.format_string(node, receiver, args, kwargs)\r
        if method in ('strip', 'rstrip', 'lstrip', 'lower', 'upper', 'title', 'capitalize') and all(isinstance(a, str) for a in args):\r
            return getattr(receiver, method)(*args)\r
        if method == 'join' and len(args) == 1 and isinstance(args[0], list) and all(isinstance(a, str) for a in args[0]):\r
            return receiver.join(args[0])\r
        if method in ('join', 'replace', 'format', 'strip', 'rstrip', 'lstrip', 'lower', 'upper'):\r
            return Opaque(label(node), 'str')\r
        return Opaque(label(node))\r
\r
    def template_method(self, node, receiver, method, args):\r
        if method == 'replace' and len(args) >= 2 and isinstance(args[0], str) and args[0]:\r
            parts = []\r
            for part in receiver.parts:\r
                if isinstance(part, str) and args[0] in part:\r
                    pieces = part.split(args[0])\r
                    parts.append(pieces[0])\r
                    for piece in pieces[1:]:\r
                        parts.extend([args[1] if isinstance(args[1], (str, Template, Opaque)) else Opaque(label(node.args[1]), 'str'), piece])\r
                else:\r
                    parts.append(part)\r
            return make_string(parts)\r
        if method in ('rstrip', 'strip') and receiver.parts and isinstance(receiver.parts[-1], str) and all(isinstance(a, str) for a in args):\r
            return make_string(list(receiver.parts[:-1]) + [receiver.parts[-1].rstrip(*args)]) if method == 'rstrip' else Opaque(label(node), 'str')\r
        return Opaque(label(node), 'str')\r
\r
    def format_string(self, node, template, args, kwargs):\r
        parts, auto = [], 0\r
        try:\r
            for literal, field, spec, conversion in string.Formatter().parse(template):\r
                parts.append(literal)\r
                if field is None:\r
                    continue\r
                if field == '':\r
                    key, auto = auto, auto + 1\r
                elif field.isdigit():\r
                    key = int(field)\r
                else:\r
                    key = field\r
                if isinstance(key, int):\r
                    val = args[key] if key < len(args) else Opaque(label(node), 'str')\r
                elif key.isidentifier():\r
                    val = kwargs.get(key, Opaque(key, 'str'))\r
                else:\r
                    val = Opaque(key, 'str')\r
                if spec or conversion or not (isinstance(val, (str, Template)) or known(val) and isinstance(val, (int, float, bool))):\r
                    val = Opaque(field or str(key), 'str')\r
                parts.append(val if isinstance(val, (str, Template, Opaque)) else str(val))\r
        except (ValueError, IndexError):\r
            return Opaque(label(node), 'str')\r
        return make_string(parts)\r
\r
    # ------------------------------------------------------------ provenance\r
    def origin(self, node):\r
        """(call_id, None) for a raw Response, (call_id, path) for decoded JSON data."""\r
        if isinstance(node, ast.Name):\r
            return self.prov.get(node.id)\r
        if isinstance(node, ast.NamedExpr):\r
            return self.origin(node.value)\r
        if isinstance(node, ast.Call):\r
            if id(node) in CTX.calls:\r
                return (CTX.calls[id(node)], None)\r
            if isinstance(node.func, ast.Attribute):\r
                source = self.origin(node.func.value)\r
                attr = node.func.attr\r
                if source is AMBIGUOUS:\r
                    return AMBIGUOUS if attr in ('json', 'get', 'copy') else None\r
                if source and source[1] is None and attr == 'json':\r
                    return (source[0], [])\r
                if source and source[1] is not None and attr == 'get' and node.args:\r
                    key = self.value(node.args[0])\r
                    return (source[0], source[1] + [key if isinstance(key, str) else '*'])\r
                if source and source[1] is not None and attr == 'copy':\r
                    return source\r
            if isinstance(node.func, ast.Name):\r
                if node.func.id in ('list', 'sorted', 'reversed', 'dict', 'tuple') and len(node.args) == 1:\r
                    return self.origin(node.args[0])\r
                info = self.function_info(node.func.id)\r
                if info is not None:\r
                    self.ensure_analyzed(info)\r
                    return info.summary\r
            return None\r
        if isinstance(node, ast.Subscript):\r
            source = self.origin(node.value)\r
            if source is AMBIGUOUS:\r
                return AMBIGUOUS\r
            if source and source[1] is not None:\r
                if isinstance(node.slice, ast.Slice):\r
                    return source\r
                key = self.value(node.slice)\r
                if isinstance(key, bool) or not isinstance(key, (str, int)):\r
                    return (source[0], source[1] + ['*'])\r
                return (source[0], source[1] + [key])\r
            return None\r
        if isinstance(node, ast.IfExp):\r
            return self.merge_origins([self.origin(node.body), self.origin(node.orelse)], node)\r
        if isinstance(node, ast.BoolOp):\r
            return self.merge_origins([self.origin(v) for v in node.values], node)\r
        return None\r
\r
    def merge_origins(self, origins, node):\r
        tracked = [o for o in origins if o is not None]\r
        if not tracked:\r
            return None\r
        if any(o is AMBIGUOUS for o in tracked) or any(o != tracked[0] for o in tracked[1:]):\r
            issue(node, 'Expression may hold data from different operations.', RESPONSE)\r
            return AMBIGUOUS\r
        return tracked[0]\r
\r
    # --------------------------------------------------------------- scanning\r
    def scan(self, node):\r
        if node is None:\r
            return\r
        if isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)):\r
            self.comprehension(node)\r
            return\r
        if isinstance(node, ast.Lambda):\r
            child = self.fork()\r
            for arg in node.args.posonlyargs + node.args.args + node.args.kwonlyargs:\r
                child.env[arg.arg] = Opaque(arg.arg)\r
                child.prov.pop(arg.arg, None)\r
            child.scan(node.body)\r
            return\r
        if isinstance(node, ast.Await):\r
            issue(node, 'Await expressions are outside the supported extraction subset.', API)\r
        for child in ast.iter_child_nodes(node):\r
            self.scan(child)\r
        if isinstance(node, ast.NamedExpr):\r
            self.assign(node.target, node.value)\r
        if isinstance(node, ast.Subscript) and isinstance(node.ctx, ast.Load):\r
            source = self.origin(node)\r
            if source is AMBIGUOUS:\r
                issue(node, 'Response field read from data with ambiguous provenance.', RESPONSE)\r
            elif source and source[1]:\r
                add(node, 'output_field', call_id=source[0], field=source[1][-1], path=source[1])\r
        if isinstance(node, ast.Call):\r
            self.call(node)\r
\r
    def comprehension(self, node):\r
        child = self.fork()\r
        for gen in node.generators:\r
            child.scan(gen.iter)\r
            source = child.origin(gen.iter)\r
            child.bind_iteration(gen.target, gen.iter, source)\r
            for cond in gen.ifs:\r
                child.scan(cond)\r
        if isinstance(node, ast.DictComp):\r
            child.scan(node.key)\r
            child.scan(node.value)\r
        else:\r
            child.scan(node.elt)\r
\r
    def bind_iteration(self, target, iterator, source):\r
        """Bind a for/comprehension target, retaining response-item provenance."""\r
        items_call = isinstance(iterator, ast.Call) and isinstance(iterator.func, ast.Attribute) \\\r
            and iterator.func.attr in ('items', 'values', 'keys') and not iterator.args\r
        if items_call:\r
            base = self.origin(iterator.func.value)\r
            if base is AMBIGUOUS:\r
                issue(iterator, 'Iteration over data with ambiguous provenance.', RESPONSE)\r
                base = None\r
            names = target.elts if isinstance(target, ast.Tuple) else [target]\r
            for i, t in enumerate(names):\r
                if isinstance(t, ast.Name):\r
                    self.env[t.id] = Opaque(t.id)\r
                    self.imports.pop(t.id, None)\r
                    is_value = iterator.func.attr == 'values' or (iterator.func.attr == 'items' and i == 1)\r
                    if base and base[1] is not None and is_value:\r
                        self.prov[t.id] = (base[0], base[1] + ['*'])\r
                    else:\r
                        self.prov.pop(t.id, None)\r
                else:\r
                    self.assign(t, None)\r
            return\r
        if isinstance(iterator, ast.Call) and isinstance(iterator.func, ast.Name) and iterator.func.id == 'enumerate' \\\r
                and iterator.args and isinstance(target, ast.Tuple) and len(target.elts) == 2:\r
            inner = self.origin(iterator.args[0])\r
            self.bind_iteration(target.elts[0], ast.Constant(0), None)\r
            self.bind_iteration(target.elts[1], iterator.args[0], inner)\r
            return\r
        if source is AMBIGUOUS:\r
            issue(iterator, 'Iteration over data with ambiguous provenance.', RESPONSE)\r
            source = None\r
        if isinstance(target, ast.Name):\r
            self.env[target.id] = Opaque(target.id)\r
            self.imports.pop(target.id, None)\r
            if source and source[1] is not None:\r
                self.prov[target.id] = (source[0], source[1] + [0])\r
            else:\r
                self.prov.pop(target.id, None)\r
        else:\r
            if source and source[1] is not None:\r
                issue(target, 'Destructuring items of a response is outside the supported subset.', RESPONSE)\r
            for n in ast.walk(target):\r
                if isinstance(n, ast.Name):\r
                    self.env[n.id] = Opaque(n.id)\r
                    self.prov.pop(n.id, None)\r
\r
    def call(self, node):\r
        name = self.qualified(node.func)\r
        method = name[len('requests.'):] if name.startswith('requests.') else ''\r
        if method.startswith('api.'):\r
            method = method[4:]\r
        if name == 'requests' or name.startswith('requests.'):\r
            add(node, 'method_call', library='requests', method=name[len('requests.'):] if name.startswith('requests.') else '')\r
        if method in HTTP or method == 'request':\r
            self.http(node, method)\r
            return\r
        if name in DYNAMIC_CODE or (isinstance(node.func, ast.Name) and node.func.id in DYNAMIC_CODE and node.func.id not in self.env):\r
            issue(node, 'Dynamic code or attribute access is unsupported.', ALL)\r
            return\r
        if name.startswith(OTHER_HTTP_CLIENTS):\r
            issue(node, 'Only direct requests calls are supported; other HTTP clients are unresolved: ' + name, API)\r
            return\r
        if name.startswith('requests.'):\r
            return  # exceptions, auth helpers, adapters and utilities: recorded, no HTTP claim\r
        if name:  # a callable resolved by name: module function, import or builtin\r
            if isinstance(node.func, ast.Name):\r
                info = self.function_info(node.func.id)\r
                if info is not None:\r
                    self.ensure_analyzed(info)\r
                    for arg in list(node.args) + [kw.value for kw in node.keywords]:\r
                        source = self.origin(arg)\r
                        if source is AMBIGUOUS or source and source[1] is not None:\r
                            issue(node, 'Response data is passed into user-defined function %s; field accesses inside it are not linked.' % node.func.id, RESPONSE)\r
                    self.havoc_arguments(node)\r
                    return\r
            if name in PURE or name in BUILTIN_EXCEPTIONS or name.split('.')[-1] in BUILTIN_EXCEPTIONS:\r
                return\r
            self.havoc_arguments(node)\r
            for arg in node.args:\r
                if isinstance(arg, ast.Lambda) and any(self.origin(a) is not None for a in node.args if a is not arg):\r
                    issue(node, 'A lambda applied to response data is outside the supported subset.', RESPONSE)\r
            return\r
        if isinstance(node.func, ast.Attribute):\r
            self.method_call(node)\r
            return\r
        self.havoc_arguments(node)\r
\r
    def havoc_arguments(self, node):\r
        """An unknown callee may mutate container arguments; forget their contents."""\r
        for arg in list(node.args) + [kw.value for kw in node.keywords]:\r
            if isinstance(arg, ast.Starred):\r
                arg = arg.value\r
            if isinstance(arg, ast.Name) and isinstance(self.env.get(arg.id), (dict, list)):\r
                self.env[arg.id] = Opaque(arg.id, type_of(self.env[arg.id]))\r
\r
    def method_call(self, node):\r
        receiver_node, attr = node.func.value, node.func.attr\r
        source = self.origin(receiver_node)\r
        if source is AMBIGUOUS:\r
            if attr == 'get':\r
                issue(node, 'Response field read from data with ambiguous provenance.', RESPONSE)\r
            return\r
        if source is not None:\r
            if source[1] is None:  # raw Response\r
                if attr == 'json' and (node.args or node.keywords):\r
                    issue(node, 'Custom JSON decoding arguments can change response shape.', RESPONSE)\r
                return\r
            if attr == 'get' and node.args:\r
                add(node, 'output_field', call_id=source[0], field=self.origin(node)[1][-1], path=self.origin(node)[1], optional_access=True)\r
            elif attr == 'pop' and node.args:\r
                key = self.value(node.args[0])\r
                path = source[1] + [key if isinstance(key, str) else '*']\r
                add(node, 'output_field', call_id=source[0], field=path[-1], path=path, optional_access=len(node.args) > 1)\r
                self.forget_response_data(receiver_node, node)\r
            elif attr in MUTATORS:\r
                self.forget_response_data(receiver_node, node)\r
            return\r
        receiver = self.value(receiver_node)\r
        if isinstance(receiver_node, ast.Name) and receiver_node.id in self.env and attr in MUTATORS:\r
            self.mutate(receiver_node.id, attr, node)\r
            return\r
        if attr in HTTP or attr == 'request':\r
            if isinstance(receiver, Opaque) and receiver.type == 'requests.Session':\r
                issue(node, 'Session-based requests are outside the supported subset.', API)\r
            elif isinstance(receiver, (Opaque, Template)) and not self.qualified(receiver_node):\r
                if attr != 'get' or self.looks_like_request(node):\r
                    issue(node, 'Unresolved HTTP-like call receiver: ' + label(node.func), API)\r
        if not self.qualified(receiver_node) and not isinstance(receiver, (str, Template, dict)):\r
            self.havoc_arguments(node)\r
\r
    def looks_like_request(self, node):\r
        if any(kw.arg in REQUEST_KWARGS - {'url'} for kw in node.keywords):\r
            return True\r
        if node.args:\r
            first = self.value(node.args[0])\r
            text = first if isinstance(first, str) else first.parts[0] if isinstance(first, Template) and isinstance(first.parts[0], str) else ''\r
            return text.startswith(('http://', 'https://', '/'))\r
        return False\r
\r
    def forget_response_data(self, receiver_node, node):\r
        issue(node, 'Response data is mutated; later field reads may not come from the API.', RESPONSE)\r
        if isinstance(receiver_node, ast.Name):\r
            self.prov[receiver_node.id] = AMBIGUOUS\r
\r
    def mutate(self, name, attr, node):\r
        """Apply a container mutation (copy-on-write) or forget the container."""\r
        current = self.env[name]\r
        args = [self.value(a) for a in node.args]\r
        kwargs = {kw.arg: self.value(kw.value) for kw in node.keywords if kw.arg}\r
        new = MISSING\r
        if isinstance(current, dict):\r
            if attr == 'update' and not any(kw.arg is None for kw in node.keywords):\r
                if not args or (len(args) == 1 and isinstance(args[0], dict)):\r
                    new = {**current, **(args[0] if args else {}), **kwargs}\r
            elif attr == 'setdefault' and args and isinstance(args[0], str):\r
                new = dict(current)\r
                new.setdefault(args[0], args[1] if len(args) > 1 else None)\r
            elif attr == 'pop' and args and isinstance(args[0], str):\r
                new = {k: v for k, v in current.items() if k != args[0]}\r
            elif attr == 'clear':\r
                new = {}\r
        elif isinstance(current, list):\r
            if attr == 'append' and len(args) == 1:\r
                new = current + [args[0]]\r
            elif attr == 'extend' and len(args) == 1 and isinstance(args[0], list):\r
                new = current + list(args[0])\r
            elif attr == 'clear':\r
                new = []\r
        if new is MISSING:\r
            new = Opaque(name, type_of(current))\r
        self.set_container(name, new)\r
\r
    def set_container(self, name, new):\r
        old = self.env.get(name)\r
        for other, value in list(self.env.items()):\r
            if other != name and value is old and isinstance(old, (dict, list)):\r
                self.env[other] = new  # keep aliases consistent\r
            elif other != name and isinstance(value, (dict, list)) and contains(value, old):\r
                self.env[other] = Opaque(other, type_of(value))\r
        self.env[name] = new\r
\r
    def http(self, node, method):\r
        args = list(node.args)\r
        kwargs = {kw.arg: kw.value for kw in node.keywords if kw.arg}\r
        expanded = any(kw.arg is None for kw in node.keywords)\r
        if expanded:\r
            issue(node, 'Expanded request keyword arguments are unsupported.', API)\r
        if method == 'request':\r
            method_node = kwargs.get('method') or (args.pop(0) if args else None)\r
            method_value = self.value(method_node)\r
        else:\r
            method_value = method.upper()\r
        url_node = kwargs.get('url') or (args.pop(0) if args else None)\r
        url = self.value(url_node)\r
        for key, val in zip(POSITIONAL.get(method, []), args):\r
            if key in kwargs:\r
                issue(node, 'Duplicate request argument.', REQUEST)\r
            kwargs[key] = val\r
        if len(args) > len(POSITIONAL.get(method, [])):\r
            issue(node, 'Unsupported positional request arguments.', REQUEST)\r
        call_id = 'call_%s_%s' % (node.lineno, node.col_offset)\r
        CTX.calls[id(node)] = call_id\r
        request = {}\r
        for via in ('params', 'json', 'data', 'headers', 'cookies', 'auth'):\r
            if via in kwargs:\r
                value = self.value(kwargs[via])\r
                request[via] = {'provided': True, 'known': known(value), 'value': public(value),\r
                                'keys_known': isinstance(value, dict), 'shape': encode(value),\r
                                'fields': {k: {'known': known(v), 'value': public(v), 'shape': encode(v)} for k, v in value.items()} if isinstance(value, dict) else {}}\r
                if isinstance(value, dict):\r
                    for field, val in value.items():\r
                        add(node, 'input_field', call_id=call_id, field=field, via=via, known=known(val), value=public(val))\r
        method_ok = isinstance(method_value, str) and method_value.upper() in {m.upper() for m in HTTP}\r
        url_ok = isinstance(url, str) or origin_known(url)\r
        if not url_ok or not method_ok:\r
            issue(node, 'Dynamic endpoint or HTTP method requires explicit input_bindings.', API)\r
        add(node, 'endpoint', call_id=call_id, endpoint=url if isinstance(url, str) else None,\r
            endpoint_template=encode(url) if isinstance(url, Template) else None,\r
            http_method=method_value.upper() if isinstance(method_value, str) else None,\r
            resolved=url_ok and method_ok, request=request, request_complete=not expanded)\r
        if 'verify' in kwargs and self.value(kwargs['verify']) is False:\r
            issue(node, 'TLS verification disabled; outside supported verification scope.', ['contextual'])\r
        if 'files' in kwargs:\r
            issue(node, 'Multipart file uploads are outside the supported request subset.', REQUEST)\r
        if any(k not in REQUEST_KWARGS | {'files'} for k in kwargs):\r
            issue(node, 'Unsupported requests keyword argument.', REQUEST)\r
\r
    # -------------------------------------------------------------- binding\r
    def assign(self, target, node, value=MISSING):\r
        if value is MISSING:\r
            value = self.value(node) if node is not None else Opaque(label(target))\r
        if isinstance(target, ast.Name):\r
            self.env[target.id] = value\r
            self.imports.pop(target.id, None)\r
            self.local_functions.pop(target.id, None)\r
            source = self.origin(node) if node is not None else None\r
            if source is not None:\r
                self.prov[target.id] = source\r
            else:\r
                self.prov.pop(target.id, None)\r
        elif isinstance(target, (ast.Tuple, ast.List)):\r
            elts = target.elts\r
            if node is not None and isinstance(node, (ast.Tuple, ast.List)) and len(node.elts) == len(elts) \\\r
                    and not any(isinstance(e, ast.Starred) for e in elts + node.elts):\r
                values = [self.value(e) for e in node.elts]\r
                for t, n, v in zip(elts, node.elts, values):\r
                    self.assign(t, n, v)\r
                return\r
            source = self.origin(node) if node is not None else None\r
            if source is AMBIGUOUS or source and source[1] is not None:\r
                issue(target, 'Destructuring response data is outside the supported subset.', RESPONSE)\r
            for t in elts:\r
                self.assign(t.value if isinstance(t, ast.Starred) else t, None, Opaque(label(t)))\r
        elif isinstance(target, ast.Subscript):\r
            self.assign_item(target, value)\r
        elif isinstance(target, ast.Attribute):\r
            root = target\r
            while isinstance(root, (ast.Attribute, ast.Subscript)):\r
                root = root.value\r
            if isinstance(root, ast.Name) and isinstance(self.env.get(root.id), (dict, list)):\r
                self.set_container(root.id, Opaque(root.id, type_of(self.env[root.id])))\r
        elif isinstance(target, ast.Starred):\r
            self.assign(target.value, None, Opaque(label(target)))\r
\r
    def assign_item(self, target, value):\r
        """d[k] = v on a tracked container (copy-on-write); otherwise forget the container."""\r
        chain = []\r
        node = target\r
        while isinstance(node, ast.Subscript):\r
            chain.append(node.slice)\r
            node = node.value\r
        if not isinstance(node, ast.Name):\r
            return\r
        name = node.id\r
        source = self.prov.get(name)\r
        if source is not None and name not in self.env or source is not None and not isinstance(self.env.get(name), (dict, list)):\r
            self.forget_response_data(node, target)\r
            return\r
        keys = [self.value(k) for k in reversed(chain)]\r
        root = self.env.get(name)\r
\r
        def update(container, path):\r
            if not path:\r
                return value\r
            key = path[0]\r
            if isinstance(container, dict) and isinstance(key, str):\r
                new = dict(container)\r
                new[key] = update(container.get(key, {}) if len(path) > 1 else None, path[1:])\r
                return new\r
            if isinstance(container, list) and isinstance(key, int) and -len(container) <= key < len(container):\r
                new = list(container)\r
                new[key] = update(container[key], path[1:])\r
                return new\r
            return MISSING\r
\r
        new = update(root, keys) if isinstance(root, (dict, list)) else MISSING\r
        if new is MISSING or contains_missing(new):\r
            new = Opaque(name, type_of(root) if root is not None else None)\r
        if name in self.env or isinstance(new, (dict, list)):\r
            self.set_container(name, new)\r
\r
    # ------------------------------------------------------------ statements\r
    def statements(self, statements):\r
        """Analyze a block; return True when it cannot fall through."""\r
        for node in statements:\r
            if self.statement(node):\r
                return True\r
        return False\r
\r
    def statement(self, node):\r
        if isinstance(node, ast.Import):\r
            for alias in node.names:\r
                self.imports[alias.asname or alias.name.split('.')[0]] = alias.name if alias.asname else alias.name.split('.')[0]\r
                self.env.pop(alias.asname or alias.name.split('.')[0], None)\r
                top = alias.name.split('.')[0]\r
                add(node, 'import', library=alias.name, stdlib=top in getattr(sys, 'stdlib_module_names', set()), local=False)\r
            return False\r
        if isinstance(node, ast.ImportFrom):\r
            mod = node.module or ''\r
            for alias in node.names:\r
                if alias.name == '*':\r
                    issue(node, 'Wildcard import is unsupported.', ALL)\r
                else:\r
                    self.imports[alias.asname or alias.name] = (mod + '.' if mod else '') + alias.name\r
                    self.env.pop(alias.asname or alias.name, None)\r
                add(node, 'import', library=mod, stdlib=mod.split('.')[0] in getattr(sys, 'stdlib_module_names', set()), local=node.level > 0)\r
            return False\r
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):\r
            for decorator in node.decorator_list:\r
                self.scan(decorator)\r
            self.env.pop(node.name, None)\r
            self.imports.pop(node.name, None)\r
            self.prov.pop(node.name, None)\r
            registered = CTX.functions.get(node.name)\r
            if self is CTX.module and registered is not None and registered.node is node:\r
                return False  # analyzed on first call, or at module end with final globals\r
            info = FunctionInfo(node)\r
            self.local_functions[node.name] = info\r
            self.analyze_function(info, self.env, self.imports, self.prov)\r
            return False\r
        if isinstance(node, ast.ClassDef):\r
            issue(node, 'Classes are outside the supported extraction subset.', API)\r
            for stmt in node.body:\r
                if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):\r
                    self.analyze_function(FunctionInfo(stmt), self.env, self.imports, self.prov)\r
            self.env.pop(node.name, None)\r
            return False\r
        if isinstance(node, ast.Assign):\r
            self.scan(node.value)\r
            value = self.value(node.value)\r
            for target in node.targets:\r
                self.scan_target(target)\r
                self.assign(target, node.value, value)\r
            return False\r
        if isinstance(node, ast.AnnAssign):\r
            if node.value is not None:\r
                self.scan(node.value)\r
                self.scan_target(node.target)\r
                self.assign(node.target, node.value)\r
            return False\r
        if isinstance(node, ast.AugAssign):\r
            self.scan(node.value)\r
            self.scan_target(node.target)\r
            if isinstance(node.target, ast.Name):\r
                combined = ast.BinOp(left=ast.Name(id=node.target.id, ctx=ast.Load()), op=node.op, right=node.value)\r
                ast.copy_location(combined, node)\r
                value = self.value(combined)\r
                if self.prov.get(node.target.id) is not None:\r
                    self.forget_response_data(node.target, node)\r
                self.env[node.target.id] = value\r
                self.imports.pop(node.target.id, None)\r
            else:\r
                self.assign(node.target, None, Opaque(label(node.target)))\r
            return False\r
        if isinstance(node, (ast.Expr,)):\r
            self.scan(node.value)\r
            return False\r
        if isinstance(node, ast.Return):\r
            self.scan(node.value)\r
            if node.value is not None:\r
                self.returns.append(self.origin(node.value))\r
            return True\r
        if isinstance(node, ast.Raise):\r
            self.scan(node.exc)\r
            self.scan(node.cause)\r
            return True\r
        if isinstance(node, (ast.Break, ast.Continue)):\r
            return True\r
        if isinstance(node, ast.Pass):\r
            return False\r
        if isinstance(node, ast.If):\r
            self.scan(node.test)\r
            body, orelse = self.fork(), self.fork()\r
            body_ends = body.statements(node.body)\r
            else_ends = orelse.statements(node.orelse)\r
            self.collect(body, orelse)\r
            self.join([None if body_ends else body, None if else_ends else orelse], node)\r
            return body_ends and else_ends\r
        if isinstance(node, (ast.For, ast.AsyncFor, ast.While)):\r
            if isinstance(node, ast.AsyncFor):\r
                issue(node, 'Async iteration is outside the supported extraction subset.', API)\r
            self.loop(node)\r
            return False\r
        if isinstance(node, (ast.Try, getattr(ast, 'TryStar', ast.Try))):\r
            return self.try_statement(node)\r
        if isinstance(node, (ast.With, ast.AsyncWith)):\r
            if isinstance(node, ast.AsyncWith):\r
                issue(node, 'Async context managers are outside the supported extraction subset.', API)\r
            for item in node.items:\r
                self.scan(item.context_expr)\r
                if item.optional_vars is not None:\r
                    source = self.origin(item.context_expr)\r
                    name = self.qualified(item.context_expr.func) if isinstance(item.context_expr, ast.Call) else ''\r
                    typed = Opaque(label(item.optional_vars), 'requests.Session' if name in ('requests.Session', 'requests.session') else None)\r
                    self.assign(item.optional_vars, None, typed)\r
                    if isinstance(item.optional_vars, ast.Name) and source is not None:\r
                        self.prov[item.optional_vars.id] = source\r
            return self.statements(node.body)\r
        if isinstance(node, ast.Delete):\r
            for target in node.targets:\r
                if isinstance(target, ast.Name):\r
                    self.env.pop(target.id, None)\r
                    self.prov.pop(target.id, None)\r
                elif isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name) and isinstance(self.env.get(target.value.id), dict):\r
                    key = self.value(target.slice)\r
                    current = self.env[target.value.id]\r
                    self.set_container(target.value.id, {k: v for k, v in current.items() if k != key} if isinstance(key, str) else Opaque(target.value.id, 'dict'))\r
                elif isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name) and self.prov.get(target.value.id) is not None:\r
                    self.forget_response_data(target.value, node)\r
            return False\r
        if isinstance(node, ast.Assert):\r
            self.scan(node.test)\r
            self.scan(node.msg)\r
            return False\r
        if isinstance(node, (ast.Global, ast.Nonlocal)):\r
            issue(node, 'global/nonlocal rebinding is outside the supported extraction subset.', API)\r
            self.havoc(node.names, keep_provenance=False)\r
            return False\r
        if isinstance(node, getattr(ast, 'Match', ())):\r
            issue(node, 'Match statements are outside the supported extraction subset.', API)\r
            self.scan(node.subject)\r
            branches = []\r
            for case in node.cases:\r
                branch = self.fork()\r
                ends = branch.statements(case.body)\r
                self.collect(branch)\r
                branches.append(None if ends else branch)\r
            self.join(branches + [self.fork()], node)\r
            return False\r
        if isinstance(node, getattr(ast, 'TypeAlias', ())):\r
            return False\r
        issue(node, 'Unsupported statement: ' + type(node).__name__, API)\r
        return False\r
\r
    def scan_target(self, target):\r
        """Scan index expressions in an assignment target without recording field reads."""\r
        if isinstance(target, ast.Subscript):\r
            self.scan_target(target.value)\r
            self.scan(target.slice)\r
        elif isinstance(target, ast.Attribute):\r
            self.scan_target(target.value)\r
        elif isinstance(target, (ast.Tuple, ast.List)):\r
            for t in target.elts:\r
                self.scan_target(t)\r
\r
    def loop(self, node):\r
        body_nodes = node.body + node.orelse\r
        changed = assigned_names(body_nodes)\r
        if isinstance(node, (ast.For, ast.AsyncFor)):\r
            self.scan(node.iter)\r
            changed |= {n.id for n in ast.walk(node.target) if isinstance(n, ast.Name)}\r
        before = {name: self.prov.get(name) for name in changed}\r
        # Any iteration may see values from an earlier iteration: forget changed values.\r
        for name in changed:\r
            if name in self.env:\r
                self.env[name] = Opaque(name, type_of(self.env[name]))\r
        if isinstance(node, ast.While):\r
            self.scan(node.test)\r
        entry = self.fork()\r
        body = self.fork()\r
        if isinstance(node, (ast.For, ast.AsyncFor)):\r
            body.bind_iteration(node.target, node.iter, self.origin(node.iter))\r
        body.statements(node.body)\r
        self.collect(body)\r
        for name in changed:\r
            start, end = before.get(name), body.prov.get(name)\r
            if start is not None and end is not None and start != end:\r
                issue(node, 'Response provenance of %s changes across loop iterations.' % name, RESPONSE)\r
                body.prov[name] = AMBIGUOUS\r
        self.join([entry, body], node)\r
        if node.orelse:\r
            self.statements(node.orelse)\r
\r
    def try_statement(self, node):\r
        before = self.fork()\r
        body = self.fork()\r
        body_ends = body.statements(node.body)\r
        changed = assigned_names(node.body)\r
        ends = []\r
        if not body_ends:\r
            else_ends = body.statements(node.orelse) if node.orelse else False\r
            ends.append(None if else_ends else body)\r
        self.collect(body)\r
        for handler in node.handlers:\r
            h = before.fork()\r
            # A handler may start after any prefix of the body ran.\r
            for name in changed:\r
                if name in h.env or name in body.env:\r
                    h.env[name] = Opaque(name)\r
                if body.prov.get(name) is not None and h.prov.get(name) != body.prov.get(name):\r
                    h.prov[name] = body.prov[name] if h.prov.get(name) is None else AMBIGUOUS\r
            if handler.name:\r
                h.env[handler.name] = Opaque(handler.name)\r
                h.prov.pop(handler.name, None)\r
            handler_ends = h.statements(handler.body)\r
            self.collect(h)\r
            ends.append(None if handler_ends else h)\r
        reachable = any(e is not None for e in ends)\r
        self.join(ends if reachable else [before], node)\r
        final_ends = self.statements(node.finalbody) if node.finalbody else False\r
        return final_ends or not reachable\r
\r
\r
def contains(container, target):\r
    if container is target:\r
        return True\r
    if isinstance(container, dict):\r
        return any(contains(v, target) for v in container.values())\r
    if isinstance(container, list):\r
        return any(contains(v, target) for v in container)\r
    return False\r
\r
\r
def contains_missing(value):\r
    if value is MISSING:\r
        return True\r
    if isinstance(value, dict):\r
        return any(contains_missing(v) for v in value.values())\r
    if isinstance(value, list):\r
        return any(contains_missing(v) for v in value)\r
    return False\r
\r
\r
def eval_binop(op, left, right):\r
    if isinstance(op, ast.Add):\r
        return left + right\r
    if isinstance(op, ast.Sub):\r
        return left - right\r
    if isinstance(op, ast.Mult):\r
        return left * right\r
    if isinstance(op, ast.Div):\r
        return left / right\r
    if isinstance(op, ast.FloorDiv):\r
        return left // right\r
    if isinstance(op, ast.Mod):\r
        return left % right\r
    raise ValueError('unsupported')\r
\r
\r
def record_unused_parameters(node, all_args):\r
    referenced = set()\r
    reflective = False\r
    for stmt in node.body:\r
        for descendant in ast.walk(stmt):\r
            if isinstance(descendant, ast.Name):\r
                referenced.add(descendant.id)\r
                if descendant.id in ('locals', 'vars'):\r
                    reflective = True\r
    if reflective:\r
        return\r
    for arg in all_args:\r
        if arg.arg in ('self', 'cls') or arg.arg in referenced:\r
            continue\r
        # Pyright ranges are 0-indexed lines; ast lines are 1-indexed.\r
        unused_parameters.append({'name': arg.arg, 'line': arg.lineno - 1,\r
                                  'start_character': arg.col_offset, 'end_character': arg.col_offset + len(arg.arg)})\r
\r
\r
def prepass(tree):\r
    """Register module-level functions so calls resolve before definitions."""\r
    counts = {}\r
    for stmt in tree.body:\r
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):\r
            counts[stmt.name] = counts.get(stmt.name, 0) + 1\r
    for stmt in tree.body:\r
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)) and counts[stmt.name] == 1:\r
            CTX.functions[stmt.name] = FunctionInfo(stmt)\r
\r
\r
try:\r
    tree = ast.parse(code)\r
    for token in tokenize.generate_tokens(io.StringIO(code).readline):\r
        if token.type == tokenize.COMMENT and ('pyright:' in token.string.lower() or 'type: ignore' in token.string.lower()):\r
            issue(types.SimpleNamespace(lineno=token.start[0]), 'Candidate contains checker suppression/configuration directives.', IDENTIFIER)\r
    module = Analyzer()\r
    CTX.module = module\r
    prepass(tree)\r
    module.statements(tree.body)\r
    for info in list(CTX.functions.values()):\r
        if not info.done:\r
            module.analyze_function(info, module.env, module.imports, module.prov)\r
    print(json.dumps({\r
        'claims': claims,\r
        'complete': not issues,\r
        'issues': issues,\r
        'unused_parameters': unused_parameters,\r
    }))\r
except (SyntaxError, ValueError) as e:\r
    print(json.dumps({'claims': [], 'complete': False, 'issues': [], 'unused_parameters': [], 'error': str(e)}))\r
`;
  }
});

// src/verificationTypes.ts
function result(layer, state, tier2, source, detail, kind = null) {
  return { layer, state, tier: tier2, weight: LAYER_WEIGHTS[layer], evidence_source: source, evidence_detail: detail, hallucination_type: kind };
}
function unknown(layer, detail) {
  return result(layer, "unverifiable", "none", "verification", detail);
}
function aggregate(layer, rows, emptyReason) {
  const applicable = rows.filter((r) => r.state !== "not_applicable");
  if (!applicable.length) return result(layer, "not_applicable", "none", "extraction / specification", rows.length ? rows.map((r) => r.evidence_detail).join("\n") : emptyReason);
  const incorrect = applicable.filter((r) => r.state === "verified_incorrect");
  const unresolved = applicable.filter((r) => r.state === "unverifiable");
  const selected = incorrect.length ? incorrect.sort((a, b) => TIER_FACTORS[b.tier] - TIER_FACTORS[a.tier])[0] : unresolved.length ? unresolved[0] : applicable.sort((a, b) => TIER_FACTORS[a.tier] - TIER_FACTORS[b.tier])[0];
  return { ...selected, evidence_detail: rows.map((r) => r.evidence_detail).join("\n"), claim_ids: rows.flatMap((r) => r.claim_ids || []) };
}
function extractionLimits(source) {
  const layers = /* @__PURE__ */ new Set(), reasons = [];
  const records = Array.isArray(source) ? source.filter((c) => c.type === "extraction_issue") : source.error || !source.complete ? [{ issues: source.issues, error: source.error ?? (source.issues?.length ? void 0 : "Extraction incomplete.") }] : [];
  for (const record of records) {
    if (record.error) {
      ALL_LAYERS.forEach((l) => layers.add(l));
      reasons.push(String(record.error));
    }
    for (const i of record.issues || []) {
      const affects = Array.isArray(i?.affects) && i.affects.length ? i.affects : ALL_LAYERS;
      for (const l of affects) if (ALL_LAYERS.includes(l)) layers.add(l);
      reasons.push(`line ${i?.line ?? "?"}: ${i?.reason ?? "unsupported construct"}`);
    }
    if (!record.error && !(record.issues || []).length) ALL_LAYERS.forEach((l) => layers.add(l));
  }
  return { layers, reasons };
}
function aggregateExtracted(layer, claims, rows, emptyReason) {
  const r = aggregate(layer, rows, emptyReason);
  const relevant = { interface: ["import"], identifier: ["method_call"], access_point: ["endpoint"], input_contract: ["endpoint", "input_field"], output_contract: ["output_field"], contextual: ["endpoint", "input_field"] };
  r.claim_ids = claims.filter((c) => relevant[layer].includes(c.type) && typeof c.id === "string").map((c) => c.id);
  const limits = extractionLimits(claims);
  if (limits.layers.has(layer) && (r.state === "verified_correct" || r.state === "not_applicable")) {
    return { ...unknown(layer, `Extraction is incomplete for this layer; unsupported claims may be missing (${limits.reasons.join("; ")}). ` + r.evidence_detail), claim_ids: r.claim_ids };
  }
  if (limits.reasons.length && !limits.layers.has(layer)) {
    r.evidence_detail += `
Extraction limitations elsewhere do not affect this layer; evidence covers the extracted ${layer === "interface" ? "imports" : "claims"} only.`;
  }
  return r;
}
var import_crypto, LAYER_WEIGHTS, ALL_LAYERS, TIER_FACTORS, hashCode, ofType;
var init_verificationTypes = __esm({
  "src/verificationTypes.ts"() {
    "use strict";
    import_crypto = require("crypto");
    LAYER_WEIGHTS = { interface: 3, identifier: 3, access_point: 4, input_contract: 2, output_contract: 1, contextual: 2 };
    ALL_LAYERS = Object.keys(LAYER_WEIGHTS);
    TIER_FACTORS = { tier_1: 1, tier_2: 0.8, tier_3: 0.9, tier_4: 0.5, none: 0 };
    hashCode = (code) => (0, import_crypto.createHash)("sha256").update(code).digest("hex");
    ofType = (claims, type) => claims.filter((c) => c.type === type);
  }
});

// src/claimExtractor.ts
async function extractClaims({ code, input_bindings = {} }) {
  const failed = (error) => ({ claims: [], complete: false, issues: [], error, candidate_hash: hashCode(code) });
  if (!code.trim()) return failed("No candidate code supplied.");
  return new Promise((resolve4) => {
    const child = (0, import_child_process.spawn)(process.env.CONFIDENCE_PYTHON || "python", ["-c", BOOTSTRAP], { stdio: "pipe", timeout: 1e4 });
    let stdout = "", stderr = "";
    child.stdout.setEncoding("utf8");
    child.stderr.setEncoding("utf8");
    child.stdout.on("data", (d) => {
      stdout += d;
    });
    child.stderr.on("data", (d) => {
      stderr += d;
    });
    child.on("error", (e) => resolve4(failed(`Python extraction could not start: ${e.message}`)));
    child.stdin.on("error", () => {
    });
    child.on("close", (exitCode, signal) => {
      if (exitCode !== 0 || signal) return resolve4(failed(`Extraction failed (${exitCode ?? signal}): ${stderr}`));
      try {
        const data = JSON.parse(stdout);
        if (!Array.isArray(data.claims) || typeof data.complete !== "boolean" || !Array.isArray(data.issues)) throw new Error("Invalid extractor result");
        if (!data.complete) data.claims.push({ id: "extraction_limitations", type: "extraction_issue", issues: data.issues, error: data.error });
        resolve4({ ...data, candidate_hash: hashCode(code) });
      } catch {
        resolve4(failed(`Invalid extraction output: ${stderr || stdout.slice(0, 200)}`));
      }
    });
    child.stdin.end(JSON.stringify(EXTRACTION_SCRIPT) + "\n" + JSON.stringify({ code, input_bindings }));
  });
}
var import_child_process, BOOTSTRAP;
var init_claimExtractor = __esm({
  "src/claimExtractor.ts"() {
    "use strict";
    import_child_process = require("child_process");
    init_extractorScript();
    init_verificationTypes();
    BOOTSTRAP = "import sys, json; exec(compile(json.loads(sys.stdin.readline()), '<extract_claims>', 'exec'))";
  }
});

// src/packageEvidence.ts
async function queryPypi({ library_name }, fetcher = fetch) {
  const top = library_name.split(".")[0], distribution = IMPORT_DISTRIBUTIONS[top] || top;
  const source_url = `https://pypi.org/pypi/${encodeURIComponent(distribution)}/json`;
  const base = { source_url, retrieved_at: (/* @__PURE__ */ new Date()).toISOString(), import_name: top, distribution };
  if (!/^[A-Za-z_][A-Za-z0-9_.-]*$/.test(top)) return { ...base, exists: null, status: "unverifiable", summary: "Invalid or relative import name." };
  try {
    const response = await fetcher(source_url, { signal: AbortSignal.timeout(8e3) });
    if (response.status === 404) return { ...base, exists: false, status: "not_found", summary: "Distribution absent from PyPI; this alone does not prove an import nonexistent." };
    if (!response.ok) return { ...base, exists: null, status: "unverifiable", summary: `PyPI HTTP ${response.status}` };
    const data = await response.json();
    if (!data.info || typeof data.info.name !== "string" || typeof data.info.version !== "string") throw new Error("Malformed PyPI metadata");
    const normalize = (name) => name.toLowerCase().replace(/[-_.]+/g, "-");
    if (normalize(data.info.name) !== normalize(distribution)) throw new Error("PyPI metadata names a different distribution.");
    return { ...base, exists: true, status: "found", latest_version: data.info.version, summary: data.info.summary || "" };
  } catch (e) {
    return { ...base, exists: null, status: "unverifiable", summary: `Package lookup failed: ${String(e)}` };
  }
}
function pickDatum(container, top) {
  if (!container) return void 0;
  const direct = container[top];
  if (direct) return direct;
  const self = container;
  if (self.distribution === top || self.import_name === top) return self;
  return void 0;
}
async function verifyInterface({ claims, pypi_data = {} }) {
  const rows = ofType(claims, "import").map((imp) => {
    const top = String(imp.library || "").split(".")[0];
    if (imp.stdlib === true) return result("interface", "verified_correct", "tier_2", "Pinned interpreter standard-library inventory", `${top} is in the verification interpreter's standard library (sys.stdlib_module_names).`);
    if (imp.local) return unknown("interface", `Local import ${imp.library} cannot be verified without its source.`);
    const datum = pickDatum(pypi_data, top);
    if (!datum || datum.status === "unverifiable" || datum.exists === null) return unknown("interface", `No usable package evidence for ${top}: ${datum?.summary || "lookup missing"}`);
    if (!Object.hasOwn(IMPORT_DISTRIBUTIONS, top)) return unknown("interface", `No reviewed import-to-distribution mapping for ${top}; registry existence or 404 cannot settle this import.`);
    if (datum.status === "not_found" && datum.exists === false) return unknown("interface", `Expected distribution ${IMPORT_DISTRIBUTIONS[top]} not found; cannot establish import nonexistence.`);
    if (datum.status !== "found" || datum.exists !== true || datum.distribution !== IMPORT_DISTRIBUTIONS[top]) return unknown(
      "interface",
      `Inconsistent package evidence for ${top}: expected status=found, exists=true and distribution=${IMPORT_DISTRIBUTIONS[top]}; received status=${datum.status}, exists=${datum.exists}, distribution=${datum.distribution ?? "(missing)"}. Preserve the full query_pypi result or use verify_candidate.`
    );
    return result("interface", "verified_correct", "tier_2", "PyPI metadata + reviewed import mapping", `${top} maps to ${datum.distribution} (${datum.latest_version || "version unknown"}). Installation/callables checked separately by Pyright.`);
  });
  return aggregateExtracted("interface", claims, rows, "No imports in the extracted candidate.");
}
var IMPORT_DISTRIBUTIONS;
var init_packageEvidence = __esm({
  "src/packageEvidence.ts"() {
    "use strict";
    init_verificationTypes();
    IMPORT_DISTRIBUTIONS = { requests: "requests", numpy: "numpy", pandas: "pandas", PIL: "Pillow", sklearn: "scikit-learn", yaml: "PyYAML", bs4: "beautifulsoup4", cv2: "opencv-python" };
  }
});

// src/specDiscovery.ts
async function resolveApiSpec({ base_url }) {
  let base;
  try {
    base = new URL(base_url);
  } catch {
    return { spec: null, source_url: null, note: "Invalid absolute URL." };
  }
  if (!["https:", "http:"].includes(base.protocol)) return { spec: null, source_url: null, note: "Only HTTP(S) discovery is supported." };
  const direct = /\.json(?:$|\?)/i.test(base_url) || /openapi|swagger|api-docs/i.test(base.pathname);
  const candidates = direct ? [base_url] : ["/openapi.json", "/swagger.json", "/v3/api-docs"].map((p) => base_url.replace(/\/$/, "") + p);
  for (const url of candidates) {
    try {
      const r = await fetch(url, { signal: AbortSignal.timeout(5e3) });
      if (!r.ok) continue;
      const raw = await r.text(), spec = JSON.parse(raw);
      if (!/^3\.0\./.test(spec.openapi || "") || !spec.paths) continue;
      return { spec, source_url: r.url || url, retrieved_at: (/* @__PURE__ */ new Date()).toISOString(), content_hash: hashCode(raw), review_required: true };
    } catch {
    }
  }
  return { spec: null, source_url: null, note: "No supported JSON OpenAPI 3.0 contract resolved. Supply a reviewed snapshot; YAML/Swagger 2/OpenAPI 3.1 are not silently interpreted as 3.0." };
}
var init_specDiscovery = __esm({
  "src/specDiscovery.ts"() {
    "use strict";
    init_verificationTypes();
  }
});

// src/pyrightRunner.ts
async function launch(command, args, timeout) {
  return new Promise((resolve4) => {
    const child = (0, import_child_process2.spawn)(command, args, { stdio: "pipe", timeout });
    let stdout = "", stderr = "";
    child.stdout.setEncoding("utf8");
    child.stderr.setEncoding("utf8");
    child.stdout.on("data", (d) => {
      stdout += d;
    });
    child.stderr.on("data", (d) => {
      stderr += d;
    });
    child.on("error", (e) => resolve4({ stdout, stderr, exit_code: null, error: e.message }));
    child.on("close", (code, signal) => resolve4({ stdout, stderr, exit_code: code, signal, timed_out: signal === "SIGTERM" }));
    child.stdin.end();
  });
}
function createPyrightRunner() {
  return async ({ python, timeout_seconds = 20 }) => {
    const candidate_hash = hashCode(python);
    const env = await launch(process.env.CONFIDENCE_PYTHON || "python", ["-c", "import sys; print(sys.executable)"], 1e4);
    if (env.exit_code !== 0 || !env.stdout.trim()) return { ...env, candidate_hash, error: "Could not resolve the verification Python environment." };
    const directory = await (0, import_promises.mkdtemp)((0, import_path.join)((0, import_os.tmpdir)(), "confidence-pyright-"));
    try {
      const path = (0, import_path.join)(directory, "candidate.py");
      await (0, import_promises.writeFile)(path, python, "utf8");
      const config = (0, import_path.join)(directory, "pyrightconfig.json");
      await (0, import_promises.writeFile)(config, JSON.stringify({
        typeCheckingMode: "standard",
        pythonVersion: "3.12",
        include: ["candidate.py"],
        reportMissingModuleSource: "warning"
      }));
      const r = await launch(process.execPath, [
        require.resolve("pyright/index.js"),
        "--outputjson",
        "--project",
        config,
        "--pythonpath",
        env.stdout.trim(),
        path
      ], Math.min(60, Math.max(0.1, timeout_seconds)) * 1e3);
      const metadata = { candidate_hash, python_executable: env.stdout.trim() };
      try {
        const json = JSON.parse(r.stdout);
        return { ...r, ...metadata, checker_version: json.version, diagnostics: json.generalDiagnostics, summary: json.summary };
      } catch {
        return { ...r, ...metadata, error: r.error || "Pyright returned no valid JSON diagnostics." };
      }
    } catch (e) {
      return { stdout: "", stderr: "", exit_code: null, candidate_hash, error: String(e) };
    } finally {
      await (0, import_promises.rm)(directory, { recursive: true, force: true });
    }
  };
}
function parsePyright(r, code) {
  if (r.error || r.timed_out || r.signal || ![0, 1].includes(r.exit_code)) return { diagnostics: [], error: r.error || `Pyright process failed (${r.exit_code ?? r.signal}). ${r.stderr}` };
  if (r.candidate_hash && r.candidate_hash !== hashCode(code)) return { diagnostics: [], error: "Pyright result belongs to a different candidate." };
  try {
    const data = JSON.parse(r.stdout);
    if (!Array.isArray(data.generalDiagnostics) || !data.summary || data.summary.filesAnalyzed < 1 || !Number.isInteger(data.summary.errorCount) || data.summary.errorCount < 0 || data.generalDiagnostics.some((d) => typeof d.message !== "string" || !["error", "warning", "information"].includes(d.severity))) throw new Error();
    const errors = data.generalDiagnostics.filter((d) => d.severity === "error").length;
    if (errors !== data.summary.errorCount || r.exit_code === 0 && errors > 0 || r.exit_code === 1 && errors === 0) throw new Error();
    return { diagnostics: data.generalDiagnostics };
  } catch {
    return { diagnostics: [], error: "Missing, malformed or inconsistent Pyright JSON output." };
  }
}
async function verifyIdentifier(code, runPyright, allowPyright = true, extraction) {
  if (!allowPyright) return unknown("identifier", "Pyright is disabled.");
  if (!code.trim()) return unknown("identifier", "No candidate supplied.");
  try {
    const parsed = parsePyright(await runPyright({ python: code }), code);
    if (parsed.error) return unknown("identifier", parsed.error);
    const context = extraction && extraction.candidate_hash === hashCode(code) ? extraction : await extractClaims({ code });
    const apiLines = new Set((context.claims || []).filter((c) => ["import", "method_call", "endpoint"].includes(c.type)).map((c) => Number(c.line) - 1));
    const errors = parsed.diagnostics.filter((d) => d.severity === "error" && !/^report(?:Unused|Unnecessary)/.test(d.rule || ""));
    const onApiLine = (d) => Number.isInteger(d.range?.start?.line) && apiLines.has(d.range.start.line);
    const text2 = (d) => `${d.rule || "syntax/type error"} (line ${(d.range?.start?.line ?? -1) + 1}): ${d.message}`;
    const incorrect = errors.filter((d) => !d.rule || IDENTIFIER_RULES.has(d.rule) || API_SIGNATURE_RULES.has(d.rule) && onApiLine(d));
    const gaps = errors.filter((d) => !incorrect.includes(d) && (EVIDENCE_GAP_RULES.has(d.rule || "") || onApiLine(d)));
    const general = errors.filter((d) => !incorrect.includes(d) && !gaps.includes(d));
    const generalNote = general.length ? "\nGeneral Python diagnostics (not API claims; reported separately, not scored): " + general.map(text2).join("; ") : "";
    if (incorrect.length) return result(
      "identifier",
      "verified_incorrect",
      "tier_4",
      "Pyright structured diagnostics",
      incorrect.map(text2).join("\n") + generalNote,
      "static_identifier_or_type_error"
    );
    if (gaps.length) return unknown("identifier", "Incomplete static evidence for API identifiers: " + gaps.map(text2).join("\n") + generalNote);
    return result(
      "identifier",
      "verified_correct",
      "tier_4",
      "Pyright structured diagnostics",
      "No identifier, attribute or API-call diagnostics in the configured environment (Pyright standard mode). A clean check does not establish REST contracts or task behavior." + generalNote
    );
  } catch (e) {
    return unknown("identifier", `Pyright failed: ${String(e)}`);
  }
}
var import_child_process2, import_promises, import_os, import_path, IDENTIFIER_RULES, API_SIGNATURE_RULES, EVIDENCE_GAP_RULES;
var init_pyrightRunner = __esm({
  "src/pyrightRunner.ts"() {
    "use strict";
    import_child_process2 = require("child_process");
    import_promises = require("fs/promises");
    import_os = require("os");
    import_path = require("path");
    init_verificationTypes();
    init_claimExtractor();
    IDENTIFIER_RULES = /* @__PURE__ */ new Set(["reportAttributeAccessIssue", "reportUndefinedVariable", "reportCallIssue", "reportPrivateImportUsage"]);
    API_SIGNATURE_RULES = /* @__PURE__ */ new Set(["reportArgumentType"]);
    EVIDENCE_GAP_RULES = /* @__PURE__ */ new Set(["reportMissingImports"]);
  }
});

// src/openApiVerifier.ts
function tier(spec) {
  return evidenceOf(spec).kind === "curated" ? "tier_2" : "tier_1";
}
function finish(layer, c, spec, success) {
  const notes = c.notes?.length ? "\nNoncritical: " + [...new Set(c.notes)].join("; ") : "";
  if (c.bad.length) return result(layer, "verified_incorrect", tier(spec), "OpenAPI contract", c.bad.join("\n") + notes, "contract_violation");
  if (c.unknown.length) return unknown(layer, c.unknown.join("\n") + notes);
  return result(layer, "verified_correct", tier(spec), "OpenAPI contract", success + notes);
}
function concrete(v) {
  if (isAbstract(v)) return false;
  if (Array.isArray(v)) return v.every(concrete);
  if (v && typeof v === "object") return Object.values(v).every(concrete);
  return true;
}
function shapeOf(entry, fallbackLabel) {
  if (entry == null) return void 0;
  if (own(entry, "shape")) return entry.shape;
  if (entry.known) return entry.value;
  if (entry.keys_known && entry.fields) return Object.fromEntries(Object.entries(entry.fields).map(([k, v]) => [k, shapeOf(v, k)]));
  return { $ca: "unknown", label: fallbackLabel, type: null };
}
function deref(value, spec) {
  const seen = /* @__PURE__ */ new Set();
  while (value && typeof value === "object" && own(value, "$ref")) {
    const ref = value.$ref;
    if (typeof ref !== "string" || !ref.startsWith("#/")) return { error: "External or invalid $ref is unsupported." };
    if (seen.has(ref)) return { error: "Cyclic reference is unresolved." };
    seen.add(ref);
    let target = spec;
    for (const key of ref.slice(2).split("/").map((k) => k.replace(/~1/g, "/").replace(/~0/g, "~"))) {
      if (!own(target, key)) return { error: `Unresolved reference ${ref}` };
      target = target[key];
    }
    value = target;
  }
  if (!value || typeof value !== "object" || Array.isArray(value)) return { error: "Missing or unsupported schema/object." };
  return { value };
}
function rootServers(spec) {
  if (Array.isArray(spec.servers) && spec.servers.length) return spec.servers;
  const overlay = evidenceOf(spec).servers;
  return Array.isArray(overlay) ? overlay : [];
}
function specProblem(spec) {
  if (!spec) return "No API specification available.";
  if (own(spec, "spec") && !own(spec, "openapi")) return "Received a discovery-result wrapper. Pass its spec field (the OpenAPI document or null), or use a bundled reference with verify_candidate.";
  if (own(spec, "distribution") || own(spec, "import_name")) return "Received a PyPI package datum, not an OpenAPI spec. Pass the spec field from resolve_api_spec (the OpenAPI document) or null.";
  if (own(spec, "note") && !own(spec, "openapi")) return "Received a discovery note, not an OpenAPI document. Pass the spec field from resolve_api_spec or null.";
  if (own(spec, "swagger")) return "Swagger/OpenAPI 2.0 documents are not read as OpenAPI 3.x; convert and review them first.";
  if (!/^3\.[01]\./.test(spec.openapi || "")) return "Only OpenAPI 3.0.x and 3.1.x contracts are supported.";
  if (!spec.paths || typeof spec.paths !== "object" || Array.isArray(spec.paths)) return "Specification has no valid paths map.";
  if (!rootServers(spec).length) return "Specification has no servers array. A spec without a server URL cannot resolve endpoint origins. Supply a reviewed snapshot whose x-confidence-evidence.servers cites the official base URL.";
}
function serverBases(spec, servers) {
  const bases = [];
  let uncertain = false;
  const documentUrl = evidenceOf(spec).document_url;
  for (const server of servers) {
    if (!server || typeof server.url !== "string") {
      uncertain = true;
      continue;
    }
    let urls = [server.url];
    for (const [name] of server.url.matchAll(/\{([^}]+)\}/g)) {
      const variable = server.variables?.[name.slice(1, -1)];
      if (!variable || typeof variable.default !== "string") {
        uncertain = true;
        urls = [];
        break;
      }
      const options = Array.isArray(variable.enum) && variable.enum.length ? variable.enum : [variable.default];
      urls = urls.flatMap((u) => options.map((o) => u.replace(name, o)));
    }
    for (const u of urls) {
      try {
        bases.push(documentUrl ? new URL(u, documentUrl) : new URL(u));
      } catch {
        uncertain = true;
      }
    }
  }
  return { bases, uncertain };
}
function parseTarget(ep) {
  const empty2 = { values: {}, complete: true };
  if (typeof ep.endpoint === "string") {
    let url;
    try {
      url = new URL(ep.endpoint);
    } catch {
      return { query: empty2, display: ep.endpoint, problem: "An absolute endpoint URL is required to establish the server." };
    }
    if (!["http:", "https:"].includes(url.protocol)) return { query: empty2, display: ep.endpoint, problem: "bad-protocol" };
    if (url.username || url.password) return { query: empty2, display: ep.endpoint, problem: "Credentials embedded in URLs are outside supported authentication analysis." };
    const values2 = /* @__PURE__ */ Object.create(null);
    let complete2 = true;
    for (const [k, v] of url.searchParams) {
      if (own(values2, k)) complete2 = false;
      else values2[k] = v;
    }
    const segments2 = url.pathname.split("/").slice(1).map((s) => {
      try {
        return { lit: decodeURIComponent(s) };
      } catch {
        return { mixed: [s] };
      }
    });
    return { origin: url.origin, segments: segments2, query: { values: values2, complete: complete2 }, display: `${url.origin}${url.pathname}` };
  }
  if (!isTemplate(ep.endpoint_template)) return { query: empty2, display: "(dynamic)", problem: "Endpoint or method is dynamic/unresolved." };
  const parts = ep.endpoint_template.parts, holes = [];
  const rendered = parts.map((p) => typeof p === "string" ? p.replace(/\u0000/g, "") : (holes.push(p.hole), HOLE)).join("");
  const display = templateText(ep.endpoint_template);
  const m = /^(https?):\/\/([^/?#\u0000]+)(?=$|[/?#])/i.exec(rendered);
  if (!m) return { query: empty2, display, problem: "The endpoint origin is a runtime value; the server cannot be established." };
  let origin;
  try {
    const u = new URL(m[0]);
    if (u.username || u.password) return { query: empty2, display, problem: "Credentials embedded in URLs are outside supported authentication analysis." };
    origin = u.origin;
  } catch {
    return { query: empty2, display, problem: "Invalid endpoint origin." };
  }
  let rest = rendered.slice(m[0].length).split("#")[0];
  const q = rest.indexOf("?");
  const pathText = q >= 0 ? rest.slice(0, q) : rest, queryText = q >= 0 ? rest.slice(q + 1) : "";
  let holeIndex = 0;
  const fragment = (text2) => {
    const pieces = [];
    text2.split(HOLE).forEach((lit, i, all) => {
      if (lit) pieces.push(lit);
      if (i < all.length - 1) pieces.push({ hole: holes[holeIndex++] ?? "value" });
    });
    if (pieces.length === 1 && typeof pieces[0] !== "string") return { $ca: "unknown", label: pieces[0].hole, type: "str" };
    return pieces.every((p) => typeof p === "string") ? pieces.join("") : { $ca: "template", parts: pieces };
  };
  const segments = (pathText || "/").split("/").slice(1).map((seg) => {
    if (!seg.includes(HOLE)) {
      try {
        return { lit: decodeURIComponent(seg) };
      } catch {
        return { mixed: [seg] };
      }
    }
    const value = fragment(seg);
    return isOpaque(value) ? { hole: value.label } : { mixed: value.parts };
  });
  const values = /* @__PURE__ */ Object.create(null);
  let complete = true;
  for (const pair of queryText ? queryText.split("&") : []) {
    const eq = pair.indexOf("="), key = eq >= 0 ? pair.slice(0, eq) : pair, raw = eq >= 0 ? pair.slice(eq + 1) : "";
    if (key.includes(HOLE)) {
      complete = false;
      fragment(key);
      fragment(raw);
      continue;
    }
    let name;
    try {
      name = decodeURIComponent(key.replace(/\+/g, " "));
    } catch {
      complete = false;
      continue;
    }
    const value = raw.includes(HOLE) ? fragment(raw) : (() => {
      try {
        return decodeURIComponent(raw.replace(/\+/g, " "));
      } catch {
        return raw;
      }
    })();
    if (own(values, name)) complete = false;
    else values[name] = value;
  }
  return { origin, segments, query: { values, complete }, display };
}
function findOperation(spec, endpoint) {
  const problem = specProblem(spec);
  if (problem) return { unknown: problem };
  if (endpoint.resolved === false || typeof endpoint.http_method !== "string" || typeof endpoint.endpoint !== "string" && !isTemplate(endpoint.endpoint_template))
    return { unknown: "Endpoint or method is dynamic/unresolved." };
  const target = parseTarget(endpoint);
  if (target.problem === "bad-protocol") return { bad: "The request does not use an HTTP(S) URL." };
  if (target.problem || !target.segments) return { unknown: target.problem || "Endpoint unresolved." };
  let serverKnown = false, serverMatches = false, uncertainServer = false, prefixUnresolved = false;
  const matches = [];
  for (const pathKey of Object.keys(spec.paths)) {
    const item = deref(spec.paths[pathKey], spec);
    if (item.error) {
      uncertainServer = true;
      continue;
    }
    const pathItem = item.value, operation = pathItem[endpoint.http_method.toLowerCase()];
    const servers = operation?.servers ?? pathItem.servers ?? rootServers(spec);
    if (!Array.isArray(servers) || !servers.length) {
      uncertainServer = true;
      continue;
    }
    const { bases, uncertain } = serverBases(spec, servers);
    if (uncertain) uncertainServer = true;
    for (const base of bases) {
      serverKnown = true;
      if (base.origin !== target.origin) continue;
      const prefix = base.pathname.split("/").filter(Boolean).map((s) => {
        try {
          return decodeURIComponent(s);
        } catch {
          return s;
        }
      });
      const segs = target.segments;
      const head = segs.slice(0, prefix.length);
      if (head.some((s) => !("lit" in s))) {
        prefixUnresolved = true;
        continue;
      }
      if (segs.length < prefix.length || head.some((s, i) => s.lit !== prefix[i])) continue;
      serverMatches = true;
      let rest = segs.slice(prefix.length);
      if (rest.length === 1 && "lit" in rest[0] && rest[0].lit === "") rest = [];
      const keys = pathKey.split("/").slice(1);
      if (pathKey === "/") keys.length = 0;
      if (keys.length !== rest.length || !operation || typeof operation !== "object") continue;
      const params = /* @__PURE__ */ Object.create(null);
      let ok = true;
      keys.forEach((key, i) => {
        if (!ok) return;
        const seg = rest[i], whole = /^\{([^}]+)\}$/.exec(key);
        if (whole) {
          if ("lit" in seg) params[whole[1]] = seg.lit;
          else if ("hole" in seg) params[whole[1]] = { $ca: "unknown", label: seg.hole, type: "str" };
          else params[whole[1]] = { $ca: "template", parts: seg.mixed };
          return;
        }
        if (!key.includes("{")) {
          ok = "lit" in seg && seg.lit === key;
          return;
        }
        if (!("lit" in seg)) {
          ok = false;
          return;
        }
        const names = [];
        const regex = new RegExp("^" + key.split(/(\{[^}]+\})/).map((p) => {
          const n = /^\{([^}]+)\}$/.exec(p);
          if (n) {
            names.push(n[1]);
            return "([^/]+)";
          }
          return p.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
        }).join("") + "$");
        const m = regex.exec(seg.lit);
        if (!m) {
          ok = false;
          return;
        }
        names.forEach((n, j) => {
          params[n] = m[j + 1];
        });
      });
      if (ok) matches.push({ pathKey, operation, pathItem, params, query: target.query, display: target.display });
    }
  }
  if (matches.length) {
    const exact = matches.filter((m) => !m.pathKey.includes("{"));
    const selected = exact.length ? exact : matches;
    if (new Set(selected.map((m) => m.pathKey)).size > 1) return { unknown: "Ambiguous templated path match." };
    return { match: selected[0] };
  }
  if (prefixUnresolved) return { unknown: "The server base path of the endpoint is a runtime value." };
  if (!serverKnown || uncertainServer) return { unknown: "Server identity or operation could not be resolved from the specification." };
  if (!serverMatches) return { bad: `Endpoint origin/base path does not match the declared API servers: ${target.display}` };
  if (evidenceOf(spec).partial) return { unknown: "Operation is outside the curated reference subset." };
  return { bad: `No declared operation matches ${endpoint.http_method} ${target.display}.` };
}
function typesOf(s, spec) {
  if (s.type === void 0) return void 0;
  const list = Array.isArray(s.type) ? s.type : [s.type];
  return s.nullable === true ? [...list, "null"] : list;
}
function schemaProblems(schema, spec) {
  const errors = Object.keys(schema).filter((k) => !supported.has(k) && !k.startsWith("x-")).map((k) => `Unsupported schema constraint: ${k}`);
  if (schema.required !== void 0 && (!Array.isArray(schema.required) || schema.required.some((x) => typeof x !== "string"))) errors.push("Invalid required declaration.");
  if (schema.enum !== void 0 && !Array.isArray(schema.enum)) errors.push("Invalid enum declaration.");
  if (schema.type !== void 0) {
    const list = Array.isArray(schema.type) && (spec === void 0 || isOas31(spec)) ? schema.type : [schema.type];
    if (!list.length || list.some((t) => !TYPES.includes(t) && !(t === "null" && Array.isArray(schema.type)))) errors.push("Unsupported schema type.");
  }
  if (schema.properties !== void 0 && (!schema.properties || typeof schema.properties !== "object" || Array.isArray(schema.properties))) errors.push("Invalid properties declaration.");
  for (const key of ["nullable", "uniqueItems", "readOnly", "writeOnly"]) if (schema[key] !== void 0 && typeof schema[key] !== "boolean") errors.push("Invalid " + key + " declaration.");
  for (const key of ["exclusiveMinimum", "exclusiveMaximum"]) if (schema[key] !== void 0 && typeof schema[key] !== "boolean" && (typeof schema[key] !== "number" || !Number.isFinite(schema[key]))) errors.push("Invalid " + key + " declaration.");
  for (const key of ["minimum", "maximum", "multipleOf", "minLength", "maxLength", "minItems", "maxItems", "minProperties", "maxProperties"]) if (schema[key] !== void 0 && (typeof schema[key] !== "number" || !Number.isFinite(schema[key]))) errors.push("Invalid " + key + " declaration.");
  return errors;
}
function checkValue(value, raw, spec, label, serialized = false, depth = 0) {
  const c = empty();
  if (depth > 30) {
    c.unknown.push(`${label}: schema depth limit`);
    return c;
  }
  const resolved = deref(raw, spec);
  if (resolved.error) {
    c.unknown.push(`${label}: ${resolved.error}`);
    return c;
  }
  const s = resolved.value;
  c.unknown.push(...schemaProblems(s, spec).map((x) => `${label}: ${x}`));
  if (c.unknown.length) return c;
  const types = typesOf(s, spec);
  if (isAbstract(value)) {
    const pyType = isTemplate(value) ? "str" : value.type;
    const jsonTypes = pyType ? PY_TO_JSON[pyType] : void 0;
    if (!serialized && types && jsonTypes && !jsonTypes.some((t) => types.includes(t))) c.bad.push(`${label}: a Python ${pyType} value is sent where the contract expects ${types.join("/")}.`);
    else note(c, `${label}: ${describe(value)} is not statically known; its value constraints are not checked`);
    return c;
  }
  if (value === null && types?.includes("null")) return c;
  let v = value;
  if (serialized && typeof v === "string" && types) {
    if ((types.includes("integer") || types.includes("number")) && !types.includes("string") && /^-?(?:0|[1-9]\d*)(?:\.\d+)?$/.test(v)) v = Number(v);
    if (types.includes("boolean") && !types.includes("string") && ["true", "false"].includes(v)) v = v === "true";
  }
  if (!types) {
    c.unknown.push(`${label}: schema type is unspecified.`);
    return c;
  }
  const matchesType = (type) => type === "string" ? typeof v === "string" : type === "integer" ? Number.isInteger(v) : type === "number" ? typeof v === "number" && Number.isFinite(v) : type === "boolean" ? typeof v === "boolean" : type === "array" ? Array.isArray(v) : type === "object" ? v !== null && typeof v === "object" && !Array.isArray(v) : type === "null" ? v === null : false;
  if (!types.some(matchesType)) {
    c.bad.push(`${label}: expected ${types.join("/")}.`);
    return c;
  }
  if (s.const !== void 0 && JSON.stringify(s.const) !== JSON.stringify(v)) c.bad.push(`${label}: value differs from const.`);
  if (Array.isArray(s.enum) && !s.enum.some((x) => JSON.stringify(x) === JSON.stringify(v))) c.bad.push(`${label}: value is outside enum.`);
  if (typeof s.format === "string" && v !== null) {
    if (INT_FORMATS[s.format] && typeof v === "number") {
      const [lo, hi] = INT_FORMATS[s.format];
      if (v < lo || v > hi) c.bad.push(`${label}: outside ${s.format} range.`);
    } else if (!["float", "double", "int32", "int64"].includes(s.format) || typeof v !== "number") c.unknown.push(`${label}: format ${s.format} is not validated.`);
  }
  if (typeof v === "number") {
    const exMin = typeof s.exclusiveMinimum === "number" ? s.exclusiveMinimum : s.exclusiveMinimum === true ? s.minimum : void 0;
    const exMax = typeof s.exclusiveMaximum === "number" ? s.exclusiveMaximum : s.exclusiveMaximum === true ? s.maximum : void 0;
    if (exMin !== void 0 && v <= exMin || s.minimum !== void 0 && s.exclusiveMinimum !== true && v < s.minimum) c.bad.push(`${label}: below minimum.`);
    if (exMax !== void 0 && v >= exMax || s.maximum !== void 0 && s.exclusiveMaximum !== true && v > s.maximum) c.bad.push(`${label}: above maximum.`);
    if (s.multipleOf !== void 0 && (s.multipleOf <= 0 || Math.abs(v / s.multipleOf - Math.round(v / s.multipleOf)) > 1e-9)) c.bad.push(`${label}: violates multipleOf.`);
  }
  if (typeof v === "string") {
    const length = [...v].length;
    if (s.minLength !== void 0 && length < s.minLength || s.maxLength !== void 0 && length > s.maxLength) c.bad.push(`${label}: invalid string length.`);
    if (typeof s.pattern === "string") {
      try {
        if (!new RegExp(s.pattern, "u").test(v)) c.bad.push(`${label}: pattern mismatch.`);
      } catch {
        c.unknown.push(`${label}: unsupported regular expression.`);
      }
    }
  }
  if (Array.isArray(v)) {
    if (s.minItems !== void 0 && v.length < s.minItems || s.maxItems !== void 0 && v.length > s.maxItems) c.bad.push(`${label}: invalid array length.`);
    if (s.uniqueItems && concrete(v) && new Set(v.map((x) => JSON.stringify(x))).size !== v.length) c.bad.push(`${label}: items are not unique.`);
    v.forEach((x, i) => merge(c, checkValue(x, s.items, spec, `${label}[${i}]`, false, depth + 1)));
  } else if (v && typeof v === "object") {
    if (s.minProperties !== void 0 && Object.keys(v).length < s.minProperties || s.maxProperties !== void 0 && Object.keys(v).length > s.maxProperties) c.bad.push(`${label}: invalid property count.`);
    for (const required of s.required || []) if (!own(v, required) && !deref(s.properties?.[required], spec).value?.readOnly) c.bad.push(`${label}: missing required property ${required}.`);
    for (const [key, val] of Object.entries(v)) {
      if (own(s.properties, key)) {
        if (deref(s.properties[key], spec).value?.readOnly) c.bad.push(`${label}.${key}: readOnly property sent in request.`);
        merge(c, checkValue(val, s.properties[key], spec, `${label}.${key}`, false, depth + 1));
      } else if (s.additionalProperties === false) c.bad.push(`${label}: undeclared property ${key}.`);
      else if (typeof s.additionalProperties === "object") merge(c, checkValue(val, s.additionalProperties, spec, `${label}.${key}`, false, depth + 1));
      else note(c, `${label}: property ${key} is not declared; the schema allows additional properties`);
    }
  }
  return c;
}
function locate(layer, spec, ep) {
  const found = findOperation(spec, ep);
  if (found.match) return { match: found.match };
  return { row: found.bad && layer === "access_point" ? finish(layer, { bad: [found.bad], unknown: [] }, spec, "") : unknown(layer, found.unknown || found.bad || "Operation unresolved.") };
}
async function verifyAccessPoint({ claims, spec }) {
  return aggregateExtracted("access_point", claims, ofType(claims, "endpoint").map((ep) => {
    const l = locate("access_point", spec, ep);
    if (l.row) return l.row;
    const m = l.match, templated = typeof ep.endpoint !== "string";
    return result("access_point", "verified_correct", tier(spec), "OpenAPI servers + path + method", `${ep.http_method} ${m.display} matches the declared server and operation ${ep.http_method} ${m.pathKey}.` + (templated ? "\nNoncritical: runtime path values are assumed to stay within one path segment." : ""));
  }), "No HTTP calls in the supported extraction.");
}
function parameters(match, spec) {
  const map = /* @__PURE__ */ new Map(), errors = [];
  for (const list of [match.pathItem.parameters, match.operation.parameters]) {
    if (list !== void 0 && !Array.isArray(list)) {
      errors.push("Invalid parameter declaration.");
      continue;
    }
    for (const raw of list || []) {
      const p = deref(raw, spec);
      if (p.error) {
        errors.push(p.error);
        continue;
      }
      if (typeof p.value.name !== "string" || !["path", "query", "header", "cookie"].includes(p.value.in)) {
        errors.push("Invalid parameter name/location.");
        continue;
      }
      const key = p.value.in + ":" + (p.value.in === "header" ? p.value.name.toLowerCase() : p.value.name);
      map.set(key, p.value);
    }
  }
  return { values: [...map.values()], errors };
}
function fields(ep, via) {
  const container = ep.request?.[via];
  if (!container) return { values: {}, complete: ep.request_complete === true };
  const shape = shapeOf(container, via);
  if (shape === null) return { values: {}, complete: true };
  if (!shape || typeof shape !== "object" || Array.isArray(shape) || isAbstract(shape)) return { values: {}, complete: false };
  const values = /* @__PURE__ */ Object.create(null);
  for (const [k, v] of Object.entries(shape)) values[via === "headers" ? k.toLowerCase() : k] = v;
  return { values, complete: true };
}
function requestFields(ep, match) {
  const query = fields(ep, "params");
  for (const [key, value] of Object.entries(match.query.values)) {
    if (own(query.values, key)) query.complete = false;
    else query.values[key] = value;
  }
  if (!match.query.complete) query.complete = false;
  return { query, header: fields(ep, "headers"), cookie: fields(ep, "cookies"), path: { values: match.params, complete: true } };
}
function securityNames(spec, operation) {
  const names = { header: /* @__PURE__ */ new Set(["authorization", "content-type", "accept", "user-agent"]), query: /* @__PURE__ */ new Set(), cookie: /* @__PURE__ */ new Set() };
  const requirements = operation.security ?? spec.security ?? [];
  const requiredNames = new Set((Array.isArray(requirements) ? requirements : []).flatMap((r) => Object.keys(r || {})));
  for (const [name, raw] of Object.entries(spec.components?.securitySchemes || {})) {
    if (!requiredNames.has(name)) continue;
    const s = deref(raw, spec).value;
    if (s?.type === "apiKey" && names[s.in] && typeof s.name === "string") names[s.in].add(s.in === "header" ? s.name.toLowerCase() : s.name);
  }
  return names;
}
function jsonSchemaOf(content) {
  if (!content || typeof content !== "object") return { found: false };
  const key = Object.keys(content).find((k) => JSON_MEDIA.test(k));
  return key ? { schema: content[key]?.schema, found: true } : { found: false };
}
function basicAuthShape(shape) {
  if (isOpaque(shape) && /HTTPBasicAuth$/.test(shape.type || "")) return true;
  return Array.isArray(shape) && shape.length === 2 && shape.every((v) => typeof v === "string" || isTemplate(v) || isOpaque(v) && (v.type == null || v.type === "str"));
}
async function verifyInputContract({ claims, spec }) {
  const rows = ofType(claims, "endpoint").map((ep) => {
    const l = locate("input_contract", spec, ep);
    if (l.row) return l.row;
    const m = l.match, c = empty(), pars = parameters(m, spec), sent = requestFields(ep, m);
    c.unknown.push(...pars.errors);
    if (!ep.request || ep.request_complete !== true) c.unknown.push("Request extraction is incomplete; required inputs cannot be established.");
    for (const p of pars.values) {
      const location = sent[p.in], key = p.in === "header" ? p.name.toLowerCase() : p.name;
      const val = location.values[key];
      if (val === void 0 || val === null) {
        if (p.required) (location.complete ? c.bad : c.unknown).push(`Missing required ${p.in} parameter ${p.name}.`);
      } else if (isAbstract(val)) {
        merge(c, checkValue(val, p.schema, spec, `${p.in}.${p.name}`, true));
      } else {
        const schema = deref(p.schema, spec).value, defaultStyle = ["query", "cookie"].includes(p.in) ? "form" : "simple";
        const style = p.style ?? defaultStyle, explode = p.explode ?? style === "form";
        if (p.content || style !== defaultStyle || schema?.type === "object") c.unknown.push(`Unsupported parameter serialization: ${p.name}`);
        else if (schema?.type === "array") {
          const items = typeof val === "string" ? explode ? [val] : val.split(",") : Array.isArray(val) && explode ? val : null;
          if (!items) c.unknown.push(`Parameter ${p.name}: the value's form does not match the declared array serialization (explode=${explode}).`);
          else {
            if (schema.minItems !== void 0 && items.length < schema.minItems || schema.maxItems !== void 0 && items.length > schema.maxItems) c.bad.push(`${p.in}.${p.name}: invalid array length.`);
            items.forEach((x, i) => merge(c, checkValue(x, schema.items, spec, `${p.in}.${p.name}[${i}]`, true)));
          }
        } else merge(c, checkValue(val, p.schema, spec, `${p.in}.${p.name}`, true));
      }
    }
    const authNames = securityNames(spec, m.operation);
    for (const loc of ["query", "header", "cookie"]) {
      if (!sent[loc].complete) c.unknown.push(`${loc} dictionary has unresolved keys.`);
      const declared = new Set(pars.values.filter((p) => p.in === loc).map((p) => loc === "header" ? p.name.toLowerCase() : p.name));
      for (const key of Object.keys(sent[loc].values)) if (!declared.has(key) && !authNames[loc].has(key)) {
        if (loc === "header") note(c, `Undeclared header ${key}; acceptance is undocumented`);
        else c.unknown.push(`Undeclared ${loc} parameter ${key}; acceptance is undocumented.`);
      }
    }
    const auth = ep.request?.auth, authShape = auth?.provided ? shapeOf(auth, "auth") : void 0;
    if (auth?.provided && authShape !== null && !basicAuthShape(authShape)) c.unknown.push("Custom/dynamic request authentication is outside the supported subset.");
    const rb = deref(m.operation.requestBody, spec);
    const body = ep.request?.json, form = ep.request?.data;
    const bodyShape = body?.provided ? shapeOf(body, "json") : void 0, formShape = form?.provided ? shapeOf(form, "data") : void 0;
    if (body?.provided && bodyShape !== null) {
      const contentType = sent.header.values["content-type"];
      if (contentType !== void 0 && typeof contentType !== "string") c.unknown.push("Request Content-Type is unresolved.");
      else if (typeof contentType === "string" && contentType.split(";")[0].trim().toLowerCase() !== "application/json") c.bad.push("JSON body sent with a non-JSON Content-Type.");
    }
    if (form?.provided && formShape !== null) c.unknown.push("Form/raw body encoding is unsupported.");
    if (m.operation.requestBody) {
      if (rb.error) c.unknown.push(rb.error);
      else {
        if (rb.value.required && (!body?.provided || bodyShape === null) && !(form?.provided && formShape !== null)) c.bad.push("Required request body is missing.");
        if (body?.provided && bodyShape !== null) {
          const { schema } = jsonSchemaOf(rb.value.content);
          if (!schema) c.unknown.push("No JSON request schema available.");
          else if (isAbstract(bodyShape) || bodyShape === void 0) c.unknown.push("Request body is unresolved.");
          else merge(c, checkValue(bodyShape, schema, spec, "body"));
        }
      }
    } else if (body?.provided && bodyShape !== null) c.unknown.push("Code sends a JSON body with no declared request-body contract.");
    return finish("input_contract", c, spec, `Required inputs, locations and supported value constraints checked for ${ep.call_id} (${m.pathKey}).`);
  });
  return aggregateExtracted("input_contract", claims, rows, "No HTTP calls; no input contract to check.");
}
function schemaView(raw, spec, depth = 0) {
  const v = { properties: {}, required: /* @__PURE__ */ new Set(), additional: void 0, nullable: false, writeOnly: false, problems: [] };
  if (depth > 20) {
    v.problems.push("Schema composition depth limit.");
    return v;
  }
  let s = raw;
  if (isOas31(spec) && s && typeof s === "object" && own(s, "$ref") && Object.keys(s).some((k) => !["$ref", "description", "summary"].includes(k))) {
    const { $ref, ...siblings } = s;
    s = { allOf: [{ $ref }, siblings] };
  }
  const r = deref(s, spec);
  if (r.error) {
    v.problems.push(r.error);
    return v;
  }
  s = r.value;
  const { allOf, oneOf, anyOf, discriminator, ...rest } = s;
  const union = oneOf ?? anyOf;
  const structural = Object.keys(rest).filter((k) => ["properties", "items", "additionalProperties", "required"].includes(k));
  if (union !== void 0 && (structural.length || allOf !== void 0 || !Array.isArray(union))) {
    v.problems.push("Unsupported schema constraint: " + (oneOf !== void 0 ? "oneOf" : "anyOf") + " combined with other structure.");
    return v;
  }
  if (union !== void 0) {
    v.alternatives = union;
    v.nullable = rest.nullable === true || Array.isArray(rest.type) && rest.type.includes("null");
    return v;
  }
  v.problems.push(...schemaProblems(rest, spec));
  v.types = typesOf(rest, spec);
  v.nullable = v.types?.includes("null") ?? false;
  v.writeOnly = rest.writeOnly === true;
  Object.assign(v.properties, rest.properties || {});
  for (const k of rest.required || []) v.required.add(k);
  v.additional = rest.additionalProperties;
  v.items = rest.items;
  if (allOf !== void 0) {
    if (!Array.isArray(allOf)) {
      v.problems.push("Invalid allOf declaration.");
      return v;
    }
    for (const member of allOf) {
      const m = schemaView(member, spec, depth + 1);
      v.problems.push(...m.problems);
      if (m.alternatives) {
        v.problems.push("Unsupported schema constraint: union inside allOf.");
        continue;
      }
      if (m.types) v.types = v.types ? v.types.filter((t) => m.types.includes(t) || t === "number" && m.types.includes("integer")) : m.types;
      Object.assign(v.properties, m.properties);
      m.required.forEach((k) => v.required.add(k));
      v.items ??= m.items;
      if (m.nullable && (!v.types || v.types.includes("null"))) v.nullable = true;
    }
    if (v.additional === false) v.additional = void 0;
  }
  if (!v.types && Object.keys(v.properties).length) v.types = ["object"];
  return v;
}
function stepInto(view, key, spec, optional) {
  const c = empty();
  if (view.problems.length) {
    c.unknown.push(...view.problems);
    return { c, next: [] };
  }
  if (view.alternatives) {
    const results = view.alternatives.map((a) => stepInto(schemaView(a, spec), key, spec, optional));
    const ok = results.filter((r) => !r.c.bad.length && !r.c.unknown.length);
    if (ok.length === results.length) {
      results.forEach((r) => merge(c, { bad: [], unknown: [], notes: r.c.notes }));
      return { c, next: results.flatMap((r) => r.next) };
    }
    if (results.every((r) => r.c.bad.length)) {
      c.bad.push(...new Set(results.flatMap((r) => r.c.bad)));
      return { c, next: [] };
    }
    c.unknown.push(`Response field ${JSON.stringify(key)} is documented in only some schema alternatives.`);
    return { c, next: [] };
  }
  if (!view.types) {
    c.unknown.push("Response schema type is unspecified.");
    return { c, next: [] };
  }
  if (view.nullable) note(c, "a response container on this path can be null");
  if (typeof key === "number" || key === "*" && view.types.includes("array") && !view.types.includes("object")) {
    if (!view.types.includes("array")) {
      c.bad.push("Array indexing used on a non-array response.");
      return { c, next: [] };
    }
    if (typeof key === "number" && !Number.isInteger(key)) {
      c.unknown.push("Non-integer response index.");
      return { c, next: [] };
    }
    if (view.items === void 0) {
      c.unknown.push("Array item schema is unspecified.");
      return { c, next: [] };
    }
    return { c, next: [view.items] };
  }
  if (key === "*") {
    c.unknown.push("Dynamic response field is unresolved.");
    return { c, next: [] };
  }
  if (!view.types.includes("object")) {
    c.bad.push(view.types.includes("array") ? `String field ${key} read directly from an array.` : `Field ${key} read from a scalar response.`);
    return { c, next: [] };
  }
  if (!own(view.properties, key)) {
    if (view.additional === false) c.bad.push(`Response field ${key} is forbidden by the closed schema.`);
    else c.unknown.push(`Response field ${key} is not documented; schema allows unspecified properties.`);
    return { c, next: [] };
  }
  if (!optional && !view.required.has(key)) note(c, `response field ${key} is optional in the contract; presence is not guaranteed`);
  const child = schemaView(view.properties[key], spec);
  if (child.writeOnly) c.unknown.push(`Response field ${key} is writeOnly.`);
  return { c, next: [view.properties[key]] };
}
function checkOutputPath(path, raw, spec, optional = false) {
  const c = empty();
  let schemas = [raw];
  for (const [i, key] of path.entries()) {
    const steps = schemas.map((s) => stepInto(schemaView(s, spec), key, spec, optional && i === path.length - 1));
    steps.forEach((s) => merge(c, s.c));
    if (c.bad.length || c.unknown.length) return c;
    schemas = steps.flatMap((s) => s.next);
  }
  return c;
}
async function verifyOutputContract({ claims, spec, code }, runPyright, allowPyright = true) {
  const outputs = ofType(claims, "output_field");
  if (!outputs.length) return aggregateExtracted("output_contract", claims, [], "No tracked response-field accesses.");
  const rows = [];
  for (const f of outputs) {
    const ep = ofType(claims, "endpoint").find((e) => e.call_id === f.call_id);
    if (!ep) {
      rows.push(unknown("output_contract", "Response access is not linked to an HTTP operation."));
      continue;
    }
    const l = locate("output_contract", spec, ep);
    if (l.row) {
      rows.push(l.row);
      continue;
    }
    const responses = l.match.operation.responses || {};
    const success = Object.entries(responses).filter(([k]) => /^2\d\d$/.test(k) || k === "2XX");
    if (!success.length) {
      rows.push(unknown("output_contract", "No documented success-response schema; a default/error response is insufficient."));
      continue;
    }
    const checks = success.map(([status, raw]) => {
      const r = deref(raw, spec);
      if (r.error) return { bad: [], unknown: [r.error] };
      const { schema } = jsonSchemaOf(r.value.content);
      if (!schema) return { bad: [], unknown: [`No JSON schema for success status ${status}.`] };
      return checkOutputPath(Array.isArray(f.path) ? f.path : [f.field], schema, spec, f.optional_access === true);
    });
    const combined = empty();
    if (checks.every((c) => c.bad.length)) combined.bad.push(...checks.flatMap((c) => c.bad));
    else {
      combined.unknown.push(...checks.flatMap((c) => c.unknown));
      if (checks.some((c) => c.bad.length)) combined.unknown.push("Field validity depends on an unresolved success status.");
    }
    checks.forEach((c) => {
      if (c.notes?.length) (combined.notes ||= []).push(...c.notes);
    });
    rows.push(finish("output_contract", combined, spec, `Response path ${JSON.stringify(f.path || [f.field])} is documented for ${f.call_id} (${l.match.pathKey}).`));
  }
  const verdict = aggregateExtracted("output_contract", claims, rows, "No output checks.");
  if (verdict.state === "unverifiable" && code && runPyright && allowPyright) {
    try {
      const p = parsePyright(await runPyright({ python: code }), code);
      verdict.evidence_detail += "\n" + (p.error ? `Pyright unavailable: ${p.error}` : "Pyright cannot establish untyped JSON response contracts; result remains unverifiable.");
    } catch (e) {
      verdict.evidence_detail += `
Pyright unavailable: ${String(e)}`;
    }
  }
  return verdict;
}
function authCheck(name, scopes, ep, match, spec) {
  const c = empty(), resolved = deref(spec.components?.securitySchemes?.[name], spec);
  if (resolved.error) {
    c.unknown.push(`Security scheme ${name}: ${resolved.error}`);
    return c;
  }
  const s = resolved.value, sent = requestFields(ep, match);
  let val, complete = false;
  if (Array.isArray(scopes) && scopes.length) note(c, `required scopes (${scopes.join(", ")}) belong to the ${name} token and cannot be checked statically; the credential is assumed to carry them`);
  if (s.type === "apiKey" && ["header", "query", "cookie"].includes(s.in)) {
    const loc = sent[s.in];
    val = loc.values[s.in === "header" ? String(s.name).toLowerCase() : s.name];
    complete = loc.complete;
    if (isAbstract(val)) note(c, `credential ${name} is placed as documented; its runtime value is not tested`);
  } else if (s.type === "http" && ["bearer", "basic"].includes(s.scheme?.toLowerCase()) || s.type === "oauth2" || s.type === "openIdConnect") {
    const scheme = s.type === "http" ? s.scheme.toLowerCase() : "bearer", label = s.type === "http" ? s.scheme : `${s.type} Bearer token`;
    val = sent.header.values.authorization;
    complete = sent.header.complete;
    if (val === void 0 && ep.request?.auth?.provided) {
      if (scheme === "basic" && basicAuthShape(shapeOf(ep.request.auth, "auth"))) return note(c, `basic credentials are supplied through requests auth; their validity is not tested`);
      c.unknown.push("Authentication adapter/value could not be established.");
      return c;
    }
    if (typeof val === "string") {
      if (!SCHEME_PREFIX[scheme].test(val.trim() ? val : "")) c.bad.push(`Authorization header does not match ${label}.`);
    } else if (isTemplate(val)) {
      const first = val.parts[0];
      if (typeof first !== "string") c.unknown.push(`The Authorization scheme is a runtime value; ${label} placement cannot be established.`);
      else if (scheme === "bearer" ? !/^Bearer\s+$/i.test(first) && !/^Bearer\s+\S/i.test(first) : !/^Basic\s+/i.test(first)) c.bad.push(`Authorization header does not match ${label}.`);
      else note(c, `the ${label} credential is a runtime value; its validity is not tested`);
      return c;
    } else if (isOpaque(val)) {
      c.unknown.push(`Credential ${name} has an unresolved runtime value; the ${label} scheme cannot be established.`);
      return c;
    }
  } else {
    c.unknown.push(`Unsupported authentication scheme/scopes: ${name} (${s.type}).`);
    return c;
  }
  if (val === void 0 || val === null) (complete ? c.bad : c.unknown).push(`Required credential ${name} is absent from the request.`);
  else if (typeof val === "string" && !val.trim()) c.bad.push(`Credential ${name} is empty or invalid.`);
  else if (!isAbstract(val) && typeof val !== "string") c.bad.push(`Credential ${name} is empty or invalid.`);
  return c;
}
async function verifyContextual({ claims, spec }) {
  const rows = ofType(claims, "endpoint").map((ep) => {
    const l = locate("contextual", spec, ep);
    if (l.row) return l.row;
    const m = l.match, security = m.operation.security ?? spec.security ?? [];
    if (!Array.isArray(security)) return unknown("contextual", "Invalid security requirements.");
    if (m.operation.deprecated) return unknown("contextual", "Operation is deprecated; task-specific acceptability needs review.");
    if (!security.length || security.some((s) => s && typeof s === "object" && !Array.isArray(s) && !Object.keys(s).length)) return result("contextual", "not_applicable", "none", "OpenAPI operation security", "No authentication requirement for this operation. Unused security definitions are not requirements.");
    const alternatives = security.map((requirement) => {
      const c = empty();
      if (!requirement || typeof requirement !== "object" || Array.isArray(requirement)) {
        c.unknown.push("Invalid security alternative.");
        return c;
      }
      for (const [name, scopes] of Object.entries(requirement)) merge(c, authCheck(name, scopes, ep, m, spec));
      return c;
    });
    const satisfied = alternatives.find((c) => !c.bad.length && !c.unknown.length);
    if (satisfied) return finish("contextual", { bad: [], unknown: [], notes: satisfied.notes }, spec, "Required authentication placement and static shape match one security alternative. Credential validity is not tested.");
    if (alternatives.every((c) => c.bad.length)) return finish("contextual", { bad: alternatives.flatMap((c) => c.bad), unknown: [] }, spec, "");
    return unknown("contextual", alternatives.flatMap((c) => [...c.bad, ...c.unknown]).join("\n"));
  });
  return aggregateExtracted("contextual", claims, rows, "No HTTP calls requiring contextual checks.");
}
var empty, note, merge, own, evidenceOf, isMarker, isOpaque, isTemplate, isAbstract, templateText, describe, PY_TO_JSON, isOas31, HOLE, supported, TYPES, INT_FORMATS, JSON_MEDIA, SCHEME_PREFIX;
var init_openApiVerifier = __esm({
  "src/openApiVerifier.ts"() {
    "use strict";
    init_verificationTypes();
    init_pyrightRunner();
    empty = () => ({ bad: [], unknown: [] });
    note = (c, text2) => {
      (c.notes ||= []).push(text2);
      return c;
    };
    merge = (a, b) => {
      a.bad.push(...b.bad);
      a.unknown.push(...b.unknown);
      if (b.notes?.length) (a.notes ||= []).push(...b.notes);
      return a;
    };
    own = (v, k) => v != null && typeof v === "object" && Object.hasOwn(v, k);
    evidenceOf = (spec) => spec && typeof spec === "object" && spec["x-confidence-evidence"] || {};
    isMarker = (v, kind) => v != null && typeof v === "object" && !Array.isArray(v) && v.$ca === kind;
    isOpaque = (v) => isMarker(v, "unknown");
    isTemplate = (v) => isMarker(v, "template");
    isAbstract = (v) => isOpaque(v) || isTemplate(v);
    templateText = (t) => (t.parts || []).map((p) => typeof p === "string" ? p : `{${p.hole}}`).join("");
    describe = (v) => isTemplate(v) ? `template "${templateText(v)}"` : isOpaque(v) ? `runtime value ${v.label || ""}`.trim() : JSON.stringify(v);
    PY_TO_JSON = { str: ["string"], int: ["integer", "number"], float: ["number"], bool: ["boolean"], dict: ["object"], list: ["array"], NoneType: ["null"] };
    isOas31 = (spec) => /^3\.1\./.test(spec?.openapi || "");
    HOLE = "\0";
    supported = /* @__PURE__ */ new Set([
      "type",
      "properties",
      "required",
      "items",
      "additionalProperties",
      "enum",
      "nullable",
      "minimum",
      "maximum",
      "exclusiveMinimum",
      "exclusiveMaximum",
      "minLength",
      "maxLength",
      "pattern",
      "minItems",
      "maxItems",
      "uniqueItems",
      "minProperties",
      "maxProperties",
      "multipleOf",
      "title",
      "description",
      "default",
      "example",
      "examples",
      "deprecated",
      "readOnly",
      "writeOnly",
      "xml",
      "externalDocs",
      "format",
      // JSON Schema 2020-12 annotations used by OpenAPI 3.1 documents.
      "const",
      "$schema",
      "$id",
      "$comment",
      "$anchor",
      "contentMediaType",
      "contentEncoding",
      "$defs"
    ]);
    TYPES = ["object", "array", "string", "integer", "number", "boolean"];
    INT_FORMATS = { int32: [-(2 ** 31), 2 ** 31 - 1], int64: [Number.MIN_SAFE_INTEGER, Number.MAX_SAFE_INTEGER] };
    JSON_MEDIA = /^application\/(?:[\w.+-]+\+)?json\s*(?:;.*)?$/i;
    SCHEME_PREFIX = { bearer: /^Bearer\s+\S/i, basic: /^Basic\s+[A-Za-z0-9+/]+=*$/i };
  }
});

// src/verificationPolicy.ts
function computeEwcs({ layer_results, task_id = "candidate", extraction_complete = false, failed_layers = [] }) {
  const acc = new EWCSAccumulator(task_id, extraction_complete, failed_layers);
  for (const r of layer_results) acc.record(r);
  return acc.finalise();
}
function makeDecision(report, correctionAttempts = 0, policy = DEFAULT_POLICY) {
  try {
    if (!report || !Array.isArray(report.contributions)) return "abstain";
    const acc = new EWCSAccumulator(report.task_id);
    for (const c of report.contributions) acc.record({ ...c, evidence_source: "report", evidence_detail: "", hallucination_type: null });
    const checked = acc.finalise();
    if (checked.has_incorrect_layer) return correctionAttempts < 1 ? "correct" : "abstain";
    if (!Array.isArray(report.missing_layers) || report.missing_layers.length || !Array.isArray(report.failed_layers) || report.failed_layers.length || checked.missing_layers.length || checked.ewcs === null || !Number.isFinite(report.ewcs) || report.ewcs !== checked.ewcs) return "abstain";
    if (policy.uncertainty_gate !== false && (report.extraction_complete !== true || checked.unverifiable_layers.length)) return "abstain";
    return checked.ewcs >= policy.deliver_threshold ? "deliver" : checked.ewcs >= policy.flag_threshold ? "deliver_with_flag" : "abstain";
  } catch {
    return "abstain";
  }
}
function presentReport({ code, ewcs_report, decision, policy = DEFAULT_POLICY }) {
  const safeCode = typeof code === "string" ? code : "";
  if (!ewcs_report || typeof ewcs_report !== "object") {
    return {
      report: "### Confidence Agent Report\n\n**Decision:** abstain\n\n**Reason:** Malformed or missing EWCS report.\n\nCode withheld pending successful verification.",
      decision: "abstain",
      code_included: false
    };
  }
  const show = (v) => typeof v === "number" && Number.isFinite(v) ? round(v) : "undefined";
  const checked = makeDecision(ewcs_report, 0, policy);
  const candidateMatches = ewcs_report.candidate_hash === hashCode(safeCode);
  const allowed = candidateMatches && ["deliver", "deliver_with_flag"].includes(checked) && ["deliver", "deliver_with_flag"].includes(decision);
  const actual = allowed ? checked : checked === "correct" && decision !== "abstain" ? "correct" : "abstain";
  const reason = allowed ? null : !candidateMatches ? typeof ewcs_report.candidate_hash !== "string" ? "This score report is not bound to any code (no candidate_hash). Reports assembled from the individual layer tools can be inspected but cannot authorize delivery; only verify_candidate binds a report to the exact code." : "This score report belongs to different code (candidate_hash mismatch). The code must be verified exactly as it will be delivered." : checked === "correct" ? "A layer verified a contradiction; a correction is required." : !["deliver", "deliver_with_flag"].includes(decision) ? `The caller requested ${decision}.` : "The decision policy withheld delivery (see unverifiable layers, extraction and thresholds below).";
  const lines = [
    "### Confidence Agent Report",
    "",
    `**Decision:** ${actual}`,
    ...reason ? [`**Reason:** ${reason}`] : [],
    `**EWCS:** ${ewcs_report.ewcs ?? "undefined (no applicable evidence)"} (signed: ${ewcs_report.signed_score ?? "undefined"}, applicable weight: ${ewcs_report.total_applicable_weight ?? "undefined"})`,
    "",
    "| Layer | State | Tier | Weight | Factor | Positive | Signed |",
    "|---|---|---|---|---|---|---|"
  ];
  for (const c of Array.isArray(ewcs_report.contributions) ? ewcs_report.contributions : []) {
    if (!c || typeof c !== "object") continue;
    lines.push(`| ${c.layer ?? "?"} | ${c.state ?? "?"} | ${c.tier ?? "?"} | ${c.weight ?? "?"} | ${c.tier_factor ?? "?"} | ${show(c.positive_contribution)} | ${show(c.signed_contribution)} |`);
  }
  lines.push("", "Scope: API-claim and static evidence only. EWCS is not a probability of correctness. Task behavior has not been independently checked by this verifier.");
  lines.push("", `Policy ${POLICY_VERSION}: thresholds ${policy.deliver_threshold}/${policy.flag_threshold}, uncertainty gate ${policy.uncertainty_gate !== false ? "on" : "OFF (exploratory)"}.`);
  if (Array.isArray(ewcs_report.layer_results) && ewcs_report.layer_results.length) {
    lines.push("", "Evidence:", "");
    for (const r of ewcs_report.layer_results) {
      if (!r || typeof r !== "object") continue;
      const detail = typeof r.evidence_detail === "string" ? r.evidence_detail : "(no detail)";
      lines.push(`- ${r.layer ?? "?"}: ${detail.replace(/\n/g, " ")}`);
    }
  }
  if (Array.isArray(ewcs_report.missing_layers) && ewcs_report.missing_layers.length) lines.push("", `Missing layers: ${ewcs_report.missing_layers.join(", ")}`);
  if (Array.isArray(ewcs_report.unverifiable_layers) && ewcs_report.unverifiable_layers.length) lines.push("", `Unverifiable layers: ${ewcs_report.unverifiable_layers.join(", ")}`);
  if (!ewcs_report.extraction_complete) lines.push("", "Extraction was incomplete or failed.");
  if (actual === "deliver_with_flag") lines.push("", "Flag: some checks rely on supporting static or package metadata evidence; the code was not executed.");
  if (allowed) {
    const fence = "`".repeat(Math.max(3, ...(safeCode.match(/`+/g) || []).map((s) => s.length + 1)));
    lines.push("", fence + "python", safeCode, fence);
  } else lines.push("", "Code withheld pending successful verification.");
  return { report: lines.join("\n"), decision: actual, code_included: allowed };
}
var round, EWCSAccumulator, POLICY_VERSION, DEFAULT_POLICY;
var init_verificationPolicy = __esm({
  "src/verificationPolicy.ts"() {
    "use strict";
    init_verificationTypes();
    round = (v) => Math.round(v * 1e4) / 1e4;
    EWCSAccumulator = class {
      constructor(taskId, extractionComplete = false, failed = []) {
        this.taskId = taskId;
        this.extractionComplete = extractionComplete;
        this.failed = failed;
      }
      taskId;
      extractionComplete;
      failed;
      results = /* @__PURE__ */ new Map();
      report = null;
      get isComplete() {
        return this.report !== null;
      }
      record(r) {
        if (this.report) throw new Error("Cannot record after finalise().");
        if (!Object.hasOwn(LAYER_WEIGHTS, r.layer)) throw new Error(`Unknown layer: ${r.layer}`);
        if (this.results.has(r.layer)) throw new Error(`Duplicate layer: ${r.layer}`);
        if (r.weight !== LAYER_WEIGHTS[r.layer]) throw new Error(`Incorrect weight for ${r.layer}`);
        if (!["verified_correct", "verified_incorrect", "unverifiable", "not_applicable"].includes(r.state)) throw new Error(`Invalid state: ${r.state}`);
        if (!Object.hasOwn(TIER_FACTORS, r.tier)) throw new Error(`Invalid tier: ${r.tier}`);
        if (r.state.startsWith("verified_") && r.tier === "none") throw new Error("Verified results require evidence.");
        if (["unverifiable", "not_applicable"].includes(r.state) && r.tier !== "none") throw new Error("Unverified results must use tier none.");
        this.results.set(r.layer, { ...r });
      }
      finalise() {
        if (this.report) return structuredClone(this.report);
        const missing = ALL_LAYERS.filter((l) => !this.results.has(l));
        const rows = ALL_LAYERS.map((l) => this.results.get(l) || result(l, "unverifiable", "none", "controller", "Required layer did not report."));
        const contributions = rows.map((r) => {
          const factor = TIER_FACTORS[r.tier];
          return {
            layer: r.layer,
            state: r.state,
            tier: r.tier,
            weight: r.weight,
            tier_factor: factor,
            positive_contribution: r.state === "verified_correct" ? round(r.weight * factor) : 0,
            signed_contribution: r.state === "verified_correct" ? round(r.weight * factor) : r.state === "verified_incorrect" ? round(-r.weight * factor) : 0
          };
        });
        const applicable = contributions.filter((c) => c.state !== "not_applicable");
        const total = applicable.reduce((s, c) => s + c.weight, 0), positive = round(applicable.reduce((s, c) => s + c.positive_contribution, 0));
        this.report = {
          task_id: this.taskId,
          ewcs: total ? round(positive / total) : null,
          signed_score: total ? round(applicable.reduce((s, c) => s + c.signed_contribution, 0) / total) : null,
          has_incorrect_layer: applicable.some((c) => c.state === "verified_incorrect"),
          total_applicable_weight: total,
          positive_weight: positive,
          contributions,
          missing_layers: missing,
          extraction_complete: this.extractionComplete,
          failed_layers: [...this.failed],
          unverifiable_layers: rows.filter((r) => r.state === "unverifiable").map((r) => r.layer),
          layer_results: rows
        };
        return structuredClone(this.report);
      }
    };
    POLICY_VERSION = "2026-09-25.1";
    DEFAULT_POLICY = Object.freeze({ uncertainty_gate: true, deliver_threshold: 0.85, flag_threshold: 0.6 });
  }
});

// src/verificationController.ts
async function verifyCandidate(request, deps = {}) {
  const code = request.code, candidate_hash = hashCode(code), snapshot = structuredClone(request.spec), bindings = structuredClone(request.input_bindings || {});
  let extraction;
  try {
    extraction = await (deps.extract || extractClaims)({ code, input_bindings: bindings });
  } catch (e) {
    extraction = { claims: [], complete: false, issues: [], error: String(e) };
  }
  if (!extraction || !Array.isArray(extraction.claims) || typeof extraction.complete !== "boolean") extraction = { claims: [], complete: false, issues: [], error: "Malformed extractor response." };
  if (extraction.candidate_hash && extraction.candidate_hash !== candidate_hash) extraction = { claims: [], complete: false, issues: [], error: "Extraction candidate hash mismatch." };
  if (extraction.error) extraction.complete = false;
  const packages = /* @__PURE__ */ Object.create(null);
  for (const imp of ofType(extraction.claims, "import")) {
    const name = String(imp.library || "").split(".")[0];
    if (imp.stdlib || imp.local || Object.hasOwn(packages, name)) continue;
    try {
      packages[name] = await (deps.lookupPackage || ((name2) => queryPypi({ library_name: name2 })))(name);
    } catch (e) {
      packages[name] = { exists: null, status: "unverifiable", summary: String(e) };
    }
  }
  let pyright = null, pyrightPromise = null;
  const run = deps.runPyright || createPyrightRunner();
  const cached = (p) => {
    if (p.python !== code) throw new Error("Checker must analyze the exact candidate.");
    if (!pyrightPromise) pyrightPromise = run(p).then((r) => {
      pyright = r;
      return r;
    });
    return pyrightPromise;
  };
  const claims = extraction.claims;
  const actions = {
    interface: () => verifyInterface({ claims, pypi_data: packages }),
    identifier: () => verifyIdentifier(code, cached, deps.allowPyright !== false, extraction),
    access_point: () => verifyAccessPoint({ claims, spec: snapshot }),
    input_contract: () => verifyInputContract({ claims, spec: snapshot }),
    output_contract: () => verifyOutputContract({ claims, spec: snapshot, code }, cached, deps.allowPyright !== false),
    contextual: () => verifyContextual({ claims, spec: snapshot })
  };
  const failed = [], layers = [];
  const limits = extractionLimits(extraction);
  for (const layer of ALL_LAYERS) {
    try {
      let r = await actions[layer]();
      if (!r || r.layer !== layer) throw new Error("Missing/mismatched layer result.");
      if (limits.layers.has(layer) && r.state === "not_applicable") r = unknown(layer, "Extraction was incomplete for this layer; absence of relevant claims does not establish inapplicability.");
      layers.push(r);
    } catch (e) {
      failed.push(layer);
      layers.push(unknown(layer, `Required verifier failed: ${String(e)}`));
    }
  }
  const ewcs_report = computeEwcs({ layer_results: layers, task_id: request.task_id, extraction_complete: extraction.complete, failed_layers: failed });
  ewcs_report.candidate_hash = candidate_hash;
  return {
    candidate_hash,
    spec_hash: hashCode(JSON.stringify(snapshot ?? null)),
    bindings_hash: hashCode(JSON.stringify(bindings)),
    extraction,
    layers,
    ewcs_report,
    decision: makeDecision(ewcs_report, 0, deps.policy ?? DEFAULT_POLICY),
    evidence: { packages, pyright }
  };
}
async function runIntervention(request, deps = {}) {
  const frozen = { ...request, spec: structuredClone(request.spec), input_bindings: structuredClone(request.input_bindings || {}) };
  const attempts = [{ code: request.code, verification: await verifyCandidate(frozen, deps) }];
  let correction_error = null;
  if (attempts[0].verification.decision === "correct" && deps.correct) {
    try {
      const revised = await deps.correct({ code: request.code, verification: structuredClone(attempts[0].verification), spec: structuredClone(frozen.spec), input_bindings: structuredClone(frozen.input_bindings) });
      if (typeof revised !== "string" || !revised.trim()) throw new Error("Correction produced no code.");
      attempts.push({ code: revised, verification: await verifyCandidate({ ...frozen, code: revised }, deps) });
    } catch (e) {
      correction_error = String(e);
    }
  }
  const last = attempts[attempts.length - 1], raw = makeDecision(last.verification.ewcs_report, attempts.length - 1, deps.policy ?? DEFAULT_POLICY);
  const decision = raw === "correct" || correction_error ? "abstain" : raw;
  const rendered = presentReport({ code: last.code, ewcs_report: last.verification.ewcs_report, decision, policy: deps.policy ?? DEFAULT_POLICY });
  return {
    decision: rendered.decision,
    delivered_code: rendered.code_included ? last.code : null,
    report: rendered.report,
    attempts,
    correction_attempted: attempts[0].verification.decision === "correct" && !!deps.correct,
    correction_error
  };
}
var init_verificationController = __esm({
  "src/verificationController.ts"() {
    "use strict";
    init_claimExtractor();
    init_packageEvidence();
    init_pyrightRunner();
    init_openApiVerifier();
    init_verificationPolicy();
    init_verificationTypes();
  }
});

// src/bundledReferences.ts
var TOOLBOX_VERSION, BUNDLED_REFERENCES;
var init_bundledReferences = __esm({
  "src/bundledReferences.ts"() {
    "use strict";
    TOOLBOX_VERSION = "3.0.0";
    BUNDLED_REFERENCES = { "jsonplaceholder-posts": { "openapi": "3.0.3", "info": { "title": "JSONPlaceholder posts: reviewed partial reference", "version": "2026-09-24.1" }, "servers": [{ "url": "https://jsonplaceholder.typicode.com" }], "x-confidence-evidence": { "kind": "curated", "partial": true, "source_url": "https://jsonplaceholder.typicode.com/guide/", "source_urls": ["https://jsonplaceholder.typicode.com/guide/", "https://jsonplaceholder.typicode.com/"], "prepared_at": "2026-09-24", "reviewed_at": "2026-09-24", "review_method": "Manual comparison by coding assistant with provider guide and routes page; not provider certification or independent team approval.", "coverage": ["GET /posts without filters", "GET /posts/1"], "note": "Partial secondary reference at tier 2, not provider-published OpenAPI. Example property types are modeled; universal field presence is not asserted. Other operations and supplied undocumented inputs remain unresolved.", "assumptions": ["200 application/json models the documented successful examples; other success/error statuses are not specified.", "Public unauthenticated GET access follows provider examples, not a formal security guarantee.", "Example property types describe the documented examples; they are not a complete provider schema."], "review_document": "examples/JSONPLACEHOLDER_REFERENCE_REVIEW.md" }, "paths": { "/posts": { "get": { "responses": { "200": { "description": "Documented successful JSON response", "content": { "application/json": { "schema": { "type": "array", "items": { "$ref": "#/components/schemas/Post" } } } } } } } }, "/posts/1": { "get": { "responses": { "200": { "description": "Documented successful JSON response", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/Post" } } } } } } } }, "components": { "schemas": { "Post": { "type": "object", "properties": { "id": { "type": "integer" }, "userId": { "type": "integer" }, "title": { "type": "string" }, "body": { "type": "string" } } } } }, "security": [] } };
  }
});

// src/evidenceRegistry.ts
function registryRoot() {
  const candidates = [process.env.CONFIDENCE_EVIDENCE_ROOT, (0, import_path2.resolve)(__dirname, ".."), process.cwd()].filter(Boolean);
  return candidates.find((root) => (0, import_fs.existsSync)((0, import_path2.join)(root, "evidence", "registry.json"))) ?? null;
}
function templateHead(t) {
  return Array.isArray(t?.parts) && typeof t.parts[0] === "string" ? t.parts[0] : "";
}
function hostOf(url) {
  return /^https?:\/\/([^/?#:]+)/i.exec(url)?.[1]?.toLowerCase() ?? null;
}
function hostsFromClaims(claims) {
  const hosts = ofType(claims, "endpoint").map((ep) => hostOf(typeof ep.endpoint === "string" ? ep.endpoint : templateHead(ep.endpoint_template)));
  return [...new Set(hosts.filter((h) => !!h))];
}
function hostsFromCode(code) {
  return [...new Set([...code.matchAll(/https?:\/\/([^/'"\s?#:{}]+)/gi)].map((m) => m[1].toLowerCase()))];
}
function selectEvidence(hosts) {
  const root = registryRoot();
  if (!root) return { provider: null, spec: null, hosts, note: "Evidence registry (evidence/registry.json) not found; set CONFIDENCE_EVIDENCE_ROOT to the Toolbox folder." };
  const registry = JSON.parse((0, import_fs.readFileSync)((0, import_path2.join)(root, "evidence", "registry.json"), "utf8"));
  const matches = Object.entries(registry.providers).filter(([, p]) => hosts.some((h) => p.hosts.includes(h)));
  if (!matches.length) return { provider: null, spec: null, hosts, note: `No frozen evidence for host(s): ${hosts.join(", ") || "(none found)"}.` };
  if (matches.length > 1) return { provider: null, spec: null, hosts, note: `Candidate calls several providers (${matches.map(([n]) => n).join(", ")}); single-provider verification only.` };
  const [provider, entry] = matches[0];
  const path = (0, import_path2.resolve)(root, "evidence", registry.sources_dir, entry.spec);
  if (!(0, import_fs.existsSync)(path)) return { provider, spec: null, hosts, note: `Frozen snapshot ${entry.spec} is missing at ${path}.` };
  if (!cache.has(path)) cache.set(path, JSON.parse((0, import_fs.readFileSync)(path, "utf8")));
  const spec = structuredClone(cache.get(path));
  spec["x-confidence-evidence"] = { ...spec["x-confidence-evidence"] || {}, ...entry.overlay, snapshot: entry.spec };
  return { provider, spec, hosts, snapshot: entry.spec, note: `Frozen evidence ${entry.spec} selected for ${provider}.` };
}
function evidenceFor(hosts, supplied) {
  const selected = selectEvidence(hosts);
  if (selected.spec) return { spec: selected.spec, source: selected.note + (supplied != null ? " A model-supplied specification was ignored." : "") };
  const usable = supplied != null && typeof supplied === "object" && !(Object.hasOwn(supplied, "spec") && !Object.hasOwn(supplied, "openapi"));
  return { spec: usable ? supplied : null, source: usable ? "Model-supplied specification (unreviewed; not frozen evidence)." : selected.note };
}
var import_fs, import_path2, cache;
var init_evidenceRegistry = __esm({
  "src/evidenceRegistry.ts"() {
    "use strict";
    import_fs = require("fs");
    import_path2 = require("path");
    init_verificationTypes();
    cache = /* @__PURE__ */ new Map();
  }
});

// src/confidenceAgentTools.ts
function createConfidenceAgentTools(deps) {
  const claims = import_zod.z.array(import_zod.z.record(import_zod.z.any())), spec = import_zod.z.record(import_zod.z.any()).nullable().optional();
  const out = [];
  function add(name, description, parameters2, implementation) {
    out.push((0, import_sdk2.tool)({ name, description, parameters: parameters2, implementation: async (p) => {
      if (!deps.isEnabled) throw new Error("Confidence Agent tools are disabled in plugin settings.");
      try {
        return await implementation(p);
      } catch (e) {
        return { error: String(e) };
      }
    } }));
  }
  const withEvidence = (fn) => async (p) => {
    const { spec: selected, source } = evidenceFor(hostsFromClaims(p.claims || []), p.spec);
    const r = await fn({ ...p, spec: selected });
    return r && typeof r === "object" ? { ...r, evidence_source_selection: source } : r;
  };
  add(
    "verify_candidate",
    "Run all six verifiers, score and report exact candidate API claims. Pass only the code: frozen evidence for JSONPlaceholder, GitHub, Open-Meteo, DummyJSON, REST Countries and Petstore is selected from the host the code calls. Never write or copy a specification. Does not prove task behavior. External controller enforces delivery and one correction.",
    { code: import_zod.z.string(), spec, reference_id: import_zod.z.enum(["jsonplaceholder-posts"]).optional(), input_bindings: import_zod.z.record(import_zod.z.any()).optional(), task_id: import_zod.z.string().optional() },
    async (p) => {
      if (p.reference_id && p.spec != null) throw new Error("Supply reference_id or spec, not both.");
      const selected = p.reference_id ? { spec: structuredClone(BUNDLED_REFERENCES[p.reference_id]), source: `Bundled reference ${p.reference_id}.` } : evidenceFor(hostsFromCode(p.code), p.spec);
      const reference = selected.spec;
      const r = await runIntervention({ ...p, spec: reference }, { runPyright: deps.runPyright, allowPyright: deps.allowPyright });
      const v = r.attempts[r.attempts.length - 1].verification;
      return {
        toolbox_version: TOOLBOX_VERSION,
        decision: r.decision,
        report: r.report,
        candidate_hash: v.candidate_hash,
        reference_id: p.reference_id ?? null,
        evidence_selection: selected.source,
        spec_hash: v.spec_hash,
        reference_evidence: reference?.["x-confidence-evidence"] ?? null,
        ewcs_report: v.ewcs_report,
        layers: v.layers,
        extraction_issues: v.extraction.issues
      };
    }
  );
  add("resolve_api_spec", "Discovery only: report whether a JSON OpenAPI 3.0 document exists at common paths, with its source and hash. Does not return the document; verify_candidate selects frozen evidence itself.", { base_url: import_zod.z.string() }, async (p) => {
    const r = await resolveApiSpec(p);
    if (!r.spec) return r;
    const operations = Object.values(r.spec.paths || {}).reduce((n, item) => n + Object.keys(item || {}).filter((k) => ["get", "put", "post", "delete", "patch", "head", "options"].includes(k)).length, 0);
    return {
      found: true,
      source_url: r.source_url,
      retrieved_at: r.retrieved_at,
      content_hash: r.content_hash,
      openapi: r.spec.openapi,
      title: r.spec.info?.title,
      version: r.spec.info?.version,
      operations,
      note: "Summary only. Do not pass a specification to verification tools; call verify_candidate with the code and frozen evidence is selected by host."
    };
  });
  add("query_pypi", "Query package metadata. exists:null/status:unverifiable means lookup failed, not that the package is nonexistent.", { library_name: import_zod.z.string() }, queryPypi);
  add("extract_claims", "Static Python extraction for a documented requests subset. Returns complete/limitations, operation-linked claims and a candidate hash. Runtime input values can be bound explicitly.", { code: import_zod.z.string(), input_bindings: import_zod.z.record(import_zod.z.any()).optional() }, extractClaims);
  add("verify_interface", "Check imports against registry evidence and explicit import/distribution mappings. Missing evidence and registry failures stay unverifiable.", { claims, pypi_data: import_zod.z.record(import_zod.z.any()).optional() }, verifyInterface);
  add("verify_identifier", "Check structured Pyright diagnostics for the exact code. Missing packages/stubs and process failure are unverifiable.", { code: import_zod.z.string() }, (p) => verifyIdentifier(p.code, deps.runPyright, deps.allowPyright));
  add("verify_access_point", "Match server origin/base path, endpoint and HTTP method. Dynamic endpoints and unsupported specs remain unverifiable.", { claims, spec }, withEvidence(verifyAccessPoint));
  add("verify_input_contract", "Check every request separately: required parameters, locations, supported values and JSON bodies. Runtime values are noted, not guessed; unknown keys block verification.", { claims, spec }, withEvidence(verifyInputContract));
  add("verify_output_contract", "Follow response provenance and local references to success schemas. A clean Pyright run never substitutes for JSON response evidence.", { claims, spec, code: import_zod.z.string().optional() }, withEvidence((p) => verifyOutputContract(p, deps.runPyright, deps.allowPyright)));
  add("verify_contextual", "Check operation-level inherited authentication alternatives against actual request arguments. Comments are not authentication.", { claims, spec, code: import_zod.z.string().optional() }, withEvidence(verifyContextual));
  add(
    "compute_ewcs",
    "Diagnostic score with canonical weights; missing checks retain weight and an empty applicable set has ewcs:null. Controller results are authoritative.",
    { layer_results: import_zod.z.array(import_zod.z.record(import_zod.z.any())), task_id: import_zod.z.string().optional(), extraction_complete: import_zod.z.boolean().optional() },
    (p) => Promise.resolve(computeEwcs(p))
  );
  add("make_decision", "Validate all six contributions. Contradiction requests correction; incomplete/unverifiable critical checks abstain before thresholds 0.85/0.60.", { ewcs_report: import_zod.z.record(import_zod.z.any()) }, async (p) => makeDecision(p.ewcs_report));
  add("save_code", "Save a candidate for inspection. This is not verified delivery; use the controller for user-facing output.", { code: import_zod.z.string(), filename: import_zod.z.string() }, async (p) => {
    const base = deps.getWorkingDirectory(), path = (0, import_path3.resolve)(base, p.filename), rel = (0, import_path3.relative)(base, path);
    if (!p.filename.trim() || rel.startsWith("..") || (0, import_path3.isAbsolute)(rel)) throw new Error("Invalid workspace-relative filename.");
    await (0, import_promises2.mkdir)((0, import_path3.dirname)(path), { recursive: true });
    await (0, import_promises2.writeFile)(path, p.code, "utf8");
    return { path };
  });
  add(
    "present_report",
    "Format a score report. Code is withheld for abstain/correct and inconsistent delivery requests. Native chat remains model controlled; use the external controller for enforcement.",
    { code: import_zod.z.string(), ewcs_report: import_zod.z.record(import_zod.z.any()), decision: import_zod.z.enum(["deliver", "deliver_with_flag", "correct", "abstain"]) },
    async (p) => presentReport(p)
  );
  return out;
}
var import_sdk2, import_promises2, import_path3, import_zod;
var init_confidenceAgentTools = __esm({
  "src/confidenceAgentTools.ts"() {
    "use strict";
    import_sdk2 = require("@lmstudio/sdk");
    import_promises2 = require("fs/promises");
    import_path3 = require("path");
    import_zod = require("zod");
    init_claimExtractor();
    init_packageEvidence();
    init_specDiscovery();
    init_pyrightRunner();
    init_openApiVerifier();
    init_verificationPolicy();
    init_verificationController();
    init_bundledReferences();
    init_evidenceRegistry();
    init_verificationTypes();
    init_verificationPolicy();
  }
});

// src/toolsProvider.ts
function resolveWorkspace(configured) {
  const raw = configured.trim().replace(/%([^%]+)%/g, (match, name) => process.env[name] ?? match);
  if (!raw) return DEFAULT_WORKSPACE;
  return (0, import_path4.isAbsolute)(raw) ? raw : (0, import_path4.resolve)(DEFAULT_WORKSPACE, raw);
}
function createPyrightTool(runPyright, allowPyright) {
  return (0, import_sdk3.tool)({
    name: "run_pyright",
    description: import_sdk3.text`
      Type-check a Python snippet with the pinned Pyright checker. Static analysis only: the code is
      NOT executed. Returns Pyright's structured JSON diagnostics, the exit code (0 no errors,
      1 type errors, higher values for checker or configuration failures), the checker version and
      the candidate hash. verify_candidate already runs Pyright; use this only for inspection.
    `,
    parameters: { python: import_zod2.z.string(), timeout_seconds: import_zod2.z.number().min(0.1).max(60).optional() },
    implementation: async (params) => {
      if (!allowPyright) throw new Error("Tool 'run_pyright' is disabled in the plugin settings (Allow Pyright).");
      return runPyright(params);
    }
  });
}
var import_sdk3, import_promises3, import_os2, import_path4, import_zod2, DEFAULT_WORKSPACE, toolsProvider;
var init_toolsProvider = __esm({
  "src/toolsProvider.ts"() {
    "use strict";
    import_sdk3 = require("@lmstudio/sdk");
    import_promises3 = require("fs/promises");
    import_os2 = require("os");
    import_path4 = require("path");
    import_zod2 = require("zod");
    init_config();
    init_confidenceAgentTools();
    init_pyrightRunner();
    DEFAULT_WORKSPACE = (0, import_path4.join)((0, import_os2.homedir)(), "confident-agent-workspace");
    toolsProvider = async (ctl) => {
      const config = ctl.getPluginConfig(pluginConfigSchematics);
      const python = config.get("pythonExecutable").trim();
      if (python) process.env.CONFIDENCE_PYTHON = python;
      const workspace = resolveWorkspace(config.get("workspacePath"));
      await (0, import_promises3.mkdir)(workspace, { recursive: true });
      const allowPyright = config.get("allowPyrightExecution");
      const runPyright = createPyrightRunner();
      const tools = [createPyrightTool(runPyright, allowPyright)];
      if (config.get("enableConfidenceAgentTools")) {
        tools.push(...createConfidenceAgentTools({ isEnabled: true, allowPyright, getWorkingDirectory: () => workspace, runPyright }));
      }
      return tools;
    };
  }
});

// src/index.ts
var src_exports = {};
__export(src_exports, {
  main: () => main
});
async function main(context) {
  context.withConfigSchematics(pluginConfigSchematics);
  context.withToolsProvider(toolsProvider);
}
var init_src = __esm({
  "src/index.ts"() {
    "use strict";
    init_config();
    init_toolsProvider();
  }
});

// .lmstudio/entry.ts
var import_sdk4 = require("@lmstudio/sdk");
var clientIdentifier = process.env.LMS_PLUGIN_CLIENT_IDENTIFIER;
var clientPasskey = process.env.LMS_PLUGIN_CLIENT_PASSKEY;
var baseUrl = process.env.LMS_PLUGIN_BASE_URL;
var client = new import_sdk4.LMStudioClient({
  clientIdentifier,
  clientPasskey,
  baseUrl
});
globalThis.__LMS_PLUGIN_CONTEXT = true;
var predictionLoopHandlerSet = false;
var promptPreprocessorSet = false;
var configSchematicsSet = false;
var globalConfigSchematicsSet = false;
var toolsProviderSet = false;
var generatorSet = false;
var selfRegistrationHost = client.plugins.getSelfRegistrationHost();
var pluginContext = {
  withPredictionLoopHandler: (generate) => {
    if (predictionLoopHandlerSet) {
      throw new Error("PredictionLoopHandler already registered");
    }
    if (toolsProviderSet) {
      throw new Error("PredictionLoopHandler cannot be used with a tools provider");
    }
    predictionLoopHandlerSet = true;
    selfRegistrationHost.setPredictionLoopHandler(generate);
    return pluginContext;
  },
  withPromptPreprocessor: (preprocess) => {
    if (promptPreprocessorSet) {
      throw new Error("PromptPreprocessor already registered");
    }
    promptPreprocessorSet = true;
    selfRegistrationHost.setPromptPreprocessor(preprocess);
    return pluginContext;
  },
  withConfigSchematics: (configSchematics) => {
    if (configSchematicsSet) {
      throw new Error("Config schematics already registered");
    }
    configSchematicsSet = true;
    selfRegistrationHost.setConfigSchematics(configSchematics);
    return pluginContext;
  },
  withGlobalConfigSchematics: (globalConfigSchematics) => {
    if (globalConfigSchematicsSet) {
      throw new Error("Global config schematics already registered");
    }
    globalConfigSchematicsSet = true;
    selfRegistrationHost.setGlobalConfigSchematics(globalConfigSchematics);
    return pluginContext;
  },
  withToolsProvider: (toolsProvider2) => {
    if (toolsProviderSet) {
      throw new Error("Tools provider already registered");
    }
    if (predictionLoopHandlerSet) {
      throw new Error("Tools provider cannot be used with a predictionLoopHandler");
    }
    toolsProviderSet = true;
    selfRegistrationHost.setToolsProvider(toolsProvider2);
    return pluginContext;
  },
  withGenerator: (generator) => {
    if (generatorSet) {
      throw new Error("Generator already registered");
    }
    generatorSet = true;
    selfRegistrationHost.setGenerator(generator);
    return pluginContext;
  }
};
Promise.resolve().then(() => (init_src(), src_exports)).then(async (module2) => {
  return await module2.main(pluginContext);
}).then(() => {
  selfRegistrationHost.initCompleted();
}).catch((error) => {
  console.error("Failed to execute the main function of the plugin.");
  console.error(error);
});
