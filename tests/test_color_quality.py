"""Offline checks for source-backed visual color arithmetic and provenance.

Run after installing jsonschema: python -m unittest discover -s tests -v
"""
import math
import unittest

from tools.validate_catalog import lab_from_srgb


class CielabConversionTests(unittest.TestCase):
    def test_black_white_reference(self):
        black = lab_from_srgb("#000000")
        white = lab_from_srgb("#FFFFFF")
        self.assertAlmostEqual(black[0], 0.0, places=4)
        self.assertAlmostEqual(white[0], 100.0, places=3)
        self.assertLess(math.dist(black, [0.0, 0.0, 0.0]), 0.01)
        self.assertLess(abs(white[1]), 0.01)
        self.assertLess(abs(white[2]), 0.01)

    def test_actual_bambu_lab_print_measurement(self):
        measured = lab_from_srgb("#424344")
        documented = [28.47, -0.23, -0.70]
        self.assertLess(math.dist(measured, documented), 2.5)

    def test_actual_creality_hyper_pla_measurement(self):
        measured = lab_from_srgb("#C63D44")
        documented = [46.62, 54.76, 27.17]
        self.assertLess(math.dist(measured, documented), 2.5)

    def test_mistyped_lab_would_be_rejected(self):
        measured = lab_from_srgb("#C63D44")
        erroneous = [80.0, -50.0, 10.0]
        self.assertGreater(math.dist(measured, erroneous), 2.5)


if __name__ == "__main__":
    unittest.main()
