from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "desarrollo-dispositivos-medicos" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "desarrollo-dispositivos-medicos" / "unit-05.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class DesarrolloDispositivosMedicosUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "desarrollo-dispositivos-medicos")
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_inherited_risk_equation_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("r=p\\times s", self.text)
        for concept in (
            "validación de diseño",
            "tarea crítica",
            "evaluación biológica",
            "evidencia clínica",
            "datos del mundo real",
            "brecha de evidencia",
        ):
            self.assertIn(concept, self.text)

    def test_theory_has_clear_u4_u5_u6_boundary(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        self.assertIn("la verificación de u4", theory)
        self.assertIn("la validación formula una pregunta diferente", theory)
        self.assertIn("necesidades de usuario", theory)
        self.assertIn("uso previsto", theory)
        self.assertIn("u6", theory)
        self.assertIn("no garantiza", theory)

    def test_human_factors_are_representative_and_synthetic(self) -> None:
        theory = " ".join(p for section in self.unit["theory_sections"] for p in section["paragraphs"]).casefold()
        self.assertIn("usuarios representativos", theory)
        self.assertIn("tarea crítica", theory)
        self.assertIn("error de uso", theory)
        self.assertIn("close call", theory)
        self.assertIn("no reclutará personas", theory)
        self.assertIn("datos personales", theory)
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("\\hat p=\\frac{n_{éxitos}}{n_{intentos}}", equations)
        self.assertIn("\\Delta=\\hat\\theta_{dispositivo}-\\hat\\theta_{comparador}", equations)

    def test_progressive_activities_are_scaffolded_and_non_clinical(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertIn("actividad guiada", activities[0]["title"].casefold())
        self.assertIn("apoyo reducido", activities[1]["title"].casefold())
        self.assertIn("reto autónomo", activities[2]["title"].casefold())
        self.assertGreaterEqual(len(activities[0]["problems"]), 14)
        self.assertGreaterEqual(len(activities[0]["deliverables"]), 8)
        self.assertGreaterEqual(len(activities[0]["checking_criteria"]), 10)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("datos sintéticos", activity_text)
        self.assertIn("no reclutes", activity_text)
        self.assertIn("no uses datos de pacientes", activity_text)
        self.assertIn("qué no permite inferir", activity_text)

    def test_glossary_examples_errors_and_assessment_are_substantive(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "validación de diseño",
            "verificación de diseño",
            "tarea crítica",
            "evaluación biológica",
            "evidencia clínica",
            "evidencia del mundo real",
            "generalización",
            "revalidación",
        ):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_current_where_needed(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn(
            "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/applying-human-factors-and-usability-engineering-medical-devices",
            urls,
        )
        self.assertIn(
            "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-real-world-evidence-support-regulatory-decision-making-medical-devices",
            urls,
        )
        self.assertIn("https://www.iso.org/standard/83968.html", urls)
        self.assertIn(
            "https://www.fda.gov/medical-devices/postmarket-requirements-devices/quality-management-system-regulation-qmsr",
            urls,
        )
        clinical = next(item for item in sources if item["title"].startswith("ISO 14155:2026"))
        self.assertEqual(clinical["year"], 2026)

    def test_editorial_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituyen revisión disciplinar humana externa", notice)
        self.assertIn("no reclutes participantes", notice)
        self.assertIn("no uses datos de pacientes", notice)
        self.assertIn("u4 aporta evidencia de verificación técnica", notice)
        self.assertIn("u5 integra evidencia de validación", notice)
        self.assertIn("u6 queda reservada", notice)
        self.assertIn("sin confundir validación con verificación técnica", purpose)


# Final user-authored trigger after publication synchronized the U5 curriculum descriptor.
if __name__ == "__main__":
    unittest.main()
