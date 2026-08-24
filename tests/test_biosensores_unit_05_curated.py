from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biosensores" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "biosensores" / "unit-05.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"

# Final normal trigger after publication metadata synchronization.


class BiosensoresUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biosensores")
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_wrong_sensitivity_definition_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertIn("sensibilidad analítica", self.text)
        self.assertIn("sensibilidad diagnóstica", self.text)
        self.assertNotIn("proporción de casos positivos de referencia que una prueba identifica correctamente", self.text)

    def test_theory_covers_core_analytical_performance(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "calibración",
            "precisión",
            "sesgo",
            "interferencia",
            "lob",
            "lod",
            "loq",
            "bland",
            "correlación",
        ):
            self.assertIn(concept, theory)
        self.assertIn("correlación alta puede ocurrir", theory)
        self.assertIn("separar asociación de acuerdo", theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("y=a+bx", equations)
        self.assertIn("x_L=\\bar x_B+k s_B", equations)
        self.assertIn("LoA=\\bar d\\pm1.96 s_d", equations)

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        activity_text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintétic", activity_text)
        self.assertIn("lob", activity_text)
        self.assertIn("lod", activity_text)
        self.assertIn("loq", activity_text)
        self.assertIn("correlación", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "calibración",
            "sensibilidad analítica",
            "sensibilidad diagnóstica",
            "precisión",
            "sesgo",
            "lob",
            "lod",
            "loq",
            "límites de acuerdo",
        ):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_methodologically_relevant(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        verified = [item for item in sources if item.get("verification_status") == "verified_directly"]
        self.assertGreaterEqual(len(verified), 10)
        urls = {item["url"] for item in sources}
        for url in (
            "https://goldbook.iupac.org/terms/view/08124",
            "https://eurachem.org/index.php/publications/guides/mv",
            "https://clsi.org/shop/standards/ep17/",
            "https://pubmed.ncbi.nlm.nih.gov/18852857/",
            "https://pubmed.ncbi.nlm.nih.gov/2868172/",
        ):
            self.assertIn(url, urls)

    def test_clinical_and_regulatory_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("validación clínica", notice)
        self.assertIn("conformidad regulatoria", notice)
        self.assertIn("sensibilidad diagnóstica", purpose)
        self.assertIn("utilidad clínica", purpose)


if __name__ == "__main__":
    unittest.main()
