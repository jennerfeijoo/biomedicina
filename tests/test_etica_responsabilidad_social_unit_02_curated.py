from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "etica-responsabilidad-social" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "etica-responsabilidad-social" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class EticaResponsabilidadSocialUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self):
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "etica-responsabilidad-social")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_moral_scoring_are_removed(self):
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("v(a)=", text)
        self.assertNotIn("\\sum_{i=1}^{k}", text)
        self.assertIn("no existe una puntuación moral agregada universal", text)

    def test_theory_is_research_ethics_specific_and_substantive(self):
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "valor social",
            "validez científica",
            "selección justa",
            "riesgo",
            "carga",
            "beneficio potencial directo",
            "vulnerabilidad",
            "consentimiento informado",
            "coerción",
            "influencia indebida",
            "confusión terapéutica",
            "revisión independiente",
            "registro",
        ):
            self.assertIn(concept, theory)
        self.assertIn("consentimiento", theory)
        self.assertIn("no se repara automáticamente", theory)

    def test_pedagogy_has_progressive_support_and_synthetic_boundary(self):
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        first = activities[0]
        self.assertGreaterEqual(first.get("duration_minutes", 0), 270)
        self.assertGreaterEqual(len(first["instructions"]), 12)
        self.assertGreaterEqual(len(first["problems"]), 16)
        self.assertGreaterEqual(len(first["deliverables"]), 10)
        self.assertGreaterEqual(len(first["checking_criteria"]), 10)
        self.assertIn("apoyo reducido", activities[1]["title"].casefold())
        self.assertIn("autónomo", activities[2]["title"].casefold())
        text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintético", text)
        self.assertIn("no reclutes", text)
        self.assertIn("no se inventan normas jurídicas", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self):
        self.assertGreaterEqual(len(self.unit["glossary"]), 25)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "valor social",
            "validez científica",
            "selección justa",
            "riesgo",
            "carga",
            "beneficio potencial directo",
            "vulnerabilidad",
            "consentimiento informado",
            "coerción",
            "influencia indebida",
            "confusión terapéutica",
            "revisión independiente",
            "good clinical practice",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_scope_is_current(self):
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(source["verification_status"] == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        for url in (
            "https://www.wma.net/policies-post/wma-declaration-of-helsinki/",
            "https://cioms.ch/publications/product/international-ethical-guidelines-for-health-related-research-involving-humans/",
            "https://www.hhs.gov/ohrp/regulations-and-policy/belmont-report/read-the-belmont-report/index.html",
            "https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106_ErrorCorrections_2025_1024.pdf",
            "https://www.who.int/publications/i/item/9789241502948",
            "https://pubmed.ncbi.nlm.nih.gov/10819955/",
        ):
            self.assertIn(url, urls)
        helsinki = next(s for s in sources if "Helsinki" in s["title"])
        ich = next(s for s in sources if "E6(R3)" in s["title"])
        self.assertIn("2024", helsinki["description"])
        self.assertIn("2025", ich["description"])
        self.assertIn("Good Clinical Practice", ich["type"])

    def test_scope_preserves_professional_and_later_unit_boundaries(self):
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        for phrase in (
            "no constituyen revisión disciplinar externa",
            "aprobación de un comité",
            "asesoría jurídica",
            "certificación good clinical practice",
            "autorización de reclutamiento",
            "sintéticos",
        ):
            self.assertIn(phrase, notice)
        self.assertIn("u3", notice)
        self.assertIn("sin reducir la decisión a una puntuación moral", purpose)
        self.assertIn("personas reales", purpose)


if __name__ == "__main__":
    unittest.main()
