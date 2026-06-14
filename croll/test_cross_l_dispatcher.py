import unittest

from croll.cross_l_dispatcher import dispatch_cross_code, dispatch_workset


class TestCrossLDispatcher(unittest.TestCase):
    def assert_safe_plan(self, plan):
        self.assertFalse(plan["execution_allowed"])
        self.assertFalse(plan["mutated"])
        self.assertTrue(plan["review"])
        self.assertEqual(plan["scope"], "CROSS_L_ONLY")
        self.assertTrue(plan["safety"]["planner_only"])
        self.assertFalse(plan["safety"]["modew_execution_allowed"])
        self.assertFalse(plan["safety"]["truth_mutation_allowed"])
        self.assertFalse(plan["safety"]["repo_write_allowed"])
        self.assertFalse(plan["safety"]["direct_merge_allowed"])

    def test_dispatch_px_1_1_rock_fast_patch(self):
        plan = dispatch_workset("1,1")
        self.assert_safe_plan(plan)
        self.assertEqual(plan["state"], "planned")
        self.assertEqual(plan["modew"], "Fixer")
        self.assertEqual(plan["action"], "call_modew_stub_only")
        self.assertEqual(plan["workset"]["rytm"], "ROCK")
        self.assertEqual(plan["workset"]["work_type"], "FAST_PATCH")
        self.assertEqual(plan["workset"]["boundary"], "temp_patch")

    def test_dispatch_px_2_1_jazz_adaptive_rule(self):
        plan = dispatch_workset("PX:[2,1]")
        self.assert_safe_plan(plan)
        self.assertEqual(plan["state"], "planned")
        self.assertEqual(plan["modew"], "Adapter")
        self.assertEqual(plan["workset"]["rytm"], "JAZZ")
        self.assertEqual(plan["workset"]["work_type"], "ADAPTIVE_RULE")
        self.assertEqual(plan["workset"]["boundary"], "observe")

    def test_dispatch_px_3_1_edm_runner(self):
        plan = dispatch_workset((3, 1))
        self.assert_safe_plan(plan)
        self.assertEqual(plan["state"], "planned")
        self.assertEqual(plan["modew"], "Runner")
        self.assertEqual(plan["workset"]["rytm"], "EDM")
        self.assertIn("unlimited_loop", plan["workset"]["deny"])

    def test_dispatch_unknown_px_requires_review(self):
        plan = dispatch_workset("99,1")
        self.assert_safe_plan(plan)
        self.assertEqual(plan["state"], "review")
        self.assertEqual(plan["modew"], "UNKNOWN")
        self.assertEqual(plan["action"], "review_before_dispatch")
        self.assertEqual(plan["workset"]["rytm"], "UNKNOWN")
        self.assertIn("not found", plan["reason"])

    def test_dispatch_invalid_px_requires_review(self):
        plan = dispatch_workset("invalid")
        self.assert_safe_plan(plan)
        self.assertEqual(plan["state"], "review")
        self.assertEqual(plan["modew"], "UNKNOWN")
        self.assertEqual(plan["action"], "review_before_dispatch")
        self.assertEqual(plan["workset"]["rytm"], "UNKNOWN")
        self.assertIn("Invalid PX format", plan["reason"])

    def test_dispatch_can_include_read_only_box_suggestion(self):
        plan = dispatch_workset("1,1", enable_box_suggestion=True)
        self.assert_safe_plan(plan)
        suggestion = plan["suggested_template"]
        self.assertTrue(suggestion["reference_only"])
        self.assertTrue(suggestion["path"].startswith("wx/templates/"))

    def test_dispatch_box_suggestion_falls_back_to_none(self):
        plan = dispatch_workset("99,99", enable_box_suggestion=True)
        self.assert_safe_plan(plan)
        self.assertIsNone(plan["suggested_template"])

    def test_dispatch_with_paper_context_marker(self):
        plan = dispatch_workset("1,1", paper_context={"paper_id": "demo", "scope": "CROSS_L_ONLY"})
        self.assert_safe_plan(plan)
        self.assertEqual(plan["state"], "planned")
        self.assertTrue(plan["workset"]["paper_context_received"])
        self.assertEqual(plan["workset"]["paper_context_keys"], ["paper_id", "scope"])

    def test_cross_code_dispatch_binds_plan_to_ecs_event(self):
        envelope = dispatch_cross_code(
            "2,1",
            chain_id="cross-test",
            event_id="ECS-06-TEST",
            paper_context={"event_system": "PX"},
        )

        self.assertEqual(envelope["kind"], "cross-code-dispatch")
        self.assertEqual(envelope["chain_id"], "cross-test")
        self.assertEqual(envelope["event_id"], "ECS-06-TEST")
        self.assertEqual(envelope["handoff"]["from"], "Cross-L")
        self.assertEqual(envelope["handoff"]["to"], "Modew")
        self.assertEqual(envelope["handoff"]["boundary"], "observe")
        self.assertFalse(envelope["execution_allowed"])
        self.assertFalse(envelope["mutated"])
        self.assertTrue(envelope["review"])

    def test_cross_code_dispatch_requires_trace_identity(self):
        with self.assertRaisesRegex(ValueError, "chain_id"):
            dispatch_cross_code("1,1", chain_id="", event_id="ECS-01")

    def test_inactive_cross_code_returns_handled_value_without_plan(self):
        envelope = dispatch_cross_code(
            "1,1",
            chain_id="cross-inactive",
            event_id="ECS-01-INACTIVE",
            active=False,
        )

        self.assertEqual(envelope["state"], "inactive")
        self.assertEqual(envelope["reason"], "cross_code_not_in_use")
        self.assertIsNone(envelope["cross_l_plan"])
        self.assertIsNone(envelope["handoff"])
        self.assertTrue(envelope["return_value"]["handled"])
        self.assertFalse(envelope["execution_allowed"])
        self.assertFalse(envelope["mutated"])


if __name__ == "__main__":
    unittest.main()
