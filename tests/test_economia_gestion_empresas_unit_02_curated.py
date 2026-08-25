from __future__ import annotations

# Final human trigger after automated publication synchronization; academic U2 content is unchanged.

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "economia-gestion-empresas" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "economia-gestion-empresas" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class EconomiaGestionEmpresasUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_exact_mirror_and_review_status(self):
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_and_premature_mcda_are_removed(self):
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("v(a)=", text)
        for concept in ("base de devengo", "margen de contribución", "punto de equilibrio", "capital de trabajo", "presupuesto flexible"):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_keeps_u5_boundary(self):
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        self.assertIn("1 de enero de 2027", theory)
        self.assertIn("se reserva para u5", theory)
        self.assertIn("no es una auditoría", theory)

    def test_core_equations_are_present(self):
        equations = {e["latex"] for section in self.unit["theory_sections"] for e in section.get("equations", [])}
        for equation in ("A=L+E", "CM_u=P-V_u", r"Q_{BE}=\frac{F}{P-V_u}", "NWC=CA-CL", r"CR=\frac{CA}{CL}", "Var=Actual-Budget"):
            self.assertIn(equation, equations)

    def test_examples_and_guided_activity_are_scaffolded_and_synthetic(self):
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 6)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 7)
        self.assertGreaterEqual(len(activity["problems"]), 14)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("fictici", text)
        self.assertIn("no incorpores", text)

    def test_glossary_errors_and_assessment_are_specific(self):
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("estado de situación financiera", "base de devengo", "margen de contribución", "punto de equilibrio", "razón corriente", "presupuesto flexible"):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_time_aware(self):
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(source["verification_status"] == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        self.assertIn("https://www.ifrs.org/issued-standards/list-of-standards/ifrs-18-presentation-and-disclosure-in-financial-statements/", urls)
        self.assertIn("https://www.ifrs.org/content/dam/ifrs/publications/pdf-standards/english/2022/issued/part-a/ias-7-statement-of-cash-flows.pdf?bypass=on", urls)
        self.assertIn("https://openstax.org/books/principles-finance-2e/pages/19-1-what-is-working-capital", urls)

    def test_professional_boundaries_are_explicit(self):
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        for phrase in ("no constituye revisión disciplinar externa", "cumplimiento ifrs", "recomendación de inversión", "evaluación económica sanitaria"):
            self.assertIn(phrase, notice)
        self.assertIn("sin presentar", purpose)


if __name__ == "__main__":
    unittest.main()
