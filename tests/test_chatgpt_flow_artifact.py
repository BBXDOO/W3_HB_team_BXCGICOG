import hashlib
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.runtime.agents.chatgpt import ChatGPTAgent
from core.runtime import engine as legacy_engine
from core.runtime.engine_v2 import run, validate_agent_result


class TestChatGPTFlowArtifact(unittest.TestCase):
    def setUp(self):
        self.previous_flow_dir = os.environ.get("W3_CHATGPT_FLOW_DIR")
        self.temp_dir = tempfile.TemporaryDirectory()
        os.environ["W3_CHATGPT_FLOW_DIR"] = self.temp_dir.name

    def tearDown(self):
        if self.previous_flow_dir is None:
            os.environ.pop("W3_CHATGPT_FLOW_DIR", None)
        else:
            os.environ["W3_CHATGPT_FLOW_DIR"] = self.previous_flow_dir
        self.temp_dir.cleanup()

    def test_execute_creates_verifiable_artifact(self):
        result = ChatGPTAgent().execute(
            "flow",
            {
                "run_with": "ChatGPT",
                "role": "Flow Architect",
                "status": "ACTIVE",
                "responsibilities": ["Create a reviewable flow"],
            },
            {
                "trace_id": "trace-artifact-test",
                "source": "BBX19",
                "target": "W3API",
                "request": {
                    "source": "BBX19",
                    "intent": "Create a traceable W3 API request flow",
                    "target": "W3API",
                    "payload": {"requirements": ["preserve trace", "human review"]},
                },
                "payload": {"requirements": ["preserve trace", "human review"]},
            },
        )

        self.assertEqual(result["status"], "COMPLETED")
        self.assertTrue(result["mutated"])
        self.assertTrue(result["review"])
        self.assertFalse(result["external_execution_allowed"])

        artifact = result["artifacts"][0]
        artifact_path = Path(artifact["path"])
        self.assertTrue(artifact_path.exists())

        content = artifact_path.read_text(encoding="utf-8")
        self.assertIn("# W3 Local Flow Artifact", content)
        self.assertIn("Create a traceable W3 API request flow", content)
        self.assertEqual(
            artifact["sha256"],
            hashlib.sha256(content.encode("utf-8")).hexdigest(),
        )

    def test_engine_returns_artifact(self):
        with patch("core.runtime.engine_v2.search_memory", return_value=[]), patch(
            "core.runtime.engine_v2.add_memory"
        ):
            result = run(
                "design",
                request={
                    "source": "BBX19",
                    "intent": "Design a local review-first flow",
                    "target": "W3",
                    "payload": {"requirements": ["artifact path", "trace id"]},
                },
            )

        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["module"], "ChatGPT")
        self.assertEqual(result["agent_result"]["capability"], "local_flow_artifact")
        self.assertEqual(len(result["artifacts"]), 1)
        self.assertTrue(Path(result["artifacts"][0]["path"]).exists())

    def test_unimplemented_module_is_not_completed(self):
        with patch("core.runtime.engine_v2.search_memory", return_value=[]), patch(
            "core.runtime.engine_v2.add_memory"
        ):
            result = run("verify")

        self.assertEqual(result["status"], "UNAVAILABLE")
        self.assertEqual(result["module"], "Gemini")
        self.assertEqual(result["artifacts"], [])
        self.assertTrue(result["agent_result"]["traceable"])

    def test_engine_v2_flags_incomplete_w3lgu_result_contract(self):
        validation = validate_agent_result("PSP2", {"status": "ACTIVE", "module": "PSP2"})

        self.assertEqual(validation["status"], "review_required")
        self.assertIn("confidence", validation["missing_fields"])
        self.assertIn("mutated", validation["missing_fields"])
        self.assertTrue(validation["review"])

    def test_engine_v2_flags_missing_expected_identity(self):
        validation = validate_agent_result(
            "PSP2",
            {
                "module": "PSP2",
                "status": "ACTIVE",
                "confidence": 0.8,
                "input_type": "package:route",
                "decision": "handoff_path_prepared",
                "reason": "route ready",
                "next": ["PX"],
                "standby": [],
                "details": {"route_scope": "cross_series", "identity": {"package_id": "PKG-1"}},
                "mutated": False,
                "traceable": True,
            },
        )

        self.assertEqual(validation["status"], "review_required")
        self.assertEqual(validation["blocking_status"], "REVIEW_REQUIRED")
        self.assertEqual(validation["identity_missing_fields"], ["chain_id", "event_id"])

    def test_engine_v2_rejects_non_dict_agent_result(self):
        with patch("core.runtime.engine_v2.search_memory", return_value=[]), patch(
            "core.runtime.engine_v2.add_memory"
        ) as add_memory, patch("core.runtime.engine_v2.dispatch", return_value="not-a-dict"):
            result = run("route")

        self.assertEqual(result["status"], "UNAVAILABLE")
        self.assertEqual(result["module"], "PSP2")
        self.assertEqual(result["artifacts"], [])
        self.assertTrue(result["agent_result"]["review"])
        add_memory.assert_called_once()
        self.assertEqual(add_memory.call_args.kwargs["score"], 1)

    def test_engine_v2_success_rule_only_completed_scores_success(self):
        with patch("core.runtime.engine_v2.search_memory", return_value=[]), patch(
            "core.runtime.engine_v2.add_memory"
        ) as add_memory, patch(
            "core.runtime.engine_v2.dispatch",
            return_value={
                "status": "ACTIVE",
                "module": "PSP2",
                "confidence": 0.8,
                "input_type": "package:route",
                "decision": "preview_only",
                "reason": "not completed",
                "next": [],
                "standby": [],
                "details": {},
                "mutated": False,
                "traceable": True,
            },
        ):
            result = run("route")

        self.assertEqual(result["status"], "ACTIVE")
        self.assertEqual(add_memory.call_args.kwargs["score"], 1)
        self.assertEqual(add_memory.call_args.kwargs["tags"], ["runtime", "active"])

    def test_legacy_engine_does_not_fabricate_success(self):
        with patch("core.runtime.engine.search_memory", return_value=[]), patch(
            "core.runtime.engine.add_memory"
        ):
            result = legacy_engine.run("verify")

        self.assertEqual(result["status"], "UNAVAILABLE")
        self.assertTrue(result["output"]["review"])
        self.assertFalse(result["output"]["mutated"])


if __name__ == "__main__":
    unittest.main()
