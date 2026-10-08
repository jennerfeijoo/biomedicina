"""Check scientific arithmetic and publication of original biomaterials figures."""
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
class BiomaterialsFigureTests(unittest.TestCase):
    def test_figures_reach_public_units_with_accessible_descriptions(self):
        registry=json.loads((ROOT/'data/courses/biomateriales/media.json').read_text())
        for i,item in enumerate(registry['items'],1):
            with self.subTest(unit=i):
                ET.parse(ROOT/item['asset_path'])
                public=(ROOT/f'ingenieria-biomedica/biomateriales/unidades/unidad-{i:02d}.html').read_text()
                self.assertIn(item['asset_path'],public)
                self.assertIn(item['alt_text'].replace('&','&amp;').replace('"','&quot;'),public)
                self.assertIn('Fuentes de apoyo:',public)
                self.assertEqual(item['status'],'complete')
    def test_geometry_normalization_and_synthetic_degradation(self):
        r=json.loads((ROOT/'assets/figures/biomateriales/calculation-record.json').read_text())
        strain=r['final_extension_mm']/r['initial_length_mm']
        self.assertAlmostEqual(strain,.01)
        for force,area in zip(r['final_forces_n'],r['areas_mm2']):
            self.assertAlmostEqual(force/area,r['young_modulus_mpa']*strain)
        for time,molar,mass in zip(r['degradation_time'],r['molar_fraction'],r['specimen_mass_fraction']):
            self.assertTrue(0<molar<=1 and 0<mass<=1)
            if 0<time<=4:
                self.assertLess(molar,1)
                self.assertEqual(mass,1)
