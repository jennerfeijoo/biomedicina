from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "electrofisica-electromecanica" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "electrofisica-electromecanica" / "unit-05.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ElectrofisicaElectromecanicaUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "electrofisica-electromecanica")
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_unrelated_snr_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("\\mathrm{snr}", self.text)
        self.assertNotIn("cadena física de transducción, acondicionamiento, adquisición", self.text)

    def test_theory_is_actuation_and_control_specific(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        for concept in (
            "actuador", "transmisión", "back-emf", "puente h", "solenoide",
            "fuerza–carrera", "realimentación", "pid", "saturación", "windup",
        ):
            self.assertIn(concept, self.text)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        for equation in (
            "P_m=\\tau\\omega",
            "\\tau_m=K_t i",
            "e=K_e\\omega",
            "V=L\\frac{di}{dt}+Ri+K_e\\omega",
            "J\\frac{d\\omega}{dt}+b\\omega=K_t i-\\tau_L",
            "W=\\int_{s_0}^{s_1}F(s)\\,ds",
            "T(s)=\\frac{C(s)G(s)}{1+C(s)G(s)}",
        ):
            self.assertIn(equation, equations)

    def test_motor_model_preserves_units_and_limits(self) -> None:
        self.assertIn("unidades si coherentes", self.text)
        self.assertIn("par continuo", self.text)
        self.assertIn("par de bloqueo", self.text)
        self.assertIn("corriente de bloqueo", self.text)
        self.assertIn("conmutación electrónica", self.text)
        self.assertIn("ciclo de trabajo", self.text)
        self.assertIn("el ciclo de trabajo no es par ni velocidad", self.text)

    def test_solenoid_and_duty_cycle_are_not_overgeneralized(self) -> None:
        self.assertIn("curva fuerza–carrera", self.text)
        self.assertIn("fuerza de retención", self.text)
        self.assertIn("trabajo mecánico", self.text)
        self.assertIn("ciclo de trabajo pwm", self.text)
        self.assertIn("ciclo de trabajo del actuador", self.text)
        self.assertIn("confundir duty cycle pwm con duty cycle térmico", self.text)

    def test_feedback_saturation_and_windup_are_explicit(self) -> None:
        self.assertIn("realimentación no implica estabilidad automática", self.text)
        self.assertIn("integrator windup", self.text)
        self.assertIn("anti-windup", self.text)
        self.assertIn("saturación", self.text)
        self.assertIn("error estacionario", self.text)
        self.assertIn("tiempo de establecimiento", self.text)

    def test_biomedical_tracking_does_not_become_clinical_efficacy(self) -> None:
        self.assertIn("u5 no prescribe una estrategia terapéutica", self.text)
        self.assertIn("una buena simulación no demuestra seguridad ni eficacia clínica", self.text)
        self.assertIn("inferir eficacia clínica de un seguimiento de trayectoria", self.text)
        self.assertIn("el desempeño de control no demuestra beneficio terapéutico ni validez clínica", self.text)

    def test_guided_activity_is_scaffolded_reproducible_and_safe(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 8)
        self.assertGreaterEqual(len(activity["problems"]), 18)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 18)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        for phrase in (
            "sintéticos", "motor", "solenoide", "lazo abierto", "pi",
            "anti-windup", "no se conectan personas",
        ):
            self.assertIn(phrase, text)

    def test_learning_scaffolds_are_specific_and_sufficient(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 40)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 18)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "actuador", "constante de par", "back-emf", "bldc", "pwm",
            "puente h", "solenoide", "pid", "saturación", "anti-windup",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_cover_core_and_biomedical_context(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 16)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://openstax.org/books/university-physics-volume-2/pages/11-5-force-and-torque-on-a-current-loop",
            "https://ctms.engin.umich.edu/CTMS/index.php?example=MotorSpeed&section=SystemModeling",
            "https://support.maxongroup.com/hc/en-us/articles/360005873794-Motor-constants",
            "https://www.microchip.com/en-us/application-notes/an905",
            "https://ww1.microchip.com/downloads/en/appnotes/00885a.pdf",
            "https://www.magnet-schultz.com/fileadmin/Daten/Vertrieb/PR1/TechnErl/GXX_e.pdf",
            "https://www.cds.caltech.edu/~murray/FBS/Second_Edition.html",
            "https://pubmed.ncbi.nlm.nih.gov/38295350/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC8688994/",
            "https://pubmed.ncbi.nlm.nih.gov/41762210/",
        ):
            self.assertIn(url, urls)

    def test_course_and_professional_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no constituyen revisión disciplinar externa",
            "validación clínica",
            "ensayo de seguridad",
            "conformidad regulatoria",
            "no autorizan conectar motores",
            "personas",
            "u4 queda reservada a transductores",
            "u6 a aislamiento",
        ):
            self.assertIn(phrase, notice)
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituyen diseño clínico", purpose)


if __name__ == "__main__":
    unittest.main()
