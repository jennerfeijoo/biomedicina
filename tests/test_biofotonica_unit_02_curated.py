from __future__ import annotations

import json
import unittest
from pathlib import Path

# Final user-authored trigger after public-site synchronization.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biofotonica" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "biofotonica" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiofotonicaUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biofotonica")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "responsividad espectral",
            "eficiencia cuántica",
            "transimpedancia",
            "ruido de disparo",
            "potencia equivalente de ruido",
        ):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_instrumentation_specific(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "led",
            "láser",
            "fotodiodo",
            "corriente oscura",
            "ancho de banda",
            "linealidad",
            "calibración",
            "seguridad óptica",
        ):
            self.assertIn(concept, theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        expected = {
            "E_\\gamma=\\frac{hc}{\\lambda}",
            "I_{ph}=R(\\lambda)P_{det}",
            "R(\\lambda)=\\eta(\\lambda)\\frac{q\\lambda}{hc}",
            "V_{out}=-I_{ph}R_f",
            "i_{shot}=\\sqrt{2qIB}",
            "NEP=\\frac{i_n}{R(\\lambda)}",
            "SNR=\\frac{I_{ph}}{i_n}",
            "P_{det}=P_{src}\\prod_k \\eta_k",
        }
        self.assertTrue(expected.issubset(equations))

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertGreaterEqual(len(activities), 2)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 10)
        self.assertGreaterEqual(len(activity["deliverables"]), 6)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 8)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("850 nm", text)
        self.assertIn("sintética", text)
        self.assertIn("no conectes láseres", text)
        self.assertIn("no se realiza ni se autoriza exposición óptica real", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 16)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 4)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 8)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "responsividad espectral",
            "eficiencia cuántica",
            "amplificador transimpedancia",
            "ruido de disparo",
            "nep",
            "rango dinámico",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_traceable(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 7)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn(
            "https://www.nist.gov/pml/sensor-science/optical-radiation/faqs-spectral-responsivity-calibrations",
            urls,
        )
        self.assertIn(
            "https://hub.hamamatsu.com/us/en/technical-notes/detector-selection/the-wits-guide-to-selecting-a-photodetector.html",
            urls,
        )
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/24860804/", urls)
        self.assertIn(
            "https://www.fda.gov/radiation-emitting-products/home-business-and-entertainment-products/laser-products-and-instruments",
            urls,
        )

    def test_safety_and_clinical_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no se autoriza encender o alinear láseres", notice)
        self.assertIn("utilidad clínica", notice)
        self.assertIn("desempeño clínico", purpose)
        self.assertIn("exposición óptica", purpose)


if __name__ == "__main__":
    unittest.main()
