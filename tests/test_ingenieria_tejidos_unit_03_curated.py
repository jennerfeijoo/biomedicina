# Final user-authored trigger after regression correction and deterministic public synchronization.
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "ingenieria-tejidos" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "ingenieria-tejidos" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class IngenieriaTejidosUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "ingenieria-tejidos")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in ("interconectividad", "hidrogel", "degradación", "funcionalización", "análisis de sensibilidad"):
            self.assertIn(concept, text)

    def test_theory_is_scaffold_specific_and_substantive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "uso previsto",
            "porosidad",
            "interconectividad",
            "anisotropía",
            "superficie condicionada",
            "retención de masa",
            "criterios no compensables",
            "iso 10993-1",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no existe un tamaño de poro universalmente óptimo", theory)
        self.assertIn("no autoriza llamar «biocompatible»", theory)

    def test_equations_are_relevant_and_bounded(self) -> None:
        equations = [e for section in self.unit["theory_sections"] for e in section.get("equations", [])]
        latex = {e["latex"] for e in equations}
        self.assertIn("\\varepsilon=1-\\frac{\\rho^*}{\\rho_s}", latex)
        self.assertIn("Q_m=\\frac{m_{wet}-m_{dry}}{m_{dry}}", latex)
        self.assertIn("M_r(t)=100\\,\\frac{m(t)}{m_0}", latex)
        meanings = " ".join(e["meaning"] for e in equations).casefold()
        self.assertIn("no informa interconectividad", meanings)
        self.assertIn("no equivale por sí sola", meanings)

    def test_guided_activities_are_progressive_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintético", text)
        self.assertIn("retira parte de la ayuda", text)
        self.assertIn("elimina progresivamente las ayudas", text)
        self.assertIn("uso previsto→requisitos→candidatos→evidencia→decisión→límite", text)
        total_items = sum(
            len(activity.get(key, []))
            for activity in activities
            for key in ("instructions", "problems", "tasks", "deliverables", "checking_criteria")
        )
        self.assertGreaterEqual(total_items, 70)

    def test_learning_support_is_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 4)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "biomaterial",
            "andamio (scaffold)",
            "porosidad",
            "interconectividad",
            "hidrogel",
            "funcionalización",
            "matriz multicriterio",
            "biocompatibilidad",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://pubmed.ncbi.nlm.nih.gov/16003400/",
            "https://pubmed.ncbi.nlm.nih.gov/11071603/",
            "https://pubmed.ncbi.nlm.nih.gov/19819008/",
            "https://pubmed.ncbi.nlm.nih.gov/24547761/",
            "https://pubmed.ncbi.nlm.nih.gov/22026626/",
            "https://pubmed.ncbi.nlm.nih.gov/24689032/",
            "https://www.iso.org/standard/10993-1",
        ):
            self.assertIn(url, urls)

    def test_curricular_and_safety_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        for boundary in ("u4", "u5", "u6", "no constituye revisión disciplinar externa", "ni recomendación de un producto"):
            self.assertIn(boundary, notice)
        self.assertIn("beneficio clínico", purpose)
        self.assertIn("biocompatible", purpose)


if __name__ == "__main__":
    unittest.main()
