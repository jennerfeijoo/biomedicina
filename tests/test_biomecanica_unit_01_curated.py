from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomecanica" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "biomecanica" / "unit-01.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomecanicaUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomecanica")
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("\\sum \\mathbf{f}=m\\mathbf{a}", text)
        self.assertIn("\\mathbf r_b=\\mathbf r_{ba}\\mathbf r_a+\\mathbf p_{ba}".replace("\\mathbf r_{ba}", "\\mathbf r_{ba}"), text)

    def test_theory_is_kinematic_and_substantive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "marco de referencia",
            "matriz de rotación",
            "diferenciación",
            "análisis bidimensional",
            "artefacto de tejido blando",
            "reproducibilidad",
        ):
            self.assertIn(concept, theory)
        self.assertNotIn("fuerzas y momentos que producen", theory.split("sin atribuir todavía", 1)[0] if "sin atribuir todavía" in theory else "")

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 10)
        self.assertGreaterEqual(len(activity["deliverables"]), 6)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        activity_text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintético", activity_text)
        self.assertIn("no grabes personas", activity_text)
        self.assertIn("2d", activity_text)
        self.assertIn("3d", activity_text)

    def test_sources_are_directly_verified_and_specific(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://www.isbweb.org/activities/standards", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/11934426/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/11415604/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/34283131/", urls)

    def test_glossary_examples_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 16)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 3)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 8)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("cinemática", "marco de referencia", "matriz de rotación", "artefacto de tejido blando"):
            self.assertIn(term, terms)

    def test_editorial_boundary_does_not_claim_external_validation(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("estado review", notice)
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no requieren registrar personas", notice)


if __name__ == "__main__":
    unittest.main()
