from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "fundamentos-biomecanica" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "fundamentos-biomecanica" / "unit-06.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class FundamentosBiomecanicaUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "fundamentos-biomecanica")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "mensurando",
            "trazabilidad metrológica",
            "calibración espacial",
            "markerless",
            "plataforma de fuerza",
            "centro de presión",
            "imu",
            "sincronización",
            "aliasing",
            "incertidumbre",
        ):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_measurement_focused(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory_words = sum(
            len(paragraph.split())
            for section in sections
            for paragraph in section["paragraphs"]
        )
        self.assertGreaterEqual(theory_words, 1150)
        theory = " ".join(
            paragraph for section in sections for paragraph in section["paragraphs"]
        ).casefold()
        self.assertIn("la variable final suele ser resultado de varias transformaciones", theory)
        self.assertIn("correlación alta no implica acuerdo", theory)
        self.assertIn("asignaturas prácticas posteriores", theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("f_s>2f_{max}", equations)
        self.assertIn("x_{CoP}=-\\frac{M_y}{F_z}", equations)
        self.assertIn("\\Delta N=f_s\\Delta t", equations)
        self.assertIn(
            "u_y^2\\approx\\sum_i\\left(\\frac{\\partial f}{\\partial x_i}\\right)^2u_{x_i}^2",
            equations,
        )

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 6)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 6)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintéticos", text)
        self.assertIn("no grabes personas", text)
        self.assertIn("cop", text)
        self.assertIn("imu", text)
        self.assertIn("sincronización", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "mensurando",
            "trazabilidad metrológica",
            "captura markerless",
            "plataforma de fuerza",
            "imu",
            "sincronización",
            "incertidumbre de medición",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_relevant(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://isbweb.org/activities/standards", urls)
        self.assertIn("https://www.nist.gov/calibrations/traceability", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/34283131/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/18755590/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/41418505/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/34698600/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/38894476/", urls)

    def test_scope_boundary_is_explicit(self) -> None:
        purpose = self.unit["purpose"].casefold()
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("laboratorio de biomecánica", purpose)
        self.assertIn("no constituyen revisión disciplinar externa", notice)
        self.assertIn("no requieren grabar personas", notice)
        self.assertIn("certificación metrológica", notice)
        self.assertIn("diagnóstico", notice)
        self.assertIn("prescripción", notice)


# Final verification trigger after regression repair.
if __name__ == "__main__":
    unittest.main()
