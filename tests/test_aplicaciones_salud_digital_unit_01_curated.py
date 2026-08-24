from __future__ import annotations

import json
import unittest
from pathlib import Path

# Final user-authored trigger after publication metadata synchronization.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "aplicaciones-salud-digital" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "aplicaciones-salud-digital" / "unit-01.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class AplicacionesSaludDigitalUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "aplicaciones-salud-digital")
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("validar técnica y clínicamente → vigilar desempeño", text)
        for concept in ("flujo as-is", "equidad digital", "nasss", "alternativas no digitales"):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_respects_unit_boundary(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "necesidad de salud",
            "problema del sistema",
            "flujo asistencial",
            "traspasos",
            "determinantes",
            "pobreza de datos",
            "merece la pena explorar una intervención digital",
            "propuesta de valor",
        ):
            self.assertIn(concept, theory)
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no diseña interfaces", purpose)
        self.assertIn("no implementa interoperabilidad", purpose)
        self.assertIn("no demuestra eficacia clínica", purpose)

    def test_pedagogy_is_progressive_and_auditable(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertGreaterEqual(sum(len(a.get("problems", [])) for a in activities), 30)
        self.assertTrue(all(len(a.get("instructions", [])) >= 5 for a in activities))
        self.assertTrue(all(len(a.get("deliverables", [])) >= 6 for a in activities))
        self.assertTrue(all(len(a.get("checking_criteria", [])) >= 8 for a in activities))
        titles = " ".join(a["title"] for a in activities).casefold()
        self.assertIn("formular el problema", titles)
        self.assertIn("mapa as-is", titles)
        self.assertIn("equidad", titles)

    def test_examples_glossary_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 4)
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {item["term"].casefold() for item in self.unit["glossary"]}
        for term in (
            "necesidad de salud",
            "flujo as-is",
            "determinante digital de la salud",
            "equidad digital",
            "pertinencia digital",
            "nasss",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_disciplinary(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(s.get("verification_status") == "verified_directly" for s in sources))
        urls = {s["url"] for s in sources}
        for url in (
            "https://www.who.int/publications/i/item/9789240116870",
            "https://www.who.int/publications/i/item/9789240081949",
            "https://www.who.int/publications/i/item/9789240010567",
            "https://www.who.int/publications/i/item/9789241550505",
            "https://pubmed.ncbi.nlm.nih.gov/29092808/",
            "https://pubmed.ncbi.nlm.nih.gov/36525960/",
        ):
            self.assertIn(url, urls)

    def test_editorial_boundary_and_synthetic_safety_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("no constituyen revisión disciplinar externa", notice)
        self.assertIn("datos sintéticos", notice)
        self.assertIn("diseño centrado en personas se desarrolla en u2", notice)
        self.assertIn("interoperabilidad en u4", notice)
        self.assertIn("evaluación clínica/económica en u5", notice)


if __name__ == "__main__":
    unittest.main()
