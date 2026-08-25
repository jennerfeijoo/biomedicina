from __future__ import annotations

import json
import unittest
from pathlib import Path

# Final user-authored validation trigger after publication metadata synchronization.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "electrofisica-electromecanica" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "electrofisica-electromecanica" / "unit-01.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ElectrofisicaElectromecanicaUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "electrofisica-electromecanica")
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_and_signal_template_content_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("snr", self.text)
        self.assertNotIn("cadena física de transducción, acondicionamiento, adquisición", self.text)

    def test_theory_is_electrostatic_and_substantive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "campo eléctrico",
            "potencial eléctrico",
            "ley de gauss",
            "permitividad",
            "polarización",
            "capacitancia",
            "dispersión",
            "sensibilidad",
        ):
            self.assertIn(concept, theory)
        self.assertIn("u3", theory)
        self.assertIn("u6", theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("\\mathbf E=-\\nabla V", equations)
        self.assertIn("C=\\frac{Q}{\\Delta V}", equations)
        self.assertIn("C=\\epsilon\\frac{A}{d}", equations)
        self.assertIn("\\mathbf D=\\epsilon\\mathbf E", equations)

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 6)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 7)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        activity_text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintét", activity_text)
        self.assertIn("no midas personas", activity_text)
        self.assertIn("ley de gauss", activity_text)
        self.assertIn("permitividad", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "campo eléctrico",
            "potencial eléctrico",
            "permitividad",
            "capacitancia",
            "dispersión dieléctrica",
            "capacitancia de membrana",
        ):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_directly_verified(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://openstax.org/books/university-physics-volume-2/pages/6-2-explaining-gausss-law",
            "https://openstax.org/books/university-physics-volume-2/pages/8-1-capacitors-and-capacitance",
            "https://pubmed.ncbi.nlm.nih.gov/2651001/",
            "https://pubmed.ncbi.nlm.nih.gov/8938025/",
            "https://pubmed.ncbi.nlm.nih.gov/8938026/",
            "https://pubmed.ncbi.nlm.nih.gov/29874833/",
            "https://pubmed.ncbi.nlm.nih.gov/35732164/",
        ):
            self.assertIn(url, urls)

    def test_biomedical_and_safety_boundaries_are_explicit(self) -> None:
        purpose = self.unit["purpose"].casefold()
        notice = self.unit["editorial_notice"].casefold()
        connections = json.dumps(self.unit["biomedical_connections"], ensure_ascii=False).casefold()
        self.assertIn("propiedad dieléctrica dependiente de frecuencia", purpose)
        self.assertIn("no constituyen revisión disciplinar externa", notice)
        self.assertIn("seguridad eléctrica", notice)
        self.assertIn("no autorizan mediciones en personas", notice)
        self.assertIn("membranas celulares", connections)
        self.assertIn("bioimpedancia", connections)


if __name__ == "__main__":
    unittest.main()
