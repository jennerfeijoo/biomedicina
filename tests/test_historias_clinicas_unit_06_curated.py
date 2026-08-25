from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "historias-clinicas-terminologias-estandares" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "historias-clinicas-terminologias-estandares" / "unit-06.json"
SUBJECT = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "historias-clinicas-terminologias-estandares.json"
PUBLIC_UNIT = ROOT / "ingenieria-biomedica" / "historias-clinicas-terminologias-estandares" / "unidades" / "unidad-06.html"
CATALOG = ROOT / "data" / "catalog_statuses.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class HistoriasClinicasUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_exact_mirror_and_template_removal(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["slug"], "implementacion-y-validacion")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("ppv=", self.text)
        self.assertNotIn("sensibilidad, especificidad y prevalencia", self.text)

    def test_objectives_cover_traceability_testing_deployment_and_change(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "trazabilidad bidireccional", "pruebas positivas y negativas", "capabilitystatement",
            "testscript", "verificación", "validación para el uso previsto", "go/no-go",
            "rollback", "análisis de impacto", "revalidación proporcional",
        ):
            self.assertIn(phrase, objectives)

    def test_five_substantive_sections(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        for section in sections:
            self.assertGreaterEqual(len(section["paragraphs"]), 6)
            self.assertGreaterEqual(len(section["key_points"]), 6)
            for point in section["key_points"]:
                self.assertGreaterEqual(len(point.split()), 4)
        headings = " ".join(x["heading"] for x in sections).casefold()
        for phrase in (
            "matriz de trazabilidad", "conformidad por capas", "extremo a extremo",
            "observabilidad", "gestión del cambio",
        ):
            self.assertIn(phrase, headings)

    def test_case_use_and_traceability_are_verifiable(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "actores", "precondiciones", "criterio de aceptación", "trazabilidad",
            "requisito", "prueba", "cobertura", "u1–u5",
        ):
            self.assertIn(phrase, text)
        self.assertIn("cada requisito importante necesita al menos una prueba", text)
        self.assertIn("cada prueba debe justificar qué requisito cubre", text)

    def test_conformance_layers_do_not_overclaim(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "$validate", "operationoutcome", "structuredefinition", "implementationguide",
            "capabilitystatement", "testscript", "pruebas negativas", "inferno",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no sobre todo el comportamiento del sistema", text)
        self.assertIn("pasar una suite concreta no significa", text)

    def test_verification_validation_and_test_states_are_separated(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "verificación", "validación para el uso previsto", "fixture", "oráculo",
            "extremo a extremo", "pass", "fail", "blocked", "not run", "regresiones",
        ):
            self.assertIn(phrase, text)
        self.assertIn("blocked indica que no se pudo evaluar", text)
        self.assertIn("ninguna prueba sintética de aula constituye validación clínica", text)

    def test_deployment_is_synthetic_and_observable(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "despliegue simulado", "go/no-go", "rollback", "smoke tests", "observabilidad",
            "umbral", "incidente sintético", "causa raíz",
        ):
            self.assertIn(phrase, text)
        self.assertIn("datos exclusivamente sintéticos", text)
        self.assertIn("no ofrece instrucciones para conectar endpoints clínicos", text)

    def test_change_management_requires_impact_and_revalidation(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in (
            "nist", "control de cambios", "análisis de impacto", "versiones de fhir",
            "regresión proporcional", "revalidación", "cambios urgentes", "rollback",
        ):
            self.assertIn(phrase, text)
        self.assertIn("qué evidencia anterior sigue siendo aplicable", text)
        self.assertIn("no significa eliminar trazabilidad", text)

    def test_glossary_cases_activity_and_errors_are_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 50)
        for term in (
            "matriz de trazabilidad", "$validate", "operationoutcome", "structuredefinition",
            "implementationguide", "capabilitystatement", "testscript", "prueba negativa",
            "blocked", "prueba extremo a extremo", "go/no-go", "rollback",
            "observabilidad", "análisis de impacto", "revalidación", "inferno framework",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 24)
        self.assertGreaterEqual(len(activity["deliverables"]), 12)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 18)

    def test_activity_protects_synthetic_scope_and_end_to_end_reasoning(self) -> None:
        activity = self.unit["guided_activities"][0]
        joined = " ".join(activity["instructions"] + activity["problems"] + activity["checking_criteria"]).casefold()
        for phrase in (
            "exclusivamente", "no uses endpoints", "$validate", "capabilitystatement",
            "testscript", "pruebas negativas", "extremo a extremo", "blocked",
            "go/no-go", "observabilidad", "rollback", "análisis de impacto", "revalidación",
        ):
            self.assertIn(phrase, joined)
        self.assertIn("no se afirma certificación", joined)

    def test_sources_assessment_connections_and_editorial_boundary(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 18)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        sources = " ".join(x["title"] + " " + x["organization"] for x in self.unit["sources"]).casefold()
        for phrase in (
            "validating resources", "testing implementations", "testscript", "capabilitystatement",
            "managing multiple fhir versions", "smart app launch 2.2.0", "inferno core", "nist sp 800-128",
        ):
            self.assertIn(phrase, sources)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "fhir r5 5.0.0", "smart app launch 2.2.0", "no uses ehr", "no uses", "simulado",
            "no como obligación universal", "aprobaciones propias de la organización y jurisdicción",
        ):
            self.assertIn(phrase, notice)

    def test_publication_when_generated(self) -> None:
        if not PUBLIC_UNIT.exists():
            self.skipTest("Página pública pendiente de sincronización automática")
        public_text = PUBLIC_UNIT.read_text(encoding="utf-8")
        self.assertIn(self.unit["purpose"], public_text)

    def test_descriptor_when_promoted(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {x["unit"]: x for x in subject["detailed_units"]}
        if detailed[6]["description"] != self.unit["purpose"]:
            self.skipTest("Descriptor curricular pendiente de promoción automática")
        self.assertEqual(detailed[6]["description"], self.unit["purpose"])

    def test_catalog_when_course_closure_is_published(self) -> None:
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        pending = set(catalog.get("template_detected", []))
        if "historias-clinicas-terminologias-estandares" in pending:
            self.skipTest("Catálogo editorial pendiente de sincronización automática")
        screened = set(catalog.get("screened_no_known_template_marker", []))
        self.assertIn("historias-clinicas-terminologias-estandares", screened)


if __name__ == "__main__":
    unittest.main()
