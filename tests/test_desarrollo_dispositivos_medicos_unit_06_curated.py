from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "desarrollo-dispositivos-medicos" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "desarrollo-dispositivos-medicos" / "unit-06.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class DesarrolloDispositivosMedicosUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "desarrollo-dispositivos-medicos")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_inherited_risk_equation_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("r=p\\times s", self.text)
        for concept in (
            "estrategia regulatoria",
            "transferencia de diseño",
            "control de cambios",
            "vigilancia posmercado",
            "qmsr",
            "estar",
            "eudamed",
        ):
            self.assertIn(concept, self.text)

    def test_theory_is_current_jurisdiction_specific_and_lifecycle_oriented(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        self.assertIn("no enseña que exista una clasificación o vía universal", theory)
        self.assertIn("2 de febrero de 2026", theory)
        self.assertIn("iso 13485:2016", theory)
        self.assertIn("28 de mayo de 2026", theory)
        self.assertIn("21 cfr part 803", theory)
        self.assertIn("21 cfr part 806", theory)
        self.assertIn("u1–u6", theory)

    def test_postmarket_rate_is_descriptive_not_a_regulatory_threshold(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("r=\\frac{n_{eventos}}{N_{exposiciones}}", equations)
        theory = " ".join(p for section in self.unit["theory_sections"] for p in section["paragraphs"]).casefold()
        self.assertIn("no establece por sí solo causalidad ni reportabilidad", theory)

    def test_progressive_activities_are_synthetic_and_scaffolded(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertIn("actividad guiada", activities[0]["title"].casefold())
        self.assertIn("apoyo reducido", activities[1]["title"].casefold())
        self.assertIn("reto autónomo", activities[2]["title"].casefold())
        self.assertGreaterEqual(len(activities[0]["problems"]), 14)
        self.assertGreaterEqual(len(activities[0]["deliverables"]), 9)
        self.assertGreaterEqual(len(activities[0]["checking_criteria"]), 11)
        self.assertGreaterEqual(len(activities[1]["problems"]), 8)
        self.assertGreaterEqual(len(activities[2]["problems"]), 8)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("exclusivamente", activity_text)
        self.assertIn("no presentes", activity_text)
        self.assertIn("casos sintéticos", activity_text)
        self.assertIn("no afirme conformidad", activity_text)

    def test_glossary_examples_errors_and_assessment_are_substantive(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "estrategia regulatoria",
            "jurisdicción",
            "estar",
            "qmsr",
            "transferencia de diseño",
            "control de cambios",
            "acción correctiva",
            "mdr",
            "pms",
            "eudamed",
        ):
            self.assertIn(term, terms)

    def test_sources_are_current_traceable_and_authoritative(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 11)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        self.assertIn(
            "https://www.fda.gov/medical-devices/postmarket-requirements-devices/quality-management-system-regulation-qmsr",
            urls,
        )
        self.assertIn(
            "https://www.fda.gov/medical-devices/how-study-and-market-your-device/estar-program",
            urls,
        )
        self.assertIn(
            "https://www.fda.gov/medical-devices/postmarket-requirements-devices/mandatory-reporting-requirements-manufacturers-importers-and-device-user-facilities",
            urls,
        )
        self.assertIn("https://www.iso.org/standard/59752.html", urls)
        self.assertIn("https://eur-lex.europa.eu/eli/reg/2017/745/2026-01-01/eng", urls)
        qmsr = next(item for item in sources if item["title"] == "Quality Management System Regulation (QMSR)")
        self.assertEqual(qmsr["year"], 2026)

    def test_editorial_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar humana externa", notice)
        self.assertIn("asesoría jurídica o regulatoria", notice)
        self.assertIn("no presentes información a autoridades", notice)
        self.assertIn("agosto de 2026", notice)
        self.assertIn("dependiente de jurisdicción", purpose)
        self.assertIn("distinguiendo preparación documental de autorización", purpose)


if __name__ == "__main__":
    unittest.main()
