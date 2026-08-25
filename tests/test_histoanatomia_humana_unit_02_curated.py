from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "histoanatomia-humana" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "histoanatomia-humana" / "unit-02.json"
SUBJECT = ROOT / "data" / "subjects" / "biologicas-medicas" / "histoanatomia-humana.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class HistoanatomiaHumanaUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["slug"], "tejidos-basicos")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn(r"v=\\frac{\\delta y}{\\delta t}", self.text)

    def test_objectives_cover_four_tissue_classes(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "epitelios de revestimiento",
            "tejido conectivo",
            "músculo esquelético, cardiaco y liso",
            "tejido nervioso",
            "rasgos positivos y negativos",
        ):
            self.assertIn(phrase, objectives)

    def test_five_substantive_theory_sections(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        for section in sections:
            self.assertGreaterEqual(len(section["paragraphs"]), 6)
            self.assertGreaterEqual(len(section["key_points"]), 6)
            for point in section["key_points"]:
                self.assertGreaterEqual(len(point.split()), 4)
        headings = " ".join(x["heading"] for x in sections).casefold()
        for phrase in ("reconocer un tejido", "tejido epitelial", "tejido conectivo", "tejido muscular", "tejido nervioso"):
            self.assertIn(phrase, headings)

    def test_epithelium_is_classified_by_architecture_not_color(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "polaridad apical-basal",
            "membrana basal",
            "simple significa",
            "estratificado",
            "seudoestratificado",
            "urothelio",
            "avascular",
        ):
            self.assertIn(phrase, text)
        errors = json.dumps(self.unit["common_errors"], ensure_ascii=False).casefold()
        self.assertIn("clasificar un epitelio por el color de h&e", errors)
        self.assertIn("contar filas de núcleos como capas epiteliales", errors)

    def test_connective_tissue_uses_matrix_and_processing_limits(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "matriz extracelular",
            "sustancia fundamental",
            "conectivo laxo",
            "conectivo denso regular",
            "conectivo denso irregular",
            "procesamiento histológico",
        ):
            self.assertIn(phrase, text)
        self.assertIn("una fibra rosada no debe identificarse automáticamente", text)

    def test_muscle_classification_respects_section_orientation(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "músculo esquelético",
            "músculo cardiaco",
            "músculo liso",
            "núcleos se sitúan típicamente en posición periférica",
            "discos intercalares",
            "corte transversal",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no ver estrías no permite concluir automáticamente músculo liso", text)

    def test_nervous_tissue_does_not_overclaim_region_or_glial_subtype(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in ("neuronas", "células gliales", "neuropilo", "sustancia gris", "sustancia blanca", "nervio periférico"):
            self.assertIn(phrase, text)
        self.assertIn("no localiza por sí sola una región", text)
        errors = json.dumps(self.unit["common_errors"], ensure_ascii=False).casefold()
        self.assertIn("tipar astrocitos, oligodendrocitos o microglía solo con h&e rutinaria", errors)

    def test_glossary_and_worked_examples_are_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 35)
        for term in (
            "epitelio",
            "polaridad apical-basal",
            "matriz extracelular",
            "conectivo denso regular",
            "músculo esquelético",
            "músculo cardiaco",
            "músculo liso",
            "neurona",
            "neuroglía",
            "neuropilo",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)

    def test_guided_activity_requires_differential_reasoning(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 240)
        self.assertGreaterEqual(len(activity["problems"]), 18)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 20)
        joined = " ".join(activity["instructions"] + activity["checking_criteria"]).casefold()
        for phrase in ("dos hipótesis", "rasgos positivos", "rasgo negativo", "no se formula diagnóstico clínico"):
            self.assertIn(phrase, joined)

    def test_sources_and_editorial_boundary(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 15)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no constituye entrenamiento diagnóstico",
            "informe anatomopatológico",
            "no establecen enfermedad",
            "material clínico",
        ):
            self.assertIn(phrase, notice)

    def test_u1_u2_u3_curricular_boundaries(self) -> None:
        self.assertIn("reutiliza la orientación, preparación y microscopía de u1", self.text)
        self.assertIn("u3 desarrollará con más detalle hueso, cartílago, tendón", self.text)
        self.assertIn("u6 desarrollará organización neuroanatómica", self.text)

    def test_published_descriptor_matches_canonical_purpose(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {x["unit"]: x for x in subject["detailed_units"]}
        self.assertEqual(detailed[2]["description"], self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()
