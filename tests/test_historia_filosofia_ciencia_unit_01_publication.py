from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "historia-filosofia-ciencia" / "units" / "unit-01.json"
SUBJECT = ROOT / "data" / "subjects" / "gestion-etica-comunicacion" / "historia-filosofia-ciencia.json"
PAGE = ROOT / "gestion-etica-comunicacion" / "historia-filosofia-ciencia" / "unidades" / "unidad-01.html"


class HistoriaFilosofiaCienciaUnit01PublicationTests(unittest.TestCase):
    def test_descriptor_and_public_page_match_canonical_purpose(self) -> None:
        unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {item["unit"]: item for item in subject["detailed_units"]}
        self.assertEqual(detailed[1]["description"], unit["purpose"])

        page = PAGE.read_text(encoding="utf-8")
        self.assertIn(unit["title"], page)
        self.assertIn(unit["purpose"], page)
        self.assertIn("Lección desarrollada · revisión experta pendiente", page)


if __name__ == "__main__":
    unittest.main()
