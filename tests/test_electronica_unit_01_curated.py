from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "electronica" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "electronica" / "unit-01.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ElectronicaUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "electronica")
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("snr}_{db}", text)
        for concept in ("unión pn", "rectificación", "zener", "tvs"):
            self.assertIn(concept, text)

    def test_theory_is_discipline_specific_and_substantive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "región de agotamiento",
            "ecuación de shockley",
            "puente de onda completa",
            "rizado",
            "impedancia dinámica",
            "tensión de clamp",
            "hoja de datos",
        ):
            self.assertIn(concept, theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn(r"I_D=I_S\left(e^{V_D/(nV_T)}-1\right)", equations)
        self.assertIn(r"\Delta V\approx\frac{I_{load}}{f_{ripple}C}", equations)
        self.assertIn(r"I_R=\frac{V_{in}-V_Z}{R}", equations)
        self.assertIn(r"P_Z\approx V_Z I_Z", equations)

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 6)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 8)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintético", text)
        self.assertIn("no conectes", text)
        self.assertIn("tvs", text)
        self.assertIn("zener", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "unión pn",
            "puente rectificador",
            "rizado",
            "diodo zener",
            "tvs",
            "tensión de clamp",
        ):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_current_where_needed(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        verified = [s for s in sources if s.get("verification_status") == "verified_directly"]
        self.assertEqual(len(verified), len(sources))
        urls = {s["url"] for s in sources}
        self.assertIn(
            "https://assets.nexperia.com/documents/brochure/Nexperia_document_book_DiodeApplicationHandbook_2022.pdf",
            urls,
        )
        self.assertIn("https://www.ti.com/lit/pdf/slvae37", urls)
        self.assertIn("https://webstore.iec.ch/en/publication/68954", urls)
        self.assertIn("https://webstore.iec.ch/en/publication/67497", urls)

    def test_medical_safety_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no autorizan conectar circuitos a personas", notice)
        self.assertIn("seguridad o conformidad", purpose)
        self.assertIn("equipos médicos", notice)


# Final user-authored validation trigger after generated publication synchronization.
if __name__ == "__main__":
    unittest.main()
