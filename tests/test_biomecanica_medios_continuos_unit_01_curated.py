from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomecanica-medios-continuos" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "biomecanica-medios-continuos" / "unit-01.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomecanicaMediosContinuosUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomecanica-medios-continuos")
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in ("hipótesis de continuo", "gradiente de deformación", "cauchy–green", "green–lagrange", "conservación de masa"):
            self.assertIn(concept, text)

    def test_core_equations_and_scope(self) -> None:
        equations = {e["latex"] for s in self.unit["theory_sections"] for e in s.get("equations", [])}
        self.assertIn("\\mathbf{F}=\\frac{\\partial\\boldsymbol{\\chi}}{\\partial\\mathbf{X}},\\qquad d\\mathbf{x}=\\mathbf{F}\\,d\\mathbf{X}", equations)
        self.assertIn("J=\\det\\mathbf{F},\\qquad dv=J\\,dV", equations)
        self.assertIn("\\mathbf{E}=\\frac{1}{2}(\\mathbf{C}-\\mathbf{I})", equations)
        self.assertIn("\\rho_0=J\\,\\rho", equations)
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("esfuerzo y equilibrio corresponden a u2", notice)
        self.assertIn("leyes constitutivas a u3", notice)
        self.assertIn("elementos finitos", notice)

    def test_theory_and_pedagogy_are_substantive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(s["paragraphs"]) >= 3 for s in sections))
        self.assertTrue(all(len(s["key_points"]) >= 4 for s in sections))
        self.assertGreaterEqual(len(self.unit["glossary"]), 16)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 3)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 6)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 8)

    def test_guided_activity_is_synthetic_and_scaffolded(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 10)
        self.assertGreaterEqual(len(activity["deliverables"]), 6)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintética", text)
        self.assertIn("rotación rígida", text)
        self.assertIn("no se calculan tensiones", text)

    def test_sources_are_traceable(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 7)
        self.assertTrue(all(s.get("verification_status") == "verified_directly_2026-08-24" for s in sources))
        urls = {s["url"] for s in sources}
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC2813063/", urls)
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC10903412/", urls)
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC8940853/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/41698563/", urls)

    def test_editorial_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("actividades son sintéticas", notice)
        self.assertIn("validación clínica", notice)


# Final user-authored trigger after publication metadata synchronization.
if __name__ == "__main__":
    unittest.main()
