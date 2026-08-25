import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data/course_redevelopment/ingenieria-datos-biomedicos/units/unit-05.json'
MIRROR = ROOT / 'data/generated_units/ingenieria-datos-biomedicos/unit-05.json'
DESCRIPTOR = ROOT / 'data/subjects/ingenieria-biomedica/ingenieria-datos-biomedicos.json'
PUBLIC = ROOT / 'ingenieria-biomedica/ingenieria-datos-biomedicos/unidades/unidad-05.html'


class IngenieriaDatosBiomedicosUnit05Curated(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(SOURCE.read_text(encoding='utf-8'))
        cls.text = json.dumps(cls.data, ensure_ascii=False).lower()

    def test_identity_and_exact_mirror(self):
        self.assertEqual(self.data['subject_id'], 'ingenieria-datos-biomedicos')
        self.assertEqual(self.data['unit'], 5)
        self.assertEqual(self.data['slug'], 'orquestacion-y-observabilidad')
        self.assertEqual(self.data['title'], 'Orquestación y observabilidad')
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_generic_template_and_irrelevant_classifier_equation_are_removed(self):
        self.assertNotIn('concepto de la unidad que debe definirse mediante entidades observables', self.text)
        self.assertNotIn('ppv=', self.text)
        self.assertNotIn('valor predictivo positivo', self.text)
        self.assertNotIn('sensibilidad y especificidad', self.text)

    def test_orchestration_semantics_are_explicit(self):
        for concept in ['dag', 'task', 'dependency', 'scheduler', 'run_id', 'logical date', 'data interval', 'job']:
            self.assertIn(concept, self.text)
        self.assertIn('now()', self.text)
        self.assertIn('no causalidad biomédica', self.text)

    def test_retry_backfill_and_idempotency_are_distinguished(self):
        for concept in ['retry budget', 'transient failure', 'deterministic failure', 'backoff', 'jitter', 'idempotency', 'backfill', 'checkpoint', 'deduplication key']:
            self.assertIn(concept, self.text)
        self.assertIn('no debe reintentarse automáticamente', self.text)
        self.assertIn('replay puede duplicar efectos', self.text)

    def test_observability_signals_are_not_collapsed(self):
        for concept in ['structured log', 'metric', 'counter', 'gauge', 'histogram', 'trace', 'span', 'trace_id', 'correlation_id', 'opentelemetry']:
            self.assertIn(concept, self.text)
        self.assertIn('logs registran eventos', self.text)
        self.assertIn('silencio en logs', self.text)
        self.assertIn('no equivale automáticamente a mayor observabilidad', self.text)

    def test_sli_slo_alerting_and_golden_signals_are_explicit(self):
        for concept in ['sli', 'slo', 'error budget', 'latency', 'traffic', 'errors', 'saturation', 'alert fatigue', 'prometheus']:
            self.assertIn(concept, self.text)
        self.assertIn('alertas deben ser accionables', self.text)
        self.assertIn('síntoma observado y causa raíz', self.text)

    def test_incident_recovery_and_openlineage_are_explicit(self):
        for concept in ['runevent', 'start', 'running', 'complete', 'abort', 'fail', 'runbook', 'incident', 'root cause', 'recovery', 'postmortem']:
            self.assertIn(concept, self.text)
        self.assertIn('desaparición de la alerta no demuestra recuperación completa', self.text)
        self.assertIn('no como verdad clínica', self.text)

    def test_curricular_boundaries_and_safety_are_explicit(self):
        purpose = self.data['purpose'].lower()
        notice = self.data['editorial_notice'].lower()
        self.assertIn('u4', purpose)
        self.assertIn('u6', purpose)
        self.assertIn('quality gates', purpose)
        for concept in ['seudonimización', 'minimización', 'autorización', 'productos de datos']:
            self.assertIn(concept, purpose)
        self.assertNotIn('interoperabilidad', purpose)
        self.assertIn('no se conectan ehr', notice)
        self.assertIn('no declara que un run exitoso pruebe calidad', notice)
        self.assertIn('se reservan para u6', notice)
        self.assertIn('no constituyen garantías de producción', notice)

    def test_academic_depth(self):
        self.assertGreaterEqual(len(self.data['learning_objectives']), 6)
        self.assertGreaterEqual(len(self.data['theory_sections']), 5)
        for section in self.data['theory_sections']:
            self.assertGreaterEqual(len(section['paragraphs']), 6)
            self.assertGreaterEqual(len(section['key_points']), 6)
            for paragraph in section['paragraphs']:
                self.assertGreaterEqual(len(paragraph.split()), 20)
            for point in section['key_points']:
                self.assertGreaterEqual(len(point.split()), 4)
        self.assertGreaterEqual(len(self.data['glossary']), 50)
        self.assertGreaterEqual(len(self.data['worked_examples']), 5)
        self.assertGreaterEqual(len(self.data['common_errors']), 18)
        self.assertGreaterEqual(len(self.data['self_assessment']), 12)
        self.assertGreaterEqual(len(self.data['biomedical_connections']), 6)
        self.assertGreaterEqual(len(self.data['sources']), 14)

    def test_guided_activity_is_substantive_and_reproducible(self):
        activity = self.data['guided_activities'][0]
        self.assertGreaterEqual(activity['estimated_time_minutes'], 420)
        self.assertGreaterEqual(len(activity['problems']), 20)
        self.assertGreaterEqual(len(activity['deliverables']), 10)
        self.assertGreaterEqual(len(activity['checking_criteria']), 24)
        joined = ' '.join(activity['problems'] + activity['deliverables'] + activity['checking_criteria']).lower()
        for concept in ['data interval', 'retry budget', 'idempot', 'backfill', 'logs estructurad', 'trace_id', 'sli', 'slo', 'error budget', 'runevent', 'runbook', 'postmortem']:
            self.assertIn(concept, joined)

    def test_glossary_and_sources_cover_core_families(self):
        terms = {g['term'].lower() for g in self.data['glossary']}
        for term in ['dag', 'logical date', 'data interval', 'idempotency', 'backfill', 'opentelemetry', 'sli', 'slo', 'error budget', 'runevent']:
            self.assertIn(term, terms)
        source_text = ' '.join(s['title'] + ' ' + s['organization'] for s in self.data['sources']).lower()
        for family in ['airflow', 'opentelemetry', 'site reliability', 'prometheus', 'openlineage']:
            self.assertIn(family, source_text)
        self.assertTrue(all(s.get('accessed') == '2026-08-25' for s in self.data['sources']))

    def test_publication_matches_canonical_unit(self):
        self.assertTrue(DESCRIPTOR.exists())
        descriptor = json.loads(DESCRIPTOR.read_text(encoding='utf-8'))
        unit = next(item for item in descriptor['detailed_units'] if item['unit'] == 5)
        self.assertEqual(unit['title'], self.data['title'])
        self.assertEqual(unit['description'], self.data['purpose'])
        published_description = unit['description'].lower()
        for concept in ['seudonimización', 'minimización', 'autorización', 'productos de datos']:
            self.assertIn(concept, published_description)
        self.assertNotIn('interoperabilidad', published_description)

        self.assertTrue(PUBLIC.exists())
        public_text = PUBLIC.read_text(encoding='utf-8').lower()
        for marker in ['retry budget', 'data interval', 'idempot', 'opentelemetry', 'error budget', 'runevent']:
            self.assertIn(marker, public_text)


if __name__ == '__main__':
    unittest.main()
