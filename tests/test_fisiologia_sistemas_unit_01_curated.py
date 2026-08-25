from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "fisiologia-sistemas" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "fisiologia-sistemas" / "unit-01.json"
SUBJECT = ROOT / "data" / "subjects" / "biologicas-medicas" / "fisiologia-sistemas.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class FisiologiaSistemasUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "fisiologia-sistemas")
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_generic_rate_equation_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("v=\\frac{\\delta y}{\\delta t}", self.text)
        self.assertNotIn("estructura o función biológica organizada en niveles", self.text)

    def test_theory_is_systems_homeostasis_specific(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        for concept in (
            "variable regulada", "variable controladora", "rango defendido", "estado estacionario",
            "retroalimentación negativa", "feedforward", "ganancia", "latencia", "saturación",
            "acoplamiento entre órganos", "modelo falsable",
        ):
            self.assertIn(concept, self.text)

    def test_key_misconceptions_are_explicitly_blocked(self) -> None:
        for phrase in (
            "una variable estable no es necesariamente una variable homeostáticamente regulada",
            "los mecanismos homeostáticos operan continuamente",
            "negativo significa que el efecto neto se opone a la perturbación",
            "un set point único es una abstracción",
            "la señal de control puede seguir aumentando mientras la respuesta efectiva deja de crecer",
        ):
            self.assertIn(phrase, self.text)

    def test_core_equations_are_present_with_limits(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        for equation in (
            "e(t)=r(t)-y(t)",
            "G=\\frac{\\Delta y_{corr}}{e_{res}}",
            "\\frac{dx}{dt}=J_{in}+P-J_{out}-U",
        ):
            self.assertIn(equation, equations)
        self.assertIn("no presupone un comparador anatómico único", self.text)
        self.assertIn("no demuestra por sí solo cuál es la variable regulada", self.text)

    def test_examples_cover_transfer_without_stealing_later_units(self) -> None:
        examples = self.unit["worked_examples"]
        self.assertGreaterEqual(len(examples), 5)
        example_text = json.dumps(examples, ensure_ascii=False).casefold()
        for phrase in ("ortostatismo", "osmolalidad", "comida", "carga térmica", "sensor"):
            self.assertIn(phrase, example_text)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "u2 desarrollará integración neuroendocrina",
            "u3 acoplamiento cardiorrespiratorio",
            "u4 balance renal y metabólico",
            "u5 inflamación e inmunidad sistémica",
            "u6 modelado integrador y datos",
        ):
            self.assertIn(phrase, notice)

    def test_guided_activity_is_scaffolded_reproducible_and_safe(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 10)
        self.assertGreaterEqual(len(activity["problems"]), 18)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 20)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        for phrase in (
            "datos sintéticos", "dos modelos candidatos", "saturación", "retraso",
            "no conviertas rangos sintéticos", "predicción falsable", "evidencia pendiente",
        ):
            self.assertIn(phrase, text)

    def test_learning_scaffolds_are_specific_and_sufficient(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 40)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 18)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "homeostasis", "variable regulada", "variable controladora", "rango defendido",
            "estado estacionario", "retroalimentación negativa", "feedforward", "ganancia",
            "latencia", "saturación", "barorreflejo", "osmorregulación", "termorregulación",
            "allostasis", "modelo falsable",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_include_core_pedagogy(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 15)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://openstax.org/books/anatomy-and-physiology-2e/pages/1-5-homeostasis",
            "https://pubmed.ncbi.nlm.nih.gov/26628646/",
            "https://pubmed.ncbi.nlm.nih.gov/27105740/",
            "https://pubmed.ncbi.nlm.nih.gov/40063381/",
            "https://pubmed.ncbi.nlm.nih.gov/41847338/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC10988470/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC9394784/",
        ):
            self.assertIn(url, urls)

    def test_course_and_clinical_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no constituye diagnóstico",
            "fisiología humana i ya introduce compartimentos, transporte y homeostasis general",
            "evita repetirlos",
            "datos sintéticos",
            "no para sustituir esas unidades",
            "ni para interpretar casos reales de pacientes",
        ):
            self.assertIn(phrase, notice)

    def test_published_descriptor_tracks_curated_unit_purpose(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        unit_one = next(item for item in subject["detailed_units"] if item["unit"] == 1)
        self.assertEqual(unit_one["title"], self.unit["title"])
        self.assertEqual(unit_one["description"], self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()
