from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "economia-gestion-empresas" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "economia-gestion-empresas" / "unit-04.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"
OLD_IMAGE_SEGMENTATION = "asignación de píxeles o vóxeles a regiones de interés según criterios anatómicos, funcionales o algorítmicos"


class EconomiaGestionEmpresasUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_exact_mirror_and_review_status(self):
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["title"], "Mercado y estrategia")
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_domain_contamination_are_removed(self):
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn(OLD_IMAGE_SEGMENTATION, text)
        self.assertNotIn("v(a)=", text)
        glossary = {item["term"].casefold(): item["definition"].casefold() for item in self.unit["glossary"]}
        self.assertIn("segmentación de mercado", glossary)
        self.assertNotIn("píxeles", glossary["segmentación de mercado"])
        self.assertIn("segmentación de imágenes", glossary)

    def test_theory_is_substantive_and_strategy_specific(self):
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "centro de compra",
            "segmentación",
            "statu quo",
            "propuesta de valor",
            "posicionamiento",
            "dimensionar una oportunidad",
            "coste-efectividad",
        ):
            self.assertIn(concept, theory)
        self.assertIn("u5", theory)
        self.assertIn("u6", theory)

    def test_bottom_up_equations_are_present_and_old_mcda_is_absent(self):
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        for equation in (
            r"S_j=\frac{N_j}{N_{ref}}",
            r"N_{eligible}=N_{ref}\,p_{eligible}",
            r"D_{period}=N_{eligible}\,f_{use}",
            r"Q_{scenario}=D_{period}\,a",
        ):
            self.assertIn(equation, equations)
        self.assertTrue(all(not equation.startswith("V(a)=") for equation in equations))

    def test_examples_and_guided_activity_are_scaffolded_and_synthetic(self):
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 6)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 9)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 12)
        activity_text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("fictici", activity_text)
        self.assertIn("no uses datos personales", activity_text)
        self.assertIn("statu quo", activity_text)
        self.assertIn("claim", activity_text)
        self.assertIn("u5", activity_text)

    def test_glossary_errors_and_assessment_are_specific(self):
        self.assertGreaterEqual(len(self.unit["glossary"]), 30)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 12)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "segmentación de mercado",
            "segmentación firmográfica",
            "centro de compra",
            "statu quo",
            "propuesta de valor",
            "uso previsto",
            "dimensionamiento bottom-up",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_cover_marketing_procurement_and_claims(self):
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 12)
        self.assertTrue(all(source["verification_status"] == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        self.assertIn("https://openstax.org/books/principles-marketing/pages/5-1-market-segmentation-and-consumer-markets", urls)
        self.assertIn("https://openstax.org/books/principles-marketing/pages/4-2-buyers-and-buying-situations-in-a-b2b-market", urls)
        self.assertIn("https://www.who.int/publications/i/item/9789241501378", urls)
        self.assertIn("https://www.fda.gov/medical-devices/classify-your-medical-device/how-determine-if-your-product-medical-device", urls)
        self.assertIn("https://www.fda.gov/medical-devices/general-device-labeling-requirements/labeling-requirements-misbranding", urls)

    def test_scope_boundaries_are_explicit(self):
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        for phrase in (
            "no constituye revisión disciplinar externa",
            "recomendación de inversión",
            "evaluación económica sanitaria",
            "validación clínica",
            "conformidad regulatoria",
            "marco estadounidense",
        ):
            self.assertIn(phrase, notice)
        self.assertIn("eficacia clínica", purpose)
        self.assertIn("evaluación económica sanitaria", purpose)


if __name__ == "__main__":
    unittest.main()
