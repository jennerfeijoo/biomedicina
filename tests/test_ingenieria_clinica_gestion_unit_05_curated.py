from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "ingenieria-clinica-gestion" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "ingenieria-clinica-gestion" / "unit-05.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class IngenieriaClinicaGestionUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "ingenieria-clinica-gestion")
        self.assertEqual(self.unit["unit"], 5)
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
        self.assertIn("\\text{tasa de eventos}=\\frac{n_{eventos}}{E}", equations)

    def test_theory_covers_incident_lifecycle_and_course_boundaries(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "preservación de evidencia",
            "reporte interno",
            "jurisdicción",
            "imdrf",
            "denominador",
            "subnotificación",
            "acción correctiva",
        ):
            self.assertIn(concept, theory)
        self.assertIn("u2", theory)
        self.assertIn("u3", theory)
        self.assertIn("u6", theory)

    def test_guided_activity_is_scaffolded_synthetic_and_non_regulatory(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 8)
        self.assertGreaterEqual(len(activity["problems"]), 14)
        self.assertGreaterEqual(len(activity["deliverables"]), 9)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 12)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintético", text)
        self.assertIn("no contactes fabricantes", text)
        self.assertIn("imdrf", text)
        self.assertIn("denominador", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 28)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "incidente",
            "problema del dispositivo",
            "señal de seguridad",
            "denominador de exposición",
            "preservación de evidencia",
            "investigación de fallos",
            "imdrf a–g",
            "fsca",
            "acción correctiva",
            "criterio de efectividad",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_current_methodology_is_present(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://www.who.int/publications/i/item/9789240010338", urls)
        self.assertIn("https://www.who.int/publications-detail-redirect/WHO-HIS-SDS-2016.22", urls)
        self.assertIn(
            "https://www.imdrf.org/documents/terminologies-categorized-adverse-event-reporting-aer-terms-terminology-and-codes",
            urls,
        )
        self.assertIn("https://www.imdrf.org/working-groups/adverse-event-terminology/combined-codes", urls)
        self.assertIn(
            "https://www.fda.gov/medical-devices/mandatory-reporting-requirements-manufacturers-importers-and-device-user-facilities/emdr-electronic-medical-device-reporting",
            urls,
        )

    def test_regulatory_and_real_case_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("decisión de reportabilidad", notice)
        self.assertIn("dispositivos reales", notice)
        self.assertIn("ejemplos jurisdiccionales", notice)
        self.assertIn("investigación oficial", purpose)
        self.assertIn("autorización de retorno al servicio", purpose)


if __name__ == "__main__":
    unittest.main()
