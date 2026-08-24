from __future__ import annotations

import json
import unittest
from pathlib import Path

# User-authored validation trigger after public-site synchronization.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "comunicacion-cientifica" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "comunicacion-cientifica" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ComunicacionCientificaUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "comunicacion-cientifica")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in ("imrad", "consort 2025", "strobe", "prisma 2020", "registro de cambios"):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_distinct_from_argument_unit(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "introducción",
            "métodos",
            "resultados",
            "discusión",
            "resumen estructurado",
            "guías de reporte",
            "referencias",
            "trazabilidad",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no certifica validez interna", theory)

    def test_pedagogy_progressively_removes_support(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        titles = " ".join(activity["title"] for activity in activities).casefold()
        self.assertIn("actividad guiada", titles)
        self.assertIn("apoyo reducido", titles)
        self.assertIn("reto autónomo", titles)
        self.assertGreaterEqual(len(activities[0]["problems"]), 10)
        self.assertGreaterEqual(len(activities[0]["deliverables"]), 6)
        self.assertGreaterEqual(len(activities[0]["checking_criteria"]), 8)
        all_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintético", all_text)
        self.assertIn("no uses datos de pacientes reales", all_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("imrad", "resumen estructurado", "consort", "strobe", "prisma", "registro de cambios"):
            self.assertIn(term, terms)

    def test_reporting_guidelines_are_not_treated_as_quality_certificates(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertIn("no certifican validez metodológica", text)
        self.assertIn("no se presenta como certificado de validez", text)
        self.assertIn("no certifica validez interna", text)

    def test_sources_are_directly_verified_and_current_where_needed(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 7)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn("https://www.icmje.org/recommendations/browse/manuscript-preparation/preparing-for-submission.html", urls)
        self.assertIn("https://www.bmj.com/content/389/bmj-2024-081123", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/18313558/", urls)
        self.assertIn("https://www.bmj.com/content/372/bmj.n71", urls)
        self.assertIn("https://www.equator-network.org/reporting-guidelines/", urls)

    def test_scope_and_professional_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar humana externa", notice)
        self.assertIn("no autorizan inferencias sobre pacientes individuales", notice)
        self.assertIn("sin confundir buena escritura con validez metodológica o clínica", purpose)


if __name__ == "__main__":
    unittest.main()
