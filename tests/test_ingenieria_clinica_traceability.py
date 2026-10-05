"""Evidence boundaries for the clinical engineering documentary review."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_scientific_traceability import load_registry
from validate_scientific_traceability import validate_repository_registry


class ClinicalEngineeringEvidenceTests(unittest.TestCase):
    def test_documentary_contract_preserves_partial_support(self):
        payload = load_registry(ROOT / 'data/courses/ingenieria-clinica-gestion/claims.json')
        self.assertEqual(validate_repository_registry(payload), [])
        self.assertEqual({c['id'] for c in payload['claims'] if c['support'] == 'partial'},
                         {'ICG-U01-C002', 'ICG-U02-C004', 'ICG-U06-C002', 'ICG-U06-C004'})
        self.assertEqual(payload['review_state'], 'ai_review_provisional')
        self.assertTrue(all(c['reviewer_validation_id'] is None for c in payload['claims']))

    def test_denominator_does_not_remove_reporting_bias(self):
        # Identical exposure and true event counts can produce different reported rates.
        exposure, true_events = 1000, 20
        reported_rates = [true_events * capture / exposure for capture in (.25, .75)]
        self.assertNotEqual(*reported_rates)
        course = ROOT / 'data/courses/ingenieria-clinica-gestion'
        unit = json.loads((course / 'units/unit-05.json').read_text())
        paragraphs = '\n'.join(b['text'] for t in unit['topics'] for s in t['subtopics']
                               for b in s['blocks'] if b['type'] == 'paragraph')
        self.assertIn('necesario, pero no suficiente', paragraphs)
        self.assertIn('subregistro', paragraphs)
        self.assertIn('fda-maude-limitations', unit['source_ids'])

    def test_reporting_rate_can_fall_without_incidence_change(self):
        # Explicit counterexample: equal underlying incidence, changing capture.
        true_events = [20, 80]
        exposure = [2000, 8000]
        capture = [.2, .1]
        self.assertEqual(true_events[0]/exposure[0], true_events[1]/exposure[1])
        observed = [n*p/e for n, p, e in zip(true_events, capture, exposure)]
        self.assertEqual(observed, [.002, .001])
        unit = json.loads((ROOT / 'data/courses/ingenieria-clinica-gestion/units/unit-05.json').read_text())
        equation = unit['topics'][3]['blocks'][0]
        self.assertIn('n_{reportes}', equation['latex'])
        self.assertIn('No estima incidencia', equation['label'])
        self.assertIn('fracción reportada', unit['examples'][4]['interpretation'])
