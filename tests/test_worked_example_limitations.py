"""Caveats from both supported authoring shapes must reach the learner."""
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from advanced_unit_renderer import render_worked_examples


class WorkedExampleLimitationsTests(unittest.TestCase):
    def test_single_prose_caveat_is_preserved_and_escaped(self):
        output = render_worked_examples({'worked_examples': [
            {'title': 'Example', 'limitations': 'Only x < 5; <script> is text.'}]})
        self.assertIn('Limitaciones', output)
        self.assertIn('Only x &lt; 5; &lt;script&gt; is text.', output)
        self.assertNotIn('<script>', output)
        self.assertEqual(output.count('<li>'), 1)

    def test_list_and_empty_forms(self):
        output = render_worked_examples({'worked_examples': [
            {'limitations': ['First caveat', 'Second caveat']}]})
        self.assertIn('First caveat', output)
        self.assertIn('Second caveat', output)
        for empty in ('', '   ', [], None):
            self.assertNotIn('Limitaciones', render_worked_examples(
                {'worked_examples': [{'limitations': empty}]}))
