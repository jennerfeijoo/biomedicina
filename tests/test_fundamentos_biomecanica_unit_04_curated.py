from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "fundamentos-biomecanica" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "fundamentos-biomecanica" / "unit-04.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class FundamentosBiomecanicaUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "fundamentos-biomecanica")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "esfuerzo",
            "deformación",
            "rigidez",
            "anisotropía",
            "viscoelasticidad",
            "histéresis",
        ):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_tissue_specific(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory_words = sum(
            len(paragraph.split())
            for section in sections
            for paragraph in section["paragraphs"]
        )
        self.assertGreaterEqual(theory_words, 1500)
        theory = " ".join(
            paragraph for section in sections for paragraph in section["paragraphs"]
        ).casefold()
        for tissue in ("hueso", "tendón", "cartílago"):
            self.assertIn(tissue, theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("\\sigma=\\frac{F}{A_0}", equations)
        self.assertIn("\\varepsilon=\\frac{L-L_0}{L_0}=\\frac{\\Delta L}{L_0}", equations)
        self.assertIn("E\\approx\\frac{\\Delta\\sigma}{\\Delta\\varepsilon}", equations)
        self.assertIn("W_{diss}=\\oint \\sigma\\,d\\varepsilon", equations)

    def test_activities_are_progressive_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        first = activities[0]
        self.assertGreaterEqual(len(first["instructions"]), 5)
        self.assertGreaterEqual(len(first["problems"]), 10)
        self.assertGreaterEqual(len(first["checking_criteria"]), 10)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintét", activity_text)
        self.assertIn("fluencia", activity_text)
        self.assertIn("histéresis", activity_text)
        self.assertIn("no se infieren adaptación, daño o lesión clínica", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 4)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 8)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "módulo de young",
            "anisotropía",
            "fluencia",
            "relajación de esfuerzo",
            "material bipásico",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_cover_tissue_mechanics(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/29865872/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/26855747/", urls)
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC8065530/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/38621832/", urls)

    def test_scope_boundary_is_explicit(self) -> None:
        purpose = self.unit["purpose"].casefold()
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("umbrales clínicos", purpose)
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("datos sintéticos", notice)
        self.assertIn("no autorizan definir umbrales de lesión", notice)
        self.assertIn("prescribir cargas", notice)


if __name__ == "__main__":
    unittest.main()
