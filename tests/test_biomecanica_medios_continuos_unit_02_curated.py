from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomecanica-medios-continuos" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "biomecanica-medios-continuos" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomecanicaMediosContinuosUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomecanica-medios-continuos")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "tensor de tensiones de cauchy",
            "vector de tracción",
            "balance de cantidad de movimiento",
            "condiciones de frontera",
            "preestrés",
        ):
            self.assertIn(concept, text)

    def test_core_equations_and_scope(self) -> None:
        equations = {e["latex"] for s in self.unit["theory_sections"] for e in s.get("equations", [])}
        self.assertIn("\\mathbf t(\\mathbf n)=\\boldsymbol\\sigma\\,\\mathbf n", equations)
        self.assertIn("\\nabla\\cdot\\boldsymbol\\sigma+\\rho\\mathbf b=\\rho\\mathbf a", equations)
        self.assertIn("\\boldsymbol\\sigma=\\boldsymbol\\sigma^{\\mathsf T}", equations)
        self.assertIn("\\bar{\\mathbf t}=-p\\mathbf n", equations)
        self.assertIn("\\mathbf P=J\\,\\boldsymbol\\sigma\\mathbf F^{-\\mathsf T}", equations)
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("leyes constitutivas", notice)
        self.assertIn("corresponden a u3", notice)

    def test_theory_and_pedagogy_are_substantive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(s["paragraphs"]) >= 3 for s in sections))
        self.assertTrue(all(len(s["key_points"]) >= 4 for s in sections))
        self.assertGreaterEqual(len(self.unit["glossary"]), 18)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 8)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)

    def test_guided_activity_is_synthetic_and_scaffolded(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 7)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 12)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintéticas", text)
        self.assertIn("no ajustes una ley constitutiva", text)
        self.assertIn("diagnóstico", text)

    def test_sources_are_traceable(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(s.get("verification_status") == "verified_directly_2026-08-24" for s in sources))
        urls = {s["url"] for s in sources}
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC7617344/", urls)
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC4958049/", urls)
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC3705970/", urls)
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC3711966/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/41698563/", urls)

    def test_clinical_and_curricular_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("una tensión calculada no se presenta como daño", notice)
        self.assertIn("la relación constitutiva", purpose)
        self.assertIn("queda para u3", purpose)


# Final user-authored trigger after U2 publication metadata synchronization.
if __name__ == "__main__":
    unittest.main()
