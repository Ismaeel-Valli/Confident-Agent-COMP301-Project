"""Independent development checks of two fixed, reviewed fixtures, using mocked HTTP.

This is separate from the static verifier and is never invoked by verify_candidate.
It executes the shipped Python functions with fake requests responses, not live APIs.
It is not a sandbox and does not accept arbitrary candidate paths. Benchmark adjudication
must be conducted independently; these fixtures are not benchmark reference answers.
"""
import hashlib
import json
from pathlib import Path
import runpy
from unittest.mock import Mock, patch

import requests

ROOT = Path(__file__).resolve().parents[1]
POSTS = [{"id": 1, "userId": 1, "title": "development test", "body": "fixture"}]
CASES = [
    ("populated_200", 200, json.dumps(POSTS).encode(), POSTS, None),
    ("empty_body_200", 200, b"", None, None),
    ("empty_body_204", 204, b"", None, None),
    ("populated_201", 201, json.dumps(POSTS).encode(), POSTS, None),
    ("empty_json_array", 200, b"[]", [], None),
    ("client_error_json", 404, b'{"error":"missing"}', None, "http"),
    ("client_error_empty", 400, b"", None, "http"),
    ("server_error_json", 500, b'{"error":"server"}', None, "http"),
    ("unresolved_redirect", 302, b"", None, "http"),
    ("invalid_json_success", 200, b"not-json", None, "json"),
    ("transport_timeout", None, None, None, "timeout"),
]


def evaluate(solve):
    results = []
    for name, status, body, expected, error in CASES:
        response = requests.Response()
        response.status_code = status or 200
        response._content = body or b""
        response.url = "https://jsonplaceholder.typicode.com/posts"
        response.json = Mock(wraps=response.json)
        fake = Mock(return_value=response)
        if error == "timeout":
            fake.side_effect = requests.Timeout("development fixture timeout")
        try:
            with patch("requests.get", fake), patch("requests.sessions.Session.request", side_effect=AssertionError("Live HTTP is forbidden in this evaluator")):
                caught = None
                try:
                    actual = solve({})
                except AssertionError:
                    raise
                except Exception as exc:
                    caught = exc
                assert fake.call_count == 1, "Expected one GET request"
                args, kwargs = fake.call_args
                assert (args[0] if args else kwargs.get("url")) == response.url, "Wrong endpoint"
                if error == "http":
                    assert caught is not None, "Unsuccessful HTTP response did not raise"
                    assert response.json.call_count == 0, "HTTP failure was decoded before checking status"
                elif error == "json":
                    assert isinstance(caught, requests.exceptions.JSONDecodeError), "Invalid JSON was hidden or changed"
                elif error == "timeout":
                    assert isinstance(caught, requests.Timeout), "Transport failure was hidden or changed"
                else:
                    assert caught is None, f"Unexpected {type(caught).__name__}: {caught}"
                    assert actual == expected, f"Expected {expected!r}, received {actual!r}"
                    assert response.json.call_count == (0 if body == b"" else 1), "Empty bodies must be checked before decoding"
            results.append({"case": name, "passed": True})
        except AssertionError as exc:
            results.append({"case": name, "passed": False, "reason": str(exc)})
    return {"passed": sum(r["passed"] for r in results), "total": len(results), "all_passed": all(r["passed"] for r in results), "cases": results}


def main():
    fixtures = {
        "original_pilot": ROOT / "tests/fixtures/pilot-return-none.py",
        "corrected_reference": ROOT / "examples/jsonplaceholder-solve.py",
    }
    report = {"method": "Independent mocked behavioral checks; no live HTTP; no EWCS input", "fixtures": {}}
    for name, path in fixtures.items():
        code = path.read_bytes()
        solve = runpy.run_path(str(path))["solve"]
        report["fixtures"][name] = {"path": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(code).hexdigest(), **evaluate(solve)}
    print(json.dumps(report, indent=2))
    return 0 if (not report["fixtures"]["original_pilot"]["all_passed"] and report["fixtures"]["corrected_reference"]["all_passed"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
