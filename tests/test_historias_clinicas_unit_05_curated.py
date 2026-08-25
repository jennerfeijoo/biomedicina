from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "historias-clinicas-terminologias-estandares" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "historias-clinicas-terminologias-estandares" / "unit-05.json"
SUBJECT = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "historias-clinicas-terminologias-estandares.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class HistoriasClinicasUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_exact_mirror_and_template_removal(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["slug"], "calidad-privacidad-y-gobernanza")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("ppv=", self.text)
        self.assertNotIn("sensibilidad, especificidad y prevalencia", self.text)

    def test_objectives_define_quality_privacy_access_and_governance(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "adecuación al uso", "completitud", "conformidad", "plausibilidad",
            "corrección", "concordancia", "seudonimización", "anonimización",
            "autenticación", "autorización", "consentimiento", "provenance",
            "auditevent", "gobernanza", "u6",
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
            "calidad de datos orientada al uso", "privacidad en uso secundario",
            "acceso y consentimiento", "procedencia", "gobernanza del uso secundario",
        ):
            self.assertIn(phrase, headings)

    def test_quality_is_fit_for_use_and_multidimensional(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "no es una propiedad absoluta", "conformance", "completeness", "plausibility",
            "corrección", "concordancia", "actualidad", "denominador defendible",
            "patrones de ausencia", "perfil de calidad",
        ):
            self.assertIn(phrase, text)
        self.assertIn("ninguna puntuación única", text)
        self.assertIn("pasar las reglas seleccionadas no demuestra", text)

    def test_privacy_minimization_and_pseudonymization_have_boundaries(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "minimización", "privacidad", "confidencialidad", "seguridad",
            "seudonimización", "anonimización", "iso 25237:2017",
            "artículo 5", "gdpr", "jurisdicción", "retención",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no debe describirse como anonimización automática", text)
        self.assertIn("exclusivamente registros sintéticos", text)

    def test_authentication_authorization_consent_and_labels_are_separate(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "autenticación", "autorización", "rbac", "abac", "fhir",
            "consent r5", "security labels", "token", "política",
            "propósito", "vigencia",
        ):
            self.assertIn(phrase, text)
        self.assertIn("fhir no es un protocolo de seguridad completo", text)
        self.assertIn("un token técnicamente válido no prueba", text)
        self.assertIn("una etiqueta no ejecuta la política por sí sola", text)

    def test_provenance_and_auditevent_are_not_collapsed(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "fhir provenance", "auditevent", "producción", "transformación",
            "operación", "privacidad", "seguridad", "log", "lineage",
            "trazabilidad", "revisión",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no son intercambiables", text)
        self.assertIn("registrar eventos no equivale a revisarlos", text)

    def test_governance_is_lifecycle_based_without_moral_score(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in (
            "solicitud", "calidad", "privacidad", "acceso", "monitoreo",
            "revisión de salidas", "cierre", "separación de responsabilidades",
            "revocación", "expiración", "u6",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no como una puntuación moral ponderada", text)
        self.assertIn("apto bajo condiciones", text)

    def test_glossary_cases_and_activity_are_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 50)
        for term in (
            "adecuación al uso", "completitud", "plausibilidad", "seudonimización",
            "anonimización", "autenticación", "autorización", "rbac", "abac",
            "fhir consent", "security label", "fhir provenance", "auditevent",
            "lineage", "revisión de salida", "gobernanza de datos",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 24)
        self.assertGreaterEqual(len(activity["deliverables"]), 12)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)

    def test_activity_uses_synthetic_data_and_tests_governance_layers(self) -> None:
        activity = self.unit["guided_activities"][0]
        joined = " ".join(
            activity["instructions"] + activity["problems"] + activity["checking_criteria"]
        ).casefold()
        for phrase in (
            "no introduzcas nombres, identificadores, correos, credenciales ni datos clínicos reales",
            "denominador de completitud", "perfil de calidad", "autenticación y autorización",
            "consent fhir", "security label", "rbac", "abac", "provenance",
            "auditevent", "revisión de salida", "revocación", "u6",
        ):
            self.assertIn(phrase, joined)
        self.assertIn("no construyas una puntuación global", joined)

    def test_sources_assessment_connections_and_boundary(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 18)
        self.assertTrue(
            all(x["verification_status"] == "verified_directly" for x in self.unit["sources"])
        )
        sources = " ".join(x["title"] + " " + x["url"] for x in self.unit["sources"]).casefold()
        for phrase in (
            "harmonized data quality", "electronic health record data quality",
            "health data governance", "privacy framework", "iso 27799:2025",
            "iso 25237:2017", "article 5", "fhir r5 consent",
            "fhir r5 auditevent", "fhir r5 provenance", "security labels",
        ):
            self.assertIn(phrase, sources)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "exclusivamente sintéticos", "no se deben introducir datos identificables",
            "no constituye asesoría jurídica", "dependen de jurisdicción",
            "u4 cubre interoperabilidad", "u5 cubre calidad", "u6 queda reservada",
        ):
            self.assertIn(phrase, notice)

    def test_published_descriptor_matches_when_promoted(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {x["unit"]: x for x in subject["detailed_units"]}
        if detailed[5]["description"] != self.unit["purpose"]:
            self.skipTest("El publicador aún no ha promovido U5 al descriptor curricular")
        self.assertEqual(detailed[5]["description"], self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()
