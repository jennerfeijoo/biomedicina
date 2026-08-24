from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "desarrollo-dispositivos-medicos" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "desarrollo-dispositivos-medicos" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class DesarrolloDispositivosMedicosUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "desarrollo-dispositivos-medicos")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed_and_scope_is_specific(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "design input",
            "trazabilidad bidireccional",
            "arquitectura",
            "interfaz",
            "criterio de aceptación",
            "factores humanos",
        ):
            self.assertIn(concept, text)

    def test_theory_separates_requirements_architecture_and_later_units(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "requisitos sin fuente",
            "gold plating",
            "requisito derivado",
            "frontera del sistema",
            "método de verificación previsto",
            "sistema de uso",
            "análisis de impacto",
        ):
            self.assertIn(concept, theory)
        self.assertIn("u3", theory)
        self.assertIn("u4", theory)
        self.assertIn("u5", theory)

    def test_progressive_activities_are_synthetic_and_scaffolded(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertGreaterEqual(len(activities[0]["problems"]), 10)
        self.assertGreaterEqual(len(activities[0]["checking_criteria"]), 8)
        self.assertGreaterEqual(len(activities[1]["problems"]), 5)
        self.assertGreaterEqual(len(activities[2]["problems"]), 5)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("ficticio", activity_text)
        self.assertIn("no uses datos de pacientes", activity_text)
        self.assertIn("apoyo reducido", activities[1]["title"].casefold())
        self.assertIn("autónomo", activities[2]["title"].casefold())

    def test_glossary_examples_errors_and_assessment_are_substantive(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "design input",
            "criterio de aceptación",
            "trazabilidad bidireccional",
            "requisito huérfano",
            "arquitectura del sistema",
            "interfaz",
            "análisis de impacto",
        ):
            self.assertIn(term, terms)

    def test_sources_are_current_traceable_and_authoritative(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn(
            "https://www.fda.gov/medical-devices/postmarket-requirements-devices/quality-management-system-regulation-qmsr",
            urls,
        )
        self.assertIn(
            "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/applying-human-factors-and-usability-engineering-medical-devices",
            urls,
        )
        self.assertIn(
            "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/content-premarket-submissions-device-software-functions",
            urls,
        )
        self.assertIn("https://www.iso.org/standard/59752.html", urls)
        self.assertIn("https://www.nasa.gov/reference/6-2-requirements-management/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/9099433/", urls)

    def test_regulatory_and_clinical_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar humana externa", notice)
        self.assertIn("2 de febrero de 2026", notice)
        self.assertIn("no uses especificaciones confidenciales ni datos de pacientes", notice)
        self.assertIn("u3 aborda gestión formal de riesgos", notice)
        self.assertIn("u4 ejecuta verificación", notice)
        self.assertIn("u5 aborda validación", notice)
        self.assertIn("sin confundir requisitos con soluciones prematuras", purpose)


# Final gate trigger; the theory uses the explicit phrase "requisitos sin fuente" while the glossary names that defect "requisito huérfano".
if __name__ == "__main__":
    unittest.main()
