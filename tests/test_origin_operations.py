import json
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path

from core.runtime.agents import get_agent
from core.runtime.agents.origin_operations import ORIGINS, ROOT, OriginFiles, digest
from tools.origin_cycle import directed_work, intake_github, load_state, periodic_work, resolve_followup


class OriginOperationsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for module in ORIGINS:
            profile_path = Path("core/identity/profiles") / (module + ".idp.json")
            profile = json.loads((ROOT / profile_path).read_text())
            profile["file_capabilities"] = {"scopes": [{"path": module, "operations": ["read", "list"]}],
                                            "review_paths": [module + "/state.json"]}
            target = self.root / profile_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(profile))
            home = self.root / module
            home.mkdir()
            (home / "state.json").write_text('{"active": true}')
        self.now = datetime(2026, 10, 9, tzinfo=timezone.utc)

    def execute(self, module, operations, **extra):
        context = {"payload": {"request_type": "origin_file_operations", "operations": operations},
                   "authority_context": {"repo_root": str(self.root)}}
        context.update(extra)
        return get_agent(module).execute("actual work", {}, context)

    def test_all_five_read_create_edit_append_copy_move_delete(self):
        for module in ORIGINS:
            with self.subTest(module=module):
                path = module + "/note.txt"
                made = self.execute(module, [{"action": "create", "path": path, "content": "hello"}])
                self.assertEqual(made["status"], "COMPLETED")
                read = self.execute(module, [{"action": "read", "path": path}])
                self.assertEqual(read["operations"][0]["content"], "hello")
                edited = self.execute(module, [{"action": "edit", "path": path, "old": "hello", "new": "real",
                                               "expected_sha256": digest(b"hello")}])
                self.assertEqual((self.root / path).read_text(), "real")
                backup = self.root / edited["operations"][0]["backup_path"]
                self.assertEqual(backup.read_text(), "hello")
                appended = self.execute(module, [{"action": "append", "path": path, "content": " work",
                                                  "expected_sha256": digest(b"real")}])
                self.assertEqual(appended["status"], "COMPLETED")
                copied = self.execute(module, [{"action": "copy", "path": path, "destination": module + "/copy.txt",
                                               "expected_sha256": digest(b"real work")}])
                self.assertEqual(copied["status"], "COMPLETED")
                moved = self.execute(module, [{"action": "move", "path": path, "destination": module + "/moved.txt",
                                              "expected_sha256": digest(b"real work")}])
                self.assertEqual(moved["status"], "COMPLETED")
                self.assertFalse((self.root / path).exists())
                removed = self.execute(module, [{"action": "delete", "path": module + "/moved.txt",
                                                "expected_sha256": digest(b"real work")}])
                self.assertEqual(removed["status"], "COMPLETED")
                self.assertFalse((self.root / module / "moved.txt").exists())

    def test_write_requires_current_hash_and_preserves_existing_data(self):
        path = self.root / "ChatGPT/state.json"
        original = path.read_bytes()
        failed = self.execute("ChatGPT", [{"action": "write", "path": "ChatGPT/state.json", "content": "wrong"}])
        self.assertEqual(failed["status"], "FAILED")
        self.assertEqual(path.read_bytes(), original)
        self.assertFalse(failed["target_mutated"])

    def test_cross_scope_from_env_works_but_payload_cannot_grant(self):
        operation = {"action": "create", "path": "docs/architecture/flow.md", "content": "actual flow"}
        denied = self.execute("ChatGPT", [operation], origin_scopes={"ChatGPT": [{"path": "docs", "operations": ["create"]}]})
        self.assertEqual(denied["status"], "FAILED")
        context = {"repo_root": str(self.root), "origin_scopes": {"ChatGPT": [{"path": "docs/architecture", "operations": ["create"]}]}}
        allowed = self.execute("ChatGPT", [operation], authority_context=context)
        self.assertEqual(allowed["status"], "COMPLETED")
        self.assertEqual((self.root / operation["path"]).read_text(), "actual flow")

    def test_traversal_and_symlink_escape_cannot_write(self):
        outside = self.root.parent / (self.root.name + "-outside")
        outside.mkdir()
        self.addCleanup(outside.rmdir)
        (self.root / "ChatGPT/link").symlink_to(outside, target_is_directory=True)
        for path in ("../bad.txt", "ChatGPT/link/bad.txt", "/tmp/bad.txt", ".git/config"):
            result = self.execute("ChatGPT", [{"action": "create", "path": path, "content": "bad"}])
            self.assertEqual(result["status"], "FAILED")
        self.assertEqual(list(outside.iterdir()), [])

    def test_partial_failure_is_not_success_and_records_real_mutations(self):
        result = self.execute("Grok", [{"action": "create", "path": "Grok/good.txt", "content": "yes"},
                                       {"action": "create", "path": "Gemini/bad.txt", "content": "no"}])
        self.assertEqual(result["status"], "FAILED")
        self.assertTrue(result["mutated"])
        self.assertEqual(len(result["operations"]), 1)
        self.assertTrue((self.root / result["log_path"]).is_file())

    def test_read_contents_not_duplicated_into_event_log(self):
        result = self.execute("Gemini", [{"action": "read", "path": "Gemini/state.json"}])
        log = json.loads((self.root / result["log_path"]).read_text())
        self.assertNotIn("content", log["operations"][0])
        self.assertTrue(result["log_mutated"])
        self.assertFalse(result["target_mutated"])
        self.assertTrue(result["mutated"])

    def test_7_day_initial_15_day_clean_and_7_day_defect(self):
        self.assertEqual(load_state(self.root, "DeepSeek")["interval_days"], 7)
        clean = periodic_work(self.root, "DeepSeek", self.now)
        self.assertEqual(clean["interval_days"], 15)
        self.assertEqual(periodic_work(self.root, "DeepSeek", self.now + timedelta(days=7))["status"], "NOT_DUE")
        (self.root / "DeepSeek/state.json").write_text('{bad json')
        bad = periodic_work(self.root, "DeepSeek", self.now + timedelta(days=15))
        self.assertEqual(bad["status"], "REVIEW_REQUIRED")
        self.assertEqual(bad["interval_days"], 7)
        self.assertEqual(bad["findings"][0]["kind"], "invalid_syntax")
        self.assertTrue((self.root / bad["report_path"]).exists())

    def test_named_work_bypasses_timer_and_preserves_periodic_due(self):
        periodic_work(self.root, "ChatGPT", self.now)
        due = load_state(self.root, "ChatGPT")["next_due"]
        request = {"request_id": "RQ-1", "source": "BBEX-Core", "intent": "write actual note",
                   "payload": {"operations": [{"action": "create", "path": "ChatGPT/work.txt", "content": "done"}]}}
        completed = directed_work(self.root, "ChatGPT", request, self.now + timedelta(days=1))
        self.assertEqual(completed["status"], "COMPLETED")
        self.assertEqual(load_state(self.root, "ChatGPT")["next_due"], due)
        self.assertEqual(directed_work(self.root, "ChatGPT", request)["status"], "SKIPPED")

    def test_text_intent_followed_up_until_explicit_evidence_resolution(self):
        request = {"request_id": "RQ-2", "source": "BBX19", "intent": "improve flow", "payload": {}}
        directed_work(self.root, "ChatGPT", request, self.now)
        state = load_state(self.root, "ChatGPT")
        pending = periodic_work(self.root, "ChatGPT", self.now + timedelta(days=7))
        self.assertEqual(pending["interval_days"], 7)
        self.assertEqual(pending["pending_count"], 1)
        resolve_followup(self.root, "ChatGPT", state["followups"][0]["receipt"],
                         "ChatGPT/state.json", digest((self.root / "ChatGPT/state.json").read_bytes()))
        clean = periodic_work(self.root, "ChatGPT", self.now + timedelta(days=14))
        self.assertEqual(clean["interval_days"], 15)

    def test_github_owner_mentions_and_structured_operations(self):
        event = {"sender": {"login": "BBXDOO"}, "issue": {"number": 12, "id": 45,
                 "body": '@Gemini @Grok\n```w3-origin\n{"operations": [{"action": "read", "path": "Gemini/state.json"}]}\n```'}}
        requests = intake_github(event, "issues")
        self.assertEqual([item["target"] for item in requests], ["Gemini", "Grok"])
        event["sender"]["login"] = "someone-else"
        self.assertEqual(intake_github(event, "issues"), [])

    def test_concurrent_directed_intake_is_idempotent(self):
        request = {"request_id": "RQ-3", "source": "BBX19", "payload": {
            "operations": [{"action": "create", "path": "Grok/one.txt", "content": "once"}]}}
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: directed_work(self.root, "Grok", request), range(2)))
        self.assertEqual(sorted(item["status"] for item in results), ["COMPLETED", "SKIPPED"])

    def test_binary_write_and_existing_file_mode_are_preserved(self):
        import base64
        path = self.root / "ChatGPT/run.py"
        path.write_text("print('old')")
        path.chmod(0o755)
        result = self.execute("ChatGPT", [{"action": "write", "path": "ChatGPT/run.py", "content": "print('new')",
                                           "expected_sha256": digest(path.read_bytes())}])
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(path.stat().st_mode & 0o777, 0o755)
        data = b"\x00\xff\x01"
        result = self.execute("ChatGPT", [{"action": "create", "path": "ChatGPT/data.bin",
                                           "data_base64": base64.b64encode(data).decode()}])
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual((self.root / "ChatGPT/data.bin").read_bytes(), data)

    def test_invalid_idp_is_a_logged_failure_and_keeps_weekly_followup(self):
        (self.root / "core/identity/profiles/Gemini.idp.json").write_text('{bad')
        result = periodic_work(self.root, "Gemini", self.now)
        self.assertEqual(result["status"], "FAILED")
        self.assertEqual(result["interval_days"], 7)
        self.assertFalse(result["target_mutated"])
        self.assertTrue((self.root / result["log_path"]).is_file())

    def test_proposal_keeps_weekly_cycle_even_when_file_work_succeeded(self):
        request = {"request_id": "RQ-PROPOSAL", "source": "BBX19", "payload": {
            "operations": [{"action": "create", "path": "Grok/proposal.txt", "content": "proposal"}],
            "proposals": ["review this proposal"]}}
        directed_work(self.root, "Grok", request, self.now)
        result = periodic_work(self.root, "Grok", self.now + timedelta(days=7))
        self.assertEqual(result["interval_days"], 7)
        self.assertEqual(result["pending_count"], 1)


if __name__ == "__main__":
    unittest.main()
