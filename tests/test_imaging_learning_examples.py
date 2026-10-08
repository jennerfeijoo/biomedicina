import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class ImagingLearningExamplesTests(unittest.TestCase):
    def test_real_examples_have_guidance_and_reach_their_units(self):
        m=json.loads((ROOT/'data/courses/imagenes-biomedicas/media.json').read_text())
        examples=[x for x in m['items'] if x['status']=='complete']
        self.assertEqual(len(examples),3)
        self.assertEqual(m['coverage_status'],'partial')
        for item in examples:
            with self.subTest(image=item['id']):
                page=(ROOT/f"ingenieria-biomedica/imagenes-biomedicas/unidades/unidad-{item['unit_id'][-2:]}.html").read_text()
                self.assertIn(item['image_url'],page)
                self.assertIn(item['license_url'],page)
                self.assertEqual(len(item['guided_observation']),2)
                self.assertIn(item['guided_observation'][0]['question'],page)
        self.assertIn('falso color',examples[-1]['caption'])
        self.assertIn('PNG',examples[1]['caption'])
