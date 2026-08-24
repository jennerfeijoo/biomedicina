from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomateriales" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "biomateriales" / "unit-06.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomaterialesUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomateriales")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_out_of_scope_mechanics_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("\\sigma=\\frac{f}{a_0}", self.text)
        for concept in (
            "uso previsto",
            "matriz de trazabilidad",
            "iso 14971:2019",
            "iso 10993-1:2025",
            "riesgo residual",
            "estado final procesado",
            "evidencia preclínica",
        ):
            self.assertIn(concept, self.text)

    def test_theory_is_substantive_and_integrates_prior_units(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for phrase in (
            "u6 no repite esas unidades",
            "peligro, daño y riesgo no son sinónimos",
            "no es '¿qué batería de ensayos exige la tabla?'",
            "la esterilización no se añade al final",
            "un borrador fdis no debe presentarse como norma publicada",
            "'más ensayos' no es sinónimo de 'mejor evidencia'",
        ):
            self.assertIn(phrase, theory)

    def test_risk_and_biological_evaluation_boundaries_are_explicit(self) -> None:
        theory = " ".join(p for section in self.unit["theory_sections"] for p in section["paragraphs"]).casefold()
        self.assertIn("una propiedad peligrosa no equivale automáticamente a riesgo", theory)
        self.assertIn("no demuestra riesgo cero", theory)
        self.assertIn("no autoriza a declarar conformidad con iso 10993", theory)
        self.assertIn("no que un dispositivo real es seguro, eficaz, conforme o listo para uso humano", theory)

    def test_sterilization_versions_and_draft_status_are_correct(self) -> None:
        self.assertIn("iso 11137-1:2025", self.text)
        self.assertIn("iso 17665:2024", self.text)
        self.assertIn("iso 11135:2014", self.text)
        self.assertIn("iso/fdis 11135", self.text)
        self.assertNotIn("iso 11135:2026", self.text)
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("iso/fdis 11135 es un proyecto final y no una norma publicada", notice)
        self.assertIn("parámetros operativos de esterilización", notice)

    def test_pedagogy_progresses_and_stays_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertIn("Matriz guiada", activities[0]["title"])
        self.assertIn("ayudas reducidas", activities[1]["title"])
        self.assertIn("Auditoría ciega", activities[2]["title"])
        for activity in activities:
            self.assertGreaterEqual(len(activity["instructions"]), 5)
            self.assertGreaterEqual(len(activity["problems"]), 10)
            self.assertGreaterEqual(len(activity["deliverables"]), 7)
            self.assertGreaterEqual(len(activity["checking_criteria"]), 8)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("sintétic", activity_text)
        self.assertIn("no propongas dosis, temperatura, presión, concentración, tiempo ni parámetros de ciclo", activity_text)
        self.assertIn("sin diseñar procedimientos de laboratorio o animales", activity_text)

    def test_glossary_examples_errors_and_assessment_are_complete(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 28)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "uso previsto",
            "requisito",
            "peligro",
            "situación peligrosa",
            "riesgo residual",
            "evaluación biológica",
            "compatibilidad con esterilización",
            "artículo de ensayo representativo",
            "reemplazo",
            "reducción",
            "refinamiento",
            "expediente de evidencia",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_preserve_status(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 12)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        expected = {
            "https://www.iso.org/standard/72704.html",
            "https://www.iso.org/standard/10993-1",
            "https://www.iso.org/standard/75769.html",
            "https://www.iso.org/standard/88205.html",
            "https://www.iso.org/standard/78866.html",
            "https://www.iso.org/standard/86246.html",
            "https://www.iso.org/standard/81721.html",
            "https://www.iso.org/standard/80271.html",
            "https://www.iso.org/es/contents/data/standard/05/61/56137.html",
            "https://www.iso.org/es/contents/data/standard/09/00/90088.html",
        }
        self.assertTrue(expected.issubset(urls))
        descriptions = json.dumps(sources, ensure_ascii=False).casefold()
        self.assertIn("confirmada por iso en 2025", descriptions)
        self.assertIn("fase 40.99 en 2026", descriptions)
        self.assertIn("proyecto final de edición 3", descriptions)

    def test_editorial_boundary_excludes_regulatory_and_experimental_execution(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no proporciona parámetros operativos de esterilización",
            "procedimientos animales",
            "selección de endpoints regulatorios",
            "no constituye evaluación de conformidad",
            "validación preclínica o clínica",
            "revisión disciplinar humana externa permanece pendiente",
        ):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
