"""Protect against the documented cross-topic citation regressions."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_scientific_traceability import load_registry
from validate_scientific_traceability import validate_repository_registry


class ElectronicsEvidenceTests(unittest.TestCase):
    def test_registered_claims_have_valid_localizers_and_literal_content(self):
        payload = load_registry(ROOT / 'data/courses/electronica/claims.json')
        self.assertEqual(validate_repository_registry(payload), [])
        self.assertNotEqual(payload['review_state'], 'human_review_validated')

    def test_mosfet_threshold_and_zener_claims_use_the_matching_device_family(self):
        payload = json.loads((ROOT / 'data/courses/electronica/claims.json').read_text())
        claims = {claim['id']: claim for claim in payload['claims']}
        self.assertEqual(claims['ELEC-U02-CL02']['source_id'], 'avoid-common-mistakes-when-selecting-and-designing-with-power-mosfets')
        self.assertEqual(claims['ELEC-U01-CL03']['source_id'], 'bzx84-series-voltage-regulator-diodes')
        self.assertEqual(claims['ELEC-U06-CL02']['source_id'], 'mt-097-dealing-with-high-speed-logic')
