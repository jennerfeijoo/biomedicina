from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "historia-filosofia-ciencia" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "historia-filosofia-ciencia" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class HistoriaFilosofiaCienciaUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["slug"], "paradigmas-y-cambio-cientifico")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn(r"v(a)=\\sum", self.text)
        self.assertNotIn("modelo multicriterio transparente", self.text)

    def test_objectives_cover_popper_kuhn_lakatos_and_boundaries(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "falsabilidad",
            "corroboración",
            "matriz disciplinaria",
            "ciencia normal",
            "inconmensurabilidad",
            "núcleo duro",
            "cinturón protector",
            "progresivos o degenerativos",
            "normativas",
            "u4",
            "u5",
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
        for phrase in ("popper", "kuhn", "lakatos", "comparar", "controversias biomédicas"):
            self.assertIn(phrase, headings)

    def test_popper_section_blocks_instant_falsification_caricature(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "falsabilidad lógica",
            "falsificación efectiva",
            "pruebas exigentes",
            "corroboración",
            "hipótesis auxiliares",
            "no todo ajuste es ad hoc",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no significa que una teoría científica sea falsa", text)

    def test_kuhn_section_distinguishes_anomaly_crisis_and_revolution(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "matriz disciplinaria",
            "ejemplares",
            "ciencia normal",
            "anomalía",
            "crisis",
            "revolución científica",
            "inconmensurabilidad",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no toda anomalía produce crisis", text)
        self.assertIn("no significa que comunidades rivales sean incapaces de comunicarse", text)

    def test_lakatos_section_requires_sequences_and_novel_content(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "programas de investigación",
            "núcleo duro",
            "cinturón protector",
            "heurística negativa",
            "heurística positiva",
            "contenido empírico excedente",
            "progreso empírico",
            "degenerativa",
        ):
            self.assertIn(phrase, text)
        self.assertIn("requieren una ventana temporal", text)

    def test_comparison_section_keeps_units_and_normative_descriptive_layers_separate(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "unidades de análisis",
            "dimensión normativa",
            "descriptiva",
            "reconstruir instrumentos disponibles",
            "matriz comparativa",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no compiten como algoritmos equivalentes", text)

    def test_biomedical_cases_resist_heroic_and_paradigm_shortcuts(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in ("h. pylori", "priones", "semmelweis", "relato heroico", "escenario sintético"):
            self.assertIn(phrase, text)
        self.assertIn("no se convierte en revolución kuhniana solo por su originalidad posterior", text)

    def test_glossary_examples_activity_and_assessment_are_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 50)
        for term in (
            "falsabilidad", "corroboración", "matriz disciplinaria", "ciencia normal", "anomalía", "crisis",
            "revolución científica", "inconmensurabilidad", "programa de investigación", "núcleo duro",
            "cinturón protector", "heurística positiva", "programa progresivo", "programa degenerativo",
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
            "no establece que una anomalía aislada falsifique automáticamente",
            "todo descubrimiento importante sea una revolución kuhniana",
            "h. pylori",
            "priones",
            "u4 desarrollará",
            "u5 analizará",
            "revisión disciplinar externa",
        ):
            self.assertIn(phrase, notice)

    def test_curricular_boundary_reserves_measurement_and_power(self) -> None:
        self.assertIn("u4 desarrollará medición, clasificación y objetividad", self.text)
        self.assertIn("u5 analizará instituciones, colonialidad, género e industria", self.text)


if __name__ == "__main__":
    unittest.main()
