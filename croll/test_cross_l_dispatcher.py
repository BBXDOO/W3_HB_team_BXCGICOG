import unittest

from cross_l_dispatcher import dispatch_workset


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

    def test_dispatch_with_paper_context_marker(self):
        plan = dispatch_workset("1,1", paper_context={"paper_id": "demo", "scope": "CROSS_L_ONLY"})
        self.assert_safe_plan(plan)
        self.assertEqual(plan["state"], "planned")
        self.assertTrue(plan["workset"]["paper_context_received"])
        self.assertEqual(plan["workset"]["paper_context_keys"], ["paper_id", "scope"])


if __name__ == "__main__":
    unittest.main()
