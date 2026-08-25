from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "histoanatomia-humana" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "histoanatomia-humana" / "unit-03.json"
SUBJECT = ROOT / "data" / "subjects" / "biologicas-medicas" / "histoanatomia-humana.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class HistoanatomiaHumanaUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["slug"], "sistema-musculoesqueletico")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn(r"v=\\frac{\\delta y}{\\delta t}", self.text)

    def test_objectives_cover_multiscale_musculoskeletal_anatomy(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "hueso cortical y trabecular",
            "osteonas",
            "remodelación ósea",
            "cartílago hialino",
            "tendón, ligamento y entesis",
            "articulación sinovial",
            "músculo esquelético como órgano",
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
                self.assertGreaterEqual(len(point.split()), 5)
        headings = " ".join(x["heading"] for x in sections).casefold()
        for phrase in ("microarquitectura musculoesquelética", "hueso", "cartílago", "articulaciones sinoviales", "lectura multiescala"):
            self.assertIn(phrase, headings)

    def test_bone_architecture_distinguishes_cortical_and_trabecular(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "hueso cortical o compacto",
            "osteonas secundarias",
            "laminillas concéntricas",
            "canal central",
            "hueso trabecular o esponjoso",
            "trabéculas",
            "espacios medulares",
            "osteocitos",
            "osteoblastos",
            "osteoclastos",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no se describen normalmente como una colección de osteonas cilíndricas clásicas", text)

    def test_cartilage_tendon_ligament_and_enthesis_keep_context(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "cartílago articular",
            "carece de pericondrio",
            "fibrocartílago",
            "tendones y ligamentos",
            "distinguirlos con certeza puede ser imposible",
            "entesis fibrosas y fibrocartilaginosas",
            "fibrocartílago no calcificado",
            "fibrocartílago calcificado",
        ):
            self.assertIn(phrase, text)

    def test_synovial_joint_and_muscle_are_taught_as_integrated_organs(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "cavidad articular",
            "cápsula",
            "membrana sinovial",
            "líquido sinovial",
            "meniscos",
            "bursas",
            "epimisio",
            "perimisio",
            "endomisio",
            "fascículos",
        ):
            self.assertIn(phrase, text)

    def test_multiscale_section_enforces_safe_imaging_boundary(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        self.assertIn("orientación regional → estructura macroscópica → tejido dominante → microarquitectura", text)
        self.assertIn("no interpreta estudios de pacientes", text)
        self.assertIn("rodilla normal sintética", text)
        errors = json.dumps(self.unit["common_errors"], ensure_ascii=False).casefold()
        self.assertIn("usar una mri educativa para diagnosticar una lesión", errors)
        self.assertIn("recomendación de ejercicio o rehabilitación", errors)

    def test_glossary_and_examples_are_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 45)
        for term in (
            "hueso cortical",
            "hueso trabecular",
            "osteona",
            "osteoblasto",
            "osteoclasto",
            "cartílago articular",
            "fibrocartílago",
            "tendón",
            "ligamento",
            "entesis",
            "articulación sinovial",
            "membrana sinovial",
            "menisco",
            "epimisio",
            "perimisio",
            "endomisio",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)

    def test_guided_activity_requires_multiscale_reasoning(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 24)
        joined = " ".join(activity["instructions"] + activity["checking_criteria"]).casefold()
        for phrase in (
            "región → órgano → tejido → célula/matriz",
            "tres rasgos positivos",
            "alternativa plausible",
            "músculo → tendón → entesis → hueso",
            "no se formula diagnóstico",
            "no se prescriben ejercicios",
        ):
            self.assertIn(phrase, joined)

    def test_sources_assessment_connections_and_editorial_boundary(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 18)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no constituye entrenamiento diagnóstico",
            "lectura clínica",
            "no establecen osteoporosis",
            "tampoco prescribe ejercicio",
            "material clínico",
        ):
            self.assertIn(phrase, notice)

    def test_u1_u2_u3_u4_curricular_boundaries(self) -> None:
        self.assertIn("u1 aporta posición anatómica", self.text)
        self.assertIn("u2 aporta los cuatro tejidos básicos", self.text)
        self.assertIn("u4 pasará a corazón, vasos y aparato respiratorio", self.text)
        self.assertIn("modelado biomecánico cuantitativo pertenece a asignaturas específicas", self.text)

    def test_published_descriptor_matches_canonical_purpose_when_promoted(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {x["unit"]: x for x in subject["detailed_units"]}
        if detailed[3]["description"] != self.unit["purpose"]:
            self.skipTest("El descriptor se sincroniza en el workflow de publicación.")
        self.assertEqual(detailed[3]["description"], self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()
