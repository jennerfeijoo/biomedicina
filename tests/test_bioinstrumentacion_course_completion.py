from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "bioinstrumentacion"

# Final normal-user commit: the corpus below was already validated strictly and regenerated.


class BioinstrumentacionCourseCompletionTests(unittest.TestCase):
    def test_course_is_content_complete_but_human_review_remains_pending(self) -> None:
        course = json.loads((COURSE / "course.json").read_text(encoding="utf-8"))
        self.assertEqual(course["content_version"], "1.0.0")
        self.assertEqual(course["status"]["content"], "complete")
        self.assertEqual(course["status"]["pedagogy"], "complete")
        self.assertEqual(course["status"]["sources"], "traceable")
        self.assertEqual(course["status"]["internal_review"], "pending")
        self.assertEqual(course["status"]["external_review"], "pending")
        self.assertEqual(course["status"]["publication"], "published_provisional")
        notice = course["editorial_notice"].lower()
        self.assertIn("completo a nivel de contenido estructurado", notice)
        self.assertIn("revisión humana interna", notice)
        self.assertIn("revisión disciplinaria externa", notice)
        self.assertIn("validez clínica", notice)
        self.assertEqual(len(course["unit_files"]), 10)

    def test_all_ten_units_have_traceable_sources_and_pending_human_review(self) -> None:
        course = json.loads((COURSE / "course.json").read_text(encoding="utf-8"))
        for unit_file in course["unit_files"]:
            unit = json.loads((COURSE / unit_file).read_text(encoding="utf-8"))
            self.assertEqual(unit["status"]["sources"], "traceable")
            self.assertEqual(unit["status"]["internal_review"], "pending")
            self.assertEqual(unit["status"]["external_review"], "pending")
            self.assertEqual(unit["status"]["publication"], "published_provisional")
            self.assertTrue(unit["activities"])
            self.assertTrue(unit["claim_ids"])
            self.assertTrue(unit["glossary_entry_ids"])

    def test_course_assessment_covers_all_outcomes_and_weights_sum_to_100(self) -> None:
        course = json.loads((COURSE / "course.json").read_text(encoding="utf-8"))
        assessment = json.loads((COURSE / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))
        outcomes = {item["id"] for item in course["learning_outcomes"]}
        plan_outcomes = {outcome for item in assessment["assessment_plan"] for outcome in item["linked_learning_outcome_ids"]}
        self.assertEqual(assessment["status"], "curated_pending_expert_review")
        self.assertEqual(sum(item["weight_percent"] for item in assessment["assessment_plan"]), 100)
        self.assertEqual(plan_outcomes, outcomes)
        self.assertEqual(set(assessment["capstone"]["linked_learning_outcome_ids"]), outcomes)
        self.assertEqual(sum(item["weight_percent"] for item in assessment["capstone"]["rubric"]), 100)
        self.assertTrue(assessment["midterm_blueprint"])
        self.assertEqual(sum(item["weight_percent"] for item in assessment["midterm_blueprint"]), 100)
        midterm_outcomes = {outcome for item in assessment["midterm_blueprint"] for outcome in item["linked_learning_outcome_ids"]}
        self.assertEqual(midterm_outcomes, {"BIOINST-LO01", "BIOINST-LO02", "BIOINST-LO03", "BIOINST-LO04"})

    def test_capstone_is_auditable_and_does_not_claim_professional_approval(self) -> None:
        assessment = json.loads((COURSE / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))
        capstone = assessment["capstone"]
        self.assertEqual(len(capstone["deliverables"]), 8)
        names = " ".join(item["name"] + " " + item["description"] for item in capstone["deliverables"]).lower()
        for marker in ["arquitectura", "presupuestos", "incertidumbre", "riesgo", "baseline", "procedencia", "discrepancias", "defensa"]:
            self.assertIn(marker, names)
        serialized = json.dumps(assessment, ensure_ascii=False).lower()
        self.assertIn("no equivale a certificación", serialized)
        self.assertIn("validez clínica", serialized)
        self.assertIn("datos sintéticos", serialized)

    def test_completion_rules_are_academic_not_regulatory(self) -> None:
        assessment = json.loads((COURSE / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))
        rules = assessment["completion_rules"]
        self.assertEqual(rules["minimum_total_percent"], 60)
        self.assertEqual(rules["minimum_capstone_percent"], 60)
        self.assertGreaterEqual(len(rules["critical_failures"]), 4)
        self.assertIn("criterios académicos internos", rules["interpretation"].lower())
        self.assertIn("no estándares profesionales", rules["interpretation"].lower())

    def test_historical_glossary_gaps_are_now_traceable(self) -> None:
        glossary = json.loads((COURSE / "glossary.json").read_text(encoding="utf-8"))
        entries = {item["id"]: item for item in glossary["entries"]}
        resolved = {
            "BIOINST-GLO-049", "BIOINST-GLO-053", "BIOINST-GLO-055", "BIOINST-GLO-058",
            "BIOINST-GLO-072", "BIOINST-GLO-073", "BIOINST-GLO-074", "BIOINST-GLO-075",
            "BIOINST-GLO-076", "BIOINST-GLO-077", "BIOINST-GLO-083",
        }
        for entry_id in resolved:
            entry = entries[entry_id]
            self.assertNotEqual(entry["verification_status"], "unverified")
            self.assertTrue(entry["source_ids"])
            self.assertTrue(entry.get("source_locators"))
        self.assertEqual(entries["BIOINST-GLO-072"]["source_ids"], ["iupac-stray-light-2025"])


if __name__ == "__main__":
    unittest.main()
