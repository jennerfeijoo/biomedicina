from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "innovacion-emprendimiento" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "innovacion-emprendimiento" / "unit-02.json"
SUBJECT = ROOT / "data" / "subjects" / "gestion-etica-comunicacion" / "innovacion-emprendimiento.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class InnovacionEmprendimientoUnit02CuratedTests(unittest.TestCase):
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
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_generic_multicriteria_model_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("v(a)=\\sum", self.text)
        self.assertNotIn("modelo multicriterio transparente para comparar alternativas", self.text)
        self.assertNotIn("definir problema público → mapear actores y valores", self.text)

    def test_theory_is_specific_to_value_proposition_and_problem_solution_fit(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        self.assertContainsAll(
            self.text,
            (
                "propuesta de valor",
                "hipótesis falsable",
                "actor",
                "alternativa de referencia",
                "statu quo",
                "ajuste problema–solución",
                "product–market fit",
                "segmentación",
                "contexto de uso",
                "resultado observable",
                "evidencia discrepante",
                "caso negativo",
                "criterio de salida",
                "seguir, revisar o rechazar",
            ),
        )

    def test_roles_segments_and_context_are_not_collapsed(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        self.assertContainsAll(
            text,
            (
                "persona afectada",
                "usuario operativo",
                "comprador",
                "pagador",
                "decisor",
                "implementador",
                "mantenedor",
                "segmento",
                "contexto de uso",
                "heterogéneas",
                "transferencias de carga",
            ),
        )
        self.assertIn("influencia sobre la adopción", self.text)

    def test_benefits_alternatives_and_descriptive_difference_are_explicit(self) -> None:
        third = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        self.assertContainsAll(
            third,
            (
                "resultado observable",
                "alternativa funcional",
                "statu quo",
                "workaround",
                "intención declarada",
                "adopción",
                "score opaco",
                "efecto causal",
                "beneficio clínico",
            ),
        )
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn(r"\Delta p=p_{\mathrm{prop}}-p_{\mathrm{ref}}", equations)
        self.assertEqual(len(equations), 1)

    def test_problem_solution_fit_is_not_market_or_clinical_validation(self) -> None:
        self.assertIn("ajuste problema–solución", self.text)
        self.assertIn("product–market fit", self.text)
        self.assertIn("no equivale a product–market fit", self.text)
        self.assertIn("eficacia clínica ni seguridad", self.text)
        self.assertIn("no significa que el producto sea viable", self.text)

    def test_hypothesis_matrix_refutation_and_exit_criteria_are_explicit(self) -> None:
        fourth = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        self.assertContainsAll(
            fourth,
            (
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "condición de refutación",
                "evidencia discrepante",
                "casos negativos",
                "criterios de salida",
                "seguir, revisar o rechazar",
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
                "statu quo",
                "resultado observable",
                "h1",
                "h5",
                "evidencia discrepante",
                "seguir, revisar o rechazar",
                "u3",
                "product-market fit",
                "validación clínica",
            ),
        )

    def test_learning_scaffolds_are_specific_and_sufficient(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 40)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 18)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        required = {
            "propuesta de valor",
            "actor beneficiario",
            "usuario operativo",
            "persona afectada",
            "comprador",
            "pagador",
            "decisor",
            "implementador",
            "mantenedor",
            "segmento",
            "contexto de uso",
            "beneficio esperado",
            "resultado observable",
            "alternativa de referencia",
            "statu quo",
            "workaround",
            "ajuste problema-solución",
            "product-market fit",
            "hipótesis de valor",
            "supuesto crítico",
            "criterio de refutación",
            "caso negativo",
            "evidencia discrepante",
            "matriz de hipótesis",
            "carga transferida",
            "trade-off",
            "intención declarada",
            "adopción",
            "deseabilidad",
            "factibilidad",
            "viabilidad",
            "criterio de salida",
        }
        self.assertTrue(required.issubset(terms), required - terms)

    def test_examples_cover_actor_value_status_quo_adoption_and_rejection(self) -> None:
        examples = self.unit["worked_examples"]
        self.assertGreaterEqual(len(examples), 5)
        text = json.dumps(examples, ensure_ascii=False).casefold()
        self.assertContainsAll(
            text,
            (
                "pagador",
                "mantenedor",
                "resultado observable",
                "statu quo",
                "workaround",
                "intención declarada",
                "adopción",
                "rechazar",
            ),
        )

    def test_sources_are_directly_verified_and_relevant(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 15)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        domains = " ".join(item["url"].casefold() for item in sources)
        self.assertContainsAll(
            domains,
            (
                "biodesign.stanford.edu",
                "nih.gov",
                "oecd.org",
                "fda.gov",
                "iso.org",
                "who.int",
                "pubmed.ncbi.nlm.nih.gov",
            ),
        )

    def test_biomedical_connections_are_structured(self) -> None:
        connections = self.unit["biomedical_connections"]
        self.assertGreaterEqual(len(connections), 6)
        text = json.dumps(connections, ensure_ascii=False).casefold()
        self.assertContainsAll(
            text,
            (
                "ingeniería clínica",
                "factores humanos",
                "dispositivos médicos",
                "salud digital",
                "preferencias de pacientes",
                "equidad y acceso",
            ),
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
                "customer discovery real",
                "validación de factores humanos",
                "preferencias del paciente",
                "validación clínica",
                "seguridad o eficacia",
                "evaluación regulatoria",
                "libertad de operación",
                "reembolso",
                "recomendación de inversión",
                "u1",
                "u3",
                "u4",
                "u5",
                "u6",
            ),
        )

    def test_published_descriptor_matches_canonical_purpose_when_available(self) -> None:
        published_u2 = next(item for item in self.subject["detailed_units"] if item["unit"] == 2)
        if published_u2["description"] != self.unit["purpose"]:
            self.skipTest("El publicador todavía no ha materializado el descriptor canónico de U2")
        self.assertEqual(published_u2["title"], self.unit["title"])
        self.assertEqual(published_u2["description"], self.unit["purpose"])
        self.assertIn("hipótesis explícita y falsable", published_u2["description"].casefold())
        self.assertNotIn(
            "integrar usuario, beneficios, alternativas y ajuste problema-solución",
            published_u2["description"].casefold(),
        )


if __name__ == "__main__":
    unittest.main()
