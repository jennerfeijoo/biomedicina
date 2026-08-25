from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "economia-gestion-empresas"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"
# Final user-authored validation trigger after canonical closure synchronization.

class EconomiaGestionCanonicalCourseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.course = json.loads((COURSE / "course.json").read_text(encoding="utf-8"))
        cls.units = [json.loads((COURSE / f"units/unit-{i:02d}.json").read_text(encoding="utf-8")) for i in range(1, 7)]
        cls.sources = json.loads((COURSE / "sources.json").read_text(encoding="utf-8"))
        cls.glossary = json.loads((COURSE / "glossary.json").read_text(encoding="utf-8"))
        cls.claims = json.loads((COURSE / "claims.json").read_text(encoding="utf-8"))
        cls.assessment = json.loads((COURSE / "assessments/course-assessment.json").read_text(encoding="utf-8"))

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

    def test_units_preserve_substantive_content_and_no_template(self):
        text = " ".join(json.dumps(u, ensure_ascii=False) for u in self.units).casefold()
        self.assertNotIn(GENERIC, text)
        self.assertTrue(all(len(u["topics"]) >= 4 for u in self.units))
        self.assertTrue(all(len(u["examples"]) >= 3 for u in self.units))
        self.assertTrue(all(len(u["activities"]) >= 1 for u in self.units))
        self.assertGreaterEqual(len(self.units[5]["activities"]), 3)

    def test_registries_are_substantive_and_traceable(self):
        self.assertGreaterEqual(len(self.sources["sources"]), 30)
        self.assertGreaterEqual(len(self.glossary["entries"]), 80)
        self.assertEqual(len(self.claims["claims"]), 24)
        source_ids = {s["id"] for s in self.sources["sources"]}
        counts = Counter(c["unit_id"] for c in self.claims["claims"])
        for u in self.units:
            self.assertEqual(counts[u["id"]], 4)
            canonical_text = json.dumps(u, ensure_ascii=False)
            for claim in [c for c in self.claims["claims"] if c["unit_id"] == u["id"]]:
                self.assertIn(claim["text"], canonical_text)
                self.assertIn(claim["source_id"], source_ids)

    def test_unit_assessments_have_reasoning_and_feedback(self):
        for i, unit in enumerate(self.units, 1):
            payload = json.loads((COURSE / f"assessments/unit-{i:02d}.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(len(payload["items"]), 8)
            self.assertTrue(all(item["answer_key"]["explanation"] for item in payload["items"]))
            self.assertTrue(all(item["feedback"]["incorrect"] for item in payload["items"]))

    def test_course_assessment_covers_all_outcomes_and_weights(self):
        self.assertEqual(sum(x["weight_percent"] for x in self.assessment["assessment_plan"]), 100)
        self.assertEqual(sum(x["weight_percent"] for x in self.assessment["midterm_blueprint"]), 100)
        self.assertEqual(sum(x["weight_percent"] for x in self.assessment["capstone"]["rubric"]), 100)
        all_los = {x["id"] for x in self.course["learning_outcomes"]}
        covered = {lo for item in self.assessment["assessment_plan"] for lo in item.get("linked_learning_outcome_ids", [])}
        self.assertEqual(all_los, covered)
        self.assertGreaterEqual(len(self.assessment["diagnostic"]["questions"]), 10)
        self.assertGreaterEqual(len(self.assessment["capstone"]["deliverables"]), 8)

if __name__ == "__main__":
    unittest.main()
