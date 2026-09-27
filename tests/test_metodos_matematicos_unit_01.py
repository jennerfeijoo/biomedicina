"""Independent exact arithmetic checks of the worked teaching examples."""
from fractions import Fraction as F
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data/course_redevelopment/metodos-matematicos/units/unit-01.json'


class LinearAlgebraLessonTests(unittest.TestCase):
    def test_full_reconstruction_replaces_boilerplate(self):
        text = SOURCE.read_text()
        self.assertNotIn('Concepto de la unidad que debe definirse', text)
        data = json.loads(text)
        self.assertEqual(data['status'], 'review')
        self.assertEqual(len(data['worked_examples']), 3)
        self.assertIn('A^T', text)
        self.assertIn('datos numéricos son didácticos y sintéticos', text)

    def test_exact_solution_and_perturbation(self):
        a = ((2, 1), (1, 3))
        multiply = lambda x: [sum(v * y for v, y in zip(row, x)) for row in a]
        self.assertEqual(multiply([2, 1]), [5, 5])
        self.assertEqual(multiply([F('2.06'), F('0.98')]), [F('5.1'), 5])

    def test_least_squares_solution_residual_and_orthogonality(self):
        t, y = [0, 1, 2], [1, 2, 2]
        predictions = [F(7, 6) + F(1, 2) * time for time in t]
        residuals = [value - pred for value, pred in zip(y, predictions)]
        self.assertEqual(residuals, [F(-1, 6), F(1, 3), F(-1, 6)])
        self.assertEqual(sum(residuals), 0)
        self.assertEqual(sum(time * r for time, r in zip(t, residuals)), 0)
        self.assertEqual(sum(r * r for r in residuals), F(1, 6))

    def test_nearly_dependent_channels_hide_large_parameter_change(self):
        a = ((F(1), F(1)), (F(1), F('1.001')))
        multiply = lambda x: [sum(v * y for v, y in zip(row, x)) for row in a]
        original = multiply([1, 1])
        perturbed = multiply([0, 2])
        self.assertEqual(original, [F(2), F('2.001')])
        self.assertEqual(perturbed, [F(2), F('2.002')])
        self.assertEqual(perturbed[1] - original[1], F('0.001'))
