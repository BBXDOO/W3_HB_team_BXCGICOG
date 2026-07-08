import unittest

from core.runtime.w3lgu_mfc_logic.redr_mfc_logic import classify_event
from core.runtime.w3lgu_mfc_logic.psp2_mfc_logic import generate_px_stamp, resolve_node, route_package
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

    def test_psp2_generate_px_stamp_matches_route_package(self):
        package = {"target": "DTML", "next": ["DTML"], "text": "trace route"}
        result = route_package(package).as_dict()
        self.assertEqual(generate_px_stamp(package), result["details"]["route_stamp"])

    def test_psp2_resolve_node_returns_first_route_target(self):
        self.assertEqual(resolve_node({"target": "PX", "next": ["PX"], "text": "cross route"}), "PX")

    def test_psp2_infers_lrc2_route_from_memory(self):
        result = route_package("memory checkpoint package")
        data = result.as_dict()
        self.assertEqual(data["module"], "PSP2")
        self.assertIn("LRC2", data["next"])
        self.assertEqual(data["details"]["route_quality"], "inferred")

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


    def test_psp2_classifies_w3db_and_w3db_append_as_cross_series(self):
        result = route_package({"next": ["W3DB", "W3DB_APPEND"], "text": "cross handoff"})
        data = result.as_dict()
        self.assertEqual(data["status"], "REVIEW_REQUIRED")
        self.assertIn("W3DB", data["details"]["cross_routes"])
        self.assertIn("W3DB_APPEND", data["details"]["cross_routes"])
        self.assertEqual(data["details"]["unknown_routes"], [])
        self.assertEqual(data["details"]["route_scope"], "cross_series")

    def test_redr_preserves_identity_from_nested_request_payload(self):
        result = classify_event({
            "request": {
                "payload": {
                    "chain_id": "CHAIN-NEST",
                    "event_id": "EVT-NEST",
                    "package_id": "PKG-NEST",
                    "text": "route package",
                }
            },
            "text": "route package",
        })
        package = result.as_dict()["details"]["package"]
        self.assertEqual(package["package_id"], "PKG-NEST")
        self.assertEqual(package["identity"]["chain_id"], "CHAIN-NEST")
        self.assertEqual(package["identity"]["event_id"], "EVT-NEST")
        self.assertEqual(package["identity"]["package_id"], "PKG-NEST")


    def test_psp2_unwraps_redr_package_before_route_classification(self):
        redr = classify_event({"target": "PX", "text": "route package to PX"}).as_dict()
        result = route_package(redr)
        data = result.as_dict()
        self.assertEqual(data["status"], "REVIEW_REQUIRED")
        self.assertIn("PX", data["details"]["cross_routes"])
        self.assertIn("PX", data["next"])

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
        self.assertEqual(data["details"]["prior_stage_summary"], psp2["reason"])
        self.assertEqual(data["details"]["identity"]["package_id"], "PKG-LRC2")
        self.assertEqual(data["details"]["identity"]["route_scope"], "cross_series")
        self.assertEqual(data["details"]["persistence"]["mode"], "preview_only")
        self.assertFalse(data["details"]["persistence"]["persisted"])
        self.assertFalse(data["details"]["persistence"]["overwrite_historical_truth"])

    def test_lrc2_missing_identity_creates_explicit_unknown(self):
        result = checkpoint_lifecycle({"module": "PSP2", "decision": "handoff_path_prepared"})
        data = result.as_dict()
        unknown = data["details"]["identity"]["unknown"]
        self.assertTrue(unknown["unknown"])
        self.assertIn("chain_id", unknown["fields"])
        self.assertIn("event_id", unknown["fields"])
        self.assertEqual(unknown["reason"], "missing_from_input")
        self.assertTrue(unknown["review"])

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
