from __future__ import annotations

import json
import unittest
from pathlib import Path

# Final user-authored gate trigger after U5 publication synchronization.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "laboratorio-biomecanica" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "laboratorio-biomecanica" / "unit-05.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class LaboratorioBiomecanicaUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_identity_and_editorial_state(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "laboratorio-biomecanica")
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["slug"], "dinamica-inversa")
        self.assertEqual(self.unit["status"], "review")

    def test_generic_and_wrong_imaging_template_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("asignación de píxeles o vóxeles", self.text)
        self.assertIn("modelo segmentario", self.text)
        self.assertIn("newton-euler", self.text)
        self.assertIn("dinámica inversa", self.text)

    def test_theory_covers_inverse_dynamics_pipeline(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "cargas externas",
            "parámetros inerciales",
            "diagrama de cuerpo libre",
            "distal",
            "perspectiva interna",
            "filtrado",
            "residual",
            "momento articular neto",
        ):
            self.assertIn(concept, theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("\\sum \\mathbf F_{ext}=m\\mathbf a_{COM}", equations)
        self.assertIn("\\mathbf M_O=(\\mathbf r_P-\\mathbf r_O)\\times\\mathbf F+\\mathbf M_P", equations)
        self.assertIn("\\Delta M\\approx F\\,\\Delta d_{\\perp}", equations)

    def test_examples_and_guided_activity_are_substantive_and_synthetic(self) -> None:
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 6)
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 8)
        self.assertGreaterEqual(len(activity["problems"]), 14)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 12)
        activity_text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintético", activity_text)
        self.assertIn("no registres participantes", activity_text)
        self.assertIn("cop", activity_text)
        self.assertIn("semg", activity_text)

    def test_glossary_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 16)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 12)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "dinámica inversa",
            "fuerza intersegmentaria",
            "momento intersegmentario",
            "momento articular neto",
            "parámetro inercial segmentario",
            "residual",
            "consistencia dinámica",
        ):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_methodologically_relevant(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://pubmed.ncbi.nlm.nih.gov/31791632/",
            "https://pubmed.ncbi.nlm.nih.gov/28821242/",
            "https://pubmed.ncbi.nlm.nih.gov/17889542/",
            "https://pubmed.ncbi.nlm.nih.gov/21727008/",
            "https://isbweb.org/activities/standards",
            "https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53090079",
        ):
            self.assertIn(url, urls)

    def test_inference_boundary_is_explicit(self) -> None:
        purpose = self.unit["purpose"].casefold()
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("no identifica fuerzas musculares individuales", purpose)
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("sin resolver fuerzas musculares individuales", notice)
        self.assertIn("u6", notice)


if __name__ == "__main__":
    unittest.main()
