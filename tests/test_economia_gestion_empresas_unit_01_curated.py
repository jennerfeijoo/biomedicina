from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "economia-gestion-empresas" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "economia-gestion-empresas" / "unit-01.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"

# Final user-authored trigger after the generated public site was synchronized.


class EconomiaGestionEmpresasUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self):
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self):
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in ("coste de oportunidad", "elasticidad", "información asimétrica", "eficiencia asignativa", "equidad"):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_keeps_u5_boundary(self):
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        self.assertIn("evaluación económica formal", theory)
        self.assertIn("se reserva para u5", theory)
        self.assertIn("no implica", theory)

    def test_core_equations_are_present(self):
        equations = {e["latex"] for s in self.unit["theory_sections"] for e in s.get("equations", [])}
        self.assertIn(r"p_x x + p_y y \leq B", equations)
        self.assertIn(r"\varepsilon_D=\frac{\%\Delta Q_D}{\%\Delta P}", equations)

    def test_examples_and_guided_activity_are_synthetic_and_scaffolded(self):
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 6)
        self.assertGreaterEqual(len(activity["problems"]), 10)
        self.assertGreaterEqual(len(activity["deliverables"]), 6)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 8)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintét", text)
        self.assertIn("no uses", text)

    def test_glossary_errors_and_assessment_are_specific(self):
        self.assertGreaterEqual(len(self.unit["glossary"]), 18)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("coste de oportunidad", "elasticidad-precio de la demanda", "información asimétrica", "eficiencia técnica", "eficiencia asignativa"):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified(self):
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(source["verification_status"] == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC2585909/", urls)
        self.assertIn("https://www.nice.org.uk/process/pmg6/chapter/assessing-cost-effectiveness", urls)
        self.assertIn("https://www.who.int/teams/health-systems-governance-and-financing/economic-analysis/costing-and-technical-efficiency/technical-efficiency", urls)

    def test_decision_boundary_is_explicit(self):
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("recomendación de financiación", notice)
        self.assertIn("política pública real", purpose)


if __name__ == "__main__":
    unittest.main()
