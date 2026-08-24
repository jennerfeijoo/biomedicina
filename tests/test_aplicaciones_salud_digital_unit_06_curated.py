from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "aplicaciones-salud-digital" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "aplicaciones-salud-digital" / "unit-06.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class AplicacionesSaludDigitalUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_source_and_generated_mirror_are_exact(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "aplicaciones-salud-digital")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_inherited_ppv_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("ppv=", self.text)
        self.assertNotIn("valor predictivo positivo", self.text)
        self.assertIn("protección de datos desde el diseño", self.text)
        self.assertIn("cybersecurity framework 2.0", self.text)

    def test_theory_covers_privacy_security_regulation_and_lifecycle(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "base jurídica",
            "minimización",
            "dpia",
            "govern",
            "integridad",
            "finalidad prevista",
            "regla 11",
            "ai act",
            "ehds",
            "control de cambios",
            "rollback",
        ):
            self.assertIn(concept, theory)

    def test_current_regulatory_timeline_is_explicitly_versioned(self) -> None:
        theory = " ".join(p for section in self.unit["theory_sections"] for p in section["paragraphs"])
        self.assertIn("24 de agosto de 2026", theory)
        self.assertIn("2 de diciembre de 2027", theory)
        self.assertIn("2 de agosto de 2028", theory)
        self.assertIn("26 de marzo de 2027", theory)
        self.assertIn("fechas son estado regulatorio actual", theory)

    def test_pedagogy_is_progressive_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertIn("Actividad guiada", activities[0]["title"])
        self.assertIn("apoyo reducido", activities[1]["title"])
        self.assertIn("Reto autónomo", activities[2]["title"])
        for activity in activities:
            self.assertGreaterEqual(len(activity["instructions"]), 5)
            self.assertGreaterEqual(len(activity["problems"]), 12)
            self.assertGreaterEqual(len(activity["deliverables"]), 7)
            self.assertGreaterEqual(len(activity["checking_criteria"]), 8)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintétic", activity_text)
        self.assertIn("no introduzcas datos personales", activity_text)
        self.assertIn("go/no-go", activity_text)

    def test_examples_glossary_errors_and_assessment_are_complete(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 30)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 12)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "base jurídica",
            "dpia",
            "riesgo residual",
            "finalidad prevista",
            "calificación regulatoria",
            "clasificación regulatoria",
            "ai act",
            "ehds",
            "control de cambios",
            "rollback",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_authoritative(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 12)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        expected = {
            "https://eur-lex.europa.eu/legal-content/ES/ALL/?uri=CELEX:32016R0679",
            "https://www.edpb.europa.eu/documents/guideline/guidelines-052020-on-consent-under-regulation-2016679_en",
            "https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20",
            "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/cybersecurity-medical-devices-quality-management-system-considerations-and-content-premarket",
            "https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32017R0745",
            "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202601744",
            "https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32025R0327",
            "https://www.who.int/publications/i/item/9789240010567",
        }
        self.assertTrue(expected.issubset(urls))

    def test_professional_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar humana externa", notice)
        self.assertIn("asesoramiento jurídico", notice)
        self.assertIn("no deben utilizar datos personales", notice)
        self.assertIn("autorización legal o regulatoria", purpose)
        self.assertIn("evidencia de valor de u5", purpose)


if __name__ == "__main__":
    unittest.main()
