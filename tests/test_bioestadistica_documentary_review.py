"""Guard the corrected claim/content contract and the repeated-measures caveat."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_scientific_traceability import load_registry
from validate_scientific_traceability import validate_repository_registry

COURSE = ROOT / 'data/courses/bioestadistica'


class BioestadisticaDocumentaryReviewTests(unittest.TestCase):
    def test_registered_claims_have_valid_sources_and_match_canonical_content(self):
        payload = load_registry(COURSE / 'claims.json')
        self.assertEqual(validate_repository_registry(payload, 'bioestadistica'), [])
        self.assertTrue(all(c['review_state'] == 'ai_review_provisional' for c in payload['claims']))

    def test_repeated_measurement_warning_does_not_assume_one_error_direction(self):
        text = '\n'.join(p.read_text() for p in (COURSE / 'units').glob('*.json'))
        self.assertNotIn('todas las visitas fueran independientes sobreestima información', text)
        self.assertNotIn('observaciones repetidas produce intervalos estrechos artificiales', text)
        self.assertIn('la dirección del error depende del contraste estimado', text)
        # Independent exact four-point check of the two error directions.
        from fractions import Fraction as F
        from itertools import product
        # U,V independent, symmetric +/-1; use X=U+V, Y=U for a rational example.
        pairs = [(u+v,u) for u,v in product((-1,1), repeat=2)]
        def variance(values):
            mean = sum(values, F(0))/len(values)
            return sum(((x-mean)**2 for x in values), F(0))/len(values)
        vx,vy = variance([x for x,y in pairs]), variance([y for x,y in pairs])
        self.assertGreater(variance([F(x+y,2) for x,y in pairs]), (vx+vy)/4)
        self.assertLess(variance([x-y for x,y in pairs]), vx+vy)
