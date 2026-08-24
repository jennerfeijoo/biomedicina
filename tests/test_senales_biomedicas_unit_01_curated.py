from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "senales-biomedicas" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "senales-biomedicas" / "unit-01.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class SenalesBiomedicasUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "senales-biomedicas")
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in ("ecg", "eeg", "semg", "ppg", "antialias", "cuantización"):
            self.assertIn(concept, text)

    def test_modalities_are_physically_distinguished(self) -> None:
        theory = " ".join(
            paragraph
            for section in self.unit["theory_sections"]
            for paragraph in section["paragraphs"]
        ).casefold()
        self.assertIn("ppg no utiliza electrodos", theory)
        self.assertIn("biopotenciales", theory)
        self.assertIn("fotodetector", theory)
        self.assertIn("la amplitud semg no es una medición directa de fuerza", theory)

    def test_sampling_and_digitization_are_substantive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        equations = {
            equation["latex"]
            for section in sections
            for equation in section.get("equations", [])
        }
        self.assertIn("f_N=\\frac{f_s}{2}", equations)
        self.assertIn("f_s>2f_{max}", equations)
        self.assertIn("\\Delta V_{ADC}=\\frac{V_{FS}}{2^N}", equations)

    def test_guided_activities_are_progressive_and_safe(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertTrue(all(len(item["instructions"]) >= 5 for item in activities))
        self.assertTrue(all(len(item["problems"]) >= 10 for item in activities))
        self.assertTrue(all(len(item["checking_criteria"]) >= 6 for item in activities))
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintétic", activity_text)
        self.assertIn("physionet", activity_text)
        self.assertIn("no se propone conectar el circuito a una persona", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 18)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("ecg", "eeg", "semg", "ppg", "aliasing", "filtro antialias", "sincronización"):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_methodologically_relevant(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        verified = [item for item in sources if item.get("verification_status") == "verified_directly"]
        self.assertEqual(len(verified), len(sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/17322457/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/36775678/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/11018445/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/17322588/", urls)
        self.assertIn("https://physionet.org/about/database/", urls)

    def test_editorial_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no requieren conectar electrodos", notice)
        self.assertIn("no autoriza diagnóstico", notice)
        self.assertIn("conclusión clínica", purpose)


if __name__ == "__main__":
    unittest.main()
