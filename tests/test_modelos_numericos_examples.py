"""Recompute course examples independently; these are not experimental validation."""
from fractions import Fraction as F
import json
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / 'data/course_redevelopment/modelos-numericos-biomedicina/units'


def lesson(n):
    return json.loads((UNITS / f'unit-{n:02}.json').read_text())


def solve(matrix, rhs):
    """Small exact elimination, independent of the lesson's closed forms."""
    a = [[F(x) for x in row] + [F(b)] for row, b in zip(matrix, rhs)]
    for k in range(len(a)):
        pivot = next(i for i in range(k, len(a)) if a[i][k])
        a[k], a[pivot] = a[pivot], a[k]
        divisor = a[k][k]
        a[k] = [x / divisor for x in a[k]]
        for i in range(len(a)):
            if i != k:
                factor = a[i][k]
                a[i] = [x - factor*y for x, y in zip(a[i], a[k])]
    return [row[-1] for row in a]


class NumericalModelsExamplesTests(unittest.TestCase):
    def test_chamber_equilibrium_transient_and_mass_balance(self):
        prose = json.dumps(lesson(1), ensure_ascii=False)
        self.assertIn('3,160603', prose)
        volume, flow, cin, loss = 2, .1, 10, .05
        decay = flow/volume + loss
        equilibrium = (flow/volume)*cin/decay
        self.assertAlmostEqual(equilibrium, 5)
        self.assertAlmostEqual(flow*cin, flow*equilibrium + loss*volume*equilibrium)
        self.assertAlmostEqual(equilibrium*(1-math.exp(-decay*10)), 3.1606027941427883)
        self.assertAlmostEqual(-math.log(.1)/decay, 23.025850929940457)

    def test_poisson_system_and_order_on_three_meshes(self):
        self.assertIn('0,43359375', json.dumps(lesson(2), ensure_ascii=False))
        errors = []
        for intervals in [2, 4, 8]:
            n = intervals - 1
            h = F(1, intervals)
            matrix = [[(2 if i == j else -1 if abs(i-j) == 1 else 0)/h**2
                       for j in range(n)] for i in range(n)]
            rhs = [12*(F(i+1)*h)**2 for i in range(n)]
            values = solve(matrix, rhs)
            for i, value in enumerate(values, 1):
                x = i*h
                self.assertEqual(value-(x-x**4), -h**2*x*(1-x))
            errors.append(abs(values[intervals//2-1]-F(7,16)))
        self.assertEqual(errors, [F(1,16), F(1,64), F(1,256)])
        self.assertEqual(errors[0]/errors[1], 4)

    def test_exact_node_does_not_make_piecewise_field_exact(self):
        self.assertIn('0,1875', json.dumps(lesson(2), ensure_ascii=False))
        interior = solve([[4]], [1])[0]
        self.assertEqual(interior, F(1,4))
        interpolated = interior/2
        exact = F(1,4)*(1-F(1,4))
        self.assertEqual(exact-interpolated, F(1,16))

    def test_shared_flux_conserves_mass_but_can_lose_positivity(self):
        self.assertIn('−0,5', json.dumps(lesson(3), ensure_ascii=False))
        initial = [F(0), F(1), F(0)]
        flux = [F(0)] + [-(b-a) for a, b in zip(initial, initial[1:])] + [F(0)]
        for dt, expected in [(F(1,4), [F(1,4), F(1,2), F(1,4)]),
                             (F(3,4), [F(3,4), F(-1,2), F(3,4)])]:
            updated = [c-dt*(flux[i+1]-flux[i]) for i,c in enumerate(initial)]
            self.assertEqual(updated, expected)
            self.assertEqual(sum(updated), sum(initial))
        self.assertLess(min(updated), 0)

    def test_combined_positivity_bound_is_stricter(self):
        self.assertIn('1/11', json.dumps(lesson(3), ensure_ascii=False))
        diffusion, speed, dx, reaction = F('.02'), F('.5'), F('.1'), F(2)
        rate = speed/dx+2*diffusion/dx**2+reaction
        self.assertEqual(1/rate, F(1,11))
        self.assertEqual(1-rate*F('.1'), F('-.1'))

    def test_implicit_mode_is_stable_but_not_exact(self):
        self.assertIn('0,1975308642', json.dumps(lesson(3), ensure_ascii=False))
        exact = math.exp(-2)
        explicit = (1-F(2)*F(1,4))**4
        implicit = (1/(1+F(2)*F(1,4)))**4
        self.assertEqual(explicit, F(1,16))
        self.assertEqual(implicit, F(16,81))
        self.assertGreater(abs(F(1,3)-exact), abs(implicit-exact))

    def test_reaction_exchange_must_use_same_transfer(self):
        self.assertIn('0,84', json.dumps(lesson(3), ensure_ascii=False))
        old_a, k, dt = F(1), F('.4'), F(1)
        transfer = k*old_a*dt
        new_a, new_b = old_a-transfer, transfer
        self.assertEqual(new_a+new_b, 1)
        self.assertEqual(new_a+k*new_a*dt, F('.84'))

    def test_bar_assembly_reactions_and_energy(self):
        self.assertIn('0,0375', json.dumps(lesson(4), ensure_ascii=False))
        k1, k2 = F(100)*2/10, F(200)*2/10
        u1, u2 = solve([[k1+k2,-k2],[-k2,k2]], [0,1])
        self.assertEqual((u1,u2), (F('.05'),F('.075')))
        self.assertEqual(-k1*u1, -1)
        self.assertEqual(k1*u1,k2*(u2-u1))
        strain_energy = (k1*u1*u1+k2*(u2-u1)**2)/2
        self.assertEqual(strain_energy,u2/2)
        self.assertEqual(strain_energy,F('.0375'))

    def test_lateral_constraint_changes_stress(self):
        self.assertIn('1,34615385', json.dumps(lesson(4), ensure_ascii=False))
        young, nu, strain = F(100), F('.3'), F('.01')
        mu = young/(2*(1+nu))
        lam = young*nu/((1+nu)*(1-2*nu))
        self.assertEqual((lam+2*mu)*strain,F(35,26))
        self.assertEqual(lam*strain,F(15,26))
        self.assertEqual(young*strain,1)

    def test_least_squares_normal_equations_and_residuals(self):
        self.assertIn('1/12', json.dumps(lesson(5), ensure_ascii=False))
        x, y = [F(0),F(1),F(2)], [F(1),F(2),F(4)]
        a,b = solve([[len(x),sum(x)],[sum(x),sum(t*t for t in x)]],
                    [sum(y),sum(t*v for t,v in zip(x,y))])
        residuals = [v-a-b*t for t,v in zip(x,y)]
        self.assertEqual((a,b),(F(5,6),F(3,2)))
        self.assertEqual(sum(residuals),0)
        self.assertEqual(sum(t*r for t,r in zip(x,residuals)),0)
        self.assertEqual(sum(r*r for r in residuals),F(1,6))

    def test_parameter_symmetry_and_covariance_effect(self):
        self.assertIn('Var(D)=4+4−2·3=2', json.dumps(lesson(5), ensure_ascii=False))
        for multiplier in [F(1,5),F(2),F(9)]:
            self.assertEqual((2*multiplier)*(3/multiplier),6)
        covariance = [[F(4),F(3)],[F(3),F(4)]]
        for grad, expected in [([1,1],14),([1,-1],2),([1,2],32),([1,-2],8)]:
            variance = sum(grad[i]*covariance[i][j]*grad[j] for i in range(2) for j in range(2))
            self.assertEqual(variance,expected)

    def test_manufactured_source_by_finite_differentiation(self):
        self.assertIn('8,869604401', json.dumps(lesson(6), ensure_ascii=False))
        def u(x,t):
            return math.exp(-t)*math.sin(math.pi*x)
        h = 1e-4
        for x,t,d in [(.5,.2,1),(.25,.7,.5),(.8,.1,2)]:
            ut = (u(x,t+h)-u(x,t-h))/(2*h)
            uxx = (u(x+h,t)-2*u(x,t)+u(x-h,t))/h**2
            source = (d*math.pi**2-1)*u(x,t)
            self.assertAlmostEqual(ut-d*uxx,source,delta=2e-6)

    def test_richardson_and_validation_difference(self):
        self.assertIn('1,109400392', json.dumps(lesson(6), ensure_ascii=False))
        coarse,medium,fine = F('1.08'),F('1.02'),F('1.005')
        self.assertEqual((coarse-medium)/(medium-fine),4)
        self.assertEqual(fine+(fine-medium)/3,1)
        combined = math.sqrt(.1**2+.15**2)
        self.assertAlmostEqual(.2/combined,1.1094003924504583)
        self.assertAlmostEqual(.1**2+.15**2-2*.005,.15**2)


if __name__ == '__main__':
    unittest.main()
