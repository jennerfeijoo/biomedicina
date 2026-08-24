from __future__ import annotations

import json
import unittest
from pathlib import Path

# User-authored validation trigger after generated-site synchronization.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "laboratorio-biomecanica" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "laboratorio-biomecanica" / "unit-01.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class LaboratorioBiomecanicaUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "laboratorio-biomecanica")
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_dynamics_equation_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("\\sum \\mathbf{f}=m\\mathbf{a}", self.text)
        self.assertNotIn("\\sum \\mathbf f=m\\mathbf a", self.text)
        for concept in (
            "pregunta de medición",
            "sistemas de coordenadas",
            "calibración",
            "verificación",
            "trazabilidad metrológica",
            "incertidumbre",
        ):
            self.assertIn(concept, self.text)

    def test_theory_is_substantive_and_protocol_focused(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        self.assertIn("unidad de análisis", theory)
        self.assertIn("volumen de medición", theory)
        self.assertIn("presupuesto de incertidumbre", theory)
        self.assertIn("metadatos", theory)
        self.assertIn("no son sinónimos", theory)

    def test_coordinate_and_quality_control_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("\\mathbf r_B=\\mathbf R_{BA}\\mathbf r_A+\\mathbf p_{BA}", equations)
        self.assertIn("\\mathbf R^{\\mathsf T}\\mathbf R=\\mathbf I,\\qquad \\det(\\mathbf R)=+1", equations)
        self.assertIn("e_{rel}=\\frac{|d_{meas}-d_{ref}|}{d_{ref}}", equations)
        self.assertTrue(any("\\mathrm{RMSE}" in equation for equation in equations))
        self.assertTrue(any("u_c(y)" in equation for equation in equations))

    def test_guided_activity_is_scaffolded_reproducible_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 6)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 12)
        activity_text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("no grabes personas", activity_text)
        self.assertIn("coordenadas", activity_text)
        self.assertIn("bitácora", activity_text)
        self.assertIn("presupuesto", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 4)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "calibración",
            "verificación",
            "trazabilidad metrológica",
            "volumen de medición",
            "criterio de aceptación",
            "metadatos",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_disciplinary(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://www.isbweb.org/activities/standards", urls)
        self.assertIn("https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53089978/Coordinate%2BSystems", urls)
        self.assertIn("https://jcgm.bipm.org/vim/en/2.39.html", urls)
        self.assertIn("https://jcgm.bipm.org/vim/en/2.44.html", urls)
        self.assertIn("https://jcgm.bipm.org/vim/en/2.41.html", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/16376351/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/39163799/", urls)

    def test_editorial_boundary_and_course_progression_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no constituye revisión disciplinar externa",
            "no se graban personas",
            "u2 desarrolla análisis cinemático",
            "u3 plataformas de fuerza",
            "u4 emg de superficie",
            "u5 dinámica inversa",
            "u6 estadística",
        ):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
