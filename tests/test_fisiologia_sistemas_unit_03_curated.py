from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "fisiologia-sistemas" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "fisiologia-sistemas" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class FisiologiaSistemasUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "fisiologia-sistemas")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_rate_placeholder_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("v=\\frac{\\delta y}{\\delta t}", self.text)
        self.assertNotIn("estructura o función biológica organizada en niveles", self.text)

    def test_theory_builds_an_oxygen_transport_chain(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        self.assertTrue(all(len(section["paragraphs"]) >= 6 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 6 for section in sections))
        for concept in (
            "ventilación alveolar", "relación v/q", "shunt", "espacio muerto",
            "contenido arterial de oxígeno", "gasto cardiaco", "entrega de oxígeno",
            "principio de fick", "fracción de extracción", "ejercicio",
            "microcirculación", "identificabilidad",
        ):
            self.assertIn(concept, self.text)

    def test_key_misconceptions_are_explicitly_blocked(self) -> None:
        for phrase in (
            "ventilación minuto y ventilación alveolar no son equivalentes",
            "presión parcial de oxígeno y el contenido de oxígeno no son sinónimos",
            "saturación no equivale a contenido",
            "la frecuencia cardiaca sola no mide flujo",
            "la ecuación por sí sola no localiza el mecanismo causal",
            "variables globales no garantizan perfusión ni utilización homogéneas",
        ):
            self.assertIn(phrase, self.text)

    def test_physiologic_equations_replace_generic_rate(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        expected = {
            "\\dot V_A=(V_T-V_D)f_R",
            "\\dot V_E=V_T f_R",
            "\\frac{\\dot V_A}{\\dot Q}",
            "C_{aO_2}\\approx1.34\\,[Hb]S_{aO_2}+0.003P_{aO_2}",
            "\\dot Q=HR\\,SV",
            "D_{O_2}=\\dot Q\\,C_{aO_2}",
            "\\dot V_{O_2}=\\dot Q\\,(C_{aO_2}-C_{vO_2})",
            "O_{2}ER=\\frac{\\dot V_{O_2}}{D_{O_2}}=\\frac{C_{aO_2}-C_{vO_2}}{C_{aO_2}}",
        }
        self.assertTrue(expected.issubset(equations))

    def test_examples_cover_major_system_failure_modes(self) -> None:
        examples = self.unit["worked_examples"]
        self.assertGreaterEqual(len(examples), 5)
        text = json.dumps(examples, ensure_ascii=False).casefold()
        for phrase in ("ventilación alveolar", "saturación", "hemoglobina", "do2", "fick", "ejercicio", "v/q"):
            self.assertIn(phrase, text)

    def test_guided_activity_is_quantitative_reproducible_and_safe(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 14)
        self.assertGreaterEqual(len(activity["problems"]), 22)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 22)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        for phrase in ("perfiles sintéticos", "conversión", "análisis de sensibilidad", "estado estable", "no uses lactato", "dato pendiente"):
            self.assertIn(phrase, text)

    def test_learning_scaffolds_are_specific_and_sufficient(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 45)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 20)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "ventilación minuto", "ventilación alveolar", "espacio muerto fisiológico",
            "relación v/q", "shunt", "contenido arterial de oxígeno", "gasto cardiaco",
            "entrega de oxígeno", "principio de fick", "fracción de extracción de oxígeno",
            "microcirculación", "identificabilidad", "análisis de sensibilidad",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_relevant(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 15)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://openstax.org/books/anatomy-and-physiology-2e/pages/22-4-gas-exchange",
            "https://openstax.org/books/anatomy-and-physiology-2e/pages/22-5-transport-of-gases",
            "https://www.ncbi.nlm.nih.gov/books/NBK539907/",
            "https://www.ncbi.nlm.nih.gov/books/NBK538336/",
            "https://www.ncbi.nlm.nih.gov/books/NBK606091/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC6785823/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC8026750/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC10912163/",
        ):
            self.assertIn(url, urls)

    def test_course_and_clinical_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no constituye diagnóstico",
            "u1 ya desarrolla homeostasis",
            "u2 integración neuroendocrina",
            "u4 desarrollará balance renal y metabólico",
            "u5 inflamación e inmunidad sistémica",
            "u6 modelado integrador multiorgánico",
            "indicación de oxígeno",
            "transfusión",
            "vasopresores",
        ):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
