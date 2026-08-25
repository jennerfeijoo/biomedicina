from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "economia-gestion-empresas" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "economia-gestion-empresas" / "unit-04.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class EconomiaGestionEmpresasUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_exact_mirror_and_review_status(self):
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "economia-gestion-empresas")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["status"], "review")

    def test_imaging_segmentation_generic_template_and_old_mcda_are_removed(self):
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("píxeles", text)
        self.assertNotIn("vóxeles", text)
        self.assertNotIn("v(a)=", text)
        for concept in (
            "segmentación de mercado",
            "statu quo",
            "propuesta de valor",
            "nasss",
            "procurement",
            "uso previsto",
        ):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_keeps_u5_u6_boundaries(self):
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        self.assertIn("reserva para u5 la evaluación económica sanitaria formal", theory)
        self.assertIn("para u6 la gobernanza", theory)
        self.assertIn("no pretende ser una solución predictiva o formulaica", theory)

    def test_scenario_equations_are_present_and_bounded(self):
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        for equation in (
            "SegmentShare=N_segment/N_eligible",
            "AnnualVolume=N_eligible*AdoptionRate*UnitsPerAdopter",
            "ScenarioRevenue=AnnualVolume*NetPrice",
        ):
            self.assertIn(equation, equations)
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertIn("no es una predicción validada", text)
        self.assertIn("no valor sanitario", text)

    def test_examples_and_progressive_activities_are_synthetic(self):
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 6)
        activities = self.unit["guided_activities"]
        self.assertGreaterEqual(len(activities), 3)
        guided = activities[1]
        self.assertGreaterEqual(len(guided["instructions"]), 9)
        self.assertGreaterEqual(len(guided["problems"]), 16)
        self.assertGreaterEqual(len(guided["deliverables"]), 9)
        self.assertGreaterEqual(len(guided["checking_criteria"]), 12)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintético", activity_text)
        self.assertIn("no hagas entrevistas", activity_text)
        self.assertIn("reto autónomo", activity_text)

    def test_glossary_errors_assessment_and_connections_are_specific(self):
        self.assertGreaterEqual(len(self.unit["glossary"]), 28)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 12)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 5)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "segmentación de mercado",
            "segmento objetivo",
            "comprador",
            "pagador",
            "statu quo",
            "posicionamiento",
            "propuesta de valor",
            "procurement",
            "análisis de sensibilidad",
            "nasss",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_current_where_needed(self):
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(source["verification_status"] == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        for url in (
            "https://www.who.int/publications/i/item/9789241501385",
            "https://www.who.int/publications/i/item/9789241501378",
            "https://eur-lex.europa.eu/eli/reg/2017/745/oj/eng",
            "https://pubmed.ncbi.nlm.nih.gov/29092808/",
            "https://pubmed.ncbi.nlm.nih.gov/40622303/",
            "https://pubmed.ncbi.nlm.nih.gov/36581959/",
        ):
            self.assertIn(url, urls)

    def test_professional_and_inference_boundaries_are_explicit(self):
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        for phrase in (
            "no constituye revisión disciplinar externa",
            "forecast comercial",
            "asesoría de inversión",
            "autorización de claims",
            "recomendación de procurement",
            "evaluación económica sanitaria",
            "recomendación clínica",
        ):
            self.assertIn(phrase, notice)
        self.assertIn("sin confundir tamaño de mercado", purpose)
        self.assertIn("beneficio clínico", purpose)


if __name__ == "__main__":
    unittest.main()
