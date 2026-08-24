from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomateriales-implantes" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "biomateriales-implantes" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomaterialesImplantesUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomateriales-implantes")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed_and_scope_is_fixation(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "estabilidad primaria",
            "estabilidad secundaria",
            "micromovimiento",
            "press-fit",
            "osteointegración",
            "ongrowth",
            "ingrowth",
            "hidroxiapatita",
            "pmma",
            "push-out",
            "pull-out",
        ):
            self.assertIn(concept, text)
        self.assertIn("u4", text)
        self.assertIn("desgaste, corrosión", text)

    def test_theory_is_substantive_and_preserves_course_boundaries(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "ajuste por interferencia",
            "contacto hueso–implante",
            "recubrimientos de hidroxiapatita",
            "fijación cementada",
            "fijación no cementada",
            "modo de fallo",
            "frontera de inferencia",
        ):
            self.assertIn(concept, theory)
        self.assertIn("u4 aborda", theory)

    def test_core_equations_are_present_and_bounded(self) -> None:
        equations = {
            equation["latex"]: equation["meaning"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("k_{int}=\\frac{F}{\\delta}", equations)
        self.assertIn("BIC=\\frac{L_{hueso-contacto}}{L_{implante-evaluable}}\\times100\\%", equations)
        self.assertIn("\\Delta_{rel}=\\frac{x_2-x_1}{x_1}\\times 100\\%", equations)
        self.assertIn("no es una constante", equations["k_{int}=\\frac{F}{\\delta}"].casefold())
        self.assertIn("no equivale por sí solo", equations["BIC=\\frac{L_{hueso-contacto}}{L_{implante-evaluable}}\\times100\\%"].casefold())

    def test_guided_activities_are_progressive_synthetic_and_safe(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        first = activities[0]
        self.assertGreaterEqual(len(first["instructions"]), 6)
        self.assertGreaterEqual(len(first["problems"]), 12)
        self.assertGreaterEqual(len(first["deliverables"]), 8)
        self.assertGreaterEqual(len(first["checking_criteria"]), 10)
        text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintético", text)
        self.assertIn("no uses historias clínicas", text)
        self.assertIn("apoyo reducido", text)
        self.assertIn("reto de transferencia", text)
        self.assertIn("no recomiende ningún implante real", text)

    def test_learning_support_is_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 28)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "osteointegración",
            "estabilidad primaria",
            "micromovimiento",
            "bic",
            "pmma",
            "interdigitación",
            "modo de fallo",
            "frontera de inferencia",
        ):
            self.assertIn(term, terms)

    def test_sources_are_current_traceable_and_version_aware(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://www.iso.org/standard/64617.html",
            "https://www.iso.org/standard/64619.html",
            "https://www.iso.org/standard/30980.html",
            "https://www.iso.org/es/contents/data/standard/08/86/88639.html",
            "https://pubmed.ncbi.nlm.nih.gov/6352924/",
            "https://pubmed.ncbi.nlm.nih.gov/7246093/",
            "https://pubmed.ncbi.nlm.nih.gov/39816715/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC13199635/",
        ):
            self.assertIn(url, urls)
        titles = " ".join(item["title"] for item in sources)
        self.assertIn("ISO 5833:2002", titles)
        self.assertIn("ISO/FDIS 5833", titles)
        source_text = json.dumps(sources, ensure_ascii=False).casefold()
        self.assertIn("fase fdis", source_text)
        self.assertIn("no se presenta como norma ya publicada", source_text)

    def test_editorial_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no deben usarse como especificaciones de productos reales", notice)
        self.assertIn("sin confundir", purpose)
        self.assertIn("u4", notice)


# Final user-authored trigger after publication metadata synchronization.
if __name__ == "__main__":
    unittest.main()
