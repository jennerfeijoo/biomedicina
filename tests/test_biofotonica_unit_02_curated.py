from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biofotonica" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "biofotonica" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiofotonicaUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biofotonica")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "responsividad espectral",
            "eficiencia cuántica",
            "shot noise",
            "amplificador transimpedancia",
            "potencia equivalente de ruido",
        ):
            self.assertIn(concept, text)

    def test_theory_covers_source_detector_chain(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "láser",
            "led",
            "sld",
            "fotodiodo",
            "corriente oscura",
            "ruido térmico",
            "ruido 1/f",
            "saturación",
            "calibración",
        ):
            self.assertIn(concept, theory)
        self.assertIn("sensibilidad instrumental no es sensibilidad clínica", theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        for equation in (
            "I_{ph}=\\mathcal{R}(\\lambda)P_{opt}",
            "\\eta=\\frac{\\mathcal{R}(\\lambda)hc}{q\\lambda}",
            "i_{shot,rms}=\\sqrt{2qIB}",
            "V_{out}\\approx-I_{in}R_f",
            "\\mathrm{NEP}=\\frac{i_n}{\\mathcal{R}(\\lambda)}",
            "\\mathrm{SNR}=\\frac{I_{signal}}{i_{noise,rms}}",
        ):
            self.assertIn(equation, equations)

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 8)
        self.assertGreaterEqual(len(activity["problems"]), 14)
        self.assertGreaterEqual(len(activity["deliverables"]), 7)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintétic", text)
        self.assertIn("no ilumines personas", text)
        self.assertIn("saturación", text)
        self.assertIn("sensibilidad", text)

    def test_learning_support_is_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "responsividad espectral",
            "eficiencia cuántica",
            "tia",
            "nep",
            "detectividad específica",
            "rango dinámico",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_disciplinary(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://www.nist.gov/programs-projects/spectral-responsivity-measurement",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC9599212/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC2596884/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC5330584/",
            "https://www.fda.gov/media/110120/download",
        ):
            self.assertIn(url, urls)

    def test_scope_and_safety_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("evaluación de exposición", notice)
        self.assertIn("validación diagnóstica o terapéutica", notice)
        self.assertIn("no ilumines personas", notice)
        self.assertIn("sensibilidad instrumental", purpose)


if __name__ == "__main__":
    unittest.main()
