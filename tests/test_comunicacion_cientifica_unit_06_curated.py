from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "comunicacion-cientifica" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "comunicacion-cientifica" / "unit-06.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ComunicacionCientificaUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "comunicacion-cientifica")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "autoría",
            "credit",
            "revisión por pares",
            "confidencialidad",
            "inteligencia artificial",
            "fabricación",
            "falsificación",
            "plagio",
            "expresión de preocupación",
            "retracción",
        ):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_scoped(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        self.assertIn("cuatro criterios", theory)
        self.assertIn("no determinan quién califica como autor", theory)
        self.assertIn("error honesto", theory)
        self.assertIn("no certifica", theory)
        self.assertIn("no demuestran por sí solos", theory)

    def test_authorship_ai_and_integrity_boundaries_are_explicit(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertIn("herramientas de ia no pueden figurar como autoras", text)
        self.assertIn("confidencialidad no esté garantizada", text)
        self.assertIn("fabricación, falsificación o plagio", text)
        self.assertIn("excluye explícitamente el error honesto", text)
        self.assertIn("sin usar la taxonomía de contribuciones como sustituto automático", text)

    def test_examples_and_progressive_activities_are_complete(self) -> None:
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertTrue(activities[0]["title"].startswith("Actividad guiada:"))
        self.assertIn("apoyo reducido", activities[1]["title"].casefold())
        self.assertTrue(activities[2]["title"].startswith("Reto autónomo:"))
        self.assertGreaterEqual(len(activities[0]["problems"]), 10)
        self.assertGreaterEqual(len(activities[0]["deliverables"]), 6)
        self.assertGreaterEqual(len(activities[0]["checking_criteria"]), 8)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("fictici", activity_text)
        self.assertIn("no investigues ni acuses", activity_text)
        self.assertIn("revisión disciplinar humana externa", activity_text)

    def test_glossary_errors_assessment_and_connections_are_complete(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 5)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "autoría",
            "credit",
            "revisión por pares",
            "error honesto",
            "publicación duplicada",
            "expresión de preocupación",
            "retracción",
            "versionado",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_authoritative(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        expected = {
            "https://www.icmje.org/recommendations/",
            "https://www.icmje.org/recommendations/browse/roles-and-responsibilities/defining-the-role-of-authors-and-contributors.html",
            "https://www.icmje.org/recommendations/browse/artificial-intelligence/",
            "https://www.icmje.org/recommendations/browse/publishing-and-editorial-issues/corrections-and-version-control.html",
            "https://credit.niso.org/",
            "https://ori.hhs.gov/sites/default/files/2025-01/42CFR93.pdf",
            "https://members.publicationethics.org/sites/default/files/retraction-guidelines-cope.pdf",
        }
        self.assertTrue(expected.issubset(urls))

    def test_editorial_legal_and_clinical_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar humana externa", notice)
        self.assertIn("asesoría jurídica", notice)
        self.assertIn("no uses esta unidad para acusar", notice)
        self.assertIn("no certifican validez científica", notice)
        self.assertIn("sin asumir", purpose)
        self.assertIn("utilidad clínica", purpose)


if __name__ == "__main__":
    unittest.main()
