from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


VALIDATOR = load_module("validate_academic_courses", "scripts/validate_academic_courses.py")
RENDERER = load_module("advanced_unit_renderer", "scripts/advanced_unit_renderer.py")


class AcademicCourseSchemaTests(unittest.TestCase):
    def test_bioestadistica_canonical_course_is_structurally_valid(self) -> None:
        report = VALIDATOR.validate_course_directory(ROOT / "data" / "courses" / "bioestadistica")
        self.assertEqual(report.errors, [])
        self.assertEqual(report.counts["units"], 8)
        self.assertEqual(report.counts["assessment_items"], 64)

    def test_machine_learning_canonical_course_is_structurally_valid(self) -> None:
        report = VALIDATOR.validate_course_directory(
            ROOT / "data" / "courses" / "machine-learning-biomedico-validacion-clinica"
        )
        self.assertEqual(report.errors, [])
        self.assertEqual(report.counts["units"], 8)
        self.assertEqual(report.counts["topics"], 32)
        self.assertEqual(report.counts["assessment_items"], 64)
        self.assertTrue(any("sin afirmaciones centrales trazadas" in gap for gap in report.gaps))
        self.assertFalse(any("estado de verificación no declarado" in gap for gap in report.gaps))

    def test_renderer_prefers_the_canonical_unit(self) -> None:
        unit = RENDERER.load_advanced_unit(ROOT, "bioestadistica", 1)
        self.assertIsNotNone(unit)
        assert unit is not None
        self.assertEqual(unit["schema_version"], "canonical-1.0")
        self.assertEqual(unit["unit"], 1)
        self.assertEqual(unit["title"], "Preguntas, datos y diseños biomédicos")
        self.assertTrue(unit["theory_sections"][0]["paragraphs"])
        self.assertEqual(len(unit["self_assessment"]), 8)

    def test_renderer_prefers_the_machine_learning_canonical_unit(self) -> None:
        unit = RENDERER.load_advanced_unit(
            ROOT, "machine-learning-biomedico-validacion-clinica", 1
        )
        self.assertIsNotNone(unit)
        assert unit is not None
        self.assertEqual(unit["schema_version"], "canonical-1.0")
        self.assertEqual(unit["unit"], 1)
        self.assertEqual(unit["title"], "Pregunta clínica, uso previsto y estimando predictivo")
        self.assertTrue(unit["theory_sections"][0]["paragraphs"])
        self.assertEqual(len(unit["theory_sections"][0]["key_points"]), 4)
        self.assertTrue(unit["theory_sections"][0]["equations"][0]["label"])
        self.assertEqual(len(unit["self_assessment"]), 8)

    def test_every_assessment_item_maps_to_a_unit_outcome(self) -> None:
        course_dir = ROOT / "data" / "courses" / "bioestadistica"
        for unit_path in sorted((course_dir / "units").glob("unit-*.json")):
            unit = json.loads(unit_path.read_text(encoding="utf-8"))
            outcomes = {item["id"] for item in unit["learning_outcomes"]}
            assessment = json.loads((course_dir / unit["assessment_file"]).read_text(encoding="utf-8"))
            self.assertEqual(assessment["unit_id"], unit["id"])
            for item in assessment["items"]:
                self.assertTrue(set(item["linked_learning_outcome_ids"]).issubset(outcomes))

    def test_course_assessment_covers_all_outcomes_and_has_a_complete_rubric(self) -> None:
        course_dir = ROOT / "data" / "courses" / "bioestadistica"
        course = json.loads((course_dir / "course.json").read_text(encoding="utf-8"))
        assessment = json.loads(
            (course_dir / "assessments" / "course-assessment.json").read_text(encoding="utf-8")
        )
        outcomes = {item["id"] for item in course["learning_outcomes"]}
        sources = {
            item["id"]
            for item in json.loads((course_dir / "sources.json").read_text(encoding="utf-8"))["sources"]
        }

        self.assertEqual(assessment["status"], "curated_pending_expert_review")
        self.assertEqual(sum(item["weight_percent"] for item in assessment["assessment_plan"]), 100)
        self.assertEqual(
            {outcome for item in assessment["assessment_plan"] for outcome in item["linked_learning_outcome_ids"]},
            outcomes,
        )
        self.assertEqual(sum(item["weight_percent"] for item in assessment["midterm_blueprint"]), 100)
        self.assertEqual(
            {outcome for item in assessment["midterm_blueprint"] for outcome in item["linked_learning_outcome_ids"]},
            {"BIOEST-LO01", "BIOEST-LO02", "BIOEST-LO03", "BIOEST-LO04"},
        )

        capstone = assessment["capstone"]
        rubric = capstone["rubric"]
        rubric_ids = {item["id"] for item in rubric}
        self.assertEqual(sum(item["weight_percent"] for item in rubric), 100)
        self.assertEqual(
            {outcome for item in capstone["phases"] for outcome in item["linked_learning_outcome_ids"]},
            outcomes,
        )
        self.assertEqual(
            {outcome for item in capstone["deliverables"] for outcome in item["linked_learning_outcome_ids"]},
            outcomes,
        )
        for criterion in rubric:
            self.assertTrue({"excellent", "competent", "developing", "insufficient"}.issubset(criterion))
            self.assertTrue(set(criterion["linked_learning_outcome_ids"]).issubset(outcomes))
        self.assertTrue(set(capstone["completion_rule"]["essential_criterion_ids"]).issubset(rubric_ids))
        self.assertTrue(set(capstone["source_ids"]).issubset(sources))

    def test_claims_reference_canonical_units_and_sources(self) -> None:
        course_dir = ROOT / "data" / "courses" / "bioestadistica"
        claims = json.loads((course_dir / "claims.json").read_text(encoding="utf-8"))["claims"]
        sources = {
            item["id"]
            for item in json.loads((course_dir / "sources.json").read_text(encoding="utf-8"))["sources"]
        }
        units = {
            json.loads(path.read_text(encoding="utf-8"))["id"]
            for path in (course_dir / "units").glob("unit-*.json")
        }
        for claim in claims:
            self.assertIn(claim["unit_id"], units)
            self.assertIn(claim["source_id"], sources)


if __name__ == "__main__":
    unittest.main()
