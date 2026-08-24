from __future__ import annotations

import json
import unittest
from pathlib import Path

# Final user-authored trigger after publication metadata synchronization.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "aplicaciones-salud-digital" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "aplicaciones-salud-digital" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class AplicacionesSaludDigitalUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "aplicaciones-salud-digital")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_and_cross_unit_template_content_is_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("diccionarios, perfiles de datos, pruebas de interoperabilidad", text)
        self.assertNotIn("ppv=", text)
        for concept in ("contexto de uso", "wcag 2.2", "evaluación formativa", "recorrido cognitivo"):
            self.assertIn(concept, text)

    def test_theory_is_human_centered_and_has_clear_boundaries(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "necesidad de usuario",
            "requisito de interacción",
            "efectividad, eficiencia y satisfacción",
            "tecnologías de asistencia",
            "think-aloud",
            "una tasa alta de finalización",
            "tarea crítica",
            "validación de factores humanos",
        ):
            self.assertIn(concept, theory)
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no implementa interoperabilidad", purpose)
        self.assertIn("no demuestra beneficio clínico o económico", purpose)
        self.assertIn("no constituye validación regulatoria", purpose)

    def test_usability_metrics_are_not_clinical_surrogates(self) -> None:
        equations = [equation for section in self.unit["theory_sections"] for equation in section.get("equations", [])]
        latex = {equation["latex"] for equation in equations}
        self.assertIn("CR=\\frac{N_{tareas\\ completadas}}{N_{intentos\\ validos}}\\times100\\%", latex)
        self.assertIn("R_e=\\frac{N_{errores\\ de\\ uso}}{N_{oportunidades\\ observadas}}", latex)
        meanings = " ".join(e["meaning"] for e in equations).casefold()
        self.assertIn("no beneficio clínico", meanings)

    def test_pedagogy_is_progressive_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertGreaterEqual(sum(len(a.get("problems", [])) for a in activities), 30)
        self.assertTrue(all(len(a.get("instructions", [])) >= 5 for a in activities))
        self.assertTrue(all(len(a.get("deliverables", [])) >= 6 for a in activities))
        self.assertTrue(all(len(a.get("checking_criteria", [])) >= 8 for a in activities))
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintético", activity_text)
        self.assertIn("no entrevistes ni observes personas reales", activity_text)
        self.assertIn("prototipo", activity_text)
        self.assertIn("tasa de finalización", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 4)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {item["term"].casefold() for item in self.unit["glossary"]}
        for term in (
            "contexto de uso",
            "requisito de interacción",
            "usabilidad",
            "accesibilidad",
            "wcag 2.2",
            "error de uso",
            "prototipo",
            "evaluación formativa",
            "tarea crítica",
            "validación de factores humanos",
        ):
            self.assertIn(term, terms)

    def test_sources_are_current_traceable_and_scope_regulation_carefully(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(s.get("verification_status") == "verified_directly" for s in sources))
        urls = {s["url"] for s in sources}
        for url in (
            "https://www.iso.org/standard/77520.html",
            "https://www.iso.org/standard/63500.html",
            "https://www.w3.org/TR/WCAG22/",
            "https://webstore.iec.ch/en/publication/59980",
            "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/applying-human-factors-and-usability-engineering-medical-devices",
            "https://pubmed.ncbi.nlm.nih.gov/39546781/",
        ):
            self.assertIn(url, urls)

    def test_editorial_notice_keeps_research_clinical_and_regulatory_limits(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no constituyen revisión disciplinar externa",
            "estudio con usuarios",
            "aprobación ética",
            "validación clínica",
            "conformidad wcag certificada",
            "validación formal de factores humanos",
            "datos sintéticos",
            "interoperabilidad en u4",
            "evaluación clínica/económica en u5",
        ):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
