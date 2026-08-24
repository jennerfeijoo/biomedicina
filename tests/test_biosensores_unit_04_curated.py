from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biosensores" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "biosensores" / "unit-04.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiosensoresUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biosensores")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_fallbacks_are_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("mathrm{snr}", text)
        for concept in ("edc/nhs", "biofouling", "reynolds", "péclet", "tiempo de residencia"):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_keeps_boundaries(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        text = SOURCE.read_text(encoding="utf-8").casefold()
        for boundary in ("u2", "u3", "u5", "u6"):
            self.assertIn(boundary, text)
        for concept in ("orientación", "pasivación", "limitación por transporte", "burbuja", "manejo de muestra"):
            self.assertIn(concept, text)

    def test_core_surface_and_microfluidic_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        expected = {
            "\\Gamma=\\frac{N}{A}",
            "\\mathrm{Re}=\\frac{\\rho U D_h}{\\mu}",
            "\\mathrm{Pe}=\\frac{UL}{D}",
            "t_D\\approx\\frac{L^2}{2D}",
            "Q=U A_c",
            "\\tau=\\frac{V}{Q}",
        }
        self.assertTrue(expected.issubset(equations))
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertIn("no significa mezcla instantánea", text)
        self.assertIn("densidad superficial", text)

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        for phrase in ("datos sintéticos", "no uses muestras humanas", "edc/nhs", "reynolds", "péclet", "u5"):
            self.assertIn(phrase, text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("inmovilización", "edc/nhs", "biofouling", "número de reynolds", "número de péclet", "tiempo de residencia"):
            self.assertIn(term, terms)
        examples = json.dumps(self.unit["worked_examples"], ensure_ascii=False).casefold()
        for result in ("100 s", "re=0.1", "pe=2000", "5 min"):
            self.assertIn(result, examples)

    def test_sources_are_directly_verified_and_disciplinary(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 12)
        self.assertTrue(all(source.get("verification_status") == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        for url in (
            "https://pubmed.ncbi.nlm.nih.gov/21951558/",
            "https://pubmed.ncbi.nlm.nih.gov/21264402/",
            "https://pubmed.ncbi.nlm.nih.gov/23337971/",
            "https://pubmed.ncbi.nlm.nih.gov/38361136/",
            "https://pubmed.ncbi.nlm.nih.gov/25841121/",
            "https://pubmed.ncbi.nlm.nih.gov/32515583/",
        ):
            self.assertIn(url, urls)

    def test_scope_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("validación analítica o clínica", notice)
        self.assertIn("validación analítica", purpose)
        self.assertIn("regulatoria", purpose)


if __name__ == "__main__":
    unittest.main()
