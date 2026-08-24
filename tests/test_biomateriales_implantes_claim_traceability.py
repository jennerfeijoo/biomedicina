from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "biomateriales-implantes"
CLAIMS_PATH = COURSE / "claims.json"
SOURCES_PATH = COURSE / "sources.json"


class BiomaterialesImplantesClaimTraceabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.claims_registry = json.loads(CLAIMS_PATH.read_text(encoding="utf-8"))
        cls.sources_registry = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))
        cls.claims = cls.claims_registry["claims"]
        cls.sources = {source["id"]: source for source in cls.sources_registry["sources"]}
        cls.units = {
            unit_no: json.loads((COURSE / "units" / f"unit-{unit_no:02d}.json").read_text(encoding="utf-8"))
            for unit_no in range(1, 7)
        }

    def test_registry_has_substantive_coverage_for_all_six_units(self) -> None:
        self.assertEqual(len(self.claims), 24)
        by_unit = {unit_no: [] for unit_no in range(1, 7)}
        for claim in self.claims:
            by_unit[claim["unit"]].append(claim)
        self.assertTrue(all(len(by_unit[unit_no]) == 4 for unit_no in range(1, 7)))

    def test_claim_ids_are_unique_and_bidirectionally_linked(self) -> None:
        ids = [claim["claim_id"] for claim in self.claims]
        self.assertEqual(len(ids), len(set(ids)))
        for unit_no, unit in self.units.items():
            expected = sorted(claim["claim_id"] for claim in self.claims if claim["unit"] == unit_no)
            self.assertEqual(unit["claim_ids"], expected)
            for claim_id in expected:
                self.assertRegex(claim_id, rf"^BIMPL-U{unit_no:02d}-C\d{{3}}$")

    def test_claim_text_is_literal_in_its_canonical_unit(self) -> None:
        for claim in self.claims:
            unit_text = json.dumps(self.units[claim["unit"]], ensure_ascii=False)
            self.assertIn(claim["text"], unit_text, claim["claim_id"])
            self.assertEqual(claim["unit_id"], f"BIMPL-U{claim['unit']:02d}")
            self.assertEqual(claim["id"], claim["claim_id"])

    def test_claim_sources_exist_are_verified_and_belong_to_unit_source_set(self) -> None:
        for claim in self.claims:
            source_id = claim["source_id"]
            self.assertIn(source_id, self.sources, claim["claim_id"])
            source = self.sources[source_id]
            self.assertEqual(source.get("verification_status"), "verified_directly", claim["claim_id"])
            self.assertEqual(claim.get("source_verification_status"), "verified_directly", claim["claim_id"])
            self.assertIn(source_id, self.units[claim["unit"]]["source_ids"], claim["claim_id"])
            self.assertTrue(claim.get("locator", {}).get("section"), claim["claim_id"])

    def test_claims_keep_human_review_pending(self) -> None:
        self.assertEqual(self.claims_registry["review_state"], "ai_review_provisional")
        self.assertIn("revisión disciplinaria humana pendiente", self.claims_registry["scope"].casefold())
        for claim in self.claims:
            self.assertEqual(claim["review_state"], "ai_review_provisional")
            self.assertIsNone(claim["reviewer_validation_id"])
            self.assertEqual(claim["reviewed_at"], "2026-08-24")
        for unit in self.units.values():
            self.assertEqual(unit["status"]["internal_review"], "pending")
            self.assertEqual(unit["status"]["external_review"], "pending")

    def test_high_risk_claims_preserve_clinical_or_regulatory_boundaries(self) -> None:
        high_risk = [claim for claim in self.claims if claim["risk"] == "high"]
        self.assertGreaterEqual(len(high_risk), 10)
        combined = " ".join(claim["context"] for claim in high_risk).casefold()
        for concept in ("riesgo", "clín", "regulator", "dispositivo"):
            self.assertIn(concept, combined)


if __name__ == "__main__":
    unittest.main()
