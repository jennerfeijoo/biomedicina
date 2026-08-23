from __future__ import annotations
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; COURSE=ROOT/"data"/"courses"/"bioinstrumentacion"
class BioinstrumentacionUnit04CuratedTests(unittest.TestCase):
 def setUp(self):
  self.u=json.loads((COURSE/"units"/"unit-04.json").read_text(encoding="utf-8")); self.a=json.loads((COURSE/"assessments"/"unit-04.json").read_text(encoding="utf-8")); self.g=json.loads((COURSE/"glossary.json").read_text(encoding="utf-8")); self.s=json.loads((COURSE/"sources.json").read_text(encoding="utf-8")); self.c=json.loads((COURSE/"claims.json").read_text(encoding="utf-8"))
 def test_theory_and_scope(self):
  self.assertEqual(len(self.u["topics"]),4); self.assertEqual(sum(len(t["subtopics"]) for t in self.u["topics"]),16); self.assertEqual(len(self.u["examples"]),3); self.assertEqual(self.u["status"]["sources"],"traceable"); self.assertEqual(self.u["status"]["internal_review"],"pending"); self.assertEqual(self.u["status"]["external_review"],"pending")
  text=json.dumps(self.u,ensure_ascii=False).lower(); self.assertIn("u5 aborda muestreo, cuantización",text)
 def test_activity(self):
  a=self.u["activities"][0]; self.assertEqual(a["status"],"curated_pending_expert_review"); self.assertEqual(a["estimated_duration_minutes"],240); self.assertEqual((len(a["instructions"]),len(a["tasks"]),len(a["deliverables"]),len(a["checking_criteria"])),(5,8,6,10))
 def test_assessment(self):
  self.assertEqual(self.a["status"],"curated_pending_expert_review"); self.assertEqual(len(self.a["items"]),8); covered=set()
  for q in self.a["items"]: self.assertEqual(q["type"],"case_analysis"); self.assertTrue(q["source_ids"]); self.assertTrue(q["answer_key"]["explanation"]); covered.update(q["linked_learning_outcome_ids"])
  self.assertEqual(covered,{f"BIOINST-U04-LO{i:02d}" for i in range(1,6)})
 def test_traceability(self):
  entries={e["id"]:e for e in self.g["entries"]}
  for eid in self.u["glossary_entry_ids"]: self.assertNotEqual(entries[eid]["verification_status"],"unverified"); self.assertTrue(entries[eid]["source_ids"]); self.assertTrue(entries[eid].get("source_locators"))
  claims=[c for c in self.c["claims"] if c.get("unit_id")=="BIOINST-U04"]; self.assertEqual(len(claims),16); self.assertEqual(self.u["claim_ids"],[c["id"] for c in claims]); serialized=json.dumps(self.u,ensure_ascii=False)
  for c in claims: self.assertIn(c["text"],serialized); self.assertEqual(c["review_state"],"ai_review_provisional"); self.assertTrue(c["locator"])
  ids={s["id"] for s in self.s["sources"]}; req={"adi-mt061-inamp-basics","ti-input-common-mode-sloa163","adi-mt047-opamp-noise","adi-an940-low-noise","adi-mt002-nyquist","ti-opamp-swing-overload-2023","hyoung-koo-common-mode-2026"}; self.assertTrue(req.issubset(ids)); self.assertTrue(req.issubset(set(self.u["source_ids"])))
if __name__=="__main__": unittest.main()
