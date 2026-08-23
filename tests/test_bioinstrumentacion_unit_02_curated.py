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
        paragraphs = [block["text"] for topic in self.unit["topics"] for sub in topic["subtopics"] for block in sub["blocks"] if block["type"] == "paragraph"]
        self.assertEqual(len(paragraphs), 24)
        self.assertGreaterEqual(sum(len(text.split()) for text in paragraphs), 2200)
        self.assertEqual(len(self.unit["examples"]), 3)
        self.assertEqual(self.unit["status"]["sources"], "traceable")
        self.assertEqual(self.unit["status"]["internal_review"], "pending")
        self.assertEqual(self.unit["status"]["external_review"], "pending")
        handoff = json.loads((ROOT / "data" / "review_handoffs" / "bioinstrumentacion-unit-02.json").read_text(encoding="utf-8"))
        self.assertFalse(handoff["decision_state_now"]["disciplinary_review_completed"])

    def test_activity_is_reproducible_and_scaffolded(self) -> None:
        activity = self.unit["activities"][0]
        self.assertEqual(activity["status"], "curated_pending_expert_review")
        self.assertEqual(activity["estimated_duration_minutes"], 240)
        self.assertEqual(len(activity["instructions"]), 5)
        self.assertEqual(len(activity["tasks"]), 8)
        self.assertEqual(len(activity["deliverables"]), 6)
        self.assertEqual(len(activity["checking_criteria"]), 10)
        joined = " ".join(activity["instructions"] + activity["tasks"] + activity["deliverables"]).lower()
        self.assertIn("static_dataset", joined)
        self.assertIn("dynamic_dataset", joined)
        self.assertIn("datasheets", joined)

    def test_assessment_covers_all_outcomes_with_sources_and_feedback(self) -> None:
        self.assertEqual(self.assessment["status"], "curated_pending_expert_review")
        self.assertEqual(len(self.assessment["items"]), 8)
        covered = set()
        for item in self.assessment["items"]:
            self.assertEqual(item["type"], "case_analysis")
            self.assertEqual(item["status"], "curated_pending_expert_review")
            self.assertNotEqual(item["difficulty"], "unclassified")
            self.assertNotEqual(item["cognitive_level"], "unclassified")
            self.assertTrue(item["answer_key"]["explanation"])
            self.assertTrue(item["answer_key"]["common_misconceptions"])
            self.assertTrue(item["feedback"]["correct"])
            self.assertTrue(item["feedback"]["incorrect"])
            self.assertTrue(item["source_ids"])
            covered.update(item["linked_learning_outcome_ids"])
        self.assertEqual(covered, {f"BIOINST-U02-LO{i:02d}" for i in range(1, 6)})

    def test_twenty_authoral_glossary_terms_are_traceable(self) -> None:
        entries = {entry["id"]: entry for entry in self.glossary["entries"]}
        self.assertEqual(len(self.unit["glossary_entry_ids"]), 20)
        for entry_id in self.unit["glossary_entry_ids"]:
            entry = entries[entry_id]
            self.assertIn("BIOINST-U02", entry["unit_ids"])
            self.assertNotEqual(entry["verification_status"], "unverified")
            self.assertTrue(entry["source_ids"])
            self.assertTrue(entry.get("source_locators"))

    def test_claims_are_exactly_present_and_traceable(self) -> None:
        u2_claims = [claim for claim in self.claims["claims"] if claim.get("unit_id") == "BIOINST-U02"]
        self.assertEqual(len(u2_claims), 18)
        self.assertEqual(self.unit["claim_ids"], [claim["id"] for claim in u2_claims])
        serialized = json.dumps(self.unit, ensure_ascii=False)
        for claim in u2_claims:
            self.assertIn(claim["text"], serialized)
            self.assertEqual(claim["review_state"], "ai_review_provisional")
            self.assertTrue(claim["source_id"])
            self.assertTrue(claim["locator"])

    def test_specific_metrology_and_component_sources_are_registered(self) -> None:
        source_ids = {item["id"] for item in self.sources["sources"]}
        required = {
            "bipm-vim-sensor", "bipm-vim-transducer", "bipm-vim-sensitivity", "bipm-vim-selectivity",
            "bipm-vim-input-quantity", "bipm-vim-output-quantity", "bipm-vim-measuring-interval",
            "bipm-vim-dead-band", "bipm-vim-instrumental-drift", "bipm-vim-step-response-time",
            "vishay-ntc-thermistor-u2", "ni-strain-gage-u2", "hamamatsu-photodiode-u2"
        }
        self.assertTrue(required.issubset(source_ids))
        self.assertTrue(required.issubset(set(self.unit["source_ids"])))


if __name__ == "__main__":
    unittest.main()
