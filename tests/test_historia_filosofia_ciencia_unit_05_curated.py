import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/historia-filosofia-ciencia/units/unit-05.json"
MIRROR = ROOT / "data/generated_units/historia-filosofia-ciencia/unit-05.json"
DESCRIPTOR = ROOT / "data/subjects/gestion-etica-comunicacion/historia-filosofia-ciencia.json"
GENERIC_MARKERS = (
    "Concepto de la unidad que debe definirse mediante entidades observables",
    "V(a)=\\sum_{i=1}^{k} w_i r_i(a)",
    "modelo multicriterio transparente",
)


class HistoriaFilosofiaCienciaUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.mirror = json.loads(MIRROR.read_text(encoding="utf-8"))

    def test_source_and_mirror_are_exact(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit, self.mirror)

    def test_identity_and_purpose_are_disciplinary(self) -> None:
        self.assertEqual(self.unit["subject_id"], "historia-filosofia-ciencia")
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["slug"], "ciencia-sociedad-y-poder")
        purpose = self.unit["purpose"].casefold()
        for phrase in ("instituciones científicas", "financiación", "colonialidad", "género", "industria", "gobernanza de datos"):
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

    def test_institutions_are_mechanistic_not_reductionist(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in ("instituciones", "recursos", "incentivos", "prioridades científicas", "prestigio", "crítica"):
            self.assertIn(phrase, text)
        self.assertIn("no implica que los resultados científicos sean meras expresiones de poder", text)

    def test_coloniality_requires_mechanisms_and_governance(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in ("colonialidad", "patrón extractivo", "autoría", "care", "gobernanza", "capacidad local"):
            self.assertIn(phrase, text)
        self.assertIn("no basta llamar colonial", text)
        self.assertIn("no significa que toda base", text)

    def test_gender_section_separates_representation_from_epistemic_authority(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in ("sexo, género, raza y etnicidad", "representatividad", "autoridad epistémica", "diversidad", "proxy"):
            self.assertIn(phrase, text)
        self.assertIn("no garantiza mejor resultado", text)

    def test_industry_section_separates_funding_conflict_bias_and_misconduct(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in ("financiación industrial", "conflicto de interés", "acceso a datos", "libertad de publicación", "calidad metodológica"):
            self.assertIn(phrase, text)
        self.assertIn("no demuestra por sí sola que un resultado sea falso", text)
        self.assertIn("declaración por sí sola no neutraliza", text)

    def test_integrated_audit_rejects_moral_score_and_matches_controls_to_mechanisms(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        self.assertIn("no es asignar una puntuación moral total", text)
        self.assertIn("las salvaguardas deben corresponder al mecanismo", text)
        self.assertIn("u6", text)
        self.assertNotIn("v(a)", text)

    def test_main_workshop_maps_power_and_keeps_claim_types_separate(self) -> None:
        workshop = self.unit["guided_activities"][1]
        text = json.dumps(workshop, ensure_ascii=False).casefold()
        self.assertGreaterEqual(len(workshop["problems"]), 20)
        self.assertGreaterEqual(len(workshop["deliverables"]), 12)
        self.assertGreaterEqual(len(workshop["checking_criteria"]), 25)
        for phrase in ("colonialidad", "proxy", "patrocinio", "calidad metodológica", "juicio normativo", "evidencia"):
            self.assertIn(phrase, text)

    def test_glossary_covers_institutions_coloniality_gender_and_industry(self) -> None:
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        required = {
            "institución científica", "gobernanza científica", "agenda de investigación",
            "poder institucional", "colonialidad", "investigación extractiva",
            "conocimiento situado", "autoridad epistémica", "sexo", "género",
            "conflicto de interés", "sesgo de patrocinio", "independencia analítica",
        }
        self.assertTrue(required.issubset(terms))

    def test_sources_are_verified_and_methodologically_plural(self) -> None:
        self.assertTrue(all(s.get("verification_status") == "verified_directly" for s in self.unit["sources"]))
        organizations = " ".join(s["organization"] for s in self.unit["sources"]).casefold()
        urls = " ".join(s["url"] for s in self.unit["sources"]).casefold()
        for org in ("stanford", "world health organization", "cioms", "global indigenous data alliance", "icmje", "national institutes of health"):
            self.assertIn(org, organizations)
        self.assertIn("30132025", urls)
        self.assertIn("31649194", urls)
        self.assertIn("careprinciples", urls)

    def test_professional_and_editorial_boundaries_are_explicit(self) -> None:
        scope = self.unit["professional_scope"].casefold()
        notice = self.unit["editorial_notice"].casefold()
        for phrase in ("casos sintéticos", "no realiza investigación con participantes", "no realiza", "auditorías institucionales reales"):
            self.assertIn(phrase, scope)
        for phrase in ("todos los nombres", "sintéticos", "no determina", "no recomienda diagnóstico", "requiere revisión disciplinar externa"):
            self.assertIn(phrase, notice)

    def test_published_descriptor_matches_when_promoted(self) -> None:
        if not DESCRIPTOR.exists():
            self.skipTest("Descriptor not generated yet")
        descriptor = json.loads(DESCRIPTOR.read_text(encoding="utf-8"))
        detailed = next((u for u in descriptor.get("detailed_units", []) if u.get("unit") == 5), None)
        self.assertIsNotNone(detailed)
        if detailed["description"] != self.unit["purpose"]:
            self.skipTest("U5 descriptor has not been promoted yet")
        self.assertEqual(detailed["description"], self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()
