from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "electronica" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "electronica" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ElectronicaUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "electronica")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_irrelevant_snr_are_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("snr}_{db}", text)
        for concept in ("bjt", "mosfet", "punto q", "rds(on)", "soa"):
            self.assertIn(concept, text)

    def test_theory_has_clear_u2_u3_boundary(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertIn("ganancia, realimentación y respuesta en frecuencia queda reservado", text)
        self.assertIn("unidad 3", text)
        for concept in (
            "beta forzado",
            "vgs(th)",
            "carga de puerta",
            "pérdida de conmutación",
            "energía inductiva",
            "área de operación segura",
        ):
            self.assertIn(concept, text)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn(r"I_C\approx\beta I_B", equations)
        self.assertIn(r"P_{cond}\approx I_D^2 R_{DS(on)}", equations)
        self.assertIn(r"E_L=\frac{1}{2}LI^2", equations)
        self.assertIn(r"I_{gate,avg}\approx Q_G f_{sw}", equations)

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
        self.assertIn("flyback", SOURCE.read_text(encoding="utf-8").casefold())

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("bjt", "punto q", "beta forzado", "mosfet", "vgs(th)", "soa"):
            self.assertIn(term, terms)

    def test_sources_are_directly_traceable(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://assets.nexperia.com/documents/data-sheet/BC817_SER.pdf", urls)
        self.assertIn("https://assets.nexperia.com/documents/data-sheet/2N7002.pdf", urls)
        self.assertIn("https://www.ti.com/lit/an/sluaao2/sluaao2.pdf", urls)
        self.assertIn("https://www.ti.com/document-viewer/lit/html/slvaf04", urls)

    def test_safety_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no autorizan conectar transistores", notice)
        self.assertIn("equipos médicos", notice)
        self.assertIn("revisión humana interna y externa permanece pendiente", notice)


if __name__ == "__main__":
    unittest.main()
