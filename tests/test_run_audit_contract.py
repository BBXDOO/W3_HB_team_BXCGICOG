import unittest
from unittest.mock import patch

from tools.run_audit import AuditOrchestrator


class TestRunAuditContract(unittest.TestCase):
    def test_bbex_audit_receives_explicit_intent_outcome_and_output(self):
        orchestrator = AuditOrchestrator()
        with patch.object(orchestrator, "print_header"), patch.object(
            orchestrator, "print_summary"
        ), patch.object(orchestrator, "run_agent", return_value=0) as run_agent:
            self.assertEqual(orchestrator.run_audit(), 0)

        bbex_call = run_agent.call_args_list[-1]
        self.assertEqual(bbex_call.args[:3], (
            "BBEX CORE (Philosophical Anchor)",
            "bbex_core_anchor.py",
            "PASSIVE",
        ))
        arguments = bbex_call.args[3]
        self.assertIn("--outcome", arguments)
        self.assertIn("--output", arguments)
        self.assertIn("BBEX_Reflection.md", arguments)


if __name__ == "__main__":
    unittest.main()
