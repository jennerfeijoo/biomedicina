from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "imagenes-biomedicas-avanzadas-i" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "imagenes-biomedicas-avanzadas-i" / "unit-04.json"
SUBJECT = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "imagenes-biomedicas-avanzadas-i.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ImagenesBiomedicasAvanzadasIUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["slug"], "imagen-nuclear-cuantitativa")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn(r"cnr=\\frac{|\\mu_1-\\mu_2|}{\\sigma_n}", self.text)

    def test_objectives_cover_quantitative_nuclear_chain(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in ("pet/spect", "atenuación", "randoms", "tiempo muerto", "osem", "actividad-concentración", "suv", "patlak", "funciones de entrada"):
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
        for phrase in ("actividad-concentración", "reconstrucción", "suv", "cinética", "validación"):
            self.assertIn(phrase, headings)

    def test_corrections_section_separates_modalities_and_time_reference(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in ("random coincidences", "attenuation correction", "scatter correction", "normalization", "dead-time correction", "decay correction", "tiempo de referencia", "dicom"):
            self.assertIn(phrase, text)
        equations = " ".join(x["latex"] for x in self.unit["theory_sections"][0]["equations"])
        self.assertIn("T_{1/2}", equations)

    def test_reconstruction_section_teaches_recovery_not_visual_sharpness(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in ("osem", "time-of-flight", "psf modelling", "collimator-detector response", "partial-volume effect", "recovery coefficient", "ground truth"):
            self.assertIn(phrase, text)
        self.assertIn("ningún único cnr", text)

    def test_suv_section_requires_net_activity_and_protocol_context(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in ("suvbw", "lean body mass", "actividad neta", "residuo postinyección", "uptake time", "suvmax", "suvmean", "suvpeak", "qiba"):
            self.assertIn(phrase, text)
        equations = " ".join(x["latex"] for x in self.unit["theory_sections"][2]["equations"])
        self.assertIn("SUV_{BW}", equations)
        self.assertIn("A_{net}", equations)

    def test_kinetic_section_separates_tac_input_function_and_model(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in ("curvas tiempo-actividad", "input function", "k1", "k2", "patlak", "logan", "identificabilidad", "parametric imaging", "buen ajuste matemático no demuestra"):
            self.assertIn(phrase, text)
        equations = " ".join(x["latex"] for x in self.unit["theory_sections"][3]["equations"])
        self.assertIn("K_1", equations)
        self.assertIn("K_i", equations)

    def test_glossary_is_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 55)
        for term in ("actividad-concentración", "random coincidence", "osem", "time-of-flight", "partial-volume effect", "recovery coefficient", "suv", "suvbw", "sul", "uptake time", "input function", "patlak plot", "logan plot", "parametric image", "qiba", "phantom"):
            self.assertIn(term, glossary)

    def test_guided_activity_requires_synthetic_quantitative_validation(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)
        joined = " ".join(activity["instructions"] + activity["problems"] + activity["checking_criteria"]).casefold()
        for phrase in ("datos identificables", "random coincidences", "recovery coefficient", "suvbw", "patlak", "input function", "dicom", "no se recomienda actividad"):
            self.assertIn(phrase, joined)

    def test_common_errors_protect_high_impact_misinterpretations(self) -> None:
        errors = json.dumps(self.unit["common_errors"], ensure_ascii=False).casefold()
        for phrase in ("cuentas reconstruidas como bq/ml", "random coincidences con scatter", "actividad administrada neta sin considerar residuo", "osem más iteraciones", "suv como una propiedad intrínseca", "patlak desde el primer frame", "input function como ground truth", "generalizar desempeño de fantoma", "armonización con certificación clínica"):
            self.assertIn(phrase, errors)

    def test_sources_assessment_connections_and_scope(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 18)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        sources = json.dumps(self.unit["sources"], ensure_ascii=False).casefold()
        for authority in ("international atomic energy agency", "dicom standards committee", "quantitative imaging biomarkers alliance", "european association of nuclear medicine", "snmmi"):
            self.assertIn(authority, sources)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in ("no administra radiotrazadores", "no selecciona actividad para pacientes", "no opera pet/spect", "no interpreta estudios clínicos", "u5 continúa con registro y fusión", "u6 queda reservada"):
            self.assertIn(phrase, notice)

    def test_published_descriptor_matches_canonical_purpose(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        published = next(x for x in subject["detailed_units"] if x["unit"] == 4)
        self.assertEqual(published["description"], self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()
