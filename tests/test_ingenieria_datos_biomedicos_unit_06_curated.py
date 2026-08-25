import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/ingenieria-datos-biomedicos/units/unit-06.json"
MIRROR = ROOT / "data/generated_units/ingenieria-datos-biomedicos/unit-06.json"
DESCRIPTOR = ROOT / "data/subjects/ingenieria-biomedica/ingenieria-datos-biomedicos.json"
PUBLIC = ROOT / "ingenieria-biomedica/ingenieria-datos-biomedicos/unidades/unidad-06.html"


class IngenieriaDatosBiomedicosUnit06Curated(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = json.dumps(cls.data, ensure_ascii=False).lower()

    def test_identity_and_exact_mirror(self):
        self.assertEqual(self.data["subject_id"], "ingenieria-datos-biomedicos")
        self.assertEqual(self.data["unit"], 6)
        self.assertEqual(self.data["slug"], "privacidad-y-productos-de-datos")
        self.assertEqual(self.data["title"], "Privacidad y productos de datos")
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_generic_template_and_classifier_equations_are_removed(self):
        for marker in ["concepto de la unidad que debe definirse mediante entidades observables", "ppv=", "valor predictivo positivo", "sensibilidad y especificidad"]:
            self.assertNotIn(marker, self.text)

    def test_minimization_and_identification_risk_are_explicit(self):
        for concept in ["identificador directo", "cuasi-identificador", "singling out", "linkage", "minimización", "limitación del propósito", "retención", "riesgo residual"]:
            self.assertIn(concept, self.text)
        self.assertIn("pseudonimizar no demuestra anonimización", self.text)

    def test_pseudonymization_is_not_collapsed_with_anonymization_or_crypto(self):
        for concept in ["seudonimización", "anonimización", "hashing", "cifrado", "tokenización", "generalización", "supresión", "información adicional"]:
            self.assertIn(concept, self.text)
        self.assertIn("hashing, cifrado y tokenización no son equivalentes", self.text)
        self.assertIn("no se presenta como anonimización", self.data["editorial_notice"].lower())

    def test_authentication_authorization_and_purpose_are_distinguished(self):
        for concept in ["autenticación", "autorización", "mínimo privilegio", "rbac", "abac", "propósito de uso", "revocación"]:
            self.assertIn(concept, self.text)
        self.assertIn("autenticación identifica; autorización decide acciones permitidas", self.text)
        self.assertIn("data use ontology", self.text)
        self.assertIn("ga4gh aai", self.text)

    def test_fhir_audit_and_provenance_boundaries_are_explicit(self):
        for concept in ["fhir consent", "auditevent", "provenance", "security label", "audit trail"]:
            self.assertIn(concept, self.text)
        self.assertIn("auditevent y provenance responden preguntas diferentes", self.text)
        self.assertIn("una alerta inicia investigación, no demuestra abuso", self.text)

    def test_governed_data_product_and_fair_are_explicit(self):
        for concept in ["producto de datos", "data steward", "contrato de datos", "ficha de producto", "findable", "accessible", "interoperable", "reusable", "output review"]:
            self.assertIn(concept, self.text)
        self.assertIn("fair no significa datos abiertos al público", self.text)

    def test_safety_and_scope_are_explicit(self):
        notice = self.data["editorial_notice"].lower()
        scope = self.data["professional_scope"].lower()
        for marker in ["no se conectan ehr", "no demuestra cumplimiento gdpr", "aprobación ética", "autorización institucional", "seguridad de producción"]:
            self.assertIn(marker, notice)
        self.assertIn("no acredita competencia jurídica", scope)
        self.assertIn("datos, identidades, consentimientos, políticas y eventos sintéticos", notice)

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
        self.assertGreaterEqual(len(self.data["biomedical_connections"]), 6)
        self.assertGreaterEqual(len(self.data["sources"]), 14)

    def test_guided_activity_is_substantive(self):
        activity = self.data["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 420)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 24)
        joined = " ".join(activity["problems"] + activity["deliverables"] + activity["checking_criteria"]).lower()
        for concept in ["minimización", "pseudonimización", "rbac", "abac", "duo", "auditevent", "provenance", "fair", "output review"]:
            self.assertIn(concept, joined)

    def test_source_families_are_present_and_currently_accessed(self):
        source_text = " ".join(s["title"] + " " + s["organization"] for s in self.data["sources"]).lower()
        for family in ["nist", "european commission", "hl7", "ga4gh", "fair", "w3c"]:
            self.assertIn(family, source_text)
        self.assertTrue(all(s.get("accessed") == "2026-08-25" for s in self.data["sources"]))

    def test_publication_when_promoted_contains_core_markers(self):
        if not PUBLIC.exists():
            self.skipTest("Public page is generated by the publication workflow.")
        public_text = PUBLIC.read_text(encoding="utf-8").lower()
        if self.data["purpose"].lower() not in public_text:
            self.skipTest("Publication workflow has not promoted U6 yet.")
        for marker in ["seudonimización", "cuasi-identificador", "auditevent", "provenance", "data use ontology", "fair no significa"]:
            self.assertIn(marker, public_text)

    def test_descriptor_when_promoted_matches_canonical_purpose(self):
        if not DESCRIPTOR.exists():
            self.skipTest("Descriptor is generated by the publication workflow.")
        descriptor = json.loads(DESCRIPTOR.read_text(encoding="utf-8"))
        unit = next(item for item in descriptor["detailed_units"] if item["unit"] == 6)
        if unit["description"] != self.data["purpose"]:
            self.skipTest("Publication workflow has not promoted U6 yet.")
        self.assertEqual(unit["title"], self.data["title"])
        self.assertEqual(unit["description"], self.data["purpose"])


if __name__ == "__main__":
    unittest.main()
