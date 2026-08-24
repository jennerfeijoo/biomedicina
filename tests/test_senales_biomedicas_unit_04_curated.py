from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "senales-biomedicas" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "senales-biomedicas" / "unit-04.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"
OLD_GENERIC_SNR = r"\mathrm{SNR}_{dB}=10\log_{10}\left(\frac{P_s}{P_n}\right)"


class SenalesBiomedicasUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "senales-biomedicas")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_old_generic_equation_are_removed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertNotIn(OLD_GENERIC_SNR, equations)
        for concept in (
            "densidad espectral de potencia",
            "fuga espectral",
            "zero-padding",
            "stft",
            "actividad aperiódica",
            "conducción de volumen",
        ):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_frequency_specific(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "periodograma",
            "welch",
            "hann",
            "espectrograma",
            "potencia de banda",
            "cross-spectrum",
            "coherencia cuadrática",
        ):
            self.assertIn(concept, theory)
        self.assertIn("no identifica dirección, causalidad ni mecanismo anatómico", theory)

    def test_core_frequency_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        expected = {
            r"X[k]=\sum_{n=0}^{N-1}x[n]e^{-j2\pi kn/N}",
            r"\Delta f=\frac{f_s}{N}=\frac{1}{T}",
            r"P_{[f_1,f_2]}=\int_{f_1}^{f_2}S_{xx}(f)\,df",
            r"\widehat{S}_{xx}^{Welch}(f)=\frac{1}{K}\sum_{r=1}^{K}\widehat{S}_{xx,r}(f)",
            r"\mathcal{S}(m,\omega)=|X(m,\omega)|^2",
            r"C_{xy}(f)=\frac{|P_{xy}(f)|^2}{P_{xx}(f)P_{yy}(f)}",
        }
        self.assertTrue(expected.issubset(equations))

    def test_zero_padding_and_time_frequency_boundaries_are_explicit(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertIn("zero-padding interpola la representación espectral", text)
        self.assertIn("no aumenta la información contenida", text)
        self.assertIn("ventanas largas favorecen resolución frecuencial", text)
        self.assertIn("ventanas cortas favorecen localización temporal", text)
        self.assertIn("hop pequeño", text)
        self.assertIn("no hace que ventanas fuertemente solapadas sean observaciones independientes", text)

    def test_guided_activities_are_progressive_quantitative_and_safe(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        self.assertTrue(all(len(item["instructions"]) >= 5 for item in activities))
        self.assertTrue(all(len(item["problems"]) >= 10 for item in activities))
        self.assertTrue(all(len(item["checking_criteria"]) >= 6 for item in activities))
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        for concept in (
            "verdad conocida",
            "zero-padding",
            "espectrograma",
            "potencia absoluta",
            "coherencia espuria",
            "fuente común",
        ):
            self.assertIn(concept, activity_text)
        self.assertIn("no conectes sensores a personas", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 22)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        expected_terms = {
            "dft",
            "fft",
            "periodograma",
            "psd",
            "resolución frecuencial",
            "fuga espectral",
            "método de welch",
            "zero-padding",
            "stft",
            "espectrograma",
            "coherencia",
            "actividad aperiódica",
        }
        self.assertTrue(expected_terms.issubset(terms))

    def test_sources_are_traceable_and_directly_verified(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        expected = {
            "https://doi.org/10.1109/TAU.1967.1161901",
            "https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html",
            "https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.ShortTimeFFT.spectrogram.html",
            "https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.coherence.html",
            "https://pubmed.ncbi.nlm.nih.gov/34268825/",
            "https://pubmed.ncbi.nlm.nih.gov/9402881/",
            "https://pubmed.ncbi.nlm.nih.gov/39549620/",
            "https://pubmed.ncbi.nlm.nih.gov/42495990/",
            "https://pubmed.ncbi.nlm.nih.gov/8737210/",
        }
        self.assertTrue(expected.issubset(urls))

    def test_physiological_and_clinical_boundaries_are_explicit(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("validación clínica", notice)
        self.assertIn("no requieren ni autorizan conectar sensores a personas", notice)
        self.assertIn("no deben interpretarse automáticamente como biomarcadores", notice)
        self.assertIn("no demuestra causalidad ni conectividad anatómica", text)
        self.assertIn("desaconsejan interpretar automáticamente", text)


# Final user-authored trigger after source, mirror and public-page synchronization.
if __name__ == "__main__":
    unittest.main()
