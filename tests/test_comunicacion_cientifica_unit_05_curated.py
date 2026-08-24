from __future__ import annotations

import json
import unittest
from pathlib import Path

# Final user-authored trigger after public and descriptor synchronization.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "comunicacion-cientifica" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "comunicacion-cientifica" / "unit-05.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ComunicacionCientificaUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "comunicacion-cientifica")
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_marker_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "lenguaje llano",
            "riesgo absoluto",
            "riesgo relativo",
            "procedencia",
            "debunking",
            "prebunking",
            "participación pública",
        ):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_preserves_unit_boundary(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        self.assertIn("unidad anterior", theory)
        self.assertIn("u6", theory)
        self.assertIn("revisión por pares", theory)
        self.assertIn("no crea", theory)

    def test_risk_equations_define_absolute_and_relative_context(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("R=\\frac{E}{N}", equations)
        self.assertIn("RR=\\frac{R_1}{R_0}", equations)
        self.assertIn("RD=R_1-R_0", equations)

    def test_examples_and_progressive_activities_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertTrue(activities[0]["title"].startswith("Actividad guiada:"))
        self.assertIn("apoyo reducido", activities[1]["title"].casefold())
        self.assertTrue(activities[2]["title"].startswith("Reto autónomo:"))
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        for concept in ("sintétic", "no uses datos", "comprensión", "procedencia", "engagement"):
            self.assertIn(concept, activity_text)
        self.assertGreaterEqual(len(activities[0]["problems"]), 10)
        self.assertGreaterEqual(len(activities[0]["deliverables"]), 6)
        self.assertGreaterEqual(len(activities[0]["checking_criteria"]), 8)

    def test_glossary_errors_assessment_and_connections_are_complete(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 5)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "lenguaje llano",
            "riesgo absoluto",
            "riesgo relativo",
            "infodemia",
            "debunking",
            "prebunking",
            "participación pública",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_cover_core_domains(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        expected = {
            "https://nap.nationalacademies.org/catalog/23674/communicating-science-effectively-a-research-agenda",
            "https://www.cdc.gov/ccindex/tool/index.html",
            "https://www.nih.gov/institutes-nih/nih-office-director/office-communications-public-liaison/clear-communication/plain-language-nih",
            "https://pubmed.ncbi.nlm.nih.gov/25133362/",
            "https://pubmed.ncbi.nlm.nih.gov/28895452/",
            "https://pubmed.ncbi.nlm.nih.gov/37560816/",
        }
        self.assertTrue(expected.issubset(urls))

    def test_clinical_and_editorial_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituyen revisión disciplinar humana externa", notice)
        self.assertIn("no asesoramiento clínico", notice)
        self.assertIn("no certifican validez científica", notice)
        self.assertIn("engagement", purpose)
        self.assertIn("consejo clínico", purpose)


if __name__ == "__main__":
    unittest.main()
