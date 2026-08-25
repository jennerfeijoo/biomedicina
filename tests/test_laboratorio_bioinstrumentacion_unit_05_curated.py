from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "laboratorio-bioinstrumentacion" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "laboratorio-bioinstrumentacion" / "unit-05.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class LaboratorioBioinstrumentacionUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "laboratorio-bioinstrumentacion")
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed_and_integration_concepts_exist(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        for concept in (
            "contrato de interfaz",
            "throughput útil",
            "buffer",
            "contador de secuencia",
            "timestamp",
            "decoupling",
            "ruta de retorno",
            "gestión de configuración",
            "baseline",
        ):
            self.assertIn(concept, self.text)

    def test_theory_is_substantive_and_keeps_u5_u6_boundary(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        self.assertIn("un buffer desacopla temporalmente productor y consumidor", theory)
        self.assertIn("no crea ancho de banda", theory)
        self.assertIn("las corrientes de conmutación", theory)
        self.assertIn("cada registro de datos debe poder asociarse a una versión de firmware", theory)
        self.assertIn("u6 tomará esta baseline", theory)

    def test_core_equations_are_present(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        for equation in (
            "R_{raw}=f_s N_{ch}\\frac{N_b}{8}",
            "\\Delta B=(R_{prod}-R_{cons})\\Delta t",
            "P_{tot}\\approx\\sum_i V_i I_i",
            "x_{phys}=a\\,code+b",
            "L_{loss}=1-\\frac{N_{rec}}{N_{exp}}",
        ):
            self.assertIn(equation, equations)

    def test_guided_activities_are_progressive_synthetic_and_auditable(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertGreaterEqual(len(activities), 3)
        self.assertGreaterEqual(len(activities[0]["problems"]), 12)
        self.assertGreaterEqual(len(activities[1]["problems"]), 18)
        self.assertGreaterEqual(len(activities[1]["deliverables"]), 12)
        self.assertGreaterEqual(len(activities[1]["checking_criteria"]), 12)
        self.assertGreaterEqual(len(activities[2]["tasks"]), 9)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("no conectes personas", activity_text)
        self.assertIn("contador de secuencia", activity_text)
        self.assertIn("baseline", activity_text)
        self.assertIn("handoff explícito a u6", activity_text)

    def test_glossary_examples_errors_and_assessment_are_specific(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 28)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "contrato de interfaz",
            "spi",
            "i²c",
            "usart",
            "throughput útil",
            "overrun",
            "crc",
            "gestión de configuración",
            "punto de prueba",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_cover_interfaces_power_and_configuration(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://www.analog.com/MT-031",
            "https://www.analog.com/media/en/training-seminars/tutorials/MT-101.pdf",
            "https://www.nxp.com/docs/en/user-guide/UM10204.pdf",
            "https://www.microchip.com/en-us/application-notes/tb3215",
            "https://www.microchip.com/en-us/application-notes/tb3216",
            "https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20170001761.pdf",
        ):
            self.assertIn(url, urls)

    def test_safety_clinical_and_course_boundary_is_explicit(self) -> None:
        purpose = self.unit["purpose"].casefold()
        notice = self.unit["editorial_notice"].casefold()
        self.assertIn("no constituye verificación final", purpose)
        self.assertIn("sin conexión a personas", notice)
        self.assertIn("red eléctrica", notice)
        self.assertIn("no constituye seguridad eléctrica", notice)
        self.assertIn("validación fisiológica o clínica", notice)
        self.assertIn("u5 entrega una baseline integrada", notice)
        self.assertIn("verificación final", notice)
        self.assertIn("u6", notice)
        self.assertIn("revisión disciplinar humana permanece pendiente", notice)


if __name__ == "__main__":
    unittest.main()
