# Final user-authored trigger after publication synchronization.
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "fundamentos-biomecanica" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "fundamentos-biomecanica" / "unit-01.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class FundamentosBiomecanicaUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "fundamentos-biomecanica")
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in ("diagrama de cuerpo libre", "brazo de momento", "equilibrio traslacional", "equilibrio rotacional"):
            self.assertIn(concept, text)

    def test_scope_remains_introductory_and_static(self) -> None:
        theory = " ".join(p for section in self.unit["theory_sections"] for p in section["paragraphs"]).casefold()
        self.assertIn("cuasiestático", theory)
        self.assertIn("u2", theory)
        self.assertIn("u3", theory)
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("\\sum \\mathbf F=\\mathbf 0", equations)
        self.assertIn("\\sum \\mathbf M_O=\\mathbf 0", equations)
        self.assertIn("\\mathbf M_O=\\mathbf r_{O\\to P}\\times\\mathbf F", equations)
        self.assertNotIn("\\sum \\mathbf F=m\\mathbf a", equations)

    def test_theory_is_substantive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        word_count = sum(len(paragraph.split()) for section in sections for paragraph in section["paragraphs"])
        self.assertGreaterEqual(word_count, 1200)

    def test_pedagogy_is_progressive_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertGreaterEqual(len(activities), 3)
        first = activities[0]
        self.assertGreaterEqual(len(first["instructions"]), 5)
        self.assertGreaterEqual(len(first["problems"]), 10)
        self.assertGreaterEqual(len(first["deliverables"]), 6)
        self.assertGreaterEqual(len(first["checking_criteria"]), 10)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintético", activity_text)
        self.assertIn("no grabes personas", activity_text)
        self.assertIn("transferencia", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 18)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 4)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 8)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("vector", "diagrama de cuerpo libre", "momento de una fuerza", "brazo de momento", "cuasiestático"):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_directly_verified(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/31791632/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/11934426/", urls)
        self.assertIn("https://www.isbweb.org/activities/standards", urls)
        self.assertIn("https://openstax.org/books/university-physics-volume-1/pages/12-1-conditions-for-static-equilibrium", urls)
        self.assertIn("https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-4-two-classes-si-units-and-si-prefixes", urls)

    def test_editorial_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("diagnóstico", notice)
        self.assertIn("prescripción", notice)
        self.assertIn("equilibrio estático", purpose)


if __name__ == "__main__":
    unittest.main()
