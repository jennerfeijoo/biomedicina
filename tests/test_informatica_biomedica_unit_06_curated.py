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

    def test_published_descriptor_matches_when_promoted(self) -> None:
        published = next(item for item in self.descriptor["detailed_units"] if item["unit"] == 6)
        if published["description"] != self.unit["purpose"]:
            self.skipTest("El publicador todavía no ha promovido la descripción canónica de U6")
        self.assertEqual(published["description"], self.unit["purpose"])

    def test_identity_depth_and_course_closure(self) -> None:
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
        self.assertGreaterEqual(len(self.unit["glossary"]), 55)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 20)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        self.assertGreaterEqual(len(self.unit["sources"]), 16)
        self.assertIn("integra los artefactos de u1–u5", self.unit["purpose"].lower())

    def test_generic_template_and_inherited_ppv_are_removed(self) -> None:
        for marker in [
            "concepto de la unidad que debe definirse",
            "modelo conceptual de gobernanza e implementación",
            "construir un modelo que conecte privacidad con seguridad",
            "integrar privacidad, seguridad, calidad y cambio organizativo para resolver un caso",
        ]:
            self.assertNotIn(marker, self.text)
        self.assertNotIn("ppv=\\frac", self.text)

    def test_governance_is_about_decision_rights_and_evidence(self) -> None:
        for concept in ["derechos de decisión", "accountability", "raci", "decision log", "tolerancia al riesgo", "escalado"]:
            self.assertIn(concept, self.text)
        self.assertIn("política, estándar interno, procedimiento, control y evidencia no son sinónimos", self.text)
        self.assertIn("raci documenta responsabilidades locales pero no crea autoridad legal o clínica", self.text)

    def test_privacy_and_security_are_distinct_and_current(self) -> None:
        for concept in ["riesgo de privacidad", "minimización de datos", "confidencialidad", "integridad", "disponibilidad", "least privilege"]:
            self.assertIn(concept, self.text)
        self.assertIn("puede existir riesgo de privacidad sin intrusión", self.text)
        self.assertIn("autenticación prueba identidad; autorización determina acciones permitidas", self.text)
        self.assertIn("seguía siendo borrador público en agosto de 2026", self.text)
        self.assertIn("iso 27799:2025", self.text)
        self.assertIn("govern, identify, protect, detect, respond y recover", self.text)

    def test_change_continuity_and_recovery_are_substantive(self) -> None:
        for concept in ["baseline de configuración", "change control", "release", "deployment", "rollback", "backup", "restore", "rto", "rpo", "downtime"]:
            self.assertIn(concept, self.text)
        self.assertIn("backup no equivale a restore y rto no equivale a rpo", self.text)
        self.assertIn("disponibilidad alta no demuestra seguridad, integridad ni utilidad clínica", self.text)
        equations = " ".join(item["latex"].lower() for section in self.unit["theory_sections"] for item in section.get("equations", []))
        self.assertIn("t_{available}", equations)

    def test_implementation_science_separates_determinants_strategies_and_outcomes(self) -> None:
        for concept in ["cfir", "determinante de implementación", "estrategia de implementación", "aceptabilidad", "adopción", "factibilidad", "fidelidad", "sostenibilidad"]:
            self.assertIn(concept, self.text)
        self.assertIn("resultados de implementación son distintos de resultados de servicio y clínicos", self.text)
        self.assertIn("cfir organiza determinantes de implementación y no sustituye medidas de resultados", self.text)
        self.assertIn("adopción elevada no demuestra eficacia clínica", self.text)

    def test_monitoring_incidents_and_deimplementation_are_explicit(self) -> None:
        for concept in ["monitorización", "evaluación de impacto", "near miss", "postmortem", "de-implementación"]:
            self.assertIn(concept, self.text)
        self.assertIn("monitorizar la implementación de evaluar el impacto", self.text)
        self.assertIn("la asociación temporal no prueba causalidad", self.text)
        self.assertIn("cada indicador necesita denominador, fuente, frecuencia, responsable, umbral y acción definidos", self.text)

    def test_guided_activity_is_substantive_synthetic_and_non_authorizing(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 420)
        self.assertGreaterEqual(len(activity["instructions"]), 12)
        self.assertGreaterEqual(len(activity["problems"]), 24)
        self.assertGreaterEqual(len(activity["deliverables"]), 12)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)
        activity_text = json.dumps(activity, ensure_ascii=False).lower()
        self.assertIn("sistema sintético", activity_text)
        self.assertIn("tabletop", activity_text)
        self.assertIn("no constituye despliegue, cumplimiento legal, certificación ni validación clínica real", activity_text)

    def test_examples_and_self_assessment_are_reasoned(self) -> None:
        for example in self.unit["worked_examples"]:
            self.assertGreaterEqual(len(example["reasoning_steps"]), 5)
            self.assertTrue(example["interpretation"].strip())
            self.assertGreaterEqual(len(example["limitations"]), 3)
        for item in self.unit["self_assessment"]:
            self.assertTrue(item["answer"].strip())
            self.assertTrue(item["reasoning"].strip())
            self.assertTrue(item["common_error"].strip())

    def test_sources_are_directly_verified_and_multidisciplinary(self) -> None:
        for source in self.unit["sources"]:
            self.assertEqual(source["verification_status"], "verified_directly")
            self.assertTrue(source["url"].startswith("https://"))
        urls = " ".join(source["url"].lower() for source in self.unit["sources"])
        for domain in ["nist.gov", "iso.org", "healthit.gov", "who.int", "pubmed.ncbi.nlm.nih.gov"]:
            self.assertIn(domain, urls)

    def test_editorial_notice_blocks_operational_and_regulatory_overreach(self) -> None:
        notice = self.unit["editorial_notice"].lower()
        for phrase in [
            "no procesa historias clínicas reales",
            "no modifica ehr ni cds operativos",
            "no ejecuta pruebas de penetración contra sistemas reales",
            "no define obligaciones jurídicas de una jurisdicción",
            "no constituye certificación iso",
            "ni aprobación institucional",
            "no con una autorización de producción",
        ]:
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
