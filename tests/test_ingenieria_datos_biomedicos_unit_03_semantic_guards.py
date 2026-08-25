from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "ingenieria-datos-biomedicos" / "units" / "unit-03.json"


class IngenieriaDatosBiomedicosUnit03SemanticGuards(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_foreign_key_is_not_record_linkage_truth(self) -> None:
        self.assertIn("no demuestra que el vínculo entre dos identidades fuente sea verdadero", self.text)

    def test_parquet_is_not_a_transactional_database(self) -> None:
        self.assertIn("parquet es un formato de archivo", self.text)
        self.assertIn("semántica de tabla requiere otra capa", self.text)

    def test_schema_evolution_does_not_authorize_semantic_reinterpretation(self) -> None:
        self.assertIn("schema evolution no autoriza reinterpretar", self.text)

    def test_event_time_and_ingest_time_are_not_interchangeable(self) -> None:
        self.assertIn("event_time", self.text)
        self.assertIn("ingest_time", self.text)
        self.assertIn("no debe reescribir event_time", self.text)

    def test_hash_is_not_clinical_identity(self) -> None:
        self.assertIn("hash verifica bytes", self.text)
        self.assertIn("no sustituye identidad", self.text)

    def test_fast_queries_do_not_establish_clinical_readiness(self) -> None:
        self.assertIn("rendimiento técnico", self.text)
        self.assertIn("utilidad clínica", self.text)
        self.assertIn("u4", self.text)
        self.assertIn("u5", self.text)
        self.assertIn("u6", self.text)


if __name__ == "__main__":
    unittest.main()
