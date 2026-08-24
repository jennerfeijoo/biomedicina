from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "ingenieria-tejidos" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "ingenieria-tejidos" / "unit-05.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class IngenieriaTejidosUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "ingenieria-tejidos")
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_wrong_mechanics_equation_are_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("\\sigma=\\frac{f}{a_0}", text)
        for concept in (
            "iso 10993-1:2025",
            "pseudorreplicación",
            "aleatorización",
            "cegamiento",
            "arrive 2.0",
            "nam",
            "peso de evidencia",
        ):
            self.assertIn(concept, text)

    def test_theory_is_preclinical_and_substantive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "seguridad biológica",
            "unidad experimental",
            "control positivo",
            "contexto de uso",
            "reemplazo, reducción y refinamiento",
            "efectos locales",
            "resultados negativos",
            "reproducibilidad",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no está diseñado por sí mismo", theory)
        self.assertIn("no autoriza a concluir restauración funcional completa", theory)

    def test_guided_activities_are_progressive_synthetic_and_reproducible(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("doce registros sintéticos", text)
        self.assertIn("modelo a", text)
        self.assertIn("modelo b", text)
        self.assertIn("modelo c", text)
        self.assertIn("datos c1–c10", text)
        self.assertIn("retira parte de la ayuda", text)
        self.assertIn("sin plantilla", text)
        self.assertIn("u6", text)
        total_items = sum(
            len(activity.get(key, []))
            for activity in activities
            for key in ("instructions", "problems", "tasks", "deliverables", "checking_criteria")
        )
        self.assertGreaterEqual(total_items, 75)

    def test_learning_support_is_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 26)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "biocompatibilidad",
            "unidad experimental",
            "pseudorreplicación",
            "nam",
            "contexto de uso",
            "3r",
            "peso de evidencia",
            "resultado negativo",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_current(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://www.iso.org/standard/10993-1",
            "https://www.iso.org/standard/78866.html",
            "https://www.iso.org/standard/83976.html",
            "https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3000410",
            "https://pubmed.ncbi.nlm.nih.gov/28938849/",
            "https://pubmed.ncbi.nlm.nih.gov/25803622/",
            "https://nc3rs.org.uk/3rs-resources/key-elements-well-designed-experiment",
        ):
            self.assertIn(url, urls)

    def test_curricular_and_safety_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        for boundary in (
            "no se proporcionan protocolos",
            "no se autoriza experimentación",
            "no constituye revisión disciplinar externa",
            "u6",
            "manufactura",
            "regulación",
        ):
            self.assertIn(boundary, notice)
        self.assertIn("sin tratar la biocompatibilidad como propiedad absoluta", purpose)
        self.assertIn("beneficio clínico", purpose)
        self.assertIn("conformidad regulatoria", purpose)


if __name__ == "__main__":
    unittest.main()
