# User-authored CI trigger after canonical corpus generation.
from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "laboratorio-bioinstrumentacion"
GENERIC = "concepto de la unidad que debe definirse"


class LaboratorioBioinstrumentacionCanonicalCourseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.course = json.loads((COURSE / "course.json").read_text(encoding="utf-8"))
        cls.sources = json.loads((COURSE / "sources.json").read_text(encoding="utf-8"))
        cls.glossary = json.loads((COURSE / "glossary.json").read_text(encoding="utf-8"))
        cls.claims = json.loads((COURSE / "claims.json").read_text(encoding="utf-8"))
        cls.media = json.loads((COURSE / "media.json").read_text(encoding="utf-8"))

    def test_status_closes_content_but_not_human_review(self):
        status = self.course["status"]
        self.assertEqual(status["content"], "complete")
        self.assertEqual(status["sources"], "traceable")
        self.assertEqual(status["pedagogy"], "complete")
        self.assertEqual(status["multimedia"], "planned")
        self.assertEqual(status["internal_review"], "pending")
        self.assertEqual(status["external_review"], "pending")
        self.assertEqual(status["publication"], "published_provisional")

    def test_six_units_are_complete_and_cover_course_outcomes(self):
        self.assertEqual(len(self.course["unit_files"]), 6)
        known = {item["id"] for item in self.course["learning_outcomes"]}
        self.assertEqual(len(known), 7)
        covered = set()
        for n, relative in enumerate(self.course["unit_files"], 1):
            unit = json.loads((COURSE / relative).read_text(encoding="utf-8"))
            covered.update(unit["course_learning_outcome_ids"])
            text = json.dumps(unit, ensure_ascii=False).casefold()
            self.assertNotIn(GENERIC, text)
            self.assertEqual(unit["id"], f"LBI-U{n:02d}")
            self.assertGreaterEqual(len(unit["topics"]), 4)
            self.assertGreaterEqual(len(unit["examples"]), 5)
            self.assertEqual(len(unit["activities"]), 3)
            self.assertTrue(all(a["estimated_duration_minutes"] > 0 for a in unit["activities"]))
            self.assertTrue(all(a["status"] == "complete" for a in unit["activities"]))
            self.assertEqual(unit["status"]["content"], "complete")
            self.assertEqual(unit["status"]["sources"], "traceable")
            self.assertEqual(unit["status"]["pedagogy"], "complete")
        self.assertEqual(known, covered)

    def test_assessments_have_recovery_feedback_and_sources(self):
        source_ids = {item["id"] for item in self.sources["sources"]}
        total = 0
        for n in range(1, 7):
            assessment = json.loads((COURSE / "assessments" / f"unit-{n:02d}.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(len(assessment["items"]), 10)
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
        self.assertGreaterEqual(total, 60)

    def test_sources_glossary_claims_and_media_are_structured(self):
        source_ids = {item["id"] for item in self.sources["sources"]}
        self.assertGreaterEqual(len(source_ids), 20)
        self.assertTrue(all(item["verification_status"] == "verified_directly" for item in self.sources["sources"]))
        self.assertEqual(self.sources["coverage_gaps"], [])
        self.assertGreaterEqual(len(self.glossary["entries"]), 60)
        for entry in self.glossary["entries"]:
            self.assertTrue(entry["source_ids"])
            self.assertTrue(set(entry["source_ids"]) <= source_ids)
            self.assertEqual(entry["verification_status"], "traceable_to_verified_source")
        claims = self.claims["claims"]
        self.assertEqual(len(claims), 24)
        self.assertEqual(Counter(c["unit"] for c in claims), Counter({n: 4 for n in range(1, 7)}))
        serialized_units = {n: json.dumps(json.loads((COURSE / "units" / f"unit-{n:02d}.json").read_text(encoding="utf-8")), ensure_ascii=False) for n in range(1, 7)}
        for claim in claims:
            self.assertIn(claim["source_id"], source_ids)
            self.assertEqual(claim["source_verification_status"], "verified_directly")
            self.assertEqual(claim["review_state"], "ai_review_provisional")
            self.assertEqual(claim["support"], "direct")
            self.assertIn(claim["text"], serialized_units[claim["unit"]])
        self.assertEqual(len(self.media["items"]), 6)
        self.assertTrue(all(item["status"] == "planned" for item in self.media["items"]))

    def test_course_assessment_is_integrative_and_weighted(self):
        assessment = json.loads((COURSE / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))
        self.assertEqual(sum(x["weight_percent"] for x in assessment["assessment_plan"]), 100)
        self.assertEqual(sum(x["weight_percent"] for x in assessment["midterm_blueprint"]), 100)
        self.assertEqual(sum(x["weight_percent"] for x in assessment["capstone"]["rubric"]), 100)
        self.assertGreaterEqual(len(assessment["diagnostic"]["questions"]), 12)
        self.assertGreaterEqual(len(assessment["capstone"]["required_deliverables"]), 12)
        self.assertEqual(assessment["status"], "complete")

    def test_course_scope_and_progression_are_explicit(self):
        purpose = self.course["purpose"].casefold()
        notice = self.course["editorial_notice"].casefold()
        for concept in ("seguridad", "metrología", "sensores", "amplificación", "filtrado", "adquisición", "hardware/firmware", "verificación"):
            self.assertIn(concept, purpose)
        for concept in ("revisión humana", "conexión a personas", "red eléctrica", "seguridad eléctrica", "emc", "validación fisiológica o clínica", "conformidad iec"):
            self.assertIn(concept, notice)
        u5 = json.loads((COURSE / "units" / "unit-05.json").read_text(encoding="utf-8"))
        u6 = json.loads((COURSE / "units" / "unit-06.json").read_text(encoding="utf-8"))
        self.assertIn("baseline", json.dumps(u5, ensure_ascii=False).casefold())
        self.assertIn("verificación y validación no son sinónimos", json.dumps(u6, ensure_ascii=False).casefold())


if __name__ == "__main__":
    unittest.main()
