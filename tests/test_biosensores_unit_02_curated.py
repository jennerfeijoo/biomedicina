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

    def test_source_and_generated_mirror_are_identical(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biosensores")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_wrong_signal_content_are_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("snr_{db}", text)
        for concept in ("afinidad", "selectividad", "anticuerpos", "aptámeros", "hibridación", "michaelis"):
            self.assertIn(concept, text)

    def test_theory_has_four_substantive_recognition_sections(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in ("k_d", "k_on", "k_off", "k_m", "mismatch", "selex", "estabilidad funcional"):
            self.assertIn(concept, theory)
        self.assertIn("u3", theory)
        self.assertIn("u4", theory)

    def test_equations_keep_binding_and_catalysis_distinct(self) -> None:
        equations = {
            eq["latex"]
            for section in self.unit["theory_sections"]
            for eq in section.get("equations", [])
        }
        self.assertIn("K_D=\\frac{[R][L]}{[RL]}=\\frac{k_{off}}{k_{on}}", equations)
        self.assertIn("\\theta=\\frac{[L]}{K_D+[L]}", equations)
        self.assertIn("v_0=\\frac{V\\,[S]}{K_m+[S]}", equations)
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertIn("k_m no debe interpretarse automáticamente como constante de afinidad", text)
        self.assertIn("k_m no es en general una constante de afinidad", text)

    def test_guided_activity_is_scaffolded_synthetic_and_cross_mechanism(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 10)
        self.assertGreaterEqual(len(activity["deliverables"]), 6)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 8)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        for concept in ("sintéticos", "no recolectes muestras", "proteína", "metabolito", "secuencia", "mismatch", "u3", "u4", "u5"):
            self.assertIn(concept, text)

    def test_glossary_examples_errors_and_self_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 18)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 4)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("afinidad", "selectividad", "k_d", "k_m", "avididad", "hibridación", "aptámero", "selex", "estabilidad funcional"):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_cover_core_mechanisms(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://pubmed.ncbi.nlm.nih.gov/30216055/",
            "https://goldbook.iupac.org/terms/view/14132",
            "https://goldbook.iupac.org/terms/view/11546",
            "https://pubmed.ncbi.nlm.nih.gov/32758356/",
            "https://pubmed.ncbi.nlm.nih.gov/2200121/",
            "https://pubmed.ncbi.nlm.nih.gov/1697402/",
            "https://pubmed.ncbi.nlm.nih.gov/35323453/",
            "https://pubmed.ncbi.nlm.nih.gov/32891698/",
        ):
            self.assertIn(url, urls)

    def test_scope_and_human_review_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("validación analítica o clínica", notice)
        self.assertIn("datos y escenarios sintéticos", notice)
        self.assertIn("no autorizan trabajo con muestras humanas", notice)
        self.assertIn("desempeño analítico o clínico", purpose)


if __name__ == "__main__":
    unittest.main()
