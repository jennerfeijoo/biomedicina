from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "imagenes-biomedicas-avanzadas-i" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "imagenes-biomedicas-avanzadas-i" / "unit-01.json"
SUBJECT = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "imagenes-biomedicas-avanzadas-i.json"
CATALOG = ROOT / "data" / "catalog_statuses.json"


class ImagenesBiomedicasAvanzadasIUnit01ReleaseStateTests(unittest.TestCase):
    def test_unit_01_is_published_without_closing_remaining_template_debt(self) -> None:
        unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))

        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        detailed = {entry["unit"]: entry for entry in subject["detailed_units"]}
        self.assertEqual(detailed[1]["description"], unit["purpose"])

        specificity = catalog["dimensions"]["specificity"]
        self.assertIn("imagenes-biomedicas-avanzadas-i", specificity["template_detected"])
        self.assertNotIn(
            "imagenes-biomedicas-avanzadas-i",
            specificity["screened_no_known_template_marker"],
        )


if __name__ == "__main__":
    unittest.main()
