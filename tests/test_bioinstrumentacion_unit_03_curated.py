from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "bioinstrumentacion"

class BioinstrumentacionUnit03CuratedTests(unittest.TestCase):
    def setUp(self):
        self.unit=json.loads((COURSE/"units"/"unit-03.json").read_text(encoding="utf-8"))
        self.assessment=json.loads((COURSE/"assessments"/"unit-03.json").read_text(encoding="utf-8"))
        self.glossary=json.loads((COURSE/"glossary.json").read_text(encoding="utf-8"))
        self.sources=json.loads((COURSE/"sources.json").read_text(encoding="utf-8"))
        self.claims=json.loads((COURSE/"claims.json").read_text(encoding="utf-8"))
    def test_theory_examples_and_review_boundary(self):
        self.assertEqual(len(self.unit["topics"]),6)
        self.assertEqual(sum(len(t["subtopics"]) for t in self.unit["topics"]),18)
        self.assertEqual(len(self.unit["examples"]),3)
        self.assertEqual(self.unit["status"]["sources"],"traceable")
        self.assertEqual(self.unit["status"]["internal_review"],"pending")
        self.assertEqual(self.unit["status"]["external_review"],"pending")
        packet=json.loads((ROOT/"data/review_packets/bioinstrumentacion-unit-03-professional-review.json").read_text(encoding="utf-8"))
        self.assertFalse(packet["current_claims"]["external_professional_review_completed"])
        self.assertFalse(packet["current_claims"]["professional_approval_obtained"])
        self.assertFalse(packet["current_claims"]["public_release_authorized"])
    def test_activity_contract(self):
        a=self.unit["activities"][0]
        self.assertEqual(a["status"],"curated_pending_expert_review")
        self.assertEqual(a["estimated_duration_minutes"],240)
        self.assertEqual((len(a["instructions"]),len(a["tasks"]),len(a["deliverables"]),len(a["checking_criteria"])),(5,8,6,10))
        text=" ".join(a["instructions"]+a["tasks"]).lower()
        self.assertIn("u3_practice_u3p1",text); self.assertIn("u3_practice_u3p2",text); self.assertIn("u3_practice_u3p3",text)
    def test_assessment(self):
        self.assertEqual(self.assessment["status"],"curated_pending_expert_review")
        self.assertEqual(len(self.assessment["items"]),8)
        covered=set()
        for q in self.assessment["items"]:
            self.assertEqual(q["type"],"case_analysis"); self.assertTrue(q["source_ids"]); self.assertTrue(q["answer_key"]["explanation"]); self.assertTrue(q["answer_key"]["common_misconceptions"]); covered.update(q["linked_learning_outcome_ids"])
        self.assertEqual(covered,{f"BIOINST-U03-LO{i:02d}" for i in range(1,6)})
    def test_glossary_claims_sources(self):
        entries={e["id"]:e for e in self.glossary["entries"]}
        self.assertTrue(self.unit["glossary_entry_ids"])
        for eid in self.unit["glossary_entry_ids"]:
            e=entries[eid]; self.assertNotEqual(e["verification_status"],"unverified"); self.assertTrue(e["source_ids"]); self.assertTrue(e.get("source_locators"))
        u3=[c for c in self.claims["claims"] if c.get("unit_id")=="BIOINST-U03"]
        self.assertEqual(len(u3),18); self.assertEqual(len(self.unit["claim_ids"]),18); self.assertEqual(self.unit["claim_ids"],[c["id"] for c in u3])
        serialized=json.dumps(self.unit,ensure_ascii=False)
        for c in u3: self.assertIn(c["text"],serialized); self.assertEqual(c["review_state"],"ai_review_provisional"); self.assertTrue(c["locator"])
        sids={s["id"] for s in self.sources["sources"]}
        required={"malmivuo-plonsey-volume-conductor","body-electrode-interface-review-2021","hyoung-koo-common-mode-2026","openstax-ap2e-action-potential","physionet-mit-bih-arrhythmia","physionet-eegmmidb","lou-bioelectric-monitoring-2026","iec-60601-1-overview"}
        self.assertTrue(required.issubset(sids)); self.assertTrue(required.issubset(set(self.unit["source_ids"])))

if __name__=="__main__": unittest.main()
