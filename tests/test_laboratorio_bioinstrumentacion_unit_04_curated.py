from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "laboratorio-bioinstrumentacion" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "laboratorio-bioinstrumentacion" / "unit-04.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class LaboratorioBioinstrumentacionUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "laboratorio-bioinstrumentacion")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed_and_acquisition_concepts_exist(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        for concept in (
            "filtro antialias",
            "frecuencia de nyquist",
            "aliasing",
            "cuantización",
            "enob",
            "clipping",
            "fase cero",
            "dato crudo",
        ):
            self.assertIn(concept, self.text)

    def test_theory_is_substantive_and_respects_signal_chain_order(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        self.assertIn("debe preceder al muestreador o adc", theory)
        self.assertIn("no puede recuperar una componente que ya se aliasó", theory)
        self.assertIn("no puede reconstruir una amplitud que se perdió por clipping", theory)
        self.assertIn("no representa lo que un sistema en tiempo real", theory)
        self.assertIn("no 16 bits garantizados", theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        for equation in (
            "f_N=\\frac{f_s}{2}",
            "f_{alias}=|f_{in}-k f_s|",
            "q=\\frac{V_{max}-V_{min}}{2^N}",
            "|e_q|\\leq\\frac{q}{2}",
            "\\mathrm{SNR}_{ideal}\\approx 6.02N+1.76\\ \\mathrm{dB}",
            "\\mathrm{ENOB}=\\frac{\\mathrm{SINAD}-1.76}{6.02}",
        ):
            self.assertIn(equation, equations)

    def test_guided_activities_are_synthetic_progressive_and_reproducible(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertGreaterEqual(len(activities), 3)
        self.assertGreaterEqual(len(activities[0]["problems"]), 10)
        self.assertGreaterEqual(len(activities[1]["problems"]), 15)
        self.assertGreaterEqual(len(activities[1]["deliverables"]), 10)
        self.assertGreaterEqual(len(activities[1]["checking_criteria"]), 10)
        self.assertGreaterEqual(len(activities[2]["tasks"]), 9)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("señales matemáticas", activity_text)
        self.assertIn("no conectes personas", activity_text)
        self.assertIn("antes–después", activity_text)
        self.assertIn("datos crudos", activity_text)
        self.assertIn("fase cero", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 25)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "filtro antialias",
            "frecuencia de nyquist",
            "aliasing",
            "adc",
            "cuantización",
            "sinad",
            "enob",
            "procedencia de procesamiento",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_cover_adc_and_filtering(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://www.analog.com/media/en/training-seminars/tutorials/mt-002.pdf",
            "https://www.analog.com/mt-004",
            "https://www.ti.com/video/series/precision-labs/ti-precision-labs-analog-to-digital-converters-adcs.html",
            "https://pubmed.ncbi.nlm.nih.gov/25128257/",
            "https://pubmed.ncbi.nlm.nih.gov/20851409/",
        ):
            self.assertIn(url, urls)

    def test_human_clinical_and_regulatory_boundary_is_explicit(self) -> None:
        purpose = self.unit["purpose"].casefold()
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("no autoriza conexión a personas", purpose)
        self.assertIn("no autorizan conexión de electrodos o prototipos a personas", notice)
        self.assertIn("red eléctrica", notice)
        self.assertIn("no constituye seguridad eléctrica", notice)
        self.assertIn("validación fisiológica o clínica", notice)
        self.assertIn("conformidad iec 60601", notice)
        self.assertIn("revisión disciplinar humana permanece pendiente", notice)


if __name__ == "__main__":
    unittest.main()
