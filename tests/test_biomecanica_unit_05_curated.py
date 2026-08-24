from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomecanica" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "biomecanica" / "unit-05.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomecanicaUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomecanica")
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in ("plataforma de fuerza", "semg", "sincronización", "markerless"):
            self.assertIn(concept, text)

    def test_theory_covers_measurement_chain_and_modeling(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        text = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "centro de presión",
            "crosstalk",
            "artefacto de tejido blando",
            "anti-aliasing",
            "normalización",
            "desfase temporal",
            "propagación",
        ):
            self.assertIn(concept, text)
        self.assertIn("no es una lectura directa de fuerza muscular", text)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn(r"x_{COP}=-\frac{M_y}{F_z}", equations)
        self.assertIn(r"x_{RMS}=\sqrt{\frac{1}{N}\sum_{i=1}^{N}x_i^2}", equations)
        self.assertIn(r"n_{lag}=\Delta t\,f_s", equations)
        self.assertIn(r"\delta\mathbf y\approx\mathbf J\,\delta\mathbf x", equations)

    def test_guided_activity_is_scaffolded_synthetic_and_multimodal(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        for concept in ("sintético", "cop", "semg", "sincronización", "resampling", "sensibilidad"):
            self.assertIn(concept, text)
        self.assertIn("no registres personas", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 9)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("plataforma de fuerza", "centro de presión", "semg", "sincronización", "c3d", "propagación de error"):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_directly_verified(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://pubmed.ncbi.nlm.nih.gov/18755590/",
            "https://pubmed.ncbi.nlm.nih.gov/28821242/",
            "https://pubmed.ncbi.nlm.nih.gov/38547715/",
            "https://pubmed.ncbi.nlm.nih.gov/39069427/",
            "https://pubmed.ncbi.nlm.nih.gov/38894476/",
            "https://www.c3d.org/docs/C3D_User_Guide.pdf",
        ):
            self.assertIn(url, urls)

    def test_measurement_inference_and_clinical_boundaries_are_explicit(self) -> None:
        purpose = self.unit["purpose"].casefold()
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("no confundir emg con fuerza muscular", purpose)
        self.assertIn("marcador con posición ósea", purpose)
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no autoriza diagnóstico", notice)
        self.assertIn("datos sintéticos", notice)


if __name__ == "__main__":
    unittest.main()
