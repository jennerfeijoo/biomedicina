import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/historia-filosofia-ciencia/units/unit-04.json"
MIRROR = ROOT / "data/generated_units/historia-filosofia-ciencia/unit-04.json"
DESCRIPTOR = ROOT / "data/subjects/gestion-etica-comunicacion/historia-filosofia-ciencia.json"
GENERIC_MARKERS = (
    "Concepto de la unidad que debe definirse mediante entidades observables",
    "V(a)=\\sum_{i=1}^{k} w_i r_i(a)",
    "modelo multicriterio transparente",
)


class HistoriaFilosofiaCienciaUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.mirror = json.loads(MIRROR.read_text(encoding="utf-8"))

    def test_source_and_mirror_are_exact(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit, self.mirror)

    def test_identity_and_purpose_are_disciplinary(self) -> None:
        self.assertEqual(self.unit["subject_id"], "historia-filosofia-ciencia")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["slug"], "medicion-clasificacion-y-objetividad")
        purpose = self.unit["purpose"].casefold()
        for phrase in ("mensurando", "calibraciones", "incertidumbre", "reglas de clasificación", "objetividad"):
            self.assertIn(phrase, purpose)

    def test_template_and_generic_score_are_absent(self) -> None:
        text = SOURCE.read_text(encoding="utf-8")
        for marker in GENERIC_MARKERS:
            self.assertNotIn(marker, text)

    def test_academic_depth_and_pedagogy(self) -> None:
        self.assertGreaterEqual(len(self.unit["learning_objectives"]), 6)
        self.assertGreaterEqual(len(self.unit["theory_sections"]), 5)
        for section in self.unit["theory_sections"]:
            self.assertGreaterEqual(len(section["paragraphs"]), 5)
            self.assertGreaterEqual(len(section["key_points"]), 5)
        self.assertGreaterEqual(len(self.unit["glossary"]), 40)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["guided_activities"]), 3)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 18)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        self.assertGreaterEqual(len(self.unit["sources"]), 16)

    def test_measurement_section_separates_indication_result_and_model(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in ("mensurando", "indicación", "resultado de medición", "modelo de medición", "precisión", "incertidumbre"):
            self.assertIn(phrase, text)
        self.assertIn("la indicación es la salida", text)
        self.assertIn("no debe confundirse con el resultado de medición", text)

    def test_traceability_is_property_of_result_not_instrument(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        self.assertIn("trazabilidad metrológica es una propiedad de un resultado de medición", text)
        self.assertIn("decir «este instrumento es trazable» abrevia de forma peligrosa", text)
        self.assertIn("trazabilidad y aptitud para uso son independientes", text)
        key_points = " ".join(self.unit["theory_sections"][1]["key_points"]).casefold()
        self.assertIn("incertidumbre sea adecuada para el uso previsto", key_points)

    def test_classification_section_distinguishes_reference_and_decision_limits(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in ("variable continua", "umbral", "intervalo de referencia", "límite de decisión", "incertidumbre", "version"):
            self.assertIn(phrase, text)
        self.assertIn("no son equivalentes", text)
        equations = json.dumps(self.unit["theory_sections"][2].get("equations", []), ensure_ascii=False)
        self.assertIn("C_t(x)", equations)
        self.assertNotIn("V(a)", equations)

    def test_objectivity_section_blocks_naive_value_free_caricature(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in ("objetividad tiene varios sentidos", "automatización no elimina necesariamente el juicio", "juicio experto", "valores epistémicos", "valores contextuales", "riesgo inductivo", "crítica comunitaria"):
            self.assertIn(phrase, text)
        self.assertIn("no existe", json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold())

    def test_integrated_activity_preserves_continuous_values_and_uncertainty(self) -> None:
        workshop = self.unit["guided_activities"][1]
        text = json.dumps(workshop, ensure_ascii=False).casefold()
        self.assertGreaterEqual(len(workshop["problems"]), 20)
        self.assertGreaterEqual(len(workshop["deliverables"]), 10)
        self.assertGreaterEqual(len(workshop["checking_criteria"]), 25)
        for phrase in ("valores continuos", "calibración", "umbral", "incertidumbre", "trazabilidad", "revisión independiente"):
            self.assertIn(phrase, text)

    def test_glossary_contains_metrology_classification_and_values(self) -> None:
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        required = {
            "mensurando", "indicación", "resultado de medición", "calibración",
            "trazabilidad metrológica", "incertidumbre de medición", "clasificación",
            "intervalo de referencia", "límite de decisión", "objetividad",
            "valor epistémico", "valor contextual", "riesgo inductivo", "aptitud para uso",
        }
        self.assertTrue(required.issubset(terms))

    def test_sources_are_verified_and_include_primary_metrology_authorities(self) -> None:
        self.assertTrue(all(s.get("verification_status") == "verified_directly" for s in self.unit["sources"]))
        organizations = " ".join(s["organization"] for s in self.unit["sources"]).casefold()
        urls = " ".join(s["url"] for s in self.unit["sources"])
        for org in ("bipm", "nist", "stanford", "world health organization"):
            self.assertIn(org, organizations)
        self.assertIn("jcgm200-2012", urls.casefold())
        self.assertIn("30047297", urls)

    def test_clinical_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for phrase in ("todos los valores", "sintéticos", "no interpreta resultados de laboratorio", "no recomienda diagnóstico", "no certifica"):
            self.assertIn(phrase, notice)

    def test_published_descriptor_matches_canonical_purpose(self) -> None:
        self.assertTrue(DESCRIPTOR.exists())
        descriptor = json.loads(DESCRIPTOR.read_text(encoding="utf-8"))
        detailed = next((u for u in descriptor.get("detailed_units", []) if u.get("unit") == 4), None)
        self.assertIsNotNone(detailed)
        self.assertEqual(detailed["description"], self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()
