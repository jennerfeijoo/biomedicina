from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "comunicacion-cientifica" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "comunicacion-cientifica" / "unit-04.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ComunicacionCientificaUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "comunicacion-cientifica")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "codificación visual",
            "barra de error",
            "eje truncado",
            "wcag 2.2",
            "texto alternativo",
            "procedencia",
        ):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_distinct_from_writing_unit(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "tabla",
            "figura",
            "distribución",
            "incertidumbre",
            "doble eje",
            "color",
            "descripción larga",
            "presentación",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no certifica causalidad", theory)

    def test_pedagogy_progressively_removes_support(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        titles = " ".join(activity["title"] for activity in activities).casefold()
        self.assertIn("actividad guiada", titles)
        self.assertIn("apoyo reducido", titles)
        self.assertIn("reto autónomo", titles)
        self.assertGreaterEqual(len(activities[0]["problems"]), 10)
        self.assertGreaterEqual(len(activities[0]["deliverables"]), 6)
        self.assertGreaterEqual(len(activities[0]["checking_criteria"]), 8)
        all_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintético", all_text)
        self.assertIn("no uses datos de pacientes reales", all_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "codificación visual",
            "barra de error",
            "paleta divergente",
            "texto alternativo",
            "descripción larga",
            "procedencia",
        ):
            self.assertIn(term, terms)

    def test_accessibility_is_integrated_not_decorative(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertIn("no debe depender exclusivamente del color", text)
        self.assertIn("imágenes complejas", text)
        self.assertIn("alternativa textual", text)
        self.assertIn("escala de grises", text)

    def test_sources_are_directly_verified(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 6)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/25210732/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/25901488/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/33116149/", urls)
        self.assertIn("https://www.w3.org/WAI/WCAG22/Understanding/use-of-color", urls)
        self.assertIn("https://www.w3.org/WAI/tutorials/images/complex/", urls)

    def test_scope_and_professional_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar humana externa", notice)
        self.assertIn("no autorizan inferencias sobre pacientes individuales", notice)
        self.assertIn("sin confundir claridad visual con validez metodológica", purpose)


if __name__ == "__main__":
    unittest.main()
