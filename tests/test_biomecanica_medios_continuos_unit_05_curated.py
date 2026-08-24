from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomecanica-medios-continuos" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "biomecanica-medios-continuos" / "unit-05.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomecanicaMediosContinuosUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomecanica-medios-continuos")
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_lumped_force_equation_are_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("\\sum \\mathbf{f}=m\\mathbf{a}", text)
        for concept in (
            "navier–stokes",
            "número de reynolds",
            "número de womersley",
            "esfuerzo cortante de pared",
            "shear thinning",
            "interacción fluido-estructura",
            "cuantificación de incertidumbre",
        ):
            self.assertIn(concept, text)

    def test_core_equations_and_scope_are_present(self) -> None:
        equations = {e["latex"] for s in self.unit["theory_sections"] for e in s.get("equations", [])}
        self.assertIn("\\nabla\\cdot\\mathbf u=0", equations)
        self.assertIn("Re=\\frac{\\rho U D}{\\mu}", equations)
        self.assertIn("\\alpha=R\\sqrt{\\frac{\\omega\\rho}{\\mu}}", equations)
        self.assertIn("TAWSS=\\frac{1}{T}\\int_0^T|\\boldsymbol\\tau_w(t)|\\,dt", equations)
        self.assertTrue(any("Carreau" in e["meaning"] for s in self.unit["theory_sections"] for e in s.get("equations", [])))

    def test_theory_and_pedagogy_are_substantive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(s["paragraphs"]) >= 4 for s in sections))
        self.assertTrue(all(len(s["key_points"]) >= 4 for s in sections))
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 12)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)

    def test_guided_activity_is_synthetic_and_auditable(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 6)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 7)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 12)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("geometrías y series sintéticas", text)
        self.assertIn("balance", text)
        self.assertIn("womersley", text)
        self.assertIn("fsi", text)
        self.assertIn("validación", text)

    def test_curricular_and_clinical_boundaries_are_explicit(self) -> None:
        purpose = self.unit["purpose"].casefold()
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("transporte intersticial tipo darcy pertenece a u4", purpose)
        self.assertIn("discretización numérica detallada a u6", purpose)
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no se presentan como diagnóstico", notice)

    def test_sources_cover_hemodynamics_rheology_airway_fsi_and_uq(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 17)
        self.assertTrue(all(s.get("verification_status") == "verified_directly_2026-08-24" for s in sources))
        urls = {s["url"] for s in sources}
        for url in (
            "https://pubmed.ncbi.nlm.nih.gov/13243354/",
            "https://pubmed.ncbi.nlm.nih.gov/31749708/",
            "https://pubmed.ncbi.nlm.nih.gov/37757568/",
            "https://pubmed.ncbi.nlm.nih.gov/32629222/",
            "https://pubmed.ncbi.nlm.nih.gov/42082857/",
            "https://pubmed.ncbi.nlm.nih.gov/32081559/",
            "https://pubmed.ncbi.nlm.nih.gov/33721602/",
        ):
            self.assertIn(url, urls)

    def test_examples_separate_mechanical_result_from_clinical_inference(self) -> None:
        text = json.dumps(self.unit["worked_examples"], ensure_ascii=False).casefold()
        self.assertIn("no constituye predicción clínica", text)
        self.assertIn("no basta para declarar", text)
        self.assertIn("segmentación", text)
        self.assertIn("no como diagnóstico", self.unit["editorial_notice"].casefold())


if __name__ == "__main__":
    unittest.main()
