"""Regression checks for force-reference and documentary corrections."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_scientific_traceability import load_registry
from validate_scientific_traceability import validate_repository_registry


class LaboratoryBiomechanicsEvidenceTests(unittest.TestCase):
    def test_claim_contract_and_partial_evidence_remain_explicit(self):
        payload = load_registry(ROOT / 'data/courses/laboratorio-biomecanica/claims.json')
        self.assertEqual(validate_repository_registry(payload), [])
        self.assertEqual(payload['review_state'], 'ai_review_provisional')
        claims = {c['id']: c for c in payload['claims']}
        self.assertEqual(claims['LABBIO-U01-C002']['support'], 'partial')
        self.assertIsNone(claims['LABBIO-U01-C002']['reviewer_validation_id'])

    def test_translation_and_cop_derivation_reach_published_lesson(self):
        unit = json.loads((ROOT / 'data/courses/laboratorio-biomecanica/units/unit-03.json').read_text())
        paragraphs = [b['text'] for t in unit['topics'] for s in t['subtopics'] for b in s['blocks'] if b['type'] == 'paragraph']
        lesson = '\n'.join(paragraphs)
        self.assertIn('las componentes de la fuerza no cambian', lesson)
        self.assertIn('MP=MO−rOP×F', lesson)
        self.assertIn('Si el momento libre solo tiene componente normal', lesson)
        # Independent cross product of the worked example, with the stated O→P direction.
        r, force = (0, 1, 0), (0, 0, 100)
        cross = (r[1]*force[2]-r[2]*force[1], r[2]*force[0]-r[0]*force[2], r[0]*force[1]-r[1]*force[0])
        self.assertEqual(tuple(m-c for m, c in zip((100, 0, 0), cross)), (0, 0, 0))
        # Nonzero tangential forces and a free normal moment leave this surface CoP unchanged.
        x, y, fx, fy, fz, free = .03, -.02, 15, -10, 100, 7
        moment = (y*fz, -x*fz, x*fy-y*fx+free)
        self.assertAlmostEqual(-moment[1]/fz, x)
        self.assertAlmostEqual(moment[0]/fz, y)

    def test_filter_reference_matches_the_taught_operation(self):
        payload = json.loads((ROOT / 'data/courses/laboratorio-biomecanica/claims.json').read_text())
        claim = next(c for c in payload['claims'] if c['id'] == 'LABBIO-U04-C004')
        self.assertEqual(claim['source_id'], 'scipy-butter-response')
        response = 1 / complex(1, 1)  # First-order Butterworth at omega=omega_c.
        self.assertAlmostEqual(100*abs(response), 70.71067811865476)
        self.assertAlmostEqual(abs(response*response.conjugate()), .5)
