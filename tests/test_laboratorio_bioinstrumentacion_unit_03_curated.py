from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "laboratorio-bioinstrumentacion" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "laboratorio-bioinstrumentacion" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class LaboratorioBioinstrumentacionUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "laboratorio-bioinstrumentacion")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed_and_core_frontend_concepts_exist(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        for concept in (
            "señal diferencial",
            "modo común",
            "cmrr total",
            "desbalance de impedancias",
            "corriente de polarización",
            "headroom",
            "ruido referido a la entrada",
        ):
            self.assertIn(concept, self.text)

    def test_theory_is_substantive_and_keeps_system_boundaries(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        self.assertIn("no es automáticamente el cmrr de un sistema", theory)
        self.assertIn("dependencia de frecuencia", theory)
        self.assertIn("diamond plot", theory)
        self.assertIn("interferencia determinista", theory)
        self.assertIn("la cadena completa", theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        for equation in (
            "v_d=v_+-v_-",
            "v_{cm}=\\frac{v_++v_-}{2}",
            "v_o=V_{REF}+A_dv_d+A_{cm}v_{cm}",
            "\\mathrm{CMRR}_{dB}=20\\log_{10}\\left|\\frac{A_d}{A_{cm}}\\right|",
            "v_{err}\\approx I_B\\,\\Delta R_s",
            "G=1+\\frac{50\\,\\mathrm{k}\\Omega}{R_G}",
            "e_{n,rms}\\approx e_n\\sqrt{B}",
        ):
            self.assertIn(equation, equations)

    def test_guided_activities_are_synthetic_and_progressive(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertGreaterEqual(len(activities), 3)
        self.assertGreaterEqual(len(activities[0]["problems"]), 9)
        self.assertGreaterEqual(len(activities[1]["problems"]), 14)
        self.assertGreaterEqual(len(activities[1]["deliverables"]), 10)
        self.assertGreaterEqual(len(activities[1]["checking_criteria"]), 10)
        self.assertGreaterEqual(len(activities[2]["tasks"]), 8)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("no conectes electrodos", activity_text)
        self.assertIn("fuentes sintéticas", activity_text)
        self.assertIn("antes–después", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 25)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "señal diferencial",
            "modo común",
            "amplificador de instrumentación",
            "cmrr",
            "cmrr total",
            "rango de modo común de entrada",
            "diamond plot",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_include_primary_electronics(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://www.ti.com/product/INA128",
            "https://www.ti.com/lit/ds/symlink/ina128.pdf",
            "https://www.analog.com/en/resources/app-notes/an-1401.html",
            "https://www.ti.com/lit/an/sbaa188/sbaa188.pdf",
            "https://pubmed.ncbi.nlm.nih.gov/41129458/",
            "https://pubmed.ncbi.nlm.nih.gov/30640594/",
        ):
            self.assertIn(url, urls)

    def test_human_and_regulatory_boundary_is_explicit(self) -> None:
        purpose = self.unit["purpose"].casefold()
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("no autoriza electrodos sobre personas", purpose)
        self.assertIn("no autoriza colocar electrodos sobre personas", notice)
        self.assertIn("trabajar con red eléctrica", notice)
        self.assertIn("no constituye seguridad eléctrica", notice)
        self.assertIn("validación ecg/emg clínica", notice)
        self.assertIn("conformidad iec 60601-1", notice)


if __name__ == "__main__":
    unittest.main()
