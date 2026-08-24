from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomecanica-medios-continuos" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "biomecanica-medios-continuos" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomecanicaMediosContinuosUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomecanica-medios-continuos")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "hiperelasticidad",
            "incompresibilidad",
            "anisotropía",
            "identificabilidad",
            "validación predictiva",
        ):
            self.assertIn(concept, text)

    def test_core_equations_and_scope(self) -> None:
        equations = {e["latex"] for s in self.unit["theory_sections"] for e in s.get("equations", [])}
        self.assertIn("\\mathbf P=\\frac{\\partial\\Psi}{\\partial\\mathbf F}", equations)
        self.assertIn("\\Psi_{NH}=\\frac{\\mu}{2}(I_1-3)", equations)
        self.assertIn("I_4=\\mathbf M\\cdot\\mathbf C\\mathbf M=\\lambda_f^2", equations)
        self.assertIn("L(\\boldsymbol\\theta)=\\sum_i w_i\\,\\|y_i-\\hat y_i(\\boldsymbol\\theta)\\|^2", equations)
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("relajación, fluencia y poroelasticidad corresponden a u4", notice)
        self.assertIn("elementos finitos", notice)

    def test_theory_and_pedagogy_are_substantive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(s["paragraphs"]) >= 3 for s in sections))
        self.assertTrue(all(len(s["key_points"]) >= 4 for s in sections))
        self.assertGreaterEqual(len(self.unit["glossary"]), 22)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)

    def test_guided_activity_is_synthetic_and_scaffolded(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 7)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 12)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintética", text)
        self.assertIn("datos reservados", text)
        self.assertIn("no introduzcas relajación", text)

    def test_sources_are_traceable(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(s.get("verification_status") == "verified_directly_2026-08-24" for s in sources))
        urls = {s["url"] for s in sources}
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/26087063/", urls)
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC6501667/", urls)
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC8518191/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/36801779/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/41698563/", urls)

    def test_clinical_and_curricular_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no se presenta como propiedad universal", notice)
        self.assertIn("respuesta dependiente del tiempo", purpose)
        self.assertIn("reservados para u4", purpose)


# Final user-authored trigger after reviewed public-site synchronization.
if __name__ == "__main__":
    unittest.main()
