from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "imagenes-biomedicas-avanzadas-i" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "imagenes-biomedicas-avanzadas-i" / "unit-04.json"
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
        self.assertNotIn(r"cnr=\frac{|\mu_1-\mu_2|}{\sigma_n}", self.text)

    def test_objectives_cover_quantitative_nuclear_chain(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "random",
            "scatter",
            "atenuación",
            "osem",
            "tof",
            "psf",
            "suvbw",
            "patlak",
            "dicom",
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
        for phrase in ("correcciones", "reconstrucción", "suv", "dinámico", "metrología"):
            self.assertIn(phrase, headings)

    def test_corrections_section_separates_physical_effects(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "true",
            "random",
            "scatter",
            "atenuación",
            "normalización",
            "tiempo muerto",
            "cross-calibration",
            "semivida",
        ):
            self.assertIn(phrase, text)
        self.assertIn("visualmente aceptable no demuestra", text)

    def test_reconstruction_section_protects_resolution_and_partial_volume(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "osem",
            "time-of-flight",
            "point-spread function",
            "voxel de 2 mm no implica",
            "spill-out",
            "spill-in",
            "recovery coefficients",
            "overshoot",
        ):
            self.assertIn(phrase, text)

    def test_suv_section_requires_protocol_and_metadata(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "suvbw",
            "sul",
            "suvmax",
            "suvmean",
            "suvpeak",
            "uptake time",
            "dicom",
            "actividad residual",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no reemplaza", text)

    def test_dynamic_section_enforces_model_assumptions(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "curva tiempo-actividad",
            "input function",
            "k1",
            "k2",
            "k3",
            "patlak",
            "t*",
            "identificabilidad",
            "ground truth",
        ):
            self.assertIn(phrase, text)
        self.assertIn("bondad de ajuste", text)
        self.assertIn("no garantiza identificabilidad", text)

    def test_glossary_is_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 60)
        for term in (
            "pet",
            "spect",
            "random coincidence",
            "attenuation correction",
            "normalization",
            "dead time",
            "cross-calibration",
            "osem",
            "tof pet",
            "partial volume effect",
            "suv",
            "suvpeak",
            "dynamic pet",
            "tac",
            "input function",
            "patlak analysis",
            "identifiability",
            "phantom",
            "repeatability",
            "harmonisation",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)

    def test_guided_activity_requires_synthetic_quantitative_audit(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)
        joined = " ".join(activity["instructions"] + activity["problems"] + activity["checking_criteria"]).casefold()
        for phrase in (
            "datos y fantomas sintéticos",
            "cross-calibration",
            "recovery coefficient",
            "suvmax",
            "patlak",
            "ground truth",
            "no se prescribe actividad",
        ):
            self.assertIn(phrase, joined)

    def test_common_errors_block_high_impact_misinterpretations(self) -> None:
        errors = json.dumps(self.unit["common_errors"], ensure_ascii=False).casefold()
        for phrase in (
            "voxel con resolución espacial",
            "el suv",
            "uptake time",
            "r² alto",
            "repeatability con exactitud",
            "fantoma como prueba de validez clínica",
            "manejo de radiofármacos",
        ):
            self.assertIn(phrase, errors)

    def test_sources_assessment_connections_and_scope(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 18)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        sources = json.dumps(self.unit["sources"], ensure_ascii=False).casefold()
        for authority in ("nibib", "iaea", "eanm", "dicom", "nist", "qiba", "snmmi"):
            self.assertIn(authority, sources)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no administra ni manipula radiofármacos",
            "no opera pet/spect clínicos",
            "no prescribe actividad",
            "no calcula dosis terapéuticas" if "no calcula dosis terapéuticas" in self.text else "u5 continúa con registro",
            "u6 con control de calidad cuantitativo",
        ):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
