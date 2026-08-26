import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.runtime.agents.bbex_core import BBEXCore, BBEXCoreAgent


class TestBBEXIntent(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.core = BBEXCore(self.root, clock=lambda: "2026-08-23T00:00:00Z")

    def test_complete_intent_is_ready_but_never_executes(self):
        record = self.core.capture(
            "preserve the W3 learning path",
            desired_outcome="the path remains traceable",
            constraints=["do not rewrite history"],
        )

        self.assertEqual(record["state"], "READY_FOR_ACTION")
        self.assertEqual(record["record_type"], "w3.intent_record")
        self.assertEqual(record["record_profile"], "perception_memory_alignment")
        self.assertEqual(record["role"], "perceptive_intent_anchor")
        self.assertFalse(record["execution"]["allowed"])
        self.assertFalse(record["execution"]["performed"])

    def test_missing_outcome_preserves_uncertainty(self):
        record = self.core.capture("improve continuity")

        self.assertEqual(record["state"], "REFLECTION_REQUIRED")
        self.assertEqual(record["missing"], ["desired_outcome"])
        self.assertIn("observable outcome", record["reflection_question"])

    def test_agent_does_not_write_without_explicit_persistence(self):
        result = BBEXCoreAgent().execute(
            "preserve intent",
            {},
            {"payload": {"desired_outcome": "intent is recorded"}},
        )

        self.assertEqual(result["status"], "COMPLETED")
        self.assertFalse(result["mutated"])
        self.assertEqual(result["artifacts"], [])
        self.assertFalse(result["intent_record"]["execution"]["performed"])

    def test_save_is_explicit_and_writes_markdown(self):
        record = self.core.capture("retain purpose", desired_outcome="purpose is reviewable")
        saved = self.core.save(record, "reflections/intent.md")

        self.assertEqual(saved, self.root / "reflections/intent.md")
        text = saved.read_text(encoding="utf-8")
        self.assertIn("# BBEX Perception Record", text)
        self.assertIn("BBEX perceives, remembers, and reflects intent", text)

    def test_revisions_keep_one_intent_without_overwriting_history(self):
        first = self.core.capture(
            "retain purpose", desired_outcome="purpose is reviewable",
            observations=["first observation"],
        )
        second = self.core.capture(
            "retain purpose", desired_outcome="purpose is reviewable",
            observations=["second observation"], drift_signals=["possible drift"],
        )

        self.assertEqual(first["intent_id"], second["intent_id"])
        self.assertNotEqual(first["record_id"], second["record_id"])
        first_path = self.core.save(first, f"reflections/{first['record_id']}.md")
        second_path = self.core.save(second, f"reflections/{second['record_id']}.md")
        self.assertTrue(first_path.exists())
        self.assertTrue(second_path.exists())
        self.assertIn("first observation", first_path.read_text(encoding="utf-8"))
        self.assertIn("second observation", second_path.read_text(encoding="utf-8"))

    def test_runtime_payload_can_explicitly_persist_intent(self):
        repo_path = Path(__file__).resolve().parents[1]
        saved_path = repo_path / "modules/BBEX-Core/reflections/test-record.md"
        with patch.object(BBEXCore, "save", return_value=saved_path) as save:
            result = BBEXCoreAgent().execute(
                "preserve intent", {},
                {"payload": {
                    "desired_outcome": "intent is recorded",
                    "persist_intent": True,
                }},
            )

        self.assertEqual(result["status"], "COMPLETED")
        self.assertTrue(result["mutated"])
        self.assertEqual(len(result["artifacts"]), 1)
        save.assert_called_once()

    def test_declared_drift_requires_reflection_without_deciding(self):
        record = self.core.capture(
            "review a structural change",
            desired_outcome="preserve W3 root intent",
            observations=["module bypasses its declared boundary"],
            drift_signals=["declared boundary was bypassed"],
        )

        self.assertEqual(record["state"], "REFLECTION_REQUIRED")
        self.assertEqual(record["alignment"]["state"], "DRIFT_REVIEW")
        self.assertFalse(record["alignment"]["decision"])
        self.assertEqual(record["memory"]["observations"], ["module bypasses its declared boundary"])

    def test_bbx19_receives_consultation_and_structural_options(self):
        record = self.core.capture(
            "consider a module boundary",
            source="BBX19",
            desired_outcome="a reviewable boundary",
            support_signals=["keeps intent and action separate"],
            structural_options=["retain BBEX as observation-only"],
        )

        self.assertEqual(record["alignment"]["state"], "SUPPORT")
        self.assertEqual(record["communication"]["mode"], "CONSULTATION")
        self.assertEqual(
            record["communication"]["structural_options"],
            ["retain BBEX as observation-only"],
        )
        self.assertFalse(record["communication"]["direct_operational_answer"])

    def test_other_modules_receive_feedback_not_structural_direction(self):
        record = self.core.capture(
            "request implementation direction",
            source="Gemini",
            desired_outcome="review the intent",
            structural_options=["rewrite the runtime"],
        )

        self.assertEqual(record["communication"]["mode"], "FEEDBACK")
        self.assertEqual(record["communication"]["structural_options"], [])
        self.assertTrue(record["communication"]["feedback_question"])
        self.assertFalse(record["communication"]["direct_operational_answer"])


if __name__ == "__main__":
    unittest.main()
