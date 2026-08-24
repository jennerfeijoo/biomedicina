from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "comunicacion-cientifica"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class ComunicacionCientificaCanonicalCourseTests(unittest.TestCase):
    def test_course_has_six_canonical_units_and_complete_editorial_state(self) -> None:
        course = load(COURSE / "course.json")
        self.assertEqual(course["id"], "comunicacion-cientifica")
        self.assertEqual(len(course["unit_files"]), 6)
        self.assertEqual(course["status"]["content"], "complete")
        self.assertEqual(course["status"]["sources"], "traceable")
        self.assertEqual(course["status"]["pedagogy"], "complete")
        self.assertEqual(course["status"]["multimedia"], "planned")
        self.assertEqual(course["status"]["internal_review"], "pending")
        self.assertEqual(course["status"]["external_review"], "pending")
        self.assertTrue(course["static_site"]["canonical_source"])
        self.assertEqual(len(course["learning_outcomes"]), 7)

    def test_units_are_substantive_and_generic_template_is_absent(self) -> None:
        for number in range(1, 7):
            unit = load(COURSE / "units" / f"unit-{number:02d}.json")
            self.assertEqual(unit["order"], number)
            self.assertEqual(unit["status"]["content"], "complete")
            self.assertEqual(unit["status"]["sources"], "traceable")
            self.assertEqual(unit["status"]["pedagogy"], "complete")
            self.assertGreaterEqual(len(unit["learning_outcomes"]), 5)
            self.assertGreaterEqual(len(unit["topics"]), 4)
            self.assertGreaterEqual(len(unit["examples"]), 2)
            self.assertGreaterEqual(len(unit["activities"]), 1)
            self.assertGreaterEqual(len(unit["source_ids"]), 5)
            text = json.dumps(unit, ensure_ascii=False).casefold()
            self.assertNotIn(GENERIC, text)
            self.assertIn("COMCI-LO07".casefold(), text)

    def test_unit_assessments_are_complete_and_recover_errors(self) -> None:
        for number in range(1, 7):
            assessment = load(COURSE / "assessments" / f"unit-{number:02d}.json")
            self.assertEqual(assessment["status"], "complete")
            self.assertGreaterEqual(len(assessment["items"]), 10)
            for item in assessment["items"]:
                self.assertNotEqual(item["difficulty"], "unclassified")
                self.assertNotEqual(item["cognitive_level"], "unclassified")
                self.assertTrue(item["feedback"]["correct"])
                self.assertTrue(item["feedback"]["incorrect"])
                self.assertEqual(item["status"], "complete")

    def test_course_assessment_weights_and_capstone_are_complete(self) -> None:
        assessment = load(COURSE / "assessments" / "course-assessment.json")
        self.assertEqual(assessment["status"], "complete")
        self.assertEqual(sum(item["weight_percent"] for item in assessment["assessment_plan"]), 100)
        self.assertEqual(sum(item["weight_percent"] for item in assessment["midterm_blueprint"]), 100)
        capstone = assessment["capstone"]
        self.assertGreaterEqual(len(capstone["required_deliverables"]), 8)
        self.assertEqual(sum(item["weight_percent"] for item in capstone["rubric"]), 100)
        self.assertIn("CRediT", json.dumps(capstone, ensure_ascii=False))
        self.assertIn("version", json.dumps(capstone, ensure_ascii=False).casefold())

    def test_sources_glossary_claim_policy_and_media_are_future_proof(self) -> None:
        sources = load(COURSE / "sources.json")
        glossary = load(COURSE / "glossary.json")
        claims = load(COURSE / "claims.json")
        media = load(COURSE / "media.json")
        self.assertGreaterEqual(len(sources["sources"]), 20)
        self.assertEqual(sources["coverage_status"], "traceable")
        self.assertEqual(sources["coverage_gaps"], [])
        self.assertGreaterEqual(len(glossary["entries"]), 50)
        self.assertTrue(all(entry.get("unit_ids") for entry in glossary["entries"]))
        self.assertTrue(any(entry.get("source_ids") for entry in glossary["entries"]))
        self.assertEqual(claims["claims"], [])
        self.assertIn("no se autogeneran", claims["scope"].casefold())
        self.assertEqual(media["status"], "planned")

    def test_integrity_and_clinical_boundaries_remain_explicit(self) -> None:
        course = load(COURSE / "course.json")
        text = json.dumps(course, ensure_ascii=False).casefold()
        for phrase in (
            "asesoría jurídica",
            "personas reales",
            "validez clínica",
            "conformidad regulatoria",
            "revisión disciplinar humana externa",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
