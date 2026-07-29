# Verificación de materialización — Bioinstrumentación

**Head permanente verificado:** `71fe915c16aca7ed6ad2a2e187a6ef20d9b2d0f7`  
**Fecha:** 29 de julio de 2026

## Comprobaciones realizadas

- El generador carga `data/catalog_statuses.json` como autoridad editorial.
- Los cursos `pending` se renderizan como `placeholder` con la etiqueta “Contenido de respaldo · desarrollo académico pendiente”.
- Las unidades de cursos `pending` muestran el mismo estado y dejan de presentarse como lecciones desarrolladas.
- Los cursos incluidos en `developed` conservan la etiqueta “Unidades desarrolladas · revisión experta pendiente”.
- Bioinstrumentación permanece en la lista `pending`; este bloque no la promueve.
- La plantilla de unidad recibe `unit_status` y `unit_status_label` desde el generador.
- El validador curricular exige que el estado público de cada asignatura coincida con `data/catalog_statuses.json` y conserva los mínimos estructurales existentes.
- El workflow canónico `synchronize-generated-site.yml` fue restaurado después de las migraciones.
- Los scripts auxiliares de migración fueron eliminados del head permanente.

## Evidencia pública comprobada

- `ingenieria-biomedica/bioinstrumentacion/index.html`: `data-status="placeholder"`.
- `ingenieria-biomedica/bioinstrumentacion/unidades/unidad-01.html`: `data-status="placeholder"`.
- `ingenieria-biomedica/analisis-instrumental/index.html`: `data-status="generated"`.

## Interpretación

La materialización corrige la verdad editorial global, pero no mejora ni sustituye el contenido fallback. Las unidades históricas de Bioinstrumentación continúan disponibles únicamente como respaldo y deben reconstruirse después de aprobar la base piloto, resolver las brechas bibliográficas y organizar revisión especializada.

## Consistencia del validador curricular

El validador histórico exigía que todas las asignaturas quedaran en `generated` o `complete`. Ese supuesto contradecía el manifiesto actual, que distingue 43 cursos desarrollados y 51 pendientes. La corrección permanente conserva todos los mínimos estructurales y exige que cada curso público coincida exactamente con su pertenencia a `pending`, `developed` o `complete` en `data/catalog_statuses.json`.

Esta modificación no reduce el control: reemplaza una condición global incorrecta por una comprobación de consistencia individual y auditable para las 94 asignaturas.

## Ciclo estable requerido

Este commit inicia un ciclo de CI no creado por `github-actions[bot]`. El PR solo podrá salir de borrador cuando:

1. los workflows aplicables terminen en verde sobre un único SHA;
2. el generador resulte idempotente;
3. el diff final no contenga auxiliares temporales;
4. Bioinstrumentación permanezca `pending`;
5. no existan revisiones ni hilos humanos bloqueantes.