from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "imagenes-biomedicas-avanzadas-i" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "imagenes-biomedicas-avanzadas-i" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ImagenesBiomedicasAvanzadasIUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["slug"], "ultrasonido-avanzado")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn(r"cnr=\frac{|\mu_1-\mu_2|}{\sigma_n}", self.text)

    def test_objectives_cover_full_ultrasound_chain(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "pulse-echo",
            "beamforming",
            "delay-and-sum",
            "doppler",
            "prf",
            "nyquist",
            "shear-wave",
            "dicom",
        ):
            self.assertIn(phrase, objectives)

    def test_five_substantive_theory_sections(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        for section in sections:
            self.assertGreaterEqual(len(section["paragraphs"]), 6)
            self.assertGreaterEqual(len(section["key_points"]), 6)
            for point in section["key_points"]:
                self.assertGreaterEqual(len(point.split()), 5)
        headings = " ".join(x["heading"] for x in sections).casefold()
        for phrase in ("beamforming", "b-mode", "doppler", "elastografía", "validación"):
            self.assertIn(phrase, headings)

    def test_beamforming_section_teaches_acoustic_chain_and_array_tradeoffs(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "rf channel data",
            "delay-and-sum",
            "velocidad del sonido",
            "apodización",
            "f-number",
            "grating lobes",
            "sidelobes",
            "rf beamformed",
        ):
            self.assertIn(phrase, text)
        equations = " ".join(x["latex"] for x in self.unit["theory_sections"][0]["equations"])
        self.assertIn("z=", equations)
        self.assertIn("\\lambda", equations)
        self.assertIn("\\sum", equations)

    def test_bmode_section_separates_sampling_resolution_and_artifacts(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "b-mode",
            "point-spread function",
            "pixel spacing",
            "speckle",
            "reverberación",
            "shadowing",
            "plane-wave imaging",
            "dicom",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no la point-spread function", text)

    def test_doppler_section_enforces_angle_sampling_and_modality_limits(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "sample volume",
            "pulse repetition frequency",
            "continuous-wave",
            "prf",
            "nyquist",
            "aliasing",
            "color doppler",
            "power doppler",
            "wall filter",
            "peak systolic velocity",
        ):
            self.assertIn(phrase, text)
        equations = " ".join(x["latex"] for x in self.unit["theory_sections"][2]["equations"])
        self.assertIn("2f_0", equations)
        self.assertIn("\\cos", equations)
        self.assertIn("PRF", equations)

    def test_elastography_section_keeps_speed_strain_and_moduli_distinct(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "strain elastography",
            "shear-wave speed",
            "young's modulus",
            "anisotropía",
            "viscoelasticidad",
            "qiba",
            "wfumb",
            "no son identidades universales",
        ):
            self.assertIn(phrase, text)
        equations = " ".join(x["latex"] for x in self.unit["theory_sections"][3]["equations"])
        self.assertIn("G\\approx", equations)
        self.assertIn("E\\approx3", equations)

    def test_glossary_is_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 55)
        for term in (
            "beamforming",
            "delay-and-sum",
            "rf channel data",
            "b-mode",
            "point-spread function",
            "pw doppler",
            "cw doppler",
            "prf",
            "aliasing doppler",
            "strain elastography",
            "shear-wave speed",
            "shear-wave elastography",
            "young's modulus",
            "thermal index",
            "mechanical index",
            "alara",
            "phantom",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)

    def test_guided_activity_requires_synthetic_multimodal_validation(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)
        joined = " ".join(activity["instructions"] + activity["problems"] + activity["checking_criteria"]).casefold()
        for phrase in (
            "rf channel data",
            "aliasing",
            "shear-wave speed",
            "ground truth",
            "no escanees personas",
            "dicom",
        ):
            self.assertIn(phrase, joined)

    def test_common_errors_protect_high_impact_misinterpretations(self) -> None:
        errors = json.dumps(self.unit["common_errors"], ensure_ascii=False).casefold()
        for phrase in (
            "rojo como arteria",
            "aliasing como inversión real",
            "shear-wave speed y young's modulus",
            "e≈3rho c_s²",
            "parámetros de adquisición ausentes",
            "generalizar un resultado de fantoma",
        ):
            self.assertIn(phrase, errors)

    def test_sources_assessment_connections_and_scope(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 18)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        sources = json.dumps(self.unit["sources"], ensure_ascii=False).casefold()
        for authority in ("nibib", "ncbi", "dicom standards committee", "aium", "food and drug administration", "wfumb", "qiba"):
            self.assertIn(authority, sources)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no escanea personas",
            "no prescribe presets",
            "no diagnostica",
            "no define umbrales clínicos",
            "u4 continúa con imagen nuclear cuantitativa",
        ):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
