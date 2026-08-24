from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "courses" / "biomateriales-implantes"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomaterialesImplantesCanonicalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.course = json.loads((BASE / "course.json").read_text(encoding="utf-8"))

    def test_course_is_complete_but_human_review_remains_pending(self):
        status = self.course["status"]
        self.assertEqual(status["content"], "complete")
        self.assertEqual(status["sources"], "traceable")
        self.assertEqual(status["pedagogy"], "complete")
        self.assertEqual(status["internal_review"], "pending")
        self.assertEqual(status["external_review"], "pending")
        self.assertEqual(status["publication"], "published_provisional")

    def test_six_units_are_canonical_and_disciplinary(self):
        self.assertEqual(len(self.course["unit_files"]), 6)
        for index, relative in enumerate(self.course["unit_files"], 1):
            unit = json.loads((BASE / relative).read_text(encoding="utf-8"))
            self.assertEqual(unit["order"], index)
            self.assertEqual(unit["status"]["content"], "complete")
            self.assertEqual(unit["status"]["sources"], "traceable")
            self.assertEqual(unit["status"]["pedagogy"], "complete")
            text = json.dumps(unit, ensure_ascii=False).casefold()
            self.assertNotIn(GENERIC, text)
            self.assertGreaterEqual(len(unit["learning_outcomes"]), 5)
            self.assertGreaterEqual(len(unit["topics"]), 4)
            self.assertGreaterEqual(len(unit["examples"]), 2)
            self.assertGreaterEqual(len(unit["activities"]), 1)
            self.assertGreaterEqual(len(unit["source_ids"]), 5)

    def test_assessments_glossary_sources_and_media_exist(self):
        for relative in self.course["assessment_files"]:
            self.assertTrue((BASE / relative).exists(), relative)
        assessment = json.loads((BASE / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))
        self.assertEqual(sum(item["weight_percent"] for item in assessment["assessment_plan"]), 100)
        self.assertGreaterEqual(len(assessment["diagnostic"]["questions"]), 10)
        self.assertGreaterEqual(len(assessment["midterm_blueprint"]), 4)
        self.assertGreaterEqual(len(assessment["capstone"].get("rubric", [])), 5)
        glossary = json.loads((BASE / "glossary.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(glossary["entries"]), 30)
        self.assertTrue(all(entry.get("source_ids") for entry in glossary["entries"]))
        sources = json.loads((BASE / "sources.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(sources["sources"]), 12)
        self.assertEqual(sources["coverage_gaps"], [])
        media = json.loads((BASE / "media.json").read_text(encoding="utf-8"))
        self.assertEqual(media["coverage_status"], "planned")
        self.assertEqual(len(media["items"]), 6)

    def test_course_outcomes_cover_the_full_sequence(self):
        self.assertEqual(len(self.course["learning_outcomes"]), 7)
        mapped = set()
        for relative in self.course["unit_files"]:
            unit = json.loads((BASE / relative).read_text(encoding="utf-8"))
            mapped.update(unit["course_learning_outcome_ids"])
        self.assertEqual(mapped, {item["id"] for item in self.course["learning_outcomes"]})


if __name__ == "__main__":
    unittest.main()
