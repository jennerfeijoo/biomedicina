from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "fundamentos-biomecanica" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "fundamentos-biomecanica" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class FundamentosBiomecanicaUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "fundamentos-biomecanica")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in ("impulso", "trabajo", "energía", "potencia", "dinámica inversa"):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_progressive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory_words = sum(
            len(paragraph.split())
            for section in sections
            for paragraph in section["paragraphs"]
        )
        self.assertGreaterEqual(theory_words, 1500)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("\\sum \\mathbf F_{ext}=m\\mathbf a_{COM}", equations)
        self.assertIn("\\mathbf J=\\int_{t_1}^{t_2}\\mathbf F_{net}(t)\\,dt=\\Delta\\mathbf p", equations)
        self.assertIn("W_{net}=\\Delta K", equations)
        self.assertIn("P_{rot}=M\\omega", equations)

    def test_activities_use_scaffolding_and_synthetic_data(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        first = activities[0]
        self.assertGreaterEqual(len(first["instructions"]), 5)
        self.assertGreaterEqual(len(first["problems"]), 10)
        self.assertGreaterEqual(len(first["checking_criteria"]), 10)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintét", activity_text)
        self.assertIn("sensibilidad", activity_text)
        self.assertIn("sin diagnóstico", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 18)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 4)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 8)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "cantidad de movimiento",
            "impulso",
            "trabajo mecánico",
            "potencia articular neta",
            "dinámica inversa",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_disciplinary(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/31791632/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/15151864/", urls)
        self.assertIn("https://www.isbweb.org/activities/standards", urls)
        self.assertIn("https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53090079", urls)

    def test_scope_boundary_is_explicit(self) -> None:
        purpose = self.unit["purpose"].casefold()
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("fuerzas musculares individuales", purpose)
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no autoriza estimar fuerzas musculares individuales", notice)
        self.assertIn("evaluar riesgo de lesión", notice)
        self.assertIn("datos sintéticos", notice)


if __name__ == "__main__":
    unittest.main()

# Final user-authored trigger after publication metadata synchronization.
