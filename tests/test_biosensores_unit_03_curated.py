from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biosensores" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "biosensores" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiosensoresUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biosensores")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_generic_snr_fallback_are_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("mathrm{snr}", text)
        for concept in ("potenciometría", "amperometría", "impedancia", "fluorescencia", "sauerbrey", "calorimetría"):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_preserves_course_boundaries(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(section["heading"] + " " + " ".join(section["paragraphs"]) for section in sections).casefold()
        for concept in ("electroquímica", "beer–lambert", "spr", "qcm", "térmica", "deriva"):
            self.assertIn(concept, theory)
        self.assertIn("u2", theory)
        self.assertIn("u4", theory)
        self.assertIn("u5", theory)

    def test_core_equations_are_present_with_explicit_limits(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("E=E^0+\\frac{RT}{zF}\\ln a_i", equations)
        self.assertIn("I=nFAJ", equations)
        self.assertIn("Z(\\omega)=\\frac{\\tilde E(\\omega)}{\\tilde I(\\omega)}", equations)
        self.assertIn("A=\\varepsilon b c=\\log_{10}\\left(\\frac{P_0}{P}\\right)", equations)
        self.assertIn("\\Delta f=-\\frac{2f_0^2}{A\\sqrt{\\rho_q\\mu_q}}\\,\\Delta m", equations)
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertIn("capa rígida", text)
        self.assertIn("muestra turbia", text)
        self.assertIn("actividad", text)

    def test_guided_activity_is_scaffolded_synthetic_and_multimodal(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 7)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 9)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        for phrase in ("datos sintéticos", "no uses muestras humanas", "matriz de decisión", "sauerbrey", "u4", "u5"):
            self.assertIn(phrase, text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 18)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 9)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("potenciometría", "amperometría", "impedancia", "spr", "qcm", "transducción térmica"):
            self.assertIn(term, terms)

    def test_sources_are_traceable_directly_verified_and_multimodal(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 12)
        self.assertTrue(all(source.get("verification_status") == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        for url in (
            "https://goldbook.iupac.org/terms/view/09127",
            "https://goldbook.iupac.org/terms/view/09128",
            "https://goldbook.iupac.org/terms/view/09168",
            "https://pubmed.ncbi.nlm.nih.gov/27879772/",
            "https://pubmed.ncbi.nlm.nih.gov/31970360/",
            "https://pubmed.ncbi.nlm.nih.gov/36908332/",
            "https://pubmed.ncbi.nlm.nih.gov/11672656/",
        ):
            self.assertIn(url, urls)

    def test_scope_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("validación analítica o clínica", notice)
        self.assertIn("u4", text)
        self.assertIn("u5", text)
        self.assertIn("inmovilización", text)
        self.assertIn("validez clínica", purpose)


if __name__ == "__main__":
    unittest.main()
