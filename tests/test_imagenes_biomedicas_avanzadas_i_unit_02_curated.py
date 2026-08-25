from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "imagenes-biomedicas-avanzadas-i" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "imagenes-biomedicas-avanzadas-i" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ImagenesBiomedicasAvanzadasIUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["slug"], "mri-avanzada")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn(r"v=\\frac{\\delta y}{\\delta t}", self.text)

    def test_objectives_cover_encoding_sequences_diffusion_and_perfusion(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "espacio k",
            "tr",
            "te",
            "spin echo",
            "gradient echo",
            "epi",
            "s(b)=s0 exp(-b·adc)",
            "t2 shine-through",
            "asl",
            "dsc",
            "dce",
            "metadatos críticos",
        ):
            self.assertIn(phrase, objectives)

    def test_five_substantive_theory_sections(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        for section in sections:
            self.assertGreaterEqual(len(section["paragraphs"]), 6)
            self.assertGreaterEqual(len(section["key_points"]), 6)
            for point in section["key_points"]:
                self.assertGreaterEqual(len(point.split()), 4)
        headings = " ".join(x["heading"] for x in sections).casefold()
        for phrase in ("espacio k", "secuencias", "difusión", "perfusión", "cuantificación reproducible"):
            self.assertIn(phrase, headings)

    def test_k_space_section_teaches_encoding_not_anatomical_mapping(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "señal compleja",
            "frecuencias espaciales",
            "trayectoria",
            "centro de k-space",
            "periferia",
            "zero filling",
            "no vóxeles anatómicos",
        ):
            self.assertIn(phrase, text)
        equations = " ".join(x["latex"] for x in self.unit["theory_sections"][0]["equations"])
        self.assertIn("\\mathbf{k}", equations)
        self.assertIn("\\gamma", equations)

    def test_sequence_section_distinguishes_weighting_from_quantification(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "spin echo",
            "gradient echo",
            "t2*",
            "tr",
            "te",
            "ti",
            "epi",
            "ponderación no equivale a una medición cuantitativa",
        ):
            self.assertIn(phrase, text)

    def test_diffusion_section_enforces_adc_boundaries(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "b-value",
            "apparent diffusion coefficient",
            "t2 shine-through",
            "bvecs",
            "eddy currents",
            "susceptibilidad",
            "partial volume",
            "no es una constante microscópica pura",
        ):
            self.assertIn(phrase, text)
        equations = " ".join(x["latex"] for x in self.unit["theory_sections"][2]["equations"])
        self.assertIn("ADC", equations)
        self.assertIn("e^{-b", equations)

    def test_perfusion_section_keeps_asl_dsc_dce_distinct(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "asl",
            "label/control",
            "post-labeling delay",
            "dsc",
            "r cbv",
            "dce",
            "ktrans",
            "mtt",
            "no producen la misma observación primaria",
        ):
            normalized = text.replace("rcbv", "r cbv")
            self.assertIn(phrase, normalized)

    def test_glossary_is_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 50)
        for term in (
            "espacio k",
            "zero filling",
            "spin echo",
            "gradient echo",
            "epi",
            "b-value",
            "adc",
            "t2 shine-through",
            "asl",
            "dsc",
            "dce",
            "dicom",
            "bids",
            "qiba",
        ):
            self.assertIn(term, glossary)

    def test_guided_activity_requires_multidomain_audit(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 9)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 20)
        joined = " ".join(activity["instructions"] + activity["problems"] + activity["checking_criteria"]).casefold()
        for phrase in (
            "k-space",
            "zero filling",
            "spin-echo",
            "adc",
            "t2 shine-through",
            "asl",
            "dsc",
            "metadatos críticos",
            "utilidad clínica",
        ):
            self.assertIn(phrase, joined)

    def test_common_errors_protect_high_impact_misinterpretations(self) -> None:
        errors = json.dumps(self.unit["common_errors"], ensure_ascii=False).casefold()
        for phrase in (
            "zero filling aumenta la resolución física",
            "dwi brillante",
            "adc como una constante tisular universal",
            "asl, dsc y dce",
            "rcbv como cbv absoluto",
            "correlación alta entre protocolos",
            "reproducibilidad técnica implica validez clínica",
        ):
            self.assertIn(phrase, errors)

    def test_sources_assessment_connections_and_scope(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 15)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no capacita para operar un escáner mri",
            "no recomienda contraste",
            "no interpreta estudios de pacientes",
            "u3 continúa con ultrasonido avanzado",
            "u6 con control de calidad cuantitativo",
        ):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
