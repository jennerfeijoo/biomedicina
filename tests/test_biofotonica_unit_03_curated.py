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

    def test_generic_template_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "ecuación de transporte radiativo",
            "problema directo",
            "problema inverso",
            "identificabilidad",
            "inverse adding-doubling",
            "sfdi",
        ):
            self.assertIn(concept, text)

    def test_theory_covers_forward_inverse_and_measurement_domains(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "radiancia",
            "ecuación de difusión",
            "cw",
            "dominio de frecuencia",
            "dominio temporal",
            "jacobiano",
            "regularización",
            "integrating sphere",
            "fantoma",
        ):
            self.assertIn(concept, theory)
        self.assertIn("un buen ajuste no garantiza", json.dumps(self.unit, ensure_ascii=False).casefold())

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        for equation in (
            "D=\\frac{1}{3(\\mu_a+\\mu_s')}",
            "-\\nabla\\cdot(D\\nabla\\Phi)+\\mu_a\\Phi=S",
            "\\mu_{eff}=\\sqrt{\\frac{\\mu_a}{D}}=\\sqrt{3\\mu_a(\\mu_a+\\mu_s')}",
            "J_{ij}=\\frac{\\partial F_i}{\\partial\\theta_j}",
            "r=y-F(\\hat{\\theta})",
        ):
            self.assertIn(equation, equations)
        self.assertTrue(any("argmin" in equation for equation in equations))

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 8)
        self.assertGreaterEqual(len(activity["problems"]), 14)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintétic", text)
        self.assertIn("no ilumines personas", text)
        self.assertIn("jacobiano", text)
        self.assertIn("identificabilidad", text)
        self.assertIn("cw", text)
        self.assertIn("sfdi", text)

    def test_learning_support_is_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "ecuación de transporte radiativo (rte)",
            "problema inverso",
            "identificabilidad",
            "inverse adding-doubling (iad)",
            "fantoma óptico",
            "tabla de búsqueda (lut)",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_methodological(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC9841994/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC11563346/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC12022801/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC6995958/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC7008504/",
            "https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917965",
        ):
            self.assertIn(url, urls)

    def test_scope_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no requiere hardware", notice)
        self.assertIn("no constituyen diagnóstico", notice)
        self.assertIn("validación clínica", notice)
        self.assertIn("problema inverso", purpose)
        self.assertIn("sin confundir", purpose)


if __name__ == "__main__":
    unittest.main()
