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
from generate_material_previews import (IMAGE_SIZE, make_thumbnail, numeric_color,
                                        prepare_specimen, preview_path, preview_tint,
                                        resolve_appearance, logo_backdrop, hazy_logo_backdrop)


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

    def test_transparent_clear_without_inventing_hex(self):
        clear = {"id": "clear", "rgba_swatches": ["#00000000"], "color_mode": "solid"}
        base = {"surface_type": "transparent", "roughness": 0.20, "transmission": 0.68}
        override = {"transmission": 0.94, "attenuation_distance_mm": 75}
        appearance = resolve_appearance(base, None, override)
        self.assertEqual(appearance["transmission"], 0.94)
        self.assertIsNone(numeric_color(clear))
        self.assertEqual(preview_tint(clear, appearance), "#F6F9F7")
        self.assertIsNone(preview_tint(clear, {"surface_type": "opaque"}))
        with self.assertRaises(ValueError):
            resolve_appearance({"surface_type": "opaque"}, None, {"transmission": 0.5})

    def test_transparency_and_thickness_change_render(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            normal, rough = root / "normal.png", root / "rough.png"
            Image.new("RGB", (64, 64), (128, 128, 255)).save(normal)
            Image.new("L", (64, 64), 190).save(rough)
            surface = prepare_specimen(normal, rough)
            solid = make_thumbnail("#F6F9F7", surface, {"transmission": 0})
            tinted = make_thumbnail("#F6F9F7", surface, {"transmission": 0.40, "haze": 0.80, "attenuation_distance_mm": 7.5})
            clear = make_thumbnail("#F6F9F7", surface, {"transmission": 0.75, "haze": 0.35, "attenuation_distance_mm": 75})
            # The ivory 4F glyph crosses the dark monogram background
            # *behind* the sphere. Increasing transmission must reveal it.
            def glyph_contrast(image):
                region = np.asarray(image, dtype=np.float32)[92:101, 99:128]
                return float(np.ptp(region.mean(axis=2)))
            self.assertGreater(glyph_contrast(clear), glyph_contrast(tinted) + 6)
            self.assertGreater(glyph_contrast(tinted), 0.5)
            self.assertNotEqual(solid.tobytes(), tinted.tobytes())
            self.assertNotEqual(tinted.tobytes(), clear.tobytes())

    def test_haze_blurs_logo_at_equal_transmission(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            normal, rough = root / "normal.png", root / "rough.png"
            Image.new("RGB", (64, 64), (128, 128, 255)).save(normal)
            Image.new("L", (64, 64), 180).save(rough)
            surface = prepare_specimen(normal, rough)
            baseline = {"transmission": 0.70, "attenuation_distance_mm": 30}
            crisp = make_thumbnail("#EAF2ED", surface, {**baseline, "haze": 0})
            hazy = make_thumbnail("#EAF2ED", surface, {**baseline, "haze": 0.90})
            self.assertNotEqual(crisp.tobytes(), hazy.tobytes())
            # Outside the specimen the official logo remains crisp and identical.
            self.assertEqual(crisp.getpixel((8, 8)), hazy.getpixel((8, 8)))
            # Stronger haze reduces high-frequency transmitted reference details.
            def contrast(im):
                return float(np.std(np.asarray(im, dtype=np.float32)[92:101, 99:128]))
            self.assertGreater(contrast(crisp), contrast(hazy))

    def test_haze_schema_version_unchanged(self):
        import json
        for name in ("line.schema.json", "preset.schema.json"):
            schema = json.loads((ROOT / "catalog/schema" / name).read_text(encoding="utf-8"))
            self.assertEqual(schema["properties"]["schema_version"]["const"], 1)
            appearance = schema["$defs"]["appearance"] if name.startswith("line") else schema["properties"]["appearance"]
            self.assertEqual(appearance["properties"]["haze"]["maximum"], 1)

    def test_official_logo_backdrop_has_monogram_not_stripes(self):
        backdrop = logo_backdrop()
        self.assertEqual(backdrop.shape, (IMAGE_SIZE[1], IMAGE_SIZE[0], 3))
        # White 4F stroke next to the midnight-blue background.
        self.assertGreater(float(backdrop[96, 106].mean()), 0.65)
        self.assertLess(float(backdrop[96, 120].mean()), 0.20)

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
