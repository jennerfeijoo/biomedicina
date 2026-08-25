from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "electrofisica-electromecanica" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "electrofisica-electromecanica" / "unit-04.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ElectrofisicaElectromecanicaUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "electrofisica-electromecanica")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_unrelated_snr_equation_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("\\mathrm{snr}", self.text)
        self.assertNotIn("cadena física de transducción, acondicionamiento, adquisición", self.text)

    def test_theory_is_specific_to_transducers_and_metrology(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        for concept in (
            "mensurando", "sensibilidad", "calibración", "trazabilidad metrológica",
            "piezoelectricidad", "d33", "galga", "wheatstone", "capacitivo",
            "lvdt", "histéresis", "incertidumbre",
        ):
            self.assertIn(concept, self.text)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        for equation in (
            "S=\\frac{\\Delta y}{\\Delta x}",
            "Q=d_{33}F",
            "\\varepsilon=\\frac{\\Delta L}{L_0}",
            "GF=\\frac{\\Delta R/R}{\\varepsilon}",
            "C=\\varepsilon\\frac{A}{d}",
            "E_{out}=E_1-E_2",
            "V_{demod}\\approx Kx",
        ):
            self.assertIn(equation, equations)

    def test_piezoelectric_scope_is_correct(self) -> None:
        theory = " ".join(
            p for section in self.unit["theory_sections"] for p in section["paragraphs"]
        ).casefold()
        self.assertIn("efecto directo", theory)
        self.assertIn("efecto inverso", theory)
        self.assertIn("fuente de carga", theory)
        self.assertIn("la tensión observada depende del circuito conectado", theory)
        self.assertIn("u5", theory)

    def test_strain_bridge_and_lvdt_are_not_overgeneralized(self) -> None:
        self.assertIn("cuarto de puente", self.text)
        self.assertIn("medio puente", self.text)
        self.assertIn("puente completo", self.text)
        self.assertIn("temperatura", self.text)
        self.assertIn("punto nulo", self.text)
        self.assertIn("demodulación", self.text)
        self.assertIn("rango lineal", self.text)

    def test_guided_activity_is_scaffolded_reproducible_and_safe(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 8)
        self.assertGreaterEqual(len(activity["problems"]), 18)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 18)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        for phrase in (
            "datos sintéticos", "piezoeléctrico", "wheatstone", "capacitivo", "lvdt",
            "histéresis", "incertidumbre", "no se conectan personas",
        ):
            self.assertIn(phrase, text)

    def test_learning_scaffolds_are_specific_and_sufficient(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 35)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 16)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "transductor", "mensurando", "sensibilidad", "calibración",
            "piezoelectricidad", "galga extensométrica", "factor de galga",
            "puente de wheatstone", "sensor capacitivo", "lvdt",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_cover_core_and_biomedical_context(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 15)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://www.ni.com/en/shop/data-acquisition/sensor-fundamentals/measuring-strain-with-strain-gages.html",
            "https://openstax.org/books/university-physics-volume-2/pages/8-1-capacitors-and-capacitance",
            "https://www.te.com/es/products/sensors/position-sensors/resources/lvdt-tutorial.html",
            "https://jcgm.bipm.org/vim/en/4.12.html",
            "https://jcgm.bipm.org/vim/en/2.39.html",
            "https://www.nist.gov/metrology/metrological-traceability",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC9041315/",
            "https://pubmed.ncbi.nlm.nih.gov/30294947/",
            "https://pubmed.ncbi.nlm.nih.gov/35262335/",
        ):
            self.assertIn(url, urls)

    def test_course_and_professional_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no constituyen revisión disciplinar externa",
            "validación clínica", "validación de un dispositivo",
            "seguridad eléctrica", "compatibilidad electromagnética",
            "no autorizan conectar sensores", "personas",
            "u5 se reserva para actuadores y control",
            "u6 para seguridad",
        ):
            self.assertIn(phrase, notice)
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituyen validación de un sensor médico", purpose)


if __name__ == "__main__":
    unittest.main()
