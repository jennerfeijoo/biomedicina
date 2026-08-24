from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "desarrollo-dispositivos-medicos" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "desarrollo-dispositivos-medicos" / "unit-01.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class DesarrolloDispositivosMedicosUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "desarrollo-dispositivos-medicos")
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertIn("needs finding", text)
        self.assertIn("need statement", text)
        self.assertIn("solution bias", text)

    def test_theory_separates_observation_need_requirement_and_solution(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "observación",
            "interpretación",
            "necesidad",
            "design input",
            "usuario",
            "entorno",
            "stakeholder",
            "triangulación",
            "caso negativo",
            "trazabilidad",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no es un requisito de diseño", theory)

    def test_progressive_activities_are_synthetic_and_scaffolded(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertGreaterEqual(len(activities[0]["problems"]), 10)
        self.assertGreaterEqual(len(activities[0]["checking_criteria"]), 8)
        self.assertGreaterEqual(len(activities[1]["problems"]), 5)
        self.assertGreaterEqual(len(activities[2]["problems"]), 5)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("ficticio", activity_text)
        self.assertIn("no observes pacientes", activity_text)
        self.assertIn("apoyo reducido", activities[1]["title"].casefold())
        self.assertIn("autónomo", activities[2]["title"].casefold())

    def test_glossary_examples_errors_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 18)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 8)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "needs finding",
            "need statement",
            "solution bias",
            "parte interesada",
            "contexto de uso",
            "design input",
            "trazabilidad",
        ):
            self.assertIn(term, terms)

    def test_sources_include_current_authoritative_material(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        verified = [item for item in sources if item.get("verification_status") == "verified_directly"]
        self.assertEqual(len(verified), len(sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/32306842/", urls)
        self.assertIn("https://biodesign.stanford.edu/about-us/process.html", urls)
        self.assertIn(
            "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/applying-human-factors-and-usability-engineering-medical-devices",
            urls,
        )
        self.assertIn(
            "https://www.fda.gov/medical-devices/postmarket-requirements-devices/quality-management-system-regulation-qmsr",
            urls,
        )

    def test_regulatory_and_clinical_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar humana externa", notice)
        self.assertIn("validación clínica", notice)
        self.assertIn("2 de febrero de 2026", notice)
        self.assertIn("no recopiles información clínica real", notice)
        self.assertIn("requisito de diseño", purpose)
        self.assertIn("afirmación regulatoria", purpose)


# Final user-authored gate trigger after deterministic public-site synchronization.
if __name__ == "__main__":
    unittest.main()
