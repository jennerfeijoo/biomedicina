from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "electronica" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "electronica" / "unit-05.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ElectronicaUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "electronica")
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_irrelevant_snr_are_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("snr_{db}", text)
        for concept in ("vih", "vil", "voh", "vol", "metastabilidad", "i2c", "spi", "uart"):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_respects_u6_boundary(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "márgenes de ruido",
            "schmitt",
            "setup",
            "hold",
            "open-drain",
            "cpol",
            "cpha",
            "diagrama temporal",
        ):
            self.assertIn(concept, theory)
        self.assertIn("u6", theory)
        self.assertIn("pcb", theory)

    def test_core_equations_are_present_and_conditioned(self) -> None:
        equations = {
            equation["latex"]: equation["meaning"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("NM_H=V_{OH(min)}-V_{IH(min)}", equations)
        self.assertIn("NM_L=V_{IL(max)}-V_{OL(max)}", equations)
        self.assertIn("R_{P(min)}=(V_{CC}-V_{OL(max)})/I_{OL}", equations)
        self.assertIn("t_r=0.8473 R_P C_b", equations)
        self.assertIn("R_{P(max)}=t_{r(max)}/(0.8473 C_b)", equations)
        self.assertIn("T_{bit}=1/baud", equations)
        self.assertIn("valores garantizados", equations["NM_H=V_{OH(min)}-V_{IH(min)}"])

    def test_guided_activities_are_progressive_synthetic_and_scaffolded(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertTrue(all(len(a["instructions"]) >= 6 for a in activities))
        self.assertTrue(all(len(a["problems"]) >= 8 for a in activities))
        self.assertTrue(all(len(a["deliverables"]) >= 5 for a in activities))
        self.assertTrue(all(len(a["checking_criteria"]) >= 8 for a in activities))
        text = json.dumps(activities, ensure_ascii=False).casefold()
        for concept in ("sintét", "pull-up", "metastabilidad", "cpol", "uart", "no conectes hardware"):
            self.assertIn(concept, text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 6)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "margen de ruido",
            "schmitt trigger",
            "metastabilidad",
            "i2c",
            "spi",
            "uart",
            "traductor de nivel",
        ):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_directly_verified(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://www.nxp.com/docs/en/user-guide/UM10204.pdf", urls)
        self.assertIn("https://www.ti.com/lit/an/slva689/slva689.pdf", urls)
        self.assertIn("https://www.analog.com/en/resources/analog-dialogue/articles/introduction-to-spi-interface.html", urls)
        self.assertIn("https://www.intel.com/content/www/us/en/docs/programmable/683068/18-1/metastability-analysis.html", urls)

    def test_editorial_and_clinical_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("validación clínica", notice)
        self.assertIn("equipos médicos en servicio", notice)
        self.assertIn("u6", purpose)
        self.assertIn("pcb", purpose)


if __name__ == "__main__":
    unittest.main()
