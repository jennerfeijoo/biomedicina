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

    def test_renderer_prefers_the_canonical_unit(self) -> None:
        unit = RENDERER.load_advanced_unit(ROOT, "bioestadistica", 1)
        self.assertIsNotNone(unit)
        assert unit is not None
        self.assertEqual(unit["schema_version"], "canonical-1.0")
        self.assertEqual(unit["unit"], 1)
        self.assertEqual(unit["title"], "Preguntas, datos y diseños biomédicos")
        self.assertTrue(unit["theory_sections"][0]["paragraphs"])
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
