import unittest

from core.runtime.agents.bbex_core import BBEXCore
from core.runtime.agents.bbx19 import BBX19Agent


class TestBBX19Action(unittest.TestCase):
    def setUp(self):
        self.agent = BBX19Agent()
        self.plan = {"role": "Final Human Decision"}

    def test_missing_explicit_decision_requires_review(self):
        result = self.agent.execute("merge release", self.plan, {"source": "BBX19"})
        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertFalse(result["execution"]["allowed"])
        self.assertFalse(result["mutated"])

    def test_approve_records_authority_without_executing(self):
        context = {"source": "BBX19", "target": "W3", "trace_id": "trace-1", "payload": {
            "decision": "approve", "confirmed": True,
            "reason": "Targeted checks passed.",
            "evidence": ["PR #276", "30/30 tests"],
            "annotation": "Approved for integration only.",
        }}
        result = self.agent.execute("merge release", self.plan, context)
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["decision"], "APPROVE")
        self.assertTrue(result["execution"]["allowed"])
        self.assertFalse(result["execution"]["performed"])
        self.assertEqual(result["decision_record"]["decided_by"], "BBX19")

    def test_non_bbx19_source_cannot_fabricate_approval(self):
        result = self.agent.execute("merge release", self.plan, {"source": "SYSTEM", "payload": {
            "decision": "approve", "confirmed": True, "reason": "Looks ready.",
            "evidence": "PR #276", "annotation": "Automated suggestion.",
        }})
        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertIn("explicit_bbx19_confirmation", result["missing"])

    def test_repeated_decision_has_stable_identity(self):
        context = {"source": "SYSTEM", "payload": {
            "decision": "hold", "approved_by": "BBX19",
            "reason": "Await external evidence.", "evidence": ["audit-01"],
            "annotations": ["Recheck after evidence arrives."],
        }}
        first = self.agent.execute("release", self.plan, context)
        second = self.agent.execute("release", self.plan, context)
        self.assertEqual(first["decision_record"]["decision_id"], second["decision_record"]["decision_id"])
        self.assertFalse(first["execution"]["allowed"])

    def test_ready_bbex_intent_is_linked_to_bbx19_decision(self):
        intent = BBEXCore(".", clock=lambda: "2026-08-24T00:00:00Z").capture(
            "preserve W3 intent",
            desired_outcome="the change remains aligned and traceable",
            support_signals=["keeps perception separate from action"],
        )
        result = self.agent.execute("approve structural change", self.plan, {
            "source": "BBX19",
            "payload": {
                "decision": "approve",
                "confirmed": True,
                "reason": "The declared outcome and implementation evidence align.",
                "evidence": ["targeted tests passed"],
                "annotation": "Approval applies only to this recorded intent.",
                "intent_record": intent,
            },
        })

        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["intent_link"]["intent_id"], intent["intent_id"])
        self.assertEqual(result["decision_record"]["intent_link"]["state"], "READY_FOR_ACTION")

    def test_bbx19_does_not_approve_drift_record_without_explicit_override(self):
        intent = BBEXCore(".", clock=lambda: "2026-08-24T00:00:00Z").capture(
            "change a module boundary",
            desired_outcome="preserve the root intent",
            drift_signals=["the proposed path bypasses the declared boundary"],
        )
        payload = {
            "decision": "approve",
            "confirmed": True,
            "reason": "Proceed after contextual review.",
            "evidence": ["BBEX intent record"],
            "annotation": "Reviewed by BBX19.",
            "intent_record": intent,
        }
        result = self.agent.execute(
            "approve structural change", self.plan, {"source": "BBX19", "payload": payload}
        )

        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertIn("declared_intent_drift", result["intent_blockers"])
        self.assertFalse(result["execution"]["allowed"])

        payload["override_intent_review"] = True
        overridden = self.agent.execute(
            "approve structural change", self.plan, {"source": "BBX19", "payload": payload}
        )
        self.assertEqual(overridden["status"], "COMPLETED")
        self.assertTrue(overridden["intent_link"]["override_applied"])

    def test_override_cannot_authorize_a_fabricated_intent_record(self):
        result = self.agent.execute("approve structural change", self.plan, {
            "source": "BBX19",
            "payload": {
                "decision": "approve",
                "confirmed": True,
                "reason": "Manual review completed.",
                "evidence": ["external note"],
                "annotation": "Do not trust untyped input.",
                "override_intent_review": True,
                "intent_record": {
                    "record_type": "untrusted.record",
                    "intent_id": "fake-1",
                    "module": "SYSTEM",
                    "state": "READY_FOR_ACTION",
                },
            },
        })

        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertIn("invalid_intent_record_type", result["missing"])
        self.assertIn("invalid_intent_source_module", result["missing"])


if __name__ == "__main__":
    unittest.main()
