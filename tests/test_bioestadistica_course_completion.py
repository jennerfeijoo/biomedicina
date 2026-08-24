from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "bioestadistica"


class BioestadisticaCourseCompletionTests(unittest.TestCase):
    def test_course_is_complete_but_human_review_remains_pending(self) -> None:
        course = json.loads((COURSE / "course.json").read_text(encoding="utf-8"))
        self.assertEqual(course["content_version"], "1.0.0")
        self.assertEqual(course["status"]["content"], "complete")
        self.assertEqual(course["status"]["pedagogy"], "complete")
        self.assertEqual(course["status"]["sources"], "traceable")
        self.assertEqual(course["status"]["multimedia"], "planned")
        self.assertEqual(course["status"]["internal_review"], "pending")
        self.assertEqual(course["status"]["external_review"], "pending")
        self.assertEqual(course["status"]["publication"], "published_provisional")
        self.assertEqual(len(course["unit_files"]), 8)
        notice = course["editorial_notice"].lower()
        self.assertIn("completo a nivel de contenido estructurado", notice)
        self.assertIn("revisión humana interna", notice)
        self.assertIn("revisión académica externa", notice)
        self.assertIn("no sustituyen asesoría bioestadística", notice)

    def test_course_assessment_is_complete_and_covers_all_outcomes(self) -> None:
        course = json.loads((COURSE / "course.json").read_text(encoding="utf-8"))
        assessment = json.loads((COURSE / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))
        outcomes = {item["id"] for item in course["learning_outcomes"]}
        plan_outcomes = {oid for item in assessment["assessment_plan"] for oid in item["linked_learning_outcome_ids"]}
        self.assertEqual(assessment["status"], "curated_pending_expert_review")
        self.assertEqual(sum(item["weight_percent"] for item in assessment["assessment_plan"]), 100)
        self.assertEqual(plan_outcomes, outcomes)
        self.assertEqual(set(assessment["capstone"]["linked_learning_outcome_ids"]), outcomes)
        self.assertTrue(assessment["midterm_blueprint"])
        self.assertEqual(sum(item["weight_percent"] for item in assessment["midterm_blueprint"]), 100)
        rubric = assessment["capstone"]["rubric"]
        self.assertEqual(sum(item["weight_percent"] for item in rubric), 100)
        self.assertGreaterEqual(len(assessment["capstone"]["deliverables"]), 8)
        for item in rubric:
            for level in ("excellent", "competent", "developing", "insufficient"):
                self.assertTrue(item[level])

    def test_all_units_keep_expert_review_pending_and_traceable_sources(self) -> None:
        course = json.loads((COURSE / "course.json").read_text(encoding="utf-8"))
        for relative in course["unit_files"]:
            unit = json.loads((COURSE / relative).read_text(encoding="utf-8"))
            self.assertEqual(unit["status"]["sources"], "traceable")
            self.assertEqual(unit["status"]["internal_review"], "pending")
            self.assertEqual(unit["status"]["external_review"], "pending")
            self.assertEqual(unit["status"]["publication"], "published_provisional")
            self.assertTrue(unit["activities"])
            self.assertTrue(unit["claim_ids"])

    def test_completion_does_not_become_clinical_or_expert_validation(self) -> None:
        course = json.loads((COURSE / "course.json").read_text(encoding="utf-8"))
        assessment = json.loads((COURSE / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))
        text = (json.dumps(course, ensure_ascii=False) + json.dumps(assessment, ensure_ascii=False)).lower()
        self.assertIn("no constituyen recomendaciones clínicas", text)
        self.assertIn("external_review", json.dumps(course, ensure_ascii=False))
        self.assertNotIn("validado por expertos", text)
        self.assertNotIn("aprobado para decisiones clínicas", text)


if __name__ == "__main__":
    unittest.main()
