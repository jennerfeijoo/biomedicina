from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "electrofisica-electromecanica" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "electrofisica-electromecanica" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ElectrofisicaElectromecanicaUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "electrofisica-electromecanica")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_signal_template_is_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("snr", self.text)
        self.assertNotIn("cadena física de transducción, acondicionamiento, adquisición", self.text)

    def test_theory_covers_transients_impedance_power_and_bioimpedance(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in (
            "transitorios rc y rl", "condiciones iniciales", "impedancia compleja",
            "régimen sinusoidal", "resonancia", "potencia media", "factor de potencia",
            "bioimpedancia", "circuito equivalente", "interfaz electrodo-tejido",
        ):
            self.assertIn(concept, self.text)
        for boundary in ("u2", "u4", "u5", "u6"):
            self.assertIn(boundary, theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        for equation in (
            "\\tau_{RC}=RC",
            "\\tau_L=\\frac{L}{R}",
            "Z_R=R,\\qquad Z_L=j\\omega L,\\qquad Z_C=\\frac{1}{j\\omega C}",
            "Z_{serie}=R+j\\left(\\omega L-\\frac{1}{\\omega C}\\right)",
            "\\omega_0=\\frac{1}{\\sqrt{LC}}",
            "P_{avg}=V_{rms}I_{rms}\\cos\\phi",
            "Z_{eq}(\\omega)=R_s+\\frac{R_p}{1+j\\omega R_pC_p}",
        ):
            self.assertIn(equation, equations)

    def test_transient_continuity_and_domain_boundaries_are_explicit(self) -> None:
        self.assertIn("v_c(0+)=v_c(0−)", self.text)
        self.assertIn("i_l(0+)=i_l(0−)", self.text)
        self.assertIn("63.2 %", self.text)
        self.assertIn("régimen sinusoidal estacionario", self.text)
        self.assertIn("no el transitorio de encendido", self.text)

    def test_guided_activity_is_scaffolded_reproducible_and_safe(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 8)
        self.assertGreaterEqual(len(activity["problems"]), 16)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 14)
        activity_text = json.dumps(activity, ensure_ascii=False).casefold()
        for phrase in (
            "no conectes red eléctrica", "personas", "sintéticos",
            "impedancias complejas", "circuito equivalente", "inferencia clínica",
        ):
            self.assertIn(phrase, activity_text)

    def test_learning_scaffolds_are_specific_and_sufficient(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 28)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 14)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "constante de tiempo", "fasor", "impedancia", "reactancia",
            "factor de potencia", "resonancia", "factor de calidad",
            "bioimpedancia", "espectroscopia de impedancia", "circuito equivalente",
        ):
            self.assertIn(term, terms)

    def test_bioimpedance_is_not_taught_as_diagnosis_or_unique_anatomy(self) -> None:
        theory = " ".join(p for section in self.unit["theory_sections"] for p in section["paragraphs"]).casefold()
        self.assertIn("no es una propiedad clínica universal", theory)
        self.assertIn("no deben identificarse automáticamente con una estructura anatómica única", theory)
        self.assertIn("buen ajuste no demuestra mecanismo causal, diagnóstico o utilidad clínica", theory)
        self.assertIn("datos sintéticos", theory)

    def test_sources_are_directly_verified_and_cover_core_and_biomedical_context(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 12)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://openstax.org/books/university-physics-volume-2/pages/10-5-rc-circuits",
            "https://openstax.org/books/university-physics-volume-2/pages/14-4-rl-circuits",
            "https://openstax.org/books/university-physics-volume-2/pages/15-3-rlc-series-circuits-with-ac",
            "https://openstax.org/books/university-physics-volume-2/pages/15-4-power-in-an-ac-circuit",
            "https://openstax.org/books/university-physics-volume-2/pages/15-5-resonance-in-an-ac-circuit",
            "https://pubmed.ncbi.nlm.nih.gov/33749256/",
            "https://pubmed.ncbi.nlm.nih.gov/36785772/",
            "https://pubmed.ncbi.nlm.nih.gov/41007171/",
            "https://pubmed.ncbi.nlm.nih.gov/42523918/",
        ):
            self.assertIn(url, urls)

    def test_professional_and_course_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for boundary in (
            "no constituyen revisión disciplinar externa",
            "validación clínica", "validación de un dispositivo",
            "seguridad eléctrica", "compatibilidad electromagnética",
            "no autorizan conectar red eléctrica", "personas",
            "operar dispositivos médicos", "emitir diagnósticos",
        ):
            self.assertIn(boundary, notice)
        purpose = self.unit["purpose"].casefold()
        self.assertIn("u2", purpose)
        self.assertIn("no constituyen caracterización de una persona o tejido real", purpose)


if __name__ == "__main__":
    unittest.main()
