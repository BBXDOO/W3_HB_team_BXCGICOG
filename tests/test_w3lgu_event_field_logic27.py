import unittest

from core.runtime.w3lgu_mfc_logic.event_field import build_event_field
from core.runtime.w3lgu_mfc_logic.logic27_registry import LOGIC27_SLOTS, get_logic_slot
from core.runtime.w3lgu_mfc_logic.logic27_selector import select_logic27


class TestW3LguEventFieldLogic27(unittest.TestCase):
    def test_logic27_registry_has_27_slots(self):
        self.assertEqual(len(LOGIC27_SLOTS), 27)
        self.assertEqual(get_logic_slot("L1-C1").name, "input_clear")
        self.assertEqual(get_logic_slot("L3-C2").name, "shadow_copy")

    def test_event_field_keeps_identity(self):
        field = build_event_field(
            chain_id="chain-a",
            event_id="event-1",
            sequence=3,
            source="W3-API",
            intent="route package",
            confidence=0.8,
        )
        data = field.to_dict()
        self.assertEqual(data["chain_id"], "chain-a")
        self.assertEqual(data["event_id"], "event-1")
        self.assertEqual(data["sequence"], 3)
        self.assertFalse(data["mutated"])
        self.assertTrue(data["traceable"])
        self.assertEqual(data["owner_scope"], "W3LGU_MFC_REFERENCE_ONLY")

    def test_clear_route_event_selects_route_slot(self):
        field = build_event_field(
            chain_id="chain-route",
            event_id="event-route",
            source="Cross-X",
            intent="route handoff to next event",
            confidence=0.8,
        )
        result = select_logic27(field).as_dict()
        self.assertEqual(result["module"], "LOGIC27")
        self.assertEqual(result["details"]["logic_slot"]["slot_id"], "L2-C1")
        self.assertEqual(result["details"]["event_identity"]["chain_id"], "chain-route")
        self.assertIn("PSP2", result["next"])

    def test_unclear_event_selects_shadow_slot(self):
        field = build_event_field(
            chain_id="chain-shadow",
            event_id="event-shadow",
            intent="unclear fuzzy field",
            confidence=0.2,
        )
        result = select_logic27(field).as_dict()
        self.assertEqual(result["status"], "WAIT")
        self.assertEqual(result["details"]["logic_slot"]["slot_id"], "L3-C2")
        self.assertIn("LRC2", result["next"])
        self.assertFalse(result["mutated"])

    def test_borrow_field_selects_borrow_slot(self):
        field = build_event_field(
            chain_id="chain-borrow",
            event_id="event-borrow",
            intent="need external field context",
            context={"borrow_field": True},
            confidence=0.55,
        )
        result = select_logic27(field).as_dict()
        self.assertEqual(result["status"], "WAIT")
        self.assertEqual(result["details"]["logic_slot"]["slot_id"], "L2-C8")
        self.assertIn("Cross-X", result["next"])
        self.assertTrue(result["details"]["proposal_only"])
        self.assertTrue(result["details"]["reference_only"])

    def test_logic27_cannot_approve_execution(self):
        field = build_event_field(
            chain_id="chain-advisory",
            event_id="event-advisory",
            intent="route handoff ready",
            confidence=0.9,
        )
        result = select_logic27(field).as_dict()
        self.assertTrue(result["details"]["proposal_only"])
        self.assertTrue(result["details"]["advisory_only"])
        self.assertFalse(result["details"]["execution_allowed"])
        self.assertFalse(result["details"]["approval_authority"])
        self.assertFalse(result["mutated"])


if __name__ == "__main__":
    unittest.main()
