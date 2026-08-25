from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "etica-responsabilidad-social" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "etica-responsabilidad-social" / "unit-04.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class EticaResponsabilidadSocialUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "etica-responsabilidad-social")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed_and_scope_is_specific(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        for concept in (
            "equidad sanitaria",
            "acceso efectivo",
            "discapacidad",
            "accesibilidad",
            "diseño universal",
            "ajuste razonable",
            "determinantes sociales",
            "brecha digital",
            "wcag 2.2",
            "co-diseño",
        ):
            self.assertIn(concept, self.text)

    def test_theory_is_substantive_and_preserves_course_boundaries(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        headings = " ".join(section["heading"] for section in sections).casefold()
        for concept in ("equidad", "discapacidad", "brecha digital", "medir acceso", "monitorización"):
            self.assertIn(concept, headings)
        self.assertIn("u3 estudió gobernanza de datos e ia", self.text)
        self.assertIn("u5 abordará ambiente y cadena de suministro", self.text)
        self.assertIn("u6 integrará deliberación y rendición de cuentas", self.text)

    def test_accessibility_and_equity_boundaries_are_explicit(self) -> None:
        self.assertIn("disponibilidad no equivale a acceso efectivo", self.text)
        self.assertIn("igualdad y equidad no son sinónimos", self.text)
        self.assertIn("una desigualdad es una diferencia observable", self.text)
        self.assertIn("wcag 2.2", self.text)
        self.assertIn("no garantiza por sí sola acceso sanitario", self.text)
        self.assertIn("digital por defecto", self.text)
        self.assertIn("digital obligatorio", self.text)

    def test_quantitative_access_example_is_descriptive_not_moral_score(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn(r"\mathrm{Completion}_g=\frac{N_{complete,g}}{N_{start,g}}", equations)
        self.assertIn(r"\Delta_{access}=p_A-p_B", equations)
        self.assertNotIn(r"V(a)=\sum", json.dumps(self.unit, ensure_ascii=False))
        examples = json.dumps(self.unit["worked_examples"], ensure_ascii=False).casefold()
        self.assertIn("a=81/90=0,90", examples)
        self.assertIn("b=56/80=0,70", examples)
        self.assertIn("0,20", examples)
        self.assertIn("no explica por qué existe ni si es injusta", self.text)

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 8)
        self.assertGreaterEqual(len(activity["problems"]), 16)
        self.assertGreaterEqual(len(activity["deliverables"]), 7)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 16)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("no cargues información personal", text)
        self.assertIn("embudo de acceso", text)
        self.assertIn("canal equivalente", text)
        self.assertIn("no presentes el ejercicio como certificación", text)

    def test_learning_scaffolds_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 22)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 13)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "equidad sanitaria",
            "acceso efectivo",
            "diseño universal",
            "ajuste razonable",
            "tecnología de apoyo",
            "brecha digital",
            "co-diseño",
            "wcag 2.2",
            "tasa de finalización",
            "canal equivalente",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_cover_rights_access_and_empirical_evidence(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(source.get("verification_status") == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        expected = {
            "https://www.who.int/publications/i/item/9789240063600",
            "https://www.who.int/news-room/fact-sheets/detail/social-determinants-of-health",
            "https://www.ohchr.org/en/instruments-mechanisms/instruments/convention-rights-persons-disabilities",
            "https://www.w3.org/TR/WCAG22/",
            "https://www.who.int/publications/i/item/9789241550505",
            "https://www.who.int/publications/i/item/9789240049451",
            "https://pubmed.ncbi.nlm.nih.gov/36707791/",
            "https://pubmed.ncbi.nlm.nih.gov/33674277/",
        }
        self.assertTrue(expected.issubset(urls))

    def test_professional_overclaiming_is_blocked(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for boundary in (
            "no constituye revisión disciplinar externa",
            "auditoría profesional de accesibilidad",
            "certificación wcag",
            "evaluación de conformidad",
            "asesoría jurídica",
            "validación clínica",
            "recomendación de compra",
            "autorización de despliegue",
        ):
            self.assertIn(boundary, notice)
        self.assertIn("jurisdicción", notice)
        self.assertIn("normativa vigente", notice)


if __name__ == "__main__":
    unittest.main()
