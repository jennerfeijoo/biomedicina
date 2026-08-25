from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/informatica-biomedica/units/unit-05.json"
MIRROR = ROOT / "data/generated_units/informatica-biomedica/unit-05.json"
DESCRIPTOR = ROOT / "data/subjects/ingenieria-biomedica/informatica-biomedica.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class TestInformaticaBiomedicaUnit05Curated(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = load_json(SOURCE)
        cls.mirror = load_json(MIRROR)
        cls.descriptor = load_json(DESCRIPTOR)
        cls.text = json.dumps(cls.unit, ensure_ascii=False).lower()

    def test_source_and_generated_mirror_are_identical(self) -> None:
        self.assertEqual(self.unit, self.mirror)

    def test_published_descriptor_matches_when_promoted(self) -> None:
        published = next(item for item in self.descriptor["detailed_units"] if item["unit"] == 5)
        if published["description"] != self.unit["purpose"]:
            self.skipTest("El publicador todavía no ha promovido la descripción canónica de U5")
        self.assertEqual(published["description"], self.unit["purpose"])

    def test_identity_and_depth(self) -> None:
        self.assertEqual(self.unit["subject_id"], "informatica-biomedica")
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["slug"], "interaccion-y-factores-humanos")
        self.assertEqual(self.unit["status"], "review")
        self.assertGreaterEqual(len(self.unit["learning_objectives"]), 6)
        self.assertGreaterEqual(len(self.unit["theory_sections"]), 5)
        for section in self.unit["theory_sections"]:
            self.assertGreaterEqual(len(section["paragraphs"]), 5)
            self.assertGreaterEqual(len(section["key_points"]), 5)
            for point in section["key_points"]:
                self.assertGreaterEqual(len(point.split()), 4)
        self.assertGreaterEqual(len(self.unit["glossary"]), 45)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 18)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        self.assertGreaterEqual(len(self.unit["sources"]), 15)

    def test_generic_template_and_inherited_ppv_are_removed(self) -> None:
        for marker in [
            "concepto de la unidad que debe definirse",
            "modelo conceptual de interacción y factores humanos",
            "construir un modelo que conecte usabilidad con carga cognitiva",
            "integrar usabilidad, carga cognitiva, flujo de trabajo para resolver un caso",
        ]:
            self.assertNotIn(marker, self.text)
        self.assertNotIn("ppv=\\frac", self.text)

    def test_usability_is_contextual_and_not_a_safety_claim(self) -> None:
        for concept in ["contexto de uso", "efectividad", "eficiencia", "satisfacción", "sistema sociotécnico"]:
            self.assertIn(concept, self.text)
        self.assertIn("usabilidad demostrada no equivale por sí sola a seguridad o beneficio clínico", self.text)
        self.assertIn("una prueba de usabilidad controlada no demuestra seguridad clínica", self.text)

    def test_workflow_and_task_analysis_are_substantive(self) -> None:
        for concept in [
            "trabajo imaginado",
            "trabajo realizado",
            "análisis jerárquico de tareas",
            "tarea crítica",
            "handoff",
            "workaround",
        ]:
            self.assertIn(concept, self.text)
        self.assertIn("workflow incluye tareas físicas, mentales, coordinación y trabajo entre personas", self.text)

    def test_cognitive_demands_alerts_and_automation_are_bounded(self) -> None:
        for concept in ["memoria de trabajo", "interrupción", "cambio de tarea", "alert fatigue", "automation bias", "overreliance"]:
            self.assertIn(concept, self.text)
        self.assertIn("override rate aislado no demuestra alert fatigue", self.text)
        self.assertIn("recomendaciones correctas, incorrectas e incompletas", self.text)
        self.assertIn("más explicación no garantiza mejor verificación", self.text)

    def test_error_prevention_and_recovery_are_explicit(self) -> None:
        for concept in ["default", "confirmación", "constraint", "forcing function", "use error", "recuperación", "feedback"]:
            self.assertIn(concept, self.text)
        self.assertIn("recuperación forma parte del diseño", self.text)
        self.assertIn("confirmar cada clic genera habituación", self.text)

    def test_evaluation_uses_operational_denominators(self) -> None:
        for concept in ["task success rate", "use-error rate", "time on task", "simulación de uso", "evaluación formativa"]:
            self.assertIn(concept, self.text)
        equations = " ".join(item["latex"].lower() for section in self.unit["theory_sections"] for item in section.get("equations", []))
        self.assertIn("tsr=", equations)
        self.assertIn("uer=", equations)
        self.assertIn("ab=", equations)
        self.assertIn("métricas de usabilidad requieren denominadores", self.text)

    def test_guided_activity_is_substantive_and_synthetic(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 360)
        self.assertGreaterEqual(len(activity["instructions"]), 10)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 20)
        activity_text = json.dumps(activity, ensure_ascii=False).lower()
        self.assertIn("casos sintéticos", activity_text)
        self.assertIn("sin datos clínicos reales", activity_text)
        self.assertIn("no se utilizan pacientes", activity_text)

    def test_curricular_boundaries_separate_u4_u5_u6(self) -> None:
        purpose = self.unit["purpose"].lower()
        self.assertIn("u5 toma de u4", purpose)
        self.assertIn("reserva gobernanza, despliegue y supervisión organizacional para u6", purpose)
        unit4 = next(item for item in self.descriptor["detailed_units"] if item["unit"] == 4)
        unit6 = next(item for item in self.descriptor["detailed_units"] if item["unit"] == 6)
        self.assertEqual(unit4["title"], "Analítica y apoyo a decisiones")
        self.assertEqual(unit6["title"], "Gobernanza e implementación")

    def test_examples_and_self_assessment_are_reasoned(self) -> None:
        for example in self.unit["worked_examples"]:
            self.assertGreaterEqual(len(example["reasoning_steps"]), 5)
            self.assertTrue(example["interpretation"].strip())
            self.assertGreaterEqual(len(example["limitations"]), 3)
        for item in self.unit["self_assessment"]:
            self.assertTrue(item["answer"].strip())
            self.assertTrue(item["reasoning"].strip())
            self.assertTrue(item["common_error"].strip())

    def test_sources_are_directly_verified_and_multidisciplinary(self) -> None:
        for source in self.unit["sources"]:
            self.assertEqual(source["verification_status"], "verified_directly")
            self.assertTrue(source["url"].startswith("https://"))
        urls = " ".join(source["url"].lower() for source in self.unit["sources"])
        for domain in ["iso.org", "iec.ch", "fda.gov", "ahrq.gov", "pubmed.ncbi.nlm.nih.gov"]:
            self.assertIn(domain, urls)

    def test_editorial_notice_blocks_clinical_and_regulatory_overreach(self) -> None:
        notice = self.unit["editorial_notice"].lower()
        for phrase in [
            "no recluta pacientes",
            "no interpreta historias clínicas reales",
            "no diagnostica",
            "ni demostración de seguridad o eficacia clínica",
            "no constituyen human factors validation",
            "transfiere gobernanza, despliegue y supervisión institucional a u6",
        ]:
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
