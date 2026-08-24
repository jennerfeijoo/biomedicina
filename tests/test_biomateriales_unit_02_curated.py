from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomateriales" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "biomateriales" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomaterialesUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomateriales")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed_and_scope_is_structure_property(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "microestructura",
            "porosidad",
            "tensión–deformación",
            "viscoelasticidad",
            "transición vítrea",
            "ángulo de contacto",
            "comportamiento en servicio",
        ):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_separated_from_u3_biology(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        text = " ".join(p for s in sections for p in s["paragraphs"]).casefold()
        self.assertIn("u3 será la unidad adecuada", text)
        self.assertIn("no equivale directamente", text)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn(r"\sigma=\frac{F}{A_0}", equations)
        self.assertIn(r"k=\frac{EA}{L}", equations)
        self.assertIn(r"\tau=\frac{\eta}{E}", equations)
        self.assertIn(r"\gamma_{SV}=\gamma_{SL}+\gamma_{LV}\cos\theta", equations)

    def test_guided_activities_are_progressive_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertGreaterEqual(len(activities), 3)
        titles = {a["title"] for a in activities}
        self.assertIn("Actividad guiada: reconstrucción de una curva tensión–deformación sintética", titles)
        self.assertIn("Actividad guiada: sensibilidad térmica y viscoelástica de un polímero", titles)
        self.assertIn("Actividad guiada: auditoría de una afirmación superficial", titles)
        primary = activities[0]
        self.assertGreaterEqual(len(primary["instructions"]), 7)
        self.assertGreaterEqual(len(primary["problems"]), 12)
        self.assertGreaterEqual(len(primary["deliverables"]), 7)
        self.assertGreaterEqual(len(primary["checking_criteria"]), 10)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("no uses muestras humanas", activity_text)
        self.assertIn("análisis de sensibilidad", activity_text)

    def test_assessment_glossary_errors_and_examples_are_substantive(self) -> None:
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 4)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 8)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        self.assertGreaterEqual(len(self.unit["glossary"]), 18)
        terms = {item["term"].casefold() for item in self.unit["glossary"]}
        for term in ("módulo elástico", "rigidez estructural", "transición vítrea", "mojabilidad"):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_current_standards_are_included(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(s.get("verification_status") == "verified_directly" for s in sources))
        urls = {s["url"] for s in sources}
        self.assertIn("https://store.astm.org/e0008_e0008m-25.html", urls)
        self.assertIn("https://store.astm.org/d0638-22.html", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/26369638/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/36205119/", urls)

    def test_clinical_and_regulatory_boundary_is_explicit(self) -> None:
        text = json.dumps(self.unit, ensure_ascii=False).casefold()
        self.assertIn("no constituye revisión disciplinar externa", text)
        self.assertIn("no autorizan ensayos en personas", text)
        self.assertIn("no deben presentarse como demostración de biocompatibilidad", text)
        self.assertIn("desempeño clínico del dispositivo final", text)


# User-authored trigger after synchronized public pages; publication metadata may follow.
if __name__ == "__main__":
    unittest.main()
