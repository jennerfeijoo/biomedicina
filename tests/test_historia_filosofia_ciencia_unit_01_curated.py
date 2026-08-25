from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "historia-filosofia-ciencia" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "historia-filosofia-ciencia" / "unit-01.json"
SUBJECT = ROOT / "data" / "subjects" / "gestion-etica-comunicacion" / "historia-filosofia-ciencia.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class HistoriaFilosofiaCienciaUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["slug"], "origenes-y-transformacion-de-la-ciencia")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn(r"v(a)=\\sum", self.text)
        self.assertNotIn("modelo multicriterio transparente", self.text)

    def test_objectives_cover_historiography_transmission_transformation_and_institutions(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "historiografía",
            "presentismo",
            "tradiciones médicas",
            "transmisión",
            "vesalio",
            "ibn al-nafis",
            "harvey",
            "revolución científica",
            "institucionalización",
            "u2",
        ):
            self.assertIn(phrase, objectives)

    def test_five_substantive_theory_sections(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        for section in sections:
            self.assertGreaterEqual(len(section["paragraphs"]), 6)
            self.assertGreaterEqual(len(section["key_points"]), 6)
            for point in section["key_points"]:
                self.assertGreaterEqual(len(point.split()), 5)
        headings = " ".join(x["heading"] for x in sections).casefold()
        for phrase in (
            "historiografía",
            "tradiciones antiguas y medievales",
            "temprana modernidad",
            "revolución científica",
            "institucionalización",
        ):
            self.assertIn(phrase, headings)

    def test_historiography_section_blocks_presentism_and_heroic_teleology(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "fuente primaria",
            "fuente secundaria",
            "presentismo",
            "teleológica",
            "historia «whig»",
            "precedencia temporal no demuestra influencia",
        ):
            self.assertIn(phrase, text)
        self.assertIn("redes de maestros, artesanos, pacientes, traductores, impresores, patronos, universidades y sociedades", text)

    def test_ancient_medieval_section_is_not_a_dark_age_story(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "corpus hippocraticum",
            "galen",
            "traducción",
            "árabes e islámicos",
            "ibn al-nafis",
            "universidades medievales",
            "disección humana",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no fue una simple conservación europea", text)
        self.assertIn("precedencia textual, alcance de una propuesta, circulación de manuscritos, recepción y evidencia de influencia", text)

    def test_early_modern_section_teaches_plural_methods_and_material_practices(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "vesalio",
            "1543",
            "william harvey",
            "1628",
            "galileo",
            "descartes",
            "bacon",
            "newton",
            "instrumentos",
            "imprenta",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no existe una receta única", text)

    def test_scientific_revolution_is_explicitly_historiographical_and_contested(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "categoría historiográfica",
            "revolución única",
            "continuidades medievales",
            "extraeuropeas",
            "ruptura",
            "continuidad",
            "escala geográfica",
        ):
            self.assertIn(phrase, text)
        self.assertIn("cambio científico no equivale automáticamente a progreso social", text)

    def test_institutionalization_section_has_correct_publishing_timeline(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in (
            "royal society",
            "1660",
            "philosophical transactions",
            "1665",
            "henry oldenburg",
            "1832",
            "profesionalización",
            "financiación",
        ):
            self.assertIn(phrase, text)
        self.assertIn("es incorrecto afirmar que la revista nació ya con el peer review contemporáneo", text)

    def test_glossary_and_worked_examples_are_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 45)
        for term in (
            "historiografía",
            "presentismo",
            "historia whig",
            "corpus hippocraticum",
            "galenismo",
            "bimaristán",
            "revolución científica",
            "royal society",
            "philosophical transactions",
            "refereeing",
            "profesionalización",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)

    def test_guided_activity_requires_traceable_competing_narratives(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)
        joined = " ".join(activity["instructions"] + activity["problems"] + activity["checking_criteria"]).casefold()
        for phrase in (
            "fuentes primarias",
            "precedencia, transmisión, recepción, influencia y prioridad",
            "narrativa de ruptura",
            "narrativa de continuidad",
            "no cuantifiques «progreso científico»",
            "no se afirma que peer review moderno exista sin cambios desde 1665",
        ):
            self.assertIn(phrase, joined)

    def test_common_errors_and_assessment_protect_historical_inference(self) -> None:
        self.assertGreaterEqual(len(self.unit["common_errors"]), 18)
        errors = json.dumps(self.unit["common_errors"], ensure_ascii=False).casefold()
        for phrase in (
            "padre de la ciencia",
            "edad oscura",
            "precedencia de influencia",
            "peer review moderno",
            "línea de tiempo como explicación causal",
        ):
            self.assertIn(phrase, errors)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)

    def test_sources_connections_and_editorial_boundaries(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 15)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no adjudica por sí solo prioridad o influencia",
            "no constituyen diagnóstico",
            "u2 abordará",
            "u5 desarrollará",
            "revisión disciplinar externa",
        ):
            self.assertIn(phrase, notice)

    def test_published_descriptor_matches_canonical_purpose(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {x["unit"]: x for x in subject["detailed_units"]}
        self.assertEqual(detailed[1]["description"], self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()
