from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "fisiologia-sistemas" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "fisiologia-sistemas" / "unit-05.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class FisiologiaSistemasUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["subject_id"], "fisiologia-sistemas")
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["slug"], "inflamacion-e-inmunidad-sistemica")
        self.assertEqual(self.unit["title"], "Inflamación e inmunidad sistémica")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("v=\\frac{\\delta y}{\\delta t}", self.text)

    def test_learning_objectives_are_specific_and_systemic(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "pamp, damp",
            "reclutamiento de neutrófilos y monocitos",
            "respuesta de fase aguda",
            "fiebre de hipertermia",
            "resolución inflamatoria",
            "infección, lesión estéril",
        ):
            self.assertIn(phrase, objectives)

    def test_theory_has_five_substantive_sections(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        for section in sections:
            self.assertGreaterEqual(len(section["paragraphs"]), 6)
            self.assertGreaterEqual(len(section["key_points"]), 6)
        headings = " ".join(section["heading"] for section in sections).casefold()
        for phrase in ("pamp", "endotelio", "fiebre", "resolución activa", "razonamiento sistémico"):
            self.assertIn(phrase, headings)

    def test_dynamic_models_separate_state_from_hidden_flows(self) -> None:
        equations = " ".join(
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        )
        for token in ("P_M", "k_{cl}", "R_N", "C_N", "AUC_M"):
            self.assertIn(token, equations)
        for phrase in (
            "una concentración plasmática no mide directamente producción tisular",
            "carga leucocitaria depende de entrada y retirada",
            "auc resume exposición temporal, no identifica fuente ni causa",
        ):
            self.assertIn(phrase, self.text)

    def test_infection_fever_and_biomarkers_are_not_diagnostic_shortcuts(self) -> None:
        errors = json.dumps(self.unit["common_errors"], ensure_ascii=False).casefold()
        for phrase in (
            "inflamación significa infección",
            "fiebre demuestra infección",
            "confundir fiebre con hipertermia",
            "crp elevada como prueba específica de infección bacteriana",
            "concentración de il-6 como medida directa de producción tisular",
            "respuesta sistémica sintética en diagnóstico de sepsis",
        ):
            self.assertIn(phrase, errors)

    def test_resolution_is_active_and_not_merely_anti_inflammatory(self) -> None:
        section = next(s for s in self.unit["theory_sections"] if "Resolución activa" in s["heading"])
        text = json.dumps(section, ensure_ascii=False).casefold()
        for phrase in (
            "eferocitosis",
            "mediadores especializados pro-resolutivos",
            "antiinflamación y pro-resolución no son sinónimos",
            "hemostasia, inflamación, proliferación y remodelado",
        ):
            self.assertIn(phrase, text)

    def test_glossary_is_disciplinary(self) -> None:
        glossary = {item["term"].casefold(): item["definition"].casefold() for item in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 55)
        for term in (
            "pamp", "damp", "prr", "inflamasoma", "quimiocina", "complemento",
            "rodamiento leucocitario", "transmigración", "fiebre", "hipertermia",
            "respuesta de fase aguda", "eferocitosis", "mediador pro-resolutivo",
            "tejido de granulación", "remodelado", "no identificabilidad",
        ):
            self.assertIn(term, glossary)

    def test_activity_is_integrative_and_reproducible(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["instructions"]), 10)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 20)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        for phrase in (
            "infección simulada con pamp",
            "lesión estéril con damp",
            "fiebre versus hipertermia",
            "eferocitosis",
            "respuesta autolimitada versus persistente",
            "no se utilizan criterios de sepsis",
        ):
            self.assertIn(phrase, text)

    def test_assessment_and_connections_are_complete(self) -> None:
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        for item in self.unit["self_assessment"]:
            for key in ("question", "answer", "reasoning", "common_error"):
                self.assertTrue(item[key].strip())
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)

    def test_sources_are_verified_and_sufficient(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 15)
        self.assertTrue(all(source["verification_status"] == "verified_directly" for source in sources))
        joined = " ".join(source["organization"] for source in sources).casefold()
        for name in ("openstax", "ncbi", "pmc"):
            self.assertIn(name, joined)

    def test_course_and_clinical_boundaries_are_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "perfiles y perturbaciones exclusivamente sintéticos",
            "no constituye diagnóstico de infección, sepsis",
            "no interpreta crp",
            "no indica antibióticos",
            "asignatura específica de inmunología",
            "u6 desarrollará modelado multiescala",
        ):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
