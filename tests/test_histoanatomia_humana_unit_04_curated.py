from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "histoanatomia-humana" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "histoanatomia-humana" / "unit-04.json"
SUBJECT = ROOT / "data" / "subjects" / "biologicas-medicas" / "histoanatomia-humana.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class HistoanatomiaHumanaUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["slug"], "sistemas-cardiovascular-y-respiratorio")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn(r"v=\\frac{\\delta y}{\\delta t}", self.text)

    def test_objectives_cover_cardiorespiratory_multiscale_anatomy(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "circuitos pulmonar y sistémico",
            "epicardio, miocardio y endocardio",
            "arterias elásticas",
            "arterias musculares",
            "tráquea a bronquios y bronquiolos",
            "neumocitos tipo i y ii",
            "barrera alveolocapilar",
            "rasgos positivos y negativos",
        ):
            self.assertIn(phrase, objectives)

    def test_five_substantive_theory_sections(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        for section in sections:
            self.assertGreaterEqual(len(section["paragraphs"]), 6)
            self.assertGreaterEqual(len(section["key_points"]), 6)
            for point in section["key_points"]:
                self.assertGreaterEqual(len(point.split()), 5)
        headings = " ".join(x["heading"] for x in sections).casefold()
        for phrase in ("corazón y circuitos", "miocardio", "árbol vascular", "vías aéreas", "barrera alveolocapilar"):
            self.assertIn(phrase, headings)

    def test_heart_section_enforces_anatomical_direction_and_wall_layers(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "mediastino",
            "arteria y vena se definen por dirección respecto del corazón",
            "válvulas auriculoventriculares y semilunares",
            "esqueleto fibroso",
            "epicardio, miocardio y endocardio",
            "ventrículo izquierdo",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no utiliza espesor de pared para diagnosticar hipertrofia", text)

    def test_cardiomyocytes_conduction_and_coronary_context_are_present(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "cardiomiocito",
            "discos intercalares",
            "nodo sinoauricular",
            "fibras de purkinje",
            "subendocárdica",
            "arterias coronarias",
            "seno coronario",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no interpreta ecg", text)

    def test_vascular_tree_uses_wall_architecture_not_lumen_shape(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "íntima, media y adventicia",
            "arterias elásticas",
            "arterias musculares",
            "arteriolas",
            "capilares continuos",
            "fenestrados",
            "sinusoides",
            "vénulas",
        ):
            self.assertIn(phrase, text)
        self.assertIn("forma redonda o colapsada es orientativa pero no absoluta", text)

    def test_airway_transition_distinguishes_bronchus_bronchiole_and_terminal(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "epitelio respiratorio seudoestratificado cilíndrico ciliado",
            "células caliciformes",
            "cartílago hialino",
            "bronquios intrapulmonares",
            "placas discontinuas",
            "bronquiolos carecen de cartílago",
            "células club",
            "bronquiolo terminal",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no contiene alvéolos abiertos directamente a la luz", text)

    def test_alveolar_section_builds_the_air_blood_interface(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in (
            "bronquiolos respiratorios",
            "conductos alveolares",
            "septos interalveolares",
            "neumocitos tipo i",
            "neumocitos tipo ii",
            "surfactante",
            "macrófagos alveolares",
            "endotelio capilar",
            "pleura visceral",
            "pleura parietal",
        ):
            self.assertIn(phrase, text)
        self.assertIn("u5 pasará a sistemas digestivo, renal y endocrino", text)

    def test_glossary_and_examples_are_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 50)
        for term in (
            "epicardio", "miocardio", "endocardio", "cardiomiocito", "fibra de purkinje",
            "túnica íntima", "arteria elástica", "capilar", "zona conductora", "tráquea",
            "bronquiolo", "bronquiolo respiratorio", "neumocito tipo i", "neumocito tipo ii",
            "barrera alveolocapilar", "pleura visceral",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)

    def test_guided_activity_requires_two_traced_pathways_and_safe_boundaries(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 24)
        joined = " ".join(activity["instructions"] + activity["checking_criteria"]).casefold()
        for phrase in (
            "dos rutas paralelas: sangre y aire",
            "tres rasgos positivos",
            "alternativa plausible",
            "corazón → vaso → microcirculación",
            "tráquea → bronquio → bronquiolo → alvéolo",
            "no se formula diagnóstico",
        ):
            self.assertIn(phrase, joined)

    def test_sources_assessment_connections_and_editorial_boundary(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 18)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no constituye entrenamiento diagnóstico",
            "interpretación de ecg",
            "no establecen hipertrofia",
            "tampoco prescribe tratamiento",
            "material clínico",
        ):
            self.assertIn(phrase, notice)

    def test_u1_u2_u3_u4_u5_curricular_boundaries(self) -> None:
        purpose = self.unit["purpose"].casefold()
        self.assertIn("orientación de u1", purpose)
        self.assertIn("criterios tisulares de u2", purpose)
        self.assertIn("razonamiento multiescala de u3", purpose)
        self.assertIn("u5 pasará a sistemas digestivo, renal y endocrino", self.text)

    def test_published_descriptor_matches_canonical_purpose(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {x["unit"]: x for x in subject["detailed_units"]}
        self.assertEqual(detailed[4]["description"], self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()
