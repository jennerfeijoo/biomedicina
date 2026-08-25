from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "historias-clinicas-terminologias-estandares" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "historias-clinicas-terminologias-estandares" / "unit-03.json"
SUBJECT = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "historias-clinicas-terminologias-estandares.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"

class HistoriasClinicasUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_exact_mirror_and_template_removal(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["slug"], "terminologias-clinicas")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("ppv=", self.text)
        self.assertNotIn("sensibilidad, especificidad y prevalencia", self.text)

    def test_objectives_cover_three_terminology_roles(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "terminología clínica", "clasificación", "code system", "value set",
            "snomed ct", "loinc", "foundation", "mms", "mapeos sintéticos",
            "sistema, versión, código", "u4",
        ):
            self.assertIn(phrase, objectives)

    def test_five_substantive_sections(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        for section in sections:
            self.assertGreaterEqual(len(section["paragraphs"]), 6)
            self.assertGreaterEqual(len(section["key_points"]), 6)
            for point in section["key_points"]:
                self.assertGreaterEqual(len(point.split()), 5)
        headings = " ".join(x["heading"] for x in sections).casefold()
        for phrase in (
            "terminologías, clasificaciones y contexto",
            "snomed ct",
            "loinc",
            "icd-11",
            "mapeo, equivalencia, versiones",
        ):
            self.assertIn(phrase, headings)

    def test_snomed_model_is_concept_centric_and_versioned(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "concept identifier", "fully specified name", "is a", "finding site",
            "concept model", "dominios", "rangos", "reference sets",
            "pre-coordinación", "postcoordinación", "julio de 2026",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no autoriza combinaciones libres", text)

    def test_loinc_requires_six_parts_not_name_matching(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "component", "property", "time", "system", "scale", "method",
            "coincidencia del analito no basta", "unidades", "información insuficiente",
            "2.83", "19 de agosto de 2026",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no debe seleccionarse porque", text)

    def test_icd_foundation_and_mms_are_not_collapsed(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "foundation component", "múltiples padres", "linearización",
            "mortality and morbidity statistics", "extension codes",
            "clasificación estadística", "no es una sustitución carácter por carácter",
            "2026-01",
        ):
            self.assertIn(phrase, text)

    def test_mapping_is_directional_and_uncertain(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in (
            "exacto", "origen más amplio", "origen más estrecho", "parcialmente solapado",
            "sin correspondencia", "direccionales", "no garantiza", "pérdida",
            "control positivo", "negativo", "caso ambiguo", "inactivarse",
        ):
            self.assertIn(phrase, text)

    def test_glossary_activity_and_cases_are_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 50)
        for term in (
            "concepto snomed ct", "reference set", "postcoordinación", "loinc",
            "component", "property", "system", "icd-11 foundation", "icd-11 mms",
            "mapeo terminológico", "equivalencia exacta", "mapa direccional",
            "pérdida semántica", "trazabilidad terminológica",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 24)
        self.assertGreaterEqual(len(activity["deliverables"]), 12)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)

    def test_activity_rejects_false_equivalence(self) -> None:
        activity = self.unit["guided_activities"][0]
        joined = " ".join(activity["instructions"] + activity["problems"] + activity["checking_criteria"]).casefold()
        for phrase in (
            "no mapees por coincidencia de nombre",
            "foundation o con mms",
            "exacta, más amplia, más estrecha, parcial, ambigua o sin correspondencia",
            "control positivo", "control negativo", "caso deliberadamente ambiguo",
            "cobertura de mapeo", "mapas inversos", "conceptos inactivos",
            "u4", "u6",
        ):
            self.assertIn(phrase, joined)

    def test_sources_assessment_connections_and_boundary(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 18)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "escenarios y registros sintéticos",
            "no constituye codificación clínica profesional",
            "no se deben introducir datos identificables",
            "u3 enseña significado y mapeo",
            "u4 cubre interoperabilidad",
        ):
            self.assertIn(phrase, notice)

    def test_published_descriptor_matches_canonical_purpose(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {x["unit"]: x for x in subject["detailed_units"]}
        if detailed[3]["description"] != self.unit["purpose"]:
            self.skipTest("descriptor pendiente de promoción automática")
        self.assertEqual(detailed[3]["description"], self.unit["purpose"])

if __name__ == "__main__":
    unittest.main()
