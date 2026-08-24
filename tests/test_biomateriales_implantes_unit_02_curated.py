from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomateriales-implantes" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "biomateriales-implantes" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomaterialesImplantesUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomateriales-implantes")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed_and_scope_is_material_selection(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "estructura–procesamiento–propiedad–entorno",
            "matriz multicriterio",
            "acero inoxidable",
            "ti-6al-4v",
            "alúmina",
            "zirconia",
            "uhmwpe",
            "caracterización química",
        ):
            self.assertIn(concept, text)
        self.assertIn("u3–u6", text)

    def test_theory_is_substantive_and_preserves_later_unit_boundaries(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "rigidez no es sinónimo de resistencia",
            "composición nominal",
            "defectos",
            "anisotropía",
            "extraíbles",
            "lixiviables",
        ):
            self.assertIn(concept, theory)
        self.assertIn("u4", theory)
        self.assertIn("u3", SOURCE.read_text(encoding="utf-8").casefold())
        self.assertIn("u6", SOURCE.read_text(encoding="utf-8").casefold())

    def test_core_equations_are_present_and_bounded(self) -> None:
        equations = {
            equation["latex"]: equation["meaning"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("E=\\frac{\\sigma}{\\varepsilon}", equations)
        self.assertIn("S_j=\\sum_{i=1}^{n} w_i x_{ij}", equations)
        self.assertIn("elástico lineal", equations["E=\\frac{\\sigma}{\\varepsilon}"].casefold())
        self.assertIn("sensibilidad", equations["S_j=\\sum_{i=1}^{n} w_i x_{ij}"].casefold())

    def test_guided_activities_are_progressive_synthetic_and_decision_bounded(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        first = activities[0]
        self.assertGreaterEqual(len(first["instructions"]), 6)
        self.assertGreaterEqual(len(first["problems"]), 12)
        self.assertGreaterEqual(len(first["deliverables"]), 8)
        self.assertGreaterEqual(len(first["checking_criteria"]), 10)
        text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintético", text)
        self.assertIn("apoyo reducido", text)
        self.assertIn("reto de transferencia", text)
        self.assertIn("no recomienda", text)
        self.assertIn("sensibilidad", text)

    def test_learning_support_is_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 26)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 4)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "módulo de young",
            "tenacidad",
            "anisotropía",
            "pasividad",
            "extraíble",
            "lixiviable",
            "matriz multicriterio",
            "frontera de evidencia",
        ):
            self.assertIn(term, terms)

    def test_sources_are_current_traceable_and_cover_all_material_families(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://www.iso.org/standard/83775.html",
            "https://www.iso.org/standard/79626.html",
            "https://www.iso.org/standard/79956.html",
            "https://www.iso.org/standard/69906.html",
            "https://www.iso.org/standard/62373.html",
            "https://www.iso.org/standard/86079.html",
            "https://www.iso.org/standard/64750.html",
            "https://pubmed.ncbi.nlm.nih.gov/30861312/",
            "https://pubmed.ncbi.nlm.nih.gov/23746930/",
            "https://pubmed.ncbi.nlm.nih.gov/26386167/",
        ):
            self.assertIn(url, urls)
        titles = " ".join(item["title"] for item in sources)
        self.assertNotIn("ISO 5832-1:2016", titles)
        self.assertNotIn("ISO 5834-2:2019", titles)
        self.assertIn("ISO 5832-1:2024", titles)
        self.assertIn("ISO 5834-2:2025", titles)

    def test_clinical_and_regulatory_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no constituye", notice)
        self.assertIn("no confundir", purpose)
        self.assertIn("selección real requiere", notice)


# Final user-authored trigger after public synchronization.
if __name__ == "__main__":
    unittest.main()
