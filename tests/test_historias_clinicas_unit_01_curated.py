from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "historias-clinicas-terminologias-estandares" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "historias-clinicas-terminologias-estandares" / "unit-01.json"
SUBJECT = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "historias-clinicas-terminologias-estandares.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class HistoriasClinicasUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["slug"], "historia-clinica-electronica")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("ppv=", self.text)
        self.assertNotIn("sensibilidad, especificidad y prevalencia", self.text)

    def test_objectives_cover_longitudinal_record_semantics(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "encuentro",
            "episodio de atención",
            "lista de problemas",
            "estado de verificación",
            "solicitud → realización → observación → informe",
            "tiempo clínicamente relevante",
            "procedencia",
            "versión",
            "ausencia de registro",
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
            "historia clínica electrónica longitudinal",
            "problemas, diagnósticos y estados",
            "solicitudes, acciones y resultados",
            "tiempo, procedencia y versiones",
            "reconstrucción longitudinal auditable",
        ):
            self.assertIn(phrase, headings)

    def test_encounter_episode_and_current_view_are_not_collapsed(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "el encuentro representa una interacción concreta",
            "un episodio de atención agrupa un periodo más amplio",
            "vista de resumen",
            "historia de estados",
            "mediciones, solicitudes, procedimientos, notas e informes",
        ):
            self.assertIn(phrase, text)
        self.assertIn("u2", text)
        self.assertIn("u4", text)

    def test_problem_list_preserves_clinical_and_verification_state(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "diagnóstico puntual de un encuentro",
            "lista de problemas",
            "estado clínico",
            "estado de verificación",
            "inicio y resolución",
            "refutada",
            "alergias",
        ):
            self.assertIn(phrase, text)
        self.assertIn("u3", text)

    def test_order_action_result_chain_does_not_equate_intent_with_execution(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "una orden o solicitud expresa intención",
            "una solicitud no demuestra",
            "procedimiento",
            "observaciones",
            "informes diagnósticos",
            "preliminar",
            "corregida",
            "solicitud → realización → observación → informe",
        ):
            self.assertIn(phrase, text)

    def test_temporal_semantics_provenance_and_missingness_are_explicit(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "tiempo clínicamente relevante",
            "tiempo de autoría",
            "tiempo de emisión",
            "tiempo de registro",
            "procedencia",
            "versión",
            "duplicados",
            "ausencia de registro no equivale a ausencia del evento",
        ):
            self.assertIn(phrase, text)

    def test_longitudinal_reconstruction_blocks_false_causality(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in (
            "línea temporal sintética auditable",
            "elementos que no pueden vincularse",
            "no autoriza por sí sola causalidad clínica",
            "contenido estructurado",
            "resultado corregido",
            "u6",
        ):
            self.assertIn(phrase, text)

    def test_glossary_examples_and_activity_are_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 45)
        for term in (
            "encuentro",
            "episodio de atención",
            "lista de problemas",
            "estado de verificación",
            "solicitud clínica",
            "observación",
            "informe diagnóstico",
            "tiempo clínicamente relevante",
            "procedencia",
            "historial de versiones",
            "elemento huérfano",
            "ausencia documentada",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 24)

    def test_activity_requires_safe_synthetic_auditable_work(self) -> None:
        activity = self.unit["guided_activities"][0]
        joined = " ".join(activity["instructions"] + activity["checking_criteria"]).casefold()
        for phrase in (
            "datos de pacientes reales",
            "tiempo clínicamente relevante",
            "estado clínico y estado de verificación",
            "solicitud → realización → observación → informe",
            "elemento huérfano",
            "dato faltante",
            "no se usan datos identificables",
            "u2",
            "u6",
        ):
            self.assertIn(phrase, joined)

    def test_sources_assessment_connections_and_editorial_boundary(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 18)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "datos exclusivamente sintéticos",
            "no constituye historia clínica real",
            "no se deben introducir datos identificables",
            "no establece diagnóstico",
            "u4 cubre interoperabilidad",
        ):
            self.assertIn(phrase, notice)

    def test_published_descriptor_matches_canonical_purpose(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {x["unit"]: x for x in subject["detailed_units"]}
        self.assertEqual(detailed[1]["description"], self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()
