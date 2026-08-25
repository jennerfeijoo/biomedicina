from __future__ import annotations

import json
import unittest
from pathlib import Path

# Final validation trigger after deterministic public-site synchronization.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "etica-responsabilidad-social" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "etica-responsabilidad-social" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class EticaResponsabilidadSocialUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "etica-responsabilidad-social")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed_and_scope_is_specific(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        for concept in (
            "seudonimización",
            "anonimización",
            "limitación de finalidad",
            "sesgo algorítmico",
            "desempeño por subgrupos",
            "explicabilidad",
            "sesgo de automatización",
            "supervisión humana",
            "monitorización posdespliegue",
        ):
            self.assertIn(concept, self.text)

    def test_theory_is_substantive_and_lifecycle_oriented(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        headings = " ".join(section["heading"] for section in sections).casefold()
        for concept in ("privacidad", "sesgo", "transparencia", "supervisión humana", "ciclo de vida"):
            self.assertIn(concept, headings)
        self.assertIn("u2 abordó consentimiento", self.text)
        self.assertIn("u3 se concentra", self.text)
        self.assertIn("validación previa no sustituye monitorización", self.text)

    def test_privacy_fairness_and_explainability_boundaries_are_explicit(self) -> None:
        self.assertIn("privacidad, confidencialidad, seguridad y protección de datos", self.text)
        self.assertIn("seudonimización no equivale a anonimización", self.text)
        self.assertIn("no existe una única métrica de fairness", self.text)
        self.assertIn("una explicación no demuestra causalidad", self.text)
        self.assertIn("salud por sí sola no sustituye el análisis jurídico", self.text)
        self.assertIn("cumplimiento regulatorio con aceptabilidad ética", self.text)

    def test_quantitative_subgroup_example_is_present_without_moral_score(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("\\mathrm{TPR}_g=\\frac{TP_g}{TP_g+FN_g}", equations)
        self.assertIn("\\Delta_{TPR}=\\mathrm{TPR}_A-\\mathrm{TPR}_B", equations)
        examples = json.dumps(self.unit["worked_examples"], ensure_ascii=False).casefold()
        self.assertIn("auroc global 0,90", examples)
        self.assertIn("0,88", examples)
        self.assertIn("0,64", examples)
        self.assertIn("no un veredicto moral", examples)

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 14)
        self.assertGreaterEqual(len(activity["deliverables"]), 7)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 14)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("no cargues datos de pacientes", text)
        self.assertIn("información personal real", text)
        self.assertIn("mapa de sesgo", text)
        self.assertIn("posdespliegue", text)
        self.assertIn("no la presentes como autorización clínica", text)

    def test_learning_scaffolds_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 12)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "privacidad",
            "seudonimización",
            "proxy",
            "fairness algorítmica",
            "explicabilidad",
            "sesgo de automatización",
            "drift",
            "monitorización posdespliegue",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_cover_governance_and_empirical_bias(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(source.get("verification_status") == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        expected = {
            "https://www.who.int/publications/i/item/9789240029200",
            "https://www.who.int/publications/i/item/9789240078871",
            "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
            "https://eur-lex.europa.eu/eli/reg/2016/679/oj",
            "https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
            "https://pubmed.ncbi.nlm.nih.gov/31649194/",
            "https://pubmed.ncbi.nlm.nih.gov/30508424/",
        }
        self.assertTrue(expected.issubset(urls))

    def test_legal_clinical_and_regulatory_overclaiming_is_blocked(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for boundary in (
            "no constituye revisión disciplinar externa",
            "asesoría jurídica",
            "interpretación vinculante del gdpr o del ai act",
            "evaluación de conformidad",
            "certificación regulatoria",
            "validación clínica",
            "autorización de despliegue",
        ):
            self.assertIn(boundary, notice)
        self.assertIn("jurisdicción", notice)
        self.assertIn("normativa vigente", notice)


if __name__ == "__main__":
    unittest.main()
