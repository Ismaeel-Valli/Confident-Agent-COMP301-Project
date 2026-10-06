"""Known-answer tests: each changes a correct reference solution in one known way and checks
the evaluator gives the class EVALUATION_PLAN.md §2 requires. Run: python -m unittest discover tests"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evaluator.classify import TaskContext, classify  # noqa: E402
from evaluator.spec import Spec  # noqa: E402
from evaluator import stats  # noqa: E402

DATASET = ROOT.parents[1] / "Code Submission" / "COMP301-Dataset-Builder" / "comp301-dataset-builder"
TASKS = {json.loads(l)["task_id"]: json.loads(l) for l in (DATASET / "output" / "rest_api_tasks_v1_DRAFT.jsonl")
         .read_text(encoding="utf-8").splitlines() if l.strip()}
SPECS: dict = {}


def context(task_id: str) -> TaskContext:
    task = TASKS[task_id]
    source = DATASET / "sources" / Path(task["api_specification"]["source_file"]).name
    SPECS.setdefault(source, Spec(source))
    return TaskContext(task, SPECS[source])


def judge(task_id: str, *replacements, code: str | None = None) -> dict:
    code = code if code is not None else TASKS[task_id]["ground_truth"]["code"]
    for old, new in replacements:
        assert old in code, f"{old!r} not in {task_id}"
        code = code.replace(old, new)
    return classify(context(task_id), code)


class ReferenceSolutions(unittest.TestCase):
    def test_references_are_correct(self):
        for tid in ("REST_PY_PS_0002", "REST_PY_GH_0071", "REST_PY_JP_0001", "REST_PY_OM_0001"):
            with self.subTest(tid):
                r = judge(tid)
                self.assertEqual(r["class"], "correct", r["reasons"])
                self.assertTrue(all(r["behaviour"].values()), r["behaviour"])


class APIHallucinations(unittest.TestCase):
    """Class A: the code breaks the API's contract."""

    def assertClass(self, result, cls, fragment):
        self.assertEqual(result["class"], cls, result["reasons"])
        self.assertTrue(any(fragment in m for m in result["reasons"]), result["reasons"])

    def test_outdated_host(self):
        self.assertClass(judge("REST_PY_PS_0002", ("petstore3.swagger.io/api/v3", "petstore.swagger.io/v2")),
                         "A", "not the task's API")

    def test_undeclared_path_official_spec(self):
        self.assertClass(judge("REST_PY_PS_0002", ("/api/v3/pet'", "/api/v3/pets'")), "A", "no declared path")

    def test_undeclared_method(self):
        self.assertClass(judge("REST_PY_PS_0002", ("request('POST'", "request('DELETE'")), "A", "DELETE is not declared")

    def test_undeclared_query_parameter_official_spec(self):
        self.assertClass(judge("REST_PY_GH_0071", ("params['sha']", "params['commit_sha']")), "A", "commit_sha is not declared")

    def test_value_outside_enum(self):
        self.assertClass(judge("REST_PY_OM_0001", ("['temperature_2m']", "['temperatureTwoMetres']")), "A",
                         "not one of the documented values")

    def test_body_field_wrong_structure(self):
        self.assertClass(judge("REST_PY_PS_0002", ("{'name': inputs['new_name']", "{'name': {'value': inputs['new_name']}")),
                         "A", "expected string")

    def test_required_body_field_missing(self):
        self.assertClass(judge("REST_PY_PS_0002", (", 'photoUrls': inputs['new_photo_links']", "")), "A",
                         "required field photoUrls is missing")

    def test_missing_credential_required_by_api(self):
        self.assertClass(judge("REST_PY_PS_0002", ("    headers['Authorization'] = 'Bearer ' + inputs[\"credential\"]\n", "")),
                         "A", "credential")

    def test_invented_requests_function(self):
        self.assertClass(judge("REST_PY_PS_0002", ("requests.request('POST', url,", "requests.send('POST', url,")),
                         "A", "requests.send")

    def test_invented_keyword_argument(self):
        self.assertClass(judge("REST_PY_PS_0002", ("timeout=20", "retries=3")), "A", "retries")

    def test_undocumented_response_field(self):
        self.assertClass(judge("REST_PY_PS_0002", ("    return data\n", "    return data['petId']\n")), "A",
                         "reads response field petId")


class PartialSpecifications(unittest.TestCase):
    def test_undeclared_name_in_partial_spec_is_undetermined(self):
        r = judge("REST_PY_JP_0001", ("params = {}", "params = {'_limit': 5}"))
        self.assertEqual(r["class"], "undetermined", r["reasons"])
        self.assertTrue(any("partial specification" in m for m in r["reasons"]))


