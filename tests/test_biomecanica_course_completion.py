from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "biomecanica"


class BiomecanicaCourseCompletionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.course = json.loads((COURSE / "course.json").read_text(encoding="utf-8"))
        cls.assessment = json.loads(
            (COURSE / "assessments" / "course-assessment.json").read_text(encoding="utf-8")
        )

    def test_course_is_complete_but_human_review_remains_pending(self) -> None:
        status = self.course["status"]
        self.assertEqual(self.course["content_version"], "1.0.0")
        self.assertEqual(status["content"], "complete")
        self.assertEqual(status["sources"], "traceable")
        self.assertEqual(status["pedagogy"], "complete")
        self.assertEqual(status["multimedia"], "planned")
        self.assertEqual(status["internal_review"], "pending")
        self.assertEqual(status["external_review"], "pending")
        self.assertEqual(status["publication"], "published_provisional")
        self.assertEqual(len(self.course["unit_files"]), 6)
        notice = self.course["editorial_notice"].casefold()
        self.assertIn("revisión humana interna", notice)
        self.assertIn("revisión disciplinaria externa", notice)

    def test_course_assessment_weights_and_outcome_coverage_are_complete(self) -> None:
        outcomes = {item["id"] for item in self.course["learning_outcomes"]}
        plan = self.assessment["assessment_plan"]
        plan_outcomes = {
            outcome_id
            for item in plan
            for outcome_id in item["linked_learning_outcome_ids"]
        }
        self.assertEqual(self.assessment["status"], "curated_pending_expert_review")
        self.assertEqual(sum(item["weight_percent"] for item in plan), 100)
        self.assertEqual(plan_outcomes, outcomes)
        self.assertTrue(all(item.get("feedback_and_revision") for item in plan))

    def test_diagnostic_is_biomechanics_specific_and_actionable(self) -> None:
        diagnostic = self.assessment["diagnostic"]
        self.assertEqual(diagnostic["scoring"]["maximum_points"], 12)
        self.assertEqual(len(diagnostic["questions"]), 12)
        domains = {item["domain"] for item in diagnostic["questions"]}
        for domain in (
            "vectores y marcos",
            "cuerpo libre",
            "momento",
            "muestreo",
            "EMG y fuerza",
            "dinámica inversa",
            "incertidumbre",
            "límites de inferencia",
        ):
            self.assertIn(domain, domains)
        self.assertGreaterEqual(len(diagnostic["interpretation"]), 3)
        self.assertTrue(all(item["action"] for item in diagnostic["interpretation"]))

    def test_midterm_blueprint_is_balanced_and_traceable(self) -> None:
        blueprint = self.assessment["midterm_blueprint"]
        self.assertEqual(sum(item["weight_percent"] for item in blueprint), 100)
        self.assertGreaterEqual(len(blueprint), 4)
        linked = {oid for item in blueprint for oid in item["learning_outcome_ids"]}
        for required in ("BIOMEC-LO01", "BIOMEC-LO02", "BIOMEC-LO03", "BIOMEC-LO05"):
            self.assertIn(required, linked)

    def test_capstone_integrates_all_outcomes_and_has_complete_rubric(self) -> None:
        outcomes = {item["id"] for item in self.course["learning_outcomes"]}
        capstone = self.assessment["capstone"]
        self.assertEqual(set(capstone["linked_learning_outcome_ids"]), outcomes)
        self.assertGreaterEqual(len(capstone["phases"]), 6)
        self.assertGreaterEqual(len(capstone["deliverables"]), 10)
        self.assertGreaterEqual(len(capstone["integration_requirements"]), 6)
        deliverable_ids = {item["id"] for item in capstone["deliverables"]}
        self.assertEqual(len(deliverable_ids), len(capstone["deliverables"]))
        rubric = capstone["rubric"]
        self.assertEqual(sum(item["weight_percent"] for item in rubric), 100)
        self.assertGreaterEqual(len(rubric), 5)
        for item in rubric:
            for level in ("excellent", "competent", "developing", "insufficient"):
                self.assertTrue(item[level])

    def test_capstone_keeps_measurement_model_and_clinical_layers_separate(self) -> None:
        text = json.dumps(self.assessment["capstone"], ensure_ascii=False).casefold()
        for concept in (
            "cinemático",
            "cinético",
            "musculoesquelética",
            "tisular",
            "medición",
            "sensibilidad",
            "reproducible",
        ):
            self.assertIn(concept, text)
        self.assertIn("sin diagnosticar", text)
        self.assertIn("causalidad clínica", text)

    def test_all_canonical_units_keep_traceability_and_review_boundaries(self) -> None:
        for relative in self.course["unit_files"]:
            unit = json.loads((COURSE / relative).read_text(encoding="utf-8"))
            status = unit["status"]
            self.assertEqual(status["content"], "complete")
            self.assertEqual(status["sources"], "traceable")
            self.assertEqual(status["pedagogy"], "complete")
            self.assertEqual(status["internal_review"], "pending")
            self.assertEqual(status["external_review"], "pending")
            self.assertEqual(status["publication"], "published_provisional")
            self.assertTrue(unit["learning_outcomes"])
            self.assertTrue(unit["activities"])
            self.assertTrue(unit["claim_ids"])

    def test_completion_is_not_presented_as_professional_validation(self) -> None:
        text = (
            json.dumps(self.course, ensure_ascii=False)
            + json.dumps(self.assessment, ensure_ascii=False)
        ).casefold()
        self.assertIn("no constituyen diagnóstico", text)
        self.assertIn("revisión disciplinaria externa", text)
        self.assertNotIn("validado por expertos", text)
        self.assertNotIn("aprobado para decisiones clínicas", text)


if __name__ == "__main__":
    unittest.main()
