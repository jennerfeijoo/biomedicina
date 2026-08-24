from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "biomecanica-medios-continuos"
GENERIC = "concepto de la unidad que debe definirse"


class BiomecanicaMediosContinuosCanonicalTests(unittest.TestCase):
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

    def test_six_units_are_canonical_and_cover_all_course_outcomes(self):
        self.assertEqual(len(self.course["unit_files"]), 6)
        known = {item["id"] for item in self.course["learning_outcomes"]}
        covered = set()
        for number, relative in enumerate(self.course["unit_files"], start=1):
            unit = json.loads((COURSE / relative).read_text(encoding="utf-8"))
            self.assertEqual(unit["id"], f"BMCONT-U{number:02d}")
            self.assertNotIn(GENERIC, json.dumps(unit, ensure_ascii=False).casefold())
            self.assertEqual(unit["status"]["content"], "complete")
            self.assertEqual(unit["status"]["sources"], "traceable")
            self.assertEqual(unit["status"]["pedagogy"], "complete")
            self.assertTrue(unit["activities"])
            self.assertTrue(all(activity["estimated_duration_minutes"] > 0 for activity in unit["activities"]))
            covered.update(unit["course_learning_outcome_ids"])
        self.assertEqual(known, covered)

    def test_sources_glossary_and_claims_are_traceable(self):
        source_ids = {item["id"] for item in self.sources["sources"]}
        self.assertGreaterEqual(len(source_ids), 40)
        self.assertTrue(all(item.get("verification_status") not in (None, "", "unverified") for item in self.sources["sources"]))
        self.assertEqual(self.sources.get("coverage_gaps"), [])

        self.assertGreaterEqual(len(self.glossary["entries"]), 100)
        for entry in self.glossary["entries"]:
            self.assertTrue(entry["source_ids"])
            self.assertTrue(set(entry["source_ids"]) <= source_ids)
            self.assertNotEqual(entry["verification_status"], "unverified")

        self.assertEqual(len(self.claims["claims"]), 24)
        expected_units = {f"BMCONT-U{number:02d}" for number in range(1, 7)}
        self.assertEqual({claim["unit_id"] for claim in self.claims["claims"]}, expected_units)
        for unit_id in expected_units:
            unit_claims = [claim for claim in self.claims["claims"] if claim["unit_id"] == unit_id]
            self.assertEqual(len(unit_claims), 4)
            unit_number = int(unit_id[-2:])
            unit = json.loads((COURSE / "units" / f"unit-{unit_number:02d}.json").read_text(encoding="utf-8"))
            unit_text = json.dumps(unit, ensure_ascii=False)
            for claim in unit_claims:
                self.assertIn(claim["text"], unit_text)
                self.assertIn(claim["source_id"], source_ids)

    def test_unit_assessments_are_classified_traceable_and_recoverable(self):
        source_ids = {item["id"] for item in self.sources["sources"]}
        for number in range(1, 7):
            assessment = json.loads((COURSE / "assessments" / f"unit-{number:02d}.json").read_text(encoding="utf-8"))
            self.assertEqual(len(assessment["items"]), 10)
            for item in assessment["items"]:
                self.assertNotEqual(item["difficulty"], "unclassified")
                self.assertNotEqual(item["cognitive_level"], "unclassified")
                self.assertTrue(item["answer_key"]["explanation"])
                self.assertTrue(item["feedback"]["correct"])
                self.assertTrue(item["feedback"]["incorrect"])
                self.assertTrue(item["source_ids"])
                self.assertTrue(set(item["source_ids"]) <= source_ids)

    def test_course_assessment_integrates_all_six_units(self):
        assessment = json.loads((COURSE / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))
        self.assertEqual(sum(item["weight_percent"] for item in assessment["assessment_plan"]), 100)
        self.assertEqual(sum(item["weight_percent"] for item in assessment["midterm_blueprint"]), 100)
        self.assertEqual(sum(item["weight_percent"] for item in assessment["capstone"]["rubric"]), 100)
        self.assertGreaterEqual(len(assessment["diagnostic"]["questions"]), 12)
        self.assertGreaterEqual(len(assessment["capstone"]["deliverables"]), 7)

    def test_curricular_boundaries_are_explicit(self):
        text = json.dumps(self.course, ensure_ascii=False).casefold()
        for concept in (
            "cinemática de medios continuos",
            "esfuerzo y equilibrio",
            "hiperelasticidad",
            "viscoelasticidad",
            "poroelasticidad",
            "navier",
            "elementos finitos",
            "verificación",
            "validación",
            "incertidumbre",
        ):
            self.assertIn(concept, text)
        self.assertIn("validación clínica", self.course["editorial_notice"].casefold())
        self.assertIn("revisión humana", self.course["editorial_notice"].casefold())


if __name__ == "__main__":
    unittest.main()
