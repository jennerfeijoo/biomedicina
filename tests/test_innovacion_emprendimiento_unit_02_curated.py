from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "innovacion-emprendimiento" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "innovacion-emprendimiento" / "unit-02.json"
SUBJECT = ROOT / "data" / "subjects" / "gestion-etica-comunicacion" / "innovacion-emprendimiento.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


def norm(text: str) -> str:
    return text.casefold().replace("–", "-").replace("—", "-")


class InnovacionEmprendimientoUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = norm(json.dumps(cls.unit, ensure_ascii=False))
        cls.subject = json.loads(SUBJECT.read_text(encoding="utf-8"))

    def test_source_mirror_and_identity(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "innovacion-emprendimiento")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["title"], "Propuesta de valor")
        self.assertEqual(self.unit["status"], "review")

    def test_template_and_generic_score_are_absent(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("v(a)=\\sum", self.text)
        self.assertNotIn("modelo multicriterio transparente para comparar alternativas", self.text)

    def test_theory_has_real_problem_solution_fit_content(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        for concept in (
            "propuesta de valor",
            "hipótesis falsable",
            "persona afectada",
            "usuario operativo",
            "pagador",
            "mantenedor",
            "alternativa de referencia",
            "statu quo",
            "resultado observable",
            "ajuste problema-solución",
            "product-market fit",
            "evidencia discrepante",
            "criterio de refutación",
            "seguir, revisar o rechazar",
            "u3",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, self.text)

    def test_only_descriptive_difference_equation_is_used(self) -> None:
        equations = [
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        ]
        self.assertEqual(equations, [r"\Delta p=p_{\mathrm{prop}}-p_{\mathrm{ref}}"])
        self.assertIn("no demuestra causalidad", self.text)
        self.assertIn("beneficio clínico", self.text)

    def test_problem_solution_fit_is_bounded(self) -> None:
        purpose = norm(self.unit["purpose"])
        self.assertIn("no demuestra product-market fit, eficacia, seguridad, adopción", purpose)
        theory = norm(json.dumps(self.unit["theory_sections"], ensure_ascii=False))
        self.assertIn("no equivale a product-market fit, adopción, ventas, eficacia clínica ni seguridad", theory)
        self.assertIn("no significa que el producto sea viable", theory)

    def test_learning_scaffolds_are_substantial(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 40)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertEqual(len(self.unit["guided_activities"]), 1)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 12)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 20)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 18)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)

    def test_sources_are_verified_and_multisource(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 15)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = " ".join(item["url"].casefold() for item in sources)
        for domain in ("biodesign.stanford.edu", "nih.gov", "oecd.org", "fda.gov", "iso.org", "who.int"):
            with self.subTest(domain=domain):
                self.assertIn(domain, urls)

    def test_editorial_boundaries_are_explicit(self) -> None:
        notice = norm(self.unit["editorial_notice"])
        for boundary in (
            "no constituye investigación con seres humanos",
            "customer discovery real",
            "validación de factores humanos",
            "validación clínica",
            "seguridad o eficacia",
            "evaluación regulatoria",
            "reembolso",
            "recomendación de inversión",
        ):
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, notice)

    def test_published_descriptor_matches_canonical_purpose(self) -> None:
        published = next(item for item in self.subject["detailed_units"] if item["unit"] == 2)
        self.assertEqual(published["title"], self.unit["title"])
        self.assertEqual(published["description"], self.unit["purpose"])
        self.assertIn("hipótesis explícita y falsable", norm(published["description"]))


if __name__ == "__main__":
    unittest.main()
