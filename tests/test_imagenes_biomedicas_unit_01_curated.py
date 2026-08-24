from __future__ import annotations

import json
import unittest
from pathlib import Path

# Final user-authored trigger after public and curriculum synchronization.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "imagenes-biomedicas" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "imagenes-biomedicas" / "unit-01.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ImagenesBiomedicasUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "imagenes-biomedicas")
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in ("pixel spacing", "nyquist", "aliasing", "mtf", "window center"):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_modality_neutral(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 3 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in ("image position", "image orientation", "volumen parcial", "rescale slope", "calidad de imagen es dependiente de la tarea"):
            self.assertIn(concept, theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("f_s=\\frac{1}{\\Delta x},\\qquad f_N=\\frac{1}{2\\Delta x}", equations)
        self.assertIn("MTF(f)=\\frac{|\\mathcal F\\{PSF(x)\\}|}{|\\mathcal F\\{PSF(x)\\}|_{f=0}}", equations)
        self.assertIn("CNR=\\frac{|\\mu_1-\\mu_2|}{\\sigma_n}", equations)
        self.assertIn("Y=m\\,SV+b", equations)

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 6)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 8)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintética", text)
        self.assertIn("no uses estudios de pacientes", text)
        self.assertIn("nyquist", text)
        self.assertIn("mtf", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 8)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("píxel", "vóxel", "pixel spacing", "frecuencia de nyquist", "mtf", "cnr"):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_authoritative(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 7)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html", urls)
        self.assertIn("https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_c.11.2.html", urls)
        self.assertIn("https://pub.iaea.org/mtcd/publications/pdf/pub1564webnew-74666420.pdf", urls)
        self.assertIn("https://www.aapm.org/pubs/reports/rpt_93.pdf", urls)

    def test_clinical_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no autorizan interpretar estudios de pacientes", notice)
        self.assertIn("información diagnóstica validada", purpose)


if __name__ == "__main__":
    unittest.main()
