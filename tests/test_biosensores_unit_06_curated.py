from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biosensores" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "biosensores" / "unit-06.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiosensoresUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biosensores")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        for concept in ("point-of-care", "wearable", "uso previsto", "contexto de uso"):
            self.assertIn(concept, self.text)

    def test_theory_separates_evidence_layers(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "verificación",
            "desempeño analítico",
            "desempeño clínico",
            "utilidad clínica",
            "factores humanos",
            "integridad de datos",
            "prevalencia",
            "seguimiento",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no se declara beneficio clínico real", theory)

    def test_diagnostic_and_wearable_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("Se=\\frac{TP}{TP+FN},\\qquad Sp=\\frac{TN}{TN+FP}", equations)
        self.assertIn("PPV=\\frac{Se\\,p}{Se\\,p+(1-Sp)(1-p)}", equations)
        self.assertIn("C=\\frac{T_{valid}}{T_{expected}}\\times100\\%", equations)

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        for concept in ("sintétic", "prevalencia", "datos faltantes", "tareas críticas", "algoritmo"):
            self.assertIn(concept, text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "uso previsto",
            "point-of-care testing",
            "wearable",
            "validación clínica",
            "utilidad clínica",
            "factores humanos",
            "integridad de datos",
            "conformidad regulatoria",
        ):
            self.assertIn(term, terms)

    def test_sources_are_current_traceable_and_scope_aware(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://www.nature.com/articles/s41746-020-0260-4",
            "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/digital-health-technologies-remote-data-acquisition-clinical-investigations",
            "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/applying-human-factors-and-usability-engineering-medical-devices",
            "https://eur-lex.europa.eu/eli/reg/2017/746",
            "https://www.iso.org/standard/76677.html",
        ):
            self.assertIn(url, urls)
        iso_22870 = next(item for item in sources if "22870" in item["title"])
        self.assertIn("retirada", (iso_22870["type"] + " " + iso_22870["description"]).casefold())

    def test_regulatory_and_clinical_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no constituye revisión disciplinar externa",
            "validación clínica",
            "evaluación de conformidad",
            "autorización de comercialización",
            "datos y escenarios son sintéticos",
        ):
            self.assertIn(phrase, notice)
        self.assertIn("iso 22870:2016", notice)
        self.assertIn("norma retirada", notice)


if __name__ == "__main__":
    unittest.main()
