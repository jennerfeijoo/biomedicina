from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "fundamentos-biomecanica" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "fundamentos-biomecanica" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class FundamentosBiomecanicaUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "fundamentos-biomecanica")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_dynamics_leak_are_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertIn("diferencia central", text)
        self.assertIn("proyección 2d", text)
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertNotIn("\\sum \\mathbf F=m\\mathbf a", equations)
        self.assertNotIn("\\sum \\mathbf{F}=m\\mathbf{a}", equations)

    def test_theory_is_substantive_and_kinematic(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        word_count = sum(len(paragraph.split()) for section in sections for paragraph in section["paragraphs"])
        self.assertGreaterEqual(word_count, 1100)
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in ("desplazamiento", "velocidad instantánea", "aceleración", "frecuencia de muestreo", "filtrado", "fuera del plano"):
            self.assertIn(concept, theory)
        self.assertIn("unidad siguiente", theory)

    def test_core_kinematic_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("\\Delta \\mathbf r=\\mathbf r_2-\\mathbf r_1", equations)
        self.assertIn("\\bar{\\mathbf v}=\\frac{\\Delta \\mathbf r}{\\Delta t}", equations)
        self.assertIn("\\mathbf v_i\\approx\\frac{\\mathbf r_{i+1}-\\mathbf r_{i-1}}{2\\Delta t}", equations)
        self.assertIn("f_s=1/\\Delta t", equations)

    def test_pedagogy_is_progressive_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertGreaterEqual(len(activities), 3)
        first = activities[0]
        self.assertGreaterEqual(len(first["instructions"]), 5)
        self.assertGreaterEqual(len(first["problems"]), 10)
        self.assertGreaterEqual(len(first["deliverables"]), 6)
        self.assertGreaterEqual(len(first["checking_criteria"]), 10)
        text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintético", text)
        self.assertIn("no grabes personas", text)
        self.assertIn("transferencia", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 18)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 4)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 8)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("cinemática", "desplazamiento", "velocidad", "aceleración", "frecuencia de muestreo", "proyección 2d"):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_directly_verified(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/11934426/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/4837552/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/34283131/", urls)
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC8884063/", urls)
        self.assertIn("https://www.isbweb.org/activities/standards", urls)

    def test_editorial_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no autoriza inferir fuerzas internas", notice)
        self.assertIn("sin atribuir", purpose)
        self.assertIn("conclusión clínica", purpose)


if __name__ == "__main__":
    unittest.main()

# Final user-authored verification trigger after public-site synchronization.
