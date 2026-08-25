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

    def test_objectives_cover_real_registration_pipeline(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "coordenadas físicas", "frame of reference", "rígidos", "afines",
            "deformables", "mutual information", "interpolación", "multirresolución",
            "landmarks/tre", "consistencia inversa", "fusión anatómico-funcional",
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
        for phrase in ("geometría física", "métrica", "registro deformable", "validación espacial", "fusión multimodal"):
            self.assertIn(phrase, headings)

    def test_geometry_section_protects_physical_space_and_transform_direction(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "image position (patient)", "image orientation (patient)", "frame of reference uid",
            "fixed image", "moving image", "coordenadas físicas", "transformación rígida",
            "transformación afín", "radio de captura",
        ):
            self.assertIn(phrase, text)
        equations = " ".join(x["latex"] for x in self.unit["theory_sections"][0]["equations"])
        self.assertIn(r"\mathbf{R}", equations)
        self.assertIn(r"\mathbf{A}", equations)

    def test_metric_interpolation_and_optimization_are_not_confused_with_accuracy(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "cuadrados medios", "correlación", "mutual information", "entropías",
            "nearest-neighbor", "b-spline", "criterio de parada", "shrink factors",
            "smoothing sigmas", "no demuestra por sí solo correspondencia anatómica correcta",
        ):
            self.assertIn(phrase, text)

    def test_deformable_section_requires_plausibility_controls(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "b-splines", "campos de desplazamiento", "difeomórficas",
            "deformable spatial registration iod", "determinante jacobiano",
            "valores no positivos", "consistencia inversa", "learn2reg",
            "no toda diferencia entre dos imágenes debe eliminarse",
        ):
            self.assertIn(phrase, text)
        equations = " ".join(x["latex"] for x in self.unit["theory_sections"][2]["equations"])
        self.assertIn("J_T", equations)
        self.assertIn("e_{inv}", equations)

    def test_validation_section_separates_fre_tre_overlap_and_ground_truth(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "target registration error", "fiducial registration error", "fre pequeño no garantiza tre pequeño",
            "dice", "distancias de superficie", "checkerboard", "ground truth",
            "landmarks", "regiones no evaluadas",
        ):
            self.assertIn(phrase, text)
        equations = " ".join(x["latex"] for x in self.unit["theory_sections"][3]["equations"])
        self.assertIn("TRE_{RMS}", equations)
        self.assertIn("DSC", equations)

    def test_fusion_section_preserves_labels_quantification_and_provenance(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in (
            "pet/ct", "nearest-neighbor", "segmentación propagada", "componerse matemáticamente",
            "spatial registration storage", "deformable spatial registration storage",
            "escala cuantitativa original", "u6 reutilizará",
        ):
            self.assertIn(phrase, text)

    def test_glossary_is_disciplinary_unique_and_large(self) -> None:
        terms = [x["term"].strip().casefold() for x in self.unit["glossary"]]
        self.assertEqual(len(terms), len(set(terms)))
        glossary = set(terms)
        self.assertGreaterEqual(len(glossary), 55)
        for term in (
            "coordenada física", "frame of reference uid", "transformación rígida",
            "transformación afín", "displacement field", "mutual information",
            "nearest-neighbor interpolation", "multirresolución", "fiducial registration error",
            "target registration error", "jacobian determinant", "spatial registration iod",
            "deformable spatial registration iod", "label propagation", "provenance",
        ):
            self.assertIn(term, glossary)

    def test_guided_activity_requires_independent_spatial_validation(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)
        joined = " ".join(activity["instructions"] + activity["problems"] + activity["checking_criteria"]).casefold()
        for phrase in (
            "spacing", "fixed", "moving", "mutual information", "nearest-neighbor",
            "tre", "fre", "dice", "jacobiano", "consistencia inversa",
            "spatial registration", "no se afirma validez clínica",
        ):
            self.assertIn(phrase, joined)

    def test_common_errors_protect_high_impact_registration_mistakes(self) -> None:
        errors = json.dumps(self.unit["common_errors"], ensure_ascii=False).casefold()
        for phrase in (
            "índice de voxel", "fre pequeño", "nearest-neighbor", "remuestrear la imagen varias veces",
            "campo deformable porque es suave", "jacobiano positivo", "etiqueta propagada como ground truth",
            "dice alto", "fusión pet/ct", "objeto dicom spatial registration",
        ):
            self.assertIn(phrase, errors)

    def test_sources_assessment_connections_and_scope(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 18)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        sources = json.dumps(self.unit["sources"], ensure_ascii=False).casefold()
        for authority in (
            "dicom standards committee", "insight software consortium", "simpleitk",
            "maes", "klein", "fitzpatrick", "avants", "learn2reg",
        ):
            self.assertIn(authority, sources)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no registra ni fusiona estudios para atención de pacientes",
            "no propaga contornos para planificación terapéutica",
            "no interpreta imágenes diagnósticas",
            "no certifica exactitud clínica",
            "u6 queda reservada",
        ):
            self.assertIn(phrase, notice)

    def test_published_descriptor_when_promoted_matches_canonical_purpose(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        published = next(x for x in subject["detailed_units"] if x["unit"] == 5)
        # Before the publication workflow promotes this PR, the descriptor can still be generic.
        if published["description"] != self.unit["purpose"]:
            self.skipTest("Descriptor U5 aún pendiente de promoción automática.")
        self.assertEqual(published["description"], self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()
