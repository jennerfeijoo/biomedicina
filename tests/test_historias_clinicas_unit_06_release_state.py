from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "historias-clinicas-terminologias-estandares" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "historias-clinicas-terminologias-estandares" / "unit-06.json"
SUBJECT = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "historias-clinicas-terminologias-estandares.json"
CATALOG = ROOT / "data" / "catalog_statuses.json"
TEMP_WORKFLOW = ROOT / ".github" / "workflows" / "patch-pr479-coverage.yml"


class HistoriasClinicasUnit06ReleaseStateTests(unittest.TestCase):
    def test_release_state_is_clean_and_published(self) -> None:
        unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))

        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        detailed = {entry["unit"]: entry for entry in subject["detailed_units"]}
        self.assertEqual(detailed[6]["description"], unit["purpose"])

        specificity = catalog["dimensions"]["specificity"]
        self.assertIn(
            "historias-clinicas-terminologias-estandares",
            specificity["screened_no_known_template_marker"],
        )
        self.assertNotIn(
            "historias-clinicas-terminologias-estandares",
            specificity["template_detected"],
        )
        self.assertFalse(TEMP_WORKFLOW.exists())


if __name__ == "__main__":
    unittest.main()
