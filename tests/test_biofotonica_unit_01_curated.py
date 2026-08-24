from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biofotonica" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "biofotonica" / "unit-01.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiofotonicaUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biofotonica")
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in ("coeficiente de absorción", "coeficiente de dispersión reducido", "anisotropía", "monte carlo"):
            self.assertIn(concept, text)

    def test_tissue_optics_theory_is_substantive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "cromóforo",
            "beer-lambert",
            "transporte radiativo",
            "aproximación de difusión",
            "problema inverso",
            "longitud característica",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no es una profundidad máxima", theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("\\mu_s'=\\mu_s(1-g)", equations)
        self.assertIn("D=\\frac{1}{3(\\mu_a+\\mu_s')}", equations)
        self.assertIn("\\mu_{eff}=\\sqrt{3\\mu_a(\\mu_a+\\mu_s')}", equations)
        self.assertIn("\\delta_{diff}=\\frac{1}{\\mu_{eff}}", equations)

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 6)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 6)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 8)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintétic", text)
        self.assertIn("no ilumines personas", text)
        self.assertIn("μs′", json.dumps(activity, ensure_ascii=False))
        self.assertIn("sensibilidad", text)

    def test_learning_support_is_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("anisotropía (g)", "problema inverso", "monte carlo fotónico"):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_disciplinary(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 7)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/23666068/", urls)
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC11166171/", urls)
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC9979671/", urls)

    def test_clinical_and_therapy_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("validación diagnóstica o terapéutica", notice)
        self.assertIn("seguridad", notice)
        self.assertIn("sin convertir", purpose)


if __name__ == "__main__":
    unittest.main()
