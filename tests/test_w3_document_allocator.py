from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import tools.w3_document_allocator as w3doc


class TestW3DocumentAllocator(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "docs/source").mkdir(parents=True)
        (self.root / "docs/target").mkdir(parents=True)
        (self.root / "docs/source/origin.md").write_text("# Origin\n", encoding="utf-8")
        (self.root / "docs/target/README.md").write_text("# Target\n", encoding="utf-8")
        self.box_registry = patch.object(
            w3doc, "load_template_registry",
            return_value={"version": "1.0", "templates": []},
        )
        self.box_suggestions = patch.object(
            w3doc, "suggest_references",
            return_value={
                "state": "not_found", "suggestions": [], "planner_only": True,
                "execution_allowed": False, "mutated": False,
                "copy_allowed_by_runtime": False, "human_review_required": True,
            },
        )
        self.box_registry.start()
        self.box_suggestions.start()

    def tearDown(self):
        self.box_suggestions.stop()
        self.box_registry.stop()
        self.temporary.cleanup()

    def spec(self, **changes) -> w3doc.DocumentSpec:
        values = {
            "title": "Thai Markdown Guide",
            "target": "docs/target/guide.md",
            "am_type": "II",
            "group": "LEARN",
            "owner": "Copilot-Gm",
            "maker": "W3 Document Allocator",
            "body": "เนื้อหาทดสอบ",
            "derived_from": ("docs/source/origin.md",),
            "request_id": "RQ-1",
        }
        values.update(changes)
        return w3doc.DocumentSpec(**values)

    def test_dry_run_preserves_box_boundary_and_does_not_write(self):
        result = w3doc.allocate_document(self.spec(), repo_root=self.root)
        self.assertEqual(result["status"], "PLANNED")
        self.assertFalse(result["mutated"])
        self.assertTrue(result["box"]["planner_only"])
        self.assertFalse(result["box"]["execution_allowed"])
        self.assertEqual(result["box"]["target_state"], "conditional")
        self.assertFalse((self.root / "docs/target/guide.md").exists())

    def test_create_writes_ams_shape_and_receipt(self):
        result = w3doc.allocate_document(
            self.spec(), mode="create", authorized_by="BBX19", repo_root=self.root,
        )
        target = self.root / "docs/target/guide.md"
        text = target.read_text(encoding="utf-8")
        self.assertEqual(result["status"], "CREATED")
        self.assertTrue(result["mutated"])
        self.assertEqual(result["artifact"]["sha256"], hashlib.sha256(target.read_bytes()).hexdigest())
        self.assertIn("AM_TYPE: II", text)
        self.assertIn("GROUP: LEARN", text)
        self.assertIn("## Movement line", text)
        self.assertIn("[docs/source/origin.md](../source/origin.md)", text)
        self.assertIn("## Owner line", text)

    def test_am_i_allows_empty_lineage_with_valid_yaml_shape(self):
        origin = self.spec(am_type="I", group="BUILD", derived_from=())
        result = w3doc.allocate_document(
            origin, mode="create", authorized_by="BBX19", repo_root=self.root,
        )
        text = (self.root / "docs/target/guide.md").read_text(encoding="utf-8")
        self.assertEqual(result["status"], "CREATED")
        self.assertIn("DERIVED_FROM: []", text)
        self.assertIn("No upstream document declared (AM:I origin)", text)

    def test_create_refuses_existing_file_without_overwrite(self):
        target = self.root / "docs/target/guide.md"
        target.write_text("original", encoding="utf-8")
        with self.assertRaisesRegex(w3doc.AllocationError, "already exists"):
            w3doc.allocate_document(
                self.spec(), mode="create", authorized_by="BBX19", repo_root=self.root,
            )
        self.assertEqual(target.read_text(encoding="utf-8"), "original")

    def test_update_requires_current_digest(self):
        target = self.root / "docs/target/guide.md"
        target.write_text("old", encoding="utf-8")
        with self.assertRaisesRegex(w3doc.AllocationError, "expected_sha256"):
            w3doc.allocate_document(
                self.spec(), mode="update", authorized_by="BBX19", repo_root=self.root,
            )
        digest = hashlib.sha256(b"old").hexdigest()
        result = w3doc.allocate_document(
            self.spec(body="new"), mode="update", authorized_by="BBX19",
            expected_sha256=digest, repo_root=self.root,
        )
        self.assertEqual(result["status"], "UPDATED")
        self.assertEqual(result["artifact"]["previous_sha256"], digest)

    def test_rejects_unsafe_or_wrong_target(self):
        for target in ("../escape.md", "/tmp/escape.md", "docs/target/not-markdown.txt"):
            with self.subTest(target=target), self.assertRaises(w3doc.AllocationError):
                w3doc.inspect_allocation(self.spec(target=target), repo_root=self.root)

    def test_am_ii_and_iii_require_existing_lineage(self):
        with self.assertRaisesRegex(w3doc.AllocationError, "DERIVED_FROM"):
            w3doc.inspect_allocation(self.spec(derived_from=()), repo_root=self.root)
        with self.assertRaisesRegex(w3doc.AllocationError, "does not exist"):
            w3doc.inspect_allocation(
                self.spec(derived_from=("docs/source/missing.md",)), repo_root=self.root,
            )

    def test_duplicate_filename_is_reported(self):
        (self.root / "docs/source/guide.md").write_text("# Existing\n", encoding="utf-8")
        plan = w3doc.inspect_allocation(self.spec(), repo_root=self.root)
        self.assertEqual(plan["duplicates"], ["docs/source/guide.md"])
        self.assertTrue(any("same filename" in warning for warning in plan["warnings"]))

    def test_box_managed_source_space_is_prohibited(self):
        (self.root / "wx/templates/paper").mkdir(parents=True)
        request = self.spec(target="wx/templates/paper/new.md")
        plan = w3doc.inspect_allocation(request, repo_root=self.root)
        self.assertEqual(plan["box"]["target_state"], "prohibited")
        with self.assertRaisesRegex(w3doc.AllocationError, "prohibited"):
            w3doc.allocate_document(
                request, mode="create", authorized_by="BBX19", repo_root=self.root,
            )

    def test_orchestration_handler_returns_real_artifact_evidence(self):
        handler = w3doc.make_orchestration_handler(
            self.spec(), authorized_by="BBX19", repo_root=self.root,
        )
        result = handler({"blocker": {"reason": "module has no file executor"}})
        self.assertTrue(result["resolved"])
        self.assertIn("#sha256=", result["evidence"])
        self.assertEqual(result["receipt"]["artifact"]["path"], "docs/target/guide.md")


if __name__ == "__main__":
    unittest.main()
