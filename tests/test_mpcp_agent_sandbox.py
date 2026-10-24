"""Public sandbox workflow regressions; standard library only."""
import json
from pathlib import Path
import tempfile
import unittest

from tools.mpcp_sandbox import ROOT, run_sandbox
from src.core.blueprint import Blueprint, BlueprintError, parse_blueprint
from protocol.w3lgu import run_line


class SandboxTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / "run"
        self.request = json.loads((ROOT / "tools/agent_sandbox/local_setup.json").read_text())

    def run_request(self, execute=True):
        return run_sandbox(ROOT, self.output, self.request, execute=execute)

    def test_real_setup_and_preserved_source(self):
        result = self.run_request()
        self.assertEqual(result["state"], "SUCCESS", result)
        self.assertTrue(result["artifact_verified"])
        self.assertTrue(result["ledger_verified"])
        self.assertEqual(len(result["ledger"]), 8)
        self.assertTrue(result["provenance"]["original_source_unchanged"])
        self.assertTrue(result["provenance"]["snapshot_unchanged"])
        manifest = json.loads((self.output / "workspace/artifacts/setup.json").read_text())
        self.assertEqual(manifest["blueprint"]["MODE"], "plan")
        for partition in ("A", "B", "C"):
            self.assertTrue((self.output / "workspace/artifacts" / partition).is_dir())
        self.assertFalse(result["phase_ready"])

    def test_no_agreement_waits_without_side_effects(self):
        result = self.run_request(execute=False)
        self.assertEqual(result["state"], "WAIT")
        self.assertIsNone(result["mpcp"])
        self.assertFalse((self.output / "workspace/artifacts").exists())

    def test_stop_and_review_do_not_execute(self):
        for confidence, state in (("0", "STOP"), ("0.5", "WAIT")):
            with self.subTest(confidence=confidence):
                self.output = self.output.parent / ("confidence-" + confidence)
                self.request["event"] = "EVENT:setup,TARGET:MPCP,CONF:" + confidence
                result = self.run_request()
                self.assertEqual(result["state"], state)
                self.assertIsNone(result["mpcp"])
                self.assertFalse((self.output / "workspace/artifacts").exists())

    def test_traversal_is_stopped_before_writes(self):
        self.request["blueprint"] = self.request["blueprint"].replace("A,B,C", "A,../escape")
        result = self.run_request()
        self.assertEqual(result["state"], "STOP")
        self.assertIn("INVALID_PARTITION", result["mpcp"]["error"])
        self.assertFalse((self.output / "workspace/artifacts").exists())

    def test_unsupported_target_reports_gap(self):
        self.request["blueprint"] = self.request["blueprint"].replace("TARGET:local", "TARGET:android")
        result = self.run_request()
        self.assertEqual(result["state"], "STOP")
        self.assertIn("UNSUPPORTED_TARGET", result["mpcp"]["error"])

    def test_malformed_request_retains_error_evidence(self):
        self.request["command"] = "anything"
        result = self.run_request()
        self.assertEqual(result["state"], "STOP")
        self.assertIn("worker_exit", result["error"])
        self.assertIn("request accepts only", (self.output / "worker.log").read_text())
        self.assertTrue((self.output / "result.json").exists())

    def test_output_is_never_overwritten(self):
        self.output.mkdir()
        sentinel = self.output / "keep"
        sentinel.write_text("unchanged")
        with self.assertRaises(FileExistsError):
            self.run_request()
        self.assertEqual(sentinel.read_text(), "unchanged")

    def test_timeout_retains_result_and_log(self):
        result = run_sandbox(ROOT, self.output, self.request, execute=True, timeout=0.00001)
        self.assertEqual(result["state"], "STOP")
        self.assertEqual(result["error"], "worker_timeout")
        self.assertTrue((self.output / "worker.log").exists())

    def test_unknown_blueprint_capabilities_are_not_silently_ignored(self):
        self.request["blueprint"] += "\nBRIDGE:android"
        result = self.run_request()
        self.assertEqual(result["state"], "STOP")
        self.assertIn("UNSUPPORTED_BLUEPRINT_FIELDS", result["mpcp"]["error"])

    def test_blueprint_keeps_declared_mode_and_validates_it(self):
        bp = parse_blueprint("NAME:TEST\nTARGET:local\nMODE:review")
        self.assertEqual(bp.mode, "review")
        self.assertEqual(parse_blueprint(bp.to_w3lgu()).mode, "review")
        self.assertEqual(Blueprint(name="X", target="Y").mode, "observe")
        with self.assertRaises(BlueprintError):
            parse_blueprint("NAME:X\nTARGET:local\nMODE:execute-now")

    def test_each_w3lgu_run_has_its_own_trace(self):
        first, second = run_line("EVENT:one"), run_line("EVENT:two")
        self.assertNotEqual(first.trace_id, second.trace_id)


if __name__ == "__main__":
    unittest.main()
