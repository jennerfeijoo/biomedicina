from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "data" / "course_redevelopment" / "fisiologia-sistemas" / "units" / "unit-03.json"
SUBJECT = ROOT / "data" / "subjects" / "biologicas-medicas" / "fisiologia-sistemas.json"


class FisiologiaSistemasUnit03BoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(UNIT.read_text(encoding="utf-8"))
        cls.text = UNIT.read_text(encoding="utf-8").casefold()
        cls.subject = json.loads(SUBJECT.read_text(encoding="utf-8"))

    def test_spo2_and_vo2_are_not_diagnostic_shortcuts(self) -> None:
        errors = json.dumps(self.unit["common_errors"], ensure_ascii=False).casefold()
        self.assertIn("interpretar sao2 normal como capacidad de transporte normal", errors)
        self.assertIn("atribuir v̇o2 reducido automáticamente al corazón", errors)
        self.assertIn("atribuir v̇o2 reducido automáticamente al pulmón", errors)

    def test_critical_care_examples_remain_educational(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for phrase in ("no constituye diagnóstico", "indicación de oxígeno", "transfusión", "vasopresores", "objetivos de reanimación"):
            self.assertIn(phrase, notice)

    def test_published_subject_descriptor_matches_curated_u3(self) -> None:
        published = next(item for item in self.subject["detailed_units"] if item["unit"] == 3)
        self.assertEqual(published["title"], self.unit["title"])
        self.assertEqual(published["description"], self.unit["purpose"])
        self.assertIn("cadena acoplada", published["description"].casefold())
        self.assertNotIn("integrar perfusión, ventilación, transporte de oxígeno para resolver", published["description"].casefold())


if __name__ == "__main__":
    unittest.main()
