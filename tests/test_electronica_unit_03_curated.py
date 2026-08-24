from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "electronica" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "electronica" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ElectronicaUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "electronica")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in ("amplificador operacional", "noise gain", "gbw", "slew rate", "cmrr", "amplificador de instrumentación"):
            self.assertIn(concept, text)

    def test_theory_has_clear_u3_u4_boundary(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertIn("unidad 4", text)
        self.assertIn("filtros activos", text)
        self.assertIn("osciladores", text)
        self.assertIn("cortocircuito virtual", text)
        self.assertIn("diamond plot", text)
        self.assertIn("ruido 1/f", text)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn(r"\frac{V_o}{V_i}=-\frac{R_F}{R_G}", equations)
        self.assertIn(r"f_{CL}\approx\frac{GBW}{NG}", equations)
        self.assertIn(r"CMRR_{dB}=20\log_{10}\left(\frac{A_d}{A_{CM}}\right)", equations)
        self.assertIn(r"e_{n,R}=\sqrt{4kTRB}", equations)

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 6)
        self.assertGreaterEqual(len(activity["problems"]), 16)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintética", text)
        self.assertIn("no conectes", text)
        self.assertIn("ina128", text)
        self.assertIn("cmrr", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("amplificador operacional", "noise gain", "gbw", "slew rate", "cmrr", "amplificador de instrumentación"):
            self.assertIn(term, terms)

    def test_sources_are_directly_traceable(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://www.analog.com/media/en/training-seminars/tutorials/mt-032.pdf", urls)
        self.assertIn("https://www.analog.com/mt-033", urls)
        self.assertIn("https://www.ti.com/lit/ds/symlink/ina128.pdf", urls)
        self.assertIn("https://www.analog.com/en/resources/app-notes/an-1401.html", urls)

    def test_safety_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no autorizan conectar circuitos", notice)
        self.assertIn("equipos médicos", notice)
        self.assertIn("revisión humana interna y externa permanece pendiente", notice)
        self.assertIn("unidad 4", purpose)


if __name__ == "__main__":
    unittest.main()
