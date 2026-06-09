import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class TestCrossLCli(unittest.TestCase):
    def run_cli(self, *args, env=None):
        child_env = os.environ.copy()
        if env:
            child_env.update(env)
        return subprocess.run(
            [sys.executable, "-m", "croll", *args],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=child_env,
        )

    def test_plan_outputs_portable_json(self):
        result = self.run_cli("plan", "PX:[2,1]", "--context", '{"paper_id":"demo"}')
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["contract_version"], "1.0")
        self.assertEqual(payload["modew"], "Adapter")
        self.assertFalse(payload["execution_allowed"])
        self.assertEqual(payload["workset"]["paper_context_keys"], ["paper_id"])

    def test_plan_forces_utf8_on_legacy_console_encoding(self):
        result = self.run_cli(
            "--compact",
            "plan",
            "1,1",
            env={"PYTHONIOENCODING": "cp1252"},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["workset"]["symbol"], "▲")

    def test_context_can_be_loaded_from_utf8_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "บริบท.json"
            path.write_text('{"scope":"ทดสอบ"}', encoding="utf-8")
            result = self.run_cli("lookup", "1,1", "--context", f"@{path}")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["paper_context_keys"], ["scope"])

    def test_list_is_stable(self):
        result = self.run_cli("--compact", "list")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["coordinates"][0], [1, 1])

    def test_validate_boundary_example(self):
        result = self.run_cli(
            "validate",
            "boundary",
            "croll/examples/boundary.w3-internal.json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["valid"])
        self.assertEqual(payload["kind"], "boundary")

    def test_validate_rejects_unsafe_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "unsafe.json"
            path.write_text(
                '{"contract_version":"1.0","kind":"croll-boundary"}',
                encoding="utf-8",
            )
            result = self.run_cli("validate", "boundary", str(path))
        self.assertEqual(result.returncode, 2)
        self.assertIn("missing required fields", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_invalid_context_is_reported_without_traceback(self):
        result = self.run_cli("plan", "1,1", "--context", "[]")
        self.assertEqual(result.returncode, 2)
        self.assertIn("context must be a JSON object", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
