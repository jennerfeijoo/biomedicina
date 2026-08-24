# Regression for curated Imágenes Biomédicas U5.
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "imagenes-biomedicas" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "imagenes-biomedicas" / "unit-05.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ImagenesBiomedicasUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "imagenes-biomedicas")
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in ("radiotrazador", "spect", "pet", "fluorescencia", "óptica difusa"):
            self.assertIn(concept, text)

    def test_theory_covers_nuclear_and_optical_imaging(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "estadística de poisson",
            "colimación mecánica",
            "coincidencia aleatoria",
            "tiempo de vuelo",
            "suv",
            "beer-lambert",
            "coeficiente de dispersión reducido",
        ):
            self.assertIn(concept, theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("A(t)=A_0e^{-\\lambda t}", equations)
        self.assertIn("T_{1/2}=\\frac{\\ln 2}{\\lambda}", equations)
        self.assertIn("\\Delta x\\approx\\frac{c_{luz}\\,\\Delta t}{2}", equations)
        self.assertIn("SUV=\\frac{C_{ROI}}{A_{ref}/m_{norm}}", equations)
        self.assertIn("I=I_0e^{-\\mu_a L}", equations)

    def test_guided_activities_are_progressive_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertTrue(all(len(item["instructions"]) >= 5 for item in activities))
        self.assertTrue(all(len(item["problems"]) >= 12 for item in activities))
        self.assertTrue(all(len(item["deliverables"]) >= 6 for item in activities))
        self.assertTrue(all(len(item["checking_criteria"]) >= 8 for item in activities))
        text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintét", text)
        self.assertIn("no se proporcionan instrucciones de adquisición sobre pacientes", text)
        self.assertIn("no se deriva una indicación clínica", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 30)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("radiotrazador", "spect", "colimador", "pet", "línea de respuesta", "suv", "dot", "fluorescencia"):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_directly_verified(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 12)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://www.nibib.nih.gov/science-education/science-topics/nuclear-medicine", urls)
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC5148182/", urls)
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC3039307/", urls)
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC9902332/", urls)
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC4482362/", urls)
        self.assertIn("https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_c.8.4.html", urls)

    def test_quantification_and_safety_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no constituye", notice)
        self.assertIn("manipular radionúclidos", notice)
        self.assertIn("administrar radiofármacos", notice)
        self.assertIn("unidad 6", notice)
        self.assertIn("suv con una propiedad biológica absoluta", purpose)
        self.assertIn("intensidad óptica con concentración", purpose)


if __name__ == "__main__":
    unittest.main()
