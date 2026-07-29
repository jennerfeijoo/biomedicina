#!/usr/bin/env python3
import json
from pathlib import Path

path = Path('data/course_redevelopment/analisis-estadistico-multivariado/units/unit-02.json')
data = json.loads(path.read_text(encoding='utf-8'))
replacement = 'El objetivo de contracción determina la estructura estadística estimada.'
points = data['theory_sections'][3]['key_points']
if points[1] != replacement:
    points[1] = replacement
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    print('Punto clave corregido.')
else:
    print('Sin cambios pendientes.')
