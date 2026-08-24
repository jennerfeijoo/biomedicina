from __future__ import annotations

# Final user-authored trigger after generated public-site synchronization.
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomecanica" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "biomecanica" / "unit-04.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomecanicaUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomecanica")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in ("tensión mecánica", "viscoelasticidad", "cartílago articular", "tendón"):
            self.assertIn(concept, text)

    def test_theory_is_tissue_mechanics_and_substantive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "rigidez estructural",
            "anisotropía",
            "hueso trabecular",
            "fluido intersticial",
            "creep",
            "relajación de tensión",
            "histéresis",
            "preacondicionamiento",
        ):
            self.assertIn(concept, theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn(r"\sigma=\frac{F}{A_0}", equations)
        self.assertIn(r"\varepsilon=\frac{L-L_0}{L_0}", equations)
        self.assertIn(r"U=\int \sigma\,d\varepsilon", equations)
        self.assertIn(r"\sigma_{total}=\sigma_{solid}+\sigma_{fluid}", equations)

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 7)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        activity_text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintético", activity_text)
        self.assertIn("no recolectes muestras ni datos de personas", activity_text)
        self.assertIn("sensibilidad", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 18)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 8)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "tensión mecánica",
            "módulo elástico",
            "anisotropía",
            "viscoelasticidad",
            "modelo bipásico",
            "preacondicionamiento",
        ):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_current_enough_for_modeling_context(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        verified = [item for item in sources if item.get("verification_status") == "verified_directly"]
        self.assertEqual(len(verified), len(sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/7382457/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/18202585/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/21925835/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/42013604/", urls)

    def test_clinical_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no autorizan diagnóstico", notice)
        self.assertIn("predicción individual de lesión", notice)
        self.assertIn("decisión clínica", purpose)


if __name__ == "__main__":
    unittest.main()
