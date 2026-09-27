"""Independent checks of representative calculations in the rebuilt math course.

These are numerical/algebraic checks, not a claim of external academic review.
Only the Python standard library is needed.
"""
import cmath
from fractions import Fraction as F
import json
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / 'data/course_redevelopment/metodos-matematicos/units'


def lesson(number):
    return json.loads((UNITS / f'unit-{number:02}.json').read_text())


def midpoint(function, start, stop, steps=4096):
    h = (stop - start) / steps
    return h * sum(function(start + (i + .5) * h) for i in range(steps))


class MathematicalExamplesTests(unittest.TestCase):
    def test_stokes_line_integral_and_orientation(self):
        data = lesson(2)
        self.assertIn('8π', data['worked_examples'][1]['reasoning_steps'][2])
        # Parametrize the circle directly; compare with curl times disk area.
        def integrand(t):
            x, y = 2 * math.cos(t), 2 * math.sin(t)
            dx, dy = -2 * math.sin(t), 2 * math.cos(t)
            return -y * dx + x * dy
        result = midpoint(integrand, 0, 2 * math.pi)
        self.assertAlmostEqual(result, 2 * math.pi * 2**2, places=10)
        self.assertAlmostEqual(midpoint(integrand, 2 * math.pi, 0), -result, places=10)

    def test_gauss_flux_independent_surface_parametrization(self):
        self.assertIn('32π', ' '.join(lesson(2)['worked_examples'][2]['reasoning_steps']))
        # G dot n = R; dS = R² sin(theta) dtheta dphi.
        flux = 2 * math.pi * midpoint(lambda theta: 8 * math.sin(theta), 0, math.pi)
        volume_integral = 3 * (4 / 3) * math.pi * 2**3
        self.assertAlmostEqual(flux, volume_integral, delta=3e-6)

    def test_fourier_sawtooth_coefficients_by_quadrature(self):
        self.assertIn('2(−1)^(n+1)/n', ' '.join(lesson(3)['worked_examples'][0]['reasoning_steps']))
        for n in range(1, 6):
            calculated = midpoint(lambda t: t * math.sin(n*t), -math.pi, math.pi) / math.pi
            self.assertAlmostEqual(calculated, 2 * (-1)**(n+1) / n, delta=2e-6)

    def test_dft_inverse_and_energy(self):
        self.assertIn('x=[1,0,−1,0]', lesson(3)['worked_examples'][1]['scenario'])
        x = [1, 0, -1, 0]
        spectrum = [sum(v * cmath.exp(-2j * math.pi*k*n/4) for n, v in enumerate(x)) for k in range(4)]
        for actual, expected in zip(spectrum, [0, 2, 0, 2]):
            self.assertAlmostEqual(abs(actual - expected), 0, places=12)
        restored = [sum(v * cmath.exp(2j * math.pi*k*n/4) for k, v in enumerate(spectrum))/4 for n in range(4)]
        for actual, expected in zip(restored, x):
            self.assertAlmostEqual(abs(actual - expected), 0, places=12)
        self.assertAlmostEqual(sum(abs(v)**2 for v in spectrum)/4, sum(v*v for v in x))

    def test_compartment_solution_conserves_quantity_and_satisfies_rhs(self):
        self.assertIn('A=1+2e^(−3t)', ' '.join(lesson(4)['worked_examples'][1]['reasoning_steps']))
        for t in [0, .1, 1, 10]:
            e = math.exp(-3*t)
            a, b = 1+2*e, 2-2*e
            self.assertAlmostEqual(a+b, 3)
            self.assertAlmostEqual(-2*a+b, -6*e)
            self.assertAlmostEqual(2*a-b, 6*e)
            self.assertGreaterEqual(a, 0)
            self.assertGreaterEqual(b, 0)

    def test_euler_instability_positivity_and_convergence_are_distinct(self):
        self.assertIn('h=1.1', lesson(4)['worked_examples'][2]['scenario'])
        self.assertEqual(1-F(2)*F('1.1'), F('-1.2'))
        self.assertEqual(1-F(2)*F('.75'), F('-.5'))
        exact = math.exp(-2)
        errors = [abs((1-2/n)**n-exact) for n in [20, 40, 80]]
        self.assertGreater(errors[0], errors[1])
        self.assertGreater(errors[1], errors[2])
        self.assertTrue(1.9 < errors[1]/errors[2] < 2.1)

    def test_residue_integral_by_contour_quadrature(self):
        self.assertIn('2πi/3', ' '.join(lesson(5)['worked_examples'][1]['reasoning_steps']))
        for radius, expected in [(.5, 0j), (1.5, 2j*math.pi/3), (3, 0j)]:
            def integrand(t):
                z = radius * cmath.exp(1j*t)
                return 1j*z/((z-1)*(z+2))
            result = midpoint(integrand, 0, 2*math.pi)
            self.assertAlmostEqual(abs(result-expected), 0, places=10)

    def test_legendre_projection_exact_rational_integration(self):
        self.assertIn('c₂=2/3', ' '.join(lesson(5)['worked_examples'][2]['reasoning_steps']))
        # Integrate even monomials exactly over [-1,1].
        integral_x2_p2 = F(3,2)*F(2,5)-F(1,2)*F(2,3)
        self.assertEqual(F(5,2)*integral_x2_p2, F(2,3))
        norm_p2 = F(9,4)*F(2,5)-F(3,2)*F(2,3)+F(1,4)*2
        self.assertEqual(norm_p2, F(2,5))
        for x in [F(-1), F(0), F(1,3), F(1)]:
            self.assertEqual(F(1,3)+F(2,3)*(3*x*x-1)/2, x*x)

    def test_nonidentifiability_is_exact_and_not_a_sampling_artifact(self):
        self.assertIn('(2,3) y (1,6)', lesson(6)['worked_examples'][1]['scenario'])
        for gamma in [F(1,10), F(2), F(7)]:
            self.assertEqual((2*gamma)*(3/gamma), 6)
        for t in [0, .1, 1, 5]:
            self.assertEqual(2*3*math.exp(-t), 1*6*math.exp(-t))

    def test_uncertainty_covariance_and_finite_sensitivity(self):
        self.assertIn('0.045', ' '.join(lesson(6)['worked_examples'][2]['reasoning_steps']))
        du, dk = F(1,2), F(-3,2)
        variance = du**2*F('0.3')**2 + dk**2*F('0.1')**2
        self.assertEqual(variance, F('0.045'))
        self.assertEqual(variance+2*du*dk*F('.01'), F('.03'))
        self.assertEqual(variance+2*du*dk*F('.03'), 0)
        self.assertEqual(F(6)/F('2.4'), F('2.5'))


if __name__ == '__main__':
    unittest.main()
