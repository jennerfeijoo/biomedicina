from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "innovacion-emprendimiento" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "innovacion-emprendimiento" / "unit-06.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


def norm(value: object) -> str:
    if isinstance(value, str):
        text = value
    else:
        text = json.dumps(value, ensure_ascii=False)
    return text.casefold().replace("–", "-").replace("—", "-")


class InnovacionEmprendimientoUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = norm(cls.unit)

    def test_identity_mirror_and_template_removal(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "innovacion-emprendimiento")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["title"], "Financiación y comunicación")
        self.assertEqual(self.unit["status"], "review")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("modelo multicriterio transparente", self.text)
        self.assertNotIn("v(a)=", self.text)

    def test_budget_milestones_and_cash_are_operational(self) -> None:
        for concept in (
            "criterio de salida", "paquete de trabajo", "dependencia", "coste único",
            "coste recurrente", "flujo de caja", "burn neto", "runway",
            "escenario base", "análisis de sensibilidad", "reserva",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, self.text)
        self.assertIn("financiar hitos, no una cronología optimista", self.text)
        self.assertIn("trayectoria mensual de caja", self.text)

    def test_funding_sources_and_dilution_have_boundaries(self) -> None:
        for concept in (
            "bootstrapping", "financiación no dilutiva", "subvención", "deuda",
            "equity", "dilución", "pre-money", "post-money", "cap table",
            "inversor estratégico", "blended finance",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, self.text)
        self.assertIn("no constituye asesoría financiera", self.text)
        self.assertIn("securities", self.text)
        self.assertIn("no para valorar una empresa ni recomendar un acuerdo", self.text)

    def test_risk_use_of_funds_and_pitch_are_evidence_based(self) -> None:
        for concept in (
            "señal temprana", "mitigación", "contingencia", "stop/adapt/go",
            "use of funds", "ask", "claim → evidencia", "cherry-picking",
            "tam", "sam", "som", "due diligence",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, self.text)
        self.assertIn("una interacción con regulador no se traduce en «aprobación asegurada»", self.text)
        self.assertIn("una carta de interés no se presenta como contrato o ingreso", self.text)

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

    def test_sources_are_official_and_scope_is_explicit(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 18)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = " ".join(item["url"].casefold() for item in sources)
        for domain in ("nih.gov", "eic.ec.europa.eu", "ec.europa.eu", "sec.gov", "sba.gov", "who.int"):
            with self.subTest(domain=domain):
                self.assertIn(domain, urls)
        for boundary in (
            "no constituye asesoría financiera", "ejercicios simplificados",
            "ninguna proyección", "autorización regulatoria", "retorno",
        ):
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, self.text)


if __name__ == "__main__":
    unittest.main()
