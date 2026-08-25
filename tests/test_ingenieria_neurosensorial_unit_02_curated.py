from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "ingenieria-neurosensorial" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "ingenieria-neurosensorial" / "unit-02.json"
SUBJECT = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "ingenieria-neurosensorial.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class IngenieriaNeurosensorialUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["slug"], "registro-neural")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn(r"\mathrm{snr}_{db}=10\log_{10}", self.text)

    def test_objectives_cover_measurement_reference_sampling_artifacts_and_erp(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "no debe interpretarse como registro directo de potenciales de acción individuales",
            "electrodo, canal, referencia, tierra/common-mode y montaje",
            "rechazo de modo común",
            "filtrado anti-aliasing",
            "actividad ocular, muscular",
            "eventos temporizados",
            "eeg-bids",
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
        for phrase in ("qué mide un eeg", "electrodos", "archivo digital", "ruido y artefactos", "potenciales evocados"):
            self.assertIn(phrase, headings)

    def test_eeg_is_differential_population_measurement(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "no es un contador directo de potenciales de acción",
            "conducción de volumen",
            "todo canal eeg es una diferencia de potencial",
            "no existe un electrodo de referencia físicamente 'cero'",
            "electrodo y canal tampoco son sinónimos",
            "10-20 y 10-10",
        ):
            self.assertIn(phrase, text)

    def test_reference_ground_and_interface_are_not_conflated(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        self.assertIn("referencia y electrodo de tierra o common-mode cumplen funciones diferentes", text)
        self.assertIn("no debe equipararse automáticamente con tierra de protección", text)
        self.assertIn("rereferenciar es una transformación matemática", text)
        self.assertIn("un valor bajo de impedancia no demuestra por sí solo buena calidad de señal", text)
        self.assertIn("cmrr nominal alto no convierte automáticamente", text)

    def test_sampling_aliasing_and_filtering_are_physically_ordered(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        self.assertIn("filtrado anti-aliasing debe ocurrir antes de la conversión analógico-digital", text)
        self.assertIn("aumentar la frecuencia de muestreo después de adquirir los datos no repara aliasing", text)
        self.assertIn("filtros digitales", text)
        self.assertIn("cambiar amplitud, latencia o forma de ondas", text)
        self.assertIn("bits no equivale directamente a resolución fisiológica útil", text)

    def test_artifact_section_requires_mechanism_and_reversible_processing(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "actividad ocular",
            "actividad muscular",
            "movimiento de cables/electrodos",
            "ica no etiqueta por sí sola la fisiología",
            "conservar señal cruda",
            "una señal residual no se vuelve neural",
        ):
            self.assertIn(phrase, text)

    def test_erp_section_preserves_event_timing_and_pipeline_dependence(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in (
            "trigger incorrecto desplaza o dispersa la respuesta",
            "baseline",
            "promediado de ensayos",
            "más ensayos no arreglan sistemáticamente un sesgo de trigger",
            "amplitud y latencia de un componente erp dependen",
            "eeg-bids",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no garantiza calidad fisiológica ni validez del experimento", text)

    def test_glossary_and_examples_are_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 50)
        for term in (
            "eeg", "referencia eeg", "rereferencia", "ground/common-mode", "cmrr",
            "frecuencia de nyquist", "aliasing", "filtro anti-aliasing", "ica", "eog",
            "erp", "trigger", "época", "baseline", "jitter temporal", "eeg-bids",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)

    def test_guided_activity_requires_reproducible_raw_to_erp_audit(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 360)
        self.assertGreaterEqual(len(activity["problems"]), 24)
        self.assertGreaterEqual(len(activity["deliverables"]), 12)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)
        joined = " ".join(activity["instructions"] + activity["checking_criteria"]).casefold()
        for phrase in (
            "preservar el archivo crudo",
            "comparar al menos dos referencias",
            "no se intenta reparar aliasing mediante upsampling posterior",
            "ica no se usa como clasificador fisiológico automático",
            "u3 queda reservada a estimulación",
            "no se interpreta el dataset como diagnóstico",
        ):
            self.assertIn(phrase, joined)

    def test_common_errors_block_high_impact_misconceptions(self) -> None:
        errors = json.dumps(self.unit["common_errors"], ensure_ascii=False).casefold()
        for phrase in (
            "registra directamente potenciales de acción individuales",
            "referencia universalmente neutro",
            "nyquist sin filtro anti-aliasing",
            "reparar aliasing con upsampling",
            "filtrar hasta que la señal se vea limpia",
            "ica es una descomposición estadística",
            "promediar elimina todo ruido",
            "archivo eeg-bids válido con eeg de alta calidad",
        ):
            self.assertIn(phrase, errors)

    def test_sources_assessment_connections_and_editorial_boundary(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 16)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no instruye adquisición en personas",
            "no interpreta eeg o potenciales evocados con fines diagnósticos",
            "no demuestra seguridad eléctrica",
            "u3 aborda estimulación",
            "u4 prótesis sensoriales",
        ):
            self.assertIn(phrase, notice)

    def test_curricular_boundaries_are_explicit(self) -> None:
        self.assertIn("u1 aporta fisiología sensorial", self.text)
        self.assertIn("u2 se limita a registro y procesamiento", self.text)
        self.assertIn("u3 aborda estimulación y seguridad de intervención", self.text)
        self.assertIn("u4 prótesis sensoriales", self.text)
        self.assertIn("clasificación y adaptación se desarrollan en u5", self.text)

    def test_published_descriptor_matches_canonical_purpose(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {x["unit"]: x for x in subject["detailed_units"]}
        self.assertEqual(detailed[2]["description"], self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()
