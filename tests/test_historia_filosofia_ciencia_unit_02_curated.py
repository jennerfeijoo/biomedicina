from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "historia-filosofia-ciencia" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "historia-filosofia-ciencia" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class HistoriaFilosofiaCienciaUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["slug"], "metodo-explicacion-y-causalidad")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn(r"v(a)=\\sum", self.text)
        self.assertNotIn("modelo multicriterio transparente", self.text)

    def test_objectives_cover_inference_explanation_and_causality(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "validez deductiva",
            "inducción",
            "abducción",
            "supuestos auxiliares",
            "predicción y explicación",
            "dependencia contrafáctica",
            "intervención",
            "triangulación",
            "u3",
        ):
            self.assertIn(phrase, objectives)

    def test_five_substantive_theory_sections(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        for section in sections:
            self.assertGreaterEqual(len(section["paragraphs"]), 6)
            self.assertGreaterEqual(len(section["key_points"]), 6)
            for point in section["key_points"]:
                self.assertGreaterEqual(len(point.split()), 5)
        headings = " ".join(x["heading"] for x in sections).casefold()
        for phrase in ("deducción", "hipótesis", "explicar", "causalidad", "evidencia biomédica plural"):
            self.assertIn(phrase, headings)

    def test_inference_section_distinguishes_three_forms(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "validez",
            "solidez",
            "modus ponens",
            "afirmación del consecuente",
            "problema clásico de la inducción",
            "abducción",
            "mejor explicación",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no garantiza que sea verdadera", text)

    def test_hypothesis_section_keeps_auxiliaries_visible(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "hipótesis científica",
            "supuestos auxiliares",
            "resultado nulo",
            "subdeterminación",
            "hipótesis → auxiliares → predicciones → observaciones → alternativas",
        ):
            self.assertIn(phrase, text)
        self.assertIn("la hipótesis fue probada", text)

    def test_explanation_section_separates_prediction_cause_and_mechanism(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "predicción y explicación",
            "deductivo-nomológico",
            "explicaciones estadísticas",
            "intervencionistas",
            "explicaciones mecanísticas",
            "componentes, actividades, organización",
        ):
            self.assertIn(phrase, text)
        self.assertIn("buen desempeño predictivo no demuestra una explicación causal", text)

    def test_causality_section_blocks_association_shortcuts(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "causa común",
            "x ← u → y",
            "contrafáctico",
            "intervención",
            "observar x=x no es necesariamente equivalente a imponer x=x",
            "ensayos aleatorizados",
            "causa probabilística",
        ):
            self.assertIn(phrase, text)
        self.assertIn("el diagrama codifica supuestos", text)

    def test_plural_evidence_section_requires_triangulation(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in (
            "evidencia mecanística",
            "triangulación",
            "fuentes de sesgo",
            "ninguna pieza aislada",
            "conclusión proporcional",
            "hipótesis rivales",
        ):
            self.assertIn(phrase, text)

    def test_glossary_examples_activity_and_assessment_are_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 45)
        for term in (
            "deducción", "inducción", "abducción", "supuesto auxiliar", "subdeterminación",
            "explicación mecanística", "confusión", "contrafáctico", "intervención", "dag", "triangulación",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 18)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)

    def test_sources_connections_and_editorial_boundaries(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 16)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no establezca una teoría filosófica única",
            "diagramas causales codifican supuestos",
            "no constituyen diagnóstico",
            "u3 abordará",
            "u4 desarrollará",
            "revisión disciplinar externa",
        ):
            self.assertIn(phrase, notice)

    def test_curricular_boundary_reserves_change_science_and_measurement(self) -> None:
        self.assertIn("reservando u3 para falsación", self.text)
        self.assertIn("u3 abordará falsación, kuhn, lakatos", self.text)
        self.assertIn("u4 desarrollará medición, clasificación y objetividad", self.text)


if __name__ == "__main__":
    unittest.main()
