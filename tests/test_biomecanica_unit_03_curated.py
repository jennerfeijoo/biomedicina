# Final user-authored trigger after public and metadata synchronization.
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomecanica" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "biomecanica" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomecanicaUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomecanica")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_u2_central_equation_are_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertNotIn("\\sum \\mathbf{F}=m\\mathbf{a}", equations)

    def test_theory_covers_musculotendon_mechanics_and_redundancy(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "arquitectura muscular",
            "fuerza-longitud",
            "fuerza-velocidad",
            "brazo de momento",
            "redundancia",
            "co-contracción",
            "optimización estática",
            "fatiga",
        ):
            self.assertIn(concept, theory)

    def test_core_muscle_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("\\tau_m=r_m(q)F_m", equations)
        self.assertIn("\\sum_{m=1}^{n} r_{m,j}(q)F_m=\\tau_j", equations)
        self.assertIn("\\min_{a_1,\\ldots,a_n}\\sum_{m=1}^{n}a_m^p", equations)

    def test_guided_activity_demonstrates_redundancy_with_synthetic_data(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 7)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintético", text)
        self.assertIn("tres distribuciones", text)
        self.assertIn("co-contracción", text)
        self.assertIn("emg", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 18)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 8)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "unidad músculo-tendón",
            "arquitectura muscular",
            "brazo de momento muscular",
            "redundancia muscular",
            "optimización estática",
            "fatiga muscular",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_disciplinary(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://pubmed.ncbi.nlm.nih.gov/2676342/",
            "https://pubmed.ncbi.nlm.nih.gov/11054744/",
            "https://pubmed.ncbi.nlm.nih.gov/23445050/",
            "https://pubmed.ncbi.nlm.nih.gov/18018689/",
            "https://pubmed.ncbi.nlm.nih.gov/23998280/",
            "https://pubmed.ncbi.nlm.nih.gov/23489436/",
            "https://pubmed.ncbi.nlm.nih.gov/17702815/",
        ):
            self.assertIn(url, urls)

    def test_measurement_and_clinical_boundaries_are_explicit(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("emg", text)
        self.assertIn("no es una lectura directa de fuerza", text)
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no autorizan diagnóstico", notice)
        self.assertIn("datos sintéticos", notice)


if __name__ == "__main__":
    unittest.main()
