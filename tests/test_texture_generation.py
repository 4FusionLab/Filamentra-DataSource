"""Tests for deterministic, tiled, uncalibrated Filamentra PBR profiles."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from generate_texture_maps import RECIPES, generate_arrays  # noqa: E402


class TextureTests(unittest.TestCase):
    def test_every_preset_has_recipe_and_expected_asset_paths(self):
        paths = list((ROOT / "catalog/presets").glob("*.json"))
        self.assertEqual(set(RECIPES), {p.stem for p in paths})
        self.assertEqual(len(paths), 18)
        for path in paths:
            doc = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(doc["status"], "uncalibrated")
            self.assertEqual(doc["provenance"], "filamentra_estimate")
            texture = doc["appearance"]["textures"]
            self.assertEqual(texture["normal_gl"], f"assets/presets/{path.stem}/normal_gl.png")
            self.assertEqual(texture["roughness"], f"assets/presets/{path.stem}/roughness.png")
            self.assertEqual(texture["tile_width_mm"], 8)
            self.assertEqual(texture["tile_height_mm"], 8)

    def test_deterministic_seamless_and_roughness_consistent(self):
        for ident in ("pla-matte", "pla-silk", "fiber-matte", "pla-wood", "pla-marble"):
            with self.subTest(ident=ident):
                normal, rough = generate_arrays(ident, 0.6, size=128)
                normal2, rough2 = generate_arrays(ident, 0.6, size=128)
                np.testing.assert_array_equal(normal, normal2)
                np.testing.assert_array_equal(rough, rough2)
                self.assertEqual(normal.shape, (128, 128, 3))
                self.assertEqual(rough.shape, (128, 128))
                np.testing.assert_array_equal(normal[0], normal[-1])
                np.testing.assert_array_equal(normal[:, 0], normal[:, -1])
                np.testing.assert_array_equal(rough[0], rough[-1])
                np.testing.assert_array_equal(rough[:, 0], rough[:, -1])
                self.assertLess(abs(float(rough.mean()) / 255 - 0.6), 0.04)

    def test_matte_has_more_microrelief_than_silk(self):
        matte, _ = generate_arrays("pla-matte", 0.86, size=128)
        silk, _ = generate_arrays("pla-silk", 0.22, size=128)
        self.assertGreater(float(matte[..., :2].std()), float(silk[..., :2].std()))


if __name__ == "__main__":
    unittest.main()
