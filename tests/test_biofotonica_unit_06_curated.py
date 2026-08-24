from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biofotonica" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "biofotonica" / "unit-06.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiofotonicaUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biofotonica")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "trazabilidad metrológica",
            "incertidumbre de medición",
            "función de transferencia de modulación",
            "reproducibilidad",
            "uso previsto",
            "riesgo residual",
        ):
            self.assertIn(concept, text)

    def test_theory_covers_measurement_performance_validation_and_translation(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "mensurando",
            "psf",
            "mtf",
            "cnr",
            "fantoma",
            "repetibilidad",
            "robustez",
            "verificación",
            "validación de diseño",
            "iso 14971",
            "qmsr",
        ):
            self.assertIn(concept, theory)

    def test_core_equations_are_present(self) -> None:
        equations = [
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        ]
        self.assertTrue(any("u_c^2" in equation for equation in equations))
        self.assertTrue(any("MTF" in equation for equation in equations))
        self.assertTrue(any("C_M" in equation for equation in equations))
        self.assertTrue(any("CNR" in equation for equation in equations))
        self.assertTrue(any("CV" in equation for equation in equations))

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 9)
        self.assertGreaterEqual(len(activity["problems"]), 15)
        self.assertGreaterEqual(len(activity["deliverables"]), 12)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 15)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("exclusivamente", text)
        self.assertIn("no uses pacientes", text)
        self.assertIn("no uses límites normativos como parámetros de exposición", text)
        self.assertIn("evaluación de banco no se presenta como validación clínica", text)

    def test_learning_support_is_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "mensurando",
            "trazabilidad metrológica",
            "mtf",
            "repetibilidad",
            "reproducibilidad",
            "fantoma",
            "desempeño esencial",
            "riesgo residual",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_current_frameworks_are_present(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://www.nist.gov/calibrations/traceability",
            "https://www.bipm.org/en/committees/jc/jcgm/publications",
            "https://pubmed.ncbi.nlm.nih.gov/35624150/",
            "https://www.iso.org/standard/72704.html",
            "https://webstore.iec.ch/en/publication/106555",
            "https://webstore.iec.ch/en/publication/73147",
            "https://www.fda.gov/medical-devices/postmarket-requirements-devices/quality-management-system-regulation-qmsr",
            "https://eur-lex.europa.eu/eli/reg/2017/745/oj",
        ):
            self.assertIn(url, urls)

    def test_regulatory_and_clinical_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        theory = " ".join(p for section in self.unit["theory_sections"] for p in section["paragraphs"]).casefold()
        self.assertIn("2 de febrero de 2026", theory)
        self.assertIn("no autoriza operar fuentes ópticas", notice)
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("validación de diseño o clínica", notice)
        self.assertIn("evaluación de conformidad", notice)
        self.assertIn("jurisdicción", notice)


if __name__ == "__main__":
    unittest.main()
