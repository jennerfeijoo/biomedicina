from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "economia-gestion-empresas"
CODE = "EGE"
CANON = ROOT / "data" / "courses" / COURSE_ID
REDEV = ROOT / "data" / "course_redevelopment" / COURSE_ID / "units"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class EconomiaGestionEmpresasCourseCompletionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.course = json.loads((CANON / "course.json").read_text(encoding="utf-8"))
        cls.sources = json.loads((CANON / "sources.json").read_text(encoding="utf-8"))
        cls.claims = json.loads((CANON / "claims.json").read_text(encoding="utf-8"))
        cls.glossary = json.loads((CANON / "glossary.json").read_text(encoding="utf-8"))
        cls.media = json.loads((CANON / "media.json").read_text(encoding="utf-8"))

    def test_course_is_complete_but_human_review_stays_pending(self):
        status = self.course["status"]
        self.assertEqual(status["content"], "complete")
        self.assertEqual(status["sources"], "traceable")
        self.assertEqual(status["pedagogy"], "complete")
        self.assertEqual(status["multimedia"], "planned")
        self.assertEqual(status["internal_review"], "pending")
        self.assertEqual(status["external_review"], "pending")
        self.assertEqual(status["publication"], "published_provisional")

    def test_six_units_preserve_all_authored_theory_and_equations(self):
        for n in range(1, 7):
            source = json.loads((REDEV / f"unit-{n:02d}.json").read_text(encoding="utf-8"))
            canonical_path = CANON / "units" / f"unit-{n:02d}.json"
            canonical_text = canonical_path.read_text(encoding="utf-8")
            canonical = json.loads(canonical_text)
            self.assertNotIn(GENERIC, canonical_text.casefold())
            self.assertEqual(canonical["id"], f"{CODE}-U{n:02d}")
            self.assertEqual(canonical["status"]["content"], "complete")
            self.assertGreaterEqual(len(canonical["activities"]), 3)
            for section in source["theory_sections"]:
                for paragraph in section["paragraphs"]:
                    self.assertIn(paragraph, canonical_text)
                for equation in section.get("equations", []):
                    self.assertIn(equation["latex"], {block["latex"] for topic in canonical["topics"] for block in topic["blocks"] if block.get("type") == "equation"})
            for objective in source["learning_objectives"]:
                self.assertIn(objective, canonical_text)

    def test_assessments_are_recoverable_and_substantive(self):
        for n in range(1, 7):
            payload = json.loads((CANON / "assessments" / f"unit-{n:02d}.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(len(payload["items"]), 10)
            self.assertTrue(all(item["difficulty"] != "unclassified" for item in payload["items"]))
            self.assertTrue(all(item["cognitive_level"] != "unclassified" for item in payload["items"]))
            self.assertTrue(all(item["answer_key"]["explanation"] for item in payload["items"]))
            self.assertTrue(all(item["feedback"]["incorrect"] for item in payload["items"]))
            self.assertTrue(all(item["source_ids"] for item in payload["items"]))

    def test_course_assessment_integrates_u1_to_u6(self):
        payload = json.loads((CANON / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))
        self.assertEqual(sum(x["weight_percent"] for x in payload["assessment_plan"]), 100)
        self.assertEqual(sum(x["weight_percent"] for x in payload["midterm_blueprint"]), 100)
        self.assertEqual(sum(x["weight_percent"] for x in payload["capstone"]["rubric"]), 100)
        self.assertGreaterEqual(len(payload["diagnostic"]["questions"]), 12)
        capstone = json.dumps(payload["capstone"], ensure_ascii=False).casefold()
        for concept in ("coste de oportunidad", "flujo de caja", "cuello de botella", "segmentación", "icer", "gobernanza"):
            self.assertIn(concept, capstone)

    def test_sources_glossary_claims_and_media_are_complete(self):
        sources = self.sources["sources"]
        self.assertGreaterEqual(len(sources), 20)
        self.assertTrue(all(s["verification_status"] == "verified_directly" for s in sources))
        self.assertEqual(self.sources["coverage_gaps"], [])
        self.assertEqual(self.sources["coverage_status"], "traceable")
        self.assertGreaterEqual(len(self.glossary["entries"]), 80)
        self.assertEqual(len(self.claims["claims"]), 24)
        self.assertTrue(all(c["source_verification_status"] == "verified_directly" for c in self.claims["claims"]))
        self.assertEqual(len(self.media["items"]), 6)
        self.assertTrue(all(item["status"] == "planned" for item in self.media["items"]))

    def test_claims_are_literal_content_and_cross_links_resolve(self):
        source_ids = {s["id"] for s in self.sources["sources"]}
        claim_ids = {c["id"] for c in self.claims["claims"]}
        glossary_ids = {g["id"] for g in self.glossary["entries"]}
        for claim in self.claims["claims"]:
            unit_text = (CANON / "units" / f"unit-{claim['unit']:02d}.json").read_text(encoding="utf-8")
            self.assertIn(claim["text"], unit_text)
            self.assertIn(claim["source_id"], source_ids)
        for n in range(1, 7):
            unit = json.loads((CANON / "units" / f"unit-{n:02d}.json").read_text(encoding="utf-8"))
            self.assertTrue(set(unit["claim_ids"]).issubset(claim_ids))
            self.assertTrue(set(unit["source_ids"]).issubset(source_ids))
            self.assertTrue(set(unit["glossary_entry_ids"]).issubset(glossary_ids))

    def test_professional_boundaries_remain_explicit(self):
        notice = self.course["editorial_notice"].casefold()
        for phrase in ("revisión humana", "asesoría económica", "hta oficial", "certificación", "conformidad regulatoria", "validación clínica"):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
