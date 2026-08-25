import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/historia-filosofia-ciencia/units/unit-06.json"
DESCRIPTOR = ROOT / "data/subjects/gestion-etica-comunicacion/historia-filosofia-ciencia.json"
CATALOG = ROOT / "data/catalog_statuses.json"
SUBJECT_ID = "historia-filosofia-ciencia"


class HistoriaFilosofiaCienciaCourseClosureTests(unittest.TestCase):
    def test_unit_06_purpose_is_published_in_curriculum_descriptor(self) -> None:
        unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        descriptor = json.loads(DESCRIPTOR.read_text(encoding="utf-8"))
        detailed = next((u for u in descriptor.get("detailed_units", []) if u.get("unit") == 6), None)
        self.assertIsNotNone(detailed)
        self.assertEqual(detailed["description"], unit["purpose"])

    def test_subject_is_closed_against_known_template_markers(self) -> None:
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        specificity = catalog.get("dimensions", {}).get("specificity", {})
        self.assertNotIn(SUBJECT_ID, specificity.get("template_detected", []))
        self.assertIn(SUBJECT_ID, specificity.get("screened_no_known_template_marker", []))


if __name__ == "__main__":
    unittest.main()
