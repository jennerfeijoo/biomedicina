from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "innovacion-emprendimiento" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "innovacion-emprendimiento" / "unit-04.json"
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
        cls.text = norm(cls.unit)

    def test_identity_mirror_and_template_removal(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "innovacion-emprendimiento")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["title"], "Modelo de negocio y acceso")
        self.assertEqual(self.unit["status"], "review")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("modelo multicriterio transparente", self.text)
        self.assertNotIn("v(a)=", self.text)

    def test_core_business_access_architecture_is_present(self) -> None:
        required = (
            "persona afectada", "usuario", "comprador", "pagador", "decisor",
            "flujo de producto o servicio", "flujo de información", "flujo económico",
            "cobertura", "mecanismo de pago", "reembolso",
            "evaluación de tecnologías sanitarias", "autorización regulatoria",
            "adopción", "adquisición", "coste total de propiedad",
            "margen de contribución", "punto de equilibrio", "efecto presupuestario",
            "asequibilidad", "accesibilidad", "equidad", "cuello de botella",
        )
        for concept in required:
            with self.subTest(concept=concept):
                self.assertIn(concept, self.text)

    def test_economic_equations_are_explicit_and_bounded(self) -> None:
        equations = [
            item["latex"]
            for section in self.unit["theory_sections"]
            for item in section.get("equations", [])
        ]
        self.assertEqual(len(equations), 3)
        self.assertIn("MC=P-CV", equations)
        self.assertTrue(any("N_{BE}" in equation and "CF" in equation for equation in equations))
        self.assertTrue(any(equation.startswith("TCO=") for equation in equations))
        for boundary in (
            "no demuestra demanda",
            "no se calculan qalys ni icers con datos inventados",
            "datos sintéticos",
            "no constituye asesoría comercial",
            "recomendación de inversión",
        ):
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, self.text)

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

    def test_sources_are_directly_verified_and_relevant(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 15)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = " ".join(item["url"].casefold() for item in sources)
        self.assertIn("biodesign.stanford.edu", urls)
        self.assertIn("who.int", urls)
        titles = " ".join(item["title"].casefold() for item in sources)
        self.assertIn("health technology assessment", titles)
        self.assertIn("program curriculum", titles)


if __name__ == "__main__":
    unittest.main()
