from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "laboratorio-biomecanica" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "laboratorio-biomecanica" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class LaboratorioBiomecanicaUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()
        cls.theory = " ".join(
            paragraph
            for section in cls.unit["theory_sections"]
            for paragraph in section["paragraphs"]
        ).casefold()

    def test_source_and_generated_mirror_match(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "laboratorio-biomecanica")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        for concept in (
            "plataforma de fuerza",
            "centro de presión",
            "momento libre",
            "impulso",
            "crosstalk",
            "calibración in situ",
            "sincronización",
        ):
            self.assertIn(concept, self.text)

    def test_theory_is_substantive_and_measurement_focused(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        for concept in (
            "wrench",
            "offset",
            "centro de masa",
            "umbral de contacto",
            "regla trapezoidal",
            "transformación espacial",
            "rmse",
        ):
            self.assertIn(concept, self.theory)

    def test_core_equations_cover_cop_impulse_and_error(self) -> None:
        equations = [
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        ]
        joined = " ".join(equations)
        self.assertIn("x_{COP}", joined)
        self.assertIn("M_{free,z}", joined)
        self.assertIn("\\mathbf J", joined)
        self.assertIn("\\Delta p_z", joined)
        self.assertIn("RMSE_{COP}", joined)

    def test_guided_activity_is_synthetic_and_complete(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 6)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 12)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("exclusivamente", text)
        self.assertIn("no uses participantes", text)
        self.assertIn("umbral", text)
        self.assertIn("impulso", text)
        self.assertIn("crosstalk", text)

    def test_learning_support_is_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "plataforma de fuerza",
            "fuerza de reacción del suelo",
            "centro de presión",
            "momento libre",
            "impulso",
            "crosstalk",
            "calibración in situ",
            "sincronización",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_disciplinary(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://pubmed.ncbi.nlm.nih.gov/18755590/",
            "https://pubmed.ncbi.nlm.nih.gov/28763716/",
            "https://pubmed.ncbi.nlm.nih.gov/20095462/",
            "https://pubmed.ncbi.nlm.nih.gov/2384485/",
            "https://pubmed.ncbi.nlm.nih.gov/10521614/",
            "https://pubmed.ncbi.nlm.nih.gov/12443947/",
            "https://pubmed.ncbi.nlm.nih.gov/25405420/",
            "https://pubmed.ncbi.nlm.nih.gov/22889928/",
            "https://pubmed.ncbi.nlm.nih.gov/34283131/",
            "https://www.isbweb.org/activities/standards",
        ):
            self.assertIn(url, urls)

    def test_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no se opera equipamiento sobre personas", notice)
        self.assertIn("u2 desarrolla la cadena cinemática", notice)
        self.assertIn("u4 incorporará emg", notice)
        self.assertIn("u5 integrará", notice)
        self.assertIn("diagnóstico", purpose)
        self.assertIn("riesgo individual", purpose)


if __name__ == "__main__":
    unittest.main()
