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
        self.assertEqual(self.unit["slug"], "interoperabilidad")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("ppv=", self.text)
        self.assertNotIn("sensibilidad, especificidad y prevalencia", self.text)

    def test_objectives_define_interoperability_layers(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "transporte", "hl7 v2", "fhir r5", "bundle",
            "structuredefinition", "declaración de capacidad", "v2→fhir",
            "parseo", "conformidad", "semántica", "api", "extremo a extremo",
            "u5", "u6",
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
            "contrato por capas", "hl7 v2", "fhir r5",
            "perfiles fhir", "transformación v2→fhir",
        ):
            self.assertIn(phrase, headings)

    def test_hl7_v2_is_event_message_segment_and_ack_aware(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "eventos disparadores", "tipo de mensaje", "msh", "pid", "orc", "obr", "obx",
            "oru^r01", "ack", "message control id", "opcionalidad", "ausencia",
            "2.9.1", "perfiles de mensaje",
        ):
            self.assertIn(phrase, text)
        self.assertIn("un ack positivo no demuestra", text)

    def test_fhir_r5_distinguishes_resources_api_search_and_bundle_semantics(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "patient", "observation", "diagnosticreport", "servicerequest", "specimen",
            "identificadores de negocio", "referencias", "api rest", "parámetros",
            "capabilitystatement", "batch", "transaction", "atómico",
            "operationoutcome", "5.0.0",
        ):
            self.assertIn(phrase, text)

    def test_profiles_and_validation_are_not_collapsed_into_operational_conformance(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "structuredefinition", "cardinalidades", "invariantes", "extensiones",
            "bindings", "valuesets", "implementationguide", "capabilitystatement",
            "$validate", "validación estática", "reglas de negocio",
            "flujo interoperable",
        ):
            self.assertIn(phrase, text)
        self.assertGreaterEqual(text.count("no es evidencia suficiente"), 2)

    def test_mapping_and_authorization_have_explicit_boundaries(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in (
            "no consiste en sustituir un segmento", "pérdida semántica",
            "pid puede aportar", "obr puede contribuir", "obx suele aportar",
            "smart app launch 2.2.0", "fhir r4", "autorización",
            "token válido", "extremo a extremo", "u5", "u6",
        ):
            self.assertIn(phrase, text)
        self.assertIn("autorización y conformidad del contenido", text)

    def test_glossary_cases_and_activity_are_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 50)
        for term in (
            "hl7 v2", "msh", "pid", "obr", "obx", "ack", "fhir r5",
            "structuredefinition", "capabilitystatement", "operationoutcome",
            "batch", "transaction", "binding", "implementationguide",
            "mapeo v2→fhir", "smart app launch", "prueba extremo a extremo",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 24)
        self.assertGreaterEqual(len(activity["deliverables"]), 12)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)

    def test_activity_tests_layers_and_rejects_real_data(self) -> None:
        activity = self.unit["guided_activities"][0]
        joined = " ".join(
            activity["instructions"] + activity["problems"] + activity["checking_criteria"]
        ).casefold()
        for phrase in (
            "no introduzcas nombres, identificadores, credenciales",
            "oru^r01", "message control id", "capabilitystatement",
            "operationoutcome", "casos positivos y negativos",
            "batch", "transaction", "smart app launch 2.2.0",
            "sintaxis, perfil, semántica, api y extremo a extremo",
            "u5", "u6",
        ):
            self.assertIn(phrase, joined)

    def test_sources_assessment_connections_and_boundary(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 18)
        self.assertTrue(
            all(x["verification_status"] == "verified_directly" for x in self.unit["sources"])
        )
        sources = " ".join(x["title"] + " " + x["url"] for x in self.unit["sources"]).casefold()
        for phrase in (
            "hl7 fhir r5", "validating resources", "structuredefinition",
            "capabilitystatement", "smart app launch 2.2.0",
            "hl7 version 2.9.1", "hl7 v2.9 chapter 2", "hl7 v2.9 chapter 7",
        ):
            self.assertIn(phrase, sources)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "exclusivamente sintéticos", "no constituye diseño, certificación ni validación",
            "no se deben introducir datos identificables", "u4 cubre interoperabilidad",
            "u5 queda reservada", "u6 para implementación",
        ):
            self.assertIn(phrase, notice)

    def test_published_descriptor_matches_canonical_purpose(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {x["unit"]: x for x in subject["detailed_units"]}
        self.assertEqual(detailed[4]["description"], self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()
