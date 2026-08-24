from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomecanica-medios-continuos" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "biomecanica-medios-continuos" / "unit-04.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomecanicaMediosContinuosUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomecanica-medios-continuos")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "relajación de esfuerzo",
            "fluencia",
            "poroelasticidad",
            "poroviscoelasticidad",
            "presión de poro",
            "permeabilidad hidráulica",
            "identificabilidad temporal",
        ):
            self.assertIn(concept, text)

    def test_core_equations_and_mechanisms_are_present(self) -> None:
        equations = {e["latex"] for s in self.unit["theory_sections"] for e in s.get("equations", [])}
        self.assertIn("E(t)=E_{\\infty}+(E_0-E_{\\infty})e^{-t/\\tau}", equations)
        self.assertIn("E(t)=E_{\\infty}+\\sum_{i=1}^{N}E_i e^{-t/\\tau_i}", equations)
        self.assertIn("\\mathbf q=-k\\nabla p", equations)
        self.assertIn("t_c\\sim\\frac{L^2}{H_A k}", equations)
        self.assertIn("\\boldsymbol\\sigma=\\boldsymbol\\sigma'_{s}-p\\mathbf I", equations)

    def test_theory_and_pedagogy_are_substantive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(s["paragraphs"]) >= 4 for s in sections))
        self.assertTrue(all(len(s["key_points"]) >= 4 for s in sections))
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 12)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)

    def test_guided_activity_is_synthetic_and_discriminates_mechanisms(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 6)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 7)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 12)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("curvas sintéticas", text)
        self.assertIn("viscoelasticidad intrínseca", text)
        self.assertIn("poroelasticidad", text)
        self.assertIn("datos no empleados en calibración", text)

    def test_curricular_boundaries_are_explicit(self) -> None:
        purpose = self.unit["purpose"].casefold()
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("el flujo libre y navier–stokes se reservan para u5", purpose)
        self.assertIn("elementos finitos para u6", notice)
        self.assertIn("la elasticidad finita procede de u3", notice)
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no se presentan como diagnóstico", notice)

    def test_sources_are_traceable_and_cover_viscoelasticity_and_biphasic_models(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 12)
        self.assertTrue(all(s.get("verification_status") == "verified_directly_2026-08-24" for s in sources))
        urls = {s["url"] for s in sources}
        for url in (
            "https://pubmed.ncbi.nlm.nih.gov/7382457/",
            "https://pubmed.ncbi.nlm.nih.gov/1921350/",
            "https://pubmed.ncbi.nlm.nih.gov/11601725/",
            "https://pubmed.ncbi.nlm.nih.gov/14618936/",
            "https://pubmed.ncbi.nlm.nih.gov/38621832/",
            "https://pubmed.ncbi.nlm.nih.gov/42013604/",
        ):
            self.assertIn(url, urls)

    def test_examples_keep_observation_model_and_inference_separate(self) -> None:
        text = json.dumps(self.unit["worked_examples"], ensure_ascii=False).casefold()
        self.assertIn("no identifica", text)
        self.assertIn("no dos mecanismos biológicos demostrados", text)
        self.assertIn("débilmente identificada", text)
        self.assertIn("espesores", text)


# Final human-authored validation trigger after synchronized public rendering.
if __name__ == "__main__":
    unittest.main()
