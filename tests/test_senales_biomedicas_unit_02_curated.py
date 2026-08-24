from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "senales-biomedicas" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "senales-biomedicas" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class SenalesBiomedicasUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "senales-biomedicas")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in ("ringing", "retardo de grupo", "fase cero", "fir", "iir", "padding"):
            self.assertIn(concept, text)

    def test_theory_covers_filter_response_and_distortion(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "deriva de línea base",
            "respuesta al impulso",
            "banda de transición",
            "causalidad",
            "señal cruda",
            "validación clínica",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no existe un 'pipeline de limpieza' universal", theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("y[n]=\\sum_{k=-\\infty}^{\\infty} h[k]x[n-k]", equations)
        self.assertIn("\\tau_g(\\omega)=-\\frac{d\\phi(\\omega)}{d\\omega}", equations)
        self.assertIn("\\mathrm{SNR}_{dB}=10\\log_{10}\\left(\\frac{P_s}{P_n}\\right)", equations)
        self.assertIn("\\mathrm{RMSE}=\\sqrt{\\frac{1}{N}\\sum_{n=1}^{N}(x[n]-\\hat{x}[n])^2}", equations)

    def test_guided_activities_are_progressive_and_safe(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertTrue(all(len(item["instructions"]) >= 5 for item in activities))
        self.assertTrue(all(len(item["problems"]) >= 10 for item in activities))
        self.assertTrue(all(len(item["checking_criteria"]) >= 6 for item in activities))
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("señales sintéticas", activity_text)
        self.assertIn("physionet", activity_text)
        self.assertIn("no conectes sensores a personas", activity_text)
        self.assertIn("verdad conocida", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "deriva de línea base",
            "filtro notch",
            "fir",
            "iir",
            "retardo de grupo",
            "fase cero",
            "ringing",
        ):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_multimodal(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://pubmed.ncbi.nlm.nih.gov/20851409/",
            "https://pubmed.ncbi.nlm.nih.gov/25128257/",
            "https://pubmed.ncbi.nlm.nih.gov/25903295/",
            "https://pubmed.ncbi.nlm.nih.gov/32763743/",
            "https://pubmed.ncbi.nlm.nih.gov/35300400/",
            "https://pubmed.ncbi.nlm.nih.gov/38297978/",
            "https://physionet.org/about/database/",
        ):
            self.assertIn(url, urls)

    def test_editorial_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no requieren ni autorizan conectar sensores", notice)
        self.assertIn("validación clínica", notice)
        self.assertIn("antes de cualquier interpretación clínica", purpose)


if __name__ == "__main__":
    unittest.main()
