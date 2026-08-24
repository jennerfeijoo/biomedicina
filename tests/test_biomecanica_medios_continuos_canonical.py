from __future__ import annotations

# Final user-authored validation trigger after canonical corpus generation and public synchronization.

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "courses" / "biomecanica-medios-continuos"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomecanicaMediosContinuosCanonicalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.course = json.loads((BASE / "course.json").read_text(encoding="utf-8"))

    def test_course_complete_human_review_pending(self):
        status = self.course["status"]
        self.assertEqual(status["content"], "complete")
        self.assertEqual(status["sources"], "traceable")
        self.assertEqual(status["pedagogy"], "complete")
        self.assertEqual(status["multimedia"], "planned")
        self.assertEqual(status["internal_review"], "pending")
        self.assertEqual(status["external_review"], "pending")
        self.assertEqual(status["publication"], "published_provisional")

    def test_six_units_are_disciplinary_and_structured(self):
        expected = ["Descripción continua de tejidos", "Esfuerzo y equilibrio", "Elasticidad", "Viscoelasticidad y poroelasticidad", "Fluidos biológicos", "Elementos finitos y validación"]
        self.assertEqual(len(self.course["unit_files"]), 6)
        for n, relative in enumerate(self.course["unit_files"], 1):
            unit = json.loads((BASE / relative).read_text(encoding="utf-8"))
            self.assertEqual(unit["order"], n)
            self.assertEqual(unit["title"], expected[n-1])
            self.assertEqual(unit["status"]["content"], "complete")
            self.assertGreaterEqual(len(unit["learning_outcomes"]), 5)
            self.assertGreaterEqual(len(unit["topics"]), 4)
            self.assertGreaterEqual(len(unit["examples"]), 3)
            self.assertGreaterEqual(len(unit["activities"]), 1)
            self.assertGreaterEqual(len(unit["source_ids"]), 5)
            self.assertEqual(len(unit["claim_ids"]), 4)
            self.assertNotIn(GENERIC, json.dumps(unit, ensure_ascii=False).casefold())

    def test_registries_trace_every_unit(self):
        sources = json.loads((BASE / "sources.json").read_text(encoding="utf-8"))
        self.assertEqual(sources["coverage_gaps"], [])
        self.assertGreaterEqual(len(sources["sources"]), 30)
        self.assertTrue(all(s.get("verification_status") != "unverified" for s in sources["sources"]))
        glossary = json.loads((BASE / "glossary.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(glossary["entries"]), 70)
        self.assertTrue(all(e.get("source_ids") for e in glossary["entries"]))
        claims = json.loads((BASE / "claims.json").read_text(encoding="utf-8"))
        self.assertEqual(len(claims["claims"]), 24)
        by_unit = {}
        for claim in claims["claims"]:
            by_unit.setdefault(claim["unit_id"], []).append(claim)
            unit_n = int(claim["unit_id"].split("U")[-1])
            unit = json.loads((BASE / "units" / f"unit-{unit_n:02d}.json").read_text(encoding="utf-8"))
            self.assertIn(claim["text"], json.dumps(unit, ensure_ascii=False))
        self.assertTrue(all(len(v) == 4 for v in by_unit.values()))
        media = json.loads((BASE / "media.json").read_text(encoding="utf-8"))
        self.assertEqual(media["coverage_status"], "planned")
        self.assertEqual(len(media["items"]), 6)

    def test_unit_and_course_assessments_are_recoverable(self):
        for n in range(1, 7):
            assessment = json.loads((BASE / "assessments" / f"unit-{n:02d}.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(len(assessment["items"]), 8)
            self.assertTrue(all(i.get("answer_key", {}).get("explanation") for i in assessment["items"]))
            self.assertTrue(all(i.get("feedback", {}).get("incorrect") for i in assessment["items"]))
            self.assertTrue(all(i.get("source_ids") for i in assessment["items"]))
        assessment = json.loads((BASE / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))
        self.assertEqual(sum(x["weight_percent"] for x in assessment["assessment_plan"]), 100)
        self.assertEqual(sum(x["weight_percent"] for x in assessment["midterm_blueprint"]), 100)
        self.assertEqual(sum(x["weight_percent"] for x in assessment["capstone"]["rubric"]), 100)
        self.assertGreaterEqual(len(assessment["diagnostic"]["questions"]), 12)

    def test_all_course_outcomes_have_unit_coverage(self):
        mapped = set()
        for relative in self.course["unit_files"]:
            unit = json.loads((BASE / relative).read_text(encoding="utf-8"))
            mapped.update(unit["course_learning_outcome_ids"])
        self.assertEqual(mapped, {x["id"] for x in self.course["learning_outcomes"]})

    def test_boundaries_are_explicit(self):
        notice = self.course["editorial_notice"].casefold()
        for phrase in ("revisión humana", "validación clínica", "certificación", "aprobación regulatoria"):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
