from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "etica-responsabilidad-social" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "etica-responsabilidad-social" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class EticaResponsabilidadSocialUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self):
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "etica-responsabilidad-social")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_moral_scoring_are_removed(self):
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("v(a)=", self.text)
        self.assertNotIn("\\sum_{i=1}^{k}", self.text)
        self.assertIn("no existe una métrica universal de fairness", self.text)

    def test_theory_is_data_and_ai_governance_specific(self):
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "privacidad",
            "protección de datos",
            "confidencialidad",
            "seguridad",
            "seudonimización",
            "anonimización",
            "proxy",
            "desempeño agregado",
            "subgrupos",
            "fairness",
            "explicación post hoc",
            "supervisión humana",
            "sesgo de automatización",
            "monitorizar",
            "rollback",
            "incidente",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no son sinónimos", theory)
        self.assertIn("no convierte una predicción en una relación causal", theory)

    def test_pedagogy_is_progressive_synthetic_and_operational(self):
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        first = activities[0]
        self.assertGreaterEqual(first.get("duration_minutes", 0), 270)
        self.assertGreaterEqual(len(first["instructions"]), 14)
        self.assertGreaterEqual(len(first["problems"]), 16)
        self.assertGreaterEqual(len(first["deliverables"]), 10)
        self.assertGreaterEqual(len(first["checking_criteria"]), 10)
        self.assertIn("apoyo reducido", activities[1]["title"].casefold())
        self.assertIn("autónomo", activities[2]["title"].casefold())
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintético", activity_text)
        self.assertIn("no uses historias clínicas", activity_text)
        self.assertIn("umbral", activity_text)
        self.assertIn("rollback", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self):
        self.assertGreaterEqual(len(self.unit["glossary"]), 30)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 12)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "minimización de datos",
            "seudonimización",
            "proxy",
            "sesgo algorítmico",
            "fairness algorítmica",
            "cambio de distribución",
            "explicabilidad",
            "contestabilidad",
            "supervisión humana",
            "sesgo de automatización",
            "monitorización posdespliegue",
            "gestión de incidentes",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_version_aware(self):
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(source["verification_status"] == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        for url in (
            "https://www.who.int/publications/i/item/9789240029200",
            "https://www.nist.gov/itl/ai-risk-management-framework",
            "https://oecd.ai/en/ai-principles",
            "https://eur-lex.europa.eu/eli/reg/2016/679/2016-05-04/eng",
            "https://eur-lex.europa.eu/eli/reg/2024/1689/oj?locale=en",
            "https://digital-strategy.ec.europa.eu/en/policies/enforcement-ai-act",
            "https://pubmed.ncbi.nlm.nih.gov/31649194/",
            "https://pubmed.ncbi.nlm.nih.gov/34711379/",
            "https://pubmed.ncbi.nlm.nih.gov/38626948/",
        ):
            self.assertIn(url, urls)
        nist = next(s for s in sources if "Risk Management Framework" in s["title"])
        oecd = next(s for s in sources if s["title"] == "OECD AI Principles")
        enforcement = next(s for s in sources if s["title"] == "The enforcement framework of the AI Act")
        self.assertIn("proceso de revisión", nist["description"])
        self.assertIn("2024", oecd["description"])
        self.assertIn("7 de agosto de 2026", enforcement["description"])

    def test_scope_preserves_legal_clinical_and_later_unit_boundaries(self):
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        for phrase in (
            "no constituye revisión disciplinar externa",
            "asesoría jurídica",
            "ciberseguridad",
            "validación clínica",
            "autorización regulatoria",
            "datos reales",
            "u4",
            "u5",
            "u6",
        ):
            self.assertIn(phrase, notice)
        self.assertIn("sin convertir una métrica técnica", purpose)
        self.assertIn("aceptabilidad ética", purpose)


if __name__ == "__main__":
    unittest.main()
