from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "imagenes-biomedicas-avanzadas-i" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "imagenes-biomedicas-avanzadas-i" / "unit-01.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ImagenesBiomedicasAvanzadasIUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["slug"], "reconstruccion-tomografica")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn(r"v=\\frac{\\delta y}{\\delta t}", self.text)

    def test_objectives_cover_forward_inverse_and_task_based_evaluation(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "atenuación exponencial",
            "transformada de radon",
            "teorema de corte de fourier",
            "retroproyección filtrada",
            "muestreo angular",
            "reconstrucción iterativa",
            "regularización",
            "nps",
            "detectabilidad",
        ):
            self.assertIn(phrase, objectives)
        # MTF y TTF son métricas distintas; no se exige una grafía editorial "TTF/MTF".
        self.assertIn("mtf", objectives)
        self.assertIn("ttf", objectives)

    def test_five_substantive_theory_sections(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        for section in sections:
            self.assertGreaterEqual(len(section["paragraphs"]), 6)
            self.assertGreaterEqual(len(section["key_points"]), 6)
            for point in section["key_points"]:
                self.assertGreaterEqual(len(point.split()), 5)
        headings = " ".join(x["heading"] for x in sections).casefold()
        for phrase in (
            "sinograma",
            "fbp",
            "problema inverso regularizado",
            "artefactos",
            "calidad cuantitativa",
        ):
            self.assertIn(phrase, headings)

    def test_forward_model_and_radon_are_explicit(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "logaritmo negativo",
            "integral de línea",
            "transformada de radon",
            "sinograma",
            "fan-beam",
            "muestreo detector",
            "muestreo angular",
            "datos crudos de proyección",
        ):
            self.assertIn(phrase, text)
        equations = " ".join(x["latex"] for x in self.unit["theory_sections"][0]["equations"])
        self.assertIn("\\exp", equations)
        self.assertIn("\\mathcal{R}", equations)

    def test_fbp_section_distinguishes_backprojection_filtering_and_missing_angles(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "teorema de corte de fourier",
            "retroproyección simple",
            "filtro rampa",
            "sparse-view",
            "limited-angle",
            "no es una referencia verdadera por definición",
        ):
            self.assertIn(phrase, text)
        # Acepta la familia léxica apodizar/apodización: lo importante es el concepto de ventana del filtro.
        self.assertIn("apodiz", text)

    def test_iterative_section_enforces_inverse_problem_boundaries(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "ax≈b",
            "fidelidad a los datos",
            "regularización",
            "parámetro λ",
            "convergencia numérica",
            "no demuestra identificabilidad",
            "no se permitirá comparar una fbp de dosis alta con una iterativa de dosis baja",
        ):
            self.assertIn(phrase, text)
        equations = " ".join(x["latex"] for x in self.unit["theory_sections"][2]["equations"])
        self.assertIn("\\arg\\min", equations)

    def test_artifact_section_teaches_mechanisms_not_appearance_only(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "beam hardening",
            "photon starvation",
            "metal artifact",
            "dispersión",
            "movimiento",
            "truncación",
            "sparse-view",
            "limited-angle",
            "volumen parcial",
            "pixel spacing",
            "prueba discriminante",
        ):
            self.assertIn(phrase, text)
        self.assertIn("puede reducir un patrón y a la vez introducir estructuras nuevas", text)

    def test_quality_section_is_task_based_and_dicom_traceable(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in (
            "unidades hounsfield",
            "noise power spectrum",
            "task transfer function",
            "c nr",
            "reconstruction algorithm",
            "convolution kernel",
            "reconstruction diameter",
            "pixel spacing",
            "metal artifact reduction",
            "no valida una reconstrucción para pacientes",
        ):
            # tolerate conventional acronym formatting while keeping semantic coverage
            normalized = text.replace("cnr", "c nr")
            self.assertIn(phrase, normalized)

    def test_glossary_is_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 45)
        for term in (
            "transformada de radon",
            "sinograma",
            "fbp",
            "filtro rampa",
            "proyector directo",
            "problema inverso",
            "regularización",
            "sparse-view",
            "limited-angle",
            "beam hardening",
            "photon starvation",
            "hounsfield unit",
            "nps",
            "mtf",
            "ttf",
            "reconstruction algorithm",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)

    def test_guided_activity_requires_reconstruction_and_audit(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 24)
        joined = " ".join(activity["instructions"] + activity["problems"] + activity["checking_criteria"]).casefold()
        for phrase in (
            "fantoma 2d sintético",
            "sinograma",
            "retroproyección simple",
            "filtro rampa",
            "limited-angle",
            "photon starvation",
            "beam hardening",
            "residual",
            "nps",
            "pixel spacing",
            "no se concluye reducción de dosis",
        ):
            self.assertIn(phrase, joined)

    def test_common_errors_protect_high_impact_misinterpretations(self) -> None:
        errors = json.dumps(self.unit["common_errors"], ensure_ascii=False).casefold()
        for phrase in (
            "retroproyección simple es la inversa exacta",
            "sparse-view y limited-angle como sinónimos",
            "pixel spacing con resolución espacial real",
            "convergencia iterativa implica validez clínica",
            "cnr como métrica total",
            "reducción segura de dosis",
        ):
            self.assertIn(phrase, errors)

    def test_sources_assessment_connections_and_scope(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 16)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no reconstruye datos crudos de pacientes",
            "no recomienda parámetros de exposición",
            "no certifica algoritmos",
            "no afirma equivalencia entre fabricantes",
            "u2 continúa con mri avanzada",
        ):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
