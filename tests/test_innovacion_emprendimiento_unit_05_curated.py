from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "innovacion-emprendimiento" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "innovacion-emprendimiento" / "unit-05.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


def norm(value: object) -> str:
    if isinstance(value, str):
        text = value
    else:
        text = json.dumps(value, ensure_ascii=False)
    return text.casefold().replace("–", "-").replace("—", "-")


class InnovacionEmprendimientoUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = norm(cls.unit)

    def test_identity_mirror_and_template_removal(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "innovacion-emprendimiento")
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["title"], "Propiedad intelectual y regulación")
        self.assertEqual(self.unit["status"], "review")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("modelo multicriterio transparente", self.text)
        self.assertNotIn("v(a)=", self.text)

    def test_ip_and_fto_are_separated(self) -> None:
        for concept in (
            "estado de la técnica", "novedad", "actividad inventiva", "reivindicación",
            "familia de patentes", "libertad de operación", "estado jurídico",
            "producto, territorio y tiempo-específica", "patent landscape",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, self.text)
        self.assertIn("no encontrar un documento", self.text)
        self.assertIn("nunca se etiqueta un producto como «libre de patentes»", self.text)

    def test_regulatory_reasoning_is_jurisdiction_specific(self) -> None:
        for concept in (
            "uso previsto", "intended use", "claims", "clasificación",
            "510(k)", "de novo", "pma", "mdr 2017/745", "jurisdicción",
            "qmsr", "2 de febrero de 2026",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, self.text)
        self.assertIn("no deben extrapolarse a la unión europea", self.text)
        self.assertIn("no para declarar una clasificación oficial", self.text)

    def test_claims_map_to_evidence_without_clinical_overreach(self) -> None:
        for concept in (
            "claim → riesgo → requisito → evidencia",
            "verificación", "validación", "validación analítica",
            "validación clínica", "evidencia clínica", "trazabilidad de requisitos",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, self.text)
        self.assertIn("una demostración de ingeniería no se transforma automáticamente en evidencia clínica", self.text)
        self.assertIn("no fija un paquete universal de ensayos", self.text)

    def test_learning_scaffolds_are_substantial(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        self.assertGreaterEqual(len(self.unit["glossary"]), 45)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertEqual(len(self.unit["guided_activities"]), 1)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 24)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 18)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)

    def test_sources_and_scope_are_strong(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 18)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = " ".join(item["url"].casefold() for item in sources)
        for domain in ("wipo.int", "fda.gov", "eur-lex.europa.eu", "imdrf.org"):
            with self.subTest(domain=domain):
                self.assertIn(domain, urls)
        for boundary in (
            "no constituyen opinión jurídica", "no constituye", "autorización de comercialización",
            "marcado ce", "profesionales y autoridades competentes",
        ):
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, self.text)


if __name__ == "__main__":
    unittest.main()
