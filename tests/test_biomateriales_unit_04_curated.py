from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomateriales" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "biomateriales" / "unit-04.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomaterialesUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomateriales")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_irrelevant_stress_equation_are_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn(r"\sigma=\frac{f}{a_0}".casefold(), text)
        for concept in (
            "pasivación",
            "corrosión por picadura",
            "corrosión galvánica",
            "fretting",
            "tribocorrosión",
            "escisión de cadena",
            "erosión en volumen",
            "autocatalización",
        ):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_preserves_unit_boundaries(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for s in sections for p in s["paragraphs"]).casefold()
        self.assertIn("u5 desarrollará", theory)
        self.assertIn("se reserva para u6", theory)
        self.assertIn("no garantiza superioridad clínica", theory)
        self.assertIn("todavía no sustituye", theory)

    def test_core_equations_are_relevant_and_limited(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn(r"m=\frac{M I t}{nF}", equations)
        self.assertIn(r"V=k\frac{WL}{H}", equations)
        self.assertIn(r"T=W_0+C_0+S", equations)
        self.assertIn(r"M_n(t)=M_{n,0}e^{-kt}", equations)
        self.assertIn(r"f_{rec}=\frac{m_{recuperada}}{m_{perdida}}", equations)

    def test_guided_activities_are_progressive_synthetic_and_scaffolded(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertGreaterEqual(len(activities), 3)
        titles = {activity["title"] for activity in activities}
        self.assertIn("Actividad guiada: mapa de corrosión de un implante metálico sintético", titles)
        self.assertIn("Actividad guiada: descomponer una señal de tribocorrosión", titles)
        self.assertIn("Actividad integradora: expediente sintético de estabilidad de un biomaterial", titles)
        primary = activities[0]
        self.assertGreaterEqual(len(primary["instructions"]), 8)
        self.assertGreaterEqual(len(primary["problems"]), 12)
        self.assertGreaterEqual(len(primary["deliverables"]), 7)
        self.assertGreaterEqual(len(primary["checking_criteria"]), 10)
        text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("datos sintéticos", text)
        self.assertIn("no realices ensayos electroquímicos reales", text)
        self.assertIn("no se afirma seguridad clínica", text)

    def test_glossary_examples_errors_and_assessment_are_substantive(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 25)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "pasivación",
            "potencial de ruptura",
            "tribocorrosión",
            "masa molar promedio numérica",
            "degradación acelerada",
            "balance de masa",
        ):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_current_versions_are_explicit(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(source.get("verification_status") == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        self.assertIn("https://www.iso.org/standard/68937.html", urls)
        self.assertIn("https://www.iso.org/es/contents/data/standard/04/40/44050.html", urls)
        self.assertIn("https://www.iso.org/standard/90742.html", urls)
        self.assertIn("https://store.astm.org/f2129-25.html", urls)
        self.assertIn("https://store.astm.org/g0119-09r21.html", urls)
        self.assertIn("https://store.astm.org/f1635-24.html", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/38525435/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/36206552/", urls)

    def test_accelerated_testing_and_clinical_boundaries_are_explicit(self) -> None:
        text = json.dumps(self.unit, ensure_ascii=False).casefold()
        self.assertIn("acelerado no significa automáticamente equivalente", text)
        self.assertIn("no constituye revisión disciplinar externa", text)
        self.assertIn("no autorizan ensayos electroquímicos", text)
        self.assertIn("u5 conserva la caracterización instrumental detallada", text)
        self.assertIn("u6 el diseño de evaluación preclínica", text)
        self.assertIn("no se extrapola astm f2129-25 a seguridad clínica", text)


if __name__ == "__main__":
    unittest.main()
