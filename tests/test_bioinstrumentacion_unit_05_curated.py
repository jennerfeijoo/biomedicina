from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "bioinstrumentacion"


class BioinstrumentacionUnit05CuratedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.unit = json.loads((COURSE / "units" / "unit-05.json").read_text(encoding="utf-8"))
        self.assessment = json.loads((COURSE / "assessments" / "unit-05.json").read_text(encoding="utf-8"))
        self.glossary = json.loads((COURSE / "glossary.json").read_text(encoding="utf-8"))
        self.sources = json.loads((COURSE / "sources.json").read_text(encoding="utf-8"))
        self.claims = json.loads((COURSE / "claims.json").read_text(encoding="utf-8"))

    def test_legacy_u4_crosswalk_is_preserved(self) -> None:
        migration = json.loads((ROOT / "data" / "course_migrations" / "bioinstrumentacion-numbering-v1.json").read_text(encoding="utf-8"))
        row = next(item for item in migration["canonical_sequence"] if item["canonical_unit"] == 5)
        self.assertEqual(row["origin"], "legacy_unit_4")
        self.assertEqual(row["action"], "migrate_without_rewriting")
        legacy = json.loads((ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "units" / "unit-04.json").read_text(encoding="utf-8"))
        self.assertFalse(legacy["limits"]["professional_review_claimed"])
        self.assertFalse(legacy["limits"]["public_release_authorized"])
        self.assertEqual(legacy["limits"]["U4-A5_status"], "pending_real_human_review")

    def test_theory_is_deep_and_keeps_u4_boundary(self) -> None:
        self.assertEqual(len(self.unit["topics"]), 7)
        self.assertEqual(sum(len(topic["subtopics"]) for topic in self.unit["topics"]), 21)
        self.assertEqual(len(self.unit["examples"]), 4)
        self.assertEqual(self.unit["status"]["sources"], "traceable")
        self.assertEqual(self.unit["status"]["internal_review"], "pending")
        self.assertEqual(self.unit["status"]["external_review"], "pending")
        self.assertEqual(self.unit["status"]["publication"], "published_provisional")
        serialized = json.dumps(self.unit, ensure_ascii=False).lower()
        self.assertIn("u4 diseña el acondicionamiento", serialized)
        self.assertIn("legacy u4", serialized)
        self.assertIn("canonical u5", serialized)

    def test_activity_uses_historical_practices_with_scaffolding(self) -> None:
        activity = self.unit["activities"][0]
        self.assertEqual(activity["status"], "curated_pending_expert_review")
        self.assertEqual(activity["estimated_duration_minutes"], 240)
        self.assertEqual(len(activity["instructions"]), 5)
        self.assertEqual(len(activity["tasks"]), 8)
        self.assertEqual(len(activity["deliverables"]), 6)
        self.assertEqual(len(activity["checking_criteria"]), 10)
        text = " ".join(activity["instructions"] + activity["tasks"]).lower()
        for marker in ["u4_practice_u4p1", "u4_practice_u4p2", "u4_practice_u4p3"]:
            self.assertIn(marker, text)

    def test_assessment_covers_all_local_outcomes(self) -> None:
        self.assertEqual(self.assessment["status"], "curated_pending_expert_review")
        self.assertEqual(len(self.assessment["items"]), 8)
        covered = set()
        for item in self.assessment["items"]:
            self.assertEqual(item["type"], "case_analysis")
            self.assertEqual(item["status"], "curated_pending_expert_review")
            self.assertTrue(item["source_ids"])
            self.assertTrue(item["answer_key"]["explanation"])
            self.assertTrue(item["answer_key"]["common_misconceptions"])
            self.assertTrue(item["feedback"]["correct"])
            self.assertTrue(item["feedback"]["incorrect"])
            covered.update(item["linked_learning_outcome_ids"])
        self.assertEqual(covered, {f"BIOINST-U05-LO{i:02d}" for i in range(1, 6)})

    def test_glossary_claims_and_sources_are_traceable(self) -> None:
        entries = {entry["id"]: entry for entry in self.glossary["entries"]}
        self.assertGreaterEqual(len(self.unit["glossary_entry_ids"]), 18)
        for entry_id in self.unit["glossary_entry_ids"]:
            entry = entries[entry_id]
            self.assertIn("BIOINST-U05", entry["unit_ids"])
            self.assertNotEqual(entry["verification_status"], "unverified")
            self.assertTrue(entry["source_ids"])
            self.assertTrue(entry.get("source_locators"))

        u5_claims = [claim for claim in self.claims["claims"] if claim.get("unit_id") == "BIOINST-U05"]
        self.assertEqual(len(u5_claims), 18)
        self.assertEqual(self.unit["claim_ids"], [claim["id"] for claim in u5_claims])
        serialized = json.dumps(self.unit, ensure_ascii=False)
        for claim in u5_claims:
            self.assertIn(claim["text"], serialized)
            self.assertEqual(claim["review_state"], "ai_review_provisional")
            self.assertTrue(claim["source_id"])
            self.assertTrue(claim["locator"])

        required = {
            "ni-analog-signal-acquisition", "ni-anti-alias-filters", "adi-adc-glossary",
            "adi-quantization-glossary", "adi-enob-dynamic-2019", "adi-adc-dynamic-parameters",
            "adi-aperture-jitter", "ni-sample-clock-2025", "ni-synchronization-explained",
            "nist-time-measurement", "rfc3550-sequence-timestamp", "iec-60601-1-overview",
        }
        source_ids = {item["id"] for item in self.sources["sources"]}
        self.assertTrue(required.issubset(source_ids))
        self.assertTrue(required.issubset(set(self.unit["source_ids"])))


if __name__ == "__main__":
    unittest.main()
