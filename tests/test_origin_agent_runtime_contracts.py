import os
import json
import tempfile
import unittest

from core.runtime.agents.cast import CastAgent
from core.runtime.agents.copilot_gm import CopilotGmAgent
from core.runtime.agents.gemini import GeminiAgent
from core.runtime.agents.registry import AGENT_TABLE, get_agent
from core.runtime.engine_v2 import build_context
from core.module_loader.router import execution_plan


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

    def test_copilot_invalid_packet_fails_safe(self):
        result = CopilotGmAgent().execute("review", None, "invalid")

        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertEqual(result["decision"], "invalid_review_input")
        self.assertFalse(result["mutated"])

    def test_copilot_accepts_structured_evidence_without_crashing(self):
        result = CopilotGmAgent().execute(
            "review",
            {},
            {"doc_text": {"policy": "governance", "checks": ["compliance"]}},
        )

        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["details"]["evidence_type"], "dict")

    def test_copilot_reads_api_payload_evidence(self):
        result = CopilotGmAgent().execute(
            "governance",
            execution_plan("governance"),
            {"payload": {"evidence": "governance policy compliance"}},
        )

        self.assertEqual(result["status"], "COMPLETED")

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

    def test_cast_router_plan_infers_reasoning_kind(self):
        result = CastAgent().execute(
            "reason",
            execution_plan("reason"),
            {"payload": {"observations": ["runtime returned STOP"]}},
        )

        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["action"], "structure_context")

    def test_engine_context_rejects_non_mapping_request_without_crashing(self):
        context = build_context("reason", "invalid")

        self.assertEqual(context["request"], {})
        self.assertIsNone(context["source"])

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

    def test_cast_invalid_packet_fails_safe(self):
        result = CastAgent().execute("assign", None, None)

        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertFalse(result["mutated"])

    def test_cast_requires_assignment_identity_before_write(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = os.path.join(temp_dir, "cast.jsonl")
            result = CastAgent().execute(
                "assign",
                {"kind": "assignment", "task": "verify"},
                {"cast_log_path": log_path},
            )

            self.assertEqual(result["status"], "REVIEW_REQUIRED")
            self.assertFalse(os.path.exists(log_path))

    def test_cast_preserves_explicit_false_report_and_actual_log_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = os.path.join(temp_dir, "nested", "cast.jsonl")
            result = CastAgent().execute(
                "report",
                {"kind": "subsystem_report", "subsystem": "MPCP", "reported": "false"},
                {"cast_log_path": log_path},
            )

            with open(log_path, "r", encoding="utf-8") as handle:
                persisted = json.loads(handle.readline())

            self.assertEqual(result["status"], "COMPLETED")
            self.assertFalse(persisted["reported"])
            self.assertEqual(persisted["log_path"], os.path.realpath(log_path))
            self.assertEqual(result["artifacts"][0]["path"], os.path.realpath(log_path))

    def test_cast_log_failure_returns_review_required(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = CastAgent().execute(
                "assign",
                {"kind": "assignment", "module": "Gemini", "task": "verify"},
                {"cast_log_path": temp_dir},
            )

        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertFalse(result["mutated"])
        self.assertIn("write failed", result["reason"])

    def test_cast_health_summary_survives_malformed_log_record(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = os.path.join(temp_dir, "cast.jsonl")
            with open(log_path, "w", encoding="utf-8") as handle:
                handle.write("not-json\n")
                handle.write(
                    json.dumps(
                        {
                            "type": "subsystem_report",
                            "timestamp": "2026-08-24T00:00:00Z",
                            "subsystem": "MPCP",
                            "reported": True,
                        }
                    )
                    + "\n"
                )
            result = CastAgent().execute(
                "health",
                {"kind": "health_summary"},
                {"cast_log_path": log_path},
            )

        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["summary"]["malformed_records"], 1)
        self.assertEqual(result["summary"]["subsystems"]["MPCP"]["total_reports"], 1)

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
