from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_ROOT = ROOT / "data" / "courses" / "biofotonica"
GENERIC = "concepto de la unidad que debe definirse"


def load(relative: str) -> dict:
    return json.loads((COURSE_ROOT / relative).read_text(encoding="utf-8"))


class BiofotonicaCanonicalCourseTests(unittest.TestCase):
    def test_course_is_complete_without_faking_human_review(self) -> None:
        course = load("course.json")
        self.assertEqual(course["code"], "BIOFOT")
        self.assertEqual(course["content_version"], "1.0.0")
        self.assertEqual(course["status"]["content"], "complete")
        self.assertEqual(course["status"]["sources"], "traceable")
        self.assertEqual(course["status"]["pedagogy"], "complete")
        self.assertEqual(course["status"]["multimedia"], "planned")
        self.assertEqual(course["status"]["internal_review"], "pending")
        self.assertEqual(course["status"]["external_review"], "pending")
        self.assertEqual(course["status"]["publication"], "published_provisional")
        self.assertTrue(course["static_site"]["canonical_source"])
        self.assertEqual(len(course["unit_files"]), 6)
        self.assertEqual(len(course["learning_outcomes"]), 7)

    def test_six_units_are_disciplinary_and_structured(self) -> None:
        expected_titles = [
            "Interacción luz-tejido",
            "Fuentes y detectores",
            "Óptica de tejidos",
            "Microscopía y espectroscopía",
            "Fototerapia y dosimetría",
            "Validación y traslación",
        ]
        for number, title in enumerate(expected_titles, 1):
            unit = load(f"units/unit-{number:02d}.json")
            self.assertEqual(unit["order"], number)
            self.assertEqual(unit["title"], title)
            self.assertEqual(unit["status"]["content"], "complete")
            self.assertEqual(unit["status"]["sources"], "traceable")
            self.assertEqual(unit["status"]["pedagogy"], "complete")
            self.assertEqual(unit["status"]["external_review"], "pending")
            text = json.dumps(unit, ensure_ascii=False).casefold()
            self.assertNotIn(GENERIC, text)
            self.assertGreaterEqual(len(unit["topics"]), 4)
            self.assertTrue(all(topic["subtopics"] for topic in unit["topics"]))
            self.assertGreaterEqual(len(unit["examples"]), 2)
            self.assertGreaterEqual(len(unit["activities"]), 1)
            self.assertTrue(all(activity["estimated_duration_minutes"] == 90 for activity in unit["activities"]))
            self.assertTrue(all(activity["status"] == "complete" for activity in unit["activities"]))
            self.assertGreaterEqual(len(unit["common_errors"]), 5)
            self.assertGreaterEqual(len(unit["source_ids"]), 5)
            self.assertIn("BIOFOT-LO07", unit["course_learning_outcome_ids"])

    def test_unit_assessments_have_feedback_classification_and_sources(self) -> None:
        for number in range(1, 7):
            assessment = load(f"assessments/unit-{number:02d}.json")
            self.assertEqual(assessment["status"], "complete")
            self.assertGreaterEqual(len(assessment["items"]), 8)
            for item in assessment["items"]:
                self.assertNotEqual(item["difficulty"], "unclassified")
                self.assertNotEqual(item["cognitive_level"], "unclassified")
                self.assertTrue(item["feedback"]["correct"])
                self.assertTrue(item["feedback"]["incorrect"])
                self.assertTrue(item["answer_key"]["expected_answer"])
                self.assertTrue(item["answer_key"]["explanation"])
                self.assertTrue(item["source_ids"])
                self.assertEqual(item["status"], "complete")

    def test_registries_resolve_all_unit_references(self) -> None:
        glossary = load("glossary.json")
        sources = load("sources.json")
        claims = load("claims.json")
        media = load("media.json")
        glossary_ids = {item["id"] for item in glossary["entries"]}
        source_ids = {item["id"] for item in sources["sources"]}
        claim_ids = {item["id"] for item in claims["claims"]}
        media_ids = {item["id"] for item in media["items"]}
        self.assertGreaterEqual(len(glossary_ids), 30)
        self.assertGreaterEqual(len(source_ids), 20)
        self.assertEqual(sources["coverage_gaps"], [])
        self.assertEqual(sources["status"], "traceable")
        self.assertEqual(media["coverage_status"], "planned")
        self.assertEqual(claims["review_state"], "pending_human_claim_mapping")
        for number in range(1, 7):
            unit = load(f"units/unit-{number:02d}.json")
            self.assertTrue(set(unit["glossary_entry_ids"]) <= glossary_ids)
            self.assertTrue(set(unit["source_ids"]) <= source_ids)
            self.assertTrue(set(unit["claim_ids"]) <= claim_ids)
            self.assertTrue(set(unit["media_ids"]) <= media_ids)

    def test_course_assessment_is_integrative_and_weighted(self) -> None:
        assessment = load("assessments/course-assessment.json")
        self.assertEqual(assessment["status"], "complete")
        self.assertEqual(sum(x["weight_percent"] for x in assessment["assessment_plan"]), 100)
        self.assertEqual(sum(x["weight_percent"] for x in assessment["midterm_blueprint"]), 100)
        self.assertEqual(sum(x["weight_percent"] for x in assessment["capstone"]["rubric"]), 100)
        self.assertGreaterEqual(len(assessment["diagnostic"]["questions"]), 10)
        self.assertGreaterEqual(len(assessment["capstone"]["required_deliverables"]), 8)
        capstone = json.dumps(assessment["capstone"], ensure_ascii=False).casefold()
        for concept in ("luz-tejido", "fuente", "detector", "fantomas", "incertidumbre", "riesgo", "clínico", "regulatorio"):
            self.assertIn(concept, capstone)

    def test_editorial_boundaries_prohibit_overclaiming(self) -> None:
        course = load("course.json")
        notice = course["editorial_notice"].casefold()
        excluded = " ".join(course["scope"]["excluded"]).casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("validación clínica", notice)
        self.assertIn("personas o animales", excluded)
        self.assertIn("conformidad regulatoria", excluded)


if __name__ == "__main__":
    unittest.main()
