from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "aplicaciones-salud-digital" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "aplicaciones-salud-digital" / "unit-05.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class AplicacionesSaludDigitalUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_source_and_generated_mirror_are_exact(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "aplicaciones-salud-digital")
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_inherited_ppv_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("ppv=", self.text)
        self.assertNotIn("valor predictivo positivo", self.text)
        self.assertIn("icer", self.text)
        self.assertIn("re-aim", self.text)

    def test_theory_is_clinical_economic_and_substantive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "eficacia",
            "efectividad",
            "engagement",
            "reach",
            "adoption",
            "equidad",
            "perspectiva",
            "qaly",
            "icer",
            "impacto presupuestario",
            "análisis de sensibilidad",
            "cheers 2022",
        ):
            self.assertIn(concept, theory)

    def test_pedagogy_is_progressive_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertIn("Actividad guiada", activities[0]["title"])
        self.assertIn("apoyo reducido", activities[1]["title"])
        self.assertIn("Reto autónomo", activities[2]["title"])
        for activity in activities:
            self.assertGreaterEqual(len(activity["instructions"]), 5)
            self.assertGreaterEqual(len(activity["problems"]), 10)
            self.assertGreaterEqual(len(activity["deliverables"]), 7)
            self.assertGreaterEqual(len(activity["checking_criteria"]), 8)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintétic", activity_text)
        self.assertIn("no uses historias clínicas", activity_text)

    def test_examples_glossary_errors_and_assessment_are_complete(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 28)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "efectividad",
            "reach",
            "adopción",
            "equidad",
            "qaly",
            "icer",
            "impacto presupuestario",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_authoritative(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        expected = {
            "https://www.who.int/health-topics/health-technology-assessment",
            "https://www.nice.org.uk/process/pmg48/chapter/methods-for-guidance-produced-in-the-nice-healthtech-programme",
            "https://www.bmj.com/content/376/bmj-2021-067975",
            "https://pubmed.ncbi.nlm.nih.gov/22209829/",
            "https://pubmed.ncbi.nlm.nih.gov/10474547/",
            "https://pubmed.ncbi.nlm.nih.gov/20957426/",
        }
        self.assertTrue(expected.issubset(urls))

    def test_curricular_and_decision_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("u4 conserva interoperabilidad", notice)
        self.assertIn("u6 conserva consentimiento", notice)
        self.assertIn("no deben emplearse para decisiones", notice)
        self.assertIn("coste-efectividad universal", purpose)
        self.assertIn("decisión de implementación", purpose)


if __name__ == "__main__":
    unittest.main()
