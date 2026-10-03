import json
import tempfile
import unittest
from pathlib import Path

from core.runtime.agents.copilot_gm import CopilotGmAgent
from tools.document_creation_flow import run_document_creation


class TestDocumentCreationFlow(unittest.TestCase):
    def test_flow_creates_validated_artifact_and_waits_for_human(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "BBX19" / "notes").mkdir(parents=True)
            (root / "BBX19" / "notes" / "README.md").write_text("# Notes\n", encoding="utf-8")
            (root / "requests").mkdir()
            source = root / "requests" / "RQ-DOC-1.md"
            source.write_text("# Request\n", encoding="utf-8")
            request = {
                "request_id": "RQ-DOC-1",
                "requester": "BBX19",
                "final_signoff_required": True,
            }
            agent_result = CopilotGmAgent().execute(
                "governance",
                {},
                {"payload": {
                    "request_type": "document_creation",
                    "document_kind": "thai_markdown_guide",
                    "request_id": "RQ-DOC-1",
                    "source_request": "requests/RQ-DOC-1.md",
                    "artifact_path": "BBX19/notes/THAI_MARKDOWN_GUIDE.md",
                }},
            )

            result = run_document_creation(request=request, agent_result=agent_result, repo_root=root)

            self.assertEqual(result["status"], "WAITING_HUMAN")
            self.assertEqual(result["gemini_result"]["status"], "COMPLETED")
            self.assertTrue((root / result["artifact_path"]).is_file())
            snapshot = json.loads((root / result["orchestration_evidence"]).read_text(encoding="utf-8"))
            self.assertEqual(snapshot["status"], "WAITING_HUMAN")
            self.assertIsNone(snapshot["human_approval"])


if __name__ == "__main__":
    unittest.main()
