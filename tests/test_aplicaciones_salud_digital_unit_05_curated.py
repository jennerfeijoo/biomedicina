from __future__ import annotations

# Final user-authored CI trigger after publication metadata synchronization.

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

    def test_generic_template_and_unrelated_ppv_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("ppv=", self.text)
        self.assertNotIn("valor predictivo positivo", self.text)

    def test_theory_is_evaluation_specific_and_substantive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "eficacia",
            "efectividad",
            "re-aim",
            "alcance",
            "adopción",
            "equidad",
            "coste incremental",
            "icer",
            "beneficio monetario neto",
            "análisis de sensibilidad",
            "transferibilidad",
            "cheers 2022",
            "nice",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no demuestra", theory)

    def test_core_equations_are_incremental_and_relevant(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("\\Delta E=E_{digital}-E_{comparador}", equations)
        self.assertIn("\\Delta C=C_{digital}-C_{comparador}", equations)
        self.assertIn("ICER=\\frac{\\Delta C}{\\Delta E}", equations)
        self.assertIn("INMB=\\lambda\\Delta E-\\Delta C", equations)
        self.assertIn("Alcance=\\frac{N_{participantes}}{N_{elegibles}}", equations)

    def test_guided_activity_is_complete_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertIn("Actividad guiada", activity["title"])
        self.assertGreaterEqual(len(activity["instructions"]), 6)
        self.assertGreaterEqual(len(activity["problems"]), 10)
        self.assertGreaterEqual(len(activity["deliverables"]), 6)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 8)
        activity_text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintético", activity_text)
        self.assertIn("no uses datos personales", activity_text)
        for concept in ("alcance", "equidad", "icer", "inmb", "sensibilidad"):
            self.assertIn(concept, activity_text)

    def test_examples_glossary_errors_and_assessment_are_complete(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 8)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "efectividad",
            "alcance",
            "adopción",
            "equidad",
            "icer",
            "qaly",
            "análisis de sensibilidad",
            "transferibilidad",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_authoritative(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        expected = {
            "https://pubmed.ncbi.nlm.nih.gov/27745684/",
            "https://pubmed.ncbi.nlm.nih.gov/35132606/",
            "https://pubmed.ncbi.nlm.nih.gov/35031096/",
            "https://pubmed.ncbi.nlm.nih.gov/10474547/",
            "https://doi.org/10.1007/s10488-010-0319-7",
            "https://www.nice.org.uk/about/what-we-do/our-programmes/evidence-standards-framework-for-digital-health-technologies",
            "https://iris.who.int/bitstream/handle/10665/252183/9789241511766-eng.pdf?sequence=1",
        }
        self.assertTrue(expected.issubset(urls))

    def test_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("recomendación de compra", notice)
        self.assertIn("certificación regulatoria", notice)
        self.assertIn("autorización clínica, regulatoria o de compra", purpose)


if __name__ == "__main__":
    unittest.main()
