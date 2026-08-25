from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "fisiologia-sistemas" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "fisiologia-sistemas" / "unit-06.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class FisiologiaSistemasUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["slug"], "modelos-integradores-y-datos")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn(r"v=\\frac{\\delta y}{\\delta t}", self.text)

    def test_specific_integrative_objectives(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "estados, entradas, salidas",
            "aliasing",
            "identificabilidad estructural",
            "identificabilidad práctica",
            "calibración, verificación",
            "paquete reproducible",
        ):
            self.assertIn(phrase, objectives)

    def test_five_substantive_theory_sections(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        for section in sections:
            self.assertGreaterEqual(len(section["paragraphs"]), 6)
            self.assertGreaterEqual(len(section["key_points"]), 6)
        headings = " ".join(x["heading"] for x in sections).casefold()
        for phrase in ("modelo de estados", "series temporales", "identificabilidad", "validación", "multiescala"):
            self.assertIn(phrase, headings)

    def test_key_points_are_explanatory_not_labels(self) -> None:
        for section in self.unit["theory_sections"]:
            for point in section["key_points"]:
                self.assertGreaterEqual(
                    len(point.split()),
                    4,
                    msg=f"Punto clave demasiado breve: {point}",
                )
        joined = " ".join(
            point.casefold()
            for section in self.unit["theory_sections"]
            for point in section["key_points"]
        )
        for phrase in (
            "frecuencia, regularidad y ventana de muestreo",
            "perturbaciones informativas revelan ganancias y constantes de tiempo",
            "sensibilidad local alta no garantiza identificabilidad",
            "calibración, verificación y validación responden a preguntas distintas",
            "estándares de intercambio facilitan reproducción y reutilización",
        ):
            self.assertIn(phrase, joined)

    def test_identifiability_is_not_fit_or_sensitivity(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "identificabilidad estructural",
            "identificabilidad práctica",
            "sensibilidad alta no garantiza identificabilidad",
            "un buen ajuste de las salidas observadas no implica que los parámetros individuales sean identificables",
        ):
            self.assertIn(phrase, text)

    def test_validation_and_reproducibility_boundaries(self) -> None:
        for phrase in (
            "calibración, verificación y validación responden a preguntas distintas",
            "computacionalmente reproducible y fisiológicamente incorrecto",
            "formato estándar o una simulación reproducible no prueban corrección fisiológica",
        ):
            self.assertIn(phrase, self.text)

    def test_glossary_is_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 35)
        for term in (
            "variable de estado",
            "aliasing",
            "identificabilidad estructural",
            "identificabilidad práctica",
            "verificación",
            "validación",
            "incertidumbre estructural",
            "multiescala",
            "acoplamiento",
        ):
            self.assertIn(term, glossary)

    def test_reproducibility_standards_are_taught_without_certifying_truth(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in ("cellml", "sed-ml", "combine", "biomodels", "physiome"):
            self.assertIn(phrase, text)
        self.assertIn("formato estándar o una simulación reproducible no prueban corrección fisiológica", self.text)

    def test_activity_is_integrative_and_reproducible(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 360)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 20)

    def test_common_errors_block_modeling_shortcuts(self) -> None:
        errors = json.dumps(self.unit["common_errors"], ensure_ascii=False).casefold()
        for phrase in (
            "sensibilidad alta con identificabilidad",
            "mismos datos para calibrar y validar",
            "modelo está validado porque tiene rmse bajo",
            "modelo reproducible es fisiológicamente verdadero",
            "cellml, sed-ml o un repositorio certifican corrección científica",
        ):
            self.assertIn(phrase, errors)

    def test_sources_and_clinical_boundary(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 15)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "exclusivamente sintéticas",
            "no constituye modelo clínico individual",
            "gemelo digital validado",
            "cualquier transferencia a personas",
        ):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
