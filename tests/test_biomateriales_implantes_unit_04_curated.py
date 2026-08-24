from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomateriales-implantes" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "biomateriales-implantes" / "unit-04.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomaterialesImplantesUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomateriales-implantes")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed_and_scope_is_degradation(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "tribología",
            "desgaste adhesivo",
            "desgaste abrasivo",
            "tribocorrosión",
            "pasivación",
            "fretting",
            "partícula de desgaste",
            "fatiga",
            "curva s–n",
            "corrosión-fatiga",
        ):
            self.assertIn(concept, text)
        self.assertIn("u5", text)
        self.assertIn("u6", text)

    def test_theory_is_substantive_and_preserves_course_boundaries(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "tercer cuerpo",
            "repasivación",
            "acoplamientos galvánicos",
            "fretting-corrosión",
            "osteólisis periprotésica",
            "razón de carga",
            "regla lineal de miner",
        ):
            self.assertIn(concept, theory)
        self.assertIn("u5 permitirá", theory)
        self.assertIn("u6 cómo se incorpora", theory)

    def test_core_equations_are_present_and_bounded(self) -> None:
        equations = {
            equation["latex"]: equation["meaning"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        for latex in (
            "\\mu=\\frac{F_t}{F_n}",
            "V=k\\frac{Ws}{H}",
            "m=\\frac{MIt}{nF}",
            "\\sigma_a=\\frac{\\sigma_{max}-\\sigma_{min}}{2}",
            "D=\\sum_i\\frac{n_i}{N_i}",
        ):
            self.assertIn(latex, equations)
        self.assertIn("depende del sistema", equations["V=k\\frac{Ws}{H}"].casefold())
        self.assertIn("ignora efectos de secuencia", equations["D=\\sum_i\\frac{n_i}{N_i}"].casefold())

    def test_guided_activities_are_progressive_synthetic_and_safe(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        first = activities[0]
        self.assertGreaterEqual(len(first["instructions"]), 8)
        self.assertGreaterEqual(len(first["problems"]), 12)
        self.assertGreaterEqual(len(first["deliverables"]), 8)
        self.assertGreaterEqual(len(first["checking_criteria"]), 10)
        text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintético", text)
        self.assertIn("datos de pacientes", text)
        self.assertIn("apoyo reducido", text)
        self.assertIn("reto de transferencia", text)
        self.assertIn("no se formula recomendación clínica", text)

    def test_learning_support_is_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 28)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "tribología",
            "tribocorrosión",
            "fretting-corrosión",
            "partícula de desgaste",
            "fatiga",
            "curva s–n",
            "regla de miner",
        ):
            self.assertIn(term, terms)

    def test_sources_are_current_traceable_and_version_aware(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 12)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://www.iso.org/standard/63073.html",
            "https://www.iso.org/standard/91365.html",
            "https://www.iso.org/standard/68937.html",
            "https://www.iso.org/standard/42769.html",
            "https://www.iso.org/standard/51186.html",
            "https://www.iso.org/standard/87769.html",
            "https://www.iso.org/standard/61997.html",
            "https://pubmed.ncbi.nlm.nih.gov/37261398/",
            "https://pubmed.ncbi.nlm.nih.gov/29529933/",
            "https://pubmed.ncbi.nlm.nih.gov/36550970/",
            "https://pubmed.ncbi.nlm.nih.gov/21951920/",
            "https://pubmed.ncbi.nlm.nih.gov/41861698/",
        ):
            self.assertIn(url, urls)
        source_text = json.dumps(sources, ensure_ascii=False).casefold()
        self.assertIn("iso 14242-1:2014", source_text)
        self.assertIn("iso/wd 14242-1", source_text)
        self.assertIn("no se trata como norma publicada", source_text)
        self.assertIn("iso 7206-6:2013", source_text)
        self.assertIn("iso/dis 7206-6", source_text)
        self.assertIn("no se presenta como norma ya publicada", source_text)
        self.assertIn("no predice desempeño in vivo", source_text)

    def test_editorial_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("datos sintéticos", notice)
        self.assertIn("no incluyen instrucciones", notice)
        self.assertIn("wd/dis", notice)
        self.assertIn("sin convertir resultados de laboratorio", purpose)


if __name__ == "__main__":
    unittest.main()
