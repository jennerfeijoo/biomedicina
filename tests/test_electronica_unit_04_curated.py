from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "electronica" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "electronica" / "unit-04.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ElectronicaUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "electronica")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in ("sallen-key", "butterworth", "bessel", "chebyshev", "puente de wien"):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_scoped(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "función de transferencia",
            "factor de calidad",
            "retardo de grupo",
            "multiple-feedback",
            "margen de fase",
            "arranque",
            "distorsión armónica",
            "anti-alias",
        ):
            self.assertIn(concept, theory)
        self.assertIn("u5", self.unit["purpose"].casefold())
        self.assertIn("u6", theory)

    def test_core_equations_are_present_and_conditioned(self) -> None:
        equations = {
            equation["latex"]: equation["meaning"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("H(s)=V_{out}(s)/V_{in}(s)", equations)
        self.assertIn("Q=1/(3-K)", equations)
        self.assertIn("f_Wien=1/(2πRC)", equations)
        self.assertIn("τ_g(ω)=-dφ(ω)/dω", equations)
        self.assertIn("caso Sallen-Key", equations["Q=1/(3-K)"])
        loop_meanings = " ".join(equations.values()).casefold()
        self.assertIn("no es por sí sola", loop_meanings)

    def test_guided_activity_is_scaffolded_and_safe(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 8)
        self.assertGreaterEqual(len(activity["problems"]), 18)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("simulación", text)
        self.assertIn("no conectadas a personas", text)
        self.assertIn("monte carlo", text)
        self.assertIn("thd", text)
        self.assertIn("arranque", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "filtro activo",
            "factor q",
            "sallen-key",
            "retardo de grupo",
            "puente de wien",
            "ganancia de lazo",
            "anti-alias",
        ):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_primary_or_technical(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        verified = [item for item in sources if item.get("verification_status") == "verified_directly"]
        self.assertEqual(len(verified), len(sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://www.analog.com/en/resources/app-notes/an-649.html", urls)
        self.assertIn("https://www.ti.com/lit/an/sloa024b/sloa024b.pdf", urls)
        self.assertIn("https://www.ti.com/lit/an/sloa060/sloa060.pdf", urls)
        self.assertIn("https://www.analog.com/media/en/technical-documentation/application-notes/an148fa.pdf", urls)

    def test_stability_and_clinical_boundaries_are_explicit(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("no garantiza arranque", text)
        self.assertIn("filtrado posterior no reconstruye", text)
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("validación clínica", notice)
        self.assertIn("equipos médicos en servicio", notice)


if __name__ == "__main__":
    unittest.main()
