from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.runtime.agents.registry import AGENT_TABLE, get_agent


MAIN_AGENTS = {
    "BBX19",
    "BBEX-Core",
    "ChatGPT",
    "Gemini",
    "Copilot-Gm",
    "Codex",
    "DeepSeek",
    "Grok",
    "Cast",
}


class TestMainAgentReadiness(unittest.TestCase):
    def test_all_main_agents_are_runtime_registered(self):
        self.assertTrue(MAIN_AGENTS.issubset(AGENT_TABLE))

    def test_bbx19_requires_explicit_human_decision(self):
        result = get_agent("BBX19").execute(
            "approve release",
            {},
            {"source": "SYSTEM"},
        )

        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertFalse(result["execution"]["allowed"])
        self.assertFalse(result["mutated"])

    def test_bbex_core_records_intent_without_executing(self):
        result = get_agent("BBEX-Core").execute(
            "preserve W3 intent",
            {},
            {"payload": {"desired_outcome": "intent remains traceable"}},
        )

        self.assertEqual(result["status"], "COMPLETED")
        self.assertFalse(result["intent_record"]["execution"]["performed"])
        self.assertFalse(result["mutated"])

    def test_chatgpt_creates_only_local_review_artifact(self):
        with tempfile.TemporaryDirectory() as temp_dir, patch.dict(
            os.environ,
            {"W3_CHATGPT_FLOW_DIR": temp_dir},
        ):
            result = get_agent("ChatGPT").execute(
                "design a review flow",
                {"role": "Flow Architect", "responsibilities": ["design flow"]},
                {"trace_id": "main-readiness-chatgpt", "source": "BBX19"},
            )

            self.assertEqual(result["status"], "COMPLETED")
            self.assertTrue(result["mutated"])
            self.assertTrue(result["review"])
            self.assertFalse(result["external_execution_allowed"])
            self.assertTrue(Path(result["artifacts"][0]["path"]).exists())

    def test_gemini_does_not_verify_without_evidence(self):
        result = get_agent("Gemini").execute("verify", {}, {})

        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertEqual(result["decision"], "UNRESOLVED")
        self.assertFalse(result["mutated"])

    def test_copilot_does_not_grant_governance_authority(self):
        result = get_agent("Copilot-Gm").execute(
            "review governance",
            {},
            {"doc_text": "governance policy compliance"},
        )

        self.assertEqual(result["status"], "COMPLETED")
        self.assertFalse(result["details"]["merge_performed"])
        self.assertFalse(result["details"]["authority_granted"])
        self.assertFalse(result["authority"]["merge_allowed"])

    def test_codex_prepares_packet_without_execution_authority(self):
        result = get_agent("Codex").execute(
            "implement adapter",
            {},
            {"source": "BBX19", "target": "W3-API"},
        )

        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertFalse(result["mutated"])
        self.assertFalse(result["authority"]["truth_mutation_allowed"])
        self.assertFalse(result["authority"]["self_merge_allowed"])

    def test_deepseek_remains_planner_only(self):
        result = get_agent("DeepSeek").execute(
            "plan PX:[1,1]",
            {},
            {"px": "1,1"},
        )

        self.assertEqual(result["status"], "PLANNED")
        self.assertTrue(result["planner_only"])
        self.assertFalse(result["execution_allowed"])
        self.assertFalse(result["mutated"])

    def test_grok_creates_observation_artifact_not_final_truth(self):
        with tempfile.TemporaryDirectory() as temp_dir, patch.dict(
            os.environ,
            {"W3_GROK_INSIGHT_DIR": temp_dir},
        ):
            result = get_agent("Grok").execute(
                "observe runtime signals",
                {"role": "Pattern Intelligence"},
                {
                    "trace_id": "main-readiness-grok",
                    "signals": [{"state": "REVIEW_REQUIRED"}],
                },
            )

            self.assertEqual(result["status"], "COMPLETED")
            self.assertTrue(result["mutated"])
            self.assertTrue(result["review"])
            self.assertFalse(result["external_execution_allowed"])
            self.assertTrue(Path(result["artifacts"][0]["path"]).exists())

    def test_cast_structures_only_supplied_observations(self):
        result = get_agent("Cast").execute(
            "interpret",
            {"kind": "interpretation"},
            {"observations": ["runtime returned REVIEW_REQUIRED"]},
        )

        self.assertEqual(result["status"], "COMPLETED")
        self.assertFalse(result["mutated"])
        self.assertTrue(result["review"])
        self.assertFalse(result["authority"]["decision_allowed"])


if __name__ == "__main__":
    unittest.main()
