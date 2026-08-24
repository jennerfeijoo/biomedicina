from __future__ import annotations

# Final user-authored CI trigger after canonical generation and public synchronization.

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_DIR = ROOT / "data" / "courses" / "biomateriales"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class BiomaterialesCanonicalCourseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.course = load(COURSE_DIR / "course.json")
        cls.units = [load(COURSE_DIR / "units" / f"unit-{i:02d}.json") for i in range(1, 7)]
        cls.sources = load(COURSE_DIR / "sources.json")
        cls.glossary = load(COURSE_DIR / "glossary.json")
        cls.claims = load(COURSE_DIR / "claims.json")
        cls.media = load(COURSE_DIR / "media.json")
        cls.assessments = [load(COURSE_DIR / "assessments" / f"unit-{i:02d}.json") for i in range(1, 7)]
        cls.course_assessment = load(COURSE_DIR / "assessments" / "course-assessment.json")

    def test_course_is_complete_but_human_review_pending(self):
        status = self.course["status"]
        self.assertEqual(status["content"], "complete")
        self.assertEqual(status["sources"], "traceable")
        self.assertEqual(status["pedagogy"], "complete")
        self.assertEqual(status["multimedia"], "planned")
        self.assertEqual(status["internal_review"], "pending")
        self.assertEqual(status["external_review"], "pending")
        self.assertEqual(status["publication"], "published_provisional")
        self.assertEqual(len(self.course["unit_files"]), 6)
        self.assertEqual(len(self.course["learning_outcomes"]), 7)

    def test_units_preserve_disciplinary_depth_and_no_template(self):
        text = " ".join(json.dumps(unit, ensure_ascii=False) for unit in self.units).casefold()
        self.assertNotIn(GENERIC, text)
        self.assertTrue(all(len(unit["learning_outcomes"]) >= 6 for unit in self.units))
        self.assertTrue(all(len(unit["topics"]) >= 4 for unit in self.units))
        self.assertTrue(all(len(unit["examples"]) >= 5 for unit in self.units))
        self.assertTrue(all(len(unit["activities"]) >= 1 for unit in self.units))
        self.assertTrue(all(unit["status"]["external_review"] == "pending" for unit in self.units))

    def test_assessments_are_classified_and_traceable(self):
        total = 0
        for unit, assessment in zip(self.units, self.assessments):
            self.assertEqual(assessment["unit_id"], unit["id"])
            self.assertGreaterEqual(len(assessment["items"]), 10)
            for item in assessment["items"]:
                self.assertNotEqual(item["difficulty"], "unclassified")
                self.assertNotEqual(item["cognitive_level"], "unclassified")
                self.assertTrue(item["answer_key"]["explanation"])
                self.assertTrue(item["feedback"]["correct"])
                self.assertTrue(item["feedback"]["incorrect"])
                self.assertTrue(item["source_ids"])
            total += len(assessment["items"])
        self.assertGreaterEqual(total, 60)

    def test_glossary_sources_claims_and_media_are_linked(self):
        self.assertGreaterEqual(len(self.glossary["entries"]), 80)
        source_ids = {item["id"] for item in self.sources["sources"]}
        self.assertGreaterEqual(len(source_ids), 30)
        self.assertTrue(all(item.get("verification_status") for item in self.sources["sources"]))
        self.assertEqual(len(self.claims["claims"]), 24)
        units_by_id = {unit["id"]: json.dumps(unit, ensure_ascii=False) for unit in self.units}
        for claim in self.claims["claims"]:
            self.assertIn(claim["source_id"], source_ids)
            self.assertIn(claim["text"], units_by_id[claim["unit_id"]])
            self.assertIsNone(claim["reviewer_validation_id"])
        self.assertEqual(len(self.media["items"]), 6)
        self.assertTrue(all(item["status"] == "planned" for item in self.media["items"]))

    def test_course_assessment_weights_are_complete(self):
        self.assertEqual(sum(item["weight_percent"] for item in self.course_assessment["assessment_plan"]), 100)
        self.assertEqual(sum(item["weight_percent"] for item in self.course_assessment["midterm_blueprint"]), 100)
        self.assertEqual(sum(item["weight_percent"] for item in self.course_assessment["capstone"]["rubric"]), 100)
        self.assertGreaterEqual(len(self.course_assessment["diagnostic"]["questions"]), 6)

    def test_curricular_boundaries_remain_explicit(self):
        course_text = json.dumps(self.course, ensure_ascii=False).casefold()
        self.assertIn("biomateriales-implantes", course_text)
        self.assertIn("evaluación de conformidad", course_text)
        self.assertIn("validación preclínica o clínica", course_text)
        u6 = json.dumps(self.units[5], ensure_ascii=False).casefold()
        self.assertIn("iso 10993-1:2025", u6)
        self.assertIn("iso 11135:2014", u6)
        self.assertIn("fdis", u6)


if __name__ == "__main__":
    unittest.main()
