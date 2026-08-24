from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_DIR = ROOT / "data" / "courses" / "ingenieria-clinica-gestion"


class IngenieriaClinicaGestionCourseCompletionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.course = json.loads((COURSE_DIR / "course.json").read_text(encoding="utf-8"))
        cls.units = [
            json.loads((COURSE_DIR / "units" / f"unit-{i:02d}.json").read_text(encoding="utf-8"))
            for i in range(1, 7)
        ]
        cls.sources = json.loads((COURSE_DIR / "sources.json").read_text(encoding="utf-8"))
        cls.glossary = json.loads((COURSE_DIR / "glossary.json").read_text(encoding="utf-8"))
        cls.claims = json.loads((COURSE_DIR / "claims.json").read_text(encoding="utf-8"))
        cls.course_assessment = json.loads(
            (COURSE_DIR / "assessments" / "course-assessment.json").read_text(encoding="utf-8")
        )

    def test_course_is_complete_but_human_review_remains_pending(self) -> None:
        status = self.course["status"]
        self.assertEqual(status["content"], "complete")
        self.assertEqual(status["sources"], "traceable")
        self.assertEqual(status["pedagogy"], "complete")
        self.assertEqual(status["multimedia"], "planned")
        self.assertEqual(status["internal_review"], "pending")
        self.assertEqual(status["external_review"], "pending")
        self.assertEqual(status["publication"], "published_provisional")

    def test_six_units_cover_distinct_lifecycle_domains(self) -> None:
        self.assertEqual([unit["order"] for unit in self.units], list(range(1, 7)))
        corpus = [json.dumps(unit, ensure_ascii=False).casefold() for unit in self.units]
        for text, expected in zip(
            corpus,
            (
                "gobernanza",
                "criticidad",
                "metrolog",
                "adquis",
                "incidente",
                "plan-do-study-act",
            ),
        ):
            self.assertIn(expected, text)
        self.assertTrue(all(unit["status"]["content"] == "complete" for unit in self.units))
        self.assertTrue(all(unit["status"]["external_review"] == "pending" for unit in self.units))

    def test_every_course_outcome_is_mapped_and_each_unit_has_full_pedagogy(self) -> None:
        course_los = {item["id"] for item in self.course["learning_outcomes"]}
        mapped = {lo for unit in self.units for lo in unit["course_learning_outcome_ids"]}
        self.assertEqual(course_los, mapped)
        for unit in self.units:
            self.assertGreaterEqual(len(unit["learning_outcomes"]), 5)
            self.assertGreaterEqual(len(unit["topics"]), 4)
            self.assertGreaterEqual(len(unit["examples"]), 2)
            self.assertGreaterEqual(len(unit["activities"]), 1)
            self.assertGreaterEqual(len(unit["common_errors"]), 8)
            self.assertGreaterEqual(len(unit["source_ids"]), 5)
            self.assertGreaterEqual(len(unit["claim_ids"]), 4)

    def test_sources_glossary_and_claims_are_traceable(self) -> None:
        sources = self.sources["sources"]
        self.assertGreaterEqual(len(sources), 20)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        entries = self.glossary["entries"]
        self.assertGreaterEqual(len(entries), 100)
        self.assertTrue(all(item.get("source_ids") for item in entries))
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in entries))
        claims = self.claims["claims"]
        self.assertGreaterEqual(len(claims), 24)
        unit_ids = {unit["id"] for unit in self.units}
        self.assertTrue(all(item["unit_id"] in unit_ids for item in claims))
        self.assertTrue(all(item.get("source_id") for item in claims))

    def test_unit_assessments_and_course_assessment_are_complete(self) -> None:
        for index, unit in enumerate(self.units, start=1):
            assessment = json.loads(
                (COURSE_DIR / "assessments" / f"unit-{index:02d}.json").read_text(encoding="utf-8")
            )
            self.assertEqual(assessment["scope"], "unit")
            self.assertGreaterEqual(len(assessment["items"]), 8)
            self.assertTrue(all(item["feedback"]["correct"] for item in assessment["items"]))
            self.assertTrue(all(item["feedback"]["incorrect"] for item in assessment["items"]))
        self.assertEqual(sum(item["weight_percent"] for item in self.course_assessment["assessment_plan"]), 100)
        self.assertEqual(sum(item["weight_percent"] for item in self.course_assessment["midterm_blueprint"]), 100)
        self.assertEqual(sum(item["weight_percent"] for item in self.course_assessment["capstone"]["rubric"]), 100)
        linked = set(self.course_assessment["capstone"]["linked_learning_outcome_ids"])
        self.assertEqual(linked, {item["id"] for item in self.course["learning_outcomes"]})

    def test_editorial_boundary_does_not_claim_external_validation(self) -> None:
        notice = self.course["editorial_notice"].casefold()
        purpose = self.course["purpose"].casefold()
        self.assertIn("revisión humana", notice)
        self.assertIn("externa", notice)
        self.assertIn("pendientes", notice)
        self.assertIn("auditoría", purpose)
        self.assertIn("certificación", purpose)
        self.assertIn("autorización operativa", purpose)


if __name__ == "__main__":
    unittest.main()
