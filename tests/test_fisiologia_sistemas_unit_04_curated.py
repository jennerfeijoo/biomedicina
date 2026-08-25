from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "fisiologia-sistemas" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "fisiologia-sistemas" / "unit-04.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class FisiologiaSistemasUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "fisiologia-sistemas")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_generic_rate_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("v=\\frac{\\delta y}{\\delta t}", self.text)
        self.assertNotIn("estructura o función biológica organizada en niveles", self.text)

    def test_theory_is_renal_metabolic_and_system_specific(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        self.assertTrue(all(len(section["paragraphs"]) >= 6 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 6 for section in sections))
        for concept in (
            "cantidad corporal", "osmolalidad", "volumen extracelular",
            "carga filtrada", "reabsorción", "secreción", "clearance",
            "vasopresina", "raas", "aldosterona", "potasio",
            "tasa de aparición", "tasa de desaparición", "ayuno",
        ):
            self.assertIn(concept, self.text)

    def test_key_misconceptions_are_explicitly_blocked(self) -> None:
        for phrase in (
            "la concentración plasmática de sodio no es una lectura directa del sodio corporal total",
            "filtración y excreción no son equivalentes",
            "clearance es una construcción funcional, no un espacio anatómico",
            "control de agua/osmolalidad y control de sodio/volumen se solapan pero no son idénticos",
            "la glucosa plasmática tampoco equivale a energía corporal total",
            "estado estacionario de concentración no significa ausencia de metabolismo",
        ):
            self.assertIn(phrase, self.text)

    def test_diuresis_and_natriuresis_are_not_equated(self) -> None:
        errors = json.dumps(self.unit["common_errors"], ensure_ascii=False).casefold()
        self.assertIn("interpretar diuresis como natriuresis", errors)
        self.assertIn("flujo de orina y excreción de sodio son magnitudes diferentes", errors)

    def test_balance_equations_replace_placeholder(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        expected = {
            "C_x=\\frac{M_x}{V}",
            "\\Delta M_x=M_{in}-M_{out}",
            "F_x=GFR\\,P_x",
            "E_x=U_x\\dot V",
            "C_x=\\frac{U_x\\dot V}{P_x}",
            "\\frac{dG}{dt}=R_a-R_d",
        }
        self.assertTrue(expected.issubset(equations))
        self.assertIn("volumen virtual", self.text)
        self.assertIn("misma frontera y unidades", self.text)

    def test_examples_and_activity_force_balance_reasoning(self) -> None:
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 14)
        self.assertGreaterEqual(len(activity["problems"]), 22)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 22)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        for phrase in (
            "cantidad, concentración, volumen", "pérdida isotónica", "clearance",
            "redistribución transcelular", "r_a y r_d", "análisis de sensibilidad",
            "no uses umbrales diagnósticos", "dato pendiente",
        ):
            self.assertIn(phrase, text)

    def test_learning_scaffolds_are_specific_and_sufficient(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 45)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 20)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "balance de masa", "cantidad corporal", "osmolalidad", "tonicidad",
            "sodio corporal total", "volumen circulante efectivo", "carga filtrada",
            "excreción urinaria", "clearance renal", "vasopresina", "raas",
            "natriuresis", "diuresis", "redistribución transcelular", "pool de glucosa",
            "tasa de aparición de glucosa", "tasa de desaparición de glucosa",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_relevant(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 15)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://openstax.org/books/anatomy-and-physiology-2e/pages/25-5-physiology-of-urine-formation",
            "https://openstax.org/books/anatomy-and-physiology-2e/pages/25-8-endocrine-regulation-of-kidney-function",
            "https://openstax.org/books/anatomy-and-physiology-2e/pages/26-3-electrolyte-balance",
            "https://www.ncbi.nlm.nih.gov/books/NBK500032/",
            "https://www.ncbi.nlm.nih.gov/books/NBK482447/?report=classic",
            "https://pubmed.ncbi.nlm.nih.gov/7006395/",
            "https://www.ncbi.nlm.nih.gov/books/NBK545201/",
            "https://www.ncbi.nlm.nih.gov/books/NBK279127/",
        ):
            self.assertIn(url, urls)

    def test_course_and_clinical_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no constituye diagnóstico renal, endocrino o electrolítico",
            "u1 ya desarrolla homeostasis",
            "u2 integración neuroendocrina",
            "u3 transporte cardiorrespiratorio",
            "u5 desarrollará inflamación e inmunidad sistémica",
            "u6 modelado integrador y datos",
            "datos exclusivamente sintéticos",
        ):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
