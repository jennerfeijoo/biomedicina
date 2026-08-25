import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/historia-filosofia-ciencia/units/unit-06.json"
MIRROR = ROOT / "data/generated_units/historia-filosofia-ciencia/unit-06.json"
GENERIC_MARKERS = (
    "Concepto de la unidad que debe definirse mediante entidades observables",
    "V(a)=\\sum_{i=1}^{k} w_i r_i(a)",
    "modelo multicriterio transparente",
)

class HistoriaFilosofiaCienciaUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.mirror = json.loads(MIRROR.read_text(encoding="utf-8"))

    def test_source_and_mirror_are_exact(self):
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit, self.mirror)

    def test_identity_and_purpose_are_disciplinary(self):
        self.assertEqual(self.unit["subject_id"], "historia-filosofia-ciencia")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["slug"], "ciencia-contemporanea")
        purpose = self.unit["purpose"].casefold()
        for phrase in ("reproducibilidad", "replicabilidad", "ciencia abierta", "incertidumbre", "desinformación", "u1–u5"):
            self.assertIn(phrase, purpose)

    def test_template_and_generic_score_are_absent(self):
        text = SOURCE.read_text(encoding="utf-8")
        for marker in GENERIC_MARKERS:
            self.assertNotIn(marker, text)

    def test_academic_depth_and_pedagogy(self):
        self.assertGreaterEqual(len(self.unit["learning_objectives"]), 6)
        self.assertGreaterEqual(len(self.unit["theory_sections"]), 5)
        for section in self.unit["theory_sections"]:
            self.assertGreaterEqual(len(section["paragraphs"]), 5)
            self.assertGreaterEqual(len(section["key_points"]), 5)
        self.assertGreaterEqual(len(self.unit["glossary"]), 45)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["guided_activities"]), 3)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 18)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        self.assertGreaterEqual(len(self.unit["sources"]), 16)

    def test_reproducibility_section_keeps_validity_separate(self):
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in ("reproducibilidad computacional", "replicabilidad", "robustez", "generalización", "datos nuevos"):
            self.assertIn(phrase, text)
        self.assertIn("no demuestra que la afirmación sea verdadera", text)
        self.assertIn("no replicación tampoco identifica automáticamente una causa", text)

    def test_open_science_section_distinguishes_fair_access_and_preregistration(self):
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in ("fair", "autenticación", "preregistro", "registered reports", "transparency and openness promotion"):
            self.assertIn(phrase, text)
        self.assertIn("ciencia abierta no significa publicar todo", text)
        self.assertIn("no garantiza", text)

    def test_self_correction_section_does_not_turn_peer_review_or_retraction_into_truth_tests(self):
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in ("revisión por pares", "corrección", "retractación", "metaciencia", "guía de reporte"):
            self.assertIn(phrase, text)
        self.assertIn("no certifica la verdad", text)
        self.assertIn("retractación no es sinónimo automático de fraude", text)

    def test_uncertainty_section_is_multidimensional_and_versioned(self):
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in ("medición", "muestreo", "parámetros", "modelo", "extrapolación", "preprint", "versiones"):
            self.assertIn(phrase, text)
        self.assertIn("no resume incertidumbre", text)
        self.assertIn("no demuestra que 'la ciencia no sabe nada'", text)

    def test_infodemic_section_separates_falsehood_from_intent(self):
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in ("información errónea", "desinformación", "intención", "infodemia", "procedencia"):
            self.assertIn(phrase, text)
        self.assertIn("inferir intención exige evidencia adicional", text)
        self.assertIn("no se produce una puntuación total", text)

    def test_integrated_workshop_is_multidimensional(self):
        workshop = self.unit["guided_activities"][1]
        text = json.dumps(workshop, ensure_ascii=False).casefold()
        self.assertGreaterEqual(len(workshop["problems"]), 25)
        self.assertGreaterEqual(len(workshop["deliverables"]), 10)
        self.assertGreaterEqual(len(workshop["checking_criteria"]), 20)
        for phrase in ("reproducción computacional", "replicación", "fair", "preregistro", "incertidumbre", "desinformación"):
            self.assertIn(phrase, text)
        self.assertIn("no existe una puntuación total", text)

    def test_glossary_covers_core_metascience_terms(self):
        terms = {x["term"].casefold() for x in self.unit["glossary"]}
        required = {"reproducibilidad computacional","replicabilidad","robustez","ciencia abierta","fair","preregistro","registered report","revisión por pares","retractación","metaciencia","preprint","información errónea","desinformación","infodemia"}
        self.assertTrue(required.issubset(terms), required - terms)

    def test_sources_are_directly_verified_and_relevant(self):
        self.assertTrue(all(s.get("verification_status") == "verified_directly" for s in self.unit["sources"]))
        organizations = " ".join(s["organization"] for s in self.unit["sources"]).casefold()
        for phrase in ("national academies", "unesco", "national institutes of health", "world health organization", "center for open science", "international committee"):
            self.assertIn(phrase, organizations)

    def test_editorial_boundary_blocks_truth_scores_and_accusations(self):
        notice = self.unit["editorial_notice"].casefold()
        for phrase in ("no declara fraude", "desinformación intencional", "indicadores binarios de verdad", "no sustituye revisión sistemática", "revisión disciplinar externa"):
            self.assertIn(phrase, notice)

if __name__ == "__main__":
    unittest.main()
