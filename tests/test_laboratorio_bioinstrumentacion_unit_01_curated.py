from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "laboratorio-bioinstrumentacion" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "laboratorio-bioinstrumentacion" / "unit-01.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class LaboratorioBioinstrumentacionUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "laboratorio-bioinstrumentacion")
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        for concept in (
            "trazabilidad metrológica",
            "calibración",
            "verificación",
            "incertidumbre",
            "bitácora",
            "iec 60601-1",
        ):
            self.assertIn(concept, self.text)

    def test_theory_is_substantive_and_metrologically_correct(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        self.assertIn("propiedad del resultado", theory)
        self.assertIn("tipo a", theory)
        self.assertIn("tipo b", theory)
        self.assertIn("no garantiza aptitud para el propósito", theory)
        equations = {
            equation["latex"]
            for section in sections
            for equation in section.get("equations", [])
        }
        self.assertIn("e = x_{ind}-x_{ref}", equations)
        self.assertIn("u_c(y)\\approx\\sqrt{\\sum_i\\left(c_i u_i\\right)^2}", equations)

    def test_safety_boundary_is_explicit(self) -> None:
        purpose = self.unit["purpose"].casefold()
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("no autorizan conexión a personas", purpose)
        self.assertIn("ni trabajo con red eléctrica", purpose)
        self.assertIn("no autorizan trabajo con red eléctrica", notice)
        self.assertIn("conexión de prototipos a personas", notice)
        self.assertIn("conformidad iec 60601-1", notice)
        self.assertIn("acreditación iso/iec 17025", notice)

    def test_guided_activities_progress_from_scaffold_to_transfer(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertGreaterEqual(len(activities), 3)
        self.assertGreaterEqual(len(activities[0]["problems"]), 8)
        self.assertGreaterEqual(len(activities[1]["problems"]), 12)
        self.assertGreaterEqual(len(activities[1]["deliverables"]), 8)
        self.assertGreaterEqual(len(activities[1]["checking_criteria"]), 8)
        self.assertGreaterEqual(len(activities[2]["tasks"]), 8)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("datos sintético", activity_text)
        self.assertIn("no conectes personas", activity_text)
        self.assertIn("antes–después", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "mensurando",
            "calibración",
            "verificación",
            "ajuste",
            "trazabilidad metrológica",
            "bitácora experimental",
            "aptitud para el propósito",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_authoritative(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://webstore.iec.ch/en/publication/2603",
            "https://www.bipm.org/en/doi/10.59161/jcgm200-2012",
            "https://www.bipm.org/en/doi/10.59161/jcgm100-2008e",
            "https://www.nist.gov/metrology/metrological-traceability",
            "https://www.iso.org/standard/66912.html",
            "https://www.who.int/publications/b/74278",
        ):
            self.assertIn(url, urls)


if __name__ == "__main__":
    unittest.main()
