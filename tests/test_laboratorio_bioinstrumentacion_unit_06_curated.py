# Final user-authored CI trigger after public synchronization.
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "laboratorio-bioinstrumentacion" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "laboratorio-bioinstrumentacion" / "unit-06.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class LaboratorioBioinstrumentacionUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "laboratorio-bioinstrumentacion")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed_and_verification_chain_exists(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        for concept in (
            "matriz de verificación",
            "criterio de aceptación",
            "evidencia objetiva",
            "repetibilidad",
            "evaluación tipo a",
            "evaluación tipo b",
            "regla de decisión",
            "discrepancia",
            "regresión",
        ):
            self.assertIn(concept, self.text)

    def test_theory_is_substantive_and_distinguishes_verification_validation(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        self.assertIn("verificación y validación no son sinónimos", theory)
        self.assertIn("definir el criterio después de observar los datos", theory)
        self.assertIn("una evaluación de tipo a", theory)
        self.assertIn("una evaluación de tipo b", theory)
        self.assertIn("una verificación rigurosa conserva resultados desfavorables", theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        for equation in (
            "x_bar = (1/n) sum_i x_i",
            "s = sqrt(sum_i (x_i - x_bar)^2 / (n-1))",
            "u_c(y) = sqrt(sum_i (c_i u(x_i))^2)",
            "U = k u_c",
            "u_A(x_bar) = s / sqrt(n)",
        ):
            self.assertIn(equation, equations)

    def test_guided_activities_are_progressive_synthetic_and_auditable(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertGreaterEqual(len(activities), 3)
        self.assertGreaterEqual(len(activities[0]["problems"]), 15)
        self.assertGreaterEqual(len(activities[0]["deliverables"]), 8)
        self.assertGreaterEqual(len(activities[1]["problems"]), 20)
        self.assertGreaterEqual(len(activities[1]["deliverables"]), 10)
        self.assertGreaterEqual(len(activities[1]["checking_criteria"]), 10)
        self.assertGreaterEqual(len(activities[2]["tasks"]), 12)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sin personas ni red eléctrica", activity_text)
        self.assertIn("no se modifican criterios post hoc", activity_text)
        self.assertIn("prueba inválida", activity_text)
        self.assertIn("nueva baseline", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 30)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 12)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 11)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "verificación",
            "validación",
            "criterio de aceptación",
            "matriz de verificación",
            "incertidumbre estándar combinada",
            "regla de decisión",
            "discrepancia",
            "regresión",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_cover_metrology_and_systems_engineering(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://jcgm.bipm.org/vim/en/2.44.html",
            "https://www.bipm.org/en/doi/10.59161/jcgm100-2008e",
            "https://www.bipm.org/en/doi/10.59161/jcgm106-2012",
            "https://www.nist.gov/pml/nist-technical-note-1297",
            "https://www.nasa.gov/reference/5-3-product-verification/",
            "https://www.fda.gov/medical-devices/investigational-device-exemption-ide/ide-related-topics",
        ):
            self.assertIn(url, urls)

    def test_safety_clinical_and_regulatory_boundary_is_explicit(self) -> None:
        purpose = self.unit["purpose"].casefold()
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("distingue verificación de validación", purpose)
        self.assertIn("no demuestra necesidades de usuario", purpose)
        self.assertIn("sin conexión a personas", notice)
        self.assertIn("red eléctrica", notice)
        self.assertIn("no constituye validación", notice)
        self.assertIn("seguridad eléctrica", notice)
        self.assertIn("validación fisiológica o clínica", notice)
        self.assertIn("revisión disciplinar humana permanece pendiente", notice)


if __name__ == "__main__":
    unittest.main()
