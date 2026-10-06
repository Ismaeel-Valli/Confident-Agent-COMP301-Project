"""Regression tests for dataset integrity checks. No HTTP requests or code execution."""
import copy
import json
import unittest
from pathlib import Path

from validate_dataset import ROOT, TemplateReader, validate_record


class ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = [json.loads(s) for s in (ROOT / 'output/rest_api_tasks_v1_DRAFT.jsonl').read_text(encoding='utf-8').splitlines()]

    def pick(self, predicate):
        return copy.deepcopy(next(r for r in self.records if predicate(r)))

    def test_wrong_http_method_in_code_is_rejected(self):
        r = self.pick(lambda r: r['api_specification']['method'] == 'GET')
        r['ground_truth']['code'] = r['ground_truth']['code'].replace("requests.request('GET'", "requests.request('POST'")
        self.assertTrue(validate_record(r))

    def test_wrong_parameter_location_is_rejected(self):
        r = self.pick(lambda r: bool(r['test_case']['expected_request']['query']))
        r['test_case']['expected_request']['json_body'] = r['test_case']['expected_request']['query']
        r['test_case']['expected_request']['query'] = {}
        self.assertTrue(validate_record(r))

    def test_unknown_query_parameter_is_rejected(self):
        r = copy.deepcopy(self.records[0])
        r['test_case']['expected_request']['query']['invented_filter'] = 'anything'
        self.assertTrue(validate_record(r))

    def test_required_body_field_is_rejected_when_missing(self):
        r = self.pick(lambda r: r['metadata']['api_name'] == 'Petstore' and r['api_specification']['endpoint'] == '/pet')
        del r['test_case']['expected_request']['json_body']['name']
        self.assertTrue(validate_record(r))

    def test_wrong_input_type_is_rejected(self):
        r = self.pick(lambda r: r['metadata']['api_name'] == 'Open-Meteo')
        r['test_case']['inputs']['latitude'] = {'not': 'a coordinate'}
        self.assertTrue(validate_record(r))

    def test_invented_base_url_is_rejected_even_if_code_agrees(self):
        r = copy.deepcopy(self.records[0])
        old = r['api_specification']['base_url']; new = 'https://invented.example.test'
        r['api_specification']['base_url'] = new
        r['test_case']['expected_request']['url'] = r['test_case']['expected_request']['url'].replace(old, new)
        r['ground_truth']['code'] = r['ground_truth']['code'].replace(old, new)
        self.assertTrue(validate_record(r))

    def test_snapshot_change_is_rejected(self):
        r = copy.deepcopy(self.records[0]); r['api_specification']['source_sha256'] = '0' * 64
        self.assertTrue(validate_record(r))

    def test_endpoint_in_prompt_is_rejected(self):
        r = copy.deepcopy(self.records[0]); r['natural_language_instruction'] += ' Call ' + r['api_specification']['endpoint']
        self.assertTrue(validate_record(r))

    def test_normal_english_pull_requests_is_accepted(self):
        r = self.pick(lambda r: r['api_specification']['endpoint'] == '/repos/{owner}/{repo}/pulls' and r['api_specification']['method'] == 'GET')
        self.assertEqual([], validate_record(r))

    def test_path_substitution_handles_spaces_without_running_code(self):
        r = self.pick(lambda r: r['metadata']['api_name'] == 'REST Countries' and '{value}' in r['api_specification']['endpoint'])
        r['test_case']['inputs']['value'] = 'United Kingdom'
        parsed = TemplateReader(r['test_case']['inputs']).request(r['ground_truth']['code'])
        self.assertIn('United%20Kingdom', parsed['url'])

    def test_arbitrary_call_is_not_evaluated(self):
        code = "def solve(inputs):\n    url = __import__('os').getcwd()\n"
        with self.assertRaises((ValueError, KeyError)):
            TemplateReader({}).request(code)


if __name__ == '__main__':
    unittest.main()
