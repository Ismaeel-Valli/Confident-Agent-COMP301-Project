"""OpenAPI access for the evaluator, written independently of the toolbox's verifier
(EVALUATION_PLAN.md §5): reference resolution, operation matching, value checks and the
response model the sandbox serves."""
from __future__ import annotations

import json
import re
from pathlib import Path

HTTP_METHODS = ("get", "put", "post", "delete", "patch", "head", "options", "trace")


class Spec:
    def __init__(self, path: Path):
        self.path = path
        self.doc = json.loads(path.read_text(encoding="utf-8"))

    # ------------------------------------------------------------ references
    def deref(self, node, depth: int = 0):
        """Follow local $refs; an unresolvable reference gives None."""
        while isinstance(node, dict) and "$ref" in node and depth < 50:
            ref = node["$ref"]
            if not isinstance(ref, str) or not ref.startswith("#/"):
                return None
            target = self.doc
            for part in ref[2:].split("/"):
                part = part.replace("~1", "/").replace("~0", "~")
                if not isinstance(target, dict) or part not in target:
                    return None
                target = target[part]
            node, depth = target, depth + 1
        return node

    def schema(self, node, depth: int = 0) -> dict | None:
        """A schema with $refs resolved and allOf merged (properties, required, type)."""
        node = self.deref(node)
        if not isinstance(node, dict) or depth > 30:
            return None
        if "allOf" not in node:
            return node
        merged = {k: v for k, v in node.items() if k != "allOf"}
        props, required = dict(merged.get("properties") or {}), list(merged.get("required") or [])
        for part in node["allOf"]:
            sub = self.schema(part, depth + 1) or {}
            props.update(sub.get("properties") or {})
            required += sub.get("required") or []
            for key in ("type", "additionalProperties", "items", "enum"):
                if key in sub and key not in merged:
                    merged[key] = sub[key]
        if props:
            merged["properties"] = props
            merged.setdefault("type", "object")
        if required:
            merged["required"] = sorted(set(required))
        return merged

    # ------------------------------------------------------------ operations
    def match(self, rel_path: str, method: str):
        """(path_key, path_item, operation, path_values) for a concrete path, or a reason."""
        segments = [s for s in rel_path.split("/") if s != ""]
        candidates = []
        for key, item in (self.doc.get("paths") or {}).items():
            parts = [s for s in key.split("/") if s != ""]
            if len(parts) != len(segments):
                continue
            values, literal = {}, 0
            for tpl, seg in zip(parts, segments):
                names = re.findall(r"\{([^}]+)\}", tpl)
                if not names:
                    if tpl != seg:
                        break
                    literal += 1
                    continue
                pattern = "^" + "".join("(.+?)" if re.fullmatch(r"\{[^}]+\}", p) else re.escape(p)
                                        for p in re.split(r"(\{[^}]+\})", tpl) if p) + "$"
                m = re.match(pattern, seg)
                if not m:
                    break
                values.update(dict(zip(names, m.groups())))
            else:
                candidates.append((literal, key, self.deref(item) or {}, values))
        if not candidates:
            return None, "no declared path matches"
        candidates.sort(key=lambda c: -c[0])  # literal segments win over templates
        for _, key, item, values in candidates:
            op = item.get(method.lower())
            if isinstance(op, dict):
                return (key, item, op, values), None
        allowed = sorted({m.upper() for _, _, item, _ in candidates for m in item if m in HTTP_METHODS})
        return None, f"{method} is not declared for {candidates[0][1]} (declared: {', '.join(allowed)})"

    def parameters(self, item: dict, op: dict) -> dict:
        found = {}
        for raw in (item.get("parameters") or []) + (op.get("parameters") or []):
            p = self.deref(raw)
            if isinstance(p, dict) and "name" in p and "in" in p:
                found[(p["in"], p["name"] if p["in"] != "header" else p["name"].lower())] = p
        return found

    def request_body(self, op: dict):
        body = self.deref(op.get("requestBody"))
        if not isinstance(body, dict):
            return None
        return {"required": bool(body.get("required")), "content": {k.split(";")[0].strip().lower(): (v or {}).get("schema")
                                                                     for k, v in (body.get("content") or {}).items()}}

    def success(self, op: dict):
        """First documented 2xx status and its JSON schema."""
        responses = op.get("responses") or {}
        for code in sorted(k for k in responses if str(k).startswith("2")):
            resp = self.deref(responses[code]) or {}
            content = resp.get("content") or {}
            schema = next((v.get("schema") for k, v in content.items() if "json" in k), None)
            return int(code) if str(code).isdigit() else 200, schema
        default = self.deref(responses.get("default")) or {}
        schema = next((v.get("schema") for k, v in (default.get("content") or {}).items() if "json" in k), None)
        return 200, schema

    def security_query_names(self, op: dict) -> set:
        names = set()
        requirements = op.get("security", self.doc.get("security") or [])
        schemes = (self.doc.get("components") or {}).get("securitySchemes") or {}
        for req in requirements or []:
            for name in req or {}:
                s = self.deref(schemes.get(name)) or {}
                if s.get("type") == "apiKey" and s.get("in") == "query":
                    names.add(s.get("name"))
        return names

    # ------------------------------------------------------------ response model
    def shape(self, node, depth: int = 0) -> dict:
        """The response the sandbox serves: every documented property with an example value.
        Objects are 'open' only when the schema explicitly allows other properties."""
        s = self.schema(node)
        if not isinstance(s, dict) or depth > 8:
            return {"t": "unknown"}
        for key in ("oneOf", "anyOf"):
            if s.get(key):
                return self.shape(s[key][0], depth + 1)
        kind = s.get("type")
        if isinstance(kind, list):
            kind = next((k for k in kind if k != "null"), None)
        if kind == "array" or "items" in s:
            return {"t": "array", "items": self.shape(s.get("items"), depth + 1)}
        if kind == "object" or "properties" in s:
            props = s.get("properties") or {}
            extra = s.get("additionalProperties")
            return {"t": "object", "props": {k: self.shape(v, depth + 1) for k, v in props.items()},
                    "open": extra is True or isinstance(extra, dict) or not props}
        if kind is None:
            return {"t": "unknown"}
        return {"t": "value", "v": example_value(s, kind)}


