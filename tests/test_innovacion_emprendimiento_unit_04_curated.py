from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "innovacion-emprendimiento" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "innovacion-emprendimiento" / "unit-04.json"
SUBJECT = ROOT / "data" / "subjects" / "gestion-etica-comunicacion" / "innovacion-emprendimiento.json"
PUBLIC = ROOT / "gestion-etica-comunicacion" / "innovacion-emprendimiento" / "unidades" / "unidad-04.html"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


def norm(value: object) -> str:
    if isinstance(value, str):
        text = value
    else:
        text = json.dumps(value, ensure_ascii=False)
    return text.casefold().replace("–", "-").replace("—", "-")


class InnovacionEmprendimientoUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        cls.text = norm(cls.unit)
        cls.public = norm(PUBLIC.read_text(encoding="utf-8"))

    def test_identity_schema_and_template_removal(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "innovacion-emprendimiento")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["title"], "Modelo de negocio y acceso")
        self.assertEqual(self.unit["status"], "review")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("modelo multicriterio transparente", self.text)
        self.assertNotIn("v(a)=", self.text)

    def test_actor_payment_and_access_architecture(self) -> None:
        required = (
            "persona afectada", "usuario", "comprador", "pagador", "decisor",
            "flujo de producto o servicio", "flujo de información", "flujo económico",
            "cobertura", "mecanismo de pago", "reembolso",
            "evaluación de tecnologías sanitarias", "autorización regulatoria",
            "adopción", "adquisición", "disponibilidad", "asequibilidad",
            "accesibilidad", "equidad",
        )
        for concept in required:
            with self.subTest(concept=concept):
                self.assertIn(concept, self.text)

    def test_economic_model_is_explicit_and_bounded(self) -> None:
        for concept in (
            "coste total de propiedad", "costes fijos", "costes variables",
            "margen de contribución", "punto de equilibrio", "efecto presupuestario",
            "sensibilidad", "perspectiva", "horizonte temporal", "coste de oportunidad",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, self.text)
        equations = [
            item["latex"]
            for section in self.unit["theory_sections"]
            for item in section.get("equations", [])
        ]
        self.assertEqual(len(equations), 3)
        self.assertIn("MC=P-CV", equations)
        self.assertTrue(any("N_{BE}" in equation and "CF" in equation for equation in equations))
        self.assertTrue(any(equation.startswith("TCO=") for equation in equations))
        self.assertIn("qalys", self.text)
        self.assertIn("icers", self.text)

    def test_distinct_decisions_and_equity_boundaries(self) -> None:
        for phrase in (
            "la autorización regulatoria y la decisión de cobertura responden a preguntas distintas",
            "la asequibilidad para el sistema no implica asequibilidad para la persona",
            "esta relación no demuestra demanda, precio aceptable, cobertura, valor clínico ni sostenibilidad global",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_implementation_channel_covers_lifecycle_and_access_bottlenecks(self) -> None:
        for concept in (
            "evaluación", "adquisición", "integración", "formación", "operación",
            "soporte", "mantenimiento", "retirada", "interoperabilidad",
            "cuello de botella", "conectividad", "centros de menor capacidad",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, self.text)

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
        self.assertGreaterEqual(len(activity["deliverables"]), 9)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 20)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 18)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)

    def test_sources_and_boundaries_are_explicit(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 15)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = " ".join(item["url"].casefold() for item in sources)
        for domain in ("biodesign.stanford.edu", "who.int"):
            with self.subTest(domain=domain):
                self.assertIn(domain, urls)
        source_titles = " ".join(item["title"].casefold() for item in sources)
        self.assertIn("health technology assessment of medical devices", source_titles)
        self.assertIn("program curriculum", source_titles)
        for boundary in (
            "datos sintéticos", "asesoría comercial", "reembolso", "regulatoria", "inversión",
        ):
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, self.text)

    def test_publication_matches_canonical_purpose(self) -> None:
        published = next(
            item for item in self.subject["detailed_units"] if item["unit"] == 4
        )
        self.assertEqual(published["description"], self.unit["purpose"])

    def test_public_page_exposes_curated_content(self) -> None:
        self.assertNotIn(GENERIC, self.public)
        for phrase in (
            "margen de contribución", "coste total de propiedad",
            "evaluación de tecnologías sanitarias", "asequibilidad",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.public)


if __name__ == "__main__":
    unittest.main()
