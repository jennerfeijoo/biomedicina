from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "senales-biomedicas" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "senales-biomedicas" / "unit-06.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"
OLD_GENERIC_SNR = r"\mathrm{SNR}_{dB}=10\log_{10}\left(\frac{P_s}{P_n}\right)"


class SenalesBiomedicasUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "senales-biomedicas")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_irrelevant_snr_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertNotIn(OLD_GENERIC_SNR, equations)
        for concept in (
            "calibración",
            "brier score",
            "incertidumbre predictiva",
            "shap",
            "dataset shift",
            "monitorización",
            "human-ai team",
            "reentrenamiento",
        ):
            self.assertIn(concept, self.text)

    def test_theory_is_substantive_and_distinct_from_u5(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(
            text
            for section in sections
            for text in (*section["paragraphs"], *section["key_points"])
        ).casefold()
        for phrase in (
            "auroc alto no autoriza",
            "atribución predictiva no equivale a causalidad fisiológica",
            "un cambio estadístico en una característica no demuestra pérdida de desempeño",
            "el rendimiento aislado del algoritmo no describe el rendimiento del equipo humano-ai",
        ):
            self.assertIn(phrase, theory)
        self.assertIn("unidad 5 termina con un procedimiento predictivo bloqueado", theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        expected = {
            r"\mathrm{Brier}=\frac{1}{N}\sum_{i=1}^{N}(p_i-y_i)^2",
            r"\operatorname{logit}\Pr(Y=1)=\alpha+\beta\operatorname{logit}(p)",
            r"\Delta m_t=m_t-m_{ref}",
            r"\mathrm{FPR}=\frac{FP}{FP+TN}",
        }
        self.assertTrue(expected.issubset(equations))

    def test_guided_activities_are_progressive_reproducible_and_safe(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertTrue(all(len(item["instructions"]) >= 5 for item in activities))
        self.assertTrue(all(len(item["problems"]) >= 10 for item in activities))
        self.assertTrue(all(len(item["checking_criteria"]) >= 6 for item in activities))
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        for concept in (
            "datos sintéticos",
            "calibración",
            "distribución de referencia",
            "fidelidad",
            "baseline de producción",
            "umbral",
            "incidente",
            "revalidación",
        ):
            self.assertIn(concept, activity_text)
        self.assertIn("no reentrenes automáticamente", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 28)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        expected_terms = {
            "calibración",
            "brier score",
            "incertidumbre predictiva",
            "explicación post hoc",
            "shap",
            "transparencia",
            "dataset shift",
            "covariate shift",
            "label shift",
            "concept drift",
            "baseline de producción",
            "monitorización",
            "human-ai team",
            "recalibración",
            "reentrenamiento",
            "uso previsto",
        }
        self.assertTrue(expected_terms.issubset(terms))

    def test_sources_are_traceable_and_directly_verified(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 11)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        expected = {
            "https://www.bmj.com/content/385/bmj-2023-078378",
            "https://www.nature.com/articles/s41591-022-01772-9",
            "https://www.fda.gov/medical-devices/software-medical-device-samd/good-machine-learning-practice-medical-device-development-guiding-principles",
            "https://www.fda.gov/medical-devices/software-medical-device-samd/transparency-machine-learning-enabled-medical-devices-guiding-principles",
            "https://proceedings.mlr.press/v70/guo17a.html",
            "https://proceedings.neurips.cc/paper_files/paper/2019/hash/8558cb408c1d76621371888657d2eb1d-Abstract.html",
            "https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10",
            "https://www.who.int/publications/i/item/9789240029200",
        }
        self.assertTrue(expected.issubset(urls))

    def test_clinical_and_deployment_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("validación clínica", notice)
        self.assertIn("no autorizan conectar sensores a personas", notice)
        self.assertIn("explicaciones post hoc no se presentan como causalidad fisiológica", notice)
        self.assertIn("dataset shift no demuestran por sí solas deterioro clínico", notice)
        self.assertIn("cualquier recalibración o reentrenamiento se trata como una nueva versión", notice)
        self.assertIn("sin convertir una explicación local en mecanismo fisiológico", purpose)
        self.assertIn("autorización de uso asistencial", purpose)


# Final user-authored trigger after publication metadata synchronization.
if __name__ == "__main__":
    unittest.main()
