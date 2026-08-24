from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "fundamentos-biomecanica" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "fundamentos-biomecanica" / "unit-05.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class FundamentosBiomecanicaUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "fundamentos-biomecanica")
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "antropometría",
            "centro de masa",
            "centro articular",
            "brazo de momento",
            "momento de inercia",
            "escalado geométrico",
            "sensibilidad",
        ):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_introductory(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory_words = sum(
            len(paragraph.split())
            for section in sections
            for paragraph in section["paragraphs"]
        )
        self.assertGreaterEqual(theory_words, 1200)
        theory = " ".join(
            paragraph for section in sections for paragraph in section["paragraphs"]
        ).casefold()
        self.assertIn("bsip", theory)
        self.assertIn("tabla antropométrica", theory)
        self.assertIn("sistema de coordenadas", theory)
        self.assertIn("línea de acción", theory)
        self.assertIn("no para realizar una dinámica inversa clínica completa", theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("I_{COM}=m k^2", equations)
        self.assertIn("I_O=I_{COM}+m d^2", equations)
        self.assertIn(
            "\\mathbf r_{COM}=\\frac{\\sum_{i=1}^{n}m_i\\mathbf r_i}{\\sum_{i=1}^{n}m_i}",
            equations,
        )
        self.assertIn("M=F d_\\perp", equations)

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 10)
        self.assertGreaterEqual(len(activity["deliverables"]), 6)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 8)
        activity_text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintético", activity_text)
        self.assertIn("no midas ni registres datos de personas", activity_text)
        self.assertIn("centro articular", activity_text)
        self.assertIn("sensibilidad", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 4)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 8)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "bsip",
            "centro de masa global",
            "centro articular",
            "brazo de momento",
            "escalado geométrico",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_methodologically_relevant(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        verified = [item for item in sources if item.get("verification_status") == "verified_directly"]
        self.assertGreaterEqual(len(verified), 8)
        urls = {item["url"] for item in sources}
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/8872282/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/16616757/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/16584737/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/11934426/", urls)
        self.assertIn(
            "https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53089158/How+Scaling+Works",
            urls,
        )

    def test_scope_boundary_is_explicit(self) -> None:
        purpose = self.unit["purpose"].casefold()
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("sin tratar tablas poblacionales como medidas individuales exactas", purpose)
        self.assertIn("no constituyen revisión disciplinar externa", notice)
        self.assertIn("no requieren medir personas", notice)
        self.assertIn("diagnóstico", notice)
        self.assertIn("prescripción", notice)
        self.assertIn("estimación individual de fuerzas musculares", notice)


if __name__ == "__main__":
    unittest.main()

# Final user-authored verification trigger after publication metadata synchronization.
