from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "imagenes-biomedicas-avanzadas-i" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "imagenes-biomedicas-avanzadas-i" / "unit-02.json"
DESCRIPTOR = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "imagenes-biomedicas-avanzadas-i.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ImagenesBiomedicasAvanzadasIUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.descriptor = json.loads(DESCRIPTOR.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["slug"], "mri-avanzada")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn(r"cnr=\frac{|\mu_1-\mu_2|}{\sigma_n}", self.text)

    def test_public_descriptor_matches_canonical_purpose(self) -> None:
        published = next(x for x in self.descriptor["detailed_units"] if x["unit"] == 2)
        self.assertEqual(published["description"], self.unit["purpose"])

    def test_objectives_cover_full_mri_chain(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "k-space",
            "spin echo",
            "gradient echo",
            "inversion recovery",
            "epi",
            "parallel imaging",
            "compressed sensing",
            "b-value",
            "adc",
            "asl",
            "dsc",
            "dce",
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
        for phrase in ("k-space", "secuencias", "aceleración", "difusión", "perfusión"):
            self.assertIn(phrase, headings)

    def test_kspace_section_prevents_spatial_misreadings(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "señal compleja",
            "frecuencia espacial",
            "codificación de fase",
            "gradiente de lectura",
            "zero filling",
            "no significa que cada punto de k-space corresponda a una región anatómica concreta",
            "no debe llamar raw k-space a una imagen dicom de magnitud",
        ):
            self.assertIn(phrase, text)
        equations = " ".join(x["latex"] for x in self.unit["theory_sections"][0]["equations"])
        self.assertIn("\\mathbf{k}", equations)
        self.assertIn("e^{-i2\\pi", equations)

    def test_sequence_section_distinguishes_weighting_from_mapping(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "tr",
            "te",
            "ti",
            "flip angle",
            "spin echo",
            "gradient echo",
            "t2*",
            "echo-planar imaging",
            "imagen 'weighted' no debe convertirse automáticamente en un mapa cuantitativo",
            "vendor-specific",
        ):
            self.assertIn(phrase, text)

    def test_acceleration_section_teaches_information_and_prior_tradeoffs(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "partial fourier",
            "zero filling",
            "parallel imaging",
            "sense",
            "grappa",
            "g-factor",
            "compressed sensing",
            "deep learning",
            "data consistency",
            "small features",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no demuestra que el contenido ausente de k-space haya sido recuperado fielmente", text)

    def test_diffusion_section_enforces_adc_metrology_and_model_limits(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "b-value",
            "b-matrix",
            "monoexponencial",
            "noise floor",
            "diffusion tensor imaging",
            "fractional anisotropy",
            "eddy currents",
            "qiba",
            "no una medición directa de tamaño celular",
        ):
            self.assertIn(phrase, text)
        equations = " ".join(x["latex"] for x in self.unit["theory_sections"][3]["equations"])
        self.assertIn("ADC", equations)

    def test_perfusion_section_keeps_modalities_and_parameters_distinct(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in (
            "arterial spin labeling",
            "label/control",
            "post-labeling delay",
            "dynamic susceptibility contrast",
            "relative cerebral blood volume",
            "dynamic contrast-enhanced",
            "ktrans",
            "arterial input function",
            "no es una lectura directa de 'permeabilidad' universal",
            "no deben compararse como una misma escala",
            "dicom enhanced mr",
            "asl context",
            "b-value/direction",
        ):
            self.assertIn(phrase, text)

    def test_glossary_is_disciplinary_and_multimodal_within_mri(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 50)
        for term in (
            "k-space",
            "spin echo",
            "gradient echo",
            "epi",
            "parallel imaging",
            "sense",
            "grappa",
            "compressed sensing",
            "b-value",
            "adc",
            "dti",
            "fractional anisotropy",
            "asl",
            "cbf",
            "dsc",
            "rcbv",
            "dce",
            "ktrans",
            "mr diffusion macro",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)

    def test_guided_activity_requires_synthetic_reconstruction_diffusion_and_perfusion(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)
        joined = " ".join(activity["instructions"] + activity["problems"] + activity["checking_criteria"]).casefold()
        for phrase in (
            "k-space complejo",
            "zero filling",
            "undersampling",
            "adc",
            "noise floor",
            "asl",
            "dsc",
            "dce",
            "ktrans",
            "no inventa sequence details",
        ):
            self.assertIn(phrase, joined)

    def test_common_errors_protect_high_impact_misinterpretations(self) -> None:
        errors = json.dumps(self.unit["common_errors"], ensure_ascii=False).casefold()
        for phrase in (
            "centro de k-space corresponde al centro anatómico",
            "zero filling con adquisición de nuevas frecuencias",
            "t1 map a cualquier imagen t1-weighted",
            "adc como tamaño celular",
            "asl, dsc y dce como tres métodos que entregan la misma perfusión",
            "ktrans simplemente como permeabilidad",
            "inventar parámetros de secuencia",
        ):
            self.assertIn(phrase, errors)

    def test_sources_assessment_connections_and_scope(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 18)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        sources = json.dumps(self.unit["sources"], ensure_ascii=False).casefold()
        for authority in ("nibib", "ncbi", "dicom standards committee", "qiba", "ismrm"):
            self.assertIn(authority, sources)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no opera escáneres",
            "no administra gadolinio",
            "no interpreta estudios clínicos",
            "no establece umbrales de adc",
            "u3 continúa con ultrasonido avanzado",
        ):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
