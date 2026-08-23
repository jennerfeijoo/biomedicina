#!/usr/bin/env python3
from pathlib import Path

path = Path("tests/test_academic_course_schema.py")
text = path.read_text(encoding="utf-8")
text = text.replace(
    'self.assertEqual(report.counts["claims"], 56)',
    'self.assertEqual(report.counts["claims"], 70)',
)
text = text.replace(
    'for unit_number in (1, 2, 3, 4):',
    'for unit_number in (1, 2, 3, 4, 5):',
)
text = text.replace(
    'if {"MLBIO-U02", "MLBIO-U03", "MLBIO-U04"}.intersection(entry["unit_ids"])',
    'if {"MLBIO-U02", "MLBIO-U03", "MLBIO-U04", "MLBIO-U05"}.intersection(entry["unit_ids"])',
)

marker = '''    def test_every_assessment_item_maps_to_a_unit_outcome(self) -> None:\n'''
new_test = '''    def test_renderer_includes_curated_machine_learning_unit_5(self) -> None:\n        unit = RENDERER.load_advanced_unit(\n            ROOT, "machine-learning-biomedico-validacion-clinica", 5\n        )\n        self.assertIsNotNone(unit)\n        assert unit is not None\n        self.assertEqual(unit["schema_version"], "canonical-1.0")\n        self.assertEqual(unit["unit"], 5)\n        self.assertEqual(unit["title"], "Validación externa, transportabilidad y actualización")\n        self.assertEqual(len(unit["self_assessment"]), 8)\n        self.assertEqual(len(unit["guided_activities"][0]["deliverables"]), 6)\n\n'''
if "test_renderer_includes_curated_machine_learning_unit_5" not in text:
    if marker not in text:
        raise RuntimeError("No se encontró el punto de inserción de la prueba de Unidad 5")
    text = text.replace(marker, new_test + marker, 1)

path.write_text(text, encoding="utf-8")
print("Regresiones de Machine Learning actualizadas para incluir la Unidad 5.")
