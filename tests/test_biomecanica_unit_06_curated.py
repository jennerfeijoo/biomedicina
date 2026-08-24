from __future__ import annotations

import json
import unittest
from pathlib import Path

# Final user-authored trigger after public and catalog synchronization.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomecanica" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "biomecanica" / "unit-06.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomecanicaUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomecanica")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in ("gait deviation index", "gait profile score", "mdc", "rnle", "lifting index", "icf"):
            self.assertIn(concept, text)

    def test_theory_covers_clinical_interpretation_without_overreach(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "error estándar de medida",
            "cambio mínimo detectable",
            "movement analysis profile",
            "compensación",
            "prótesis y órtesis",
            "revised niosh lifting equation",
            "recommended weight limit",
            "análisis de sensibilidad",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no demuestra por sí solo", theory)
        self.assertIn("no significa riesgo individual cero", theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn(r"MDC_{95}=1.96\sqrt{2}\,SEM", equations)
        self.assertIn(r"RWL=LC\cdot HM\cdot VM\cdot DM\cdot AM\cdot FM\cdot CM", equations)
        self.assertIn(r"LI=\frac{L}{RWL}", equations)

    def test_guided_activity_is_scaffolded_synthetic_and_decision_bounded(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        for concept in ("sintético", "mdc", "gps", "rwl", "li", "sensibilidad", "causalidad"):
            self.assertIn(concept, text)
        self.assertIn("no evalúes pacientes", text)
        self.assertIn("no se presenta como efecto causal", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 18)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 8)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "gait deviation index",
            "gait profile score",
            "sem",
            "mdc",
            "icf",
            "recommended weight limit",
            "lifting index",
        ):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_directly_verified(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://pubmed.ncbi.nlm.nih.gov/19013070/",
            "https://pubmed.ncbi.nlm.nih.gov/15705040/",
            "https://pubmed.ncbi.nlm.nih.gov/18565753/",
            "https://pubmed.ncbi.nlm.nih.gov/19632117/",
            "https://pubmed.ncbi.nlm.nih.gov/36563467/",
            "https://www.who.int/classifications/international-classification-of-functioning-disability-and-health",
            "https://www.who.int/publications/i/item/9789241512480",
            "https://www.cdc.gov/niosh/ergonomics/about/rnle.html",
        ):
            self.assertIn(url, urls)

    def test_clinical_device_and_occupational_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no autorizan diagnóstico", notice)
        self.assertIn("prescripción de tratamiento", notice)
        self.assertIn("selección o ajuste de prótesis/órtesis", notice)
        self.assertIn("aptitud laboral", notice)
        self.assertIn("sin convertir una desviación biomecánica en diagnóstico", purpose)
        self.assertIn("efecto causal", purpose)


if __name__ == "__main__":
    unittest.main()
