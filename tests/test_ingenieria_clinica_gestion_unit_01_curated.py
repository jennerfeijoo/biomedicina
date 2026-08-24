from __future__ import annotations

import json
import unittest
from pathlib import Path

# Final user-authored trigger after publication metadata synchronization.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "ingenieria-clinica-gestion" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "ingenieria-clinica-gestion" / "unit-01.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class IngenieriaClinicaGestionUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "ingenieria-clinica-gestion")
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        for concept in ("gestión de tecnologías sanitarias", "ciclo de vida", "raci", "gobernanza", "handoff", "trazabilidad"):
            self.assertIn(concept, self.text)

    def test_theory_is_substantive_and_respects_course_boundaries(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        purpose = self.unit["purpose"].casefold()
        self.assertIn("mantenimiento operativo detallado", purpose)
        notice = self.unit["editorial_notice"].casefold()
        for boundary in ("u2", "u3", "u4", "u5", "u6"):
            self.assertIn(boundary, notice)

    def test_pedagogy_is_scaffolded_and_synthetic(self) -> None:
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 4)
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 10)
        self.assertGreaterEqual(len(activity["deliverables"]), 6)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        activity_text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintético", activity_text)
        self.assertIn("no intervengas equipos médicos", activity_text)

    def test_sources_are_traceable_and_current_sources_are_present(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://www.who.int/publications/i/item/9789240111257", urls)
        self.assertIn("https://www.who.int/publications/i/item/9789241565479", urls)
        self.assertIn("https://ced.ifmbe.org/resources/clinical-engineering-definitions/", urls)
        self.assertIn("https://accenet.org/about/Pages/ClinicalEngineer.aspx", urls)

    def test_professional_and_clinical_limits_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no constituye revisión disciplinar externa",
            "certificación profesional",
            "conformidad regulatoria",
            "validación clínica",
            "no requieren acceso a pacientes",
        ):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
