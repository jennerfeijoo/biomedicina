from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "economia-gestion-empresas" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "economia-gestion-empresas" / "unit-06.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class EconomiaGestionEmpresasUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self):
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed_and_scope_is_governance(self):
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "gobernanza",
            "accountability",
            "derechos de decisión",
            "kpi",
            "gestión del riesgo",
            "compliance",
            "assurance",
        ):
            self.assertIn(concept, text)
        self.assertNotIn("r=p\\times s", text)

    def test_theory_is_substantive_and_integrates_course_without_duplication(self):
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "gobernanza y gestión no son sinónimos",
            "indicadores adelantados",
            "indicadores rezagados",
            "iso 31000:2018",
            "committee draft",
            "iso 37301:2021",
            "three lines model",
            "u1–u5",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no es una ley cuantitativa universal", theory)
        self.assertIn("no demuestra causalidad", theory)

    def test_core_equations_preserve_interpretive_limits(self):
        equations = {e["latex"] for section in self.unit["theory_sections"] for e in section.get("equations", [])}
        self.assertIn(r"Tasa=\frac{eventos}{oportunidades}\times k", equations)
        self.assertIn(r"Cumplimiento_{meta}=\frac{x}{T}\times100\%", equations)
        self.assertIn(r"E[L]=\sum_{s=1}^{n}p_sL_s", equations)
        self.assertIn(r"Cobertura_{control}=\frac{obligaciones\ con\ control\ documentado}{obligaciones\ aplicables}\times100\%", equations)

    def test_pedagogy_uses_progressive_support_and_synthetic_cases(self):
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertGreaterEqual(activities[0].get("duration_minutes", 0), 270)
        self.assertGreaterEqual(len(activities[0]["problems"]), 18)
        self.assertGreaterEqual(len(activities[0]["deliverables"]), 10)
        self.assertGreaterEqual(len(activities[0]["checking_criteria"]), 12)
        self.assertIn("apoyo reducido", activities[1]["title"].casefold())
        self.assertIn("autónomo", activities[2]["title"].casefold())
        text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintético", text)
        self.assertIn("no incorpores datos personales", text)
        self.assertIn("no se inventan obligaciones jurídicas reales", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self):
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 12)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "gobernanza organizacional",
            "órgano de gobierno",
            "accountability",
            "derecho de decisión",
            "kpi",
            "indicador adelantado",
            "gestión del riesgo",
            "compliance",
            "assurance",
            "registro de decisiones",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_current_status_is_explicit(self):
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(source["verification_status"] == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        for url in (
            "https://www.iso.org/standard/65036.html",
            "https://www.iso.org/standard/65694.html",
            "https://www.iso.org/standard/88574.html",
            "https://www.iso.org/standard/75080.html",
            "https://www.who.int/health-topics/health-systems-governance",
            "https://pubmed.ncbi.nlm.nih.gov/32771874/",
            "https://pubmed.ncbi.nlm.nih.gov/24320168/",
            "https://pubmed.ncbi.nlm.nih.gov/29518702/",
        ):
            self.assertIn(url, urls)
        draft = next(source for source in sources if source["url"] == "https://www.iso.org/standard/88574.html")
        self.assertIn("no se presenta como norma publicada", draft["description"].casefold())

    def test_real_world_and_professional_boundaries_are_explicit(self):
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        for phrase in (
            "no constituyen revisión disciplinar externa",
            "auditoría de gobierno corporativo",
            "certificación iso",
            "determinación jurídica de compliance",
            "validación clínica",
        ):
            self.assertIn(phrase, notice)
        self.assertIn("no confundir gobernanza con gestión diaria", purpose)
        self.assertIn("cumplimiento documentado con certificación", purpose)


if __name__ == "__main__":
    unittest.main()
