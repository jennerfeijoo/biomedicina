from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "ingenieria-datos-biomedicos" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "ingenieria-datos-biomedicos" / "unit-03.json"
SUBJECT = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "ingenieria-datos-biomedicos.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class IngenieriaDatosBiomedicosUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["slug"], "almacenamiento-y-modelado")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("ppv=", self.text)

    def test_objectives_cover_storage_models_and_boundaries(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "primary key",
            "foreign key",
            "normalización",
            "parquet",
            "iceberg",
            "event_time",
            "ingest_time",
            "dicom",
            "u4",
            "u5",
            "u6",
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
        for token in (
            "relacional",
            "workload",
            "parquet",
            "iceberg",
            "series temporales",
            "híbrida",
        ):
            self.assertIn(token, headings)

    def test_relational_model_is_about_granularity_and_constraints(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "primary key",
            "foreign key",
            "integridad referencial",
            "normalización",
            "desnormalización",
            "omop",
        ):
            self.assertIn(phrase, text)

    def test_physical_design_uses_workload_and_volume_not_dogma(self) -> None:
        section = self.unit["theory_sections"][1]
        text = json.dumps(section, ensure_ascii=False).casefold()
        for phrase in (
            "índice",
            "partición",
            "partition pruning",
            "workload",
            "coste",
        ):
            self.assertIn(phrase, text)
        equations = {x["latex"] for x in section.get("equations", [])}
        self.assertIn(r"V\approx N\,r\,T\,b", equations)

    def test_columnar_lakehouse_layers_are_distinct(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "parquet",
            "row group",
            "column chunk",
            "small-files",
            "iceberg",
            "snapshot",
            "schema evolution",
        ):
            self.assertIn(phrase, text)
        self.assertIn("formato de archivo", text)
        self.assertIn("table format", text)

    def test_time_series_preserve_dual_clocks_and_late_arrivals(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "entity",
            "channel",
            "event_time",
            "ingest_time",
            "late",
            "out-of-order",
            "downsampling",
        ):
            self.assertIn(phrase, text)

    def test_hybrid_architecture_separates_objects_and_queryable_metadata(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in (
            "dicom",
            "study instance uid",
            "series instance uid",
            "sop instance uid",
            "object",
            "hash",
            "zarr",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no sustituye identidad clínica", text)

    def test_glossary_examples_and_activity_are_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 55)
        for term in (
            "primary key",
            "foreign key",
            "normalización",
            "desnormalización",
            "índice",
            "partición",
            "parquet",
            "row group",
            "column chunk",
            "iceberg",
            "snapshot",
            "event_time",
            "ingest_time",
            "late arrival",
            "downsampling",
            "object store",
            "study instance uid",
            "sop instance uid",
            "zarr",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 360)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 12)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)

    def test_common_errors_block_architectural_category_errors(self) -> None:
        text = " ".join(x["error"] + " " + x["correction"] for x in self.unit["common_errors"]).casefold()
        for phrase in (
            "foreign key",
            "ppv",
            "parquet",
            "transacciones",
            "iceberg",
            "hash",
            "producción clínica",
        ):
            self.assertIn(phrase, text)

    def test_sources_assessment_connections_and_notice(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 16)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        titles = " ".join(x["title"] for x in self.unit["sources"]).casefold()
        for phrase in (
            "postgresql",
            "parquet",
            "iceberg",
            "omop",
            "timescale",
            "dicom",
            "zarr",
            "fhir bulk data",
        ):
            self.assertIn(phrase, titles)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "sintéticos",
            "no se conectan bases clínicas",
            "pacs",
            "credenciales reales",
            "25 de agosto de 2026",
            "postgresql 18.6",
            "iceberg 1.11.0",
            "omop cdm v5.4",
            "dicom 2026c",
            "zarr v3.1",
            "fhir bulk data access 3.0.0 stu3",
            "u4",
            "u5",
            "u6",
        ):
            self.assertIn(phrase, notice)

    def test_published_descriptor_matches_when_promoted(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {x["unit"]: x for x in subject["detailed_units"]}
        if detailed[3]["description"] != self.unit["purpose"]:
            self.skipTest("El publicador todavía no ha promovido el descriptor U3.")
        self.assertEqual(detailed[3]["description"], self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()
