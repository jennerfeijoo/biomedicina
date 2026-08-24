from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "bioinstrumentacion"


class BioinstrumentacionUnit08CuratedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.unit = json.loads((COURSE / "units" / "unit-08.json").read_text(encoding="utf-8"))
        self.assessment = json.loads((COURSE / "assessments" / "unit-08.json").read_text(encoding="utf-8"))
        self.glossary = json.loads((COURSE / "glossary.json").read_text(encoding="utf-8"))
        self.sources = json.loads((COURSE / "sources.json").read_text(encoding="utf-8"))
        self.claims = json.loads((COURSE / "claims.json").read_text(encoding="utf-8"))

    def test_u8_is_new_canonical_authoring_not_rewritten_legacy(self) -> None:
        migration = json.loads((ROOT / "data/course_migrations/bioinstrumentacion-numbering-v1.json").read_text(encoding="utf-8"))
        row = next(item for item in migration["canonical_sequence"] if item["canonical_unit"] == 8)
        self.assertEqual(row["origin"], "new")
        self.assertEqual(row["action"], "author")
        self.assertFalse((ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-08.json").exists())
        notice = self.unit["editorial_notice"].lower()
        self.assertIn("autoría canónica nueva", notice)
        self.assertIn("sin unidad autoral histórica equivalente", notice)

    def test_theory_examples_and_review_state(self) -> None:
        self.assertEqual(len(self.unit["topics"]), 6)
        self.assertEqual(sum(len(topic["subtopics"]) for topic in self.unit["topics"]), 18)
        self.assertEqual(len(self.unit["examples"]), 6)
        self.assertEqual(self.unit["status"]["sources"], "traceable")
        self.assertEqual(self.unit["status"]["content"], "in_review")
        self.assertEqual(self.unit["status"]["pedagogy"], "in_review")
        self.assertEqual(self.unit["status"]["internal_review"], "pending")
        self.assertEqual(self.unit["status"]["external_review"], "pending")
        self.assertEqual(self.unit["status"]["publication"], "published_provisional")
        text = json.dumps(self.unit, ensure_ascii=False).lower()
        for marker in ["calibración", "ajuste", "repetibilidad", "reproducibilidad", "covarianza", "regla de decisión", "zona de guarda"]:
            self.assertIn(marker, text)
        self.assertIn("no demuestran por sí solos", text)

    def test_activity_is_reproducible_and_scaffolded(self) -> None:
        activity = self.unit["activities"][0]
        self.assertEqual(activity["status"], "curated_pending_expert_review")
        self.assertEqual(activity["estimated_duration_minutes"], 240)
        self.assertEqual(len(activity["instructions"]), 5)
        self.assertEqual(len(activity["tasks"]), 8)
        self.assertEqual(len(activity["deliverables"]), 6)
        self.assertEqual(len(activity["checking_criteria"]), 10)
        text = " ".join(activity["instructions"] + activity["tasks"] + activity["checking_criteria"]).lower()
        for marker in ["antes de calcular", "conjunto sintético", "calibración", "ajuste", "correlacion", "guard band", "validez clínica"]:
            self.assertIn(marker, text)
        self.assertIn("no se modifican para acomodar resultados", text)

    def test_assessment_is_case_based_and_covers_all_outcomes(self) -> None:
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
        self.assertEqual(covered, {f"BIOINST-U08-LO{i:02d}" for i in range(1, 6)})
        serialized = json.dumps(self.assessment, ensure_ascii=False).lower()
        self.assertIn("r²=0.9999", serialized)
        self.assertIn("ρ=0.8", serialized)
        self.assertIn("trazable", serialized)

    def test_glossary_claims_and_sources_are_traceable(self) -> None:
        entries = {entry["id"]: entry for entry in self.glossary["entries"]}
        self.assertEqual(len(self.unit["glossary_entry_ids"]), 18)
        for entry_id in self.unit["glossary_entry_ids"]:
            entry = entries[entry_id]
            self.assertIn("BIOINST-U08", entry["unit_ids"])
            self.assertNotEqual(entry["verification_status"], "unverified")
            self.assertTrue(entry["source_ids"])
            self.assertTrue(entry.get("source_locators"))

        u8_claims = [claim for claim in self.claims["claims"] if claim.get("unit_id") == "BIOINST-U08"]
        self.assertEqual(len(u8_claims), 18)
        self.assertEqual(self.unit["claim_ids"], [claim["id"] for claim in u8_claims])
        serialized = json.dumps(self.unit, ensure_ascii=False)
        for claim in u8_claims:
            self.assertIn(claim["text"], serialized)
            self.assertEqual(claim["review_state"], "ai_review_provisional")
            self.assertTrue(claim["source_id"])
            self.assertTrue(claim["locator"])

        required = {
            "bipm-vim-calibration", "bipm-vim-adjustment", "bipm-vim-verification",
            "bipm-vim-repeatability", "bipm-vim-reproducibility", "bipm-vim-expanded-uncertainty",
            "jcgm-gum-6-2020", "jcgm-100-2008", "jcgm-100-amd1-2026", "jcgm-101-2008",
            "jcgm-gum-5-2026", "jcgm-106-2012", "ilac-g8-2019", "nist-tn-2156-traceability",
        }
        source_ids = {item["id"] for item in self.sources["sources"]}
        self.assertTrue(required.issubset(source_ids))
        self.assertTrue(required.issubset(set(self.unit["source_ids"])))

    def test_biomedical_specific_review_gap_remains_explicit(self) -> None:
        gap = next(g for g in self.sources["coverage_gaps"] if g["domain"] == "calibración e incertidumbre en instrumentación fisiológica")
        self.assertEqual(gap["status"], "general_framework_traceable_biomedical_review_pending")
        self.assertIn("revisión disciplinaria humana", gap["need"])
        self.assertNotIn("complete", gap["status"])


if __name__ == "__main__":
    unittest.main()
