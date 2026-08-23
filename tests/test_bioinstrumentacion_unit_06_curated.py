from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "bioinstrumentacion"


class BioinstrumentacionUnit06CuratedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.unit = json.loads((COURSE / "units" / "unit-06.json").read_text(encoding="utf-8"))
        self.assessment = json.loads((COURSE / "assessments" / "unit-06.json").read_text(encoding="utf-8"))
        self.glossary = json.loads((COURSE / "glossary.json").read_text(encoding="utf-8"))
        self.sources = json.loads((COURSE / "sources.json").read_text(encoding="utf-8"))
        self.claims = json.loads((COURSE / "claims.json").read_text(encoding="utf-8"))

    def test_legacy_u5_crosswalk_and_review_state_are_preserved(self) -> None:
        migration = json.loads((ROOT / "data/course_migrations/bioinstrumentacion-numbering-v1.json").read_text(encoding="utf-8"))
        row = next(item for item in migration["canonical_sequence"] if item["canonical_unit"] == 6)
        self.assertEqual(row["origin"], "legacy_unit_5")
        self.assertEqual(row["action"], "migrate_without_rewriting")
        legacy = json.loads((ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-05.json").read_text(encoding="utf-8"))
        self.assertFalse(legacy["limits"]["professional_review_claimed"])
        self.assertFalse(legacy["limits"]["public_release_authorized"])
        self.assertEqual(legacy["limits"]["U5-A5_status"], "pending_real_human_review")

    def test_theory_examples_and_status(self) -> None:
        self.assertEqual(len(self.unit["topics"]), 6)
        self.assertEqual(sum(len(topic["subtopics"]) for topic in self.unit["topics"]), 18)
        self.assertEqual(len(self.unit["examples"]), 6)
        self.assertEqual(self.unit["status"]["sources"], "traceable")
        self.assertEqual(self.unit["status"]["internal_review"], "pending")
        self.assertEqual(self.unit["status"]["external_review"], "pending")
        self.assertEqual(self.unit["status"]["publication"], "published_provisional")
        text = json.dumps(self.unit, ensure_ascii=False).lower()
        for marker in ["presión", "constante de tiempo", "caudal volumétrico", "beer", "presupuesto de incertidumbre", "multimodal"]:
            self.assertIn(marker, text)

    def test_activity_uses_historical_practices_and_is_scaffolded(self) -> None:
        activity = self.unit["activities"][0]
        self.assertEqual(activity["status"], "curated_pending_expert_review")
        self.assertEqual(activity["estimated_duration_minutes"], 240)
        self.assertEqual((len(activity["instructions"]), len(activity["tasks"]), len(activity["deliverables"]), len(activity["checking_criteria"])), (5, 8, 6, 10))
        text = " ".join(activity["instructions"] + activity["tasks"] + activity["deliverables"]).lower()
        for marker in ["u5-p1", "u5-p2", "u5-p3", "legacy u5", "canonical u6"]:
            self.assertIn(marker, text)

    def test_assessment_covers_all_outcomes(self) -> None:
        self.assertEqual(self.assessment["status"], "curated_pending_expert_review")
        self.assertEqual(len(self.assessment["items"]), 8)
        covered = set()
        for item in self.assessment["items"]:
            self.assertEqual(item["type"], "case_analysis")
            self.assertEqual(item["status"], "curated_pending_expert_review")
            self.assertTrue(item["source_ids"])
            self.assertTrue(item["answer_key"]["explanation"])
            self.assertTrue(item["answer_key"]["common_misconceptions"])
            covered.update(item["linked_learning_outcome_ids"])
        self.assertEqual(covered, {f"BIOINST-U06-LO{i:02d}" for i in range(1, 6)})

    def test_glossary_claims_and_sources_are_traceable(self) -> None:
        entries = {entry["id"]: entry for entry in self.glossary["entries"]}
        self.assertGreaterEqual(len(self.unit["glossary_entry_ids"]), 16)
        for entry_id in self.unit["glossary_entry_ids"]:
            entry = entries[entry_id]
            self.assertIn("BIOINST-U06", entry["unit_ids"])
            self.assertNotEqual(entry["verification_status"], "unverified")
            self.assertTrue(entry["source_ids"])
            self.assertTrue(entry.get("source_locators"))

        u6_claims = [claim for claim in self.claims["claims"] if claim.get("unit_id") == "BIOINST-U06"]
        self.assertEqual(len(u6_claims), 18)
        self.assertEqual(self.unit["claim_ids"], [claim["id"] for claim in u6_claims])
        serialized = json.dumps(self.unit, ensure_ascii=False)
        for claim in u6_claims:
            self.assertIn(claim["text"], serialized)
            self.assertEqual(claim["review_state"], "ai_review_provisional")
            self.assertTrue(claim["source_id"])
            self.assertTrue(claim["locator"])

        required = {
            "nist-pressure-vacuum-calibrations", "nist-piston-gauges-2026", "vishay-ntc-thermistor-u2",
            "nist-liquid-flow-sp250-98", "iupac-transmittance-2025", "iupac-beer-lambert-2025",
            "iupac-reflectance-2025", "iupac-scattering-2025", "jcgm-gum-1-2023", "jcgm-gum-6-2020",
        }
        source_ids = {item["id"] for item in self.sources["sources"]}
        self.assertTrue(required.issubset(source_ids))
        self.assertTrue(required.issubset(set(self.unit["source_ids"])))


if __name__ == "__main__":
    unittest.main()
