from __future__ import annotations

# Final user-authored gate trigger after current-main public regeneration.

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "senales-biomedicas"
GENERIC = "concepto de la unidad que debe definirse"


class SenalesBiomedicasCanonicalCourseTests(unittest.TestCase):
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

    def test_six_units_cover_all_course_outcomes_and_content_layers(self):
        self.assertEqual(len(self.course["unit_files"]), 6)
        known = {item["id"] for item in self.course["learning_outcomes"]}
        covered = set()
        topic_count = 0
        subtopic_count = 0
        for relative in self.course["unit_files"]:
            unit = json.loads((COURSE / relative).read_text(encoding="utf-8"))
            covered.update(unit["course_learning_outcome_ids"])
            self.assertNotIn(GENERIC, json.dumps(unit, ensure_ascii=False).casefold())
            self.assertEqual(unit["status"]["content"], "complete")
            self.assertEqual(unit["status"]["sources"], "traceable")
            self.assertEqual(unit["status"]["pedagogy"], "complete")
            self.assertGreaterEqual(len(unit["learning_outcomes"]), 6)
            self.assertEqual(len(unit["topics"]), 4)
            self.assertGreaterEqual(len(unit["examples"]), 5)
            self.assertGreaterEqual(len(unit["activities"]), 3)
            self.assertTrue(all(activity["estimated_duration_minutes"] > 0 for activity in unit["activities"]))
            topic_count += len(unit["topics"])
            subtopic_count += sum(len(topic["subtopics"]) for topic in unit["topics"])
        self.assertEqual(known, covered)
        self.assertEqual(topic_count, 24)
        self.assertGreaterEqual(subtopic_count, 96)

    def test_assessment_items_are_classified_feedback_rich_and_traceable(self):
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
        self.assertGreaterEqual(len(self.glossary["entries"]), 90)
        for entry in self.glossary["entries"]:
            self.assertTrue(entry["source_ids"])
            self.assertTrue(set(entry["source_ids"]) <= source_ids)
            self.assertNotEqual(entry["verification_status"], "unverified")
        self.assertEqual(len(self.claims["claims"]), 48)
        self.assertEqual(
            {claim["unit_id"] for claim in self.claims["claims"]},
            {f"SENBIO-U{i:02d}" for i in range(1, 7)},
        )
        for claim in self.claims["claims"]:
            self.assertIn(claim["source_id"], source_ids)
            self.assertEqual(claim["review_state"], "ai_review_provisional")
            self.assertIsNone(claim["reviewer_validation_id"])

    def test_core_sources_are_verified_and_cover_the_course(self):
        by_id = {item["id"]: item for item in self.sources["sources"]}
        self.assertGreaterEqual(len(self.course["core_source_ids"]), 12)
        for source_id in self.course["core_source_ids"]:
            self.assertIn(source_id, by_id)
            self.assertEqual(by_id[source_id]["verification_status"], "verified_directly")

    def test_course_assessment_integrates_all_six_units(self):
        assessment = json.loads((COURSE / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))
        self.assertEqual(sum(item["weight_percent"] for item in assessment["assessment_plan"]), 100)
        self.assertEqual(sum(item["weight_percent"] for item in assessment["midterm_blueprint"]), 100)
        self.assertEqual(sum(item["weight_percent"] for item in assessment["capstone"]["rubric"]), 100)
        self.assertGreaterEqual(len(assessment["diagnostic"]["questions"]), 12)
        self.assertGreaterEqual(len(assessment["capstone"]["required_deliverables"]), 8)
        self.assertEqual(assessment["status"], "complete")

    def test_curricular_boundaries_are_explicit(self):
        notice = self.course["editorial_notice"].casefold()
        excluded = " ".join(self.course["scope"]["excluded"]).casefold()
        self.assertIn("revisión disciplinaria externa", notice)
        self.assertIn("validación clínica", notice)
        self.assertIn("conformidad regulatoria", notice)
        self.assertIn("diagnóstico", excluded)
        self.assertIn("mecanismos fisiológicos causales", excluded)
        self.assertIn("reentrenar", excluded)


# Final user-authored verification trigger after canonical generation.
if __name__ == "__main__":
    unittest.main()
