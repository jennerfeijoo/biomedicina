"""Independent numeric checks and publication checks for the revised course."""
import json
import math
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
COURSE='modelado-simulacion-biomedicina'

def unit(n):
    return json.loads((ROOT/f'data/generated_units/{COURSE}/unit-{n:02}.json').read_text())

def case(n,title):
    return next(c for c in unit(n)['worked_examples'] if c['title']==title)

class ModelingRevisionTests(unittest.TestCase):
    def test_mapped_questions_and_diagnostic_have_explanations(self):
        for n in range(1,7):
            d=unit(n)
            ids=[o['id'] for o in d['assessment_blueprint']['objectives']]
            self.assertEqual(len(ids),6)
            for key in ids:
                qs=[q for q in d['self_assessment'] if key in q['objective_ids']]
                self.assertEqual(len(qs),4)
                self.assertTrue(all(q['answer'] and q['reasoning'] for q in qs))
            self.assertNotIn('Concepto de la unidad que debe definirse',json.dumps(d,ensure_ascii=False))
            self.assertEqual(d['status'],'review')
        course=json.loads((ROOT/f'data/generated_courses/{COURSE}.json').read_text())
        self.assertTrue(all(q['question'] and q['answer'] for q in course['diagnostic_assessment']['questions']))
        self.assertNotIn('Curso completo',course['course_purpose'])

    def test_amount_volume_and_analytic_cases(self):
        # Differentiate A/V independently by a small perturbation of volume.
        h=1e-5
        derivative=((20/(4+h))-(20/(4-h)))/(2*h)
        self.assertAlmostEqual(derivative,-1.25,places=8)
        self.assertIn('−1,25',case(1,'Volumen creciente')['answer'])
        self.assertAlmostEqual(100*math.exp(-.2*5),36.7879,places=4)
        self.assertIn('36,7879',case(2,'Decaimiento exacto')['answer'])
        self.assertAlmostEqual(math.log(2)/.2,3.4657,places=4)
        self.assertAlmostEqual(50*(1-math.exp(-1)),31.6060,places=4)
        self.assertAlmostEqual(40*math.exp(-.3),29.6327,places=4)
        self.assertAlmostEqual(math.log(4)/.5,2.7726,places=4)

    def test_euler_convergence_and_physical_failure(self):
        def euler(h):
            a=1.0
            for _ in range(round(1/h)): a-=h*a
            return a
        self.assertEqual(euler(.25),.31640625)
        self.assertIn('0,31640625',case(2,'Refinamiento de Euler')['answer'])
        errors=[abs(euler(h)-math.exp(-1)) for h in [1/32,1/64,1/128]]
        self.assertTrue(1.9 < errors[0]/errors[1] < 2.1)
        self.assertTrue(1.9 < errors[1]/errors[2] < 2.1)
        trajectory=[10]
        for _ in range(4):trajectory.append(trajectory[-1]*(1-1.5))
        self.assertEqual(trajectory[1],-5)
        self.assertLess(abs(trajectory[-1]),abs(trajectory[0]))

    def test_markov_and_monte_carlo_arithmetic(self):
        p=[.8,.2];matrix=[[.8,.2],[.1,.9]]
        out=[sum(p[i]*matrix[i][j] for i in range(2)) for j in range(2)]
        self.assertAlmostEqual(out[0],.66);self.assertAlmostEqual(out[1],.34)
        self.assertIn('0,66',case(3,'Dos pasos de Markov')['answer'])
        self.assertAlmostEqual(1-math.exp(-1),.63212056,places=8)
        self.assertAlmostEqual(math.sqrt(.2*.8/200),.028284,places=6)
        self.assertEqual(6/math.sqrt(400),.3)

    def test_identifiability_and_finite_difference(self):
        for t in [0,1,5,10,100]:
            self.assertEqual(math.exp(-(2/10)*t),math.exp(-(4/20)*t))
        f=lambda k:100*math.exp(-k*5)
        h=1e-6
        deriv=(f(.2+h)-f(.2-h))/(2*h)
        self.assertAlmostEqual(deriv,-183.9397,places=4)
        self.assertIn('−183,9397',case(4,'Derivada analítica')['answer'])
        self.assertAlmostEqual(100*math.exp(-1.5),22.3130,places=4)
        self.assertAlmostEqual(100*math.exp(-.5),60.6531,places=4)

    def test_decision_and_validation_cases(self):
        losses=[[2,10],[5,4]];p=[.75,.25]
        expected=[sum(x*y for x,y in zip(row,p)) for row in losses]
        perfect=sum(min(row[j] for row in losses)*p[j] for j in range(2))
        self.assertEqual(expected,[4,4.75]);self.assertEqual(min(expected)-perfect,1.5)
        self.assertIn('1,5',case(6,'Información perfecta')['answer'])
        threshold=(5-2)/((10-2)-(4-5))
        self.assertAlmostEqual(threshold,1/3)
        regrets=[[row[j]-min(r[j] for r in losses) for j in range(2)] for row in losses]
        self.assertEqual(regrets,[[0,6],[3,0]])
        errors=[-2,0,2]
        self.assertAlmostEqual(math.sqrt(sum(e*e for e in errors)/3),1.6330,places=4)
        self.assertIn('1,6330',case(5,'Sesgo y magnitud')['answer'])
        self.assertAlmostEqual(math.sqrt((4/3)/4),.57735,places=5)

    def test_figures_and_solutions_reach_public_pages(self):
        for n in range(1,7):
            d=unit(n); figures=[f for s in d['theory_sections'] for f in s.get('figures',[])]
            self.assertEqual(len(figures),1)
            fig=figures[0];svg=ET.parse(ROOT/fig['asset_path']).getroot()
            self.assertTrue(svg.find('{http://www.w3.org/2000/svg}title').text)
            self.assertTrue(svg.find('{http://www.w3.org/2000/svg}desc').text)
            public=(ROOT/f'ingenieria-biomedica/{COURSE}/unidades/unidad-{n:02}.html').read_text()
            self.assertIn(fig['asset_path'],public)
            self.assertIn(fig['guided_observation'][0]['question'],public)
            self.assertIn(d['worked_examples'][0]['answer'],public)
            self.assertNotIn('Concepto de la unidad que debe definirse',public)
