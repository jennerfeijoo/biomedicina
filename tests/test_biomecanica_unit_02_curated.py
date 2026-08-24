# Final user-authored trigger after public-site synchronization.
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomecanica" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "biomecanica" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomecanicaUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomecanica")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertIn("newton-euler", text)
        self.assertIn("dinámica inversa", text)

    def test_theory_is_kinetic_and_substantive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "diagrama de cuerpo libre",
            "centro de presión",
            "centro de masa",
            "momento articular",
            "parámetros inerciales",
            "filtrado",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no identifica", theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("\\sum \\mathbf F_{ext}=m\\mathbf a_{COM}", equations)
        self.assertIn("\\mathbf M_O=\\mathbf r_{O\\to P}\\times\\mathbf F", equations)
        self.assertIn("\\Delta M\\approx F\\,\\Delta d_\\perp", equations)

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 10)
        self.assertGreaterEqual(len(activity["deliverables"]), 6)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 8)
        activity_text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintético", activity_text)
        self.assertIn("no grabes personas", activity_text)
        self.assertIn("cop", activity_text)
        self.assertIn("com", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 16)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 8)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "cinética",
            "diagrama de cuerpo libre",
            "centro de presión",
            "momento articular neto",
            "dinámica inversa",
        ):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_include_primary_methodology(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 6)
        verified = [item for item in sources if item.get("verification_status") == "verified_directly"]
        self.assertGreaterEqual(len(verified), 5)
        urls = {item["url"] for item in sources}
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/31791632/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/10213082/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/34283131/", urls)
        self.assertIn("https://www.isbweb.org/activities/standards", urls)

    def test_clinical_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no autoriza diagnóstico", notice)
        self.assertIn("fuerzas musculares individuales", purpose)
        self.assertIn("conclusiones clínicas", purpose)


if __name__ == "__main__":
    unittest.main()
