from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "machine-learning-biomedico-validacion-clinica"


class MachineLearningUnit05CuratedTests(unittest.TestCase):
    def test_unit_05_keeps_curated_activity_and_traceability(self) -> None:
        unit = json.loads((COURSE / "units" / "unit-05.json").read_text(encoding="utf-8"))
        assessment = json.loads(
            (COURSE / "assessments" / "unit-05.json").read_text(encoding="utf-8")
        )
        activity = unit["activities"][0]

        self.assertEqual(activity["status"], "curated_pending_expert_review")
        self.assertEqual(activity["estimated_duration_minutes"], 240)
        self.assertEqual(len(activity["deliverables"]), 6)
        self.assertEqual(len(activity["checking_criteria"]), 9)
        self.assertEqual(len(unit["claim_ids"]), 14)
        self.assertEqual(len(assessment["items"]), 8)
        self.assertTrue(
            all(item["status"] == "curated_pending_expert_review" for item in assessment["items"])
        )
        self.assertTrue(all(item["source_ids"] for item in assessment["items"]))


if __name__ == "__main__":
    unittest.main()
