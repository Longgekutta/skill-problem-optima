#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import os
import re
import subprocess
import sys
from pathlib import Path


class TestSkillProblemOptimaContract(unittest.TestCase):
    def setUp(self):
        self.skill_dir = Path(__file__).resolve().parent.parent
        self.skill_file = self.skill_dir / "SKILL.md"

    def test_skill_file_exists_and_valid_frontmatter(self):
        self.assertTrue(self.skill_file.exists(), "SKILL.md must exist in skill root")
        content = self.skill_file.read_text(encoding="utf-8")

        # Verify YAML frontmatter
        self.assertTrue(content.startswith("---"), "SKILL.md must start with YAML frontmatter delimiter '---'")
        m = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        self.assertIsNotNone(m, "SKILL.md must contain enclosing YAML frontmatter '---'")

        frontmatter = m.group(1)
        self.assertIn("name: skill-problem-optima", frontmatter)
        self.assertIn("description:", frontmatter)

    def test_skill_contains_sop_and_modes(self):
        content = self.skill_file.read_text(encoding="utf-8")
        self.assertIn("四步标准作业程序", content, "SKILL.md must outline the 4-step SOP")
        self.assertIn("Dogfood", content, "SKILL.md must include Mode A (Dogfood session audit)")
        self.assertIn("Audit", content, "SKILL.md must include Mode B (Static code audit)")
        self.assertIn("Judge", content, "SKILL.md must include Mode C (Final mutation judge)")
        self.assertIn("32 类病理张量", content, "SKILL.md must document 32-class pathology tensor")

    def test_referenced_tool_resolution(self):
        # Locate tool-problem-optima
        tool_dir = self.skill_dir.parent / "tool-problem-optima"
        if not tool_dir.exists():
            tool_dir = Path("D:/github/tool-problem-optima")
        self.assertTrue(tool_dir.exists(), f"Underlying tool-problem-optima must exist at {tool_dir}")
        self.assertTrue((tool_dir / "main.py").exists(), "tool-problem-optima/main.py must exist")

    def test_underlying_tool_invocation(self):
        tool_dir = self.skill_dir.parent / "tool-problem-optima"
        if not tool_dir.exists():
            tool_dir = Path("D:/github/tool-problem-optima")

        main_script = tool_dir / "main.py"
        cmd = [sys.executable, str(main_script), "health"]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        self.assertEqual(res.returncode, 0, f"tool health check failed: {res.stderr}")
        self.assertIn("HEALTH", res.stdout)


if __name__ == "__main__":
    unittest.main()
