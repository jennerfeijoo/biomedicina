import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/historia-filosofia-ciencia/units/unit-05.json"
MIRROR = ROOT / "data/generated_units/historia-filosofia-ciencia/unit-05.json"
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
        for phrase in ("instituciones", "financiación", "coloniales", "género", "industriales", "calidad epistémica"):
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

    def test_institutions_section_separates_power_from_truth_and_misconduct(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in ("agenda de investigación", "ausencia de evidencia", "poder científico", "incentivos institucionales"):
            self.assertIn(phrase, text)
        self.assertIn("no determinan mecánicamente qué resultados serán verdaderos", text)
        self.assertIn("poder no equivale necesariamente a abuso", text)

    def test_colonial_section_distinguishes_history_continuity_and_local_agency(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in ("colonialismo", "colonialidad", "agencia local", "circulación de conocimiento", "financiación", "autoría"):
            self.assertIn(phrase, text)
        self.assertIn("no debe aplicarse como etiqueta autosuficiente", text)
        self.assertIn("no convierte automáticamente cada resultado científico en falso", text)

    def test_gender_section_separates_participation_sex_gender_and_objectivity(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in ("participación", "sexo y género", "revitalization act", "conocimiento situado", "diversidad"):
            self.assertIn(phrase, text)
        self.assertIn("no garantiza por sí solo", text)
        self.assertIn("no significa que cada grupo posea una verdad privada", text)

    def test_industry_section_audits_mechanisms_instead_of_declaring_falsehood(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in ("conflicto de interés", "comparador", "desenlace", "patrocinio", "independencia analítica", "acceso a datos"):
            self.assertIn(phrase, text)
        self.assertIn("no demuestra por sí sola que un resultado sea falso", text)
        self.assertIn("no demuestra conducta impropia", text)

    def test_integrated_activity_keeps_epistemic_and_institutional_dimensions_separate(self) -> None:
        workshop = self.unit["guided_activities"][1]
        text = json.dumps(workshop, ensure_ascii=False).casefold()
        self.assertGreaterEqual(len(workshop["problems"]), 25)
        self.assertGreaterEqual(len(workshop["deliverables"]), 12)
        self.assertGreaterEqual(len(workshop["checking_criteria"]), 25)
        for phrase in ("mapa multidimensional de poder", "continuidad colonial", "sexo y género", "patrocinio", "independencia analítica", "justicia institucional"):
            self.assertIn(phrase, text)
        self.assertIn("no se usa una puntuación total de poder o justicia", text)

    def test_glossary_covers_institutions_coloniality_gender_and_sponsorship(self) -> None:
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        required = {
            "institución científica", "agenda de investigación", "poder científico",
            "colonialismo", "colonialidad", "circulación de conocimiento",
            "conocimiento situado", "género", "sexo como variable biológica",
            "conflicto de interés", "patrocinio industrial", "independencia analítica",
            "gobernanza compartida", "mapa de poder", "justicia epistémica",
        }
        self.assertTrue(required.issubset(terms))

    def test_sources_are_verified_and_cover_primary_institutional_and_empirical_evidence(self) -> None:
        self.assertTrue(all(s.get("verification_status") == "verified_directly" for s in self.unit["sources"]))
        organizations = " ".join(s["organization"] for s in self.unit["sources"]).casefold()
        urls = " ".join(s["url"] for s in self.unit["sources"]).casefold()
        for org in ("unesco", "stanford", "cochrane", "nih", "bmj"):
            self.assertIn(org, organizations)
        self.assertIn("mr000033", urls)
        self.assertIn("nih-revitalization-act-1993", urls)
        self.assertIn("pmc3865944", urls)

    def test_editorial_boundary_blocks_accusation_and_clinical_use(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "son sintéticos", "no acusa a personas o instituciones reales",
            "no infiere mala conducta", "no interpreta colonialidad sin mecanismo",
            "no recomienda decisiones clínicas", "u6 cubrirá reproducibilidad",
        ):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
