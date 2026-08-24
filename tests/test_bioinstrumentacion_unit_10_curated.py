from __future__ import annotations

import json
import unittest
from pathlib import Path

# Final clean-head gate trigger; this comment changes no academic behavior.
ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "bioinstrumentacion"


class BioinstrumentacionUnit10CuratedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.unit = json.loads((COURSE / "units" / "unit-10.json").read_text(encoding="utf-8"))
        self.assessment = json.loads((COURSE / "assessments" / "unit-10.json").read_text(encoding="utf-8"))
        self.glossary = json.loads((COURSE / "glossary.json").read_text(encoding="utf-8"))
        self.sources = json.loads((COURSE / "sources.json").read_text(encoding="utf-8"))
        self.claims = json.loads((COURSE / "claims.json").read_text(encoding="utf-8"))

    def test_u10_is_new_authoring_and_final_integration_unit(self) -> None:
        migration = json.loads((ROOT / "data/course_migrations/bioinstrumentacion-numbering-v1.json").read_text(encoding="utf-8"))
        row = next(item for item in migration["canonical_sequence"] if item["canonical_unit"] == 10)
        self.assertEqual(row["origin"], "new")
        self.assertEqual(row["action"], "author")
        self.assertFalse((ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-10.json").exists())
        self.assertEqual(self.unit["prerequisite_unit_ids"], ["BIOINST-U09"])
        notice = self.unit["editorial_notice"].lower()
        self.assertIn("integra las nueve unidades previas", notice)
        self.assertIn("revisión humana", notice)

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
        for marker in ["arquitectura", "presupuestos", "baseline", "procedencia", "reproducibilidad computacional", "manifiesto", "análisis de impacto", "cierre"]:
            self.assertIn(marker, text)

    def test_capstone_activity_is_reproducible_and_auditable(self) -> None:
        activity = self.unit["activities"][0]
        self.assertEqual(activity["status"], "curated_pending_expert_review")
        self.assertGreaterEqual(activity["estimated_duration_minutes"], 240)
        self.assertEqual((len(activity["instructions"]), len(activity["tasks"]), len(activity["deliverables"]), len(activity["checking_criteria"])), (5,8,6,10))
        text = " ".join(activity["instructions"] + activity["tasks"] + activity["checking_criteria"]).lower()
        for marker in ["u1–u9", "baseline", "hash", "entorno limpio", "procedencia", "cambio", "discrepancias", "revisión humana"]:
            self.assertIn(marker, text)
        self.assertIn("no usar personas ni hardware médico energizado", text)
        self.assertIn("no se sobrescriben", text)

    def test_assessment_is_integrative_and_covers_all_outcomes(self) -> None:
        self.assertEqual(self.assessment["status"], "curated_pending_expert_review")
        self.assertEqual(len(self.assessment["items"]), 8)
        covered=set()
        for item in self.assessment["items"]:
            self.assertEqual(item["type"], "case_analysis")
            self.assertEqual(item["status"], "curated_pending_expert_review")
            self.assertTrue(item["source_ids"])
            self.assertTrue(item["answer_key"]["explanation"])
            self.assertTrue(item["answer_key"]["common_misconceptions"])
            covered.update(item["linked_learning_outcome_ids"])
        self.assertEqual(covered, {f"BIOINST-U10-LO{i:02d}" for i in range(1,6)})
        text=json.dumps(self.assessment, ensure_ascii=False).lower()
        for marker in ["±2.5 v", "etiquetado v1.0", "raw.csv", "otra máquina", "se cambia el sensor", "se borra el resultado fallido", "uso clínico"]:
            self.assertIn(marker, text)

    def test_glossary_claims_and_sources_are_traceable(self) -> None:
        entries={e["id"]:e for e in self.glossary["entries"]}
        self.assertEqual(len(self.unit["glossary_entry_ids"]),18)
        for eid in self.unit["glossary_entry_ids"]:
            e=entries[eid]
            self.assertIn("BIOINST-U10",e["unit_ids"])
            self.assertNotEqual(e["verification_status"],"unverified")
            self.assertTrue(e["source_ids"])
            self.assertTrue(e.get("source_locators"))
        u10=[c for c in self.claims["claims"] if c.get("unit_id")=="BIOINST-U10"]
        self.assertEqual(len(u10),18)
        self.assertEqual(self.unit["claim_ids"],[c["id"] for c in u10])
        serialized=json.dumps(self.unit, ensure_ascii=False)
        for c in u10:
            self.assertIn(c["text"],serialized)
            self.assertEqual(c["review_state"],"ai_review_provisional")
            self.assertTrue(c["source_id"])
            self.assertTrue(c["locator"])
        required={"nasa-configuration-management","nasa-technical-data-management","nasa-npr-7123-1b-cm","w3c-prov-primer","nist-rdaf-1500-18r2","nasem-reproducibility-2019","nih-reproducibility-2026"}
        source_ids={s["id"] for s in self.sources["sources"]}
        self.assertTrue(required.issubset(source_ids))
        self.assertTrue(required.issubset(set(self.unit["source_ids"])))

    def test_reproducibility_does_not_become_regulatory_or_clinical_approval(self) -> None:
        text=json.dumps(self.unit, ensure_ascii=False).lower()
        self.assertIn("no demuestra por sí solo conformidad", text)
        self.assertIn("validez clínica", text)
        activity=json.dumps(self.unit["activities"][0], ensure_ascii=False).lower()
        self.assertIn("niega que el expediente demuestre conformidad, seguridad o validez clínica",activity)
        self.assertNotIn("aprobado para pacientes",text)


if __name__ == "__main__":
    unittest.main()
