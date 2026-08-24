from __future__ import annotations

import json
import unittest
from pathlib import Path

# Final user-authored gate trigger after generated-site synchronization on the current branch head.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "laboratorio-biomecanica" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "laboratorio-biomecanica" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class LaboratorioBiomecanicaUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()
        cls.theory = " ".join(
            paragraph
            for section in cls.unit["theory_sections"]
            for paragraph in section["paragraphs"]
        ).casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "laboratorio-biomecanica")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_dynamics_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("\\sum \\mathbf{f}=m\\mathbf{a}", self.text)
        self.assertNotIn("\\sum \\mathbf f=m\\mathbf a", self.text)
        self.assertNotIn("equilibrio estático, solución analítica, refinamiento de discretización", self.text)

    def test_theory_is_substantive_and_kinematic(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        for concept in (
            "análisis 2d",
            "reconstrucción 3d",
            "artefacto de tejido blando",
            "frecuencia de muestreo",
            "aliasing",
            "interpolación",
            "filtrado",
            "diferencias centrales",
            "rmse",
            "correlación",
        ):
            self.assertIn(concept, self.theory)

    def test_core_kinematic_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("x=f\\frac{X}{Z},\\qquad y=f\\frac{Y}{Z}", equations)
        self.assertIn("\\mathbf v_i\\approx\\frac{\\mathbf r_{i+1}-\\mathbf r_{i-1}}{2\\Delta t}", equations)
        self.assertIn("\\mathbf a_i\\approx\\frac{\\mathbf r_{i+1}-2\\mathbf r_i+\\mathbf r_{i-1}}{\\Delta t^2}", equations)
        self.assertTrue(any("\\mathrm{RMSE}" in equation for equation in equations))

    def test_guided_activity_is_self_contained_and_synthetic(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 6)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 12)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        for phrase in ("no grabes personas", "serie a=[10,18,25,17,9]", "2d", "3d", "rmse"):
            self.assertIn(phrase, text)

    def test_learning_support_is_specific_and_sufficient(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("aliasing", "proyección 2d", "reconstrucción 3d", "artefacto de tejido blando", "interpolación", "filtrado", "rmse"):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_disciplinary(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://www.isbweb.org/activities/standards",
            "https://pubmed.ncbi.nlm.nih.gov/11415549/",
            "https://pubmed.ncbi.nlm.nih.gov/11415604/",
            "https://pubmed.ncbi.nlm.nih.gov/28923393/",
            "https://pubmed.ncbi.nlm.nih.gov/4837552/",
            "https://pubmed.ncbi.nlm.nih.gov/34283131/",
            "https://pubmed.ncbi.nlm.nih.gov/1517265/",
            "https://pubmed.ncbi.nlm.nih.gov/28549599/",
            "https://pubmed.ncbi.nlm.nih.gov/32705424/",
            "https://pubmed.ncbi.nlm.nih.gov/37307761/",
            "https://pubmed.ncbi.nlm.nih.gov/37541054/",
        ):
            self.assertIn(url, urls)

    def test_editorial_boundary_and_course_progression_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        for phrase in (
            "no constituye revisión disciplinar externa",
            "autorización para registrar personas",
            "u1 establece protocolo",
            "u3 incorpora plataformas de fuerza",
            "u4 emg de superficie",
            "u5 dinámica inversa",
            "u6 estadística",
        ):
            self.assertIn(phrase, notice)
        self.assertIn("convierte una trayectoria", purpose)
        self.assertIn("conclusión clínica", purpose)


if __name__ == "__main__":
    unittest.main()
