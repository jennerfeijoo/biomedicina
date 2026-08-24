from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "ingenieria-tejidos" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "ingenieria-tejidos" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class IngenieriaTejidosUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "ingenieria-tejidos")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_and_biomaterials_fallbacks_are_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("\\sigma=\\frac{f}{a_0}", text)
        self.assertNotIn("condición de envejecimiento", text)
        self.assertNotIn("ensayos mecánicos, superficies, degradación", text)
        self.assertIn("autorrenovación", text)
        self.assertIn("heterogeneidad", text)
        self.assertIn("autenticación", text)

    def test_theory_is_cell_source_specific_and_substantive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "células primarias",
            "progenitoras",
            "pluripotentes",
            "stemness",
            "duplicaciones poblacionales",
            "variabilidad entre donantes",
            "estabilidad genómica",
            "células fuera del objetivo",
        ):
            self.assertIn(concept, theory)
        self.assertIn("los marcadores no sustituyen a la función", self.unit["theory_sections"][1]["heading"].casefold())

    def test_population_doubling_equation_is_present_and_bounded(self) -> None:
        equations = [
            equation
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        ]
        self.assertEqual(len(equations), 1)
        self.assertEqual(equations[0]["latex"], "PD=\\log_2\\left(\\frac{N_f}{N_i}\\right)")
        self.assertIn("no identidad, potencia ni función", equations[0]["meaning"].casefold())

    def test_guided_activities_are_progressive_synthetic_and_decision_bounded(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintéticas", text)
        self.assertIn("retira la plantilla", text)
        self.assertIn("necesidad→requisito→evidencia→decisión→límite", text)
        self.assertIn("análisis de sensibilidad", text)
        total_items = sum(
            len(activity.get(key, []))
            for activity in activities
            for key in ("instructions", "problems", "tasks", "deliverables", "checking_criteria")
        )
        self.assertGreaterEqual(total_items, 60)

    def test_learning_support_is_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 4)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "célula primaria",
            "célula madre tisular",
            "célula pluripotente inducida",
            "autorrenovación",
            "duplicación poblacional",
            "estabilidad genómica",
            "trazabilidad de material",
        ):
            self.assertIn(term, terms)

    def test_msc_nomenclature_is_not_overclaimed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertIn("mesenchymal stromal cells", text)
        self.assertIn("no demuestra por sí mismo autorrenovación in vivo", text)
        self.assertIn("especificar origen tisular", text)

    def test_sources_are_directly_verified_and_current_where_needed(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://www.isscr.org/basic-research-standards/",
            "https://www.isscr.org/guidelines",
            "https://pubmed.ncbi.nlm.nih.gov/31526643/",
            "https://pubmed.ncbi.nlm.nih.gov/16923606/",
            "https://pubmed.ncbi.nlm.nih.gov/38873900/",
            "https://pubmed.ncbi.nlm.nih.gov/42367074/",
        ):
            self.assertIn(url, urls)

    def test_editorial_and_clinical_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no proporciona protocolos de aislamiento", notice)
        self.assertIn("no autoriza obtención de muestras", notice)
        self.assertIn("u3", notice)
        self.assertIn("u6", notice)
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("idoneidad clínica", purpose)


if __name__ == "__main__":
    unittest.main()
