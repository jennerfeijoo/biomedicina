from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "desarrollo-dispositivos-medicos" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "desarrollo-dispositivos-medicos" / "unit-04.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class DesarrolloDispositivosMedicosUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "desarrollo-dispositivos-medicos")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_inherited_risk_equation_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("r=p\\times s", self.text)
        for concept in (
            "matriz de verificación",
            "configuración",
            "criterio de aceptación",
            "incertidumbre de medición",
            "regla de decisión",
            "desviación",
        ):
            self.assertIn(concept, self.text)

    def test_theory_is_verification_specific_and_distinguishes_validation(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        self.assertIn("la pregunta central de verificación es específica", theory)
        self.assertIn("la salida de diseño satisface el requisito especificado", theory)
        self.assertIn("validación", theory)
        self.assertIn("necesidades del usuario y uso previsto", theory)
        self.assertIn("peor caso", theory)
        self.assertIn("repetir una prueba solo porque falló", theory)
        self.assertIn("no existe una regla universal", theory)

    def test_measurement_uncertainty_and_tolerance_models_are_explicit(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("U=k\\,u_c", equations)
        self.assertIn("T_{WC}=\\sum_i |T_i|", equations)
        self.assertIn("T_{RSS}\\approx\\sqrt{\\sum_i T_i^2}", equations)
        theory = " ".join(p for section in self.unit["theory_sections"] for p in section["paragraphs"]).casefold()
        self.assertIn("tolerancias del diseño y la incertidumbre de medición son conceptos distintos", theory)
        self.assertIn("jcgm 106", theory)

    def test_progressive_activities_are_synthetic_and_scaffolded(self) -> None:
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
        self.assertIn("no uses pacientes", activity_text)
        self.assertIn("control de riesgo", activity_text)

    def test_glossary_examples_errors_and_assessment_are_substantive(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "verificación",
            "validación",
            "matriz de verificación",
            "mensurando",
            "incertidumbre de medición",
            "regla de decisión",
            "guard band",
            "análisis de impacto",
        ):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_current_where_needed(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn(
            "https://www.fda.gov/medical-devices/postmarket-requirements-devices/quality-management-system-regulation-qmsr",
            urls,
        )
        self.assertIn("https://www.iso.org/standard/59752.html", urls)
        self.assertIn("https://www.nist.gov/pml/nist-technical-note-1297", urls)
        self.assertIn("https://www.bipm.org/documents/20126/2071204/JCGM_106_2012_E.pdf", urls)
        self.assertIn("https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf", urls)
        qmsr = next(item for item in sources if item["title"] == "Quality Management System Regulation (QMSR)")
        self.assertEqual(qmsr["year"], 2026)

    def test_regulatory_and_clinical_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituyen revisión disciplinar humana externa", notice)
        self.assertIn("no deben aplicarse a pacientes", notice)
        self.assertIn("u4 verifica requisitos", notice)
        self.assertIn("u5 aborda validación", notice)
        self.assertIn("sin confundir verificación con validación", purpose)


# Final user-authored trigger after publication synchronized the U4 curriculum descriptor.
if __name__ == "__main__":
    unittest.main()
