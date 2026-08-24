from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "desarrollo-dispositivos-medicos" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "desarrollo-dispositivos-medicos" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class DesarrolloDispositivosMedicosUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "desarrollo-dispositivos-medicos")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed_and_risk_scope_is_specific(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "situación peligrosa",
            "secuencia de eventos",
            "riesgo residual",
            "riesgo residual global",
            "producción y posproducción",
            "beneficio-riesgo",
        ):
            self.assertIn(concept, text)

    def test_theory_preserves_causal_model_and_control_hierarchy(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "peligro",
            "situación peligrosa",
            "daño",
            "criterios de aceptabilidad",
            "seguridad inherente",
            "medidas protectoras",
            "información para la seguridad",
            "riesgo residual global",
        ):
            self.assertIn(concept, theory)
        self.assertIn("u4", theory)
        self.assertFalse(any(section.get("equations") for section in sections))

    def test_ordinal_risk_scores_are_not_treated_as_physical_equations(self) -> None:
        theory = " ".join(p for section in self.unit["theory_sections"] for p in section["paragraphs"]).casefold()
        self.assertIn("no convierte automáticamente probabilidad y severidad en números multiplicables", theory)
        self.assertIn("no adquiere por ello las propiedades de una magnitud física", theory)
        self.assertIn("elimina por tanto `r=p×s` como ecuación central", theory)

    def test_progressive_activities_are_synthetic_and_scaffolded(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertGreaterEqual(len(activities[0]["problems"]), 12)
        self.assertGreaterEqual(len(activities[0]["checking_criteria"]), 10)
        self.assertGreaterEqual(len(activities[1]["problems"]), 5)
        self.assertGreaterEqual(len(activities[2]["problems"]), 5)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("no incorpores datos de pacientes", activity_text)
        self.assertIn("apoyo reducido", activities[1]["title"].casefold())
        self.assertIn("autónomo", activities[2]["title"].casefold())
        self.assertIn("verificación prevista", activity_text)

    def test_glossary_examples_errors_and_assessment_are_substantive(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "peligro",
            "situación peligrosa",
            "daño",
            "matriz de riesgo",
            "control del riesgo",
            "riesgo residual",
            "análisis beneficio-riesgo",
            "riesgo residual global",
            "archivo de gestión de riesgos",
        ):
            self.assertIn(term, terms)

    def test_sources_are_current_traceable_and_authoritative(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://www.iso.org/standard/72704.html", urls)
        self.assertIn("https://www.iso.org/standard/74437.html", urls)
        self.assertIn("https://www.iso.org/standard/94297.html", urls)
        self.assertIn(
            "https://www.accessdata.fda.gov/scripts/cdrh/cfstandards/detail.cfm?standard__identification_no=41349",
            urls,
        )
        self.assertIn(
            "https://www.fda.gov/medical-devices/postmarket-requirements-devices/quality-management-system-regulation-qmsr",
            urls,
        )
        self.assertIn(
            "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/applying-human-factors-and-usability-engineering-medical-devices",
            urls,
        )

    def test_lifecycle_and_regulatory_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("iso 14971:2019 sigue siendo la edición iso vigente", notice)
        self.assertIn("confirmada en 2025", notice)
        self.assertIn("aún no debe tratarse como reemplazo publicado", notice)
        self.assertIn("no uses datos de pacientes", notice)
        self.assertIn("u4 ejecuta la verificación controlada", notice)
        self.assertIn("u5 aborda validación", notice)
        self.assertIn("sin reducir el riesgo a una multiplicación de escalas ordinales", purpose)


# User-authored final-gate trigger after deterministic public-site synchronization.
if __name__ == "__main__":
    unittest.main()
