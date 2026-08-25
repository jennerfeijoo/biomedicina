from __future__ import annotations

# Final human-authored trigger after public pages and curricular descriptor synchronization.

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "economia-gestion-empresas" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "economia-gestion-empresas" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class EconomiaGestionEmpresasUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_exact_mirror_and_review_status(self):
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "economia-gestion-empresas")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_premature_mcda_are_removed(self):
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("v(a)=", text)
        for concept in (
            "ley de little",
            "cuello de botella",
            "tiempo de respuesta",
            "punto de reposición",
            "pdsa",
            "medida de balance",
        ):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_keeps_curricular_boundaries(self):
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        self.assertIn("u4 abordará mercado y estrategia", theory)
        self.assertIn("u5 evaluación económica", theory)
        self.assertIn("no demuestra por sí solo causalidad", SOURCE.read_text(encoding="utf-8").casefold())

    def test_core_operations_equations_are_present(self):
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        for equation in (
            "L=lambda*W",
            "rho=lambda/(c*mu)",
            "TAT=t_release-t_receipt",
            "RejectRate=N_rejected/N_received",
            "DaysCover=Stock_usable/d",
            "ROP=d*LT+SS",
            "RelativeChange=(Y_post-Y_pre)/Y_pre",
        ):
            self.assertIn(equation, equations)

    def test_examples_and_progressive_activities_are_synthetic(self):
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 6)
        activities = self.unit["guided_activities"]
        self.assertGreaterEqual(len(activities), 3)
        guided = activities[1]
        self.assertGreaterEqual(len(guided["instructions"]), 7)
        self.assertGreaterEqual(len(guided["problems"]), 14)
        self.assertGreaterEqual(len(guided["deliverables"]), 8)
        self.assertGreaterEqual(len(guided["checking_criteria"]), 10)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintético", activity_text)
        self.assertIn("no incorpores datos de pacientes", activity_text)
        self.assertIn("reto autónomo", activity_text)

    def test_glossary_errors_assessment_and_connections_are_specific(self):
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 5)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "capacidad nominal",
            "throughput",
            "ley de little",
            "punto de reposición",
            "medida de balance",
            "pdsa",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_methodologically_relevant(self):
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(source["verification_status"] == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        for url in (
            "https://pubsonline.informs.org/doi/abs/10.1287/opre.9.3.383",
            "https://www.iso.org/standard/76677.html",
            "https://extranet.who.int/lqsi/node/137",
            "https://www.ihi.org/library/model-for-improvement",
            "https://pubmed.ncbi.nlm.nih.gov/34969531/",
        ):
            self.assertIn(url, urls)

    def test_professional_and_clinical_boundaries_are_explicit(self):
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        for phrase in (
            "no constituye revisión disciplinar externa",
            "acreditación iso 15189",
            "decisión de dotación o compra",
            "evaluación económica",
            "recomendación clínica",
        ):
            self.assertIn(phrase, notice)
        self.assertIn("sin convertir una mejora operativa en evidencia clínica", purpose)


if __name__ == "__main__":
    unittest.main()
