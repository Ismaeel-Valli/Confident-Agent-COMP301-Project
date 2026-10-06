"""Tests for run discovery (roles, quantization, archives) and the stats compiler's tidy tables.
Run: python -m unittest discover tests"""
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evaluator import runs  # noqa: E402
import compile_stats as cs  # noqa: E402


def manifest(label, quant, version, model="qwen3.5-9b", gpu=True, mode="baseline"):
    settings = {"benchmark_version": version, "mode": mode, "model": model, "temperature": 0.2, "max_tokens": 4096,
                "thinking": "off", "seed": None}
    if mode == "intervention":
        settings.update({"max_turns": 4, "package_evidence_sha256": "abc"})
    power = {"backend": "LibreHardwareMonitor", "gpus": [{"name": "AMD Radeon RX 9070 XT"}], "idle_w": {"gpu": 50.0, "cpu": 40.0}} if gpu else {}
    return {"model_label": label, "settings": settings, "context_limit": 30208,
            "lmstudio_model_info": {"id": model, "quantization": quant, "arch": "qwen35"},
            "invocations": [{"started": "2026-09-28T10:00:00+00:00", "git_commit": "3e85a3c1234",
                             "environment": {"cpu": "Ryzen", "ram_gb": 32.0, "gpus": []}, "power": power}]}


def write_run(base: Path, label, quant, version, as_zip=False, nested="", **kw):
    for mode, folder in runs.MODE_DIRS.items():
        body = json.dumps(manifest(label, quant, version, mode=mode, **kw))
        if as_zip:
            target = base / nested
            target.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(target / f"{folder}.zip", "a") as z:
                z.writestr(f"{folder}/{label}/run_manifest.json", body)
                z.writestr(f"{folder}/{label}/T1/result.json", json.dumps({"meta": {"duration_seconds": 1.5}}))
        else:
            d = base / folder / label
            d.mkdir(parents=True, exist_ok=True)
            (d / "run_manifest.json").write_text(body, encoding="utf-8")


class RunDiscovery(unittest.TestCase):
    def test_roles_follow_the_newest_benchmark_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            write_run(base, "Q4-early", "Q4_K_M", "2026-09-26.2", as_zip=True, nested="Completed Runs/Q4/Run 1")
            write_run(base, "Q4-second", "Q4_K_M", "2026-09-27.2", as_zip=True, nested="Completed Runs/Q4/Run 2")
            write_run(base, "Q8-live", "Q8_0", "2026-09-27.2")  # a run folder on disk
            found = runs.discover(base)
        self.assertEqual({k: v["role"] for k, v in found.items()}, {"Q4-early": "preliminary", "Q4-second": "main", "Q8-live": "main"})
        self.assertEqual(found["Q8-live"]["quantization"], "Q8_0")
        self.assertEqual(found["Q4-second"]["machine_gpu"], "AMD Radeon RX 9070 XT")
        self.assertEqual(found["Q4-second"]["power_backend"], "LibreHardwareMonitor")
        self.assertEqual(found["Q4-second"]["commits"], ["3e85a3c"])

    def test_label_that_disagrees_with_the_reported_quantization_is_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_run(Path(tmp), "Qwen3.5-9B-Q6_0-full", "Q6_K", "2026-09-27.2")
            write_run(Path(tmp), "Qwen3.5-9B-Q8_0-full", "Q8_0", "2026-09-27.2")
            found = runs.discover(Path(tmp))
        self.assertFalse(found["Qwen3.5-9B-Q6_0-full"]["label_matches_quantization"])
        self.assertTrue(found["Qwen3.5-9B-Q8_0-full"]["label_matches_quantization"])

    def test_archived_results_are_readable_and_a_folder_wins_over_an_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            write_run(base, "R", "Q4_K_M", "2026-09-27.2", as_zip=True, nested="Completed Runs/R")
            files = runs.BenchmarkFiles(base)
            self.assertEqual(files.result("baseline", "R", "T1")["meta"]["duration_seconds"], 1.5)
            folder = base / "Baseline_Tests" / "R" / "T1"
            folder.mkdir(parents=True)
            (folder / "result.json").write_text(json.dumps({"meta": {"duration_seconds": 9.0}}), encoding="utf-8")
            self.assertEqual(files.result("baseline", "R", "T1")["meta"]["duration_seconds"], 9.0)
            self.assertIsNone(files.result("baseline", "R", "missing"))
            files.close()

    def test_archives_named_after_the_mode_hold_the_label_folder(self):
        """Completed Runs/<model>/Baseline_Tests.zip and Baseline_Tests/<label>.zip both hold <label>/..."""
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            for mode, folder in runs.MODE_DIRS.items():
                for archive, label in ((base / "Completed Runs" / "Q8" / f"{folder}.zip", "Q8-run"),
                                       (base / "Old" / folder / "Q6-run.zip", "Q6-run")):
                    archive.parent.mkdir(parents=True, exist_ok=True)
                    with zipfile.ZipFile(archive, "w") as z:
                        z.writestr(f"{label}/run_manifest.json", json.dumps(manifest(label, label[:2], "2026-09-27.2", mode=mode)))
                        z.writestr(f"{label}/T1/result.json", json.dumps({"meta": {"duration_seconds": 2.0}}))
            files = runs.BenchmarkFiles(base)
            self.assertEqual(files.labels(), {"Q8-run", "Q6-run"})
            self.assertEqual(files.result("intervention", "Q8-run", "T1")["meta"]["duration_seconds"], 2.0)
            self.assertEqual(files.manifest("baseline", "Q6-run")["lmstudio_model_info"]["quantization"], "Q6")
            files.close()


