from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomateriales" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "biomateriales" / "unit-01.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomaterialesUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomateriales")
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed_and_scope_is_material_selection(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "restricciones",
            "módulo elástico",
            "tenacidad a fractura",
            "biocompatibilidad",
            "análisis de sensibilidad",
            "dispositivo final",
        ):
            self.assertIn(concept, text)

    def test_theory_has_four_disciplinary_sections(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        self.assertGreaterEqual(len(self.unit["learning_objectives"]), 6)

    def test_worked_examples_and_guided_activities_are_progressive(self) -> None:
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 3)
        activities = self.unit["guided_activities"]
        self.assertGreaterEqual(len(activities), 3)
        titles = {activity["title"] for activity in activities}
        self.assertIn("Actividad guiada: preselección reproducible de un biomaterial", titles)
        self.assertIn("Actividad guiada: auditoría de datos de propiedades antes de comparar materiales", titles)
        self.assertIn("Actividad guiada: auditoría de una afirmación de biocompatibilidad", titles)
        primary = activities[0]
        self.assertGreaterEqual(len(primary["instructions"]), 6)
        self.assertGreaterEqual(len(primary["problems"]), 12)
        self.assertGreaterEqual(len(primary["deliverables"]), 7)
        self.assertGreaterEqual(len(primary["checking_criteria"]), 10)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("escenario sintético", activity_text)
        self.assertIn("análisis de sensibilidad", activity_text)
        self.assertIn("preselección", activity_text)
        self.assertIn("datos de propiedades", activity_text)
        self.assertIn("afirmación de biocompatibilidad", activity_text)

    def test_assessment_glossary_errors_and_sources_are_substantive(self) -> None:
        self.assertGreaterEqual(len(self.unit["common_errors"]), 8)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        self.assertGreaterEqual(len(self.unit["glossary"]), 15)
        self.assertGreaterEqual(len(self.unit["sources"]), 8)
        verified = [s for s in self.unit["sources"] if s.get("verification_status") == "verified_directly"]
        self.assertGreaterEqual(len(verified), 8)
        urls = {s["url"] for s in self.unit["sources"]}
        self.assertIn("https://www.nibib.nih.gov/science-education/science-topics/biomaterials", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/18440630/", urls)

    def test_biocompatibility_and_clinical_boundary_are_explicit(self) -> None:
        text = json.dumps(self.unit, ensure_ascii=False).casefold()
        self.assertIn("no debe tratarse como sí/no", text)
        self.assertIn("preselección técnica", text)
        self.assertIn("conformidad regulatoria", text)
        self.assertIn("no uses datos de pacientes", text)


# Final user-authored trigger after three-activity pedagogy synchronization.
if __name__ == "__main__":
    unittest.main()
