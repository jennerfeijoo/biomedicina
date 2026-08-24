from __future__ import annotations

# Final human-authored validation trigger after public and editorial synchronization.

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomecanica-medios-continuos" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "biomecanica-medios-continuos" / "unit-06.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomecanicaMediosContinuosUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomecanica-medios-continuos")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_lumped_force_equation_are_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("\\sum \\mathbf{f}=m\\mathbf{a}", text)
        for concept in (
            "formulación débil",
            "convergencia de malla",
            "verificación de código",
            "calibración",
            "validación",
            "cuantificación de incertidumbre",
            "contexto de uso",
            "credibilidad",
        ):
            self.assertIn(concept, text)

    def test_core_equations_and_scope_are_present(self) -> None:
        equations = {e["latex"] for s in self.unit["theory_sections"] for e in s.get("equations", [])}
        self.assertIn("\\mathbf K\\mathbf u=\\mathbf f", equations)
        self.assertIn("\\mathbf R(\\mathbf u)=\\mathbf f_{ext}-\\mathbf f_{int}(\\mathbf u)=\\mathbf 0", equations)
        self.assertIn("RMSE=\\sqrt{\\frac{1}{n}\\sum_{i=1}^{n}(y_i-\\hat y_i)^2}", equations)
        self.assertTrue(any("forma débil" in e["meaning"].casefold() for s in self.unit["theory_sections"] for e in s.get("equations", [])))

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
        self.assertIn("sintéticos", text)
        self.assertIn("tres mallas", text)
        self.assertIn("calibración", text)
        self.assertIn("validación", text)
        self.assertIn("incertidumbre", text)
        self.assertIn("contexto de uso", text)

    def test_closing_boundaries_are_explicit(self) -> None:
        purpose = self.unit["purpose"].casefold()
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("modelos constitutivos y de flujo de u1–u5", purpose)
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no implica conformidad", notice)
        self.assertIn("no constituye", notice)
        self.assertIn("validación clínica", notice)

    def test_sources_cover_vv_fem_reporting_validation_and_uncertainty(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 15)
        self.assertTrue(all(s.get("verification_status") == "verified_directly_2026-08-24" for s in sources))
        urls = {s["url"] for s in sources}
        for url in (
            "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/assessing-credibility-computational-modeling-and-simulation-medical-device-submissions",
            "https://pubmed.ncbi.nlm.nih.gov/17558646/",
            "https://pubmed.ncbi.nlm.nih.gov/25474098/",
            "https://pubmed.ncbi.nlm.nih.gov/23623312/",
            "https://pubmed.ncbi.nlm.nih.gov/34167708/",
            "https://pubmed.ncbi.nlm.nih.gov/40180526/",
        ):
            self.assertIn(url, urls)

    def test_examples_separate_numerical_evidence_from_physical_validity(self) -> None:
        text = json.dumps(self.unit["worked_examples"], ensure_ascii=False).casefold()
        self.assertIn("no demuestra", text)
        self.assertIn("calibración", text)
        self.assertIn("evidencia predictiva", text)
        self.assertIn("credibilidad requerida", text)


if __name__ == "__main__":
    unittest.main()
