from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "electronica" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "electronica" / "unit-06.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"
OLD_GENERIC_SNR = r"\mathrm{SNR}_{dB}=10\log_{10}\left(\frac{P_s}{P_n}\right)"


class ElectronicaUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "electronica")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_irrelevant_snr_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertNotIn(OLD_GENERIC_SNR, equations)
        for concept in (
            "erc",
            "drc",
            "footprint",
            "camino de retorno",
            "desacoplo",
            "ground lead",
            "bring-up",
            "pre-compliance",
        ):
            self.assertIn(concept, self.text)

    def test_u6_boundary_is_physical_implementation_and_verification(self) -> None:
        purpose = self.unit["purpose"].casefold()
        self.assertIn("implementación física verificable", purpose)
        self.assertIn("esquemático", purpose)
        self.assertIn("pcb", purpose)
        self.assertIn("instrumentación", purpose)
        self.assertIn("diagnóstico de fallos", purpose)
        self.assertNotIn("i2c", purpose)
        self.assertNotIn("uart", purpose)

    def test_theory_is_substantive_and_has_measurement_limits(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(
            text
            for section in sections
            for text in (*section["paragraphs"], *section["key_points"])
        ).casefold()
        for phrase in (
            "el layout forma parte del circuito",
            "no es 'separar siempre tierra analógica y digital'",
            "el instrumento modifica el circuito que mide",
            "nunca se elimina la tierra de protección del osciloscopio",
            "diagnosticar no es sustituir componentes al azar",
            "no sustituye pruebas normativas",
        ):
            self.assertIn(phrase, theory)

    def test_core_equations_are_present_and_relevant(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        expected = {
            r"v_L=L\frac{di}{dt}",
            r"Z_C=\frac{1}{j\omega C}",
            r"\Delta V\approx I\,R",
            r"P_{loss}\approx I^2R",
            r"Z_{probe}(\omega)\approx R_p\parallel\frac{1}{j\omega C_p}",
            r"V_m=V_s\frac{Z_{in}}{Z_s+Z_{in}}",
            r"f_0\approx\frac{1}{2\pi\sqrt{LC}}",
        }
        self.assertTrue(expected.issubset(equations))

    def test_guided_activities_are_progressive_and_safe(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertTrue(all(len(item["instructions"]) >= 5 for item in activities))
        self.assertTrue(all(len(item["problems"]) >= 12 for item in activities))
        self.assertTrue(all(len(item["checking_criteria"]) >= 6 for item in activities))
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        for concept in (
            "matriz requisito→componente→net→test point",
            "camino de corriente de ida y retorno",
            "fallos sintéticos",
            "stop criteria",
            "prueba discriminante",
            "near-field",
        ):
            self.assertIn(concept, activity_text)
        self.assertIn("no se conectan prototipos a personas", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 30)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        expected_terms = {
            "esquemático",
            "footprint",
            "erc",
            "drc",
            "stack-up",
            "camino de retorno",
            "desacoplo",
            "pds",
            "test point",
            "loading",
            "ground lead",
            "bring-up",
            "fault injection",
            "prueba discriminante",
            "emc",
            "pre-compliance",
        }
        self.assertTrue(expected_terms.issubset(terms))

    def test_sources_are_traceable_and_directly_verified(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 11)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        expected = {
            "https://docs.kicad.org/9.0/en/pcbnew/pcbnew.html",
            "https://docs.kicad.org/9.0/en/cli/cli.html",
            "https://www.electronics.org/ipc-document-revision-table",
            "https://www.analog.com/en/resources/app-notes/an-1142.html",
            "https://www.tek.com/en/documents/whitepaper/abcs-probes-primer",
            "https://webstore.iec.ch/en/publication/67497",
            "https://webstore.iec.ch/en/publication/67554",
        }
        self.assertTrue(expected.issubset(urls))

    def test_safety_and_regulatory_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("certificación ipc", notice)
        self.assertIn("conformidad iec 60601", notice)
        self.assertIn("sin conexión a personas", notice)
        self.assertIn("nunca se debe derrotar la protective earth", notice)
        self.assertIn("pre-compliance emc", notice)
        self.assertIn("no para declarar conformidad", notice)


# Final user-authored trigger after Electronics publication metadata synchronization.
if __name__ == "__main__":
    unittest.main()
