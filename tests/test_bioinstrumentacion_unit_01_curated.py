from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "bioinstrumentacion"


class BioinstrumentacionUnit01CuratedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.unit = json.loads((COURSE / "units" / "unit-01.json").read_text(encoding="utf-8"))
        self.assessment = json.loads((COURSE / "assessments" / "unit-01.json").read_text(encoding="utf-8"))
        self.glossary = json.loads((COURSE / "glossary.json").read_text(encoding="utf-8"))
        self.sources = json.loads((COURSE / "sources.json").read_text(encoding="utf-8"))
        self.claims = json.loads((COURSE / "claims.json").read_text(encoding="utf-8"))

    def test_authoral_theory_is_integrated_without_claiming_human_review(self) -> None:
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
        self.assertEqual(self.unit["status"]["internal_review"], "pending")
        self.assertEqual(self.unit["status"]["external_review"], "pending")
        self.assertIn("revisión disciplinaria humana sigue pendiente", self.unit["editorial_notice"])

        handoff = json.loads(
            (ROOT / "data" / "review_handoffs" / "bioinstrumentacion-unit-01.json").read_text(encoding="utf-8")
        )
        self.assertFalse(handoff["decision_state_now"]["disciplinary_review_completed"])
        self.assertFalse(handoff["decision_state_now"]["controlled_drafting_authorized"])

    def test_activity_has_guided_reproducible_contract(self) -> None:
        activity = self.unit["activities"][0]
        self.assertEqual(activity["status"], "curated_pending_expert_review")
        self.assertEqual(activity["estimated_duration_minutes"], 240)
        self.assertEqual(len(activity["instructions"]), 5)
        self.assertEqual(len(activity["tasks"]), 8)
        self.assertEqual(len(activity["deliverables"]), 6)
        self.assertEqual(len(activity["checking_criteria"]), 10)
        joined = " ".join(activity["instructions"] + activity["tasks"] + activity["deliverables"])
        self.assertIn("thermal", joined.lower())
        self.assertIn("wfdb", joined.lower())
        self.assertIn("trazabilidad", joined.lower())

    def test_assessment_is_case_based_explanatory_and_sourced(self) -> None:
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
        self.assertEqual(covered, {f"BIOINST-U01-LO{i:02d}" for i in range(1, 6)})

    def test_glossary_and_claims_are_traceable(self) -> None:
        entries = {entry["id"]: entry for entry in self.glossary["entries"]}
        for number in range(1, 13):
            entry = entries[f"BIOINST-GLO-{number:03d}"]
            self.assertNotEqual(entry["verification_status"], "unverified")
            self.assertTrue(entry["source_ids"])
            self.assertTrue(entry.get("source_locators"))

        u1_claims = [claim for claim in self.claims["claims"] if claim.get("unit_id") == "BIOINST-U01"]
        self.assertEqual(len(u1_claims), 18)
        self.assertEqual(self.unit["claim_ids"], [claim["id"] for claim in u1_claims])
        serialized_unit = json.dumps(self.unit, ensure_ascii=False)
        for claim in u1_claims:
            self.assertIn(claim["text"], serialized_unit)
            self.assertEqual(claim["review_state"], "ai_review_provisional")
            self.assertTrue(claim["source_id"])
            self.assertTrue(claim["locator"])

    def test_direct_metrology_sources_are_registered_for_unit_1(self) -> None:
        source_ids = {source["id"] for source in self.sources["sources"]}
        required = {
            "bipm-vim-quantity",
            "bipm-vim-measurand",
            "bipm-vim-indication",
            "bipm-vim-measured-value",
            "bipm-vim-measurement-result",
            "bipm-vim-measuring-system",
            "bipm-vim-measuring-chain",
            "bipm-vim-measurement-model",
            "bipm-vim-calibration",
            "bipm-vim-traceability",
            "bipm-vim-uncertainty",
            "jcgm-gum-1-2023",
            "jcgm-gum-6-2020",
            "nist-tn-2156",
            "physionet-mit-bih-arrhythmia",
        }
        self.assertTrue(required.issubset(source_ids))
        self.assertTrue(required.issubset(set(self.unit["source_ids"])))


if __name__ == "__main__":
    unittest.main()
