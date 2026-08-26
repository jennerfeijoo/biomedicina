from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "innovacion-emprendimiento" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "innovacion-emprendimiento" / "unit-03.json"
SUBJECT = ROOT / "data" / "subjects" / "gestion-etica-comunicacion" / "innovacion-emprendimiento.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


def norm(text: str) -> str:
    return text.casefold().replace("–", "-").replace("—", "-")


class InnovacionEmprendimientoUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = norm(json.dumps(cls.unit, ensure_ascii=False))
        cls.subject = json.loads(SUBJECT.read_text(encoding="utf-8"))

    def test_source_mirror_and_identity(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "innovacion-emprendimiento")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["title"], "Prototipo y experimentos")
        self.assertEqual(self.unit["status"], "review")

    def test_template_and_generic_score_are_absent(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("v(a)=\\sum", self.text)
        self.assertNotIn("modelo multicriterio transparente para comparar alternativas", self.text)

    def test_learning_objectives_use_experiment_language(self) -> None:
        objectives = norm(" ".join(self.unit["learning_objectives"]))
        for phrase in (
            "mvp",
            "prototipo",
            "métrica y umbral",
            "resultados favorables, nulos y discrepantes",
            "documentar un ciclo",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, objectives)
        self.assertIn("criterio de refutación", self.text)
        self.assertIn("decisiones de aprendizaje", self.text)
        self.assertIn("evidencia discrepante", self.text)

    def test_theory_has_real_prototyping_and_experiment_content(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        for concept in (
            "mapa de supuestos",
            "hipótesis falsable",
            "prueba de concepto",
            "mvp",
            "fidelidad mínima",
            "feature creep",
            "baseline",
            "control negativo",
            "caso límite",
            "umbral de decisión",
            "evidencia independiente",
            "evidencia discrepante",
            "coste hundido",
            "evaluación formativa",
            "validación de factores humanos",
            "dossier de aprendizaje",
            "u4",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, self.text)

    def test_experiments_are_predefined_and_decision_oriented(self) -> None:
        theory = norm(json.dumps(self.unit["theory_sections"], ensure_ascii=False))
        self.assertIn("antes de mirar la salida", theory)
        self.assertIn("criterio de refutación", theory)
        self.assertIn("repetición técnica", theory)
        self.assertIn("sobreajuste al banco de pruebas", theory)
        self.assertIn("continuar, revisar el prototipo, reformular el supuesto, pivotar", theory)

    def test_mvp_and_validation_are_bounded(self) -> None:
        purpose = norm(self.unit["purpose"])
        self.assertIn("mvp educativo", purpose)
        self.assertIn("producto médico validado", purpose)
        self.assertIn("seguro, eficaz", purpose)
        self.assertIn("investigación con personas", purpose)
        self.assertIn("no autoriza saltarse gestión de riesgos", self.text)
        self.assertIn("no un producto para uso humano", self.text)
        self.assertIn("no demuestra desempeño en pacientes", self.text)

    def test_learning_scaffolds_are_substantial(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 45)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertEqual(len(self.unit["guided_activities"]), 1)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 12)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 9)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 18)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)

    def test_sources_are_verified_and_multisource(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 15)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = " ".join(item["url"].casefold() for item in sources)
        for domain in ("biodesign.stanford.edu", "fda.gov", "nih.gov", "nimh.nih.gov", "who.int", "iso.org"):
            with self.subTest(domain=domain):
                self.assertIn(domain, urls)

    def test_editorial_boundaries_are_explicit(self) -> None:
        notice = norm(self.unit["editorial_notice"])
        for boundary in (
            "no constituye investigación con seres humanos",
            "customer discovery real",
            "validación de factores humanos",
            "validación clínica",
            "seguridad o eficacia",
            "autorización para uso humano",
            "propiedad intelectual",
            "reembolso",
            "recomendación de inversión",
        ):
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, notice)

    def test_published_descriptor_matches_canonical_unit(self) -> None:
        published = next(item for item in self.subject["detailed_units"] if item["unit"] == 3)
        self.assertEqual(published["title"], self.unit["title"])
        self.assertEqual(published["description"], self.unit["purpose"])
        self.assertIn("fidelidad mínima necesaria", norm(published["description"]))
        self.assertIn("mvp educativo", norm(published["description"]))


if __name__ == "__main__":
    unittest.main()
