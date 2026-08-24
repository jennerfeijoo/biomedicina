from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biofotonica" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "biofotonica" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiofotonicaUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biofotonica")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed_and_u1_is_not_repeated(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "problema inverso",
            "identificabilidad",
            "inverse adding-doubling",
            "esfera integradora",
            "sfdi",
            "fantoma óptico",
        ):
            self.assertIn(concept, text)
        self.assertIn("u1 introdujo", text)

    def test_theory_focuses_on_measurement_inversion_and_phantoms(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "modelo directo",
            "regularización",
            "reflectancia total",
            "frecuencia espacial",
            "agente dispersor",
            "estabilidad temporal",
            "sesgo de calibración",
            "reproducibilidad",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no demuestra que la misma inversión sea válida", theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("\\mu_s'=\\mu_s(1-g)", equations)
        self.assertIn("\\mathbf y_{IAD}=\\left[R_{tot},T_{tot},T_{coll}\\right]", equations)
        self.assertIn("I(x)=I_0\\left[1+m\\cos(2\\pi f_x x+\\phi)\\right]", equations)
        self.assertIn("CV=\\frac{s}{\\bar{x}}\\times100\\%", equations)
        self.assertTrue(any("arg\\min" in equation for equation in equations))

    def test_guided_activity_is_scaffolded_synthetic_and_inverse(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 8)
        self.assertGreaterEqual(len(activity["problems"]), 15)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 12)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("datos sintéticos", text)
        self.assertIn("no ilumines personas o animales", text)
        self.assertIn("lut", text)
        self.assertIn("χ²", json.dumps(activity, ensure_ascii=False))
        self.assertIn("cv y sesgo", text)

    def test_learning_support_is_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 6)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 12)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "problema inverso",
            "identificabilidad",
            "inverse adding-doubling",
            "fantoma óptico",
            "error de modelo",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_disciplinary(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://opg.optica.org/ao/abstract.cfm?uri=ao-32-4-559", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/20802704/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/16965130/", urls)
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC6995958/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/35112513/", urls)
        self.assertIn("https://onlinelibrary.wiley.com/doi/full/10.1002/jbio.70261", urls)

    def test_clinical_and_phantom_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no requieren fabricar fantomas", notice)
        self.assertIn("ni iluminar personas o animales", notice)
        self.assertIn("validación independientes", notice)
        self.assertIn("sin repetir la introducción al transporte de u1", purpose)
        self.assertIn("sin convertir resultados de fantomas en afirmaciones clínicas", purpose)


if __name__ == "__main__":
    unittest.main()
