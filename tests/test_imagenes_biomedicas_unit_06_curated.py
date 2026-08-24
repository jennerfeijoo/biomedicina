from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "imagenes-biomedicas" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "imagenes-biomedicas" / "unit-06.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"
# Final user-authored trigger after publication and catalog synchronization.


class ImagenesBiomedicasUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "imagenes-biomedicas")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in ("mtf", "nps", "artefacto", "quality assurance", "quality control", "mri", "ultrasonido"):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_task_based(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "respecto de una tarea",
            "tamaño de píxel",
            "fantoma",
            "línea base",
            "diagnostic reference levels",
            "campo magnético estático",
            "índice térmico",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no demuestra", theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("SNR=\\frac{\\mu_s}{\\sigma_n}", equations)
        self.assertIn("CNR=\\frac{|\\mu_1-\\mu_2|}{\\sigma_n}", equations)
        self.assertTrue(any(eq.startswith("MTF(f)=") for eq in equations))
        self.assertIn("\\Delta x_t=x_t-x_{baseline}", equations)

    def test_guided_activities_are_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertGreaterEqual(len(activities), 3)
        for activity in activities:
            self.assertGreaterEqual(len(activity["instructions"]), 5)
            self.assertGreaterEqual(len(activity["problems"]), 12)
            self.assertGreaterEqual(len(activity["deliverables"]), 6)
            self.assertGreaterEqual(len(activity["checking_criteria"]), 8)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintét", activity_text)
        self.assertIn("no cargues estudios de pacientes", activity_text)
        self.assertIn("no prescribas", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 25)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("mtf", "nps", "qa", "qc", "drl", "mr conditional", "índice térmico"):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_authoritative(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        verified = [item for item in sources if item.get("verification_status") == "verified_directly"]
        self.assertEqual(len(verified), len(sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://www.fda.gov/radiation-emitting-products/medical-imaging/medical-x-ray-imaging", urls)
        self.assertIn("https://www.fda.gov/radiation-emitting-products/mri-magnetic-resonance-imaging/benefits-and-risks", urls)
        self.assertIn("https://www.fda.gov/radiation-emitting-products/medical-imaging/ultrasound-imaging", urls)
        self.assertTrue(any("iaea.org" in url for url in urls))

    def test_professional_and_clinical_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("ni autorización para operar equipos", notice)
        self.assertIn("recomendación clínica", purpose)


if __name__ == "__main__":
    unittest.main()
