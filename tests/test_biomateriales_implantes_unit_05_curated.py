from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomateriales-implantes" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "biomateriales-implantes" / "unit-05.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"
# Final validation trigger after descriptor synchronization.


class BiomaterialesImplantesUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomateriales-implantes")
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed_and_scope_is_specific_implants(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "stress shielding",
            "osseointegración",
            "hemocompatibilidad",
            "trombogenicidad",
            "malla quirúrgica",
            "prótesis mamaria",
            "transferibilidad",
        ):
            self.assertIn(concept, text)
        self.assertIn("u6", text)

    def test_theory_is_substantive_and_comparative(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "transferencia de carga",
            "estabilidad primaria",
            "soporte radial",
            "número de reynolds",
            "respuesta a cuerpo extraño",
            "densidad areal",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no predice desempeño in vivo", theory)
        self.assertIn("no es una propiedad absoluta", theory)

    def test_equations_are_present_and_bounded(self) -> None:
        equations = {
            equation["latex"]: equation["meaning"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        for latex in (
            "\\sigma=\\frac{F}{A}",
            "p=\\frac{F}{A_c}",
            "M=F d_\\perp",
            "Re=\\frac{\\rho v D}{\\mu}",
            "m_A=\\frac{m}{A}",
        ):
            self.assertIn(latex, equations)
        self.assertIn("no constituye una métrica de trombogenicidad", equations["Re=\\frac{\\rho v D}{\\mu}"].casefold())
        self.assertIn("insuficiente", equations["m_A=\\frac{m}{A}"].casefold())

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
        self.assertIn("no uses datos de pacientes", text)
        self.assertIn("apoyo reducido", text)
        self.assertIn("reto de transferencia", text)
        self.assertIn("no se formulan decisiones clínicas", text)

    def test_learning_support_is_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "stress shielding",
            "implante dental endoóseo",
            "hemocompatibilidad",
            "malla quirúrgica",
            "respuesta a cuerpo extraño",
            "transferibilidad",
        ):
            self.assertIn(term, terms)

    def test_sources_are_traceable_current_and_version_aware(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 12)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://www.iso.org/standard/61997.html",
            "https://www.iso.org/standard/91565.html",
            "https://www.iso.org/standard/66925.html",
            "https://www.iso.org/standard/77033.html",
            "https://www.iso.org/standard/88490.html",
            "https://www.iso.org/standard/82020.html",
            "https://pubmed.ncbi.nlm.nih.gov/25579990/",
            "https://pubmed.ncbi.nlm.nih.gov/32090904/",
            "https://pubmed.ncbi.nlm.nih.gov/36186971/",
            "https://pubmed.ncbi.nlm.nih.gov/25919260/",
            "https://pubmed.ncbi.nlm.nih.gov/28938360/",
        ):
            self.assertIn(url, urls)
        source_text = json.dumps(sources, ensure_ascii=False).casefold()
        self.assertIn("iso 14801:2016", source_text)
        self.assertIn("en desarrollo", source_text)
        self.assertIn("no se presenta como norma publicada", source_text)
        self.assertIn("iso 14607:2024", source_text)

    def test_clinical_and_regulatory_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no constituye", notice)
        self.assertIn("evaluación regulatoria", notice)
        self.assertIn("datos sintéticos", notice)
        self.assertIn("no convertir", purpose)
        self.assertIn("recomendación clínica", purpose)


if __name__ == "__main__":
    unittest.main()
