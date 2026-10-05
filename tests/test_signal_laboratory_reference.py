"""Independent arithmetic and exhaustive small-event matching checks."""
import importlib.util
import itertools
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('signal_lab', ROOT / 'assets/labs/signal_laboratory.py')
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


class SignalLaboratoryReferenceTests(unittest.TestCase):
    def test_alias_and_units(self):
        result = lab.demonstration()
        self.assertLess(result['u1']['alias_max_abs_error'], 1e-10)
        self.assertEqual(result['u1']['calibrated_mV'], [0, 1, -1])
        self.assertAlmostEqual(result['u6']['power_scale'], 1e6)
        self.assertAlmostEqual(lab.rms([1, 3])**2, 2**2 + 1)

    def test_quality_union(self):
        self.assertEqual(lab.coverage(10, {0, 1, 2}, {2, 3}), .6)
        self.assertEqual(lab.coverage(10), 1)
        for size, excluded in [(0, set()), (2, {-1}), (2, {2}), (2, {.5})]:
            with self.assertRaises(ValueError):
                lab.coverage(size, excluded)

    def test_filter_interior_and_border(self):
        self.assertEqual(lab.moving_average_three([3]*5), [1, 2, 3, 3, 3])
        periodic = [math.cos(2*math.pi*n/3) for n in range(15)]
        self.assertTrue(all(abs(y) < 1e-12 for y in lab.moving_average_three(periodic)[2:]))

    def test_duplicate_detection_and_undefined_denominators(self):
        result = lab.match_events([100, 200, 300], [98, 102, 205, 450], 5)
        self.assertEqual((result['TP'], result['FP'], result['FN']), (2, 2, 1))
        self.assertIsNone(lab.match_events([], [], 0)['sensitivity'])
        self.assertIsNone(lab.match_events([1], [], 0)['positive_predictive_value'])
        self.assertEqual(lab.match_events([1], [2], 1)['TP'], 1)

    def test_matching_against_exhaustive_assignments(self):
        # Brute-force all unrestricted one-to-one associations for small ordered sets.
        # This oracle does not use the dynamic recurrence or assume noncrossing pairs.
        cases = [([0, 2, 4], [1, 2, 3], 1), ([1, 1], [1, 1, 2], 0),
                 ([0, 3], [2, 4], 2), ([1, 2], [0, 1], 1), ([], [1], 2)]
        for ref, pred, tol in cases:
            scores = [(0, 0)]
            for count in range(1, min(len(ref), len(pred))+1):
                for ri in itertools.combinations(range(len(ref)), count):
                    for pj in itertools.permutations(range(len(pred)), count):
                        errors = [abs(ref[a]-pred[b]) for a, b in zip(ri, pj)]
                        if all(e <= tol for e in errors):
                            scores.append((count, -sum(errors)))
            actual = lab.match_events(ref, pred, tol)
            self.assertEqual((actual['TP'], -sum(abs(e) for e in actual['signed_errors'])), max(scores))
            self.assertEqual(len({a for a, b in actual['pairs']}), actual['TP'])
            self.assertEqual(len({b for a, b in actual['pairs']}), actual['TP'])

    def test_invalid_inputs_are_not_silent_empty_results(self):
        for seq in ([], [float('nan')], [float('inf')]):
            with self.assertRaises(ValueError):
                lab.rms(seq)
        for ref, pred, tol in [([2, 1], [], 0), ([float('nan')], [], 0), ([], [], -1), ([], [], float('inf'))]:
            with self.assertRaises(ValueError):
                lab.match_events(ref, pred, tol)
        with self.assertRaises(ValueError):
            lab.moving_average_three([0, float('nan')])
