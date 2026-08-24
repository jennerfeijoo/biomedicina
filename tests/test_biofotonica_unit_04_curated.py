from __future__ import annotations

import json
import unittest
from pathlib import Path

# Final user-authored validation trigger after JSON syntax repair.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biofotonica" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "biofotonica" / "unit-04.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiofotonicaUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biofotonica")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed_and_modalities_are_distinct(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "rendimiento cuántico",
            "pinhole",
            "desplazamiento raman",
            "interferometría de baja coherencia",
            "a-scan",
            "speckle",
        ):
            self.assertIn(concept, text)
        self.assertIn("fluorescencia puede emplear fluoróforos endógenos o etiquetas exógenas", text)

    def test_theory_is_substantive_and_quantitative(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "fotoblanqueo",
            "apertura numérica",
            "calibración de número de onda",
            "corrección de intensidad",
            "resolución axial",
            "resolución lateral",
            "roll-off",
        ):
            self.assertIn(concept, theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("\\Phi=\\frac{N_{emitidos}}{N_{absorbidos}}", equations)
        self.assertIn("\\tau=\\frac{1}{k_r+k_{nr}}", equations)
        self.assertIn("R_{lat}\\approx\\frac{0.4\\lambda}{NA}", equations)
        self.assertIn("R_{ax}\\approx\\frac{1.4n\\lambda}{NA^2}", equations)
        self.assertTrue(any("Delta\\tilde" in equation or "\\Delta\\tilde" in equation for equation in equations))
        self.assertTrue(any("delta z_{air}" in equation or "\\delta z_{air}" in equation for equation in equations))

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 8)
        self.assertGreaterEqual(len(activity["problems"]), 14)
        self.assertGreaterEqual(len(activity["deliverables"]), 9)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 12)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("exclusivamente", text)
        self.assertIn("no ilumines personas", text)
        self.assertIn("fotoblanqueo", text)
        self.assertIn("cm⁻¹", text)
        self.assertIn("a-scan", text)

    def test_learning_support_is_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 30)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "fluorescencia",
            "función de dispersión de punto (psf)",
            "desplazamiento raman",
            "oct",
            "a-scan",
            "roll-off de sensibilidad",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_cover_metrology(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC6961134/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC3000600/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC11340246/",
            "https://pubmed.ncbi.nlm.nih.gov/1957169/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC9901537/",
            "https://www.nist.gov/publications/standard-guide-fluorescence-instrument-calibration-and-validation",
        ):
            self.assertIn(url, urls)

    def test_scope_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no requieren hardware", notice)
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("validación clínica", notice)
        self.assertIn("evaluación de seguridad óptica", notice)
        self.assertIn("sin confundir", purpose)
        self.assertIn("diagnóstico clínico", purpose)


if __name__ == "__main__":
    unittest.main()
