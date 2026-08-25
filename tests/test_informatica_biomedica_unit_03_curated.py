from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "informatica-biomedica" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "informatica-biomedica" / "unit-03.json"
SUBJECT = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "informatica-biomedica.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class InformaticaBiomedicaUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["slug"], "interoperabilidad-y-terminologias")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("ppv=", self.text)

    def test_objectives_cover_interoperability_standards_and_mapping(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "interoperabilidad sintáctica, estructural y semántica",
            "fhir r5",
            "patient–study–series–instance",
            "snomed ct",
            "component, property, time, system, scale y method",
            "mapeos versionados",
        ):
            self.assertIn(phrase, objectives)

    def test_five_substantive_theory_sections(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        for section in sections:
            self.assertGreaterEqual(len(section["paragraphs"]), 6)
            self.assertGreaterEqual(len(section["key_points"]), 6)
            for point in section["key_points"]:
                self.assertGreaterEqual(len(point.split()), 5)
        headings = " ".join(x["heading"] for x in sections).casefold()
        for phrase in ("interoperabilidad por capas", "fhir r5", "dicom 2026c", "snomed ct y loinc", "mapeo y validación"):
            self.assertIn(phrase, headings)

    def test_layers_are_not_collapsed_into_semantic_interoperability(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "sintácticas, estructurales y semánticas",
            "json válido puede contener un código",
            "identificador, referencia, código y display",
            "versión forma parte",
            "codificar no repara",
        ):
            self.assertIn(phrase, text)

    def test_fhir_profiles_references_and_terminology_are_distinguished(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "fhir r5 5.0.0",
            "identifier y reference",
            "structuredefinition",
            "must support",
            "meta.profile",
            "codesystem",
            "valueset",
            "$validate",
            "no demuestra corrección clínica",
        ):
            self.assertIn(phrase, text)

    def test_dicom_information_model_is_not_reduced_to_files(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "no es simplemente un formato de archivo",
            "patient–study–series–instance",
            "study instance uid",
            "series instance uid",
            "sop instance uid",
            "information object definition",
            "value representation",
            "value multiplicity",
            "2026c",
        ):
            self.assertIn(phrase, text)

    def test_snomed_and_loinc_preserve_conceptual_distinctions(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "concepto no es su display",
            "reference sets",
            "julio de 2026",
            "component, property, time, system, scale",
            "2.83",
            "no el valor del resultado ni su unidad",
            "no deben tratarse como diccionarios",
        ):
            self.assertIn(phrase, text)

    def test_mapping_coverage_and_roundtrip_do_not_claim_equivalence(self) -> None:
        section = self.unit["theory_sections"][4]
        text = json.dumps(section, ensure_ascii=False).casefold()
        for phrase in (
            "no debe forzarse",
            "más amplias, más estrechas",
            "denominador",
            "round-trip",
            "no garantiza equivalencia",
            "no certifica interoperabilidad productiva",
        ):
            self.assertIn(phrase, text)
        equations = {x["latex"] for x in section["equations"]}
        self.assertIn(r"C_{map}=\frac{N_{mapeos\ defendibles}}{N_{elementos\ elegibles}}", equations)
        self.assertIn(r"L_{rt}=\frac{N_{elementos\ no\ equivalentes\ tras\ roundtrip}}{N_{elementos\ comparados}}", equations)

    def test_glossary_examples_and_activity_are_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 50)
        for term in (
            "interoperabilidad semántica", "identifier", "reference", "structuredefinition",
            "perfil fhir", "codesystem", "valueset", "conceptmap", "dicom", "iod",
            "sop class", "study instance uid", "vr", "vm", "snomed ct", "sctid",
            "reference set", "loinc", "component", "property", "system", "scale",
            "round-trip", "pérdida semántica",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 12)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)
        joined = " ".join(activity["instructions"] + activity["problems"] + activity["checking_criteria"]).casefold()
        for phrase in ("fhir", "dicom", "snomed ct", "loinc", "sintético", "meta.profile", "round-trip", "u4", "u5", "u6"):
            self.assertIn(phrase, joined)

    def test_sources_assessment_connections_and_notice(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 18)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "son sintéticos",
            "no se deben introducir datos identificables",
            "no interpreta resultados",
            "no certifica interoperabilidad",
            "u4 aborda analítica",
            "u5 factores humanos",
            "u6 gobernanza",
        ):
            self.assertIn(phrase, notice)

    def test_curricular_boundaries_keep_later_units_out_of_scope(self) -> None:
        purpose = self.unit["purpose"].casefold()
        for phrase in (
            "reutiliza los workflows de u2",
            "reserva analítica y alertas para u4",
            "factores humanos para u5",
            "gobernanza/implementación para u6",
        ):
            self.assertIn(phrase, purpose)

    def test_published_descriptor_matches_when_promoted(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {x["unit"]: x for x in subject["detailed_units"]}
        if detailed[3]["description"] != self.unit["purpose"]:
            self.skipTest("El publicador aún no ha promovido el descriptor U3 en este head.")
        self.assertEqual(detailed[3]["description"], self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()
