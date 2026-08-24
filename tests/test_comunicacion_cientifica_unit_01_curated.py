from __future__ import annotations

import json
import unittest
from pathlib import Path

# Final user-authored validation trigger after publication metadata synchronization.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "comunicacion-cientifica" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "comunicacion-cientifica" / "unit-01.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ComunicacionCientificaUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "comunicacion-cientifica")
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        for concept in ("objetivo comunicativo", "audiencia", "lenguaje claro", "pretest", "trazabilidad"):
            self.assertIn(concept, self.text)

    def test_theory_is_substantive_and_preserves_scientific_boundaries(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "objetivo científico",
            "arquitectura por capas",
            "legibilidad",
            "comprensión",
            "confianza",
            "incertidumbre",
            "registro de cambios",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no diagnostica", theory)

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 10)
        self.assertGreaterEqual(len(activity["deliverables"]), 6)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 8)
        activity_text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintétic", activity_text)
        self.assertIn("no reclutes personas", activity_text)
        self.assertIn("comprensión", activity_text)
        self.assertIn("registro", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 18)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "objetivo comunicativo",
            "audiencia prevista",
            "brief de comunicación",
            "lenguaje claro",
            "pretest",
            "trazabilidad editorial",
        ):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_authoritative(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        verified = [item for item in sources if item.get("verification_status") == "verified_directly"]
        self.assertEqual(len(verified), len(sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://nap.nationalacademies.org/catalog/23674/communicating-science-effectively-a-research-agenda", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/23942125/", urls)
        self.assertIn("https://www.cdc.gov/ccindex/pdf/clear-communication-user-guide.pdf", urls)
        self.assertIn("https://www.nih.gov/institutes-nih/nih-office-director/office-communications-public-liaison/clear-communication", urls)

    def test_biomedical_and_clinical_boundary_is_explicit(self) -> None:
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 5)
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("no constituye", notice)
        self.assertIn("no recogen datos personales", notice)
        self.assertIn("propósito explícito", purpose)
        self.assertIn("sin alterar la evidencia", purpose)


if __name__ == "__main__":
    unittest.main()
