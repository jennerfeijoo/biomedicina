from __future__ import annotations

import json
import unittest
from pathlib import Path

# Final user-authored validation trigger after publication metadata synchronization.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "electrofisica-electromecanica" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "electrofisica-electromecanica" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ElectrofisicaElectromecanicaUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "electrofisica-electromecanica")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_and_signal_template_content_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("snr", self.text)
        self.assertNotIn("cadena física de transducción, acondicionamiento, adquisición", self.text)

    def test_theory_is_magnetic_and_inductive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "campo magnético",
            "biot-savart",
            "ampère",
            "flujo magnético",
            "faraday",
            "lenz",
            "autoinductancia",
            "inductancia mutua",
            "tms",
        ):
            self.assertIn(concept, theory)
        for boundary in ("u3", "u4", "u5", "u6"):
            self.assertIn(boundary, theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        for equation in (
            "\\mathbf F_B=q\\mathbf v\\times\\mathbf B",
            "\\Phi_B=\\int_S \\mathbf B\\cdot d\\mathbf A",
            "\\mathcal E=-N\\frac{d\\Phi_B}{dt}",
            "N\\Phi_B=LI",
            "\\mathcal E_L=-L\\frac{dI}{dt}",
            "\\mathcal E_2=-M\\frac{dI_1}{dt}",
        ):
            self.assertIn(equation, equations)

    def test_guided_activity_is_scaffolded_and_safe(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 6)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 7)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        activity_text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintét", activity_text)
        self.assertIn("no energices bobinas", activity_text)
        self.assertIn("no conectes red eléctrica", activity_text)
        self.assertIn("tms", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "campo magnético",
            "ley de biot-savart",
            "flujo magnético",
            "ley de faraday",
            "autoinductancia",
            "inductancia mutua",
            "tms",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_cover_core_and_biomedical_context(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 12)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://openstax.org/books/university-physics-volume-2/pages/12-1-the-biot-savart-law",
            "https://openstax.org/books/university-physics-volume-2/pages/13-1-faradays-law",
            "https://openstax.org/books/university-physics-volume-2/pages/14-1-mutual-inductance",
            "https://pubmed.ncbi.nlm.nih.gov/2860322/",
            "https://pubmed.ncbi.nlm.nih.gov/17640522/",
            "https://pubmed.ncbi.nlm.nih.gov/33243615/",
            "https://pubmed.ncbi.nlm.nih.gov/38061463/",
        ):
            self.assertIn(url, urls)

    def test_tms_and_course_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        examples = json.dumps(self.unit["worked_examples"], ensure_ascii=False).casefold()
        self.assertIn("no constituyen revisión disciplinar externa", notice)
        self.assertIn("no autorizan energizar bobinas", notice)
        self.assertIn("realizar estimulación magnética en personas", notice)
        self.assertIn("seguridad o eficacia clínica", purpose)
        self.assertIn("no interpretar 2.0 v como voltaje cortical", examples)


if __name__ == "__main__":
    unittest.main()