class StatsTables(unittest.TestCase):
    def test_metrics_long_splits_mode_and_skips_text(self):
        rows = cs.metrics_long([{"model_label": "R", "quantization": "Q8_0", "run_role": "main", "benchmark_version": "v",
                                 "dimension": "api", "group": "GitHub", "n": 10, "b_hallucination_rate": 0.5,
                                 "i_hallucination_rate": 0.1, "hallucination_repairs": 4, "note": "text", "b_energy_j": None}])
        got = {(r["mode"], r["metric"]): r["value"] for r in rows}
        self.assertEqual(got, {("paired", "n"): 10, ("baseline", "hallucination_rate"): 0.5,
                               ("intervention", "hallucination_rate"): 0.1, ("paired", "hallucination_repairs"): 4})
        self.assertTrue(all(r["group"] == "GitHub" and r["quantization"] == "Q8_0" for r in rows))

    def test_ci_columns_are_numeric(self):
        ci = cs.ci_columns("b_hallucination_rate", 0.1, 100)
        self.assertLess(ci["b_hallucination_rate_ci_low"], 0.1)
        self.assertGreater(ci["b_hallucination_rate_ci_high"], 0.1)
        self.assertEqual(cs.ci_columns("x", None, 0), {"x_ci_low": None, "x_ci_high": None})


class PromptRowBooleans(unittest.TestCase):
    """The first version of the compiler blanked every true/false column (corrections, reply
    handling, behaviour checks); this builds a row from minimal data and checks they are filled."""

    def row(self):
        task = {"task_id": "T1", "natural_language_instruction": "x",
                "api_specification": {"api_name": "GitHub", "method": "GET", "endpoint": "/e", "auth": None, "coverage": "Provider"},
                "metadata": {"category": "read", "difficulty": "easy", "operation_family_id": "f"}}
        ev = {"baseline_class": "A", "shown_class": "correct", "final_class": "correct", "first_class": "A", "delivered": True,
              "pilot": False, "decision": "deliver", "ewcs": 0.8, "code_shown": True, "shown_is_unapproved_reply": False,
              "protocol_notes": [], "baseline_reasons": [], "shown_reasons": [], "baseline_a_reasons": [], "baseline_b_reasons": [],
              "shown_a_reasons": [], "shown_b_reasons": [],
              "baseline_behaviour": {"returns_expected_value": True, "empty_response_ok": False, "error_raises": True},
              "shown_behaviour": {"returns_expected_value": True, "empty_response_ok": True, "error_raises": True}}
        ires = {"jsonl": {"first_has_contradiction": True, "correction_attempted": True, "correction_allowed": True,
                          "correction_count": 1, "final_reply_prompted": False, "verification_calls": 2, "tool_failures": 0,
                          "first_decision": "abstain"},
                "meta": {"turns": [{}, {}, {}], "final_reply": {"matches_report": True}, "duration_seconds": 30.0}}
        return cs.prompt_row("R", task, ev, {"jsonl": {}, "meta": {"duration_seconds": 5.0}}, ires,
                             {"role": "main", "quantization": "Q8_0"})

    def test_true_false_columns_are_recorded(self):
        r = self.row()
        self.assertEqual((r["i_first_had_contradiction"], r["i_correction_attempted"], r["i_correction_allowed"]), (1, 1, 1))
        self.assertEqual((r["i_final_reply_prompted"], r["i_reply_matches_report"]), (0, 1))
        self.assertEqual((r["b_returns_expected"], r["b_empty_response_ok"], r["b_error_raises"]), (1, 0, 1))
        self.assertEqual(r["i_correction_outcome"], "A->correct")

    def test_group_summary_uses_them(self):
        g = cs.group_summary([self.row()])
        self.assertEqual(g["i_corrections_attempted"], 1)
        self.assertEqual(g["i_correction_success_rate"], 1.0)
        self.assertEqual(g["i_final_reply_prompted_rate"], 0.0)
        self.assertEqual(g["b_behaviour_all_ok_rate"], 0.0)
        self.assertEqual(g["i_behaviour_all_ok_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
