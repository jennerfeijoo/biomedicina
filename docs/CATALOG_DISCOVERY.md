# Descubrimiento del catálogo

CitoNauta publica un catálogo global generado desde `data/citonauta_curriculum.json` y rutas interdisciplinarias definidas en `data/tracks.json`.

## Principios

- La búsqueda opera sobre título, descripción, conexión biomédica, área y rutas.
- Las rutas agrupan asignaturas por tipo de problema; no representan semestres, calendarios ni secuencias obligatorias.
- Una asignatura puede pertenecer a varias rutas.
- No se publica un filtro de dificultad hasta disponer de una definición reproducible, revisada y consistente entre disciplinas.
- Los catálogos de área y el catálogo global se regeneran desde la misma fuente de verdad.

## Rutas iniciales

1. Bioinformática y ómicas.
2. IA clínica y datos de salud.
3. Señales, neuroingeniería e interfaces.
4. Imágenes biomédicas y biofotónica.
5. Biomecánica, modelado y rehabilitación.
6. Biomateriales, tejidos y dispositivos.

## Validación

```bash
python scripts/generate_site.py --force
python scripts/validate_catalog.py
```

El validador comprueba la existencia de las 84 asignaturas, la integridad de las rutas, su carácter interdisciplinario y la sincronización de las tarjetas publicadas.
