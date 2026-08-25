from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "economia-gestion-empresas" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "economia-gestion-empresas" / "unit-04.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"
# Final user-authored trigger after successful U4 curation and cleanup.


class EconomiaGestionEmpresasUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self):
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["status"], "review")

    def test_cross_domain_definition_and_generic_template_are_removed(self):
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        glossary = {entry["term"].casefold(): entry["definition"].casefold() for entry in self.unit["glossary"]}
        market_definition = glossary["segmentación de mercado"]
        self.assertNotIn("píxeles", market_definition)
        self.assertNotIn("vóxeles", market_definition)
        self.assertIn("grupos", market_definition)
        theory = " ".join(p for section in self.unit["theory_sections"] for p in section["paragraphs"]).casefold()
        self.assertIn("no significa etiquetar píxeles ni vóxeles", theory)
        for concept in (
            "segmentación de mercado",
            "segmento objetivo",
            "centro de compra",
            "sustituto",
            "propuesta de valor",
            "posicionamiento",
            "tam",
            "sam",
            "som",
            "hta",
        ):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_keeps_strategy_boundaries(self):
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        self.assertIn("centro de compra", theory)
        self.assertIn("usuarios", theory)
        self.assertIn("compradores", theory)
        self.assertIn("decisores", theory)
        self.assertIn("pagador distinto del comprador", theory)
        self.assertIn("ausencia de un producto idéntico no implica ausencia de competencia", theory)
        self.assertIn("no autoriza afirmar superioridad clínica", theory)
        self.assertIn("escenario, no como pronóstico", theory)
        self.assertIn("aprobación regulatoria", theory)
        self.assertIn("evaluación de tecnologías sanitarias", theory)

    def test_market_sizing_equations_are_scenarios_not_forecasts(self):
        equations = {e["latex"] for section in self.unit["theory_sections"] for e in section.get("equations", [])}
        self.assertIn(r"N_{adoptantes}=N_{accesibles}\times p_{adopcion}", equations)
        self.assertIn(r"V_{escenario}=N_{adoptantes}\times q\times P", equations)
        theory = " ".join(p for section in self.unit["theory_sections"] for p in section["paragraphs"]).casefold()
        self.assertIn("no como pronóstico", theory)

    def test_guided_activity_is_synthetic_scaffolded_and_auditable(self):
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(activity.get("duration_minutes", 0), 240)
        self.assertGreaterEqual(len(activity["instructions"]), 10)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 12)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintético", text)
        self.assertIn("no uses datos personales", text)
        self.assertIn("tam", text)
        self.assertIn("regulación", text)
        self.assertIn("hta", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self):
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 12)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "segmentación de mercado",
            "segmento objetivo",
            "centro de compra",
            "propuesta de valor",
            "posicionamiento",
            "tam",
            "sam",
            "som",
            "hta",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_cover_core_domains(self):
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(source["verification_status"] == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        self.assertIn("https://openstax.org/books/principles-marketing/pages/5-1-market-segmentation-and-consumer-markets", urls)
        self.assertIn("https://openstax.org/books/principles-marketing/pages/5-2-segmentation-of-b2b-markets", urls)
        self.assertIn("https://openstax.org/books/principles-marketing/pages/4-2-buyers-and-buying-situations-in-a-b2b-market", urls)
        self.assertIn("https://openstax.org/books/principles-marketing/pages/5-6-product-positioning", urls)
        self.assertIn("https://hbr.org/2008/01/the-five-competitive-forces-that-shape-strategy", urls)
        self.assertIn("https://www.who.int/publications/i/item/9789240110878", urls)

    def test_real_world_boundary_is_explicit(self):
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituyen revisión disciplinar externa", notice)
        self.assertIn("asesoría comercial", notice)
        self.assertIn("aprobación regulatoria", notice)
        self.assertIn("hta", notice)
        self.assertIn("atractivo comercial", purpose)
        self.assertIn("valor clínico", purpose)


if __name__ == "__main__":
    unittest.main()
