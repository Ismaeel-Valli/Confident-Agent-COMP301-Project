"""Conservative static extraction. Never imports or executes the candidate."""
import ast
import json
import sys
import tokenize
import io

payload = json.load(sys.stdin)
code = payload.get('code', '')
bindings = payload.get('input_bindings', {})
claims, issues = [], []
UNKNOWN = object()
HTTP = {'get', 'post', 'put', 'patch', 'delete', 'head', 'options'}


def issue(node, reason):
    item = {'line': getattr(node, 'lineno', 0), 'reason': reason}
    if item not in issues:
        issues.append(item)


def add(node, kind, **fields):
    result = {'id': 'claim_%s' % (len(claims) + 1), 'type': kind,
              'line': getattr(node, 'lineno', 0), **fields}
    claims.append(result)
    return result


def known(value):
    if value is UNKNOWN:
        return False
    if isinstance(value, dict):
        return all(known(v) for v in value.values())
    if isinstance(value, (list, tuple)):
        return all(known(v) for v in value)
    return True


def public(value):
    return value if known(value) else None


class Analyzer:
    def __init__(self, env=None, imports=None, provenance=None):
        self.env = dict(env or {})
        self.imports = dict(imports or {})
        self.provenance = dict(provenance or {})
        self.calls = {}

    def value(self, node):
        if node is None:
            return UNKNOWN
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):
            return self.env.get(node.id, UNKNOWN)
        if isinstance(node, ast.Dict):
            result = {}
            for k, v in zip(node.keys, node.values):
                key = self.value(k)
                if k is None or not isinstance(key, str):
                    return UNKNOWN
                result[key] = self.value(v)
            return result
        if isinstance(node, (ast.List, ast.Tuple)):
            return [self.value(v) for v in node.elts]
        if isinstance(node, ast.Subscript):
            obj, key = self.value(node.value), self.value(node.slice)
            if obj is not UNKNOWN and key is not UNKNOWN:
                try:
                    return obj[key]
                except (KeyError, IndexError, TypeError):
                    pass
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            left, right = self.value(node.left), self.value(node.right)
            if isinstance(left, str) and isinstance(right, str):
                return left + right
        if isinstance(node, ast.JoinedStr):
            values = []
            for part in node.values:
                if isinstance(part, ast.Constant):
                    values.append(part.value)
                elif isinstance(part, ast.FormattedValue) and not part.format_spec and part.conversion == -1:
                    val = self.value(part.value)
                    if not known(val):
                        return UNKNOWN
                    values.append(str(val))
                else:
                    return UNKNOWN
            return ''.join(values)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            v = self.value(node.operand)
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                return -v if isinstance(node.op, ast.USub) else v
        # inputs.get('key', literal_default), without running arbitrary methods.
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'get':
            obj = self.value(node.func.value)
            if isinstance(obj, dict) and node.args:
                key = self.value(node.args[0])
                if isinstance(key, str):
                    return obj.get(key, self.value(node.args[1]) if len(node.args) > 1 else None)
        return UNKNOWN

    def qualified(self, node):
        if isinstance(node, ast.Name):
            return self.imports.get(node.id, node.id)
        if isinstance(node, ast.Attribute):
            return self.qualified(node.value) + '.' + node.attr
        return ''

    def origin(self, node):
        if isinstance(node, ast.Name):
            return self.provenance.get(node.id)
        if isinstance(node, ast.Call):
            if id(node) in self.calls:
                return (self.calls[id(node)], None)  # HTTP response, before .json()
            if isinstance(node.func, ast.Attribute) and node.func.attr == 'json':
                source = self.origin(node.func.value)
                if source and source[1] is None:
                    return (source[0], [])
            if isinstance(node.func, ast.Attribute) and node.func.attr == 'get' and node.args:
                source, key = self.origin(node.func.value), self.value(node.args[0])
                if source and source[1] is not None:
                    return (source[0], source[1] + [key if isinstance(key, str) else '*'])
        if isinstance(node, ast.Subscript):
            source, key = self.origin(node.value), self.value(node.slice)
            if source and source[1] is not None:
                if not isinstance(key, (str, int)) or isinstance(key, bool):
                    issue(node, 'Dynamic response subscript cannot be resolved.')
                    return (source[0], source[1] + ['*'])
                return (source[0], source[1] + [key])
        return None

    def scan(self, node):
        if node is None:
            return
        for child in ast.iter_child_nodes(node):
            self.scan(child)
        if isinstance(node, ast.Subscript):
            origin = self.origin(node)
            if origin and origin[1] is not None:
                add(node, 'output_field', call_id=origin[0], field=origin[1][-1], path=origin[1])
        if not isinstance(node, ast.Call):
            return
        name = self.qualified(node.func)
        if name.startswith('requests.'):
            add(node, 'method_call', library='requests', method=name[9:])
        method = name[9:] if name.startswith('requests.') else ''
        if method in HTTP or method == 'request':
            args = list(node.args)
            kwargs = {kw.arg: kw.value for kw in node.keywords if kw.arg}
            if any(kw.arg is None for kw in node.keywords):
                issue(node, 'Expanded request keyword arguments are unsupported.')
            if method == 'request':
                method_value = self.value(kwargs.get('method') or (args.pop(0) if args else None))
            else:
                method_value = method.upper()
            url_node = kwargs.get('url') or (args.pop(0) if args else None)
            url = self.value(url_node)
            # requests.get(url, params) and requests.post(url, data, json)
            if args:
                positional = ['data', 'json'] if method == 'post' else (['params'] if method == 'get' else [])
                for key, val in zip(positional, args):
                    if key in kwargs:
                        issue(node, 'Duplicate request argument.')
                    kwargs[key] = val
                if len(args) > len(positional):
                    issue(node, 'Unsupported positional request arguments.')
            call_id = 'call_%s_%s' % (node.lineno, node.col_offset)
            self.calls[id(node)] = call_id
            request = {}
            for via in ('params', 'json', 'data', 'headers', 'cookies', 'auth'):
                if via in kwargs:
                    value = self.value(kwargs[via])
                    request[via] = {'provided': True, 'known': known(value), 'value': public(value),
                                    'keys_known': isinstance(value, dict),
                                    'fields': {k: {'known': known(v), 'value': public(v)} for k, v in value.items()} if isinstance(value, dict) else {}}
                    if isinstance(value, dict):
                        for field, val in value.items():
                            add(node, 'input_field', call_id=call_id, field=field, via=via, known=known(val), value=public(val))
            if not isinstance(url, str) or not isinstance(method_value, str):
                issue(node, 'Dynamic endpoint or HTTP method requires explicit input_bindings.')
            add(node, 'endpoint', call_id=call_id, endpoint=url if isinstance(url, str) else None,
                http_method=method_value.upper() if isinstance(method_value, str) else None,
                resolved=isinstance(url, str) and isinstance(method_value, str), request=request,
                request_complete=not any(kw.arg is None for kw in node.keywords))
            if kwargs.get('verify') and self.value(kwargs['verify']) is False:
                issue(node, 'TLS verification disabled; outside supported verification scope.')
            if any(k not in ('url', 'method', 'params', 'json', 'data', 'headers', 'cookies', 'auth', 'timeout', 'allow_redirects', 'verify') for k in kwargs):
                issue(node, 'Unsupported requests keyword argument.')
        elif isinstance(node.func, ast.Attribute) and node.func.attr == 'get' and self.origin(node):
            origin = self.origin(node)
            add(node, 'output_field', call_id=origin[0], field=origin[1][-1], path=origin[1], optional_access=True)
        elif name.startswith(('requests.', 'httpx.', 'aiohttp.', 'urllib.')):
            issue(node, 'Only direct requests calls are supported; session/other client use is unresolved.')
        elif isinstance(node.func, ast.Attribute):
            receiver = self.origin(node.func.value)
            if receiver:
                if node.func.attr == 'json' and (node.args or node.keywords):
                    issue(node, 'Custom JSON decoding arguments can change response shape.')
                if node.func.attr not in ('json', 'raise_for_status', 'get'):
                    issue(node, 'Unsupported response method: ' + node.func.attr)
            elif node.func.attr in HTTP and not isinstance(self.value(node.func.value), dict):
                issue(node, 'Unresolved HTTP-like call receiver: ' + name)
            elif node.func.attr in ('update', 'append', 'extend', 'pop', 'setdefault', 'clear'):
                issue(node, 'Mutation requires flow analysis outside the supported subset.')
        # Calls other than documented client operations, pure input dict.get, or print
        # can mutate arguments/globals. They are retained as an extraction limitation.
        elif name not in ('print', 'len', 'str', 'int', 'float', 'bool') and name not in ('',):
            issue(node, 'User-defined/dynamic callable requires interprocedural analysis: ' + name)

    def assign(self, target, node):
        if isinstance(target, ast.Name):
            self.env[target.id] = self.value(node)
            self.imports.pop(target.id, None)
            origin = self.origin(node)
            if origin:
                self.provenance[target.id] = origin
            else:
                self.provenance.pop(target.id, None)
        else:
            issue(target, 'Destructuring or mutation assignment is unsupported.')

    def statements(self, statements):
        for node in statements:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.imports[alias.asname or alias.name.split('.')[0]] = alias.name
                    top = alias.name.split('.')[0]
                    add(node, 'import', library=alias.name, stdlib=top in getattr(sys, 'stdlib_module_names', set()), local=False)
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ''
                for alias in node.names:
                    self.imports[alias.asname or alias.name] = mod + '.' + alias.name
                    add(node, 'import', library=mod, stdlib=mod.split('.')[0] in getattr(sys, 'stdlib_module_names', set()), local=node.level > 0)
                    if alias.name == '*':
                        issue(node, 'Wildcard import is unsupported.')
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                child = Analyzer(self.env, self.imports, self.provenance)
                for arg in node.args.posonlyargs + node.args.args + node.args.kwonlyargs:
                    child.env[arg.arg] = bindings.get(arg.arg, UNKNOWN)
                    child.imports.pop(arg.arg, None)
                    child.provenance.pop(arg.arg, None)
                if isinstance(node, ast.AsyncFunctionDef) or node.decorator_list:
                    issue(node, 'Async/decorated functions are unsupported.')
                child.statements(node.body)
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                self.scan(node.value)
                for target in node.targets if isinstance(node, ast.Assign) else [node.target]:
                    self.assign(target, node.value)
            elif isinstance(node, ast.For):
                self.scan(node.iter)
                origin = self.origin(node.iter)
                child = Analyzer(self.env, self.imports, self.provenance)
                if origin and origin[1] is not None and isinstance(node.target, ast.Name):
                    child.env[node.target.id] = UNKNOWN
                    child.provenance[node.target.id] = (origin[0], origin[1] + [0])
                    child.statements(node.body)
                    child.statements(node.orelse)
                    if any(isinstance(x, (ast.Assign, ast.AnnAssign, ast.AugAssign)) for x in ast.walk(node)):
                        issue(node, 'Assignments across loop iterations require unsupported flow analysis.')
                else:
                    issue(node, 'Only iteration over a tracked JSON response is supported.')
            elif isinstance(node, (ast.If, ast.While, ast.Try, ast.With, ast.ClassDef, ast.Match)):
                issue(node, 'Control flow/context manager/class is outside the supported extraction subset.')
                # Scan branches independently so definite contradictions are still visible.
                for attr in ('body', 'orelse', 'finalbody'):
                    Analyzer(self.env, self.imports, self.provenance).statements(getattr(node, attr, []))
                for handler in getattr(node, 'handlers', []):
                    Analyzer(self.env, self.imports, self.provenance).statements(handler.body)
                self.env = {k: UNKNOWN for k in self.env}
                self.provenance.clear()
            elif isinstance(node, (ast.Expr, ast.Return)):
                self.scan(node.value)
            elif isinstance(node, ast.Pass):
                pass
            else:
                issue(node, 'Unsupported statement: ' + type(node).__name__)
        # Comprehensions and dynamic attribute access must never disappear silently.

try:
    tree = ast.parse(code)
    for token in tokenize.generate_tokens(io.StringIO(code).readline):
        if token.type == tokenize.COMMENT and ('pyright:' in token.string.lower() or 'type: ignore' in token.string.lower()):
            issues.append({'line': token.start[0], 'reason': 'Candidate contains checker suppression/configuration directives.'})
    for n in ast.walk(tree):
        if isinstance(n, (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp, ast.Lambda, ast.Await)):
            issue(n, 'Unsupported dynamic expression: ' + type(n).__name__)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in ('getattr', 'eval', 'exec', '__import__'):
            issue(n, 'Dynamic code or attribute access is unsupported.')
    Analyzer().statements(tree.body)
    print(json.dumps({'claims': claims, 'complete': not issues, 'issues': issues}))
except (SyntaxError, ValueError) as e:
    print(json.dumps({'claims': [], 'complete': False, 'issues': [], 'error': str(e)}))
