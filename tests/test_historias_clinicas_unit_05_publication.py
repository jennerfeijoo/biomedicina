from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "historias-clinicas-terminologias-estandares" / "units" / "unit-05.json"
SUBJECT = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "historias-clinicas-terminologias-estandares.json"
PUBLIC = ROOT / "ingenieria-biomedica" / "historias-clinicas-terminologias-estandares" / "unidades" / "unidad-05.html"


class HistoriasClinicasUnit05PublicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        cls.public_html = PUBLIC.read_text(encoding="utf-8")

    def test_published_descriptor_matches_canonical_purpose(self) -> None:
        detailed = {item["unit"]: item for item in self.subject["detailed_units"]}
        self.assertEqual(detailed[5]["description"], self.unit["purpose"])

    def test_public_page_contains_canonical_purpose(self) -> None:
        self.assertIn(self.unit["purpose"], self.public_html)

    def test_publication_preserves_scope_boundary(self) -> None:
        html = self.public_html.casefold()
        for phrase in (
            "datos clínicos sintéticos",
            "no constituye asesoría jurídica",
            "u6",
        ):
            self.assertIn(phrase, html)


if __name__ == "__main__":
    unittest.main()
