"""Check independent calculations and publication of image foundations; not expert validation."""
import json
import math
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'data/generated_units/tratamiento-digital-imagenes'
class ImageFoundationsRevision(unittest.TestCase):
 def test_aliasing_counterexample(self):
  for n in range(11):
   self.assertAlmostEqual(math.cos(2*math.pi*7*n/10),math.cos(2*math.pi*3*n/10),places=12)
  # They do differ off the sampling grid: acquisition ambiguity, not identical signals.
  self.assertNotAlmostEqual(math.cos(2*math.pi*7*.025),math.cos(2*math.pi*3*.025),places=3)
 def test_quantizer_boundary_and_geometry(self):
  def quantize(x):return min(8,max(0,2*math.floor(x/2+.5)))
  self.assertEqual([quantize(x) for x in [-1,0,1,3,7,9]],[0,0,2,4,8,8])
  self.assertGreater(abs(quantize(12)-12),1)
  self.assertAlmostEqual(250*.4*.7,70)
  self.assertEqual(1000*.5*.5*2,500)
  self.assertEqual(800*.5*.5*3,600)
  self.assertEqual(512*512*4*2,2097152)
 def test_histogram_does_not_encode_neighborhoods(self):
  a=[[0,0],[1,1]];b=[[0,1],[1,0]]
  self.assertEqual(sorted(sum(a,[])),sorted(sum(b,[])))
  def horizontal_changes(m):return sum(row[0]!=row[1] for row in m)
  self.assertEqual(horizontal_changes(a),0);self.assertEqual(horizontal_changes(b),2)
 def test_affine_cnr_and_nonlinear_means(self):
  self.assertEqual(abs(50-30)/5,abs((4*50+10)-(4*30+10))/(4*5))
  self.assertAlmostEqual((math.sqrt(.04)+math.sqrt(.64))/2,.5)
  self.assertAlmostEqual(math.sqrt((.04+.64)/2),.58309518948453)
 def test_windows_and_equalization(self):
  def window(x,lo,hi):return min(1,max(0,(x-lo)/(hi-lo)))
  self.assertEqual([window(x,0,100) for x in [0,25,50,75,100]],[0,.25,.5,.75,1])
  self.assertEqual([window(x,25,75) for x in [0,25,50,75,100]],[0,0,.5,1,1])
  def equalize(counts):
   total=sum(counts);cum=0;lut=[];out=[0]*len(counts)
   for count in counts:
    cum+=count;lut.append(math.floor((len(counts)-1)*cum/total+.5))
   for count,j in zip(counts,lut):out[j]+=count
   return lut,out
  self.assertEqual(equalize([4,2,1,1]),([2,2,3,3],[0,0,6,2]))
  self.assertEqual(equalize([1,3,0,4]),([0,2,2,3],[1,0,3,4]))
 def test_source_and_published_content(self):
  for n in [1,2]:
   with self.subTest(unit=n):
    p=BASE/f'unit-{n:02}.json';u=json.loads(p.read_text())
    source=ROOT/f'data/course_redevelopment/tratamiento-digital-imagenes/units/unit-{n:02}.json'
    self.assertEqual(u,json.loads(source.read_text()))
    ids=[o['id'] for o in u['assessment_blueprint']['objectives']]
    for i in ids:self.assertEqual(sum(i in q['objective_ids'] for q in u['self_assessment']),4)
    self.assertEqual(sum(len(u[k]) for k in ['self_assessment','worked_examples','common_errors','glossary']),60)
    page=(ROOT/f'ingenieria-biomedica/tratamiento-digital-imagenes/unidades/unidad-{n:02}.html').read_text()
    self.assertIn('Solución.',page)
    for s in u['theory_sections']:
     for f in s.get('figures',[]):
      self.assertIn(f['asset_path'],page);svg=(ROOT/f['asset_path']).read_text()
      self.assertIn('<title>',svg);self.assertIn('<desc>',svg)
    for a in u['guided_activities']:
     self.assertTrue(a['checking_criteria'][0].startswith('Solución orientativa:'))
     self.assertIn(a['title'],page)
if __name__=='__main__':unittest.main()
