import contextlib
import importlib.util
import io
import pathlib
import unittest
from unittest import mock


CLI_PATH = pathlib.Path(__file__).resolve().parents[1] / ".cli.py"
SPEC = importlib.util.spec_from_file_location("w3_task_cli", CLI_PATH)
CLI = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CLI)


class TaskCliTests(unittest.TestCase):
    def test_submit_task_reports_queued_task_identity(self):
        created = {
            "task_id": "task-123",
            "agent": "gemini",
            "module": "mpcp",
        }
        output = io.StringIO()

        with mock.patch.object(CLI, "create_task", return_value=created) as create:
            with contextlib.redirect_stdout(output):
                status = CLI.submit_task("Review", "Check contract", "gemini", "mpcp")

        self.assertEqual(status, 0)
        self.assertIn("เข้าคิวแล้ว: task-123", output.getvalue())
        create.assert_called_once_with(
            "Review", "Check contract", agent="gemini", module="mpcp"
        )

    def test_submit_task_returns_failure_for_exception(self):
        error = io.StringIO()
        with mock.patch.object(CLI, "create_task", side_effect=OSError("queue unavailable")):
            with contextlib.redirect_stderr(error):
                status = CLI.submit_task("Review", "Check", "gemini", "mpcp")

        self.assertEqual(status, 1)
        self.assertIn("queue unavailable", error.getvalue())

    def test_submit_task_rejects_result_without_task_id(self):
        with mock.patch.object(CLI, "create_task", return_value={}):
            with contextlib.redirect_stderr(io.StringIO()):
                status = CLI.submit_task("Review", "Check", "gemini", "mpcp")
        self.assertEqual(status, 1)

    def test_parser_trims_values_and_preserves_defaults(self):
        args = CLI.build_parser().parse_args(
            ["submit-task", "--name", "  Review  ", "--desc", "  Check  "]
        )
        self.assertEqual(args.name, "Review")
        self.assertEqual(args.desc, "Check")
        self.assertEqual(args.agent, "copilot-gm")
        self.assertEqual(args.module, "W3Lgu")

    def test_parser_rejects_blank_values(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as raised:
                CLI.build_parser().parse_args(
                    ["submit-task", "--name", "   ", "--desc", "Check"]
                )
        self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
