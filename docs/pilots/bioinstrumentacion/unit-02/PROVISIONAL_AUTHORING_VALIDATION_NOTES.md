# Notas de validación — autorización provisional de autoría U2

## Propósito

Este archivo documenta las comprobaciones esperadas del bloque de autorización provisional. No contiene teoría de la unidad, evidencia humana ni una decisión profesional.

## Regresiones protegidas

El gate debe fallar si ocurre cualquiera de estas condiciones:

- se modifica el commit base `a29fcedce078de03976970cdb8ce21a10b300245`;
- la auditoría deja de registrar seis hallazgos resueltos y cero críticos o mayores pendientes;
- se elimina una restricción científica o editorial obligatoria;
- se presenta el override del propietario como revisión humana o profesional;
- el curso deja de estar en `pending`;
- se autoriza publicación o estado `developed`;
- se crea evidencia externa ficticia;
- se crea parcialmente el futuro paquete autoral sin fuente, constructor y validador completos.

## Separación de estados

La autorización provisional habilita autoría controlada, pero mantiene independientes:

```text
internal_controlled_authoring: authorized_provisionally
external_professional_review: pending_human_review
student_cognitive_test: pending_human_execution
feedback_usability_review: pending_human_execution
inter_rater_round: pending_human_execution
public_release: blocked
course_state: pending
```

La futura creación de `unit-02.json` deberá ocurrir en un PR separado y acompañarse de fuente modular, constructor determinista, validador autoral y auditoría posterior del borrador.
