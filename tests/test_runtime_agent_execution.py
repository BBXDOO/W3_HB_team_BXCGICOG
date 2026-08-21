import json
import tempfile
import unittest
from pathlib import Path

from core.runtime.agents.lrc2 import LRC2Agent
from core.runtime.agents.psp2 import PSP2Agent
from core.runtime.agents.registry import get_agent


class TestRuntimeAgentExecution(unittest.TestCase):
    def test_w3lgu_agents_have_real_execute_contracts(self):
        context = {"trace_id": "TRACE-1", "payload": {"text": "route package trace"}}
        for name in ("REDR", "PSP2", "DTML", "LRC2"):
            result = get_agent(name).execute("route package trace", {"role": "test"}, context)
            self.assertNotEqual(result["status"], "UNAVAILABLE", name)
            self.assertEqual(result["module"], name)
            self.assertTrue(result["traceable"])
            self.assertIn("decision", result)

    def test_psp2_does_not_mutate_source_package(self):
        package = {"package_id": "PKG-1", "text": "route", "next": ["DTML"]}
        original = dict(package)
        result = PSP2Agent().dispatch(package, ["DTML"])
        self.assertEqual(package, original)
        self.assertIn("_psp2_stamp", result["package"])

    def test_lrc2_requires_approval_before_append(self):
        result = LRC2Agent().execute(
            "record", {"record": True}, {"payload": {"event_id": "EV-1"}}
        )
        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertFalse(result["details"]["persistence"]["persisted"])

    def test_lrc2_appends_hash_chained_records(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "lifecycle.jsonl"
            agent = LRC2Agent()
            for event_id in ("EV-1", "EV-2"):
                result = agent.execute(
                    "record lifecycle",
                    {"record": True, "approved": True},
                    {"payload": {"event_id": event_id}, "lifecycle_log_path": str(path)},
                )
                self.assertTrue(result["details"]["persistence"]["persisted"])
            records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(records[0]["previous_hash"], "GENESIS")
            self.assertEqual(records[1]["previous_hash"], records[0]["record_hash"])


if __name__ == "__main__":
    unittest.main()
