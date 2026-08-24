from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "imagenes-biomedicas" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "imagenes-biomedicas" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ImagenesBiomedicasUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "imagenes-biomedicas")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed_and_scope_is_mri_specific(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in ("larmor", "t1", "t2*", "spin echo", "gradient echo", "espacio-k", "fourier", "dicom"):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_preserves_curricular_boundary(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in ("magnetización neta", "radiofrecuencia", "recuperación longitudinal", "codificación de fase", "frecuencia espacial", "resolución efectiva"):
            self.assertIn(concept, theory)
        self.assertIn("u6", theory)
        self.assertIn("artefactos", theory)
        self.assertIn("seguridad", theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        expected = {
            "\\omega_0=\\gamma B_0",
            "f_0=\\frac{\\gamma}{2\\pi}B_0",
            "M_z(t)=M_0\\left(1-e^{-t/T_1}\\right)",
            "M_{xy}(t)=M_{xy}(0)e^{-t/T_2}",
            "\\frac{1}{T_2^*}=\\frac{1}{T_2}+\\frac{1}{T_2'}",
            "S_{SE}\\propto \\rho\\left(1-e^{-TR/T_1}\\right)e^{-TE/T_2}",
            "\\mathbf k(t)=\\frac{\\gamma}{2\\pi}\\int_0^t \\mathbf G(\\tau)\\,d\\tau",
            "\\Delta x=\\frac{FOV_x}{N_x}",
        }
        self.assertTrue(expected.issubset(equations))

    def test_guided_activities_are_progressive_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertGreaterEqual(len(activities[0]["problems"]), 12)
        self.assertTrue(all(len(activity["instructions"]) >= 5 for activity in activities))
        self.assertTrue(all(len(activity["deliverables"]) >= 6 for activity in activities))
        self.assertTrue(all(len(activity["checking_criteria"]) >= 8 for activity in activities))
        text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintét", text)
        self.assertIn("no uses estudios de pacientes", text)
        self.assertIn("no necesitas software de rm ni acceso a un escáner", text)
        self.assertIn("no recomiendes parámetros para pacientes", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("frecuencia de larmor", "t1", "t2", "t2*", "spin echo", "gradient echo", "espacio-k", "transformada de fourier"):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_authoritative(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://www.nibib.nih.gov/science-education/science-topics/magnetic-resonance-imaging-mri",
            "https://journals.aps.org/pr/abstract/10.1103/PhysRev.70.460",
            "https://journals.aps.org/pr/abstract/10.1103/PhysRev.80.580",
            "https://www.nature.com/articles/242190a0",
            "https://dicom.nema.org/medical/dicom/2025e/output/chtml/part03/sect_C.8.3.html",
        ):
            self.assertIn(url, urls)

    def test_physical_and_clinical_limits_are_explicit(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("escala universal análoga", text)
        self.assertIn("hounsfield", text)
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no autorizan modificar protocolos clínicos", notice)
        self.assertIn("escanear personas", notice)
        self.assertIn("interpretar estudios de pacientes", notice)


if __name__ == "__main__":
    unittest.main()
