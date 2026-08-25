from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "economia-gestion-empresas" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "economia-gestion-empresas" / "unit-05.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class EconomiaGestionEmpresasUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self):
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_and_diagnostic_sensitivity_contamination_are_removed(self):
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        glossary = {entry["term"].casefold(): entry["definition"].casefold() for entry in self.unit["glossary"]}
        sensitivity = glossary["análisis de sensibilidad"]
        self.assertIn("resultados económicos", sensitivity)
        self.assertNotIn("casos positivos", sensitivity)
        theory = " ".join(p for section in self.unit["theory_sections"] for p in section["paragraphs"]).casefold()
        self.assertIn("no significa sensibilidad diagnóstica", theory)

    def test_theory_is_substantive_and_keeps_economic_boundaries(self):
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "perspectiva",
            "horizonte temporal",
            "dominancia",
            "icer",
            "beneficio monetario neto",
            "impacto presupuestario",
            "asequibilidad",
            "análisis probabilístico",
            "estructura del modelo",
            "cheers 2022",
        ):
            self.assertIn(concept, theory)
        self.assertIn("la incertidumbre no es solo paramétrica", theory)
        self.assertIn("no demuestra que exista presupuesto disponible", theory)
        self.assertIn("no un sello que garantice", theory)

    def test_core_equations_are_present(self):
        equations = {e["latex"] for section in self.unit["theory_sections"] for e in section.get("equations", [])}
        for equation in (
            r"QALY=\sum_j u_j\,\Delta t_j",
            r"PV(X_t)=\frac{X_t}{(1+r)^t}",
            r"\Delta C=C_A-C_B",
            r"\Delta E=E_A-E_B",
            r"ICER=\frac{\Delta C}{\Delta E}",
            r"INMB=\lambda\Delta E-\Delta C",
            r"N_{tratados,t}=N_{elegibles,t}\times p_{adopcion,t}",
            r"BI_t=C_{nuevo,t}-C_{actual,t}",
        ):
            self.assertIn(equation, equations)

    def test_guided_activity_is_synthetic_scaffolded_and_auditable(self):
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(activity.get("duration_minutes", 0), 270)
        self.assertGreaterEqual(len(activity["instructions"]), 12)
        self.assertGreaterEqual(len(activity["problems"]), 25)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 14)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("conjunto sintético", text)
        self.assertIn("no incorpores datos identificables", text)
        self.assertIn("icer", text)
        self.assertIn("impacto presupuestario", text)
        self.assertIn("cheers 2022", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self):
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 12)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "evaluación económica sanitaria",
            "comparador",
            "perspectiva",
            "qaly",
            "icer",
            "dominancia",
            "beneficio monetario neto",
            "impacto presupuestario",
            "asequibilidad",
            "análisis de sensibilidad",
            "análisis probabilístico",
            "cheers 2022",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_cover_core_methodology(self):
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(source["verification_status"] == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC8755935/", urls)
        self.assertIn("https://www.nice.org.uk/process/pmg36/chapter/economic-evaluation-2/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/24438712/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/27623463/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/22999133/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/22999134/", urls)
        self.assertIn("https://www.who.int/publications/i/item/9789240110878", urls)

    def test_real_world_boundary_is_explicit(self):
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituyen revisión disciplinar externa", notice)
        self.assertIn("evaluación económica oficial", notice)
        self.assertIn("recomendación de reembolso", notice)
        self.assertIn("asesoría de compra", notice)
        self.assertIn("coste-efectividad de asequibilidad", purpose)
        self.assertIn("decisión de financiación", purpose)


if __name__ == "__main__":
    unittest.main()
