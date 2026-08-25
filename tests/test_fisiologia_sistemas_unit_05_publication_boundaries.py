from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "fisiologia-sistemas" / "units" / "unit-05.json"
SUBJECT = ROOT / "data" / "subjects" / "biologicas-medicas" / "fisiologia-sistemas.json"
PUBLIC_UNIT = ROOT / "biologicas-medicas" / "fisiologia-sistemas" / "unidades" / "unidad-05.html"


class FisiologiaSistemasUnit05PublicationBoundaryTests(unittest.TestCase):
    def test_public_u5_preserves_non_diagnostic_boundaries(self) -> None:
        text = PUBLIC_UNIT.read_text(encoding="utf-8").casefold()
        for phrase in (
            "distinguir infección de inflamación estéril",
            "fiebre de hipertermia",
            "evitando usar una citocina o crp como marcador etiológico específico",
            "sin convertir la temperatura corporal en prueba de infección",
            "resolución activa",
            "perfiles exclusivamente sintéticos",
        ):
            self.assertIn(phrase, text)

    def test_published_subject_descriptor_matches_canonical_u5_purpose(self) -> None:
        unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        published = next(item for item in subject["detailed_units"] if item["unit"] == 5)
        self.assertEqual(published["title"], unit["title"])
        self.assertEqual(published["description"], unit["purpose"])
        self.assertIn("resolución activa y reparación tisular", published["description"].casefold())
        self.assertNotIn("integrar señales inmunes, fiebre, reparación para resolver", published["description"].casefold())


if __name__ == "__main__":
    unittest.main()
