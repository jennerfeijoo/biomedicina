from __future__ import annotations

import json
import unittest
from pathlib import Path

# Final user-authored trigger after public-site synchronization.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "comunicacion-cientifica" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "comunicacion-cientifica" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ComunicacionCientificaUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "comunicacion-cientifica")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in ("toulmin", "valor p", "spin", "contraevidencia", "afirmación causal"):
            self.assertIn(concept, text)

    def test_argument_structure_and_inference_are_substantive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "afirmación",
            "evidencia",
            "razonamiento",
            "asociación",
            "causal",
            "intervalo de confianza",
            "significación estadística",
            "transferibilidad",
        ):
            self.assertIn(concept, theory)

    def test_statistics_are_not_reduced_to_thresholds(self) -> None:
        theory = " ".join(p for section in self.unit["theory_sections"] for p in section["paragraphs"]).casefold()
        self.assertIn("no es la probabilidad de que la hipótesis nula sea verdadera", theory)
        self.assertIn("no comunica el tamaño del efecto", theory)
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("SE(\\bar x_1-\\bar x_2)=\\sqrt{\\frac{s_1^2}{n_1}+\\frac{s_2^2}{n_2}}", equations)

    def test_pedagogy_progressively_removes_support(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertGreaterEqual(len(activities), 3)
        titles = " ".join(activity["title"] for activity in activities).casefold()
        self.assertIn("actividad guiada", titles)
        self.assertIn("apoyo reducido", titles)
        self.assertIn("reto autónomo", titles)
        first = activities[0]
        self.assertGreaterEqual(len(first["problems"]), 10)
        self.assertGreaterEqual(len(first["deliverables"]), 6)
        self.assertGreaterEqual(len(first["checking_criteria"]), 8)
        all_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintético", all_text)
        self.assertNotIn("datos de pacientes reales", all_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 18)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("afirmación", "razonamiento", "valor p", "spin", "transferibilidad"):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_current_where_needed(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://www.icmje.org/icmje-recommendations.pdf", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/27209009/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/29565659/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/20501928/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/40228833/", urls)

    def test_scope_and_professional_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no autorizan diagnóstico", notice)
        self.assertIn("significación estadística", purpose)
        self.assertIn("importancia clínica", purpose)


if __name__ == "__main__":
    unittest.main()
