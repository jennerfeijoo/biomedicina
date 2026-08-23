from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_DIR = ROOT / "data" / "courses" / "bioinstrumentacion"


def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


RENDERER = load_module("advanced_unit_renderer_bioinst", "scripts/advanced_unit_renderer.py")


class BioinstrumentacionCanonicalBootstrapTests(unittest.TestCase):
    def test_course_has_ten_canonical_units_and_review_state(self) -> None:
        course = json.loads((COURSE_DIR / "course.json").read_text(encoding="utf-8"))
        self.assertEqual(course["code"], "BIOINST")
        self.assertEqual(len(course["unit_files"]), 10)
        self.assertEqual(len(course["learning_outcomes"]), 8)
        self.assertEqual(course["status"]["content"], "in_review")
        self.assertEqual(course["status"]["pedagogy"], "in_review")
        self.assertEqual(course["status"]["internal_review"], "pending")
        self.assertEqual(course["status"]["external_review"], "pending")
        self.assertEqual(course["status"]["publication"], "published_provisional")

    def test_course_outcome_mapping_is_explicit_for_shared_outcomes(self) -> None:
        expected = {
            1: ["BIOINST-LO01"],
            2: ["BIOINST-LO02"],
            3: ["BIOINST-LO03"],
            4: ["BIOINST-LO04"],
            5: ["BIOINST-LO04"],
            6: ["BIOINST-LO05"],
            7: ["BIOINST-LO06"],
            8: ["BIOINST-LO07"],
            9: ["BIOINST-LO08"],
            10: ["BIOINST-LO08"],
        }
        for number, outcome_ids in expected.items():
            unit = json.loads(
                (COURSE_DIR / "units" / f"unit-{number:02d}.json").read_text(encoding="utf-8")
            )
            self.assertEqual(unit["course_learning_outcome_ids"], outcome_ids)
            self.assertTrue(unit["course_learning_outcome_ids"])

    def test_historical_authoral_sources_are_preserved(self) -> None:
        for number in range(1, 7):
            self.assertTrue(
                (ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "units" / f"unit-{number:02d}.json").exists()
            )

        migration = json.loads(
            (ROOT / "data" / "course_migrations" / "bioinstrumentacion-numbering-v1.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(migration["status"], "canonical_academic_bootstrap_executed")
        bootstrap = migration["canonical_academic_bootstrap"]
        self.assertEqual(bootstrap["unit_count"], 10)
        self.assertTrue(bootstrap["historical_authoral_sources_preserved"])
        self.assertFalse(bootstrap["legacy_numbering_rewritten"])
        self.assertFalse(bootstrap["human_review_executed"])
        self.assertFalse(bootstrap["disciplinary_review_complete"])

    def test_renderer_prefers_canonical_bioinstrumentation_unit(self) -> None:
        unit = RENDERER.load_advanced_unit(ROOT, "bioinstrumentacion", 1)
        self.assertIsNotNone(unit)
        assert unit is not None
        self.assertEqual(unit["schema_version"], "canonical-1.0")
        self.assertEqual(unit["unit"], 1)
        self.assertEqual(unit["title"], "Mensurando, sistema de medición y cadena de trazabilidad")


if __name__ == "__main__":
    unittest.main()
