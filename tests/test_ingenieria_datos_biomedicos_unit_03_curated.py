from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "ingenieria-datos-biomedicos" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "ingenieria-datos-biomedicos" / "unit-03.json"
SUBJECT = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "ingenieria-datos-biomedicos.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class IngenieriaDatosBiomedicosUnit03Curated(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.mirror = json.loads(MIRROR.read_text(encoding="utf-8"))
        cls.text = json.dumps(cls.data, ensure_ascii=False).lower()

    def test_identity_and_mirror(self) -> None:
        self.assertEqual(self.data["subject_id"], "ingenieria-datos-biomedicos")
        self.assertEqual(self.data["unit"], 3)
        self.assertEqual(self.data["slug"], "almacenamiento-y-modelado")
        self.assertEqual(self.data, self.mirror)

    def test_template_and_irrelevant_ppv_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("ppv=", self.text)
        self.assertNotIn("valor predictivo positivo", self.text)
        self.assertNotIn("sensibilidad, especificidad y prevalencia", self.text)

    def test_curricular_boundaries_are_explicit(self) -> None:
        purpose = self.data["purpose"].lower()
        for token in ("u2", "u4", "u5", "u6"):
            self.assertIn(token, purpose)
        self.assertIn("calidad", purpose)
        self.assertIn("orquestación", purpose)
        self.assertIn("privacidad", purpose)

    def test_relational_model_is_substantive(self) -> None:
        section = self.data["theory_sections"][0]
        text = " ".join(section["paragraphs"] + section["key_points"]).lower()
        for term in ("clave primaria", "clave foránea", "normaliz", "desnormaliz", "foreign key", "omop"):
            self.assertIn(term, text)
        self.assertIn("no demuestra corrección clínica", text)

    def test_physical_storage_distinctions(self) -> None:
        section = self.data["theory_sections"][1]
        text = " ".join(section["paragraphs"] + section["key_points"]).lower()
        for term in ("parquet", "row group", "column chunk", "índice", "particion", "small files", "benchmark"):
            self.assertIn(term, text)
        self.assertIn("no es una base de datos", text)
        self.assertIn("más particiones no implica más rendimiento", text)

    def test_file_table_snapshot_layers_are_separated(self) -> None:
        section = self.data["theory_sections"][2]
        text = " ".join(section["paragraphs"] + section["key_points"]).lower()
        for term in ("formato de archivo", "formato de tabla", "iceberg", "snapshot", "manifest", "schema evolution"):
            self.assertIn(term, text)
        self.assertIn("no equivalen automáticamente a copias de seguridad", text)
        self.assertIn("no demuestra equivalencia semántica", text)

    def test_temporal_semantics_are_preserved(self) -> None:
        section = self.data["theory_sections"][3]
        text = " ".join(section["paragraphs"] + section["key_points"]).lower()
        for term in ("effective", "issued", "ingest", "amended", "resampling", "long", "wide"):
            self.assertIn(term, text)
        self.assertIn("no son duplicados", text)
        self.assertIn("no deben confundirse con observaciones originales", text)

    def test_workload_precedes_technology(self) -> None:
        section = self.data["theory_sections"][4]
        text = " ".join(section["paragraphs"] + section["key_points"]).lower()
        for term in ("architecture decision record", "workload", "point lookup", "latencia", "arquitectura híbrida"):
            self.assertIn(term, text)
        self.assertIn("no demuestran utilidad clínica", text)

    def test_equations_measure_storage_not_clinical_prediction(self) -> None:
        equations = [eq for section in self.data["theory_sections"] for eq in section.get("equations", [])]
        latex = " ".join(eq["latex"] for eq in equations)
        meanings = " ".join(eq["meaning"] for eq in equations).lower()
        self.assertIn("CR=", latex)
        self.assertIn("A_{scan}", latex)
        self.assertIn("T=", latex)
        self.assertIn("compresión", meanings)
        self.assertIn("lectura", meanings)
        self.assertNotIn("prevalencia", meanings)

    def test_pedagogical_depth(self) -> None:
        self.assertGreaterEqual(len(self.data["learning_objectives"]), 6)
        self.assertGreaterEqual(len(self.data["theory_sections"]), 5)
        for section in self.data["theory_sections"]:
            self.assertGreaterEqual(len(section["paragraphs"]), 6)
            self.assertGreaterEqual(len(section["key_points"]), 6)
        self.assertGreaterEqual(len(self.data["glossary"]), 45)
        self.assertGreaterEqual(len(self.data["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.data["common_errors"]), 18)
        self.assertGreaterEqual(len(self.data["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.data["sources"]), 12)

    def test_guided_activity_is_reproducible_and_comparative(self) -> None:
        self.assertEqual(len(self.data["guided_activities"]), 1)
        activity = self.data["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 360)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 24)
        activity_text = json.dumps(activity, ensure_ascii=False).lower()
        for term in ("baseline", "parquet", "workload", "effective", "issued", "ingest", "adr"):
            self.assertIn(term, activity_text)
        self.assertIn("datos sintéticos", activity_text)

    def test_glossary_contains_architecture_and_time_terms(self) -> None:
        terms = {item["term"].lower() for item in self.data["glossary"]}
        expected = {
            "clave primaria", "clave foránea", "normalización", "desnormalización", "índice",
            "partición", "parquet", "row group", "formato de tabla", "snapshot", "manifest",
            "schema evolution", "effective time", "issued time", "ingest time", "workload"
        }
        self.assertTrue(expected.issubset(terms))

    def test_sources_cover_current_primary_technical_references(self) -> None:
        sources = " ".join(f'{s["title"]} {s["organization"]} {s["url"]}' for s in self.data["sources"]).lower()
        for term in ("postgresql", "parquet", "iceberg", "hl7", "fhir", "ohdsi", "omop"):
            self.assertIn(term, sources)

    def test_scope_does_not_claim_clinical_or_production_readiness(self) -> None:
        notice = self.data["editorial_notice"].lower()
        for term in ("datos exclusivamente sintéticos", "no conecta", "no configura credenciales", "no interpreta datos de pacientes"):
            self.assertIn(term, notice)
        self.assertIn("revalidar versiones", notice)

    def test_public_descriptor_matches_after_promotion(self) -> None:
        if not SUBJECT.exists():
            self.skipTest("El descriptor curricular aún no existe")
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        unit = next(item for item in subject["detailed_units"] if item["unit"] == 3)
        if unit["description"] != self.data["purpose"]:
            self.skipTest("El publicador todavía no ha promovido U3 en este head")
        self.assertEqual(unit["description"], self.data["purpose"])


if __name__ == "__main__":
    unittest.main()
