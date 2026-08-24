from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biofotonica" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "biofotonica" / "unit-05.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiofotonicaUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biofotonica")
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "tasa de fluencia",
            "dosimetría explícita",
            "dosimetría implícita",
            "fotoblanqueo",
            "bioheat de pennes",
            "integral de arrhenius",
        ):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_separates_dose_layers(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "potencia radiante",
            "irradiancia",
            "exposición radiante",
            "fotosensibilizador",
            "oxígeno singlete",
            "perfusión",
            "clasificación de producto",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no debe usarse como sinónimo", theory)
        self.assertIn("no debe copiarse como dosis terapéutica", theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("E_e=\\frac{P}{A}", equations)
        self.assertIn("H_e=\\int_0^t E_e(\\tau)\\,d\\tau", equations)
        self.assertIn("q_{abs}=\\mu_a\\,\\phi", equations)
        self.assertTrue(any("partial T" in equation for equation in equations))
        self.assertTrue(any("Omega(t)" in equation for equation in equations))

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 9)
        self.assertGreaterEqual(len(activity["problems"]), 14)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 13)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("exclusivamente", text)
        self.assertIn("no ilumines personas", text)
        self.assertIn("límite ficticio", text)
        self.assertIn("no prescribe", text)

    def test_learning_support_is_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "irradiancia",
            "exposición radiante",
            "tasa de fluencia",
            "dosimetría explícita",
            "bioheat de pennes",
            "trazabilidad metrológica",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_cover_dosimetry_safety(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://pubmed.ncbi.nlm.nih.gov/39815459/",
            "https://pubmed.ncbi.nlm.nih.gov/23927297/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC12715725/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC3930104/",
            "https://webstore.iec.ch/en/publication/3587",
            "https://www.icnirp.org/cms/upload/publications/ICNIRPLaser180gdl_2013.pdf",
        ):
            self.assertIn(url, urls)

    def test_safety_and_clinical_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no requieren hardware", notice)
        self.assertIn("no para prescribir potencia", notice)
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("conformidad regulatoria", notice)
        self.assertIn("sin convertir cálculos sintéticos en prescripciones", purpose)


if __name__ == "__main__":
    unittest.main()
