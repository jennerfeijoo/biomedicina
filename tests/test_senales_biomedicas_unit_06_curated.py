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
            "sanity check",
            "dataset shift",
            "signal quality index",
            "monitorización por subgrupos",
            "modelo bloqueado",
            "reentrenamiento",
        ):
            self.assertIn(concept, self.text)

    def test_theory_is_substantive_and_preserves_u5_boundary(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "discriminación",
            "calibración",
            "atribución",
            "no demuestra que el rasgo sea causal",
            "covariate shift",
            "concept drift",
            "etiquetas llegan con retraso",
            "supervisión humana",
            "cambio controlado",
        ):
            self.assertIn(concept, theory)
        self.assertIn("la unidad 5 termina", theory)
        self.assertIn("no demuestra beneficio clínico", theory)

    def test_core_equations_are_present_and_bounded(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        expected = {
            r"\mathrm{BS}=\frac{1}{N}\sum_{i=1}^{N}(p_i-y_i)^2",
            r"g_b=\bar p_b-\bar y_b",
            r"H(p)=-p\log p-(1-p)\log(1-p)",
            r"\Delta f_j=f(\mathbf x+\delta_j)-f(\mathbf x)",
            r"\Delta z_j=\frac{\mu_{j,current}-\mu_{j,ref}}{\sigma_{j,ref}}",
            r"\Delta M=M_{current}-M_{reference}",
        }
        self.assertTrue(expected.issubset(equations))
        meanings = " ".join(
            equation.get("meaning", "")
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        ).casefold()
        self.assertIn("no constituye un umbral universal", meanings)
        self.assertIn("no convierte la diferencia en efecto causal", meanings)

    def test_guided_activities_are_progressive_reproducible_and_safe(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertTrue(all(len(item["instructions"]) >= 5 for item in activities))
        self.assertTrue(all(len(item["problems"]) >= 10 for item in activities))
        self.assertTrue(all(len(item["checking_criteria"]) >= 6 for item in activities))
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        for concept in (
            "sintétic",
            "calibración",
            "sanity check",
            "monitorización",
            "etiquetas diferidas",
            "subgrupos",
            "registro de cambios",
            "revalidación",
        ):
            self.assertIn(concept, activity_text)
        self.assertIn("no se autoriza despliegue clínico", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        expected_terms = {
            "calibración",
            "brier score",
            "incertidumbre predictiva",
            "explicabilidad",
            "atribución",
            "saliencia",
            "sanity check",
            "signal quality index",
            "dataset shift",
            "covariate shift",
            "concept drift",
            "monitorización",
            "modelo bloqueado",
            "abstención",
            "modo sombra",
            "reentrenamiento",
        }
        self.assertTrue(expected_terms.issubset(terms))

    def test_sources_are_traceable_directly_verified_and_lifecycle_aware(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 12)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        expected = {
            "https://pubmed.ncbi.nlm.nih.gov/32106284/",
            "https://pubmed.ncbi.nlm.nih.gov/34711379/",
            "https://papers.nips.cc/paper/2018/hash/294a8ed24b1ad22ec2e7efea049b8737-Abstract.html",
            "https://pubmed.ncbi.nlm.nih.gov/25069129/",
            "https://pubmed.ncbi.nlm.nih.gov/34470057/",
            "https://pubmed.ncbi.nlm.nih.gov/40876698/",
            "https://pubmed.ncbi.nlm.nih.gov/38626948/",
            "https://pubmed.ncbi.nlm.nih.gov/35584845/",
            "https://www.fda.gov/medical-devices/software-medical-device-samd/good-machine-learning-practice-medical-device-development-guiding-principles",
            "https://www.fda.gov/medical-devices/software-medical-device-samd/transparency-machine-learning-enabled-medical-devices-guiding-principles",
        }
        self.assertTrue(expected.issubset(urls))

    def test_editorial_boundary_rejects_clinical_and_regulatory_overreach(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        for phrase in (
            "no constituyen revisión disciplinar externa",
            "validación clínica",
            "certificación regulatoria",
            "no autorizan conectar sensores o circuitos a personas",
            "nueva versión",
        ):
            self.assertIn(phrase, notice)
        self.assertIn("sin presentar la validación interna de u5 como utilidad clínica", purpose)
        self.assertIn("ni autorizar despliegue asistencial", purpose)


# Final human-authored trigger after publication synchronization and semantic regression repair.
if __name__ == "__main__":
    unittest.main()
