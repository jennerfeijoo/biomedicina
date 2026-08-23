from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "bioinstrumentacion"


class BioinstrumentacionUnit07CuratedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.unit = json.loads((COURSE / "units" / "unit-07.json").read_text(encoding="utf-8"))
        self.assessment = json.loads((COURSE / "assessments" / "unit-07.json").read_text(encoding="utf-8"))
        self.glossary = json.loads((COURSE / "glossary.json").read_text(encoding="utf-8"))
        self.sources = json.loads((COURSE / "sources.json").read_text(encoding="utf-8"))
        self.claims = json.loads((COURSE / "claims.json").read_text(encoding="utf-8"))

    def test_legacy_u6_crosswalk_and_safety_boundary_are_preserved(self) -> None:
        migration = json.loads((ROOT / "data/course_migrations/bioinstrumentacion-numbering-v1.json").read_text(encoding="utf-8"))
        row = next(item for item in migration["canonical_sequence"] if item["canonical_unit"] == 7)
        self.assertEqual(row["origin"], "legacy_unit_6")
        self.assertEqual(row["action"], "migrate_without_rewriting")
        legacy = json.loads((ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-06.json").read_text(encoding="utf-8"))
        self.assertTrue(legacy["safety_boundary"]["synthetic_offline_only"])
        self.assertFalse(legacy["safety_boundary"]["human_participants_allowed"])
        self.assertFalse(legacy["safety_boundary"]["energized_medical_devices_allowed"])
        self.assertFalse(legacy["safety_boundary"]["professional_review_claimed"])
        self.assertFalse(legacy["editorial_decision"]["human_review_executed"])
        self.assertFalse(legacy["editorial_decision"]["professional_review_executed"])
        self.assertFalse(legacy["editorial_decision"]["public_release_authorized"])
        legacy_assessment = json.loads((ROOT / "data/assessment_implementations/bioinstrumentacion-unit-06.json").read_text(encoding="utf-8"))
        u6a5 = next(item for item in legacy_assessment["assessments"] if item["id"] == "U6-A5")
        self.assertEqual(u6a5["status"], "pending_human_execution")

    def test_theory_examples_and_status(self) -> None:
        self.assertEqual(len(self.unit["topics"]), 6)
        self.assertEqual(sum(len(topic["subtopics"]) for topic in self.unit["topics"]), 18)
        self.assertEqual(len(self.unit["examples"]), 6)
        self.assertEqual(self.unit["status"]["sources"], "traceable")
        self.assertEqual(self.unit["status"]["internal_review"], "pending")
        self.assertEqual(self.unit["status"]["external_review"], "pending")
        self.assertEqual(self.unit["status"]["publication"], "published_provisional")
        text = json.dumps(self.unit, ensure_ascii=False).lower()
        for marker in ["peligro", "barrera", "emisiones", "inmunidad", "fallo simple", "conformidad"]:
            self.assertIn(marker, text)

    def test_activity_is_scaffolded_and_keeps_work_offline(self) -> None:
        activity = self.unit["activities"][0]
        self.assertEqual(activity["status"], "curated_pending_expert_review")
        self.assertEqual(activity["estimated_duration_minutes"], 240)
        self.assertEqual((len(activity["instructions"]), len(activity["tasks"]), len(activity["deliverables"]), len(activity["checking_criteria"])), (5, 8, 6, 10))
        text = " ".join(activity["instructions"] + activity["tasks"] + activity["checking_criteria"]).lower()
        for marker in ["u6-p1", "u6-p2", "u6-p3", "legacy u6", "canonical u7", "no conectar"]:
            self.assertIn(marker, text)
        forbidden = ["conectar una persona", "conecte una persona", "conectar electrodos al", "energizar un equipo médico"]
        for phrase in forbidden:
            self.assertNotIn(phrase, text)

    def test_assessment_covers_all_outcomes_without_claiming_conformity(self) -> None:
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
        self.assertEqual(covered, {f"BIOINST-U07-LO{i:02d}" for i in range(1, 6)})
        serialized = json.dumps(self.assessment, ensure_ascii=False).lower()
        self.assertIn("no está autorizado", serialized)
        self.assertIn("no demuestra", serialized)

    def test_glossary_claims_and_sources_are_traceable(self) -> None:
        entries = {entry["id"]: entry for entry in self.glossary["entries"]}
        self.assertGreaterEqual(len(self.unit["glossary_entry_ids"]), 18)
        for entry_id in self.unit["glossary_entry_ids"]:
            entry = entries[entry_id]
            self.assertIn("BIOINST-U07", entry["unit_ids"])
            self.assertNotEqual(entry["verification_status"], "unverified")
            self.assertTrue(entry["source_ids"])
            self.assertTrue(entry.get("source_locators"))

        u7_claims = [claim for claim in self.claims["claims"] if claim.get("unit_id") == "BIOINST-U07"]
        self.assertEqual(len(u7_claims), 18)
        self.assertEqual(self.unit["claim_ids"], [claim["id"] for claim in u7_claims])
        serialized = json.dumps(self.unit, ensure_ascii=False)
        for claim in u7_claims:
            self.assertIn(claim["text"], serialized)
            self.assertEqual(claim["review_state"], "ai_review_provisional")
            self.assertTrue(claim["source_id"])
            self.assertTrue(claim["locator"])

        required = {
            "iec-60601-1-edition-3-2", "iec-60601-1-2-edition-4-1",
            "iso-14971-2019-current", "fda-emc-guidance-2022", "fda-emc-overview-2026",
        }
        source_ids = {item["id"] for item in self.sources["sources"]}
        self.assertTrue(required.issubset(source_ids))
        self.assertTrue(required.issubset(set(self.unit["source_ids"])))


if __name__ == "__main__":
    unittest.main()
