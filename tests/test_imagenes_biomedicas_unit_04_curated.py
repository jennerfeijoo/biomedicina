from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "imagenes-biomedicas" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "imagenes-biomedicas" / "unit-04.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ImagenesBiomedicasUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "imagenes-biomedicas")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertIn("pulse-echo", text)
        self.assertIn("beamforming", text)
        self.assertIn("doppler", text)

    def test_theory_is_ultrasound_specific_and_substantive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "impedancia acústica",
            "resolución axial",
            "resolución lateral",
            "compresión logarítmica",
            "tgc",
            "speckle",
            "aliasing",
        ):
            self.assertIn(concept, theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("d=\\frac{ct}{2}", equations)
        self.assertIn("\\Delta f=\\frac{2f_0v\\cos\\theta}{c}", equations)
        self.assertIn("|\\Delta f|<\\frac{PRF}{2}", equations)

    def test_guided_activities_are_progressive_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertTrue(all(len(activity["instructions"]) >= 5 for activity in activities))
        self.assertTrue(all(len(activity["problems"]) >= 12 for activity in activities))
        self.assertTrue(all(len(activity["deliverables"]) >= 6 for activity in activities))
        self.assertTrue(all(len(activity["checking_criteria"]) >= 8 for activity in activities))
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintét", activity_text)
        self.assertIn("no adquieras datos de personas", activity_text)
        self.assertIn("no se dan recomendaciones de exposición", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 30)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "impedancia acústica",
            "beamforming",
            "b-mode",
            "color doppler",
            "índice térmico",
            "índice mecánico",
        ):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_directly_verified(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://www.nibib.nih.gov/science-education/science-topics/ultrasound", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/30603155/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/33360053/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/2662551/", urls)
        self.assertIn("https://www.fda.gov/radiation-emitting-products/medical-imaging/ultrasound-imaging", urls)

    def test_curricular_and_clinical_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        theory = " ".join(p for section in self.unit["theory_sections"] for p in section["paragraphs"]).casefold()
        self.assertIn("unidad 6", notice)
        self.assertIn("no autorizan escanear personas", notice)
        self.assertIn("no autoriza ajustar salida acústica", theory)
        self.assertIn("interpretación diagnóstica", notice)


if __name__ == "__main__":
    unittest.main()
