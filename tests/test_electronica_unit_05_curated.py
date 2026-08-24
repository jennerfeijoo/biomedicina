from __future__ import annotations

# Final user-authored validation trigger after curriculum/publication synchronization.

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

    def test_generic_template_is_removed_and_scope_is_digital(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in ("vih", "vil", "metastabilidad", "i²c", "spi", "uart", "debounce"):
            self.assertIn(concept, text)
        self.assertIn("u6", self.unit["purpose"].casefold())

    def test_theory_is_substantive_and_separates_layers(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(
            [p for section in sections for p in section["paragraphs"]]
            + [point for section in sections for point in section["key_points"]]
        ).casefold()
        for concept in (
            "márgenes de ruido",
            "lógica combinacional",
            "setup",
            "hold",
            "sincronizador",
            "open-drain",
            "cpol",
            "cpha",
            "framing error",
            "analizador lógico",
        ):
            self.assertIn(concept, theory)
        self.assertIn("función, niveles eléctricos, temporización y protocolo", theory)

    def test_core_equations_and_directionality_are_present(self) -> None:
        equations = {
            equation["latex"]: equation["meaning"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("NM_H=V_{OH(min)}-V_{IH(min)}", equations)
        self.assertIn("NM_L=V_{IL(max)}-V_{OL(max)}", equations)
        self.assertIn("T_{clk}>=t_{CQ(max)}+t_{comb(max)}+t_{SU}+t_{skew/jitter}", equations)
        self.assertIn("R_{P(max)}=t_r/(0.8473 C_b)", equations)
        self.assertIn("R_{byte,8N1}=baud/10", equations)
        self.assertIn("emisor", equations["NM_H=V_{OH(min)}-V_{IH(min)}"])
        self.assertIn("receptor", equations["NM_H=V_{OH(min)}-V_{IH(min)}"])

    def test_activity_is_scaffolded_synthetic_and_fault_oriented(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 8)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 12)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 12)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("no conectes", text)
        self.assertIn("pull-up", text)
        self.assertIn("sincronizador", text)
        self.assertIn("cpol", text)
        self.assertIn("uart", text)
        self.assertIn("fallos inducidos", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 6)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "margen de ruido",
            "open-drain",
            "setup time",
            "metastabilidad",
            "sincronizador",
            "i²c",
            "cpol",
            "uart",
        ):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_directly_verified(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://www.ti.com/lit/an/szza036c/szza036c.pdf", urls)
        self.assertIn("https://www.ti.com/lit/an/scza004a/scza004a.pdf", urls)
        self.assertIn("https://www.nxp.com/docs/en/user-guide/UM10204.pdf", urls)
        self.assertIn("https://www.ti.com/lit/pdf/slva689", urls)
        self.assertIn("https://ww1.microchip.com/downloads/en/Appnotes/TB3216-Getting-Started-with-USART-90003216B.pdf", urls)

    def test_important_misconceptions_and_boundary_are_explicit(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("no una garantía absoluta", text)
        self.assertIn("debounce no reemplaza sincronización", text)
        self.assertIn("115200 baud", text)
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("validación clínica", notice)
        self.assertIn("equipos médicos en servicio", notice)


if __name__ == "__main__":
    unittest.main()
