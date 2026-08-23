from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "bioinstrumentacion"


class BioinstrumentacionUnit02CuratedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.unit = json.loads((COURSE / "units" / "unit-02.json").read_text(encoding="utf-8"))
        self.assessment = json.loads((COURSE / "assessments" / "unit-02.json").read_text(encoding="utf-8"))
        self.glossary = json.loads((COURSE / "glossary.json").read_text(encoding="utf-8"))
        self.sources = json.loads((COURSE / "sources.json").read_text(encoding="utf-8"))
        self.claims = json.loads((COURSE / "claims.json").read_text(encoding="utf-8"))

    def test_authoral_theory_and_examples_are_integrated(self) -> None:
        self.assertEqual(len(self.unit["topics"]), 6)
        self.assertEqual(sum(len(topic["subtopics"]) for topic in self.unit["topics"]), 24)
        paragraphs = [
            block["text"]
            for topic in self.unit["topics"]
            for subtopic in topic["subtopics"]
            for block in subtopic["blocks"]
            if block["type"] == "paragraph"
        ]
        self.assertEqual(len(paragraphs), 24)
        self.assertTrue(all(len(paragraph) >= 250 for paragraph in paragraphs))
        self.assertEqual(len(self.unit["examples"]), 3)
        self.assertEqual(self.unit["status"]["internal_review"], "pending")
        self.assertEqual(self.unit["status"]["external_review"], "pending")

        handoff = json.loads(
            (ROOT / "data" / "review_handoffs" / "bioinstrumentacion-unit-02.json").read_text(encoding="utf-8")
        )
        self.assertFalse(handoff["decision_state_now"]["disciplinary_review_completed"])
        self.assertFalse(handoff["decision_state_now"]["full_theory_drafting_authorized"])
        self.assertFalse(handoff["decision_state_now"]["practice_implementation_authorized"])

    def test_activity_uses_all_three_existing_reproducible_practices(self) -> None:
        activity = self.unit["activities"][0]
        self.assertEqual(activity["status"], "curated_pending_expert_review")
        self.assertEqual(activity["estimated_duration_minutes"], 240)
        self.assertEqual(len(activity["instructions"]), 5)
        self.assertEqual(len(activity["tasks"]), 8)
        self.assertEqual(len(activity["deliverables"]), 6)
        self.assertEqual(len(activity["checking_criteria"]), 10)
        joined = " ".join(activity["instructions"] + activity["tasks"] + activity["deliverables"])
        for practice_id in ("U2-P1", "U2-P2", "U2-P3"):
            self.assertIn(practice_id, joined)
        self.assertIn("primer orden", joined.lower())
        self.assertIn("controles negativos", joined.lower())

    def test_assessment_covers_all_outcomes_with_explanatory_cases(self) -> None:
        items = self.assessment["items"]
        self.assertEqual(len(items), 8)
        self.assertEqual(self.assessment["status"], "curated_pending_expert_review")
        for item in items:
            self.assertEqual(item["type"], "case_analysis")
            self.assertEqual(item["status"], "curated_pending_expert_review")
            self.assertNotEqual(item["difficulty"], "unclassified")
            self.assertNotEqual(item["cognitive_level"], "unclassified")
            self.assertTrue(item["answer_key"]["explanation"])
            self.assertTrue(item["answer_key"]["common_misconceptions"])
            self.assertTrue(item["feedback"]["correct"])
            self.assertTrue(item["feedback"]["incorrect"])
            self.assertTrue(item["source_ids"])

        covered = {lo for item in items for lo in item["linked_learning_outcome_ids"]}
        self.assertEqual(covered, {f"BIOINST-U02-LO{i:02d}" for i in range(1, 6)})
        prompts = " ".join(item["prompt"] for item in items).lower()
        self.assertIn("retardo", prompts)
        self.assertIn("oscila", prompts)
        self.assertIn("sin eje temporal", prompts)

    def test_u2_glossary_is_verified_and_sourced(self) -> None:
        entries = {entry["id"]: entry for entry in self.glossary["entries"]}
        for number in range(13, 25):
            entry = entries[f"BIOINST-GLO-{number:03d}"]
            self.assertNotEqual(entry["verification_status"], "unverified")
            self.assertTrue(entry["source_ids"])
            self.assertTrue(entry.get("source_locators"))

    def test_u2_claims_are_literal_traceable_and_provisional(self) -> None:
        u2_claims = [claim for claim in self.claims["claims"] if claim.get("unit_id") == "BIOINST-U02"]
        self.assertEqual(len(u2_claims), 24)
        self.assertEqual(self.unit["claim_ids"], [claim["id"] for claim in u2_claims])
        serialized_unit = json.dumps(self.unit, ensure_ascii=False)
        for claim in u2_claims:
            self.assertIn(claim["text"], serialized_unit)
            self.assertEqual(claim["review_state"], "ai_review_provisional")
            self.assertEqual(claim["source_verification_status"], "verified_directly")
            self.assertTrue(claim["source_id"])
            self.assertTrue(claim["locator"])

    def test_u2_source_dossiers_are_registered(self) -> None:
        source_ids = {source["id"] for source in self.sources["sources"]}
        required = {
            "vim3-transducer-3-7",
            "vim3-sensor-3-8",
            "vim3-sensitivity-4-12",
            "vim3-selectivity-4-13",
            "vim3-step-response-4-23",
            "jcgm-gum-6-2020-u2",
            "vishay-ntc-thermistor-u2",
            "ni-strain-gage-u2",
            "hamamatsu-photodiode-u2",
            "vishay-ntclg100e2103jb-datasheet",
            "micro-measurements-cea-06-125una-350",
            "ni-strain-gage-loading-u2",
            "hamamatsu-s5821-03-product",
        }
        self.assertTrue(required.issubset(source_ids))
        self.assertTrue(required.issubset(set(self.unit["source_ids"])))


if __name__ == "__main__":
    unittest.main()
