from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "innovacion-emprendimiento" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "innovacion-emprendimiento" / "unit-01.json"
SUBJECT = ROOT / "data" / "subjects" / "gestion-etica-comunicacion" / "innovacion-emprendimiento.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class InnovacionEmprendimientoUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()
        cls.subject = json.loads(SUBJECT.read_text(encoding="utf-8"))

    def assertContainsAll(self, text: str, terms: tuple[str, ...]) -> None:
        for term in terms:
            with self.subTest(term=term):
                self.assertIn(term, text)

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "innovacion-emprendimiento")
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_generic_multicriteria_model_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("v(a)=\\sum", self.text)
        self.assertNotIn("modelo multicriterio transparente para comparar alternativas", self.text)
        self.assertNotIn("definir problema público → mapear actores y valores", self.text)

    def test_theory_is_specific_to_needs_finding(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        self.assertContainsAll(
            self.text,
            (
                "innovación guiada por necesidades",
                "declaración de necesidad",
                "solution-neutral",
                "observación contextual",
                "workaround",
                "efecto del observador",
                "reflexividad",
                "entrevistas semiestructuradas",
                "preguntas abiertas",
                "priming",
                "saturación cualitativa",
                "mapa de actores",
                "persona afectada",
                "mantenedor",
                "triangulación",
                "evidencia discrepante",
                "caso negativo",
                "matriz de evidencia",
            ),
        )

    def test_sampling_and_interview_strategy_are_explicit(self) -> None:
        theory = json.dumps(self.unit["theory_sections"], ensure_ascii=False).casefold()
        self.assertContainsAll(
            theory,
            (
                "muestreo cualitativo",
                "diversidad informativa",
                "saturación cualitativa",
                "representatividad estadística",
                "preguntas abiertas",
                "preguntas neutrales",
                "priming",
                "sondas",
            ),
        )

    def test_need_and_solution_layers_are_not_collapsed(self) -> None:
        first = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        self.assertContainsAll(
            first,
            (
                "observación",
                "interpretación",
                "hipótesis causal",
                "necesidad",
                "solución",
                "neutral respecto de la solución",
                "u2",
                "u3",
                "u4",
                "u5",
                "u6",
            ),
        )
        self.assertIn("un workaround no es automáticamente un fallo", self.text)
        self.assertIn("bajo poder formal no implica baja relevancia", self.text)
        self.assertIn("triangular significa comparar evidencias, no sumar votos", self.text)

    def test_observation_ratio_is_descriptive_not_population_inference(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn(
            r"R_{obs}=\frac{n_{\mathrm{eventos\ observados}}}{n_{\mathrm{oportunidades\ elegibles}}}",
            equations,
        )
        observation = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        self.assertContainsAll(
            observation,
            (
                "denominador",
                "oportunidades elegibles",
                "prevalencia poblacional",
                "causalidad",
                "efecto del observador",
                "sesgo de selección",
            ),
        )

    def test_examples_cover_solution_bias_interviews_stakeholders_and_discrepancy(self) -> None:
        examples = self.unit["worked_examples"]
        self.assertGreaterEqual(len(examples), 5)
        text = json.dumps(examples, ensure_ascii=False).casefold()
        self.assertContainsAll(
            text,
            (
                "workaround",
                "pregunta sugestiva",
                "paciente",
                "profesional",
                "mantenimiento",
                "solución",
                "adopción",
            ),
        )

    def test_guided_activity_is_scaffolded_reproducible_and_safe(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 12)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 20)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertContainsAll(
            text,
            (
                "exclusivamente",
                "oportunidades elegibles",
                "preguntas abiertas",
                "neutrales",
                "evidencia discrepante",
                "influencia formal",
                "solution-neutral",
                "validación de mercado",
            ),
        )

    def test_learning_scaffolds_are_specific_and_sufficient(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 40)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 16)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        required = {
            "needs finding",
            "innovación guiada por necesidades",
            "declaración de necesidad",
            "indagación contextual",
            "oportunidad elegible",
            "efecto del observador",
            "reflexividad",
            "entrevista semiestructurada",
            "pregunta sugestiva",
            "priming",
            "muestreo deliberado",
            "saturación cualitativa",
            "triangulación",
            "evidencia discrepante",
            "caso negativo",
            "mapa de actores",
            "persona afectada",
            "mantenedor",
            "matriz de evidencia",
            "ajuste problema-solución",
            "validación de mercado",
        }
        self.assertTrue(required.issubset(terms), required - terms)

    def test_sources_are_directly_verified_and_relevant(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 14)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        domains = " ".join(item["url"].casefold() for item in sources)
        self.assertContainsAll(domains, ("biodesign.stanford.edu", "fda.gov", "pubmed.ncbi.nlm.nih.gov"))
        pmids = {item["url"] for item in sources if "pubmed.ncbi.nlm.nih.gov" in item["url"]}
        self.assertGreaterEqual(len(pmids), 5)

    def test_biomedical_connections_are_structured(self) -> None:
        connections = self.unit["biomedical_connections"]
        self.assertGreaterEqual(len(connections), 6)
        text = json.dumps(connections, ensure_ascii=False).casefold()
        self.assertContainsAll(
            text,
            ("ingeniería clínica", "factores humanos", "salud digital", "dispositivos médicos", "equidad en salud"),
        )

    def test_course_and_human_research_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        self.assertContainsAll(
            notice,
            (
                "no constituye investigación con seres humanos",
                "aprobación ética",
                "consentimiento informado",
                "estudio de mercado",
                "validación clínica",
                "libertad de operación",
                "u2",
                "u3",
                "u4",
                "u5",
                "u6",
            ),
        )

    def test_published_descriptor_matches_canonical_purpose(self) -> None:
        published_u1 = next(item for item in self.subject["detailed_units"] if item["unit"] == 1)
        self.assertEqual(published_u1["title"], self.unit["title"])
        self.assertEqual(published_u1["description"], self.unit["purpose"])
        self.assertIn("observación contextual", published_u1["description"].casefold())
        self.assertNotIn(
            "integrar observación, entrevistas, mapa de actores para resolver",
            published_u1["description"].casefold(),
        )


if __name__ == "__main__":
    unittest.main()
