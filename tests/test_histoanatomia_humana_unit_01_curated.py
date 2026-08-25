from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "histoanatomia-humana" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "histoanatomia-humana" / "unit-01.json"
SUBJECT = ROOT / "data" / "subjects" / "biologicas-medicas" / "histoanatomia-humana.json"
CATALOG = ROOT / "data" / "catalog_statuses.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class HistoanatomiaHumanaUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_generic_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["slug"], "metodos-y-organizacion-corporal")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn(r"v=\frac{\delta y}{\delta t}", self.text)

    def test_learning_objectives_cover_orientation_preparation_and_microscopy(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "posición anatómica",
            "sección bidimensional",
            "fijación",
            "h&e",
            "apertura numérica",
            "registro trazable",
        ):
            self.assertIn(phrase, objectives)

    def test_five_substantive_theory_sections(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        for section in sections:
            self.assertGreaterEqual(len(section["paragraphs"]), 6)
            self.assertGreaterEqual(len(section["key_points"]), 6)
            for point in section["key_points"]:
                self.assertGreaterEqual(len(point.split()), 7)
        headings = " ".join(x["heading"] for x in sections).casefold()
        for phrase in ("referencia anatómica", "estructura 3d", "preparación histológica", "h&e", "microscopía óptica"):
            self.assertIn(phrase, headings)

    def test_3d_to_2d_geometry_is_explicit(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in ("plano de corte", "nivel", "corte tangencial", "cortes seriados", "observación directa"):
            self.assertIn(phrase, text)

    def test_histology_pipeline_and_artifacts_are_explicit(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in ("fijación", "deshidratación", "aclaramiento", "inclusión", "microtomía", "artefacto", "trazabilidad"):
            self.assertIn(phrase, text)

    def test_staining_does_not_overclaim_identity(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        self.assertIn("el color no es una etiqueta de identidad absoluta", text)
        self.assertIn("no una medición molecular específica", text)
        self.assertIn("u2", text)

    def test_microscopy_teaches_resolution_not_empty_magnification(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in ("magnificación y resolución no son sinónimos", "apertura numérica", "0.61", "magnificación vacía", "calibración"):
            self.assertIn(phrase, text)

    def test_glossary_is_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 35)
        for term in (
            "posición anatómica",
            "plano sagital",
            "corte tangencial",
            "fijación",
            "microtomía",
            "artefacto histológico",
            "hematoxilina-eosina (h&e)",
            "resolución",
            "apertura numérica",
            "calibración espacial",
        ):
            self.assertIn(term, glossary)

    def test_activity_is_applied_and_auditable(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 18)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 20)

    def test_common_errors_block_core_misconceptions(self) -> None:
        errors = json.dumps(self.unit["common_errors"], ensure_ascii=False).casefold()
        for phrase in (
            "derecha/izquierda de la pantalla",
            "forma 3d única",
            "corte tangencial",
            "pliegues, chatter o estrías",
            "magnificación con resolución",
            "píxeles como si fueran micrómetros",
        ):
            self.assertIn(phrase, errors)

    def test_assessment_connections_sources_and_scope(self) -> None:
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        self.assertGreaterEqual(len(self.unit["sources"]), 15)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        notice = self.unit["editorial_notice"].casefold()
        for phrase in ("no constituye entrenamiento diagnóstico", "se reserva para u2", "no garantizan resolución real", "decisiones asistenciales"):
            self.assertIn(phrase, notice)

    def test_published_descriptor_matches_curated_unit(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {x["unit"]: x for x in subject["detailed_units"]}
        self.assertEqual(detailed[1]["description"], self.unit["purpose"])

    def test_course_leaves_template_detected_after_units_1_to_6_are_curated(self) -> None:
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        specificity = catalog["dimensions"]["specificity"]
        self.assertIn("histoanatomia-humana", specificity["screened_no_known_template_marker"])
        self.assertNotIn("histoanatomia-humana", specificity["template_detected"])


if __name__ == "__main__":
    unittest.main()
