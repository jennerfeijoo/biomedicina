# Implementación de evaluación — Bioinstrumentación Unidad 4

Estado editorial: `course_state: pending`.

## Alcance

La implementación cubre `U4-A1` a `U4-A4` mediante corrección determinista interna y mantiene `U4-A5` como evaluación integradora con revisión humana real obligatoria.

- `U4-A1`: aliasing ideal.
- `U4-A2`: cálculo de LSB nominal.
- `U4-A3`: detección de pérdida por contador de secuencia.
- `U4-A4`: límites de inferencia sobre sincronización.
- `U4-A5`: diseño integrador con rúbrica de seis dimensiones.

## Feedback

Cada respuesta produce criterio, respuesta observada, decisión, explicación, ruta de recuperación y límite de inferencia.

`U4-A5` solo puede devolver `pending_human_review`; no existe aprobación automática.

## Límites

- `human_review_executed: false`
- `professional_review_claimed: false`
- `public_release_authorized: false`
- no se afirma seguridad, conformidad, validez clínica o utilidad diagnóstica;
- no se conectan personas, electrodos ni equipos biomédicos;
- `unit-04.json` permanece ausente.
