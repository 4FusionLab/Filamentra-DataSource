"""Ensure every push can recover unpublished releases and PRs validate inputs.

The workflow is deliberately parsed with stdlib to avoid external YAML
parser dependencies. PR filters stay narrow, while push is unfiltered.
"""

import ast
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "validate.yml"


def trigger_paths(event):
    contents = WORKFLOW.read_text(encoding="utf-8")
    block = re.search(
        rf"(?m)^  {re.escape(event)}:\n    paths:\n((?:      - .+\n)+)",
        contents,
    )
    if block is None:
        raise AssertionError(f"Missing {event} path filter in {WORKFLOW.name}")
    return [ast.literal_eval(line.strip().removeprefix("- ").strip())
            for line in block.group(1).splitlines()]


class CatalogCITriggerTests(unittest.TestCase):
    def test_push_is_unfiltered_to_recover_missed_releases(self):
        contents = WORKFLOW.read_text(encoding="utf-8")
        self.assertRegex(
            contents, r"(?m)^  push: \{\}(?: #.*)?$",
            "Every push must trigger release recovery, even docs-only pushes",
        )

    def test_pull_request_paths_do_not_have_duplicates(self):
        pull_request = trigger_paths("pull_request")
        self.assertEqual(len(pull_request), len(set(pull_request)), "Duplicate PR path")

    def test_critical_catalog_distribution_inputs_are_covered(self):
        required = {
            "catalog/**",
            "scripts/build_release.py",
            "tools/generate_texture_maps.py",
            "tools/generate_material_previews.py",
            "tools/audit_missing_colors.py",
            "package.json",
            "tests/**",
            ".github/release-paths.txt",
            ".github/workflows/validate.yml",
        }
        self.assertFalse(required - set(trigger_paths("pull_request")))


if __name__ == "__main__":
    unittest.main()
