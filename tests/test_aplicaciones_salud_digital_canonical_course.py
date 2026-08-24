from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_ROOT = ROOT / "data" / "courses" / "aplicaciones-salud-digital"
GENERIC = "concepto de la unidad que debe definirse"


def load(relative: str) -> dict:
    return json.loads((COURSE_ROOT / relative).read_text(encoding="utf-8"))


class AplicacionesSaludDigitalCanonicalCourseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.course = load("course.json")
        cls.units = [load(f"units/unit-{n:02d}.json") for n in range(1, 7)]
        cls.sources = load("sources.json")
        cls.glossary = load("glossary.json")
        cls.claims = load("claims.json")
        cls.media = load("media.json")
        cls.course_assessment = load("assessments/course-assessment.json")

    def test_course_is_complete_without_false_human_review(self) -> None:
        self.assertEqual(self.course["id"], "aplicaciones-salud-digital")
        self.assertEqual(self.course["code"], "SALUDDIG")
        status = self.course["status"]
        self.assertEqual(status["content"], "complete")
        self.assertEqual(status["sources"], "traceable")
        self.assertEqual(status["pedagogy"], "complete")
        self.assertEqual(status["multimedia"], "planned")
        self.assertEqual(status["internal_review"], "pending")
        self.assertEqual(status["external_review"], "pending")
        self.assertEqual(status["publication"], "published_provisional")

    def test_six_units_are_present_and_distinct(self) -> None:
        self.assertEqual(
            [unit["title"] for unit in self.units],
            [
                "Necesidades y ecosistema digital",
                "Diseño centrado en las personas",
                "Telemedicina, apps y monitorización",
                "Datos e interoperabilidad",
                "Evaluación clínica y económica",
                "Privacidad, regulación e implementación",
            ],
        )
        all_text = json.dumps(self.units, ensure_ascii=False).casefold()
        self.assertNotIn(GENERIC, all_text)
        for concept in ("teoría de cambio", "usabilidad", "telemedicina", "fhir", "icer", "ciberseguridad"):
            self.assertIn(concept, all_text)

    def test_each_unit_has_full_pedagogical_structure(self) -> None:
        for n, unit in enumerate(self.units, 1):
            with self.subTest(unit=n):
                self.assertGreaterEqual(len(unit["learning_outcomes"]), 5)
                self.assertGreaterEqual(len(unit["topics"]), 4)
                self.assertGreaterEqual(len(unit["examples"]), 2)
                self.assertGreaterEqual(len(unit["activities"]), 1)
                self.assertTrue(unit["glossary_entry_ids"])
                self.assertTrue(unit["source_ids"])
                self.assertEqual(len(unit["claim_ids"]), 4)
                assessment = load(f"assessments/unit-{n:02d}.json")
                self.assertEqual(assessment["unit_id"], unit["id"])
                self.assertGreaterEqual(len(assessment["items"]), 8)
                self.assertTrue(all(item["answer_key"]["explanation"] for item in assessment["items"]))
                self.assertTrue(all(item["feedback"]["correct"] and item["feedback"]["incorrect"] for item in assessment["items"]))

    def test_course_learning_outcomes_are_covered(self) -> None:
        course_los = {item["id"] for item in self.course["learning_outcomes"]}
        mapped = {lo for unit in self.units for lo in unit["course_learning_outcome_ids"]}
        self.assertEqual(course_los, mapped)
        self.assertEqual(len(course_los), 7)

    def test_sources_glossary_and_claims_are_traceable(self) -> None:
        source_ids = {item["id"] for item in self.sources["sources"]}
        self.assertGreaterEqual(len(source_ids), 25)
        self.assertEqual(self.sources.get("coverage_gaps"), [])
        self.assertTrue(all(item.get("verification_status") != "unverified" for item in self.sources["sources"]))
        entries = self.glossary["entries"]
        self.assertGreaterEqual(len(entries), 80)
        self.assertTrue(all(entry.get("source_ids") for entry in entries))
        self.assertTrue(all(set(entry["source_ids"]) <= source_ids for entry in entries))
        claims = self.claims["claims"]
        self.assertEqual(len(claims), 24)
        canonical_text = {unit["id"]: json.dumps(unit, ensure_ascii=False) for unit in self.units}
        for claim in claims:
            self.assertIn(claim["source_id"], source_ids)
            self.assertIn(claim["text"], canonical_text[claim["unit_id"]])

    def test_course_assessment_is_complete_and_weighted(self) -> None:
        assessment = self.course_assessment
        self.assertEqual(assessment["scope"], "course")
        self.assertEqual(sum(item["weight_percent"] for item in assessment["assessment_plan"]), 100)
        self.assertEqual(sum(item["weight_percent"] for item in assessment["midterm_blueprint"]), 100)
        self.assertEqual(sum(item["weight_percent"] for item in assessment["capstone"]["rubric"]), 100)
        self.assertGreaterEqual(len(assessment["diagnostic"]["questions"]), 5)
        self.assertGreaterEqual(len(assessment["capstone"]["required_deliverables"]), 6)

    def test_course_preserves_evidence_boundaries(self) -> None:
        text = json.dumps(self.units, ensure_ascii=False).casefold()
        for distinction in ("consentimiento", "base jurídica", "interoperabilidad", "efectividad", "privacidad", "regulación"):
            self.assertIn(distinction, text)
        notice = self.course["editorial_notice"].casefold()
        self.assertIn("revisión disciplinaria humana", notice)
        self.assertIn("validación clínica", notice)
        self.assertIn("asesoramiento jurídico", notice)
        self.assertIn("autorización de despliegue", notice)

    def test_media_remains_planned(self) -> None:
        self.assertEqual(self.media["coverage_status"], "planned")
        self.assertEqual(len(self.media["items"]), 6)
        self.assertTrue(all(item["status"] == "planned" for item in self.media["items"]))


# Permanent regression for canonical Digital Health closure.
if __name__ == "__main__":
    unittest.main()
