import hashlib
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.runtime.agents.chatgpt import ChatGPTAgent
from core.runtime.engine_v2 import run


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
        with patch("core.runtime.engine_v2.add_memory"):
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
        with patch("core.runtime.engine_v2.add_memory"):
            result = run("verify")

        self.assertEqual(result["status"], "UNAVAILABLE")
        self.assertEqual(result["module"], "Gemini")
        self.assertEqual(result["artifacts"], [])


if __name__ == "__main__":
    unittest.main()
