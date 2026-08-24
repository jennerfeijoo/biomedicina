from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "biomecanica"
GENERIC = "concepto de la unidad que debe definirse"


class BiomecanicaCanonicalCourseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.course = json.loads((COURSE / "course.json").read_text(encoding="utf-8"))
        cls.sources = json.loads((COURSE / "sources.json").read_text(encoding="utf-8"))
        cls.glossary = json.loads((COURSE / "glossary.json").read_text(encoding="utf-8"))
        cls.claims = json.loads((COURSE / "claims.json").read_text(encoding="utf-8"))

    def test_course_status_preserves_human_review_boundary(self):
        status = self.course["status"]
        self.assertEqual(status["content"], "complete")
        self.assertEqual(status["sources"], "traceable")
        self.assertEqual(status["pedagogy"], "complete")
        self.assertEqual(status["multimedia"], "planned")
        self.assertEqual(status["internal_review"], "pending")
        self.assertEqual(status["external_review"], "pending")

    def test_six_units_and_all_course_outcomes_are_covered(self):
        self.assertEqual(len(self.course["unit_files"]), 6)
        known = {item["id"] for item in self.course["learning_outcomes"]}
        covered = set()
        for relative in self.course["unit_files"]:
            unit = json.loads((COURSE / relative).read_text(encoding="utf-8"))
            covered.update(unit["course_learning_outcome_ids"])
            self.assertNotIn(GENERIC, json.dumps(unit, ensure_ascii=False).casefold())
            self.assertTrue(unit["activities"][0]["estimated_duration_minutes"] > 0)
        self.assertEqual(known, covered)

    def test_assessment_items_are_classified_and_have_feedback(self):
        source_ids = {item["id"] for item in self.sources["sources"]}
        for n in range(1, 7):
            assessment = json.loads((COURSE / "assessments" / f"unit-{n:02d}.json").read_text(encoding="utf-8"))
            self.assertEqual(len(assessment["items"]), 10)
            for item in assessment["items"]:
                self.assertNotEqual(item["difficulty"], "unclassified")
                self.assertNotEqual(item["cognitive_level"], "unclassified")
                self.assertTrue(item["feedback"]["correct"])
                self.assertTrue(item["feedback"]["incorrect"])
                self.assertTrue(set(item["source_ids"]) <= source_ids)

    def test_glossary_and_claims_are_traceable(self):
        source_ids = {item["id"] for item in self.sources["sources"]}
        self.assertGreaterEqual(len(self.glossary["entries"]), 100)
        for entry in self.glossary["entries"]:
            self.assertTrue(entry["source_ids"])
            self.assertTrue(set(entry["source_ids"]) <= source_ids)
            self.assertNotEqual(entry["verification_status"], "unverified")
        self.assertGreaterEqual(len(self.claims["claims"]), 40)
        self.assertEqual({claim["unit_id"] for claim in self.claims["claims"]}, {f"BIOMEC-U{i:02d}" for i in range(1, 7)})

    def test_course_assessment_integrates_all_units(self):
        assessment = json.loads((COURSE / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))
        self.assertEqual(sum(item["weight_percent"] for item in assessment["assessment_plan"]), 100)
        self.assertEqual(sum(item["weight_percent"] for item in assessment["midterm_blueprint"]), 100)
        self.assertEqual(sum(item["weight_percent"] for item in assessment["capstone"]["rubric"]), 100)
        self.assertGreaterEqual(len(assessment["diagnostic"]["questions"]), 10)


if __name__ == "__main__":
    unittest.main()
