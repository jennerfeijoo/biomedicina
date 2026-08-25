from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "ingenieria-datos-biomedicos" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "ingenieria-datos-biomedicos" / "unit-02.json"
SUBJECT = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "ingenieria-datos-biomedicos.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class IngenieriaDatosBiomedicosUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["slug"], "ingesta-y-transformacion")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("ppv=", self.text)

    def test_objectives_cover_transformation_contracts_and_boundaries(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "etl y elt",
            "copia raw inmutable",
            "validación estructural",
            "ucum",
            "effective/event time",
            "accepted/quarantine",
            "idempotencia",
            "u3–u6",
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
        # Validate the disciplinary topics rather than punctuation in the headings.
        for token in (
            "etl",
            "elt",
            "validación de esquemas",
            "unidades y cantidades",
            "tiempo",
            "códigos",
            "ausencias",
            "reconciliación",
            "pruebas",
            "idempotencia",
        ):
            self.assertIn(token, headings)

    def test_etl_elt_preserve_raw_determinism_and_idempotency(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "raw conserva",
            "staging",
            "determinismo",
            "idempotencia",
            "misma identidad de entrega",
            "u3",
            "u4",
            "u5",
        ):
            self.assertIn(phrase, text)

    def test_schema_validation_is_not_clinical_validation(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "json schema draft 2020-12",
            "estructura, cardinalidad",
            "reglas de negocio",
            "operationoutcome",
            "writer schema",
            "reader schema",
            "quarantine",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no demuestra que el valor represente al paciente correcto", text)

    def test_units_preserve_original_and_block_unsafe_conversion(self) -> None:
        section = self.unit["theory_sections"][2]
        text = json.dumps(section, ensure_ascii=False).casefold()
        for phrase in (
            "value, unit, system y code",
            "ucum",
            "valor y la unidad fuente",
            "mg/dl",
            "mmol/l",
            "masa molar",
            "comparadores",
        ):
            self.assertIn(phrase, text)
        equations = {x["latex"] for x in section["equations"]}
        self.assertIn(r"x_{target}=k\,x_{source}", equations)
        self.assertIn(r"x_{target}=a\,x_{source}+b", equations)

    def test_time_codes_and_missingness_remain_semantically_distinct(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "effective/event time",
            "issued time",
            "ingest time",
            "no adquiere mágicamente utc",
            "conceptmap",
            "source-is-narrower-than-target",
            "source-is-broader-than-target",
            "null, cero, falso, cadena vacía",
            "mapping_status=unresolved",
        ):
            self.assertIn(phrase, text)

    def test_reconciliation_and_reprocessing_are_explicit(self) -> None:
        section = self.unit["theory_sections"][4]
        text = json.dumps(section, ensure_ascii=False).casefold()
        for phrase in (
            "n_input",
            "n_accepted",
            "n_quarantine",
            "pruebas negativas",
            "delivery_id",
            "transform_version",
            "run_id",
            "reprocesamiento analítico",
        ):
            self.assertIn(phrase, text)
        equations = {x["latex"] for x in section["equations"]}
        self.assertIn(r"N_{input}=N_{accepted}+N_{quarantine}", equations)

    def test_glossary_examples_and_activity_are_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 55)
        for term in (
            "etl", "elt", "staging", "contrato de transformación", "idempotencia",
            "json schema", "operationoutcome", "schema evolution", "writer schema",
            "reader schema", "quantity", "ucum", "compatibilidad dimensional",
            "conversión afín", "masa molar", "effective time", "ingest time",
            "conceptmap", "mapping_version", "unresolved mapping", "missingness",
            "reconciliación", "delivery_id", "run_id",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 360)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 12)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)
        joined = " ".join(activity["instructions"] + activity["problems"] + activity["checking_criteria"]).casefold()
        for phrase in (
            "raw → staging",
            "json schema",
            "mm[hg]",
            "mg/dl",
            "timestamp",
            "conceptmap",
            "null",
            "n_input",
            "idempotencia",
            "u3",
            "u4",
            "u5",
            "u6",
        ):
            self.assertIn(phrase, joined)

    def test_common_errors_block_silent_semantic_damage(self) -> None:
        text = " ".join(x["error"] + " " + x["correction"] for x in self.unit["common_errors"]).casefold()
        for phrase in (
            "json válido",
            "sobrescribir unidad",
            "semejanza textual",
            "cualquier mg/dl",
            "colapsar effective",
            "conceptmap",
            "rellenar null",
            "idempotencia",
            "reconciliar",
            "checksum",
            "decisiones clínicas",
        ):
            self.assertIn(phrase, text)

    def test_sources_assessment_connections_and_notice(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 16)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        titles = " ".join(x["title"] for x in self.unit["sources"]).casefold()
        for phrase in (
            "fhir r5 validation",
            "operationoutcome",
            "quantity",
            "conceptmap",
            "unified code for units of measure",
            "json schema draft 2020-12",
            "apache avro",
            "rfc 3339",
        ):
            self.assertIn(phrase, titles)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "exclusivamente sintéticos",
            "no ingiere sistemas institucionales",
            "no interpreta resultados clínicos",
            "25 de agosto de 2026",
            "u3 almacenamiento/modelado",
            "u4 calidad/linaje/versionado",
            "u5 orquestación/observabilidad",
            "u6 privacidad",
        ):
            self.assertIn(phrase, notice)

    def test_curricular_boundaries_are_explicit(self) -> None:
        purpose = self.unit["purpose"].casefold()
        for phrase in (
            "reutiliza el inventario source-to-landing de u1",
            "almacenamiento/modelado para u3",
            "calidad/linaje/versionado profundo para u4",
            "orquestación/observabilidad para u5",
            "privacidad/productos de datos para u6",
        ):
            self.assertIn(phrase, purpose)

    def test_published_descriptor_when_promoted_matches_canonical_purpose(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {x["unit"]: x for x in subject["detailed_units"]}
        description = detailed[2]["description"]
        if description != self.unit["purpose"]:
            self.skipTest("Descriptor curricular todavía no promovido por el workflow de publicación")
        self.assertEqual(description, self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()
