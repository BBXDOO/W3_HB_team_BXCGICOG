import unittest

from core.runtime.w3lgu_mfc_logic.redr_mfc_logic import classify_event
from core.runtime.w3lgu_mfc_logic.psp2_mfc_logic import route_package
from core.runtime.w3lgu_mfc_logic.dtml_mfc_logic import trace_decision
from core.runtime.w3lgu_mfc_logic.lrc2_mfc_logic import checkpoint_lifecycle


class TestW3LguMFCLogic(unittest.TestCase):
    def test_redr_classifies_risk_event(self):
        result = classify_event("git conflict requires review")
        data = result.as_dict()
        self.assertEqual(data["module"], "REDR")
        self.assertEqual(data["status"], "REVIEW_REQUIRED")
        self.assertIn("DTML", data["next"])
        self.assertFalse(data["mutated"])

    def test_redr_classifies_memory_event(self):
        result = classify_event("create memory checkpoint for lifecycle history")
        data = result.as_dict()
        self.assertEqual(data["input_type"], "event:memory")
        self.assertIn("LRC2", data["next"])
        self.assertIn("PSP2", data["standby"])

    def test_psp2_creates_route_stamp(self):
        result = route_package({"target": "DTML", "next": ["DTML"], "text": "trace route"})
        data = result.as_dict()
        self.assertEqual(data["module"], "PSP2")
        self.assertEqual(data["status"], "ACTIVE")
        self.assertIn("DTML", data["next"])
        self.assertIn("route_stamp", data["details"])
        self.assertEqual(data["details"]["route_quality"], "explicit")

    def test_psp2_infers_lrc2_route_from_memory(self):
        result = route_package("memory checkpoint package")
        data = result.as_dict()
        self.assertEqual(data["module"], "PSP2")
        self.assertIn("LRC2", data["next"])
        self.assertEqual(data["details"]["route_quality"], "inferred")

    def test_dtml_builds_review_trace(self):
        result = trace_decision({"text": "runtime review", "review_required": True})
        data = result.as_dict()
        self.assertEqual(data["module"], "DTML")
        self.assertEqual(data["status"], "REVIEW_REQUIRED")
        self.assertIn("LRC2", data["next"])
        self.assertIn("trace", data["details"])
        self.assertEqual(data["details"]["review_state"], "review_required")

    def test_dtml_waits_on_unclear_trace(self):
        result = trace_decision("plain message without route marker")
        data = result.as_dict()
        self.assertEqual(data["module"], "DTML")
        self.assertEqual(data["status"], "WAIT")
        self.assertEqual(data["details"]["review_state"], "unclear")

    def test_lrc2_creates_checkpoint_preview(self):
        result = checkpoint_lifecycle({"module": "REDR", "decision": "review_trace_required"})
        data = result.as_dict()
        self.assertEqual(data["module"], "LRC2")
        self.assertEqual(data["status"], "ACTIVE")
        self.assertIn("checkpoint_key", data["details"])
        self.assertFalse(data["mutated"])

    def test_lrc2_detects_memory_record_phase(self):
        result = checkpoint_lifecycle("memory checkpoint record for continuity")
        data = result.as_dict()
        self.assertEqual(data["details"]["record_phase"], "memory")
        self.assertGreaterEqual(data["confidence"], 0.8)

    def test_minimum_chain(self):
        redr = classify_event("route package to decision trace")
        psp2 = route_package(redr.as_dict())
        dtml = trace_decision(psp2.as_dict())
        lrc2 = checkpoint_lifecycle(dtml.as_dict())

        self.assertEqual(redr.as_dict()["module"], "REDR")
        self.assertEqual(psp2.as_dict()["module"], "PSP2")
        self.assertEqual(dtml.as_dict()["module"], "DTML")
        self.assertEqual(lrc2.as_dict()["module"], "LRC2")
        self.assertTrue(lrc2.as_dict()["traceable"])


if __name__ == "__main__":
    unittest.main()
