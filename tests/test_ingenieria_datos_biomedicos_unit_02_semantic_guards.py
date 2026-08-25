from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "ingenieria-datos-biomedicos" / "units" / "unit-02.json"


class IngenieriaDatosBiomedicosUnit02SemanticGuards(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_time_normalization_does_not_invent_timezone(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        self.assertIn("una hora sin zona no adquiere mágicamente utc", text)
        self.assertIn("parsing de inferencia", text)

    def test_terminology_mapping_can_remain_unresolved(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        self.assertIn("mapping_status=unresolved", text)
        self.assertIn("source-is-narrower-than-target", text)
        self.assertIn("source-is-broader-than-target", text)

    def test_dimensional_compatibility_is_not_clinical_equivalence(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        self.assertIn("compatibilidad dimensional", text)
        self.assertIn("puede no ser suficiente", text)
        self.assertIn("masa molar", text)


if __name__ == "__main__":
    unittest.main()
