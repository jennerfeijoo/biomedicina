from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomateriales-implantes" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "biomateriales-implantes" / "unit-01.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomaterialesImplantesUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomateriales-implantes")
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertIn("uso previsto", text)
        self.assertIn("matriz de trazabilidad", text)
        self.assertIn("criterio de aceptación", text)

    def test_theory_is_substantive_and_preserves_course_boundaries(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "necesidad clínica",
            "uso previsto",
            "casos de carga",
            "situación peligrosa",
            "evaluación biológica",
            "verificación",
            "validación",
            "trazabilidad",
        ):
            self.assertIn(concept, theory)
        self.assertIn("selección de materiales", theory)
        self.assertIn("unidades 2 a 6", theory)

    def test_core_equations_are_present_with_limits(self) -> None:
        equations = {
            equation["latex"]: equation["meaning"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("\\sigma=\\frac{F}{A_0}", equations)
        self.assertIn("\\varepsilon=\\frac{\\Delta L}{L_0}", equations)
        self.assertIn("modelo simplificado", equations["\\sigma=\\frac{F}{A_0}"].casefold())

    def test_guided_practice_has_progressive_scaffolding_and_synthetic_boundary(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        first = activities[0]
        self.assertGreaterEqual(len(first["instructions"]), 6)
        self.assertGreaterEqual(len(first["problems"]), 12)
        self.assertGreaterEqual(len(first["deliverables"]), 8)
        self.assertGreaterEqual(len(first["checking_criteria"]), 10)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintético", activity_text)
        self.assertIn("no uses historias clínicas", activity_text)
        self.assertIn("apoyo reducido", activity_text)
        self.assertIn("transferencia", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 4)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "necesidad clínica",
            "uso previsto",
            "criterio de aceptación",
            "situación peligrosa",
            "riesgo residual",
            "verificación",
            "validación",
            "trazabilidad",
        ):
            self.assertIn(term, terms)

    def test_sources_use_current_official_references(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://www.iso.org/standard/76810.html", urls)
        self.assertIn("https://www.iso.org/standard/72704.html", urls)
        self.assertIn("https://www.iso.org/standard/10993-1", urls)
        self.assertIn(
            "https://www.fda.gov/medical-devices/postmarket-requirements-devices/quality-management-system-regulation-qmsr",
            urls,
        )
        self.assertIn("https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32017R0745", urls)
        source_titles = " ".join(item["title"] for item in sources)
        self.assertNotIn("ISO 14630:2012", source_titles)
        self.assertIn("ISO 14630:2024", source_titles)
        self.assertIn("ISO 10993-1:2025", source_titles)

    def test_editorial_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no deben usarse como especificaciones de productos reales", notice)
        self.assertIn("sin convertir una actividad educativa", purpose)


if __name__ == "__main__":
    unittest.main()
