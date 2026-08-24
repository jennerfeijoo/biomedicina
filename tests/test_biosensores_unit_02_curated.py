from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biosensores" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "biosensores" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiosensoresUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biosensores")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_signal_noise_fallback_are_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("mathrm{snr}", text)
        for concept in ("afinidad", "avididad", "reactividad cruzada", "michaelis-menten", "selex"):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_preserves_course_boundaries(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(section["heading"] + " " + " ".join(section["paragraphs"]) for section in sections).casefold()
        for concept in ("k_on", "k_off", "enzimas", "anticuerpos", "hibridación", "aptámeros", "estabilidad"):
            self.assertIn(concept, theory)
        self.assertIn("u3", theory)
        self.assertIn("u4", theory)
        self.assertIn("u5", theory)

    def test_core_equations_are_present_with_explicit_limits(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("K_D=\\frac{k_{off}}{k_{on}}", equations)
        self.assertIn("\\theta=\\frac{[L]}{K_D+[L]}", equations)
        self.assertIn("v=\\frac{V_{max}[S]}{K_m+[S]}", equations)
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertIn("no debe etiquetarse automáticamente como k_d", text)
        self.assertIn("modelo ideal 1:1", text)

    def test_guided_activity_is_scaffolded_synthetic_and_decision_bounded(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 7)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 9)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        for phrase in ("sintéticos", "no uses muestras humanas", "análogo", "no diana", "matriz de decisión"):
            self.assertIn(phrase, text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 18)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 4)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 8)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("afinidad", "avididad", "reactividad cruzada", "aptámero", "selex", "hibridación"):
            self.assertIn(term, terms)

    def test_sources_are_traceable_directly_verified_and_disciplinary(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(source.get("verification_status") == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        for url in (
            "https://pubmed.ncbi.nlm.nih.gov/30216055/",
            "https://pubmed.ncbi.nlm.nih.gov/2200121/",
            "https://pubmed.ncbi.nlm.nih.gov/1697402/",
            "https://pubmed.ncbi.nlm.nih.gov/21337107/",
            "https://pubmed.ncbi.nlm.nih.gov/39959045/",
            "https://pubmed.ncbi.nlm.nih.gov/33926034/",
        ):
            self.assertIn(url, urls)

    def test_scope_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("validación analítica o clínica", notice)
        self.assertIn("transductor", purpose)
        self.assertIn("validez clínica", purpose)


# Final user-authored trigger after publication metadata synchronization.
if __name__ == "__main__":
    unittest.main()
