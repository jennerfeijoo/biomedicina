from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "laboratorio-bioinstrumentacion" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "laboratorio-bioinstrumentacion" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"
WRONG_DIAGNOSTIC_DEFINITION = "proporción de casos positivos de referencia que una prueba identifica correctamente"

# Final user-authored validation trigger after public-site synchronization.


class LaboratorioBioinstrumentacionUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "laboratorio-bioinstrumentacion")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_wrong_sensor_sensitivity_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        glossary = {entry["term"].casefold(): entry["definition"].casefold() for entry in self.unit["glossary"]}
        self.assertIn("sensibilidad metrológica", glossary)
        self.assertIn("cociente", glossary["sensibilidad metrológica"])
        self.assertNotIn(WRONG_DIAGNOSTIC_DEFINITION, glossary["sensibilidad metrológica"])
        self.assertIn("sensibilidad diagnóstica", glossary)
        self.assertIn("métrica clínica distinta", glossary["sensibilidad diagnóstica"])

    def test_theory_covers_static_dynamic_and_time_stability(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "sensibilidad de un sistema de medida",
            "histéresis",
            "repetibilidad",
            "instrumental drift",
            "respuesta a escalón",
            "constante de tiempo",
            "ancho de banda",
            "aptitud para el propósito",
        ):
            self.assertIn(concept, theory)

    def test_core_equations_and_model_boundaries_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        for equation in (
            "y=a+Sx",
            "S=\\frac{\\Delta y}{\\Delta x}",
            "H(x)=y_{\\uparrow}(x)-y_{\\downarrow}(x)",
            "D(t)=y(t)-y(t_0)",
            "y(t)=y_{\\infty}+(y_0-y_{\\infty})e^{-t/\\tau}",
            "f_c=\\frac{1}{2\\pi\\tau}",
        ):
            self.assertIn(equation, equations)
        dynamic = " ".join(self.unit["theory_sections"][2]["paragraphs"]).casefold()
        self.assertIn("solo si", dynamic)
        self.assertIn("modelo de primer orden", dynamic)

    def test_guided_activities_are_synthetic_and_progressive(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertGreaterEqual(len(activities), 3)
        self.assertGreaterEqual(len(activities[0]["problems"]), 9)
        self.assertGreaterEqual(len(activities[1]["problems"]), 14)
        self.assertGreaterEqual(len(activities[1]["deliverables"]), 10)
        self.assertGreaterEqual(len(activities[1]["checking_criteria"]), 10)
        self.assertGreaterEqual(len(activities[2]["tasks"]), 8)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintético", activity_text)
        self.assertIn("no conectes sensores educativos a personas", activity_text)
        self.assertIn("antes–después", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "sensibilidad metrológica",
            "histéresis",
            "repetibilidad",
            "deriva instrumental",
            "tiempo de respuesta a escalón",
            "constante de tiempo",
            "aptitud para el propósito",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_relevant(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://www.bipm.org/en/doi/10.59161/jcgm200-2012",
            "https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nbsspecialpublication615.pdf",
            "https://nvlpubs.nist.gov/nistpubs/Legacy/TN/nbstechnicalnote411.pdf",
            "https://www.nist.gov/publications/calibration-time-response-thermometers-concepts-and-model-calculations",
            "https://www.nist.gov/publications/time-domain-calibrations-d-dot-sensors",
            "https://www.ni.com/en/shop/data-acquisition/sensor-fundamentals/sensor-terminology.html",
        ):
            self.assertIn(url, urls)

    def test_scope_boundary_is_explicit(self) -> None:
        purpose = self.unit["purpose"].casefold()
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("sin confundir desempeño del sensor con sensibilidad diagnóstica", purpose)
        self.assertIn("no autoriza conexión a personas", notice)
        self.assertIn("no constituyen validación clínica", notice)
        self.assertIn("conformidad regulatoria", notice)


if __name__ == "__main__":
    unittest.main()
