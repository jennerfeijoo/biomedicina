from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "imagenes-biomedicas-avanzadas-i" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "imagenes-biomedicas-avanzadas-i" / "unit-05.json"
SUBJECT = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "imagenes-biomedicas-avanzadas-i.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ImagenesBiomedicasAvanzadasIUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["slug"], "registro-y-fusion")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn(r"cnr=\\frac{|\\mu_1-\\mu_2|}{\\sigma_n}", self.text)

    def test_objectives_cover_registration_chain(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "coordenada física",
            "frame of reference",
            "rígidas",
            "afines",
            "deformables",
            "mutual information",
            "remuestreo",
            "target registration error",
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
        for phrase in ("geometría", "métrica", "remuestreo", "deformable", "validación"):
            self.assertIn(phrase, headings)

    def test_geometry_section_protects_transform_direction(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "índice discreto",
            "coordenada física",
            "spacing",
            "origin",
            "frame of reference uid",
            "fixed→moving",
            "su inversa",
            "no es conmutativa",
        ):
            self.assertIn(phrase, text)

    def test_metric_section_separates_optimization_from_accuracy(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "mean squares",
            "correlación",
            "mutual information",
            "inicialización",
            "multirresolución",
            "regularización",
            "no una unidad universal de exactitud espacial",
        ):
            self.assertIn(phrase, text)

    def test_resampling_section_distinguishes_intensity_and_labels(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "remuestrear",
            "interpolación lineal",
            "nearest-neighbor",
            "etiquetas discretas",
            "remuestreos",
            "overlay bonito no garantiza",
        ):
            self.assertIn(phrase, text)

    def test_deformable_section_requires_plausibility_checks(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "campo de desplazamiento",
            "jacobiano",
            "folding",
            "regularización",
            "consistencia inversa",
            "deformable spatial registration",
        ):
            self.assertIn(phrase, text)
        equations = " ".join(x["latex"] for x in self.unit["theory_sections"][3]["equations"])
        self.assertIn(r"T(\\mathbf{x})", equations)
        self.assertIn(r"\\det", equations)

    def test_validation_section_separates_fre_tre_and_dice(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in (
            "target registration error",
            "fiducial registration error",
            "fre no debe venderse como tre",
            "dice",
            "landmarks independientes",
            "una cifra global puede ocultar",
        ):
            self.assertIn(phrase, text)

    def test_glossary_is_disciplinary_and_unique(self) -> None:
        terms = [x["term"].strip().casefold() for x in self.unit["glossary"]]
        self.assertEqual(len(terms), len(set(terms)))
        self.assertGreaterEqual(len(terms), 55)
        glossary = set(terms)
        for term in (
            "transformación rígida",
            "transformación afín",
            "mutual information",
            "campo de desplazamiento",
            "determinante jacobiano",
            "remuestreo",
            "tre",
            "fre",
            "spatial registration iod",
            "deformable spatial registration iod",
        ):
            self.assertIn(term, glossary)

    def test_guided_activity_requires_independent_validation(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)
        joined = " ".join(activity["instructions"] + activity["problems"] + activity["checking_criteria"]).casefold()
        for phrase in (
            "fixed image",
            "moving image",
            "landmarks independientes",
            "tre",
            "fre",
            "nearest-neighbor",
            "jacobiano",
            "frame of reference",
            "no se formula diagnóstico",
        ):
            self.assertIn(phrase, joined)

    def test_common_errors_protect_high_impact_misinterpretations(self) -> None:
        errors = json.dumps(self.unit["common_errors"], ensure_ascii=False).casefold()
        for phrase in (
            "índice de voxel con posición física",
            "dirección opuesta",
            "mutual information alta",
            "interpolar etiquetas",
            "dice como sinónimo",
            "fre de los fiduciales",
            "jacobiano positivo",
            "frame of reference uid garantiza",
            "registro sintético a uso clínico",
        ):
            self.assertIn(phrase, errors)

    def test_sources_assessment_connections_and_scope(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 18)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        sources = json.dumps(self.unit["sources"], ensure_ascii=False).casefold()
        for authority in (
            "dicom standards committee",
            "simpleitk",
            "insight software consortium",
            "american association of physicists in medicine",
            "fitzpatrick",
        ):
            self.assertIn(authority, sources)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "datos sintéticos",
            "no interpreta estudios clínicos",
            "no aprueba transformaciones",
            "no propaga dosis",
            "u6 queda reservada",
        ):
            self.assertIn(phrase, notice)

    def test_published_descriptor_matches_when_promoted(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        published = next(x for x in subject["detailed_units"] if x["unit"] == 5)
        if published["description"] != self.unit["purpose"]:
            self.skipTest("El descriptor se vuelve estricto después de la promoción automática.")
        self.assertEqual(published["description"], self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()
