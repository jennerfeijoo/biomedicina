from __future__ import annotations

import json
import unittest
from pathlib import Path

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

    def test_generic_template_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in ("emisión estimulada", "responsividad", "transimpedancia", "nep", "rango dinámico"):
            self.assertIn(concept, text)

    def test_source_detector_theory_is_substantive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "emisión espontánea",
            "eficiencia cuántica",
            "fotocorriente",
            "ruido de disparo",
            "ancho de banda",
            "saturación",
            "detección síncrona",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no equivale a un dispositivo clínicamente válido", theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("E_\\gamma=\\frac{hc}{\\lambda}", equations)
        self.assertIn("R(\\lambda)=\\eta\\frac{q\\lambda}{hc}", equations)
        self.assertIn("I_{ph}=R(\\lambda)P_{det}", equations)
        self.assertIn("i_{shot}=\\sqrt{2qIB}", equations)
        self.assertIn("\\mathrm{NEP}=\\frac{i_n}{R(\\lambda)}", equations)
        self.assertIn("P_{det}=P_{src}\\,T_{opt}\\,T_{sample}\\,T_{coupling}", equations)

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 8)
        self.assertGreaterEqual(len(activity["problems"]), 14)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintétic", text)
        self.assertIn("no ilumines personas ni animales", text)
        self.assertIn("headroom", text)
        self.assertIn("nep", text)
        self.assertIn("no se calcula ni se afirma una exposición segura", text)

    def test_learning_support_is_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 6)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 12)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("responsividad", "transimpedancia", "ruido de disparo", "nep", "speckle"):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_disciplinary(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/30011842/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/32329266/", urls)
        self.assertIn("https://webstore.iec.ch/en/publication/3587", urls)
        self.assertIn(
            "https://hub.hamamatsu.com/us/en/technical-notes/detector-selection/the-wits-guide-to-selecting-a-photodetector.html",
            urls,
        )

    def test_clinical_and_safety_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("evaluación de seguridad óptica", notice)
        self.assertIn("ni autorizan iluminar personas o animales", notice)
        self.assertIn("evidencia clínica", purpose)
        self.assertIn("conformidad regulatoria", purpose)


# Final user-authored trigger after publication synchronization.
if __name__ == "__main__":
    unittest.main()
