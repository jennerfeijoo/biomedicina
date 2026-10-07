"""Protect documentary scope without upgrading scientific review status."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_scientific_traceability import load_registry
from validate_scientific_traceability import validate_repository_registry
COURSE = ROOT / 'data/courses/desarrollo-dispositivos-medicos'

class DeviceDevelopmentDocumentaryReviewTests(unittest.TestCase):
    def test_claims_match_sources_and_keep_provisional_review(self):
        payload = load_registry(COURSE / 'claims.json')
        self.assertEqual(validate_repository_registry(payload), [])
        for claim in payload['claims']:
            self.assertEqual(claim['review_state'], 'ai_review_provisional')
            self.assertIsNone(claim['reviewer_validation_id'])
            self.assertTrue(claim['support_note'])
            if claim['risk'] == 'high':
                self.assertEqual(claim['support'], 'direct')

    def test_jurisdiction_and_reproducibility_extensions_remain_visible(self):
        claims = {c['id']: c for c in load_registry(COURSE / 'claims.json')['claims']}
        self.assertTrue(claims['DDM-U06-C001']['text'].startswith('En Estados Unidos,'))
        self.assertIn('no clínicos de banco', claims['DDM-U05-C003']['text'])
        unit = json.loads((COURSE / 'units/unit-04.json').read_text())
        note = unit['topics'][0]['subtopics'][0]['blocks'][0]['text']
        self.assertIn('no elimina la identificación de versiones, la seguridad', note)
        self.assertIn('regla de reproducibilidad de este curso', note)
        self.assertEqual(claims['DDM-U04-C004']['support'], 'partial')
