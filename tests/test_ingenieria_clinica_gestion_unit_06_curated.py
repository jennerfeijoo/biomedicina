from __future__ import annotations

# Final validation trigger after publication and catalog synchronization.

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "ingenieria-clinica-gestion" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "ingenieria-clinica-gestion" / "unit-06.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class IngenieriaClinicaGestionUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "ingenieria-clinica-gestion")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_wrong_risk_equation_are_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertNotIn("R=P\\times S", equations)
        self.assertIn("A=\\frac{T_{disponible}}{T_{observado}}\\times 100\\%", equations)
        self.assertIn("C_{SLA}=\\frac{N_{casos\\ que\\ cumplen}}{N_{casos\\ elegibles}}\\times 100\\%", equations)
        self.assertIn("CSR=\\frac{C_{servicio,anual}}{V_{inventario}}\\times 100\\%", equations)

    def test_theory_covers_measurement_contracts_improvement_and_change(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "definición operacional",
            "medida de balance",
            "tiempo de respuesta",
            "acuerdo de nivel de servicio",
            "plan-do-study-act",
            "probar, implementar y extender",
            "competencia",
            "adopción",
            "sostenibilidad",
            "iso 7101",
        ):
            self.assertIn(concept, theory)
        for boundary in ("u1", "u2", "u3", "u4", "u5", "u6"):
            self.assertIn(boundary, theory)

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 9)
        self.assertGreaterEqual(len(activity["problems"]), 14)
        self.assertGreaterEqual(len(activity["deliverables"]), 9)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 12)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintéticos", text)
        self.assertIn("sla", text)
        self.assertIn("pdsa", text)
        self.assertIn("competencia", text)
        self.assertIn("sostenibilidad", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 28)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "kpi",
            "medida de resultado",
            "medida de proceso",
            "medida de balance",
            "sla",
            "cost of service ratio (csr)",
            "pdsa",
            "implementación",
            "adopción",
            "competencia",
            "sostenibilidad",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_include_current_quality_guidance(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://www.who.int/publications/i/item/9789240111257", urls)
        self.assertIn("https://www.who.int/publications/i/item/9789241501538", urls)
        self.assertIn("https://www.iso.org/standard/81647.html", urls)
        self.assertIn("https://www.ihi.org/library/model-for-improvement", urls)
        self.assertIn("https://www.ihi.org/library/model-for-improvement/establishing-measures", urls)
        self.assertIn("https://www.ihi.org/library/white-papers/ihi-psychology-change-framework", urls)

    def test_contractual_certification_and_real_service_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("asesoría jurídica o contractual", notice)
        self.assertIn("declaración de conformidad con iso 7101", notice)
        self.assertIn("dispositivos reales", notice)
        self.assertIn("datos son sintéticos", notice)
        self.assertIn("contratación", purpose)
        self.assertIn("calidad clínica", purpose)


if __name__ == "__main__":
    unittest.main()
