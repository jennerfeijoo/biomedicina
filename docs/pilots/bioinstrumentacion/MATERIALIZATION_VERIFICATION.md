# Verificación de materialización — Bioinstrumentación

**Head materializado:** `9e467bfd53efcc5b9c30a2bcbe8cc3154f39930f`  
**Fecha:** 29 de julio de 2026

## Comprobaciones realizadas

- El generador carga `data/catalog_statuses.json` como autoridad editorial.
- Los cursos `pending` se renderizan como `placeholder` con la etiqueta “Contenido de respaldo · desarrollo académico pendiente”.
- Las unidades de cursos `pending` muestran el mismo estado y dejan de presentarse como lecciones desarrolladas.
- Los cursos incluidos en `developed` conservan la etiqueta “Unidades desarrolladas · revisión experta pendiente”.
- Bioinstrumentación permanece en la lista `pending`; este bloque no la promueve.
- La plantilla de unidad recibe `unit_status` y `unit_status_label` desde el generador.
- El workflow canónico `synchronize-generated-site.yml` fue restaurado después de la migración.
- El script de migración temporal fue eliminado del head materializado.

## Evidencia pública comprobada

- `ingenieria-biomedica/bioinstrumentacion/index.html`: `data-status="placeholder"`.
- `ingenieria-biomedica/bioinstrumentacion/unidades/unidad-01.html`: `data-status="placeholder"`.
- `ingenieria-biomedica/analisis-instrumental/index.html`: `data-status="generated"`.

## Interpretación

La materialización corrige la verdad editorial global, pero no mejora ni sustituye el contenido fallback. Las unidades históricas de Bioinstrumentación continúan disponibles únicamente como respaldo y deben reconstruirse después de aprobar la base piloto, resolver las brechas bibliográficas y organizar revisión especializada.

## Ciclo estable requerido

El commit de este documento inicia un ciclo de CI no creado por `github-actions[bot]`. El PR solo podrá salir de borrador cuando:

1. los workflows aplicables terminen en verde sobre un único SHA;
2. el generador resulte idempotente;
3. el diff final no contenga auxiliares temporales;
4. Bioinstrumentación permanezca `pending`;
5. no existan revisiones ni hilos humanos bloqueantes.
