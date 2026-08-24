from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biosensores" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "biosensores" / "unit-01.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiosensoresUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biosensores")
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "mensurando",
            "reconocimiento biológico",
            "transductor",
            "calibración",
            "matriz",
            "saturación",
        ):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_preserves_unit_boundaries(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "cadena de medición",
            "bioreceptor",
            "transductor",
            "fondo",
            "interferente",
            "saturación",
            "incertidumbre",
        ):
            self.assertIn(concept, theory)
        self.assertIn("u2", theory)
        self.assertIn("u3", theory)
        self.assertIn("u5", theory)

    def test_core_equations_are_present_with_explicit_limits(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("y=y_0+S\\,c", equations)
        self.assertIn("\\theta=\\frac{c}{K_D+c}", equations)
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertIn("aproximadamente lineal", text)
        self.assertIn("modelo de langmuir ideal", text)
        self.assertIn("no describe todos los biosensores", text)

    def test_guided_activity_is_scaffolded_synthetic_and_reproducible(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 10)
        self.assertGreaterEqual(len(activity["deliverables"]), 6)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 8)
        activity_text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintético", activity_text)
        self.assertIn("muestras humanas", activity_text)
        self.assertIn("diagrama de bloques", activity_text)
        self.assertIn("no-diana", activity_text)
        self.assertIn("diagnóstico", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 19)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 4)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 8)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "biosensor",
            "analito",
            "mensurando",
            "transductor",
            "curva de calibración",
            "efecto de matriz",
        ):
            self.assertIn(term, terms)

    def test_sources_are_traceable_directly_verified_and_disciplinary(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://goldbook.iupac.org/terms/view/B00663",
            "https://publications.iupac.org/pac/71/12/2333/index.html",
            "https://pubmed.ncbi.nlm.nih.gov/23420144/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC3663003/",
            "https://pubmed.ncbi.nlm.nih.gov/14021529/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC6416154/",
            "https://www.fda.gov/medical-devices/ivd-regulatory-assistance/overview-ivd-regulation",
        ):
            self.assertIn(url, urls)

    def test_analytical_clinical_and_regulatory_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        theory = " ".join(p for section in self.unit["theory_sections"] for p in section["paragraphs"]).casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("validación analítica o clínica", notice)
        self.assertIn("datos y escenarios sintéticos", notice)
        self.assertIn("utilidad clínica", purpose)
        self.assertIn("desempeño clínico", theory)
        self.assertIn("conformidad regulatoria", theory)


if __name__ == "__main__":
    unittest.main()
