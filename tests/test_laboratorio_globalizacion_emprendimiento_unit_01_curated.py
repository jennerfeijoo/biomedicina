from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "laboratorio-globalizacion-emprendimiento" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "laboratorio-globalizacion-emprendimiento" / "unit-01.json"
SUBJECT = ROOT / "data" / "subjects" / "gestion-etica-comunicacion" / "laboratorio-globalizacion-emprendimiento.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class LaboratorioGlobalizacionEmprendimientoUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["slug"], "retos-globales-de-salud")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("v(a)=", self.text)
        self.assertNotIn("modelo multicriterio transparente para comparar alternativas", self.text)

    def test_objectives_cover_burden_equity_systems_and_priority_reasoning(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "yll",
            "yld",
            "daly",
            "desagregación",
            "desigualdad",
            "inequidad",
            "sistema sanitario",
            "perfil de priorización multicriterio no compensatorio",
            "brief de reto priorizado",
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
        for phrase in ("reto global", "carga de enfermedad", "desigualdad", "sistemas sanitarios", "priorizar"):
            self.assertIn(phrase, headings)

    def test_burden_section_keeps_denominators_and_versioning(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "recuentos",
            "tasas",
            "incidencia",
            "prevalencia",
            "mortalidad",
            "yll",
            "yld",
            "daly",
            "fuente, año de publicación, periodo estimado y versión",
            "no son directamente comparables",
        ):
            self.assertIn(phrase, text)
        equations = json.dumps(self.unit["theory_sections"][1].get("equations", []), ensure_ascii=False).casefold()
        self.assertIn(r"\mathrm{daly}=\mathrm{yll}+\mathrm{yld}", equations)
        self.assertIn("n_{poblacion}", equations)

    def test_equity_section_distinguishes_descriptive_and_normative_claims(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "desigualdad en salud describe diferencias mensurables",
            "inequidad añade una evaluación normativa",
            "brechas absolutas y relativas",
            "grupo de referencia",
            "promedio",
            "distribución desigual",
        ):
            self.assertIn(phrase, text)
        equations = json.dumps(self.unit["theory_sections"][2].get("equations", []), ensure_ascii=False).casefold()
        self.assertIn(r"\delta_{abs}", equations)
        self.assertIn("r_{rel}", equations)

    def test_health_system_section_separates_access_coverage_and_quality(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "prestación de servicios",
            "fuerza laboral",
            "sistemas de información",
            "medicamentos y tecnologías",
            "financiación",
            "gobernanza",
            "acceso, cobertura y calidad deben separarse",
            "protección financiera",
            "cuello de botella hipotético",
        ):
            self.assertIn(phrase, text)

    def test_prioritization_keeps_criteria_visible_and_uses_sensitivity(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in (
            "perfil de decisión, no una suma ponderada",
            "magnitud",
            "tendencia",
            "distribución desigual",
            "brecha de atención",
            "calidad de datos",
            "no autoriza sumar ordinales",
            "análisis de sensibilidad",
            "shortlist",
            "no afirma que el reto elegido deba convertirse en una empresa",
        ):
            self.assertIn(phrase, text)

    def test_glossary_and_examples_are_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 45)
        for term in (
            "salud global",
            "tasa",
            "incidencia",
            "prevalencia",
            "yll",
            "yld",
            "daly",
            "desigualdad en salud",
            "inequidad en salud",
            "brecha absoluta",
            "razón relativa",
            "sistema sanitario",
            "cobertura efectiva",
            "protección financiera",
            "perfil de decisión",
            "análisis de sensibilidad",
            "brief de reto",
            "gather",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)

    def test_guided_activity_requires_auditable_priority_profile(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 24)
        joined = " ".join(activity["instructions"] + activity["checking_criteria"]).casefold()
        for phrase in (
            "datos agregados abiertos o",
            "toda cifra principal tiene fuente, periodo y versión",
            "no construyas una suma ponderada",
            "brecha absoluta y relativa",
            "no existe una suma ponderada, score total o ranking automático de países",
            "u1 termina con preguntas para u2",
        ):
            self.assertIn(phrase, joined)

    def test_sources_assessment_connections_and_editorial_boundary(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 15)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no sustituye epidemiología oficial",
            "datos agregados abiertos o sintéticos",
            "no autorizan diagnóstico",
            "ranking estigmatizante de países",
            "asignación vinculante de recursos",
            "u2 desarrolla esa investigación de contexto",
        ):
            self.assertIn(phrase, notice)

    def test_curricular_boundaries_keep_u1_as_problem_brief(self) -> None:
        for phrase in (
            "u2 será responsable de comprobarlas",
            "u1 termina con un brief del reto, no con una solución",
            "investigación profunda de actores, cultura, infraestructura y regulación queda reservada para u2",
            "no adelanta entrevistas, codiseño, prototipos, escalado ni pitch final",
        ):
            self.assertIn(phrase, self.text)

    def test_published_descriptor_matches_canonical_purpose(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {x["unit"]: x for x in subject["detailed_units"]}
        self.assertEqual(detailed[1]["description"], self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()
