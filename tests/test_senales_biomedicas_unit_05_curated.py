from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "senales-biomedicas" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "senales-biomedicas" / "unit-05.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"
OLD_GENERIC_SNR = r"\mathrm{SNR}_{dB}=10\log_{10}\left(\frac{P_s}{P_n}\right)"


class SenalesBiomedicasUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "senales-biomedicas")
        self.assertEqual(self.unit["unit"], 5)
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
            "unidad de generalización",
            "fuga de datos",
            "groupkfold",
            "pipeline",
            "validación anidada",
            "test bloqueado",
            "auprc",
            "balanced accuracy",
        ):
            self.assertIn(concept, self.text)

    def test_theory_is_substantive_and_preserves_validation_boundaries(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "múltiples filas por sujeto",
            "selección de características",
            "dentro de cada fold",
            "baseline",
            "regularización",
            "matriz de confusión",
            "prevalencia",
            "validación interna",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no demuestra utilidad clínica", theory)

    def test_core_modeling_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        expected = {
            r"z_j=\frac{x_j-\mu_{j,train}}{\sigma_{j,train}}",
            r"\mathbf X\in\mathbb R^{n\times p}",
            r"p(y=1\mid\mathbf x)=\frac{1}{1+e^{-(\beta_0+\boldsymbol\beta^T\mathbf x)}}",
            r"\mathrm{Sensibilidad}=\frac{TP}{TP+FN}",
            r"\mathrm{PPV}=\frac{TP}{TP+FP}",
            r"\mathrm{BalancedAccuracy}=\frac{1}{2}\left(\frac{TP}{TP+FN}+\frac{TN}{TN+FP}\right)",
        }
        self.assertTrue(expected.issubset(equations))

    def test_grouped_split_and_training_only_transformations_are_explicit(self) -> None:
        for phrase in (
            "ninguna ventana del mismo sujeto puede aparecer en entrenamiento y prueba",
            "toda operación que aprenda parámetros debe vivir dentro de la rama de entrenamiento",
            "remuestreo",
            "el conjunto de prueba solo recibe transformaciones ya aprendidas",
            "no participa en escoger variables, umbrales, hiperparámetros",
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
            "split agrupado por sujeto",
            "selección de características",
            "pipeline",
            "validación anidada",
            "baseline",
            "modelo bloqueado",
        ):
            self.assertIn(concept, activity_text)
        self.assertIn("datos sintéticos", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        expected_terms = {
            "característica",
            "unidad de generalización",
            "fuga de datos",
            "fuga por sujeto",
            "pipeline",
            "selección de características",
            "validación cruzada anidada",
            "test bloqueado",
            "auroc",
            "auprc",
            "balanced accuracy",
            "modelo bloqueado",
        }
        self.assertTrue(expected_terms.issubset(terms))

    def test_sources_are_traceable_and_directly_verified(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        expected = {
            "https://pubmed.ncbi.nlm.nih.gov/38418819/",
            "https://pubmed.ncbi.nlm.nih.gov/33846489/",
            "https://pubmed.ncbi.nlm.nih.gov/34817740/",
            "https://pubmed.ncbi.nlm.nih.gov/25738806/",
            "https://pubmed.ncbi.nlm.nih.gov/28655633/",
            "https://pubmed.ncbi.nlm.nih.gov/38626948/",
            "https://scikit-learn.org/stable/common_pitfalls.html",
            "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html",
            "https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html",
        }
        self.assertTrue(expected.issubset(urls))

    def test_u6_and_clinical_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("validación clínica", notice)
        self.assertIn("no demuestra utilidad clínica", notice)
        self.assertIn("interpretación, explicabilidad y monitorización operativa", notice)
        self.assertIn("unidad 6", notice)
        self.assertIn("sin convertir desempeño interno en utilidad clínica", purpose)


# Final user-authored trigger after source, mirror, descriptor and public-page synchronization.
if __name__ == "__main__":
    unittest.main()
