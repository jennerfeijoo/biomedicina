from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "electrofisica-electromecanica" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "electrofisica-electromecanica" / "unit-06.json"
CATALOG = ROOT / "data" / "catalog_statuses.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ElectrofisicaElectromecanicaUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "electrofisica-electromecanica")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_unrelated_snr_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("\\mathrm{snr}", self.text)
        self.assertNotIn("cadena física de transducción, acondicionamiento, adquisición", self.text)

    def test_course_stays_out_of_template_detected_catalog_status(self) -> None:
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        specificity = catalog["dimensions"]["specificity"]
        subject = "electrofisica-electromecanica"
        self.assertIn(subject, specificity["screened_no_known_template_marker"])
        self.assertNotIn(subject, specificity["template_detected"])

    def test_theory_is_safety_emc_and_verification_specific(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        for concept in (
            "seguridad básica", "desempeño esencial", "fallo único", "mopp", "moop",
            "creepage", "clearance", "corriente de fuga", "inmunidad", "emisiones",
            "esd", "verificación", "trazabilidad",
        ):
            self.assertIn(concept, self.text)

    def test_core_equations_are_present_and_non_normative(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        for equation in (
            "I_C=2\\pi f C V_{rms}",
            "R_{path}=\\frac{V_{drop}}{I_{test}}",
            "i_C(t)=C_p\\frac{dv(t)}{dt}",
            "C_{ver}=\\frac{N_{verificados}}{N_{aplicables}}",
        ):
            self.assertIn(equation, equations)
        self.assertIn("no un método normativo", self.text)
        self.assertIn("no es una puntuación de seguridad", self.text)

    def test_electrical_protection_is_not_overclaimed(self) -> None:
        for phrase in (
            "la conformidad del componente no se hereda automáticamente al sistema",
            "creepage se mide sobre superficie; clearance, a través del aire",
            "la puesta a tierra de protección y el aislamiento controlan rutas de fallo diferentes",
            "los límites y métodos normativos no se deducen",
        ):
            self.assertIn(phrase, self.text)

    def test_component_evidence_is_not_promoted_to_system_conformity(self) -> None:
        errors = " ".join(item["error"].casefold() for item in self.unit["common_errors"])
        corrections = " ".join(item["correction"].casefold() for item in self.unit["common_errors"])
        self.assertIn("componente 2mopp", errors)
        self.assertIn("rutas e interfaces del sistema final", corrections)
        self.assertIn("la conformidad del componente no se hereda automáticamente al sistema", self.text)
        self.assertIn("no constituyen ensayo de conformidad", self.unit["purpose"].casefold())

    def test_applied_parts_and_mop_are_present_without_auto_certification(self) -> None:
        for phrase in (
            "tipo b", "tipo bf", "tipo cf", "mopp", "moop", "parte aplicada",
            "no se asignan como conformes", "arquitectura conceptual y no como certificación",
        ):
            self.assertIn(phrase, self.text)

    def test_emc_disturbances_and_pass_fail_logic_are_explicit(self) -> None:
        for phrase in (
            "emisiones e inmunidad son problemas diferentes",
            "descarga electrostática", "transitorios eléctricos rápidos", "sobretensiones",
            "rf conducida", "rf radiada", "campos magnéticos",
            "cuantitativo, específico y observable",
            "durante y después",
        ):
            self.assertIn(phrase, self.text)
        self.assertIn("decir que un equipo es inmune porque no se reinicia", self.text)

    def test_guided_activity_is_scaffolded_reproducible_and_safe(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 10)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 20)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        for phrase in (
            "no conectes", "sintéticos", "fallo simulado", "emc", "criterios cuantitativos",
            "evidencia pendiente", "no se usa ninguna simulación",
        ):
            self.assertIn(phrase, text)

    def test_learning_scaffolds_are_specific_and_sufficient(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 45)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 20)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "seguridad básica", "desempeño esencial", "mopp", "moop", "clearance",
            "creepage", "tipo bf", "tipo cf", "emc", "emi", "esd", "verificación",
            "validación", "trazabilidad de requisitos",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_current_core_standards_are_present(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 15)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://webstore.iec.ch/en/publication/67497",
            "https://webstore.iec.ch/en/publication/67554",
            "https://webstore.iec.ch/en/publication/80393",
            "https://webstore.iec.ch/en/publication/80394",
            "https://www.iso.org/standard/72704.html",
            "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/electromagnetic-compatibility-emc-medical-devices",
            "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/detail.cfm?standard__identification_no=44029",
        ):
            self.assertIn(url, urls)

    def test_course_and_professional_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no constituyen revisión disciplinar externa",
            "ensayo iec 60601-1/60601-1-2",
            "certificación",
            "validación clínica",
            "valores de corriente, resistencia, tiempo, perturbación y criterios",
            "deliberadamente sintéticos",
            "u4 cubre transductores",
            "u5 actuación y control",
            "u6 integra ambos",
        ):
            self.assertIn(phrase, notice)
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituyen ensayo de conformidad", purpose)


if __name__ == "__main__":
    unittest.main()
