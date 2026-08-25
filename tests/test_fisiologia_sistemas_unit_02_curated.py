from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "fisiologia-sistemas" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "fisiologia-sistemas" / "unit-02.json"
SUBJECT = ROOT / "data" / "subjects" / "biologicas-medicas" / "fisiologia-sistemas.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class FisiologiaSistemasUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()
        cls.subject = json.loads(SUBJECT.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "fisiologia-sistemas")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_generic_rate_equation_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("v=\\frac{\\delta y}{\\delta t}", self.text)
        self.assertNotIn("estructura o función biológica organizada en niveles", self.text)

    def test_theory_is_neuroendocrine_specific(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        for concept in (
            "adenohipófisis", "neurohipófisis", "sistema porta hipofisario",
            "eje hpa", "eje hpt", "eje hpg", "gh/igf-1", "prolactina",
            "pulsatilidad", "ritmo ultradiano", "ritmo circadiano",
            "núcleo supraquiasmático", "frecuencia de muestreo", "aliasing",
            "modelo falsable",
        ):
            self.assertIn(concept, self.text)

    def test_key_misconceptions_are_explicitly_blocked(self) -> None:
        for phrase in (
            "prolactina recuerda que no todos los sistemas",
            "una concentración periférica medida en sangre",
            "una muestra única de gh",
            "cortisol no es sinónimo universal de estrés",
            "un desfase temporal no demuestra causalidad",
            "el muestreo escaso puede ocultar o deformar pulsos hormonales",
        ):
            self.assertIn(phrase, self.text)

    def test_temporal_equations_are_descriptive_and_limited(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        for equation in (
            "f_p=\\frac{N_p}{T_{obs}}",
            "\\Delta t_{AB}=t_{pico,B}-t_{pico,A}",
            "AUC\\approx\\sum_i\\frac{C_i+C_{i+1}}{2}\\Delta t_i",
        ):
            self.assertIn(equation, equations)
        self.assertIn("depende de muestreo y algoritmo", self.text)
        self.assertIn("apoya secuencia temporal pero no prueba causalidad", self.text)
        self.assertIn("puede ocultar fase y pulsos", self.text)

    def test_examples_cover_axis_diversity_and_temporal_reasoning(self) -> None:
        examples = self.unit["worked_examples"]
        self.assertGreaterEqual(len(examples), 5)
        example_text = json.dumps(examples, ensure_ascii=False).casefold()
        for phrase in ("cortisol", "hpt", "gnrh", "prolactina", "fase circadiana"):
            self.assertIn(phrase, example_text)

    def test_guided_activity_is_scaffolded_reproducible_and_safe(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 12)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 9)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 20)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        for phrase in (
            "series sintéticas", "submuestrea", "aliasing", "auc",
            "confusor", "no conviertas valores sintéticos", "evidencia pendiente",
        ):
            self.assertIn(phrase, text)

    def test_learning_scaffolds_are_specific_and_sufficient(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 40)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 20)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "integración neuroendocrina", "adenohipófisis", "neurohipófisis",
            "sistema porta hipofisario", "eje hpa", "eje hpt", "eje hpg",
            "pulsatilidad", "ritmo ultradiano", "ritmo circadiano",
            "núcleo supraquiasmático", "frecuencia de muestreo", "aliasing",
            "confusor temporal", "modelo falsable",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_relevant(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 15)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://openstax.org/books/anatomy-and-physiology-2e/pages/17-3-the-pituitary-gland-and-hypothalamus",
            "https://www.ncbi.nlm.nih.gov/books/NBK278995/",
            "https://www.ncbi.nlm.nih.gov/books/NBK278958/",
            "https://www.ncbi.nlm.nih.gov/books/NBK279070/",
            "https://www.ncbi.nlm.nih.gov/books/NBK279056/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC2647703/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC4698454/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC8813037/",
        ):
            self.assertIn(url, urls)

    def test_course_and_clinical_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no constituye diagnóstico endocrinológico",
            "u1 ya desarrolla homeostasis",
            "u3 desarrollará acoplamiento cardiorrespiratorio",
            "u4 balance renal y metabólico",
            "u5 inflamación e inmunidad sistémica",
            "u6 modelado integrador y datos",
            "no deben transformarse en rangos clínicos",
        ):
            self.assertIn(phrase, notice)

    def test_published_subject_descriptor_uses_curated_u2_purpose(self) -> None:
        published_u2 = next(item for item in self.subject["detailed_units"] if item["unit"] == 2)
        self.assertEqual(published_u2["title"], self.unit["title"])
        self.assertEqual(published_u2["description"], self.unit["purpose"])
        self.assertIn("múltiples escalas temporales", published_u2["description"].casefold())
        self.assertNotIn("integrar ejes, ritmos, estrés y conducta para resolver", published_u2["description"].casefold())


if __name__ == "__main__":
    unittest.main()
