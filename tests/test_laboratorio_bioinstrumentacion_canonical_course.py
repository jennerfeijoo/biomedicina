from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_DIR = ROOT / "data" / "courses" / "laboratorio-bioinstrumentacion"
COURSE = COURSE_DIR / "course.json"


class LaboratorioBioinstrumentacionCanonicalCourseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.course = json.loads(COURSE.read_text(encoding="utf-8"))
        cls.units = [
            json.loads((COURSE_DIR / f"units/unit-{number:02d}.json").read_text(encoding="utf-8"))
            for number in range(1, 7)
        ]
        cls.assessment = json.loads((COURSE_DIR / "assessments/course-assessment.json").read_text(encoding="utf-8"))
        cls.glossary = json.loads((COURSE_DIR / "glossary.json").read_text(encoding="utf-8"))
        cls.sources = json.loads((COURSE_DIR / "sources.json").read_text(encoding="utf-8"))
        cls.claims = json.loads((COURSE_DIR / "claims.json").read_text(encoding="utf-8"))

    def test_course_is_complete_but_human_review_remains_pending(self) -> None:
        self.assertEqual(self.course["schema_version"], "1.0")
        self.assertEqual(self.course["code"], "LABBIO")
        status = self.course["status"]
        self.assertEqual(status["content"], "complete")
        self.assertEqual(status["sources"], "traceable")
        self.assertEqual(status["pedagogy"], "complete")
        self.assertEqual(status["multimedia"], "planned")
        self.assertEqual(status["internal_review"], "pending")
        self.assertEqual(status["external_review"], "pending")
        self.assertEqual(status["publication"], "published_provisional")

    def test_six_units_cover_the_full_lab_progression(self) -> None:
        self.assertEqual([unit["order"] for unit in self.units], [1, 2, 3, 4, 5, 6])
        corpus = " ".join(
            [self.course["purpose"]]
            + [unit["purpose"] for unit in self.units]
            + [topic["title"] for unit in self.units for topic in unit["topics"]]
        ).casefold()
        for concept in (
            "mensurando",
            "sensor",
            "front-end",
            "muestreo",
            "integr",
            "verific",
            "incertidumbre",
        ):
            self.assertIn(concept, corpus)
        self.assertNotIn("concepto de la unidad que debe definirse", corpus)

    def test_units_keep_complete_status_and_pedagogical_scaffolding(self) -> None:
        for unit in self.units:
            self.assertEqual(unit["status"]["content"], "complete")
            self.assertEqual(unit["status"]["sources"], "traceable")
            self.assertEqual(unit["status"]["pedagogy"], "complete")
            self.assertGreaterEqual(len(unit["topics"]), 4)
            self.assertGreaterEqual(len(unit["examples"]), 2)
            self.assertGreaterEqual(len(unit["activities"]), 1)
            self.assertTrue(all(activity["estimated_duration_minutes"] for activity in unit["activities"]))
            self.assertTrue(all(activity["deliverables"] for activity in unit["activities"]))
            self.assertTrue(unit["source_ids"])
            self.assertTrue(unit["claim_ids"])

    def test_course_assessment_is_complete_and_integrates_u1_to_u6(self) -> None:
        self.assertEqual(sum(item["weight_percent"] for item in self.assessment["assessment_plan"]), 100)
        self.assertEqual(sum(item["weight_percent"] for item in self.assessment["midterm_blueprint"]), 100)
        rubric = self.assessment["capstone"]["rubric"]
        self.assertEqual(sum(item["weight_percent"] for item in rubric), 100)
        capstone_text = json.dumps(self.assessment["capstone"], ensure_ascii=False).casefold()
        for label in ("u1", "u2", "u3", "u4", "u5", "u6"):
            self.assertIn(label, capstone_text)
        self.assertIn("no usar personas", capstone_text)
        self.assertEqual(self.assessment["status"], "curated_internal_review_pending")

    def test_all_unit_assessments_have_reasoning_feedback_and_sources(self) -> None:
        for number in range(1, 7):
            payload = json.loads((COURSE_DIR / f"assessments/unit-{number:02d}.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(len(payload["items"]), 8)
            for item in payload["items"]:
                self.assertNotEqual(item["difficulty"], "unclassified")
                self.assertNotEqual(item["cognitive_level"], "unclassified")
                self.assertTrue(item["answer_key"]["explanation"])
                self.assertTrue(item["feedback"]["correct"])
                self.assertTrue(item["feedback"]["incorrect"])
                self.assertTrue(item["source_ids"])

    def test_glossary_sources_and_claims_are_traceable(self) -> None:
        source_ids = {source["id"] for source in self.sources["sources"]}
        self.assertGreaterEqual(len(self.glossary["entries"]), 30)
        for entry in self.glossary["entries"]:
            self.assertTrue(entry["source_ids"])
            self.assertTrue(set(entry["source_ids"]).issubset(source_ids))
            self.assertNotEqual(entry["verification_status"], "unverified")
        self.assertGreaterEqual(len(self.claims["claims"]), 24)
        for claim in self.claims["claims"]:
            self.assertIn(claim["source_id"], source_ids)
            self.assertEqual(claim["review_state"], "ai_review_provisional")
            self.assertIsNone(claim["reviewer_validation_id"])

    def test_scope_does_not_claim_human_use_or_certification(self) -> None:
        excluded = " ".join(self.course["scope"]["excluded"]).casefold()
        notice = self.course["editorial_notice"].casefold()
        self.assertIn("personas", excluded)
        self.assertIn("validación clínica", excluded)
        self.assertIn("conformidad regulatoria", excluded)
        self.assertIn("revisión disciplinaria humana", notice)
        self.assertIn("no autoriza conexión a personas", notice)


if __name__ == "__main__":
    unittest.main()
