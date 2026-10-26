import json
import tempfile
import unittest
from pathlib import Path

from tools.forge import analyze


class ForgeAnalyserTests(unittest.TestCase):
    def test_empty_directory_is_valid_and_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = analyze(root)
            second = analyze(root)
            self.assertEqual(first["summary"]["files"], 0)
            self.assertEqual(first, second)
            self.assertEqual(first["preliminary_feasibility"]["category"], "unknown")

    def test_pc_executable_is_classified_as_binary_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "game.exe").write_bytes(b"not a real executable")
            report = analyze(root)
            self.assertEqual(report["preliminary_feasibility"]["category"], "binary_only")
            self.assertEqual(report["summary"]["files"], 1)

    def test_disc_image_is_not_claimed_as_convertible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "disc.iso").write_bytes(b"not a real disc image")
            report = analyze(root)
            self.assertEqual(report["preliminary_feasibility"]["category"], "binary_or_disc_only")
            self.assertTrue(any("cannot be converted" in warning for warning in report["warnings"]))

    def test_source_like_file_is_only_a_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "main.cpp").write_text("int main() {}", encoding="utf-8")
            report = analyze(root)
            self.assertEqual(report["preliminary_feasibility"]["category"], "source_candidate")
            self.assertIn("does not prove", report["preliminary_feasibility"]["summary"])

    def test_case_insensitive_extension_inventory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "MODEL.DFF").write_bytes(b"x")
            report = analyze(root)
            self.assertEqual(report["summary"]["extensions"][".dff"], 1)
            self.assertEqual(report["clues"]["common_asset_formats"][0]["clue"], ".dff")


if __name__ == "__main__":
    unittest.main()
