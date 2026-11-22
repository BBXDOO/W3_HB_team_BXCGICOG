"""Isolated temporary-repository tests; never touch the W3 working tree."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).with_name("rams_readme_assistant.py")
spec = importlib.util.spec_from_file_location("rams_readme_assistant", MODULE)
rams = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rams)

class RamsAssistantTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / ".git").mkdir()
        (self.root / "docs" / "empty").mkdir(parents=True)
        (self.root / "docs" / "empty" / ".gitkeep").touch()
        (self.root / "docs" / "present").mkdir()
        (self.root / "docs" / "present" / "README.md").write_text("original")
        (self.root / "docs" / "empty" / "sub").mkdir()

    def test_dry_run_does_not_write(self):
        result = rams.run(self.root, "docs", {1, 2}, "dry-run", "BBX19", "Test")
        self.assertFalse(result["mutated"])
        self.assertFalse((self.root / "docs" / "README.md").exists())
        self.assertEqual(len(result["records"]), 3)

    def test_create_levels_and_idempotency(self):
        result = rams.run(self.root, "docs", {1, 2}, "create", "BBX19", "Test")
        self.assertTrue(result["mutated"])
        self.assertIn("≡ Ar1ra - RAMS", (self.root / "docs" / "README.md").read_text())
        text = (self.root / "docs" / "empty" / "README.md").read_text()
        self.assertIn("≡ Br1ra - RAMS", text)
        self.assertIn(".gitkeep", text)
        self.assertFalse((self.root / "docs" / "empty" / "sub" / "README.md").exists())
        again = rams.run(self.root, "docs", {1, 2}, "create", "BBX19", "Test")
        self.assertFalse(again["mutated"])
        self.assertEqual((self.root / "docs" / "present" / "README.md").read_text(), "original")

    def test_c_level_and_scope_safety(self):
        result = rams.run(self.root, "docs/empty", {3}, "create", "BBX19", "Test")
        self.assertIn("≡ Cr1ra - RAMS", (self.root / "docs" / "empty" / "sub" / "README.md").read_text())
        for scope in ("../outside", "/tmp", "missing"):
            with self.assertRaises(ValueError):
                rams.run(self.root, scope, {1}, "dry-run", "BBX19", "Test")

    def test_symlink_is_not_traversed(self):
        (self.root / "docs" / "linked").symlink_to(self.root / "docs" / "empty", target_is_directory=True)
        result = rams.run(self.root, "docs", {1, 2}, "dry-run", "BBX19", "Test")
        self.assertFalse(any("linked/README" in r["path"] for r in result["records"]))

if __name__ == "__main__":
    unittest.main()
