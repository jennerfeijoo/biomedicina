from __future__ import annotations

import json
import unittest
from pathlib import Path

# User-authored validation trigger after public-site synchronization.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "ingenieria-clinica-gestion" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "ingenieria-clinica-gestion" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class IngenieriaClinicaGestionUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "ingenieria-clinica-gestion")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed_and_core_domain_is_present(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        for concept in (
            "identificador local del activo",
            "nomenclatura",
            "calidad de datos",
            "criticidad",
            "análisis de sensibilidad",
            "dato faltante",
        ):
            self.assertIn(concept, self.text)

    def test_theory_is_substantive_and_not_a_universal_risk_formula(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        equations = [eq["latex"] for section in sections for eq in section.get("equations", [])]
        self.assertEqual(len(equations), 1)
        self.assertIn("\\sum", equations[0])
        self.assertNotEqual(equations[0], "R=P\\times S")
        self.assertIn("no representa una magnitud física", self.text)

    def test_identity_nomenclature_and_data_quality_are_distinguished(self) -> None:
        glossary = {item["term"].casefold(): item["definition"].casefold() for item in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 20)
        for term in ("udi", "emdn", "gmdn", "diccionario de datos", "completitud", "unicidad", "criticidad"):
            self.assertIn(term, glossary)
        self.assertIn("no identifica por sí sola una unidad física", glossary["modelo"])

    def test_pedagogy_is_scaffolded_reproducible_and_synthetic(self) -> None:
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 4)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 12)
        activity_text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("12 activos", activity_text)
        self.assertIn("no solicites inventarios hospitalarios reales", activity_text)
        self.assertIn("inversión de ranking", self.text)

    def test_sources_are_traceable_and_include_current_guidance(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://www.who.int/publications/i/item/9789240111257", urls)
        self.assertIn("https://www.who.int/teams/health-product-and-policy-standards/assistive-and-medical-technology/medical-devices/nomenclature", urls)
        self.assertIn("https://www.imdrf.org/documents/udi-guidance-unique-device-identification-udi-medical-devices", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/42057968/", urls)

    def test_course_boundaries_and_professional_limits_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no constituye revisión disciplinar externa",
            "datos sintéticos",
            "no como probabilidad de daño",
            "u3 desarrolla mantenimiento",
            "u4 adquisición",
            "u5 seguridad",
        ):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
