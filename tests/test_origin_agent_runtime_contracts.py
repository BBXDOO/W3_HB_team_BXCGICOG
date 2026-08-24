import os
import tempfile
import unittest

from core.runtime.agents.cast import CastAgent
from core.runtime.agents.copilot_gm import CopilotGmAgent
from core.runtime.agents.gemini import GeminiAgent
from core.runtime.agents.registry import AGENT_TABLE, get_agent


class TestOriginAgentRuntimeContracts(unittest.TestCase):
    def test_copilot_requires_governance_evidence(self):
        missing = CopilotGmAgent().execute("review", {}, {})
        supplied = CopilotGmAgent().execute(
            "review",
            {},
            {"doc_text": "Governance policy and compliance evidence", "target": "W3"},
        )

        self.assertEqual(missing["status"], "REVIEW_REQUIRED")
        self.assertEqual(supplied["status"], "COMPLETED")
        self.assertFalse(supplied["details"]["merge_performed"])
        self.assertFalse(supplied["details"]["authority_granted"])

    def test_gemini_does_not_verify_without_checks_and_evidence(self):
        unresolved = GeminiAgent().execute("verify", {}, {})
        verified = GeminiAgent().execute(
            "verify",
            {},
            {
                "checks": [{"name": "contract", "passed": True}],
                "evidence": [{"path": "tests/result.txt"}],
                "event_identity": {"chain_id": "CH-1", "event_id": "EV-1", "sequence": 1},
            },
        )

        self.assertEqual(unresolved["status"], "REVIEW_REQUIRED")
        self.assertEqual(verified["status"], "COMPLETED")
        self.assertEqual(verified["decision"], "VERIFIED")

    def test_cast_structures_only_supplied_observations(self):
        missing = CastAgent().execute("interpret", {"kind": "interpretation"}, {})
        structured = CastAgent().execute(
            "interpret",
            {"kind": "interpretation"},
            {"observations": ["runtime returned STOP"], "assumptions": ["input was red"]},
        )

        self.assertEqual(missing["status"], "REVIEW_REQUIRED")
        self.assertEqual(structured["status"], "COMPLETED")
        self.assertFalse(structured["mutated"])
        self.assertFalse(structured["authority"]["decision_allowed"])

    def test_cast_log_write_is_reported_as_mutation(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            previous = os.getcwd()
            os.chdir(temp_dir)
            try:
                result = CastAgent().execute(
                    "assign",
                    {"kind": "assignment", "module": "Gemini", "task": "verify"},
                    {},
                )
            finally:
                os.chdir(previous)

        self.assertEqual(result["status"], "COMPLETED")
        self.assertTrue(result["mutated"])
        self.assertTrue(result["traceable"])

    def test_codex_is_runtime_routable_but_cannot_self_approve(self):
        self.assertIn("Codex", AGENT_TABLE)
        result = get_agent("Codex").execute(
            "implement adapter",
            {},
            {"source": "BBX19", "target": "W3-API"},
        )

        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertEqual(result["module"], "Codex")
        self.assertFalse(result["authority"]["truth_mutation_allowed"])
        self.assertFalse(result["authority"]["self_merge_allowed"])
        packet = result["artifacts"][0]["packet"]
        self.assertEqual(len(packet["w3lgu"].splitlines()), 5)


if __name__ == "__main__":
    unittest.main()
