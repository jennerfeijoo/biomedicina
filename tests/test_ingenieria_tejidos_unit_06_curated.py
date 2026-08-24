from __future__ import annotations

# Final user-authored trigger after publication and catalog synchronization.

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "ingenieria-tejidos" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "ingenieria-tejidos" / "unit-06.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class IngenieriaTejidosUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "ingenieria-tejidos")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_wrong_equation_are_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("\\\\sigma=\\\\frac{f}{a_0}", text)
        for concept in ("atributo crítico de calidad", "parámetro de proceso", "comparabilidad",
                        "ich q9(r1)", "ich q10", "atmp", "hct/p", "producto combinado"):
            self.assertIn(concept, text)

    def test_theory_is_translational_and_substantive(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in ("liberación de lote", "escalar", "transferencia tecnológica",
                        "gestión de cambios", "desviación", "gmp",
                        "clasificación regulatoria", "comercialización prematura"):
            self.assertIn(concept, theory)
        self.assertIn("no demuestra seguridad clínica", theory)
        self.assertIn("no determina por sí sola una vía regulatoria universal", theory)

    def test_guided_activities_are_progressive_synthetic_and_non_operational(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 2)
        text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("solo con el caso sintético", text)
        self.assertIn("menos ayuda", text)
        self.assertIn("sin plantilla final", text)
        self.assertIn("no diseñes protocolos de cultivo o fabricación real", text)
        total_items = sum(
            len(activity.get(key, []))
            for activity in activities
            for key in ("instructions", "problems", "tasks", "deliverables", "checking_criteria")
        )
        self.assertGreaterEqual(total_items, 60)

    def test_learning_support_is_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("atributo crítico de calidad", "comparabilidad", "gmp", "cmc",
                     "atmp", "hct/p", "trazabilidad"):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_current(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/chemistry-manufacturing-and-controls-flexibilities-developing-human-cellular-and-gene-therapy",
            "https://www.ema.europa.eu/en/guideline-quality-non-clinical-clinical-requirements-investigational-advanced-therapy-medicinal-products-clinical-trials-scientific-guideline",
            "https://database.ich.org/sites/default/files/ICH_Q9%28R1%29_Guideline_Step4_2023_0126_0.pdf",
            "https://database.ich.org/sites/default/files/Q10%20Guideline.pdf",
            "https://www.isscr.org/guidelines",
        ):
            self.assertIn(url, urls)

    def test_regulatory_and_clinical_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        for boundary in ("no se proporcionan instrucciones operativas",
                         "no constituye revisión disciplinar externa",
                         "asesoría regulatoria",
                         "no determinan por sí solas",
                         "beneficio para pacientes"):
            self.assertIn(boundary, notice)
        self.assertIn("sin convertir cumplimiento gmp", purpose)
        self.assertIn("eficacia clínica", purpose)


if __name__ == "__main__":
    unittest.main()
