from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "fisiologia-sistemas" / "units" / "unit-02.json"
SUBJECT = ROOT / "data" / "subjects" / "biologicas-medicas" / "fisiologia-sistemas.json"
PUBLIC_UNIT = ROOT / "biologicas-medicas" / "fisiologia-sistemas" / "unidades" / "unidad-02.html"
GENERIC = "Concepto de la unidad que debe definirse mediante entidades observables"


class FisiologiaSistemasUnit02PublicationTests(unittest.TestCase):
    def test_descriptor_and_public_page_follow_canonical_unit(self) -> None:
        unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        published = PUBLIC_UNIT.read_text(encoding="utf-8")

        descriptor = next(item for item in subject["detailed_units"] if item["unit"] == 2)
        self.assertEqual(descriptor["title"], unit["title"])
        self.assertEqual(descriptor["description"], unit["purpose"])
        self.assertIn("Comprender la integración neuroendocrina como un sistema dinámico", published)
        self.assertIn("frecuencia de muestreo", published.casefold())
        self.assertIn("Cortisol no es sinónimo universal de estrés", published)
        self.assertNotIn(GENERIC, published)


if __name__ == "__main__":
    unittest.main()
