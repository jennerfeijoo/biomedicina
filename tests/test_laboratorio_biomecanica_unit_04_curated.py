from __future__ import annotations

import json
import unittest
from pathlib import Path

# Final user-authored validation trigger after publication synchronization and literature audit.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "laboratorio-biomecanica" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "laboratorio-biomecanica" / "unit-04.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class LaboratorioBiomecanicaUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()
        cls.theory = " ".join(
            paragraph
            for section in cls.unit["theory_sections"]
            for paragraph in section["paragraphs"]
        ).casefold()

    def test_source_and_generated_mirror_match(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "laboratorio-biomecanica")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_and_wrong_dynamics_fallback_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("\\sum \\mathbf{f}=m\\mathbf{a}", self.text)
        for concept in (
            "semg",
            "volumen conductor",
            "crosstalk",
            "zona de inervación",
            "cmrr",
            "rms",
            "normalización",
            "sincronización",
        ):
            self.assertIn(concept, self.text)

    def test_theory_is_substantive_and_semg_focused(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        for concept in (
            "señal interferencial",
            "distancia interelectrodo",
            "antialiasing",
            "artefactos de movimiento",
            "envolvente lineal",
            "%mvc",
            "neural drive",
        ):
            self.assertIn(concept, self.theory)
        self.assertIn("no puede concluirse", self.theory)

    def test_core_equations_are_measurement_specific(self) -> None:
        equations = [
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        ]
        joined = " ".join(equations)
        self.assertIn("CMRR_{dB}", joined)
        self.assertIn("RMS=", joined)
        self.assertIn("EMG_{norm}", joined)
        self.assertIn("f_s>2f_{max}", joined)
        self.assertIn("\\Delta V", joined)

    def test_guided_activity_is_synthetic_and_scaffolded(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 6)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 12)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("exclusivamente", text)
        self.assertIn("no uses participantes", text)
        self.assertIn("crosstalk", text)
        self.assertIn("%mvc", text)
        self.assertIn("sincronización", text)

    def test_learning_support_is_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "semg",
            "electrodo bipolar",
            "crosstalk",
            "cmrr",
            "rms",
            "normalización",
            "%mvc",
            "sincronización",
            "neural drive",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_disciplinary(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://isek.org/emg-standards/",
            "https://pubmed.ncbi.nlm.nih.gov/11018445/",
            "https://pubmed.ncbi.nlm.nih.gov/31352156/",
            "https://pubmed.ncbi.nlm.nih.gov/32569878/",
            "https://pubmed.ncbi.nlm.nih.gov/39069427/",
            "https://pubmed.ncbi.nlm.nih.gov/25277737/",
            "https://pubmed.ncbi.nlm.nih.gov/33240204/",
            "https://pubmed.ncbi.nlm.nih.gov/29354060/",
            "https://pubmed.ncbi.nlm.nih.gov/18829347/",
            "https://pubmed.ncbi.nlm.nih.gov/11369267/",
        ):
            self.assertIn(url, urls)

    def test_force_recruitment_and_clinical_boundaries_are_explicit(self) -> None:
        purpose = self.unit["purpose"].casefold()
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("sin interpretar la amplitud semg como medida directa de fuerza muscular", purpose)
        self.assertIn("reclutamiento de unidades motoras", purpose)
        self.assertIn("diagnóstico", purpose)
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no se colocan electrodos", notice)
        self.assertIn("u3 cubre plataformas de fuerza", notice)
        self.assertIn("u5 integrará", notice)
        self.assertIn("u6 abordará", notice)


if __name__ == "__main__":
    unittest.main()
