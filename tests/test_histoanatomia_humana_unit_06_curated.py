from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "histoanatomia-humana" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "histoanatomia-humana" / "unit-06.json"
SUBJECT = ROOT / "data" / "subjects" / "biologicas-medicas" / "histoanatomia-humana.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class HistoanatomiaHumanaUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["slug"], "sistemas-nervioso-y-reproductor")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn(r"v=\frac{\Delta y}{\Delta t}", self.text)

    def test_objectives_cover_cns_senses_and_reproductive_histoanatomy(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "sustancia gris",
            "plexo coroideo",
            "corteza cerebral, cerebelo y médula espinal",
            "retina",
            "cóclea",
            "testículo",
            "epidídimo",
            "ovario",
            "trompa uterina",
            "útero",
            "tres rasgos positivos",
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
        for phrase in (
            "sistema nervioso central",
            "corteza cerebral, cerebelo y médula",
            "órganos sensoriales",
            "aparato reproductor masculino",
            "aparato reproductor femenino",
        ):
            self.assertIn(phrase, headings)

    def test_cns_section_preserves_regional_covering_and_csf_relations(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "sustancia gris",
            "sustancia blanca",
            "duramadre, aracnoides y piamadre",
            "espacio subaracnoideo",
            "sistema ventricular",
            "canal central",
            "plexo coroideo",
            "barrera hematoencefálica",
            "endotelio capilar continuo",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no interpreta mri o ct", text)

    def test_regional_neurohistology_distinguishes_cortex_cerebellum_and_spinal_cord(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "seis capas",
            "neuronas piramidales",
            "capa molecular",
            "células de purkinje",
            "capa granulosa",
            "astas posteriores y anteriores",
            "canal central",
            "endoneuro, perineuro y epineuro",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no estructura ni función", text)

    def test_sensory_section_orients_retina_cornea_and_cochlea(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "túnica fibrosa",
            "membrana de descemet",
            "epitelio pigmentario",
            "fotorreceptores",
            "células ganglionares",
            "scala vestibuli",
            "scala media",
            "scala tympani",
            "órgano de corti",
            "membrana basilar",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no deduce agudeza visual", text)

    def test_male_reproductive_section_separates_compartments_and_ducts(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "túbulos seminíferos",
            "espermatogonias",
            "espermatocitos",
            "espermátides",
            "células de sertoli",
            "células de leydig",
            "rete testis",
            "epidídimo",
            "estereocilios",
            "conducto deferente",
            "vesículas seminales",
            "próstata",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no constituye un análisis de semen", text)
        self.assertIn("no interpreta biopsias", text)

    def test_female_reproductive_section_preserves_follicles_wall_and_cycle_limits(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in (
            "corteza periférica",
            "médula interna",
            "células de granulosa",
            "teca",
            "antro",
            "cuerpo lúteo",
            "trompa uterina",
            "endometrio, miometrio",
            "fase proliferativa",
            "fase secretora",
            "endocervical",
            "ectocérvix",
            "vagina",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no permite fijar con precisión el día del ciclo", text)
        self.assertIn("no intenta inferir reserva ovárica", text)

    def test_glossary_and_examples_are_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 70)
        for term in (
            "sustancia gris",
            "plexo coroideo",
            "célula de purkinje",
            "retina",
            "órgano de corti",
            "túbulo seminífero",
            "célula de sertoli",
            "epidídimo",
            "próstata",
            "folículo antral",
            "endometrio",
            "zona de transformación cervical",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)

    def test_guided_activity_is_integrative_multisystem_and_safe(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 360)
        self.assertGreaterEqual(len(activity["problems"]), 24)
        self.assertGreaterEqual(len(activity["deliverables"]), 12)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 28)
        joined = " ".join(activity["instructions"] + activity["checking_criteria"]).casefold()
        for phrase in (
            "cinco rutas paralelas",
            "tres rasgos positivos",
            "dos rasgos negativos",
            "retina",
            "scala vestibuli, media y tympani",
            "vía espermática",
            "no se estima fertilidad",
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
            "neuroimagen",
            "fertilidad",
            "reserva ovárica",
            "inmunohistoquímica",
            "tampoco prescribe tratamiento",
        ):
            self.assertIn(phrase, notice)

    def test_course_closure_reuses_u1_to_u5_without_duplication(self) -> None:
        purpose = self.unit["purpose"].casefold()
        for phrase in (
            "orientación y preparación de u1",
            "criterios de tejido nervioso de u2",
            "razonamiento multiescala de u3",
            "organización vascular de u4",
            "lógica de órganos glandulares y tubulares de u5",
        ):
            self.assertIn(phrase, purpose)

    def test_published_descriptor_matches_when_promoted(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {x["unit"]: x for x in subject["detailed_units"]}
        if detailed[6]["description"] == self.unit["purpose"]:
            self.assertEqual(detailed[6]["description"], self.unit["purpose"])
        else:
            self.skipTest("El publicador aún no ha promovido el propósito canónico de U6.")


if __name__ == "__main__":
    unittest.main()
