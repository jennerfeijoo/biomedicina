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

    def test_generic_template_and_old_generic_snr_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertNotIn(OLD_GENERIC_SNR, equations)
        for concept in (
            "calibración",
            "abstención",
            "explicabilidad",
            "dataset shift",
            "monitorización posdespliegue",
            "rollback",
            "uso previsto",
        ):
            self.assertIn(concept, self.text)

    def test_theory_is_substantive_and_preserves_deployment_boundaries(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "discriminación",
            "gráfica de calibración",
            "incertidumbre epistémica",
            "fidelidad",
            "estabilidad",
            "cambio de distribución",
            "etiquetas",
            "recalibración",
            "revalidación",
            "interacción humana",
        ):
            self.assertIn(concept, theory)
        self.assertIn("validación offline no demuestra", theory)
        self.assertIn("no demuestra que el modelo haya fallado", theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        expected = {
            r"\mathrm{Brier}=\frac{1}{N}\sum_{i=1}^{N}(p_i-y_i)^2",
            r"\Pr(Y=1\mid \hat p\approx q)\approx q",
            r"\mathrm{Cobertura}=\frac{N_{aceptados}}{N_{total}}",
            r"f(\mathbf x)\approx \phi_0+\sum_{j=1}^{p}\phi_j",
            r"\mathrm{SMD}_j=\frac{\mu_{j,t}-\mu_{j,ref}}{s_{pooled}}",
            r"C(t)=c_{FN}FN(t)+c_{FP}FP(t)",
        }
        self.assertTrue(expected.issubset(equations))

    def test_explainability_is_not_treated_as_validation_or_causality(self) -> None:
        for phrase in (
            "no se convierte automáticamente en biomarcador causal",
            "la explicación tampoco sustituye validación",
            "no deben interpretarse automáticamente como efectos causales",
            "no se presenta atribución como causalidad",
        ):
            self.assertIn(phrase, self.text)

    def test_monitoring_has_layers_alerts_and_actions(self) -> None:
        for phrase in (
            "capa de entrada",
            "capa de salida",
            "capa de desempeño",
            "no existe un umbral universal de deriva",
            "recalibrar",
            "revalidar externamente",
            "volver a una versión anterior",
            "suspender el sistema",
        ):
            self.assertIn(phrase, self.text)

    def test_guided_activities_are_progressive_reproducible_and_safe(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertTrue(all(len(item["instructions"]) >= 5 for item in activities))
        self.assertTrue(all(len(item["problems"]) >= 10 for item in activities))
        self.assertTrue(all(len(item["checking_criteria"]) >= 6 for item in activities))
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        for concept in (
            "brier score",
            "zona de abstención",
            "explicación local",
            "perturbaciones",
            "monitorización",
            "rollback",
            "datos sintéticos",
        ):
            self.assertIn(concept, activity_text)
        self.assertIn("no uses datos personales", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 28)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        expected_terms = {
            "calibración",
            "brier score",
            "incertidumbre epistémica",
            "abstención",
            "cobertura",
            "explicación local",
            "fidelidad",
            "dataset shift",
            "monitorización de desempeño",
            "recalibración",
            "revalidación",
            "rollback",
            "uso previsto",
            "pccp",
        }
        self.assertTrue(expected_terms.issubset(terms))

    def test_sources_are_traceable_and_directly_verified(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        expected = {
            "https://www.bmj.com/content/385/bmj-2023-078378",
            "https://www.nature.com/articles/s41591-022-01772-9",
            "https://pubmed.ncbi.nlm.nih.gov/34711379/",
            "https://pubmed.ncbi.nlm.nih.gov/34260843/",
            "https://pubmed.ncbi.nlm.nih.gov/31842878/",
            "https://pubmed.ncbi.nlm.nih.gov/37526541/",
            "https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10",
            "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/artificial-intelligence-enabled-device-software-functions-lifecycle-management-and-marketing",
            "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/marketing-submission-recommendations-predetermined-change-control-plan-artificial-intelligence",
        }
        self.assertTrue(expected.issubset(urls))

    def test_regulatory_and_clinical_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("validación clínica", notice)
        self.assertIn("guías de reporte", notice)
        self.assertIn("marco voluntario", notice)
        self.assertIn("sigue siendo borrador", notice)
        self.assertIn("beneficio clínico demostrado", purpose)


# Final user-authored trigger after publication synchronization and regression alignment.
if __name__ == "__main__":
    unittest.main()
