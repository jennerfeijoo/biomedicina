from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "course_redevelopment" / "biomecanica" / "course.json"
SUBJECT = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "biomecanica.json"
UNIT_DIR = ROOT / "data" / "course_redevelopment" / "biomecanica" / "units"


class BiomecanicaCourseClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.course = json.loads(COURSE.read_text(encoding="utf-8"))
        cls.subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        cls.units = [
            json.loads((UNIT_DIR / f"unit-{index:02d}.json").read_text(encoding="utf-8"))
            for index in range(1, 7)
        ]

    def test_course_and_curriculum_descriptor_match(self) -> None:
        self.assertEqual(self.course, self.subject)
        self.assertEqual(self.course["status"], "review")

    def test_six_curated_units_are_reflected_exactly(self) -> None:
        details = self.course["detailed_units"]
        self.assertEqual(len(details), 6)
        for detail, unit in zip(details, self.units, strict=True):
            self.assertEqual(detail["unit"], unit["unit"])
            self.assertEqual(detail["title"], unit["title"])
            self.assertEqual(detail["description"], unit["purpose"])
            self.assertEqual(detail["learning_outcomes"], unit["learning_objectives"])
            self.assertIn(unit["purpose"], self.course["modules"][unit["unit"] - 1])

    def test_course_outcomes_are_biomechanics_specific(self) -> None:
        text = " ".join(self.course["learning_outcomes"]).casefold()
        for concept in (
            "marcos de referencia",
            "newton-euler",
            "redundancia muscular",
            "viscoelasticidad",
            "semg",
            "cambio mínimo detectable",
            "trazabilidad",
        ):
            self.assertIn(concept, text)
        self.assertNotIn("explica y relaciona los dominios centrales", text)

    def test_guided_activities_cover_every_unit(self) -> None:
        activities = self.course["practical_activities"]
        self.assertEqual(len(activities), 6)
        for index, activity in enumerate(activities, start=1):
            self.assertTrue(activity["title"].startswith(f"Reto {index}:"))
            self.assertIn("sintéticos o material abierto", activity["description"])
            self.assertEqual(activity["type"], "actividad guiada reproducible")

    def test_assessment_plan_is_complete(self) -> None:
        weights = [int(item["weight"].split()[0]) for item in self.course["assessment"]]
        self.assertEqual(sum(weights), 100)
        self.assertEqual(len(self.course["assessment"]), 5)
        titles = " ".join(item["title"] for item in self.course["assessment"]).casefold()
        self.assertIn("proyecto integrador", titles)
        self.assertIn("revisión por pares", titles)

    def test_diagnostic_is_specific_and_non_grading(self) -> None:
        diagnostic = self.course["diagnostic_assessment"]
        self.assertEqual(len(diagnostic["questions"]), 12)
        text = " ".join(diagnostic["questions"]).casefold()
        for concept in ("cuerpo libre", "semg", "módulo material", "cambio mínimo detectable"):
            self.assertIn(concept, text)
        self.assertIn("no se usa como calificación final", diagnostic["purpose"])

    def test_final_project_integrates_u1_to_u6_with_safe_boundaries(self) -> None:
        project = self.course["final_project"]
        self.assertEqual(sum(item["weight_percent"] for item in project["rubric"]), 100)
        requirements = " ".join(project["integration_requirements"]).casefold()
        for unit in range(1, 7):
            self.assertIn(str(unit), requirements)
        project_text = json.dumps(project, ensure_ascii=False).casefold()
        self.assertIn("datos sintéticos o abiertos", project_text)
        self.assertIn("sin intervenir en personas", project_text)
        self.assertIn("diagnóstico", project_text)
        self.assertIn("causalidad", project_text)

    def test_external_review_is_not_claimed(self) -> None:
        principles = " ".join(self.course["assessment_principles"]).casefold()
        criteria = " ".join(self.course["completion_criteria"]).casefold()
        self.assertIn("revisión disciplinar humana externa", principles)
        self.assertIn("revisión disciplinar externa", criteria)
        self.assertIn("validación clínica", criteria)


if __name__ == "__main__":
    unittest.main()
