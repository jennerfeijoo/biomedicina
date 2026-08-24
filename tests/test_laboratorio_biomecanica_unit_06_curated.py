from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "laboratorio-biomecanica" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "laboratorio-biomecanica" / "unit-06.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class LaboratorioBiomecanicaUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "laboratorio-biomecanica")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_wrong_mechanics_focus_are_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("\\sum \\mathbf{f}=m\\mathbf{a}", text)
        for concept in ("incertidumbre de medición", "icc", "mdc", "bland-altman", "fair", "checksum"):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_closes_the_lab_pipeline(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "estimando",
            "procedencia",
            "fiabilidad",
            "acuerdo",
            "pseudorreplicación",
            "intervalo de confianza",
            "metadatos",
            "reproducibilidad",
        ):
            self.assertIn(concept, theory)

    def test_core_reporting_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("SEM=SD\\sqrt{1-ICC}", equations)
        self.assertIn("MDC_{95}=1.96\\sqrt{2}\\,SEM", equations)
        self.assertIn("LoA=\\bar d\\pm1.96\\,s_d", equations)
        self.assertIn("u_c(y)=\\sqrt{\\sum_i \\left(c_i u(x_i)\\right)^2}", equations)

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 10)
        self.assertGreaterEqual(len(activity["problems"]), 15)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 14)
        activity_text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintético", activity_text)
        self.assertIn("no registres participantes", activity_text)
        self.assertIn("claim→evidencia", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 6)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 12)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("estimando", "incertidumbre de medición", "icc", "sem", "mdc", "límites de acuerdo", "fair", "checksum"):
            self.assertIn(term, terms)

    def test_reliability_agreement_and_clinical_boundaries_are_explicit(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertIn("correlación no demuestra acuerdo", text)
        self.assertIn("mdc no", text)
        self.assertIn("importancia clínica", text)
        self.assertIn("reproducibilidad no", text)
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no constituye", notice)
        self.assertIn("datos de participantes", notice)

    def test_sources_are_directly_traceable(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        expected = {
            "https://www.bipm.org/en/doi/10.59161/jcgm100-2008e",
            "https://www.bipm.org/en/doi/10.59161/jcgm101-2008",
            "https://pubmed.ncbi.nlm.nih.gov/27330520/",
            "https://pubmed.ncbi.nlm.nih.gov/2868172/",
            "https://pubmed.ncbi.nlm.nih.gov/26978244/",
            "https://pubmed.ncbi.nlm.nih.gov/31791632/",
            "https://pubmed.ncbi.nlm.nih.gov/25901488/",
        }
        self.assertTrue(expected.issubset(urls))


if __name__ == "__main__":
    unittest.main()
