from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "ingenieria-clinica-gestion" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "ingenieria-clinica-gestion" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class IngenieriaClinicaGestionUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "ingenieria-clinica-gestion")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_wrong_risk_equation_are_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("r=p\\times s", text)
        self.assertIn("mantenimiento preventivo", text)
        self.assertIn("trazabilidad metrológica", text)
        self.assertIn("iec 62353", text)

    def test_theory_is_substantive_and_preserves_curricular_boundaries(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "mantenimiento correctivo",
            "orden de trabajo",
            "disponibilidad operacional",
            "mttr",
            "mtbf",
            "calibración",
            "verificación",
            "ajuste",
            "incertidumbre",
            "liberación",
        ):
            self.assertIn(concept, theory)
        self.assertIn("u2", theory)
        self.assertIn("u4", theory)
        self.assertIn("u5", theory)

    def test_core_equations_are_present_and_scoped(self) -> None:
        equations = [
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        ]
        self.assertIn("A_o=\\frac{T_{disponible}}{T_{requerido}}", equations)
        self.assertIn("MTTR=\\frac{\\sum_{i=1}^{n} t_{rep,i}}{n}", equations)
        self.assertIn("MTBF=\\frac{T_{operacion}}{N_{fallos}}", equations)
        self.assertIn("e=x_{ind}-x_{ref}", equations)
        self.assertIn("u_c(y)=\\sqrt{\\sum_i (c_i u_i)^2}", equations)

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 14)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 14)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintético", text)
        self.assertIn("no uses inventarios hospitalarios reales", text)
        self.assertIn("mtbf", text)
        self.assertIn("trazabilidad metrológica", text)
        self.assertIn("liberación", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "mantenimiento preventivo",
            "orden de trabajo",
            "disponibilidad operacional",
            "calibración",
            "verificación",
            "ajuste",
            "trazabilidad metrológica",
            "incertidumbre de medida",
            "liberación al servicio",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_current_where_needed(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://www.who.int/publications/i/item/9789240111257", urls)
        self.assertIn("https://www.who.int/publications/i/item/9789241501538", urls)
        self.assertIn("https://jcgm.bipm.org/vim/en/2.39.html", urls)
        self.assertIn("https://jcgm.bipm.org/vim/en/2.41.html", urls)
        self.assertIn("https://www.iso.org/standard/10012", urls)
        self.assertIn("https://webstore.iec.ch/en/publication/6913", urls)
        iso = next(item for item in sources if item["url"] == "https://www.iso.org/standard/10012")
        self.assertEqual(iso["year"], 2026)

    def test_scope_boundary_and_real_equipment_prohibition_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("equipos médicos reales", notice)
        self.assertIn("no autoriza", self.unit["self_assessment"][-1]["answer"].casefold())
        self.assertIn("sin convertir una actividad educativa", purpose)


if __name__ == "__main__":
    unittest.main()
