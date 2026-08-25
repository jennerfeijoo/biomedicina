from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/informatica-biomedica/units/unit-04.json"
MIRROR = ROOT / "data/generated_units/informatica-biomedica/unit-04.json"
DESCRIPTOR = ROOT / "data/subjects/ingenieria-biomedica/informatica-biomedica.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class TestInformaticaBiomedicaUnit04Curated(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = load_json(SOURCE)
        cls.mirror = load_json(MIRROR)
        cls.descriptor = load_json(DESCRIPTOR)
        cls.text = json.dumps(cls.unit, ensure_ascii=False).lower()

    def test_source_and_generated_mirror_are_identical(self) -> None:
        self.assertEqual(self.unit, self.mirror)

    def test_published_descriptor_matches_canonical_purpose(self) -> None:
        published = next(item for item in self.descriptor["detailed_units"] if item["unit"] == 4)
        self.assertEqual(published["description"], self.unit["purpose"])

    def test_identity_and_depth(self) -> None:
        self.assertEqual(self.unit["subject_id"], "informatica-biomedica")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["slug"], "analitica-y-apoyo-a-decisiones")
        self.assertEqual(self.unit["status"], "review")
        self.assertGreaterEqual(len(self.unit["learning_objectives"]), 6)
        self.assertGreaterEqual(len(self.unit["theory_sections"]), 5)
        for section in self.unit["theory_sections"]:
            self.assertGreaterEqual(len(section["paragraphs"]), 5)
            self.assertGreaterEqual(len(section["key_points"]), 5)
            for point in section["key_points"]:
                self.assertGreaterEqual(len(point.split()), 4)
        self.assertGreaterEqual(len(self.unit["glossary"]), 40)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 16)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        self.assertGreaterEqual(len(self.unit["sources"]), 15)

    def test_guided_activity_is_substantive(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["instructions"]), 10)
        self.assertGreaterEqual(len(activity["problems"]), 18)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 18)

    def test_generic_template_is_removed(self) -> None:
        banned = [
            "concepto de la unidad que debe definirse",
            "modelo conceptual de analítica y apoyo a decisiones",
            "integrar cohortes, modelos, alertas y evaluación para resolver un caso",
            "construir un modelo que conecte cohortes con modelos",
        ]
        for marker in banned:
            self.assertNotIn(marker, self.text)

    def test_temporal_cohort_boundaries_are_explicit(self) -> None:
        for concept in [
            "tiempo cero",
            "ventana de observación",
            "ventana de predicción",
            "fuga temporal",
            "unidad de observación",
            "validación temporal",
            "validación externa",
        ]:
            self.assertIn(concept, self.text)
        self.assertIn("prohibir variables registradas después", self.text)
        self.assertIn("mismo paciente en una sola partición", self.text)

    def test_prediction_performance_is_not_collapsed_to_auc(self) -> None:
        for concept in [
            "auroc",
            "calibración",
            "calibration-in-the-large",
            "pendiente de calibración",
            "brier score",
            "ppv",
            "npv",
            "beneficio neto",
            "decision curve analysis",
        ]:
            self.assertIn(concept, self.text)
        self.assertIn("un auroc alto puede coexistir con probabilidades sistemáticamente demasiado altas o bajas", self.text)
        self.assertIn("ppv y npv dependen de la prevalencia", self.text)

    def test_thresholds_and_alerts_have_operational_denominators(self) -> None:
        self.assertIn("matriz de confusión", self.text)
        self.assertIn("carga de alertas", self.text)
        self.assertIn("firing rate", self.text)
        self.assertIn("acceptance rate", self.text)
        self.assertIn("override rate", self.text)
        self.assertIn("override rate o acceptance rate son métricas de comportamiento y no equivalen por sí solas a alert fatigue", self.text)
        self.assertIn("los criterios de aceptación se predefinen", self.text)

    def test_cds_architecture_and_workflow_are_explicit(self) -> None:
        for concept in [
            "five rights",
            "cds hooks",
            "clinical quality language",
            "cql",
            "fhir",
            "patient-view",
            "silent mode",
        ]:
            self.assertIn(concept, self.text)
        self.assertIn("fhir y cds hooks integran datos y eventos pero no validan contenido clínico", self.text)
        self.assertIn("que una expresión compile o ejecute contra fhir no valida la evidencia clínica", self.text)

    def test_evaluation_layers_are_separated(self) -> None:
        self.assertIn("offline, simulación, silent mode y uso visible responden preguntas diferentes", self.text)
        self.assertIn("desempeño predictivo no equivale a efecto de una intervención cds", self.text)
        self.assertIn("antes-después puede confundir intervención con tendencias y cointervenciones", self.text)
        self.assertIn("cambios de población, software o workflow pueden exigir revalidación", self.text)

    def test_examples_and_self_assessment_are_reasoned(self) -> None:
        for example in self.unit["worked_examples"]:
            self.assertGreaterEqual(len(example["reasoning_steps"]), 5)
            self.assertTrue(example["interpretation"].strip())
            self.assertGreaterEqual(len(example["limitations"]), 3)
        for item in self.unit["self_assessment"]:
            self.assertTrue(item["answer"].strip())
            self.assertTrue(item["reasoning"].strip())
            self.assertTrue(item["common_error"].strip())

    def test_sources_are_verified_and_current_domains_are_present(self) -> None:
        for source in self.unit["sources"]:
            self.assertEqual(source["verification_status"], "verified_directly")
            self.assertTrue(source["url"].startswith("https://"))
        urls = " ".join(source["url"].lower() for source in self.unit["sources"])
        for domain in ["ahrq.gov", "hl7.org", "fda.gov", "bmj.com", "nature.com", "pubmed.ncbi.nlm.nih.gov"]:
            self.assertIn(domain, urls)

    def test_editorial_notice_blocks_clinical_overreach(self) -> None:
        notice = self.unit["editorial_notice"].lower()
        for phrase in [
            "no interpreta historias clínicas reales",
            "no diagnostica",
            "ni recomienda tratamientos",
            "no sustituye validación clínica",
            "no para clasificar un producto concreto",
        ]:
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
