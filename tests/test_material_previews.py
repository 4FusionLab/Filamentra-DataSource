"""Tests for deterministic catalog specimen previews."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from generate_material_previews import IMAGE_SIZE, make_thumbnail, numeric_color, prepare_specimen, preview_path


class MaterialPreviewTests(unittest.TestCase):
    def test_source_priority(self):
        self.assertEqual(numeric_color({"hex": "#334455"}), "#334455")
        self.assertEqual(numeric_color({"hex": "#334455", "measured_sample": {"hex": "#445566"}}), "#445566")
        self.assertEqual(numeric_color({"rgba_swatches": ["#ABCDEFff"]}), "#ABCDEF")
        self.assertIsNone(numeric_color({"name": "Crimson"}))
        self.assertIsNone(numeric_color({"color_mode": "multicolor", "hex": "#334455"}))
        self.assertIsNone(numeric_color({"color_mode": "gradient", "rgba_swatches": ["#445566FF"]}))
        self.assertIsNone(numeric_color({"rgba_swatches": ["#00112200"]}))
        self.assertIsNone(numeric_color({"rgba_swatches": ["#112233FF", "#334455FF"]}))

    def test_safe_paths(self):
        self.assertEqual(preview_path("bambu-lab/pla-matte", "ash-gray"),
                         "assets/material-previews/bambu-lab/pla-matte/ash-gray.webp")
        with self.assertRaises(ValueError):
            preview_path("../outside", "sample")
        with self.assertRaises(ValueError):
            preview_path("bambu-lab/pla-matte", "../../escape")

    def test_colored_specimen(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            normal, rough = root / "normal.png", root / "rough.png"
            Image.new("RGB", (64, 64), (128, 128, 255)).save(normal)
            Image.new("L", (64, 64), 180).save(rough)
            prepared = prepare_specimen(normal, rough)
            red = make_thumbnail("#B73B37", prepared)
            blue = make_thumbnail("#3976B6", prepared)
            self.assertEqual(red.size, IMAGE_SIZE)
            self.assertNotEqual(red.tobytes(), blue.tobytes())
            self.assertGreater(np.asarray(red).std(), 10)


if __name__ == "__main__":
    unittest.main()
