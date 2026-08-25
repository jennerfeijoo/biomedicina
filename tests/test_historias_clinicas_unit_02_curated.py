from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "historias-clinicas-terminologias-estandares" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "historias-clinicas-terminologias-estandares" / "unit-02.json"
SUBJECT = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "historias-clinicas-terminologias-estandares.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class HistoriasClinicasUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_template_and_ppv_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["slug"], "modelos-de-informacion")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("ppv=", self.text)
        self.assertNotIn("sensibilidad, especificidad y prevalencia", self.text)

    def test_objectives_cover_information_model_layers(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "modelo conceptual",
            "modelo lógico",
            "modelo de referencia",
            "serialización",
            "tipo de dato",
            "cardinalidad",
            "contexto",
            "identificadores de negocio",
            "referencias",
            "versiones",
            "procedencia",
            "arquetipos",
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
        for phrase in (
            "capas del modelo",
            "tipos, cardinalidad y ausencia",
            "contexto y relaciones",
            "identidad, referencias, versiones y procedencia",
            "restricciones, arquetipos y contratos de datos",
        ):
            self.assertIn(phrase, headings)

    def test_reference_model_is_not_serialization_or_physical_storage(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "modelo conceptual",
            "modelo lógico",
            "modelo físico",
            "modelo de referencia",
            "la instancia",
            "la serialización",
            "validar una instancia contra un esquema solo demuestra",
            "dos niveles",
        ):
            self.assertIn(phrase, text)
        self.assertIn("u4", text)

    def test_structure_preserves_types_cardinality_and_missingness(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "tipo de dato",
            "cardinalidad",
            "0..1",
            "1..1",
            "0..*",
            "dato faltante",
            "negación explícita",
            "desconocido",
            "no aplicable",
            "unidades",
            "estructuralmente válida",
        ):
            self.assertIn(phrase, text)

    def test_context_and_relationships_are_explicit(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "sujeto",
            "encuentro",
            "tiempo",
            "autor",
            "embebido y referenciado",
            "dirección y semántica",
            "ruta",
            "u4",
        ):
            self.assertIn(phrase, text)

    def test_identifier_version_and_provenance_are_not_collapsed(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "identificador de negocio",
            "identificador técnico",
            "sistema emisor",
            "referencia",
            "la identidad persiste mientras las versiones cambian",
            "versionid",
            "versioned_object",
            "procedencia",
            "mapa origen→destino",
        ):
            self.assertIn(phrase, text)
        self.assertIn("u5", text)

    def test_constraints_do_not_claim_semantic_interoperability(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in (
            "structuredefinition",
            "arquetipos",
            "iso 13606-2:2019",
            "mayor restricción no siempre significa mayor interoperabilidad",
            "contrato de datos",
            "pérdidas estructurales",
            "pérdidas de contexto",
            "pérdidas de identidad",
            "pérdidas semánticas",
            "u3",
            "u6",
        ):
            self.assertIn(phrase, text)

    def test_glossary_examples_activity_and_controls_are_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 45)
        for term in (
            "modelo de información",
            "modelo de referencia",
            "serialización",
            "cardinalidad",
            "dato faltante",
            "identificador de negocio",
            "identificador técnico",
            "integridad referencial",
            "versionado",
            "procedencia",
            "arquetipo",
            "contrato de datos",
            "equivalencia semántica",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 24)
        self.assertGreaterEqual(len(activity["deliverables"]), 12)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)

    def test_activity_blocks_common_false_equivalences(self) -> None:
        activity = self.unit["guided_activities"][0]
        joined = " ".join(activity["instructions"] + activity["checking_criteria"] + activity["problems"]).casefold()
        for phrase in (
            "modelo conceptual",
            "modelo lógico",
            "dato faltante",
            "identificadores de negocio",
            "identificador técnico",
            "coincidencia de cadenas",
            "identidad de una entidad",
            "control negativo",
            "equivalencia semántica",
            "json válido",
            "u3",
            "u6",
        ):
            self.assertIn(phrase, joined)

    def test_sources_assessment_connections_and_safety_boundary(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 18)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "datos sintéticos",
            "no constituye diseño de una hce productiva",
            "no asigna terminologías clínicas",
            "no se deben introducir datos identificables",
            "u3–u6",
        ):
            self.assertIn(phrase, notice)

    def test_published_descriptor_matches_canonical_purpose(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {x["unit"]: x for x in subject["detailed_units"]}
        self.assertEqual(detailed[2]["description"], self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()
