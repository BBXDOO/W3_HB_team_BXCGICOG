import unittest

from table_x import get_workset_from_px, parse_px


class TestTableX(unittest.TestCase):
    def test_parse_px_string(self):
        self.assertEqual(parse_px("1,1"), (1, 1))
        self.assertEqual(parse_px("PX:[2,1]"), (2, 1))
        self.assertEqual(parse_px("[3,1]"), (3, 1))

    def test_parse_px_tuple_and_list(self):
        self.assertEqual(parse_px((4, 1)), (4, 1))
        self.assertEqual(parse_px([5, 1]), (5, 1))

    def test_px_1_1_rock_fast_patch(self):
        ws = get_workset_from_px("1,1")
        self.assertEqual(ws["px"], [1, 1])
        self.assertEqual(ws["rytm"], "ROCK")
        self.assertEqual(ws["work_type"], "FAST_PATCH")
        self.assertEqual(ws["modew_style"], "Fixer")
        self.assertEqual(ws["boundary"], "temp_patch")
        self.assertFalse(ws["mutated"])
        self.assertTrue(ws["review"])
        self.assertIn("patch_candidate", ws["return_contract"])
        self.assertIn("truth_mutation", ws["deny"])

    def test_px_2_1_jazz_adaptive_rule(self):
        ws = get_workset_from_px("PX:[2,1]")
        self.assertEqual(ws["rytm"], "JAZZ")
        self.assertEqual(ws["work_type"], "ADAPTIVE_RULE")
        self.assertEqual(ws["modew_style"], "Adapter")
        self.assertEqual(ws["boundary"], "observe")
        self.assertFalse(ws["mutated"])
        self.assertTrue(ws["review"])
        self.assertIn("Lua", ws["lang_candidate"])

    def test_px_3_1_edm_pulse_loop(self):
        ws = get_workset_from_px((3, 1))
        self.assertEqual(ws["rytm"], "EDM")
        self.assertEqual(ws["work_type"], "PULSE_LOOP")
        self.assertEqual(ws["modew_style"], "Runner")
        self.assertEqual(ws["boundary"], "observe_loop")
        self.assertFalse(ws["mutated"])
        self.assertTrue(ws["review"])
        self.assertIn("stop_condition", ws["return_contract"])

    def test_px_4_1_ballad_memory_note(self):
        ws = get_workset_from_px("4,1")
        self.assertEqual(ws["rytm"], "BALLAD")
        self.assertEqual(ws["work_type"], "MEMORY_NOTE")
        self.assertEqual(ws["modew_style"], "Keeper")
        self.assertEqual(ws["boundary"], "record_only")
        self.assertFalse(ws["mutated"])
        self.assertTrue(ws["review"])
        self.assertIn("stored_path", ws["return_contract"])

    def test_px_5_1_rnb_human_report(self):
        ws = get_workset_from_px("5,1")
        self.assertEqual(ws["rytm"], "R&B")
        self.assertEqual(ws["work_type"], "HUMAN_REPORT")
        self.assertEqual(ws["modew_style"], "Translator")
        self.assertEqual(ws["boundary"], "readable_output")
        self.assertFalse(ws["mutated"])
        self.assertTrue(ws["review"])
        self.assertIn("risk", ws["return_contract"])
        self.assertIn("risk_hiding", ws["deny"])

    def test_px_6_1_string_knowledge_chain(self):
        ws = get_workset_from_px("6,1")
        self.assertEqual(ws["rytm"], "STRING")
        self.assertEqual(ws["work_type"], "KNOWLEDGE_CHAIN")
        self.assertEqual(ws["modew_style"], "Binder")
        self.assertEqual(ws["boundary"], "knowledge_index")
        self.assertFalse(ws["mutated"])
        self.assertTrue(ws["review"])
        self.assertIn("relation_map", ws["return_contract"])

    def test_px_not_found_fallback(self):
        ws = get_workset_from_px("99,1")
        self.assertEqual(ws["rytm"], "UNKNOWN")
        self.assertTrue(ws["review"])
        self.assertFalse(ws["mutated"])
        self.assertIn("not found", ws["reason"])

    def test_invalid_px_format(self):
        ws = get_workset_from_px("invalid")
        self.assertEqual(ws["rytm"], "UNKNOWN")
        self.assertTrue(ws["review"])
        self.assertIn("Invalid PX format", ws["reason"])

    def test_paper_context_marker(self):
        ws = get_workset_from_px("1,1", paper_context={"paper_id": "demo", "scope": "CROSS_L_ONLY"})
        self.assertTrue(ws["paper_context_received"])
        self.assertEqual(ws["paper_context_keys"], ["paper_id", "scope"])


if __name__ == "__main__":
    unittest.main()
