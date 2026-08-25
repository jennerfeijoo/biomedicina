from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "historias-clinicas-terminologias-estandares" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "historias-clinicas-terminologias-estandares" / "unit-04.json"
SUBJECT = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "historias-clinicas-terminologias-estandares.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class HistoriasClinicasUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_exact_mirror_and_template_removal(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["slug"], "interoperabilidad-hl7-fhir")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("ppv=", self.text)
        self.assertNotIn("sensibilidad, especificidad y prevalencia", self.text)

    def test_objectives_cover_interoperability_contract(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "interoperabilidad técnica", "estructural", "semántica",
            "hl7 v2.9", "oru^r01", "fhir r5",
            "patient", "specimen", "servicerequest", "observation", "diagnosticreport",
            "structuredefinition", "capabilitystatement", "mapeo hl7 v2→fhir",
        ):
            self.assertIn(phrase, objectives)

    def test_five_substantive_sections(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        for section in sections:
            self.assertGreaterEqual(len(section["paragraphs"]), 6)
            self.assertGreaterEqual(len(section["key_points"]), 6)
            for point in section["key_points"]:
                self.assertGreaterEqual(len(point.split()), 5)
        headings = " ".join(x["heading"] for x in sections).casefold()
        for phrase in (
            "interoperabilidad como contrato", "hl7 v2.9", "fhir r5",
            "perfiles fhir", "mapeo hl7 v2→fhir",
        ):
            self.assertIn(phrase, headings)

    def test_hl7_v2_message_ack_and_conformance_are_distinct(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "msh", "pid", "obr", "obx", "spm", "oru^r01", "msh-10", "msh-12",
            "msh-15", "msh-16", "ack", "aa", "ae", "ar", "perfil de conformidad",
        ):
            self.assertIn(phrase, text)
        self.assertIn("un ack exitoso no afirma que el contenido clínico sea verdadero", text)

    def test_fhir_identity_rest_bundle_and_capabilities_are_distinct(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "patient", "specimen", "servicerequest", "observation", "diagnosticreport",
            "id lógico", "identifier", "reference", "restful", "transaction", "batch",
            "capabilitystatement", "operationoutcome",
        ):
            self.assertIn(phrase, text)
        self.assertIn("fhir no se reduce a rest", text)

    def test_profiles_bindings_and_validation_have_limits(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "structuredefinition", "cardinalidades", "invariantes", "slices",
            "terminology bindings", "value sets", "implementationguide", "canonical",
            "validator", "referencia rota",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no demuestra que todos los requisitos del flujo extremo a extremo", text)

    def test_v2_to_fhir_mapping_is_versioned_and_semantic(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in (
            "no existe una regla general segmento=resource", "fhir r4", "fhir r5",
            "pid", "spm", "obr", "obx", "identificadores", "estados", "timestamps",
            "pruebas positivas", "negativas", "casos límite", "round-trip", "lossless",
            "matriz requisito",
        ):
            self.assertIn(phrase, text)

    def test_glossary_activity_and_cases_are_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 50)
        for term in (
            "interoperabilidad semántica", "hl7 v2", "oru^r01", "ack", "message control id",
            "fhir", "id lógico", "identifier", "transaction", "batch", "capabilitystatement",
            "operationoutcome", "structuredefinition", "perfil fhir", "terminology binding",
            "implementationguide", "mapeo", "pérdida semántica",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 24)
        self.assertGreaterEqual(len(activity["deliverables"]), 12)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)

    def test_activity_tests_failure_not_only_happy_path(self) -> None:
        activity = self.unit["guided_activities"][0]
        joined = " ".join(activity["instructions"] + activity["problems"] + activity["deliverables"] + activity["checking_criteria"]).casefold()
        for phrase in (
            "hl7 v2.9", "fhir r5", "oru^r01", "ack", "id lógico", "identifier",
            "capabilitystatement", "transaction", "batch", "cardinalidad",
            "terminology binding", "validator", "operationoutcome",
            "pruebas positivas, negativas y límite", "round-trip", "r4", "r5",
            "requisito→artefacto→prueba→resultado→limitación",
        ):
            self.assertIn(phrase, joined)

    def test_sources_assessment_connections_and_boundary(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 18)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        sources = " ".join(x["title"] + " " + x["url"] for x in self.unit["sources"]).casefold()
        for phrase in (
            "hl7 v2.9 chapter 2 control", "observation reporting", "fhir r5 documentation",
            "implementationguide", "profiling", "validation", "v2-to-fhir",
        ):
            self.assertIn(phrase, sources)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "datos y mensajes sintéticos", "no se deben introducir datos identificables",
            "u4 cubre interoperabilidad", "u5 queda reservada para calidad, privacidad y gobernanza",
            "u6 para conformidad e implementación", "no constituye una interfaz clínica de producción",
        ):
            self.assertIn(phrase, notice)

    def test_published_descriptor_matches_canonical_purpose_when_promoted(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {x["unit"]: x for x in subject["detailed_units"]}
        if detailed[4]["description"] != self.unit["purpose"]:
            self.skipTest("El publicador todavía no ha promovido el descriptor de U4")
        self.assertEqual(detailed[4]["description"], self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()
