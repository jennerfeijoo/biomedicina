# Final user-authored trigger after public synchronization and regression correction.
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "ingenieria-tejidos" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "ingenieria-tejidos" / "unit-04.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class IngenieriaTejidosUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "ingenieria-tejidos")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_wrong_mechanics_equation_are_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("\\sigma=\\frac{f}{a_0}", text)
        for concept in (
            "difusión-reacción",
            "número de péclet",
            "red perfusable",
            "anastomosis",
            "mecanotransducción",
            "monitorización",
        ):
            self.assertIn(concept, text)

    def test_theory_is_transport_specific_and_substantive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "condiciones de frontera",
            "consumo",
            "caudal que registra una bomba",
            "heterogeneidad espacial",
            "perfusabilidad",
            "esfuerzo cortante",
            "controles discriminantes",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no es una puntuación de «buena perfusión»", theory)
        self.assertIn("no sobre seguridad o eficacia en personas", theory)

    def test_transport_equations_are_present_and_bounded(self) -> None:
        equations = [e for section in self.unit["theory_sections"] for e in section.get("equations", [])]
        latex = {e["latex"] for e in equations}
        for equation in (
            "\\mathbf{J}=-D\\nabla C",
            "t_D\\sim\\frac{L^2}{D}",
            "\\frac{\\partial C}{\\partial t}=D\\nabla^2 C-R(C)",
            "Pe=\\frac{uL}{D}",
            "\\frac{dM}{dt}=\\dot m_{in}-\\dot m_{out}-\\dot m_{cons}",
        ):
            self.assertIn(equation, latex)
        meanings = " ".join(e["meaning"] for e in equations).casefold()
        self.assertIn("no determina por sí sola viabilidad", meanings)
        self.assertIn("no certifica uniformidad", meanings)

    def test_guided_activities_are_progressive_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintético", text)
        self.assertIn("retira parte de la ayuda", text)
        self.assertIn("sin plantilla", text)
        self.assertIn("u5", text)
        self.assertIn("u6", text)
        total_items = sum(
            len(activity.get(key, []))
            for activity in activities
            for key in ("instructions", "problems", "tasks", "deliverables", "checking_criteria")
        )
        self.assertGreaterEqual(total_items, 75)

    def test_learning_support_is_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "difusión",
            "difusividad efectiva",
            "número de péclet",
            "vascularización",
            "red perfusable",
            "biorreactor",
            "mecanotransducción",
            "control discriminante",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_transport_relevant(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://pubmed.ncbi.nlm.nih.gov/19496677/",
            "https://pubmed.ncbi.nlm.nih.gov/23507883/",
            "https://pubmed.ncbi.nlm.nih.gov/28374578/",
            "https://pubmed.ncbi.nlm.nih.gov/20799909/",
            "https://pubmed.ncbi.nlm.nih.gov/12031108/",
            "https://pubmed.ncbi.nlm.nih.gov/14551059/",
            "https://pubmed.ncbi.nlm.nih.gov/36751469/",
            "https://pubmed.ncbi.nlm.nih.gov/19226211/",
            "https://pubmed.ncbi.nlm.nih.gov/35223131/",
        ):
            self.assertIn(url, urls)

    def test_curricular_and_safety_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        for boundary in (
            "u5",
            "u6",
            "no se proporcionan protocolos",
            "no constituye revisión disciplinar externa",
            "evaluación preclínica o clínica",
        ):
            self.assertIn(boundary, notice)
        self.assertIn("perfusión con vascularización funcional", purpose)
        self.assertIn("eficacia preclínica o clínica", purpose)


if __name__ == "__main__":
    unittest.main()
