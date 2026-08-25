from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "informatica-biomedica" / "units" / "unit-03.json"
SUBJECT = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "informatica-biomedica.json"
PUBLIC = ROOT / "ingenieria-biomedica" / "informatica-biomedica" / "unidades" / "unidad-03.html"


class InformaticaBiomedicaUnit03PublicationTests(unittest.TestCase):
    def test_published_descriptor_matches_canonical_purpose(self) -> None:
        unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {x["unit"]: x for x in subject["detailed_units"]}
        self.assertEqual(detailed[3]["description"], unit["purpose"])

    def test_public_page_is_generated_for_curated_unit(self) -> None:
        html = PUBLIC.read_text(encoding="utf-8").casefold()
        for phrase in (
            "interoperabilidad y terminologías",
            "fhir r5",
            "dicomweb",
            "snomed ct",
            "loinc",
            "ucum",
        ):
            self.assertIn(phrase, html)


if __name__ == "__main__":
    unittest.main()
