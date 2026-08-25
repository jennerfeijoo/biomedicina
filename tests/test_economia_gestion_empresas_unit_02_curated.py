from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "economia-gestion-empresas" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "economia-gestion-empresas" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"

# User-authored trigger after deterministic curation and site synchronization.


class EconomiaGestionEmpresasUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self):
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self):
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "estado de situación financiera",
            "devengo",
            "margen de contribución",
            "punto de equilibrio",
            "presupuesto de caja",
            "valor presente neto",
        ):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_keeps_u5_boundary(self):
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        self.assertIn("se reserva para u5", theory)
        self.assertIn("coste-efectividad", theory)
        self.assertIn("beneficio contable no garantiza efectivo", theory)

    def test_core_equations_are_present(self):
        equations = {e["latex"] for section in self.unit["theory_sections"] for e in section.get("equations", [])}
        self.assertIn(r"A=L+E", equations)
        self.assertIn(r"C_T(q)=F+vq", equations)
        self.assertIn(r"q_{BE}=\frac{F}{p-v}", equations)
        self.assertIn(r"PV=\frac{FV}{(1+r)^n}", equations)
        self.assertIn(r"NPV=\sum_{t=0}^{T}\frac{CF_t}{(1+r)^t}", equations)

    def test_examples_and_guided_activity_are_synthetic_and_scaffolded(self):
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 8)
        self.assertGreaterEqual(len(activity["problems"]), 15)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintético", text)
        self.assertIn("no uses", text)
        self.assertIn("qaly", text)
        self.assertIn("icer", text)

    def test_glossary_errors_and_assessment_are_specific(self):
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 12)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "devengo",
            "coste fijo",
            "coste variable",
            "margen de contribución",
            "punto de equilibrio",
            "liquidez",
            "valor presente neto (npv)",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified(self):
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(source["verification_status"] == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        self.assertIn("https://www.ifrs.org/issued-standards/list-of-standards/conceptual-framework/", urls)
        self.assertIn("https://www.sec.gov/about/reports-publications/beginners-guide-financial-statements", urls)
        self.assertIn("https://openstax.org/books/principles-managerial-accounting/pages/3-2-calculate-a-break-even-point-in-units-and-dollars", urls)
        self.assertIn("https://openstax.org/books/principles-finance-2e/pages/16-2-net-present-value-npv-method", urls)

    def test_financial_decision_boundary_is_explicit(self):
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("asesoría contable", notice)
        self.assertIn("evaluación económica sanitaria formal de u5", purpose)
        self.assertIn("no sustituye contabilidad profesional", purpose)


if __name__ == "__main__":
    unittest.main()
