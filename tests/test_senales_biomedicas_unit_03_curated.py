from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "senales-biomedicas" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "senales-biomedicas" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class SenalesBiomedicasUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "senales-biomedicas")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed_and_scope_is_temporal(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "punto fiducial",
            "ventana de tolerancia",
            "error temporal",
            "sdnn",
            "rmssd",
            "prv",
            "onset semg",
        ):
            self.assertIn(concept, text)
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for frequency_domain_concept in ("psd", "espectrograma", "coherencia"):
            self.assertNotIn(frequency_domain_concept, objectives)

    def test_theory_is_substantive_and_multimodal(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "pan y tompkins",
            "delinear",
            "intervalos nn",
            "variabilidad del pulso",
            "fiducial ppg",
            "onset",
            "potenciales relacionados con eventos",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no debe presentarse como sustituto universal de hrv", theory)

    def test_core_temporal_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        expected = {
            "\\mathrm{Se}=\\frac{TP}{TP+FN}",
            "\\mathrm{PPV}=\\frac{TP}{TP+FP}",
            "I_i=t_{i+1}-t_i",
            "\\Delta t=\\frac{1}{f_s}",
            "SDNN=\\sqrt{\\frac{1}{N-1}\\sum_{i=1}^{N}(NN_i-\\overline{NN})^2}",
            "RMSSD=\\sqrt{\\frac{1}{N-1}\\sum_{i=1}^{N-1}(NN_{i+1}-NN_i)^2}",
        }
        self.assertTrue(expected.issubset(equations))

    def test_guided_activities_are_progressive_and_safe(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertTrue(all(len(item["instructions"]) >= 5 for item in activities))
        self.assertTrue(all(len(item["problems"]) >= 10 for item in activities))
        self.assertTrue(all(len(item["checking_criteria"]) >= 6 for item in activities))
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("verdad conocida", activity_text)
        self.assertIn("physionet", activity_text)
        self.assertIn("hrv y prv", activity_text)
        self.assertIn("no se usa la métrica como evidencia de validez clínica", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "evento",
            "punto fiducial",
            "intervalo rr",
            "intervalo nn",
            "hrv",
            "prv",
            "sdnn",
            "rmssd",
            "onset semg",
        ):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_directly_verified(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        expected = {
            "https://pubmed.ncbi.nlm.nih.gov/3997178/",
            "https://pubmed.ncbi.nlm.nih.gov/15072211/",
            "https://pubmed.ncbi.nlm.nih.gov/8737210/",
            "https://pubmed.ncbi.nlm.nih.gov/38873876/",
            "https://pubmed.ncbi.nlm.nih.gov/35300400/",
            "https://pubmed.ncbi.nlm.nih.gov/32498055/",
            "https://pubmed.ncbi.nlm.nih.gov/37872633/",
            "https://pubmed.ncbi.nlm.nih.gov/23216521/",
            "https://physionet.org/about/database/",
        }
        self.assertTrue(expected.issubset(urls))

    def test_hrv_prv_and_clinical_boundaries_are_explicit(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("no son intercambiables de forma universal", text)
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("validación clínica", notice)
        self.assertIn("no requieren ni autorizan conectar sensores a personas", notice)
        self.assertIn("no demuestra que una métrica temporal identifique enfermedad", text)


if __name__ == "__main__":
    unittest.main()
