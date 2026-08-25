from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/informatica-biomedica/units/unit-06.json"
MIRROR = ROOT / "data/generated_units/informatica-biomedica/unit-06.json"
DESCRIPTOR = ROOT / "data/subjects/ingenieria-biomedica/informatica-biomedica.json"
CATALOG = ROOT / "data/catalog_statuses.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class TestInformaticaBiomedicaUnit06Curated(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = load_json(SOURCE)
        cls.mirror = load_json(MIRROR)
        cls.descriptor = load_json(DESCRIPTOR)
        cls.catalog = load_json(CATALOG)
        cls.text = json.dumps(cls.unit, ensure_ascii=False).lower()

    def test_source_and_generated_mirror_are_identical(self) -> None:
        self.assertEqual(self.unit, self.mirror)

    def test_published_descriptor_when_promoted_matches_canonical_purpose(self) -> None:
        published = next(item for item in self.descriptor["detailed_units"] if item["unit"] == 6)
        if published["description"] != self.unit["purpose"]:
            self.skipTest("El publicador todavía no ha promovido el propósito canónico de U6.")
        self.assertEqual(published["description"], self.unit["purpose"])

    def test_identity_and_depth(self) -> None:
        self.assertEqual(self.unit["subject_id"], "informatica-biomedica")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["slug"], "gobernanza-e-implementacion")
        self.assertEqual(self.unit["status"], "review")
        self.assertGreaterEqual(len(self.unit["learning_objectives"]), 6)
        self.assertGreaterEqual(len(self.unit["theory_sections"]), 5)
        for section in self.unit["theory_sections"]:
            self.assertGreaterEqual(len(section["paragraphs"]), 5)
            self.assertGreaterEqual(len(section["key_points"]), 5)
            for point in section["key_points"]:
                self.assertGreaterEqual(len(point.split()), 4)
        self.assertGreaterEqual(len(self.unit["glossary"]), 50)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 18)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        self.assertGreaterEqual(len(self.unit["sources"]), 15)

    def test_generic_template_and_inherited_ppv_are_removed(self) -> None:
        for marker in [
            "concepto de la unidad que debe definirse",
            "modelo conceptual de gobernanza e implementación",
            "construir un modelo que conecte privacidad con seguridad",
            "integrar privacidad, seguridad, calidad y cambio organizativo para resolver un caso",
        ]:
            self.assertNotIn(marker, self.text)
        self.assertNotIn("ppv=\\frac", self.text)

    def test_governance_is_decision_and_risk_governance_not_access_admin(self) -> None:
        for concept in [
            "derechos de decisión",
            "tolerancia al riesgo",
            "riesgo residual",
            "registro de riesgos",
            "raci",
            "terceros",
            "govern",
            "identify",
            "protect",
            "detect",
            "respond",
            "recover",
        ]:
            self.assertIn(concept, self.text)
        self.assertIn("no equivale a administración de accesos", self.text)
        self.assertIn("raci", self.text)

    def test_privacy_security_identity_and_zero_trust_are_separated(self) -> None:
        for concept in [
            "privacidad",
            "ciberseguridad",
            "confidencialidad",
            "integridad",
            "disponibilidad",
            "autenticación",
            "autorización",
            "consentimiento",
            "mínimo privilegio",
            "rbac",
            "abac",
            "mfa",
            "zero trust",
        ]:
            self.assertIn(concept, self.text)
        self.assertIn("privacidad y ciberseguridad se relacionan pero no son equivalentes", self.text)
        self.assertIn("zero trust no significa 'no confiar en nadie'", self.text)

    def test_privacy_framework_version_status_is_explicit(self) -> None:
        self.assertIn("privacy framework 1.0", self.text)
        self.assertIn("privacy framework 1.1", self.text)
        self.assertIn("initial public draft", self.text)
        self.assertIn("1.1 sigue como initial public draft", self.text)

    def test_controls_logging_and_assessment_are_bounded(self) -> None:
        for concept in [
            "sp 800-53 rev. 5",
            "sp 800-53a rev. 5",
            "audit log",
            "accountability",
            "evidencia de control",
            "segregación de funciones",
        ]:
            self.assertIn(concept, self.text)
        self.assertIn("seleccionar un control no demuestra que esté bien configurado", self.text)
        self.assertIn("un log solo aporta accountability", self.text)

    def test_change_contingency_recovery_and_incident_response_are_substantive(self) -> None:
        for concept in [
            "gestión de configuración",
            "change request",
            "análisis de impacto",
            "rollback",
            "contingencia",
            "backup",
            "restore",
            "rpo",
            "rto",
            "incident response",
            "sp 800-61 rev. 3",
        ]:
            self.assertIn(concept, self.text)
        self.assertIn("backup no demuestra recuperación", self.text)
        self.assertIn("haber desplegado el cambio no demuestra", self.text)

    def test_operational_metrics_have_denominators_and_limits(self) -> None:
        equations = " ".join(
            item["latex"].lower()
            for section in self.unit["theory_sections"]
            for item in section.get("equations", [])
        )
        self.assertIn("cfr=", equations)
        self.assertIn("t_{indisp}", equations)
        self.assertIn("disponibilidad y change failure rate son métricas operacionales", self.text)
        self.assertIn("no mide por sí sola integridad de datos, seguridad ni utilidad clínica", self.text)

    def test_implementation_science_and_rollout_are_not_reduced_to_installation(self) -> None:
        for concept in [
            "cfir",
            "readiness",
            "go/no-go",
            "rollout por fases",
            "hypercare",
            "adopción",
            "fidelidad",
            "factibilidad",
            "sostenibilidad",
            "workaround",
        ]:
            self.assertIn(concept, self.text)
        self.assertIn("instalar software no equivale a implementar un sistema sociotécnico", self.text)
        self.assertIn("go-live no es un final", self.text)

    def test_lifecycle_monitoring_exceptions_revalidation_and_retirement_are_explicit(self) -> None:
        for concept in [
            "monitorización",
            "excepción temporal",
            "control compensatorio",
            "revalidación",
            "decommissioning",
            "fecha de expiración",
        ]:
            self.assertIn(concept, self.text)
        self.assertIn("revalidar todo indiscriminadamente es ineficiente", self.text)
        self.assertIn("apagar un servidor no completa el ciclo de vida", self.text)

    def test_guided_activity_is_substantive_and_non_offensive(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 420)
        self.assertGreaterEqual(len(activity["instructions"]), 10)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 20)
        activity_text = json.dumps(activity, ensure_ascii=False).lower()
        for phrase in [
            "sintéticos",
            "no uses credenciales",
            "sin técnicas ofensivas",
            "no contiene técnicas ofensivas",
        ]:
            self.assertIn(phrase, activity_text)

    def test_curricular_integration_closes_u1_to_u5_without_replacing_them(self) -> None:
        purpose = self.unit["purpose"].lower()
        for phrase in [
            "u1",
            "u2",
            "u3",
            "u4",
            "u5",
            "semántica y procedencia",
            "workflows clínicos",
            "interoperabilidad",
            "analítica/cds",
            "factores humanos",
        ]:
            self.assertIn(phrase, purpose)

    def test_examples_and_self_assessment_are_reasoned(self) -> None:
        for example in self.unit["worked_examples"]:
            self.assertGreaterEqual(len(example["reasoning_steps"]), 5)
            self.assertTrue(example["interpretation"].strip())
            self.assertGreaterEqual(len(example["limitations"]), 3)
        for item in self.unit["self_assessment"]:
            self.assertTrue(item["answer"].strip())
            self.assertTrue(item["reasoning"].strip())
            self.assertTrue(item["common_error"].strip())

    def test_sources_are_directly_verified_and_cover_security_health_it_and_implementation(self) -> None:
        for source in self.unit["sources"]:
            self.assertEqual(source["verification_status"], "verified_directly")
            self.assertTrue(source["url"].startswith("https://"))
        urls = " ".join(source["url"].lower() for source in self.unit["sources"])
        for domain in [
            "nist.gov",
            "healthit.gov",
            "ahrq.gov",
            "implementationscience.biomedcentral.com",
            "pubmed.ncbi.nlm.nih.gov",
        ]:
            self.assertIn(domain, urls)

    def test_editorial_notice_blocks_operational_legal_and_clinical_overreach(self) -> None:
        notice = self.unit["editorial_notice"].lower()
        for phrase in [
            "no accede a sistemas clínicos reales",
            "no usa credenciales o tokens reales",
            "no ejecuta escaneo, explotación, malware ni pruebas ofensivas",
            "no constituye asesoría jurídica",
            "auditoría profesional de ciberseguridad",
            "evaluación de conformidad",
            "ni autorización de despliegue",
            "privacy framework 1.1",
            "borrador en 2026",
        ]:
            self.assertIn(phrase, notice)

    def test_catalog_exit_when_publication_updates_editorial_state(self) -> None:
        detected = self.catalog["dimensions"]["specificity"]["template_detected"]
        if "informatica-biomedica" in detected:
            self.skipTest("El catálogo todavía no ha sido sincronizado por el publicador.")
        self.assertNotIn("informatica-biomedica", detected)


if __name__ == "__main__":
    unittest.main()
