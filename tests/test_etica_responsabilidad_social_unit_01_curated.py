# Final user-authored trigger after moral-residue and publication metadata synchronization.
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "etica-responsabilidad-social" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "etica-responsabilidad-social" / "unit-01.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class EticaResponsabilidadSocialUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self):
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_moral_scoring_are_removed(self):
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("v(a)=", text)
        self.assertIn("no existe una suma ponderada universal", text)
        self.assertIn("sin puntuación moral agregada", text)

    def test_theory_distinguishes_theories_principles_rights_and_law(self):
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "consecuencialismo",
            "deontológicos",
            "ética de la virtud",
            "ética del cuidado",
            "principlismo",
            "autonomía",
            "beneficencia",
            "no maleficencia",
            "justicia",
            "dignidad",
            "vulnerabilidad",
            "solidaridad",
            "pluralismo",
            "residuo moral",
        ):
            self.assertIn(concept, theory)
        self.assertIn("legalidad y justificación moral responden a preguntas distintas", theory)

    def test_pedagogy_has_progressive_support_and_synthetic_boundary(self):
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertGreaterEqual(activities[0].get("duration_minutes", 0), 270)
        self.assertGreaterEqual(len(activities[0]["instructions"]), 12)
        self.assertGreaterEqual(len(activities[0]["problems"]), 16)
        self.assertGreaterEqual(len(activities[0]["deliverables"]), 10)
        self.assertGreaterEqual(len(activities[0]["checking_criteria"]), 10)
        self.assertIn("apoyo reducido", activities[1]["title"].casefold())
        self.assertIn("autónomo", activities[2]["title"].casefold())
        text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintético", text)
        self.assertIn("no uses historias clínicas", text)
        self.assertIn("no se inventan normas jurídicas", text)

    def test_glossary_examples_errors_and_assessment_are_specific(self):
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "teoría normativa",
            "consecuencialismo",
            "deontología",
            "ética de la virtud",
            "ética del cuidado",
            "principlismo",
            "autonomía",
            "beneficencia",
            "no maleficencia",
            "justicia",
            "residuo moral",
            "deliberación ética",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_current(self):
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(source["verification_status"] == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        for url in (
            "https://www.unesco.org/en/ethics-science-technology/bioethics-and-human-rights?hub=387",
            "https://www.unesco.org/en/ethics-science-technology/education",
            "https://www.hhs.gov/ohrp/regulations-and-policy/belmont-report/read-the-belmont-report/index.html",
            "https://www.wma.net/policies-post/wma-declaration-of-helsinki/",
            "https://cioms.ch/wp-content/uploads/2017/01/WEB-CIOMS-EthicalGuidelines.pdf",
            "https://www.coe.int/en/web/human-rights-and-biomedicine/the-oviedo-convention-and-human-rights-principles-regarding-health",
            "https://pubmed.ncbi.nlm.nih.gov/24182363/",
        ):
            self.assertIn(url, urls)
        helsinki = next(s for s in sources if "Helsinki" in s["title"])
        self.assertIn("2024", helsinki["description"])

    def test_scope_preserves_unit_boundaries_and_professional_limits(self):
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        for phrase in (
            "no constituyen revisión disciplinar externa",
            "consulta de ética clínica",
            "asesoría jurídica",
            "decisiones reales",
            "sintéticos",
        ):
            self.assertIn(phrase, notice)
        self.assertIn("u2–u6", notice)
        self.assertIn("sin convertir los principios en una fórmula automática", purpose)
        self.assertIn("decisión clínica, jurídica o regulatoria real", purpose)


if __name__ == "__main__":
    unittest.main()
