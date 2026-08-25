from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "electrofisica-electromecanica" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "electrofisica-electromecanica" / "unit-01.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ElectrofisicaElectromecanicaUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "electrofisica-electromecanica")
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_signal_template_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("snr_{db}", text)
        self.assertNotIn("cadena física de transducción, acondicionamiento, adquisición", text)
        for concept in ("campo eléctrico", "potencial eléctrico", "permitividad", "capacitancia", "dispersión dieléctrica"):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_respects_course_boundaries(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        words = sum(len(p.split()) for section in sections for p in section["paragraphs"])
        self.assertGreaterEqual(words, 1400)
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        self.assertIn("magnetismo y la inducción se reservan para u2", theory)
        self.assertIn("transitorios, impedancia y potencia para u3", theory)
        self.assertIn("u6 seguridad", theory)
        self.assertIn("no demuestra", theory)

    def test_core_electrostatic_equations_are_present(self) -> None:
        equations = {
            eq["latex"]
            for section in self.unit["theory_sections"]
            for eq in section.get("equations", [])
        }
        self.assertIn(r"\mathbf E=-\nabla V", equations)
        self.assertIn(r"\Delta V=V_b-V_a=-\int_a^b \mathbf E\cdot d\mathbf l", equations)
        self.assertIn(r"\mathbf D=\varepsilon\mathbf E=\varepsilon_0\varepsilon_r\mathbf E", equations)
        self.assertIn(r"C=\frac{Q}{\Delta V}", equations)
        self.assertIn(r"C=\frac{\varepsilon A}{d}", equations)
        self.assertIn(r"\frac{1}{C_{eq}}=\sum_i\frac{1}{C_i}", equations)

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(activity["duration_minutes"], 240)
        self.assertGreaterEqual(len(activity["instructions"]), 8)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 15)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintéticos", text)
        self.assertIn("no conectes electrodos a personas", text)
        self.assertIn("no se infiere seguridad eléctrica", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "campo eléctrico",
            "potencial eléctrico",
            "polarización dieléctrica",
            "permitividad",
            "dispersión dieléctrica",
            "capacitancia",
            "interfaz dieléctrica",
            "modelo cuasiestático",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_cover_tissue_dispersion(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(source["verification_status"] == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        for url in (
            "https://pubmed.ncbi.nlm.nih.gov/8938024/",
            "https://pubmed.ncbi.nlm.nih.gov/8938025/",
            "https://pubmed.ncbi.nlm.nih.gov/8938026/",
            "https://pubmed.ncbi.nlm.nih.gov/2651001/",
            "https://openstax.org/books/university-physics-volume-2/pages/8-1-capacitors-and-capacitance",
        ):
            self.assertIn(url, urls)

    def test_frequency_and_measurement_context_are_explicit(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        for phrase in (
            "10 hz a 20 ghz",
            "frecuencia, tejido, temperatura",
            "polarización de electrodo",
            "inductancia parásita",
            "variabilidad",
        ):
            self.assertIn(phrase, text)

    def test_clinical_safety_and_regulatory_boundaries_are_explicit(self) -> None:
        purpose = self.unit["purpose"].casefold()
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("sin confundir una magnitud calculada con una medición directa", purpose)
        for phrase in (
            "no constituyen revisión disciplinar externa",
            "validación clínica",
            "seguridad eléctrica o electromagnética",
            "eficacia de estimulación",
            "ensayo de conformidad",
            "diagnóstica o terapéutica",
        ):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
