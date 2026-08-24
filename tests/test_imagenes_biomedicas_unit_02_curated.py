from __future__ import annotations

import json
import unittest
from pathlib import Path

# Final user-authored trigger after public and curriculum synchronization.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "imagenes-biomedicas" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "imagenes-biomedicas" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ImagenesBiomedicasUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "imagenes-biomedicas")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in ("beer-lambert", "sinograma", "retroproyección filtrada", "hounsfield", "ctdivol", "ssde"):
            self.assertIn(concept, text)

    def test_theory_has_physics_reconstruction_quality_and_dose(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "endurecimiento del haz",
            "transformada de radon",
            "reconstrucción iterativa",
            "rescale slope",
            "kernel",
            "fantoma de referencia",
        ):
            self.assertIn(concept, theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("I=I_0 e^{-\\mu x}", equations)
        self.assertIn("p=-\\ln\\left(\\frac{I}{I_0}\\right)=\\int_L \\mu(\\mathbf r)\\,ds", equations)
        self.assertIn("HU=1000\\frac{\\mu-\\mu_{agua}}{\\mu_{agua}}", equations)
        self.assertIn("DLP=CTDI_{vol}\\,L", equations)
        self.assertIn("SSDE=f_{size}\\,CTDI_{vol}", equations)

    def test_dose_indices_are_not_presented_as_patient_dose(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertIn("ctdivol es un índice de salida", text)
        self.assertIn("no es una dosis de órgano", text)
        self.assertIn("no es dosis absorbida individual", text)
        self.assertIn("fantoma de referencia", text)

    def test_guided_activity_is_scaffolded_and_phantom_only(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 14)
        self.assertGreaterEqual(len(activity["deliverables"]), 6)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("fantoma", text)
        self.assertIn("no interpretes estudios de pacientes", text)
        self.assertIn("ctdivol", text)
        self.assertIn("ssde", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("sinograma", "retroproyección filtrada (fbp)", "unidad hounsfield (hu)", "ctdivol", "dlp", "ssde"):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_authoritative(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_c.8.15.3.10.html", urls)
        self.assertIn("https://www.aapm.org/pubs/reports/detail.asp?docid=97", urls)
        self.assertIn("https://www.aapm.org/pubs/reports/detail.asp?docid=143", urls)
        self.assertIn("https://www.aapm.org/pubs/reports/detail.asp?docid=146", urls)
        self.assertIn("https://www.slaney.org/pct/pct-toc.html", urls)

    def test_clinical_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no autorizan interpretar estudios de pacientes", notice)
        self.assertIn("sin tratarlos como dosis absorbida individual", purpose)


if __name__ == "__main__":
    unittest.main()
