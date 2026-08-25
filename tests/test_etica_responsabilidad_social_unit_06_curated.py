from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "etica-responsabilidad-social" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "etica-responsabilidad-social" / "unit-06.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class EticaResponsabilidadSocialUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "etica-responsabilidad-social")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["status"], "review")
        purpose = self.unit["purpose"].casefold()
        self.assertIn("integrar el razonamiento ético del curso", purpose)
        self.assertIn("no sustituir comités de ética", purpose)

    def test_generic_template_and_generic_mcdm_equation_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        raw = json.dumps(self.unit, ensure_ascii=False)
        self.assertNotIn(r"V(a)=\sum", raw)
        for concept in (
            "deliberación ética", "participación social", "conflicto de interés",
            "transparencia", "rendición de cuentas", "apelación",
            "desacuerdo razonable", "registro de decisión",
        ):
            self.assertIn(concept, self.text)

    def test_theory_is_substantive_and_integrates_previous_units(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        headings = " ".join(section["heading"] for section in sections).casefold()
        for concept in ("deliberación ética", "actores y participación", "conflictos de interés", "transparencia", "rendición de cuentas"):
            self.assertIn(concept, headings)
        for marker in ("u1 aporta", "u2, obligaciones de investigación", "u3, gobernanza de datos e ia", "u4, acceso y equidad", "u5, ambiente y cadena de suministro"):
            self.assertIn(marker, self.text)

    def test_deliberation_is_not_taught_as_moral_scoring(self) -> None:
        self.assertIn("hechos, incertidumbres, valores", self.text)
        self.assertIn("ayuda de trazabilidad, no una fórmula de optimización", self.text)
        self.assertIn("no elimina los juicios de valor", self.text)
        self.assertIn("no requiere", self.text)
        self.assertIn("consenso", self.text)
        self.assertIn("opinión minoritaria", self.text)

    def test_participation_is_meaningful_and_power_aware(self) -> None:
        for concept in (
            "afectación, poder, conocimiento, representación",
            "asimetrías de poder", "barreras de idioma", "discapacidad",
            "participación significativa", "participación social",
        ):
            self.assertIn(concept, self.text)
        self.assertIn("participación tampoco equivale a consentimiento", self.text)
        self.assertIn("no convierte cada preferencia en veto", self.text)

    def test_conflict_of_interest_is_assessed_and_managed_not_merely_disclosed(self) -> None:
        self.assertIn("no constituye automáticamente un conflicto de interés", self.text)
        for concept in (
            "conflicto real", "potencial", "aparente", "recusarse",
            "revisión independiente", "proporcional", "plan de manejo",
        ):
            self.assertIn(concept, self.text)
        self.assertIn("no equivale por sí mismo a corrupción", self.text)

    def test_transparency_has_reason_giving_and_confidentiality_boundaries(self) -> None:
        self.assertIn("transparencia no significa publicar todo", self.text)
        self.assertIn("privacidad, confidencialidad", self.text)
        self.assertIn("razones", self.text)
        self.assertIn("registro de decisión", self.text)
        self.assertIn("opinión minoritaria", self.text)
        self.assertIn("versión pública", self.text)

    def test_accountability_has_revision_appeal_and_named_responsibility(self) -> None:
        for concept in (
            "quién recomienda", "quién decide", "quién implementa", "quién supervisa",
            "desencadenante", "vía de apelación", "nueva evidencia", "queja fundamentada",
        ):
            self.assertIn(concept, self.text)
        for condition in ("publicidad", "relevancia", "revisión o apelación", "aseguramiento o regulación"):
            self.assertIn(condition, self.text)
        self.assertIn("no una garantía universal de corrección ética", self.text)

    def test_guided_activity_is_capstone_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 10)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 20)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("no cargues datos de pacientes", text)
        self.assertIn("u1–u5", text)
        self.assertIn("no uses una suma ponderada", text)
        self.assertIn("opinión minoritaria", text)
        self.assertIn("desencadenantes de revisión", text)
        self.assertIn("vía de apelación", text)

    def test_learning_scaffolds_are_specific_and_sufficient(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 13)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "deliberación ética", "participación social", "asimetría de poder",
            "conflicto de interés real", "conflicto de interés potencial",
            "conflicto de interés aparente", "declaración de intereses",
            "recusación", "trazabilidad de decisión", "razón pública",
            "rendición de cuentas", "apelación", "accountability for reasonableness (a4r)",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_cover_deliberation_participation_and_governance(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(source.get("verification_status") == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        expected = {
            "https://www.who.int/publications/i/item/9789240085923",
            "https://www.who.int/publications/i/item/9789240027794/",
            "https://www.who.int/publications/i/item/9789241548960",
            "https://www.who.int/publications/i/item/9789240029200",
            "https://legalinstruments.oecd.org/public/doc/130/body-text.en.html",
            "https://cioms.ch/publications/product/international-ethical-guidelines-for-health-related-research-involving-humans/",
            "https://cioms.ch/publications/product/international-guidelines-on-good-governance-practice-for-research-institutions/",
            "https://www.bmj.com/content/337/bmj.a1850",
            "https://publications.gc.ca/site/eng/9.818019/publication.html",
        }
        self.assertTrue(expected.issubset(urls))

    def test_professional_overclaiming_is_blocked(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for boundary in (
            "no constituye revisión disciplinar externa",
            "dictamen de comité de ética", "aprobación de investigación",
            "evaluación regulatoria", "autorización clínica", "asesoría jurídica",
            "auditoría de gobernanza", "certificación de integridad",
            "investigación de conflicto de interés", "decisión de contratación",
            "recomendación sobre una tecnología real", "autorización de despliegue",
        ):
            self.assertIn(boundary, notice)
        self.assertIn("jurisdicción", notice)
        self.assertIn("normativa vigente", notice)
        self.assertIn("no como criterio universal de corrección moral", notice)


if __name__ == "__main__":
    unittest.main()
