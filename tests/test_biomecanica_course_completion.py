from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_PATH = ROOT / "data" / "course_redevelopment" / "biomecanica" / "course.json"
UNITS_DIR = ROOT / "data" / "course_redevelopment" / "biomecanica" / "units"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"
OUTCOMES = {f"LO{i:02d}" for i in range(1, 8)}

# Final user-authored trigger after publication synchronization.


def weight(value: str) -> float:
    match = re.search(r"\d+(?:[.,]\d+)?", value)
    if not match:
        raise AssertionError(f"Ponderación inválida: {value!r}")
    return float(match.group(0).replace(",", "."))


class BiomecanicaCourseCompletionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.course = json.loads(COURSE_PATH.read_text(encoding="utf-8"))
        cls.units = [
            json.loads((UNITS_DIR / f"unit-{number:02d}.json").read_text(encoding="utf-8"))
            for number in range(1, 7)
        ]

    def test_course_is_content_complete_but_human_review_remains_pending(self) -> None:
        self.assertEqual(self.course["status"], "review")
        state = self.course["completion_state"]
        self.assertEqual(state["content"], "complete")
        self.assertEqual(state["pedagogy"], "complete")
        self.assertEqual(state["unit_sources"], "traceable")
        self.assertEqual(state["internal_review"], "pending")
        self.assertEqual(state["external_review"], "pending")
        self.assertEqual(state["publication"], "published_provisional")

    def test_all_six_units_are_curated_and_descriptor_matches_source(self) -> None:
        detailed = self.course["detailed_units"]
        self.assertEqual(len(detailed), 6)
        self.assertEqual([item["unit"] for item in detailed], list(range(1, 7)))
        for descriptor, unit in zip(detailed, self.units, strict=True):
            self.assertEqual(unit["status"], "review")
            self.assertEqual(descriptor["title"], unit["title"])
            self.assertEqual(descriptor["description"], unit["purpose"])
            self.assertEqual(descriptor["learning_outcomes"], unit["learning_objectives"])
            text = json.dumps(unit, ensure_ascii=False).casefold()
            self.assertNotIn(GENERIC, text)

    def test_course_descriptor_is_disciplinary_not_template_level(self) -> None:
        text = COURSE_PATH.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "marcos de referencia",
            "newton-euler",
            "redundancia muscular",
            "viscoelasticidad",
            "semg",
            "gait profile score",
            "revised niosh lifting equation",
        ):
            self.assertIn(concept, text)
        self.assertNotIn("definir marcha patológica, ergonomía y prótesis", text)

    def test_assessment_sums_to_100_and_covers_every_course_outcome(self) -> None:
        components = self.course["assessment"]
        self.assertEqual(len(components), 5)
        self.assertAlmostEqual(sum(weight(item["weight"]) for item in components), 100.0)
        covered = {outcome for item in components for outcome in item["mapped_outcomes"]}
        self.assertEqual(covered, OUTCOMES)
        mapping = self.course["assessment_mapping"]
        self.assertEqual(set(mapping), OUTCOMES)
        self.assertTrue(all(mapping[outcome] for outcome in OUTCOMES))

    def test_capstone_integrates_all_units_and_all_outcomes(self) -> None:
        project = self.course["final_project"]
        self.assertEqual(set(project["mapped_outcomes"]), OUTCOMES)
        requirements = " ".join(project["integration_requirements"]).casefold()
        for unit in ("u1", "u2", "u3", "u4", "u5", "u6"):
            self.assertIn(unit, requirements)
        self.assertGreaterEqual(len(project["phases"]), 6)
        self.assertGreaterEqual(len(project["deliverables"]), 8)
        rubric = project["rubric"]
        self.assertEqual(sum(item["weight_percent"] for item in rubric), 100)
        for item in rubric:
            for level in ("excellent", "proficient", "developing", "insufficient"):
                self.assertTrue(item[level].strip())

    def test_each_unit_retains_full_pedagogical_and_reference_contract(self) -> None:
        for unit in self.units:
            self.assertGreaterEqual(len(unit["learning_objectives"]), 5)
            self.assertGreaterEqual(len(unit["theory_sections"]), 4)
            self.assertGreaterEqual(len(unit["glossary"]), 12)
            self.assertGreaterEqual(len(unit["worked_examples"]), 2)
            self.assertGreaterEqual(len(unit["common_errors"]), 5)
            self.assertGreaterEqual(len(unit["self_assessment"]), 8)
            self.assertGreaterEqual(len(unit["sources"]), 5)
            self.assertGreaterEqual(len(unit["guided_activities"]), 1)

    def test_course_core_resources_are_traceable(self) -> None:
        resources = self.course["core_resources"]
        self.assertGreaterEqual(len(resources), 7)
        self.assertTrue(all(item["url"].startswith("https://") for item in resources))
        self.assertTrue(all(item["verification_status"] == "verified_directly" for item in resources))
        urls = {item["url"] for item in resources}
        self.assertIn("https://www.isbweb.org/activities/standards", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/28821242/", urls)
        self.assertIn("https://www.cdc.gov/niosh/ergonomics/about/rnle.html", urls)

    def test_completion_never_becomes_external_or_clinical_validation(self) -> None:
        notice = self.course["editorial_notice"].casefold()
        self.assertIn("revisión humana interna", notice)
        self.assertIn("revisión disciplinar externa", notice)
        self.assertIn("no se han realizado", notice)
        for boundary in (
            "diagnóstico",
            "prescripción",
            "prótesis/órtesis",
            "aptitud laboral",
            "eficacia clínica",
        ):
            self.assertIn(boundary, notice)


if __name__ == "__main__":
    unittest.main()
