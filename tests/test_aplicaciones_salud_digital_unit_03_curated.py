from __future__ import annotations

import json
import unittest
from pathlib import Path

# Final user-authored trigger after generated publication synchronization.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "aplicaciones-salud-digital" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "aplicaciones-salud-digital" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class AplicacionesSaludDigitalUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "aplicaciones-salud-digital")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed_and_scope_is_specific(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "teleconsulta sincrónica",
            "monitorización remota",
            "cadena de medición",
            "carga de alertas",
            "ruta de escalado",
            "contingencia",
        ):
            self.assertIn(concept, text)
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no demuestra eficacia clínica", purpose)
        self.assertIn("no valida un dispositivo concreto", purpose)
        self.assertIn("no sustituye evaluación regulatoria", purpose)

    def test_theory_covers_service_sensor_alert_and_safety_layers(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = json.dumps(sections, ensure_ascii=False).casefold()
        for phrase in (
            "calidad de telehealth",
            "sensor, contacto con el cuerpo",
            "completitud y latencia",
            "valor predictivo positivo",
            "persona-tiempo",
            "fallar de manera visible",
            "el silencio del sistema",
            "desempeño técnico, proceso asistencial y resultado clínico",
        ):
            self.assertIn(phrase, theory)

    def test_metrics_are_remote_monitoring_specific_and_bounded(self) -> None:
        equations = [eq for section in self.unit["theory_sections"] for eq in section.get("equations", [])]
        latex = {eq["latex"] for eq in equations}
        self.assertIn("C=\\frac{N_{datos\\ utilizables}}{N_{datos\\ esperados}}\\times100\\%", latex)
        self.assertIn("L_i=t_{disponible,i}-t_{medicion,i}", latex)
        self.assertIn("PPV=\\frac{Se\\,\\pi}{Se\\,\\pi+(1-Sp)(1-\\pi)}", latex)
        self.assertIn("B=\\frac{N_{alertas}}{N_{personas}\\cdot T}", latex)
        meanings = " ".join(eq["meaning"] for eq in equations).casefold()
        self.assertIn("completitud", meanings)
        self.assertIn("carga de alertas", meanings)

    def test_pedagogy_is_progressive_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertGreaterEqual(sum(len(a.get("problems", [])) for a in activities), 30)
        self.assertTrue(all(len(a.get("instructions", [])) >= 5 for a in activities))
        self.assertTrue(all(len(a.get("deliverables", [])) >= 6 for a in activities))
        self.assertTrue(all(len(a.get("checking_criteria", [])) >= 8 for a in activities))
        text = json.dumps(activities, ensure_ascii=False).casefold()
        for phrase in (
            "caso ficticio",
            "datos sintéticos",
            "no conectes dispositivos reales",
            "ppv",
            "persona-día",
            "evidencia que faltaría",
        ):
            self.assertIn(phrase, text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {item["term"].casefold() for item in self.unit["glossary"]}
        for term in (
            "telemedicina",
            "teleconsulta sincrónica",
            "monitorización remota",
            "completitud",
            "latencia",
            "alerta",
            "valor predictivo positivo",
            "carga de alertas",
            "contingencia",
            "equidad digital",
        ):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_current_for_the_unit_scope(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(s.get("verification_status") == "verified_directly" for s in sources))
        urls = {s["url"] for s in sources}
        for url in (
            "https://www.who.int/europe/publications/i/item/WHO-EURO-2024-9475-49247-73556",
            "https://www.who.int/publications/b/74046",
            "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/digital-health-technologies-remote-data-acquisition-clinical-investigations",
            "https://www.nice.org.uk/corporate/ecd7",
            "https://pubmed.ncbi.nlm.nih.gov/33420338/",
            "https://pubmed.ncbi.nlm.nih.gov/40513050/",
        ):
            self.assertIn(url, urls)

    def test_editorial_notice_keeps_clinical_regulatory_and_cross_unit_limits(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no constituyen revisión disciplinar externa",
            "no se contacta a pacientes ni profesionales",
            "no se conectan dispositivos reales",
            "interoperabilidad se desarrolla en u4",
            "eficacia clínica y económica en u5",
            "privacidad, regulación, ciberseguridad e implementación en u6",
        ):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
