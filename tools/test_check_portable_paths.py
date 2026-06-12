import unittest

from tools.check_portable_paths import case_collisions, path_problems


class TestPortablePaths(unittest.TestCase):
    def test_accepts_portable_unicode_and_normal_paths(self):
        self.assertEqual(path_problems("protocol/docs/คู่มือ.md"), [])
        self.assertEqual(path_problems("Grok/requests/request_001.md"), [])

    def test_rejects_windows_invalid_characters(self):
        self.assertTrue(path_problems("Grok/requests/request_001.md:"))
        self.assertTrue(path_problems("docs/name*.md"))

    def test_rejects_trailing_space_and_period(self):
        self.assertTrue(path_problems("docs/ARCHITECTURE /paper.md"))
        self.assertTrue(path_problems("docs/paper./README.md"))

    def test_rejects_windows_device_names(self):
        self.assertTrue(path_problems("docs/CON.md"))
        self.assertTrue(path_problems("docs/aux.txt"))

    def test_detects_case_insensitive_collisions(self):
        collisions = case_collisions(["docs/README.md", "docs/readme.md", "docs/guide.md"])
        self.assertEqual(len(collisions), 1)


if __name__ == "__main__":
    unittest.main()
