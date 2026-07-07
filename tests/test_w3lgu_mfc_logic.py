import unittest

from core.runtime.w3lgu_mfc_logic.redr_mfc_logic import classify_event
from core.runtime.w3lgu_mfc_logic.psp2_mfc_logic import (
    generate_px_stamp,
    register_node,
    resolve_node,
    route_package,
)
from core.runtime.w3lgu_mfc_logic.dtml_mfc_logic import trace_decision
from core.runtime.w3lgu_mfc_logic.lrc2_mfc_logic import checkpoint_lifecycle
from core.runtime.agents.psp2 import PSP2Agent


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

    def test_psp2_generates_px_stamp(self):
        pkg = {"package_id": "PKG-001"}
        stamp = generate_px_stamp(pkg)
        self.assertTrue(stamp.startswith("PX:LN"))
        self.assertIn("'", stamp)

    def test_psp2_stamp_with_system_id(self):
        pkg = {"package_id": "XS-042", "_room": "CA"}
        stamp = generate_px_stamp(pkg, system_id="HBISOCITY")
        self.assertTrue(stamp.startswith("PX:HBISOCITY/"))
        self.assertIn("LNCA", stamp)

    def test_psp2_resolves_known_node(self):
        node = resolve_node("DTML")
        self.assertEqual(node, "ni:dtml")

    def test_psp2_resolves_unknown_node_as_cross_system(self):
        node = resolve_node("UNKNOWN_SYS")
        self.assertTrue(node.startswith("xs:"))

    def test_psp2_can_register_new_node(self):
        register_node("WHUB", "ni:whub_main")
        node = resolve_node("WHUB")
        self.assertEqual(node, "ni:whub_main")

    def test_psp2_agent_stamp(self):
        agent = PSP2Agent()
        pkg = {"package_id": "PKG-099"}
        stamp = agent.stamp(pkg)
        self.assertTrue(stamp.startswith("PX:"))

    def test_psp2_agent_run(self):
        agent = PSP2Agent()
        result = agent.run("forward", {"package": {"package_id": "PKG-001"}}, {})
        self.assertIn("PSP2", result)
        self.assertIn("forwarded", result)

    def test_psp2_agent_execute(self):
        agent = PSP2Agent()
        result = agent.execute("forward", {"package": {"package_id": "PKG-001"}}, {})
        self.assertEqual(result["status"], "DISPATCHED")
        self.assertFalse(result["mutated"])
        self.assertIn("stamp", result)
        self.assertIn("node", result)

    def test_psp2_preserves_cross_route_for_review(self):
        result = route_package(
            {
                "package_id": "PKG-CROSS",
                "source": "W3-API",
                "target": "PX",
                "next": ["PX", "W3DB_APPEND", "LRC2"],
                "text": "cross route package",
            }
        )
        data = result.as_dict()
        self.assertEqual(data["status"], "REVIEW_REQUIRED")
        self.assertTrue(data["review"])
        self.assertIn("PX", data["next"])
        self.assertIn("W3DB_APPEND", data["details"]["cross_routes"])
        self.assertEqual(data["details"]["route_scope"], "mixed")
        self.assertFalse(data["mutated"])

    def test_psp2_preserves_unknown_route_for_review(self):
        result = route_package({"next": ["NEW_SYSTEM"], "text": "handoff"})
        data = result.as_dict()
        self.assertEqual(data["status"], "REVIEW_REQUIRED")
        self.assertIn("NEW_SYSTEM", data["next"])
        self.assertEqual(data["details"]["unknown_routes"], ["NEW_SYSTEM"])
        self.assertEqual(data["details"]["route_scope"], "unknown")

    def test_psp2_preserves_cross_route_for_review(self):
        result = route_package(
            {
                "package_id": "PKG-CROSS",
                "source": "W3-API",
                "target": "PX",
                "next": ["PX", "W3DB_APPEND", "LRC2"],
                "text": "cross route package",
            }
        )
        data = result.as_dict()
        self.assertEqual(data["status"], "REVIEW_REQUIRED")
        self.assertTrue(data["review"])
        self.assertIn("PX", data["next"])
        self.assertIn("W3DB_APPEND", data["details"]["cross_routes"])
        self.assertEqual(data["details"]["route_scope"], "mixed")
        self.assertFalse(data["mutated"])

    def test_psp2_preserves_unknown_route_for_review(self):
        result = route_package({"next": ["NEW_SYSTEM"], "text": "handoff"})
        data = result.as_dict()
        self.assertEqual(data["status"], "REVIEW_REQUIRED")
        self.assertIn("NEW_SYSTEM", data["next"])
        self.assertEqual(data["details"]["unknown_routes"], ["NEW_SYSTEM"])
        self.assertEqual(data["details"]["route_scope"], "unknown")

    def test_dtml_builds_review_trace(self):
        result = trace_decision({"text": "runtime review", "review_required": True})
        data = result.as_dict()
        self.assertEqual(data["module"], "DTML")
        self.assertEqual(data["status"], "REVIEW_REQUIRED")
        self.assertIn("LRC2", data["next"])
        self.assertIn("trace", data["details"])
        self.assertEqual(data["details"]["review_state"], "review_required")

    def test_dtml_waits_on_unclear_trace(self):
        result = trace_decision("plain message without context clue")
        data = result.as_dict()
        self.assertEqual(data["module"], "DTML")
        self.assertEqual(data["status"], "WAIT")
        self.assertEqual(data["details"]["review_state"], "unclear")

    def test_dtml_reviews_unknown_and_cross_routes(self):
        psp2 = route_package({"next": ["PX", "NEW_SYSTEM"], "text": "cross handoff"}).as_dict()
        result = trace_decision(psp2)
        data = result.as_dict()
        self.assertEqual(data["status"], "REVIEW_REQUIRED")
        self.assertEqual(data["details"]["route_scope"], "mixed")
        self.assertIn("NEW_SYSTEM", data["details"]["unknown_routes"])
        self.assertIn("PX", data["details"]["cross_routes"])

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

    def test_lrc2_records_route_stamp_and_identity(self):
        psp2 = route_package({"package_id": "PKG-LRC2", "next": ["PX"], "text": "cross handoff"}).as_dict()
        result = checkpoint_lifecycle(psp2)
        data = result.as_dict()
        self.assertEqual(data["details"]["route_stamp"], psp2["details"]["route_stamp"])
        self.assertEqual(data["details"]["identity"]["package_id"], "PKG-LRC2")
        self.assertEqual(data["details"]["identity"]["route_scope"], "cross_series")

    def test_minimum_chain(self):
        redr = classify_event("route package to decision trace")
        # PSP2 now stamps + forwards via node (not W3LguLogicResult)
        psp2_result = generate_px_stamp({"package_id": "chain-001"})
        self.assertTrue(psp2_result.startswith("PX:"))

        dtml = trace_decision({"text": "decision trace", "review_required": True})
        lrc2 = checkpoint_lifecycle(dtml.as_dict())

        self.assertEqual(redr.as_dict()["module"], "REDR")
        self.assertEqual(dtml.as_dict()["module"], "DTML")
        self.assertEqual(lrc2.as_dict()["module"], "LRC2")
        self.assertTrue(lrc2.as_dict()["traceable"])


if __name__ == "__main__":
    unittest.main()
