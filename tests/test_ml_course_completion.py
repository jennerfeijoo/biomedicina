import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "machine-learning-biomedico-validacion-clinica"


class MachineLearningCourseCompletionTests(unittest.TestCase):
    def test_course_is_content_complete_but_human_review_remains_pending(self) -> None:
        course = json.loads((COURSE / "course.json").read_text(encoding="utf-8"))
        self.assertEqual(course["status"]["content"], "complete")
        self.assertEqual(course["status"]["pedagogy"], "complete")
        self.assertEqual(course["status"]["sources"], "traceable")
        self.assertEqual(course["status"]["internal_review"], "pending")
        self.assertEqual(course["status"]["external_review"], "pending")
        self.assertEqual(course["status"]["publication"], "published_provisional")
        self.assertTrue(course["scope"]["included"])
        self.assertTrue(course["scope"]["excluded"])
        self.assertTrue(course["scope"]["handoff_courses"])

    def test_course_assessment_covers_all_outcomes_and_weights_sum_to_100(self) -> None:
        course = json.loads((COURSE / "course.json").read_text(encoding="utf-8"))
        assessment = json.loads((COURSE / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))
        outcomes = {item["id"] for item in course["learning_outcomes"]}
        plan_outcomes = {outcome for item in assessment["assessment_plan"] for outcome in item["linked_learning_outcome_ids"]}
        self.assertEqual(assessment["status"], "curated_pending_expert_review")
        self.assertEqual(sum(item["weight_percent"] for item in assessment["assessment_plan"]), 100)
        self.assertEqual(plan_outcomes, outcomes)
        self.assertEqual(set(assessment["capstone"]["linked_learning_outcome_ids"]), outcomes)
        self.assertEqual(sum(item["weight_percent"] for item in assessment["capstone"]["rubric"]), 100)
        self.assertTrue(assessment["midterm_blueprint"])
        self.assertEqual(sum(item["weight_percent"] for item in assessment["midterm_blueprint"]), 100)

    def test_course_sources_have_no_consor_spirit_duplicate_ids(self) -> None:
        sources = json.loads((COURSE / "sources.json").read_text(encoding="utf-8"))["sources"]
        ids = [item["id"] for item in sources]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("consort-ai", ids)
        self.assertIn("spirit-ai", ids)
        self.assertNotIn("consort-ai-2020", ids)
        self.assertNotIn("spirit-ai-2020", ids)


if __name__ == "__main__":
    unittest.main()
