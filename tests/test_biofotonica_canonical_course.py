from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "biofotonica"
GENERIC = "concepto de la unidad que debe definirse"


class BiofotonicaCanonicalCourseTests(unittest.TestCase):
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
        self.assertEqual(status["publication"], "published_provisional")

    def test_six_units_cover_all_course_outcomes_without_generic_template(self):
        self.assertEqual(len(self.course["unit_files"]), 6)
        known = {item["id"] for item in self.course["learning_outcomes"]}
        covered = set()
        for relative in self.course["unit_files"]:
            unit = json.loads((COURSE / relative).read_text(encoding="utf-8"))
            covered.update(unit["course_learning_outcome_ids"])
            self.assertNotIn(GENERIC, json.dumps(unit, ensure_ascii=False).casefold())
            self.assertGreaterEqual(len(unit["topics"]), 4)
            self.assertGreaterEqual(len(unit["examples"]), 3)
            self.assertTrue(unit["activities"])
            self.assertTrue(all(activity["estimated_duration_minutes"] > 0 for activity in unit["activities"]))
            self.assertTrue(all(activity["status"] == "complete" for activity in unit["activities"]))
            self.assertEqual(unit["status"]["content"], "complete")
            self.assertEqual(unit["status"]["sources"], "traceable")
            self.assertEqual(unit["status"]["pedagogy"], "complete")
        self.assertEqual(known, covered)

    def test_sixty_assessment_items_are_classified_feedback_rich_and_traceable(self):
        source_ids = {item["id"] for item in self.sources["sources"]}
        total = 0
        for n in range(1, 7):
            assessment = json.loads((COURSE / "assessments" / f"unit-{n:02d}.json").read_text(encoding="utf-8"))
            self.assertEqual(len(assessment["items"]), 10)
            self.assertEqual(assessment["status"], "complete")
            total += len(assessment["items"])
            for item in assessment["items"]:
                self.assertNotEqual(item["difficulty"], "unclassified")
                self.assertNotEqual(item["cognitive_level"], "unclassified")
                self.assertTrue(item["answer_key"]["explanation"])
                self.assertTrue(item["feedback"]["correct"])
                self.assertTrue(item["feedback"]["incorrect"])
                self.assertTrue(item["source_ids"])
                self.assertTrue(set(item["source_ids"]) <= source_ids)
                self.assertEqual(item["status"], "complete")
        self.assertEqual(total, 60)

    def test_glossary_claims_and_sources_are_cross_linked(self):
        source_ids = {item["id"] for item in self.sources["sources"]}
        self.assertGreaterEqual(len(source_ids), 30)
        self.assertTrue(all(item["verification_status"] == "verified_directly" for item in self.sources["sources"]))
        self.assertEqual(self.sources["coverage_gaps"], [])
        self.assertGreaterEqual(len(self.glossary["entries"]), 70)
        for entry in self.glossary["entries"]:
            self.assertTrue(entry["source_ids"])
            self.assertTrue(set(entry["source_ids"]) <= source_ids)
            self.assertEqual(entry["verification_status"], "traceable_to_verified_source")
        self.assertEqual(len(self.claims["claims"]), 48)
        self.assertEqual({claim["unit_id"] for claim in self.claims["claims"]}, {f"BIOFOT-U{i:02d}" for i in range(1, 7)})
        for claim in self.claims["claims"]:
            self.assertIn(claim["source_id"], source_ids)
            self.assertEqual(claim["source_verification_status"], "verified_directly")
            self.assertEqual(claim["review_state"], "ai_review_provisional")

    def test_course_assessment_integrates_all_six_units(self):
        assessment = json.loads((COURSE / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))
        self.assertEqual(sum(item["weight_percent"] for item in assessment["assessment_plan"]), 100)
        self.assertEqual(sum(item["weight_percent"] for item in assessment["midterm_blueprint"]), 100)
        self.assertEqual(sum(item["weight_percent"] for item in assessment["capstone"]["rubric"]), 100)
        self.assertGreaterEqual(len(assessment["diagnostic"]["questions"]), 12)
        self.assertGreaterEqual(len(assessment["capstone"]["required_deliverables"]), 8)
        self.assertEqual(assessment["status"], "complete")

    def test_course_scope_and_review_boundary_are_explicit(self):
        notice = self.course["editorial_notice"].casefold()
        purpose = self.course["purpose"].casefold()
        self.assertIn("revisión disciplinaria externa", notice)
        self.assertIn("validación clínica", notice)
        self.assertIn("conformidad regulatoria", notice)
        self.assertIn("radiación óptica", notice)
        self.assertIn("interacción luz-tejido", purpose)
        self.assertIn("incertidumbre", purpose)
        self.assertIn("validación clínica", purpose)


if __name__ == "__main__":
    unittest.main()
