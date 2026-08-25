from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "imagenes-biomedicas-avanzadas-i" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "imagenes-biomedicas-avanzadas-i" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class ImagenesBiomedicasAvanzadasIUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["slug"], "ultrasonido-avanzado")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn(r"cnr=\frac{|\mu_1-\mu_2|}{\sigma_n}", self.text)

    def test_objectives_cover_full_advanced_ultrasound_chain(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "delay-and-sum",
            "apodización",
            "f-number",
            "plane-wave imaging",
            "coherent compounding",
            "doppler",
            "prf",
            "nyquist",
            "aliasing",
            "strain elastography",
            "shear-wave elastography",
            "dicom",
            "preload",
            "roi",
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
        for phrase in ("beamforming", "plane waves", "doppler", "elastografía", "dicom"):
            self.assertIn(phrase, headings)

    def test_beamforming_section_preserves_signal_chain_and_model_dependence(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "channel",
            "delay-and-sum",
            "f-number",
            "apodización",
            "sidelobes",
            "grating lobes",
            "velocidad del sonido",
            "ninguna imagen debe denominarse raw",
        ):
            self.assertIn(phrase, text)
        equations = " ".join(x["latex"] for x in self.unit["theory_sections"][0]["equations"])
        self.assertIn("\\tau_m", equations)
        self.assertIn("ct}{2}", equations)

    def test_ultrafast_section_enforces_temporal_spatial_tradeoff(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "plane-wave imaging",
            "coherent plane-wave compounding",
            "frame rate",
            "movimiento entre emisiones",
            "adaptive beamforming",
            "ground truth sintético",
            "fwhm",
            "task-specific",
        ):
            self.assertIn(phrase, text)
        self.assertIn("frame rate y image quality no pueden optimizarse de forma independiente", text)

    def test_doppler_section_enforces_projection_sampling_and_modality_distinctions(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "componente proyectada",
            "coseno del ángulo",
            "sample volume",
            "límite de nyquist",
            "aliasing",
            "spectral doppler",
            "color doppler",
            "power doppler",
            "wall filters",
            "volume flow",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no evidencia de que la sangre haya cambiado realmente de dirección", text)
        equations = " ".join(x["latex"] for x in self.unit["theory_sections"][2]["equations"])
        self.assertIn("f_D", equations)
        self.assertIn("PRF", equations)
        self.assertIn("\\bar{v}A", equations)

    def test_elastography_section_keeps_measurement_and_mechanical_model_separate(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "strain elastography",
            "shear-wave elastography",
            "m/s",
            "lineal",
            "homogéneo",
            "isotrópico",
            "incompresibilidad",
            "viscoelásticos",
            "anisotrópicos",
            "dispersivos",
            "preload",
            "qiba",
        ):
            self.assertIn(phrase, text)
        self.assertIn("m/s y kpa no son unidades intercambiables", text)
        equations = " ".join(x["latex"] for x in self.unit["theory_sections"][3]["equations"])
        self.assertIn("\\varepsilon", equations)
        self.assertIn("\\rho c_s^2", equations)

    def test_metrology_section_uses_calibrated_regions_and_non_operational_safety_scope(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in (
            "us region calibration module",
            "unidades físicas",
            "fantomas",
            "mechanical index",
            "thermal index",
            "alara",
            "no elige output levels",
            "u4 cambia de modalidad hacia imagen nuclear cuantitativa",
        ):
            self.assertIn(phrase, text)

    def test_glossary_is_disciplinary_and_sufficiently_deep(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 50)
        for term in (
            "channel data",
            "beamforming",
            "delay-and-sum",
            "f-number",
            "apodization",
            "plane-wave imaging",
            "coherent compounding",
            "doppler shift",
            "prf",
            "nyquist limit",
            "aliasing",
            "spectral doppler",
            "power doppler",
            "strain elastography",
            "shear-wave elastography",
            "shear-wave speed",
            "viscoelasticity",
            "anisotropy",
            "us region calibration",
            "mechanical index",
            "thermal index",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)

    def test_guided_activity_is_synthetic_quantitative_and_reproducible(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)
        joined = " ".join(activity["instructions"] + activity["problems"] + activity["checking_criteria"]).casefold()
        for phrase in (
            "channel data",
            "delay-and-sum",
            "f-number",
            "plane waves",
            "coherent compounding",
            "error angular",
            "aliasing",
            "wall filter",
            "volume flow",
            "strain",
            "shear-wave speed",
            "dicom-like",
            "ground truth",
        ):
            self.assertIn(phrase, joined)
        self.assertIn("no adquirir señales de personas, animales ni dispositivos clínicos", joined)

    def test_common_errors_protect_high_impact_misinterpretations(self) -> None:
        errors = json.dumps(self.unit["common_errors"], ensure_ascii=False).casefold()
        for phrase in (
            "imagen raw al b-mode exportado",
            "más ángulos de plane-wave compounding siempre son mejores",
            "doppler shift como velocidad directamente",
            "aliasing como cambio real de dirección",
            "power doppler informa dirección igual que color doppler",
            "calcular volume flow con peak velocity",
            "stiffness a cualquier mapa de strain",
            "convertir automáticamente shear-wave speed en kpa",
            "quality map de elastografía como ground truth",
            "inventar unidades físicas",
        ):
            self.assertIn(phrase, errors)

    def test_sources_assessment_connections_and_scope(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 18)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        sources = json.dumps(self.unit["sources"], ensure_ascii=False).casefold()
        for authority in ("nibib", "qiba", "dicom standards committee", "american institute of ultrasound in medicine", "food and drug administration"):
            self.assertIn(authority, sources)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no opera escáneres",
            "no expone personas o animales",
            "no selecciona potencia acústica",
            "no interpreta estudios clínicos",
            "no aplica cut-offs de elastografía",
            "u4 continúa con imagen nuclear cuantitativa",
        ):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