def example_value(s: dict, kind: str):
    for key in ("example", "default"):
        if key in s and not isinstance(s[key], (dict, list)):
            return s[key]
    if s.get("enum"):
        return s["enum"][0]
    return {"string": "example", "integer": 1, "number": 1.5, "boolean": True, "null": None}.get(kind, "example")


def plain_example(shape: dict):
    """The JSON value of a response model (what the sandbox's response.json() equals)."""
    kind = shape.get("t")
    if kind == "object":
        return {k: plain_example(v) for k, v in (shape.get("props") or {}).items()}
    if kind == "array":
        return [plain_example(shape.get("items") or {"t": "unknown"})]
    if kind == "value":
        return shape.get("v")
    return {}


# ---------------------------------------------------------------- value checks
def types_of(s: dict) -> list:
    t = s.get("type")
    types = t if isinstance(t, list) else [t] if t else []
    if s.get("nullable"):
        types.append("null")
    return types


def check_value(spec: Spec, value, schema, where: str, from_text: bool = False, depth: int = 0) -> list:
    """Problems of a value against a schema: [(kind, message)] with kind 'undeclared' for a
    field the schema does not declare (a hallucination only if the schema is complete) and
    'invalid' for everything else."""
    s = spec.schema(schema)
    if not isinstance(s, dict) or depth > 20:
        return []
    for key in ("oneOf", "anyOf"):
        if s.get(key):
            results = [check_value(spec, value, option, where, from_text, depth + 1) for option in s[key]]
            return [] if any(not r for r in results) else min(results, key=len)
    types = types_of(s)
    if from_text and isinstance(value, str):
        value = coerce_text(value, types)
    if value is None:
        return [] if "null" in types or not types else [("invalid", f"{where}: null is not allowed")]
    if types and not any(matches_type(value, t) for t in types):
        return [("invalid", f"{where}: expected {'/'.join(types)}, got {type(value).__name__} {json.dumps(value)[:60]}")]
    problems = []
    if s.get("enum") is not None and value not in s["enum"] and not (isinstance(value, str) and value.lower() in
                                                                      [str(e).lower() for e in s["enum"]]):
        problems.append(("invalid", f"{where}: {json.dumps(value)[:60]} is not one of the documented values"))
    if isinstance(value, dict):
        props, extra = s.get("properties") or {}, s.get("additionalProperties")
        for name in s.get("required") or []:
            if name not in value and not (spec.schema(props.get(name)) or {}).get("readOnly"):
                problems.append(("invalid", f"{where}: required field {name} is missing"))
        for key, sub in value.items():
            if key in props:
                problems += check_value(spec, sub, props[key], f"{where}.{key}", False, depth + 1)
            elif extra is False:
                problems.append(("invalid", f"{where}: field {key} is not allowed"))
            elif isinstance(extra, dict):
                problems += check_value(spec, sub, extra, f"{where}.{key}", False, depth + 1)
            elif extra is not True:
                problems.append(("undeclared", f"{where}: field {key} is not declared"))
    if isinstance(value, list) and s.get("items") is not None:
        for i, item in enumerate(value):
            problems += check_value(spec, item, s["items"], f"{where}[{i}]", from_text, depth + 1)
    return problems


def coerce_text(value: str, types: list):
    """Query and path values arrive as text; read them as the declared type when they parse."""
    if "integer" in types and re.fullmatch(r"-?\d+", value):
        return int(value)
    if "number" in types and re.fullmatch(r"-?\d+(\.\d+)?([eE][-+]?\d+)?", value):
        return float(value)
    if "boolean" in types and value.lower() in ("true", "false"):
        return value.lower() == "true"
    return value


def matches_type(value, t: str) -> bool:
    return {"string": isinstance(value, str), "integer": isinstance(value, int) and not isinstance(value, bool),
            "number": isinstance(value, (int, float)) and not isinstance(value, bool),
            "boolean": isinstance(value, bool), "array": isinstance(value, list), "object": isinstance(value, dict),
            "null": value is None}.get(t, True)
