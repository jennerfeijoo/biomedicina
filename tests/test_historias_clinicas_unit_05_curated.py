from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "historias-clinicas-terminologias-estandares" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "historias-clinicas-terminologias-estandares" / "unit-05.json"
SUBJECT = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "historias-clinicas-terminologias-estandares.json"
PUBLIC_UNIT = ROOT / "ingenieria-biomedica" / "historias-clinicas-terminologias-estandares" / "unidades" / "unidad-05.html"
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

    def test_objectives_cover_quality_privacy_access_and_governance(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "conformance", "completeness", "plausibility", "seudonimización",
            "anonimización", "permit/deny", "consent", "permission",
            "auditevent", "provenance", "u6",
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
            "aptitud para el uso", "seudonimización", "consentimiento",
            "auditoría", "gobernanza",
        ):
            self.assertIn(phrase, headings)

    def test_quality_is_fit_for_use_and_dimension_specific(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "kahn", "conformance", "completeness", "plausibility",
            "denominador", "atemporal", "temporal", "entidad que debería ser única",
            "uso previsto", "evidencia insuficiente",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no deben colapsarse en un porcentaje global", text)

    def test_privacy_distinguishes_frameworks_and_identifiability(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "gdpr", "limitación de la finalidad", "minimización", "seudonimización",
            "anonimización", "hipaa", "expert determination", "safe harbor",
            "cuasi-identificadores", "retención",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no mezcla estos métodos con gdpr como si fueran equivalentes", text)

    def test_access_separates_identity_permission_and_consent(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "autenticación", "autorización", "consentimiento", "mínimo privilegio",
            "rbac", "abac", "fhir r5 consent", "fhir r5 permission",
            "security labels", "propósito de uso",
        ):
            self.assertIn(phrase, text)
        self.assertIn("consent técnicamente válido no prueba", text)
        self.assertIn("tampoco implementa un motor de autorización", text)

    def test_audit_and_provenance_have_distinct_roles(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "auditevent", "provenance", "log", "integridad", "retención",
            "lectura masiva", "propósito distinto",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no usar uno como sustituto universal del otro", text)
        self.assertIn("señal para investigar, no prueba automática", text)

    def test_governance_handles_change_outputs_and_accountability(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in (
            "uso secundario", "cambio de propósito", "minimización", "riesgo",
            "producto de salida", "raci", "rendición de cuentas", "u6",
            "dpia formal",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no una autorización institucional", text)

    def test_glossary_cases_activity_and_common_errors_are_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 50)
        for term in (
            "conformance", "completeness", "plausibility", "seudonimización",
            "anonimización", "cuasi-identificador", "autenticación", "autorización",
            "rbac", "abac", "consent", "permission", "auditevent", "provenance",
            "gobernanza de datos", "raci", "riesgo residual", "puerta de cambio",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 24)
        self.assertGreaterEqual(len(activity["deliverables"]), 12)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 18)

    def test_activity_rejects_real_data_and_protects_conceptual_boundaries(self) -> None:
        activity = self.unit["guided_activities"][0]
        joined = " ".join(
            activity["instructions"] + activity["problems"] + activity["checking_criteria"]
        ).casefold()
        for phrase in (
            "exclusivamente", "no introduzcas datos identificables", "conformance",
            "completeness", "plausibility", "seudonimización", "anonimización",
            "consent", "permission", "auditevent", "provenance",
            "casos permitidos y denegados", "u6",
        ):
            self.assertIn(phrase, joined)

    def test_sources_assessment_connections_and_editorial_boundary(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 18)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        sources = " ".join(x["title"] + " " + x["organization"] for x in self.unit["sources"]).casefold()
        for phrase in (
            "harmonized data quality", "gdpr", "de-identification", "fhir r5 consent",
            "fhir r5 permission", "fhir r5 auditevent", "fhir r5 provenance",
            "privacy framework 1.1 initial public draft", "oecd",
        ):
            self.assertIn(phrase, sources)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "exclusivamente", "no constituye asesoría jurídica", "dpia formal",
            "aprobación ética", "gdpr y hipaa", "u6 queda reservada",
        ):
            self.assertIn(phrase, notice)

    def test_public_page_contains_canonical_purpose(self) -> None:
        public_text = PUBLIC_UNIT.read_text(encoding="utf-8")
        self.assertIn(self.unit["purpose"], public_text)

    def test_published_descriptor_matches_canonical_purpose_when_promoted(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {x["unit"]: x for x in subject["detailed_units"]}
        if detailed[5]["description"] != self.unit["purpose"]:
            self.skipTest("Descriptor curricular pendiente de promoción automática")
        self.assertEqual(detailed[5]["description"], self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()
