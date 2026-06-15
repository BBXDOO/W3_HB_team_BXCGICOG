from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from wx.engine_index import BoxRegistryError, find_templates, load_template_registry, search_by_px
from wx.indexor import suggest_references
from wx.portdc import BoxExportError, export_registered_template


class TestBoxEngineIndex(unittest.TestCase):
    def test_registry_is_valid_and_paths_exist(self):
        registry = load_template_registry()
        self.assertEqual(registry["version"], "1.0")
        self.assertGreaterEqual(len(registry["templates"]), 3)
        self.assertTrue(all(item["path"].startswith("wx/templates/") for item in registry["templates"]))

    def test_search_by_px_is_normalized_and_deterministic(self):
        template = search_by_px("PX:[1,1]")
        self.assertIsNotNone(template)
        self.assertEqual(template["template_id"], "PAPER:FAST_PATCH_V1")
        self.assertEqual(template["px"], ["1,1"])

    def test_combined_filters_return_only_matching_reference(self):
        templates = find_templates(px=[1, 1], work_type="fast_patch", rytm="rock")
        self.assertEqual(
            [item["template_id"] for item in templates],
            ["PAPER:FAST_PATCH_V1", "CROSS_L:ROCK_BLOCK_V1"],
        )

    def test_indexor_never_grants_copy_or_execution(self):
        response = suggest_references(px="2,1")
        self.assertEqual(response["state"], "suggested")
        self.assertFalse(response["execution_allowed"])
        self.assertFalse(response["mutated"])
        self.assertFalse(response["copy_allowed_by_runtime"])
        self.assertTrue(response["human_review_required"])
        self.assertEqual(response["suggestions"][0]["template_id"], "PAPER:ADAPTIVE_RULE_V1")

    def test_portdc_exports_data_without_writing(self):
        response = export_registered_template("PAPER:FAST_PATCH_V1")
        self.assertIn("# Fast Patch Paper", response["content"])
        self.assertFalse(response["execution_allowed"])
        self.assertFalse(response["mutated"])
        self.assertFalse(response["write_performed"])
        self.assertTrue(response["human_copy_required"])

    def test_portdc_rejects_unknown_template(self):
        with self.assertRaises(BoxExportError):
            export_registered_template("UNKNOWN")

    def test_registry_rejects_front_matter_drift(self):
        registry = load_template_registry()
        registry["templates"][0]["version"] = "9.9.9"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.json"
            path.write_text(json.dumps(registry), encoding="utf-8")
            with self.assertRaises(BoxRegistryError):
                load_template_registry(path)

    def test_registry_rejects_repository_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.json"
            path.write_text(json.dumps({
                "version": "1.0",
                "templates": [{
                    "template_id": "BAD",
                    "name": "Bad",
                    "path": "../outside.md",
                    "version": "1.0.0",
                    "owner": "BBX19",
                    "status": "active",
                    "work_type": "BAD",
                    "rytm": "BAD",
                    "px": ["1,1"],
                    "boundary": "observe",
                    "deny": ["truth_mutation"]
                }]
            }), encoding="utf-8")
            with self.assertRaises(BoxRegistryError):
                load_template_registry(path)


if __name__ == "__main__":
    unittest.main()
