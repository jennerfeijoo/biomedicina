from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "bioinstrumentacion"


class BioinstrumentacionUnit09CuratedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.unit = json.loads((COURSE / "units" / "unit-09.json").read_text(encoding="utf-8"))
        self.assessment = json.loads((COURSE / "assessments" / "unit-09.json").read_text(encoding="utf-8"))
        self.glossary = json.loads((COURSE / "glossary.json").read_text(encoding="utf-8"))
        self.sources = json.loads((COURSE / "sources.json").read_text(encoding="utf-8"))
        self.claims = json.loads((COURSE / "claims.json").read_text(encoding="utf-8"))

    def test_u9_is_new_authoring_with_current_regulatory_boundary(self) -> None:
        migration = json.loads((ROOT / "data/course_migrations/bioinstrumentacion-numbering-v1.json").read_text(encoding="utf-8"))
        row = next(item for item in migration["canonical_sequence"] if item["canonical_unit"] == 9)
        self.assertEqual(row["origin"], "new")
        self.assertEqual(row["action"], "author")
        self.assertFalse((ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-09.json").exists())
        notice = self.unit["editorial_notice"].lower()
        self.assertIn("autoría canónica nueva", notice)
        self.assertIn("validación clínica", notice)
        self.assertIn("fuera", notice)

    def test_theory_examples_and_status(self) -> None:
        self.assertEqual(len(self.unit["topics"]), 6)
        self.assertEqual(sum(len(t["subtopics"]) for t in self.unit["topics"]), 18)
        self.assertEqual(len(self.unit["examples"]), 6)
        self.assertEqual(self.unit["status"]["sources"], "traceable")
        self.assertEqual(self.unit["status"]["content"], "in_review")
        self.assertEqual(self.unit["status"]["pedagogy"], "in_review")
        self.assertEqual(self.unit["status"]["internal_review"], "pending")
        self.assertEqual(self.unit["status"]["external_review"], "pending")
        self.assertEqual(self.unit["status"]["publication"], "published_provisional")
        text = json.dumps(self.unit, ensure_ascii=False).lower()
        for marker in ["uso previsto", "trazabilidad bidireccional", "verificación", "validación", "situación peligrosa", "riesgo residual", "discrepancia", "qmsr"]:
            self.assertIn(marker, text)

    def test_activity_has_complete_scaffold_and_no_fake_human_validation(self) -> None:
        activity = self.unit["activities"][0]
        self.assertEqual(activity["status"], "curated_pending_expert_review")
        self.assertEqual(activity["estimated_duration_minutes"], 240)
        self.assertEqual((len(activity["instructions"]), len(activity["tasks"]), len(activity["deliverables"]), len(activity["checking_criteria"])), (5,8,6,10))
        text = " ".join(activity["instructions"] + activity["tasks"] + activity["checking_criteria"]).lower()
        for marker in ["uso previsto educativo", "trazabilidad", "peligro", "usuarios", "no ejecutar estudios con personas", "discrepancias", "autorización de comercialización"]:
            self.assertIn(marker, text)
        self.assertNotIn("reclutar pacientes", text)
        self.assertNotIn("conectar participantes", text)

    def test_assessment_is_case_based_and_covers_all_outcomes(self) -> None:
        self.assertEqual(self.assessment["status"], "curated_pending_expert_review")
        self.assertEqual(len(self.assessment["items"]), 8)
        covered=set()
        for item in self.assessment["items"]:
            self.assertEqual(item["type"], "case_analysis")
            self.assertEqual(item["status"], "curated_pending_expert_review")
            self.assertTrue(item["source_ids"])
            self.assertTrue(item["answer_key"]["explanation"])
            self.assertTrue(item["answer_key"]["common_misconceptions"])
            self.assertTrue(item["feedback"]["correct"])
            self.assertTrue(item["feedback"]["incorrect"])
            covered.update(item["linked_learning_outcome_ids"])
        self.assertEqual(covered, {f"BIOINST-U09-LO{i:02d}" for i in range(1,6)})
        text=json.dumps(self.assessment, ensure_ascii=False).lower()
        self.assertIn("2.4 s", text)
        self.assertIn("desarrolladores", text)
        self.assertIn("qmsr", text)

    def test_glossary_claims_and_sources_are_traceable(self) -> None:
        entries={e["id"]:e for e in self.glossary["entries"]}
        self.assertEqual(len(self.unit["glossary_entry_ids"]),18)
        for eid in self.unit["glossary_entry_ids"]:
            e=entries[eid]
            self.assertIn("BIOINST-U09",e["unit_ids"])
            self.assertNotEqual(e["verification_status"],"unverified")
            self.assertTrue(e["source_ids"])
            self.assertTrue(e.get("source_locators"))
        u9=[c for c in self.claims["claims"] if c.get("unit_id")=="BIOINST-U09"]
        self.assertEqual(len(u9),18)
        self.assertEqual(self.unit["claim_ids"],[c["id"] for c in u9])
        serialized=json.dumps(self.unit, ensure_ascii=False)
        for c in u9:
            self.assertIn(c["text"],serialized)
            self.assertEqual(c["review_state"],"ai_review_provisional")
            self.assertTrue(c["source_id"])
            self.assertTrue(c["locator"])
        required={"nasa-se-handbook-vv-2016","nasa-requirements-traceability","nasa-requirements-appendix","iso-14971-2019-current","fda-qmsr-2026","fda-qmsr-risk-design-2026","fda-human-factors-2026","fda-human-factors-content-2026"}
        source_ids={s["id"] for s in self.sources["sources"]}
        self.assertTrue(required.issubset(source_ids))
        self.assertTrue(required.issubset(set(self.unit["source_ids"])))

    def test_current_qmsr_and_risk_sources_are_not_promoted_to_course_approval(self) -> None:
        source_map={s["id"]:s for s in self.sources["sources"]}
        self.assertIn("2026-02-02",source_map["fda-qmsr-2026"]["locator"])
        self.assertIn("confirmed 2025",source_map["iso-14971-2019-current"]["locator"])
        text=json.dumps(self.unit, ensure_ascii=False).lower()
        self.assertIn("no equivale a demostrar cumplimiento",text)
        self.assertIn("no una etiqueta de 'aprobado para uso clínico'",text)


if __name__ == "__main__":
    unittest.main()
