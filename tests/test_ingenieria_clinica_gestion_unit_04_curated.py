from __future__ import annotations

# User-authored validation trigger after public-site synchronization.
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "ingenieria-clinica-gestion" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "ingenieria-clinica-gestion" / "unit-04.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class IngenieriaClinicaGestionUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "ingenieria-clinica-gestion")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_wrong_risk_equation_are_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("r=p\\times s", text)
        self.assertIn("coste total", text)
        self.assertIn("evaluación de tecnologías sanitarias", text)
        self.assertIn("requisito obligatorio", text)

    def test_theory_is_substantive_and_preserves_boundaries(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "coste total",
            "interoperabilidad",
            "hta",
            "multicriterio",
            "sensibilidad",
            "conflicto de interés",
            "elegibilidad",
        ):
            self.assertIn(concept, theory)
        self.assertIn("u2", theory)
        self.assertIn("u3", theory)
        self.assertIn("u5", theory)
        self.assertIn("u6", theory)

    def test_equations_are_procurement_specific(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertTrue(any(eq.startswith("TCO=") for eq in equations))
        self.assertIn("VP=C_0+\\sum_{t=1}^{N}\\frac{C_t}{(1+r)^t}", equations)
        self.assertIn("S_i=\\sum_{j=1}^{k} w_j s_{ij},\\qquad \\sum_{j=1}^{k}w_j=1", equations)

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 6)
        self.assertGreaterEqual(len(activity["problems"]), 14)
        self.assertGreaterEqual(len(activity["deliverables"]), 9)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 12)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintéticas", text)
        self.assertIn("no solicites cotizaciones reales", text)
        self.assertIn("tco", text)
        self.assertIn("sensibilidad", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "requisito obligatorio",
            "coste total de propiedad (tco)",
            "evaluación de tecnologías sanitarias (hta)",
            "matriz multicriterio",
            "análisis de sensibilidad",
            "conflicto de interés",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_include_current_hta(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 7)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://www.who.int/publications/i/item/9789241501378", urls)
        self.assertIn("https://www.who.int/publications/i/item/9789241501385", urls)
        self.assertIn("https://www.who.int/publications/i/item/9789240110878", urls)
        self.assertIn("https://www.who.int/publications/i/item/9789240111257", urls)
        self.assertIn("https://www.who.int/health-topics/health-technology-assessment", urls)

    def test_procurement_and_clinical_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no constituye", notice)
        self.assertIn("no requiere", notice)
        self.assertIn("sin convertir una actividad educativa en una licitación real", purpose)
        self.assertIn("sin evidencia suficiente", purpose)


if __name__ == "__main__":
    unittest.main()
