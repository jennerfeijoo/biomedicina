import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "machine-learning-biomedico-validacion-clinica"


class MachineLearningUnit08PedagogyTests(unittest.TestCase):
    def test_unit_08_keeps_curated_activity_contract(self) -> None:
        unit = json.loads((COURSE / "units" / "unit-08.json").read_text(encoding="utf-8"))
        activity = unit["activities"][0]
        self.assertEqual(activity["status"], "curated_pending_expert_review")
        self.assertEqual(activity["estimated_duration_minutes"], 240)
        self.assertEqual(len(activity["tasks"]), 8)
        self.assertEqual(len(activity["deliverables"]), 6)
        self.assertEqual(len(activity["checking_criteria"]), 10)
        self.assertEqual(len(unit["claim_ids"]), 14)
        self.assertEqual(unit["prerequisite_unit_ids"], [f"MLBIO-U0{i}" for i in range(1, 8)])

    def test_unit_08_assessment_is_explanatory_and_source_backed(self) -> None:
        assessment = json.loads((COURSE / "assessments" / "unit-08.json").read_text(encoding="utf-8"))
        self.assertEqual(assessment["status"], "curated_pending_expert_review")
        self.assertEqual(len(assessment["items"]), 8)
        self.assertTrue(all(item["difficulty"] != "unclassified" for item in assessment["items"]))
        self.assertTrue(all(item["answer_key"]["explanation"] for item in assessment["items"]))
        self.assertTrue(all(item["feedback"]["correct"] and item["feedback"]["incorrect"] for item in assessment["items"]))
        self.assertTrue(all(item["source_ids"] for item in assessment["items"]))


if __name__ == "__main__":
    unittest.main()
