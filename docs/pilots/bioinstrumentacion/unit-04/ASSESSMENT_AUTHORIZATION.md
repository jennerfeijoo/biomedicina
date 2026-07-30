# Autorización interna de evaluación — Bioinstrumentación Unidad 4

## Alcance

Se autoriza la implementación interna de las evaluaciones `U4-A1` a `U4-A5` después de verificar que los seis bloqueos técnicos fueron resueltos y que las prácticas `U4-P1`, `U4-P2` y `U4-P3` existen bajo una política exclusivamente sintética.

La autorización no equivale a publicación, validación clínica, conformidad reglamentaria, seguridad eléctrica ni aprobación profesional.

## Evaluaciones autorizadas

- `U4-A1`: muestreo, banda y aliasing.
- `U4-A2`: rango, LSB, cuantización y saturación.
- `U4-A3`: ENOB, bits nominales y condiciones de prueba.
- `U4-A4`: sincronización, pérdida, duplicación y reordenamiento.
- `U4-A5`: diseño trazable de una cadena de digitalización biomédica.

`U4-A1` a `U4-A4` podrán utilizar corrección determinista. `U4-A5` deberá quedar como evaluación mediante rúbrica y revisión humana real. Ninguna automatización podrá marcar `U4-A5` como aprobada.

## Contrato de feedback

Toda respuesta deberá devolver:

1. criterio evaluado;
2. respuesta observada;
3. decisión;
4. explicación causal;
5. ruta de recuperación;
6. límite de inferencia.

El feedback no podrá afirmar validez clínica, rendimiento diagnóstico, seguridad eléctrica, conformidad regulatoria o aprobación profesional.

## Restricciones

- sin red ni paquetes externos;
- sin datos personales;
- sin adquisición con personas, electrodos o equipos biomédicos;
- sin creación de `unit-04.json`;
- sin publicación;
- `course_state: pending`.

## Estado resultante

```text
assessment_implementation_authorized: true
automatic_scoring_authorized: U4-A1..U4-A4
human_review_required: U4-A5
full_theory_drafting_authorized: false
public_release_authorized: false
professional_review_claimed: false
course_state: pending
```
