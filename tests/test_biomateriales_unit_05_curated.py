from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomateriales" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "biomateriales" / "unit-05.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomaterialesUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomateriales")
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        for concept in (
            "mensurando",
            "astm e8/e8m-24",
            "astm d638-22",
            "iso 25178-2:2021",
            "sem/eds",
            "afm",
            "xps",
            "iso 10993-18:2020",
        ):
            self.assertIn(concept, self.text)
        self.assertNotIn("iso 4287", self.text)

    def test_theory_is_substantive_and_keeps_scales_separate(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for phrase in (
            "propiedades del volumen de propiedades de superficie",
            "ángulo de contacto",
            "una micrografía atractiva no es una medición representativa",
            "profundidad de análisis",
            "extractables y leachables",
        ):
            self.assertIn(phrase, theory)
        self.assertIn("no afirma seguridad", theory)

    def test_equations_match_characterization_scope(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("\\sigma=\\frac{F}{A_0}", equations)
        self.assertIn("\\varepsilon=\\frac{L-L_0}{L_0}", equations)
        self.assertIn("E\\approx\\frac{\\Delta\\sigma}{\\Delta\\varepsilon}", equations)
        self.assertIn("S_a=\\frac{1}{A}\\iint_A |z(x,y)|\\,dx\\,dy", equations)

    def test_pedagogy_progresses_from_scaffold_to_audit(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertIn("Elegir la técnica", activities[0]["title"])
        self.assertIn("multimodal", activities[1]["title"].casefold())
        self.assertIn("Auditoría ciega", activities[2]["title"])
        for activity in activities:
            self.assertGreaterEqual(len(activity["instructions"]), 5)
            self.assertGreaterEqual(len(activity["problems"]), 8)
            self.assertGreaterEqual(len(activity["deliverables"]), 6)
            self.assertGreaterEqual(len(activity["checking_criteria"]), 8)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintétic", activity_text)
        self.assertIn("no prepares muestras ni operes equipos reales", activity_text)

    def test_glossary_examples_errors_and_assessment_are_complete(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "mensurando",
            "rugosidad areal",
            "ángulo de contacto",
            "microscopía electrónica de barrido (sem)",
            "eds/edx",
            "microscopía de fuerza atómica (afm)",
            "xps",
            "incertidumbre de medición",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_current(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        expected = {
            "https://www.iso.org/standard/64750.html",
            "https://www.iso.org/standard/82241.html",
            "https://www.iso.org/standard/75138.html",
            "https://store.astm.org/e0008_e0008m-24.html",
            "https://store.astm.org/standards/d638/1000",
            "https://www.iso.org/standard/74591.html",
            "https://store.astm.org/standards/d7334",
            "https://www.bipm.org/en/doi/10.59161/jcgm100-2008e",
        }
        self.assertTrue(expected.issubset(urls))

    def test_boundaries_with_u4_u6_and_clinical_inference_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        connections = json.dumps(self.unit["biomedical_connections"], ensure_ascii=False).casefold()
        self.assertIn("u4", connections)
        self.assertIn("u6", connections)
        self.assertIn("no constituye por sí sola evaluación de biocompatibilidad", notice)
        self.assertIn("seguridad clínica", notice)
        self.assertIn("evaluación de conformidad", notice)
        self.assertIn("revisión disciplinar humana externa permanece pendiente", notice)


if __name__ == "__main__":
    unittest.main()
