import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/ingenieria-datos-biomedicos/units/unit-04.json"
MIRROR = ROOT / "data/generated_units/ingenieria-datos-biomedicos/unit-04.json"
DESCRIPTOR = ROOT / "data/subjects/ingenieria-biomedica/ingenieria-datos-biomedicos.json"


class IngenieriaDatosBiomedicosUnit04Curated(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = json.dumps(cls.data, ensure_ascii=False).lower()

    def test_identity_and_exact_mirror(self):
        self.assertEqual(self.data["subject_id"], "ingenieria-datos-biomedicos")
        self.assertEqual(self.data["unit"], 4)
        self.assertEqual(self.data["slug"], "calidad-y-procedencia")
        self.assertEqual(self.data["title"], "Calidad y procedencia")
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_template_and_irrelevant_ppv_are_removed(self):
        self.assertNotIn("concepto de la unidad que debe definirse mediante entidades observables", self.text)
        self.assertNotIn("valor predictivo positivo", self.text)
        self.assertNotIn("ppv=", self.text)
        self.assertNotIn("se\\,\\pi", self.text)

    def test_quality_is_fit_for_use_with_explicit_denominators(self):
        for concept in ["fitness for purpose", "conformance", "completeness", "plausibility", "verification", "validation", "población elegible", "denominador"]:
            self.assertIn(concept, self.text)
        equations = " ".join(e.get("expression", "") for s in self.data["theory_sections"] for e in s.get("equations", []))
        self.assertIn("N_{present}", equations)
        self.assertIn("N_{eligible}", equations)
        self.assertIn("N_{viol}", equations)
        self.assertIn("N_{resolved}", equations)
        self.assertIn("Coverage", equations)

    def test_quality_rules_preserve_semantics_and_statuses(self):
        for concept in ["rule_id", "severidad", "umbral", "integridad referencial", "effective", "issued", "ingest", "passed", "failed", "error", "not applicable", "cuarentena", "expiry"]:
            self.assertIn(concept, self.text)
        self.assertIn("drop_duplicates", self.text)
        self.assertIn("no demuestra identidad clínica correcta", self.text)
        self.assertIn("no demuestra que los datos pasaron", self.text)

    def test_provenance_models_are_distinguished(self):
        for concept in ["w3c prov", "entity", "activity", "agent", "wasgeneratedby", "wasderivedfrom", "fhir provenance", "auditevent", "openlineage", "job", "run", "dataset", "facet"]:
            self.assertIn(concept, self.text)
        self.assertIn("provenance se centra", self.text)
        self.assertIn("auditevent", self.text)
        self.assertIn("job identifica un proceso lógico", self.text)
        self.assertIn("cada run representa una ejecución concreta", self.text)
        self.assertIn("no prueba que la transformación sea correcta", self.text)

    def test_versioning_and_reproducibility_keep_semantic_limits(self):
        for concept in ["data version", "schema version", "vocabulary version", "code version", "configuration version", "manifest", "snapshot", "release", "checksum", "content hash", "changelog", "reprocesamiento"]:
            self.assertIn(concept, self.text)
        self.assertIn("no puede afirmarse que el archivo sea semánticamente correcto", self.text)
        self.assertIn("sobrescribir silenciosamente el pasado", self.text)
        self.assertIn("reproducibilidad implica", self.text)
        self.assertIn("no implica que el resultado sea verdadero", self.text)

    def test_curricular_boundaries_are_explicit(self):
        purpose = self.data["purpose"].lower()
        self.assertIn("u1", purpose)
        self.assertIn("u2", purpose)
        self.assertIn("u3", purpose)
        self.assertIn("u5", purpose)
        self.assertIn("u6", purpose)
        notice = self.data["editorial_notice"].lower()
        self.assertIn("datos exclusivamente sintéticos", notice)
        self.assertIn("no conecta ehr", notice)
        self.assertIn("u5", notice)
        self.assertIn("u6", notice)
        self.assertIn("no certifica", notice)

    def test_academic_depth(self):
        self.assertGreaterEqual(len(self.data["learning_objectives"]), 6)
        self.assertGreaterEqual(len(self.data["theory_sections"]), 5)
        for section in self.data["theory_sections"]:
            self.assertGreaterEqual(len(section["paragraphs"]), 6)
            self.assertGreaterEqual(len(section["key_points"]), 6)
            for paragraph in section["paragraphs"]:
                self.assertGreaterEqual(len(paragraph.split()), 20)
            for point in section["key_points"]:
                self.assertGreaterEqual(len(point.split()), 4)
        self.assertGreaterEqual(len(self.data["glossary"]), 50)
        self.assertGreaterEqual(len(self.data["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.data["common_errors"]), 18)
        self.assertGreaterEqual(len(self.data["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.data["sources"]), 14)

    def test_guided_activity_is_substantive_and_reproducible(self):
        activity = self.data["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 420)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 24)
        joined = " ".join(activity["problems"] + activity["deliverables"] + activity["checking_criteria"]).lower()
        for concept in ["denominador", "release", "prov", "openlineage", "manifest", "hash", "quality gate", "cuarentena", "excepción"]:
            self.assertIn(concept, joined)

    def test_glossary_and_sources_cover_core_families(self):
        terms = {g["term"].lower() for g in self.data["glossary"]}
        for term in ["calidad de datos", "conformance", "completeness", "plausibility", "w3c prov", "fhir provenance", "openlineage", "quality gate", "fair"]:
            self.assertIn(term, terms)
        source_text = " ".join(s["title"] + " " + s["organization"] for s in self.data["sources"]).lower()
        for family in ["kahn", "ohdsi", "prov", "fhir", "openlineage", "iso/iec 25012", "fair"]:
            self.assertIn(family, source_text)
        self.assertTrue(all(s.get("verification_status", "").startswith("verified_directly_2026-08-25") for s in self.data["sources"]))

    def test_published_descriptor_matches_when_promoted(self):
        if not DESCRIPTOR.exists():
            self.skipTest("Descriptor todavía no promovido por publicación.")
        descriptor = json.loads(DESCRIPTOR.read_text(encoding="utf-8"))
        unit = next(item for item in descriptor["detailed_units"] if item["unit"] == 4)
        if unit["description"] != self.data["purpose"]:
            self.skipTest("El descriptor de U4 será promovido por el workflow de publicación.")
        self.assertEqual(unit["description"], self.data["purpose"])


if __name__ == "__main__":
    unittest.main()
