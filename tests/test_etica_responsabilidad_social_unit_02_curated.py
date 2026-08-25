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
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "etica-responsabilidad-social")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        for concept in (
            "confusión terapéutica",
            "selección justa",
            "vulnerabilidad",
            "riesgo-beneficio",
            "capacidad decisional",
            "revisión independiente",
            "registro",
        ):
            self.assertIn(concept, self.text)

    def test_theory_is_substantive_and_scoped(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(
            paragraph for section in sections for paragraph in section["paragraphs"]
        ).casefold()
        self.assertIn("consentimiento informado no vuelve ético", theory)
        self.assertIn("calidad metodológica tiene dimensión ética", theory)
        self.assertIn("vulnerabilidad", theory)
        self.assertIn("contextuales o dinámicos", theory)
        self.assertIn("daños de exclusión", theory)
        self.assertIn("u1 aporta teorías", theory)
        self.assertIn("u3 profundizará privacidad", theory)

    def test_consent_and_jurisdictional_boundaries_are_explicit(self) -> None:
        consent_section = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        self.assertIn("firma", consent_section)
        self.assertIn("comprensión", consent_section)
        self.assertIn("voluntariedad", consent_section)
        self.assertIn("representación", consent_section)
        self.assertIn("asentimiento", consent_section)
        all_text = self.text
        self.assertIn("regulación estadounidense", all_text)
        self.assertIn("jurisdicción", all_text)
        self.assertIn("no constituye revisión disciplinar externa", all_text)
        self.assertIn("asesoría jurídica", all_text)
        self.assertIn("aprobación de un protocolo real", all_text)

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 5)
        self.assertGreaterEqual(len(activity["problems"]), 10)
        self.assertGreaterEqual(len(activity["deliverables"]), 6)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        activity_text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintéticos", activity_text)
        self.assertIn("no reclutes personas", activity_text)
        self.assertIn("no uses datos personales reales", activity_text)
        self.assertIn("valor y validez", activity_text)
        self.assertIn("teach-back", activity_text)

    def test_learning_scaffolds_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 16)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 3)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 8)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 8)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "valor social o científico",
            "validez científica",
            "selección justa",
            "consentimiento informado",
            "confusión terapéutica",
            "revisión independiente",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_authoritative(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(source.get("verification_status") == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        expected = {
            "https://www.wma.net/policies-post/wma-declaration-of-helsinki/",
            "https://cioms.ch/publications/product/international-ethical-guidelines-for-health-related-research-involving-humans/",
            "https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf",
            "https://www.hhs.gov/ohrp/regulations-and-policy/regulations/45-cfr-46/index.html",
            "https://pubmed.ncbi.nlm.nih.gov/10819955/",
        }
        self.assertTrue(expected.issubset(urls))

    def test_clinical_and_regulatory_overclaiming_is_blocked(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("dictamen de un comité de ética", notice)
        self.assertIn("asesoría jurídica", notice)
        self.assertIn("autorización regulatoria", notice)
        self.assertIn("aprobación de un protocolo real", notice)
        self.assertIn("recomendación clínica", notice)
        self.assertIn("jurisdicción", notice)


if __name__ == "__main__":
    unittest.main()
