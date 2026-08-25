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
        for concept in (
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
            "muestreo cualitativo",
            "saturación cualitativa",
            "mapa de actores",
            "persona afectada",
            "mantenedor",
            "triangulación",
            "evidencia discrepante",
            "caso negativo",
            "matriz de evidencia",
        ):
            self.assertIn(concept, self.text)

    def test_sampling_strategy_is_explicit_in_theory(self) -> None:
        theory_text = " ".join(
            paragraph.casefold()
            for section in self.unit["theory_sections"]
            for paragraph in section["paragraphs"]
        )
        theory_text += " " + " ".join(
            point.casefold()
            for section in self.unit["theory_sections"]
            for point in section["key_points"]
        )
        self.assertIn("muestreo con variación deliberada", theory_text)
        self.assertIn("saturación cualitativa", theory_text)

    def test_need_and_solution_layers_are_not_collapsed(self) -> None:
        for phrase in (
            "observación, interpretación, causalidad, necesidad y solución son capas distintas",
            "una declaración de necesidad debe evitar soluciones escondidas",
            "un workaround no es automáticamente un fallo",
            "saturación cualitativa no significa representatividad estadística",
            "bajo poder formal no implica baja relevancia",
            "triangular significa comparar evidencias, no sumar votos",
        ):
            self.assertIn(phrase, self.text)

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
        self.assertIn("no estima por sí solo prevalencia poblacional ni demuestra causalidad", self.text)
        self.assertIn("el denominador debe establecerse antes de contar", self.text)

    def test_examples_cover_solution_bias_interview_stakeholders_and_negative_evidence(self) -> None:
        examples = self.unit["worked_examples"]
        self.assertGreaterEqual(len(examples), 5)
        example_text = json.dumps(examples, ensure_ascii=False).casefold()
        for phrase in (
            "workaround",
            "pregunta sugestiva",
            "paciente y profesional",
            "mantenedor",
            "solución escondida",
        ):
            self.assertIn(phrase, example_text)
        self.assertIn("no interpretar entusiasmo hipotético como adopción", example_text)

    def test_guided_activity_is_scaffolded_reproducible_and_safe(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 12)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 20)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        for phrase in (
            "exclusivamente",
            "oportunidades elegibles",
            "preguntas abiertas y neutrales",
            "evidencia discrepante",
            "baja influencia formal",
            "solution-neutral",
            "no afirma validación de mercado",
        ):
            self.assertIn(phrase, text)

    def test_learning_scaffolds_are_specific_and_sufficient(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 40)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 16)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
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
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_relevant(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 14)
        self.assertTrue(
            all(item.get("verification_status") == "verified_directly" for item in sources)
        )
        urls = {item["url"] for item in sources}
        for url in (
            "https://biodesign.stanford.edu/programs/stanford-courses/needs-finding-for-medical-students.html",
            "https://biodesign.stanford.edu/programs/stanford-courses/needs-finding-in-healthcare.html",
            "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/patient-focused-drug-development-collecting-comprehensive-and-representative-input",
            "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/patient-focused-drug-development-methods-identify-what-important-patients",
            "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/applying-human-factors-and-usability-engineering-medical-devices",
            "https://pubmed.ncbi.nlm.nih.gov/17872937/",
            "https://pubmed.ncbi.nlm.nih.gov/24979285/",
            "https://pubmed.ncbi.nlm.nih.gov/34100147/",
            "https://pubmed.ncbi.nlm.nih.gov/32829927/",
        ):
            self.assertIn(url, urls)

    def test_biomedical_connections_are_structured(self) -> None:
        connections = self.unit["biomedical_connections"]
        self.assertGreaterEqual(len(connections), 6)
        text = json.dumps(connections, ensure_ascii=False).casefold()
        for phrase in (
            "ingeniería clínica",
            "factores humanos",
            "salud digital",
            "dispositivos médicos",
            "equidad en salud",
        ):
            self.assertIn(phrase, text)

    def test_course_and_human_research_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no constituye investigación con seres humanos",
            "no constituye",
            "aprobación ética",
            "consentimiento informado",
            "estudio de mercado",
            "validación clínica",
            "libertad de operación",
            "u2 desarrollará propuesta de valor",
            "u3 prototipo y experimentos",
            "u4 modelo de negocio y acceso",
            "u5 propiedad intelectual y regulación",
            "u6 financiación y comunicación",
        ):
            self.assertIn(phrase, notice)

    def test_published_descriptor_can_be_promoted_to_canonical_purpose(self) -> None:
        published_u1 = next(
            item for item in self.subject["detailed_units"] if item["unit"] == 1
        )
        self.assertEqual(published_u1["title"], self.unit["title"])
        if published_u1["description"] != self.unit["purpose"]:
            self.skipTest("El publicador todavía no ha promovido el propósito canónico de U1.")
        self.assertEqual(published_u1["description"], self.unit["purpose"])
        self.assertIn("observación contextual", published_u1["description"].casefold())
        self.assertNotIn(
            "integrar observación, entrevistas, mapa de actores para resolver",
            published_u1["description"].casefold(),
        )


if __name__ == "__main__":
    unittest.main()