class TaskFidelityAndEquivalence(unittest.TestCase):
    def test_github_token_scheme_is_equivalent(self):
        r = judge("REST_PY_GH_0071", ("'Bearer ' + inputs", "'token ' + inputs"))
        self.assertEqual(r["class"], "correct", r["reasons"])

    def test_omitted_parameter_the_task_specifies(self):
        r = judge("REST_PY_GH_0071", ("    params['sha'] = str(inputs['sha'])\n", ""))
        self.assertEqual(r["class"], "B", r["reasons"])

    def test_extra_documented_body_field(self):
        r = judge("REST_PY_PS_0002", ("'photoUrls': inputs['new_photo_links']}", "'photoUrls': inputs['new_photo_links'], 'status': 'sold'}"))
        self.assertEqual(r["class"], "B", r["reasons"])

    def test_runtime_failure(self):
        r = judge("REST_PY_PS_0002", ("inputs['new_name']", "inputs['pet_name']"))
        self.assertEqual(r["class"], "runtime_failure", r["reasons"])

    def test_syntax_error(self):
        self.assertEqual(judge("REST_PY_PS_0002", code="def solve(inputs)\n    return 1\n")["class"], "runtime_failure")

    def test_behaviour_empty_response(self):
        r = judge("REST_PY_PS_0002", ("    if response.status_code == 204 or not response.content:\n        return None\n", ""))
        self.assertEqual(r["class"], "correct")
        self.assertFalse(r["behaviour"]["empty_response_ok"])


class Statistics(unittest.TestCase):
    def test_mcnemar_exact(self):
        self.assertAlmostEqual(stats.mcnemar_exact(0, 10), 0.001953125)
        self.assertAlmostEqual(stats.mcnemar_exact(3, 10), 0.0922851562, places=6)

    def test_holm(self):
        self.assertEqual(stats.holm({"a": 0.01, "b": 0.04, "c": 0.03}), {"a": 0.03, "c": 0.06, "b": 0.06})


if __name__ == "__main__":
    unittest.main()


class HallucinationTypes(unittest.TestCase):
    def test_reasons_map_to_one_kind_each(self):
        import evaluate_benchmark as e
        cases = {"request 1 (GET x): not the task's API (https://x); wrong host, version or base path": "wrong host, version or base path",
                 "request 1 (POST x): body: required field photoUrls is missing": "missing required part or credential",
                 "request 1 (GET x): query parameter sort is not declared": "invented parameter or body field",
                 "request 1 (PATCH x): PATCH is not declared for /albums (declared: GET)": "invented endpoint or method",
                 "request 1 (POST x): body.category.name: expected string, got dict {}": "invalid value or structure",
                 "request 1 (GET x): reads response field id, which the response does not document": "undocumented response field",
                 "uses requests API that does not exist: requests.fetch": "non-existent requests API"}
        for reason, kind in cases.items():
            self.assertEqual(e.hallucination_types([reason]), {kind}, reason)


class ErrorKinds(unittest.TestCase):
    def test_task_error_kinds(self):
        import evaluate_benchmark as e
        cases = {"request 1 (GET x): query hourly=a, the task needs b": "different parameter value",
                 "makes 2 requests; the task needs one": "extra requests",
                 "request 1 (POST x): body {} differs from the task's {}": "request body differs (fields or values)",
                 "request 1 (GET x): a different declared endpoint than the task's (GET /a)": "different declared endpoint",
                 "request 1 (PUT x): method PUT is not acceptable for this task (PATCH)": "method not acceptable for the task",
                 "request 1 (GET x): omits query parameter sha=a that the task specifies": "omitted parameter the task specifies"}
        for reason, kind in cases.items():
            self.assertEqual(e.task_error_types([reason, "no request matches the expected method and endpoint"]), {kind}, reason)

    def test_runtime_failure_kinds(self):
        import evaluate_benchmark as e
        cases = {"AttributeError: 'str' object has no attribute 'get'": "input used as the wrong type (e.g. credential string as a dict)",
                 "KeyError: 'page'": "reads an input the task does not provide", "SyntaxError: invalid syntax": "syntax error",
                 "never calls the API": "makes no request", "Timeout: did not finish within 10 s": "does not finish (timeout)"}
        for reason, kind in cases.items():
            self.assertEqual(e.runtime_failure_type([reason]), kind, reason)
