"""Ensure PR and main-branch catalog validation run for the same inputs.

The workflow is deliberately parsed with stdlib to keep the test independent
of YAML parser dependencies. Only the two trigger path lists are inspected.
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
    def test_pull_requests_and_pushes_validate_identical_inputs(self):
        push, pull_request = trigger_paths("push"), trigger_paths("pull_request")
        self.assertEqual(len(push), len(set(push)), "Duplicate push path")
        self.assertEqual(len(pull_request), len(set(pull_request)), "Duplicate PR path")
        self.assertEqual(
            set(push),
            set(pull_request),
            "Inputs tested on main must also be tested before merging a PR",
        )

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
