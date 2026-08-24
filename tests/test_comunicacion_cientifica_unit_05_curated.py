from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "comunicacion-cientifica" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "comunicacion-cientifica" / "unit-05.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ComunicacionCientificaUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "comunicacion-cientifica")
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "lenguaje llano",
            "riesgo absoluto",
            "riesgo relativo",
            "preprint",
            "registro de cambios",
            "pretest",
        ):
            self.assertIn(concept, text)

    def test_theory_is_public_communication_and_not_visualization_or_publication_ethics(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "denominador",
            "horizonte temporal",
            "incertidumbre",
            "formatos digitales",
            "titular",
            "fuente primaria",
            "evidencia, interpretación, opinión",
            "engagement",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no valida una afirmación", theory)

    def test_pedagogy_progressively_removes_support(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        titles = " ".join(activity["title"] for activity in activities).casefold()
        self.assertIn("actividad guiada", titles)
        self.assertIn("apoyo reducido", titles)
        self.assertIn("reto autónomo", titles)
        self.assertGreaterEqual(len(activities[0]["problems"]), 10)
        self.assertGreaterEqual(len(activities[0]["deliverables"]), 6)
        self.assertGreaterEqual(len(activities[0]["checking_criteria"]), 8)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintético", activity_text)
        self.assertIn("no uses datos de pacientes reales", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "lenguaje llano",
            "riesgo absoluto",
            "frecuencia natural",
            "resultado preliminar",
            "preprint",
            "verificación",
            "pretest",
            "registro de cambios",
        ):
            self.assertIn(term, terms)

    def test_risk_and_uncertainty_are_not_overstated(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertIn("reducción absoluta", text)
        self.assertIn("comunicar incertidumbre", text)
        self.assertIn("impide imponer una única forma universal", text)
        self.assertIn("no ofrece consejo médico individual", text)

    def test_sources_are_directly_verified(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 7)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://www.nih.gov/institutes-nih/nih-office-director/office-communications-public-liaison/clear-communication/plain-language-nih", urls)
        self.assertIn("https://www.cdc.gov/ccindex/index.html", urls)
        self.assertIn("https://www.who.int/europe/publications/communicating-uncertainty-in-health-emergencies-guidance-and-tips", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/25133362/", urls)

    def test_scope_and_professional_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar humana externa", notice)
        self.assertIn("no autorizan inferencias sobre pacientes individuales", notice)
        self.assertIn("sin convertir simplificación", purpose)
        self.assertIn("consejo médico individual", purpose)


if __name__ == "__main__":
    unittest.main()
