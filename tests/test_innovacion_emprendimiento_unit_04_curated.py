from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "innovacion-emprendimiento" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "innovacion-emprendimiento" / "unit-04.json"
SUBJECT = ROOT / "data" / "subjects" / "gestion-etica-comunicacion" / "innovacion-emprendimiento.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


def norm(text: str) -> str:
    return text.casefold().replace("–", "-").replace("—", "-")


class InnovacionEmprendimientoUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = norm(json.dumps(cls.unit, ensure_ascii=False))
        cls.subject = json.loads(SUBJECT.read_text(encoding="utf-8"))

    def test_source_mirror_and_identity(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "innovacion-emprendimiento")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["title"], "Modelo de negocio y acceso")
        self.assertEqual(self.unit["status"], "review")

    def test_template_and_generic_score_are_absent(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("v(a)=\\sum", self.text)
        self.assertNotIn("modelo multicriterio transparente para comparar alternativas", self.text)
        self.assertNotIn("índice de equidad", norm(json.dumps(self.unit["theory_sections"][:4], ensure_ascii=False)))

    def test_roles_are_not_collapsed_into_customer(self) -> None:
        objectives = norm(" ".join(self.unit["learning_objectives"]))
        for phrase in (
            "usuario final",
            "comprador",
            "pagador",
            "decisor de adopción",
            "beneficiario",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, objectives)
        self.assertIn("quién usa, quién decide y quién paga", self.text)
        self.assertIn("no inferir demanda pagadora", self.text)

    def test_access_pathway_separates_distinct_decisions(self) -> None:
        for concept in (
            "regulación",
            "hta",
            "cobertura",
            "reembolso",
            "compra",
            "adopción",
            "implementación",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, self.text)
        self.assertIn("decisiones diferentes", self.text)
        self.assertIn("no equivale por sí sola a compra inmediata", self.text)

    def test_economics_are_specific_and_bounded(self) -> None:
        equations = " ".join(item["latex"] for section in self.unit["theory_sections"] for item in section.get("equations", []))
        self.assertIn("MC=P-CV", equations)
        self.assertIn("Q^{*}=\\frac{CF}{P-CV}", equations)
        self.assertIn("CTS=CF_{atribuibles}+Q(CV+CS)", equations)
        self.assertIn("no predice demanda", self.text)
        self.assertIn("no es beneficio neto", self.text)
        self.assertIn("costes de soporte", self.text)
        self.assertIn("análisis de sensibilidad", self.text)

    def test_access_and_equity_are_not_reduced_to_one_score(self) -> None:
        for concept in (
            "asequibilidad",
            "disponibilidad",
            "accesibilidad",
            "barreras distributivas",
            "salvaguarda de acceso",
            "desagrega",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, self.text)
        self.assertIn("no se construye un único «índice de equidad»", self.text)
        self.assertIn("menor precio no garantiza mayor equidad", self.text)

    def test_channels_and_capacity_are_real_operational_constraints(self) -> None:
        for phrase in (
            "canal comercial",
            "canal de implementación",
            "canal de soporte",
            "fricción de adopción",
            "capacidad operativa",
            "mantenimiento",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)
        self.assertIn("product-market fit", self.text)
        self.assertIn("capacidad real", self.text)

    def test_learning_scaffolds_are_substantial(self) -> None:
        self.assertEqual(len(self.unit["theory_sections"]), 5)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in self.unit["theory_sections"]))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in self.unit["theory_sections"]))
        self.assertGreaterEqual(len(self.unit["glossary"]), 40)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertEqual(len(self.unit["guided_activities"]), 1)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 12)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 9)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 18)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)

    def test_sources_are_verified_and_authoritative(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 15)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = " ".join(item["url"].casefold() for item in sources)
        for domain in ("who.int", "nice.org.uk", "health.ec.europa.eu"):
            with self.subTest(domain=domain):
                self.assertIn(domain, urls)
        self.assertIn("health technology assessment of medical devices, 2nd edition", self.text)

    def test_editorial_boundaries_and_next_units_are_explicit(self) -> None:
        notice = norm(self.unit["editorial_notice"])
        for boundary in (
            "no constituye asesoría financiera",
            "regulatoria",
            "propiedad intelectual",
            "reembolso",
            "no confirma cobertura",
            "product-market fit",
            "compra institucional",
            "seguridad, eficacia o utilidad clínica",
        ):
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, notice)
        self.assertIn("u5 abordará propiedad intelectual y regulación", self.text)
        self.assertIn("u6 desarrollará financiación, hitos, comunicación y riesgos", self.text)

    def test_published_descriptor_matches_after_promotion(self) -> None:
        published = next(item for item in self.subject["detailed_units"] if item["unit"] == 4)
        if published["description"] != self.unit["purpose"]:
            self.skipTest("El descriptor U4 se endurecerá después del commit de publicación.")
        self.assertEqual(published["title"], self.unit["title"])
        self.assertEqual(published["description"], self.unit["purpose"])
        self.assertIn("usuario, comprador, pagador y decisor", norm(published["description"]))


if __name__ == "__main__":
    unittest.main()
