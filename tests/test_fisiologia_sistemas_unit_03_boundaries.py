from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "data" / "course_redevelopment" / "fisiologia-sistemas" / "units" / "unit-03.json"


class FisiologiaSistemasUnit03BoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(UNIT.read_text(encoding="utf-8"))
        cls.text = UNIT.read_text(encoding="utf-8").casefold()

    def test_spo2_and_vo2_are_not_diagnostic_shortcuts(self) -> None:
        errors = json.dumps(self.unit["common_errors"], ensure_ascii=False).casefold()
        self.assertIn("interpretar sao2 normal como capacidad de transporte normal", errors)
        self.assertIn("atribuir v̇o2 reducido automáticamente al corazón", errors)
        self.assertIn("atribuir v̇o2 reducido automáticamente al pulmón", errors)

    def test_critical_care_examples_remain_educational(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for phrase in ("no constituye diagnóstico", "indicación de oxígeno", "transfusión", "vasopresores", "objetivos de reanimación"):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
