from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "informatica-biomedica" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "informatica-biomedica" / "unit-01.json"
SUBJECT = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "informatica-biomedica.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class InformaticaBiomedicaUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["slug"], "datos-informacion-y-conocimiento-en-salud")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("ppv=", self.text)

    def test_objectives_cover_semantics_lifecycle_provenance_and_quality(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "dato, información y conocimiento",
            "estructura, escala de medición",
            "ciclo de vida de datos",
            "entidades, actividades y agentes",
            "conformance, completeness, plausibility",
            "grafo de procedencia",
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
        for phrase in ("datos a información", "tipos y representaciones", "ciclo de vida", "metadatos y procedencia", "calidad dependiente"):
            self.assertIn(phrase, headings)

    def test_data_information_knowledge_is_not_an_automatic_ladder(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "no aparece automáticamente",
            "no debe tratarse como una ley universal",
            "el flujo es iterativo",
            "unidad, tiempo, método, fuente",
        ):
            self.assertIn(phrase, text)

    def test_data_types_units_time_identifiers_and_missingness_are_separated(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "estructurado",
            "semiestructurado",
            "no estructurado",
            "nominales",
            "ordinales",
            "unidad",
            "tiempo del evento",
            "tiempo de disponibilidad",
            "identificadores no son atributos clínicos",
            "no medido",
            "no aplicable",
            "desconocido",
        ):
            self.assertIn(phrase, text)

    def test_lifecycle_preserves_versions_and_derived_lineage(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "ciclo de vida",
            "grafo de estados y actividades",
            "entrada, salida, regla o código aplicado",
            "versionar",
            "dato derivado",
            "no sustituye las observaciones originales",
            "reproducibilidad",
        ):
            self.assertIn(phrase, text)

    def test_provenance_uses_entity_activity_agent_without_claiming_truth(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "entity, activity y agent",
            "procedencia no es sinónimo de auditoría",
            "tampoco demuestra calidad o verdad",
            "fair",
            "no como una certificación",
            "grafo de procedencia",
        ):
            self.assertIn(phrase, text)

    def test_quality_is_use_dependent_and_denominators_are_explicit(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in (
            "conformance",
            "completeness",
            "plausibility",
            "concordance",
            "correctness",
            "currency",
            "denominador defendible",
            "no debe renombrarse plausibilidad como",
        ):
            self.assertIn(phrase, text)
        equations = {x["latex"] for x in self.unit["theory_sections"][4]["equations"]}
        self.assertIn(r"C=\frac{N_{presentes}}{N_{esperados}}", equations)
        self.assertIn(r"\Delta t=t_{disponible}-t_{evento}", equations)

    def test_glossary_examples_and_activity_are_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 50)
        for term in (
            "dato", "información", "conocimiento", "metadatos", "ciclo de vida de datos",
            "dato derivado", "procedencia", "entidad de procedencia", "actividad de procedencia",
            "agente de procedencia", "linaje de datos", "trazabilidad", "conformance",
            "completeness", "plausibility", "concordance", "correctness", "currency",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)

        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 12)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)
        joined = " ".join(activity["instructions"] + activity["checking_criteria"]).casefold()
        for phrase in (
            "exclusivamente con el conjunto sintético",
            "entidades, actividades y agentes",
            "n_esperados",
            "conformance",
            "plausibility",
            "no se usan datos identificables",
            "u2, u3, u4, u5 y u6",
        ):
            self.assertIn(phrase, joined)

    def test_sources_assessment_connections_and_editorial_boundary(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 18)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "datos, identificadores, metadatos y transformaciones sintéticos",
            "no constituye documentación clínica",
            "no se deben introducir datos identificables",
            "puede seguir siendo incorrecto",
            "u3",
        ):
            self.assertIn(phrase, notice)

    def test_curricular_boundaries_keep_later_units_out_of_scope(self) -> None:
        purpose = self.unit["purpose"].casefold()
        for phrase in (
            "sistemas clínicos de u2",
            "interoperabilidad y terminologías de u3",
            "analítica de u4",
            "factores humanos de u5",
            "gobernanza e implementación de u6",
        ):
            self.assertIn(phrase, purpose)

    def test_published_descriptor_matches_canonical_purpose(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {x["unit"]: x for x in subject["detailed_units"]}
        self.assertEqual(detailed[1]["description"], self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()
