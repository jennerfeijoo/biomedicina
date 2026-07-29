# Paquete de entrega y autorización — Bioinstrumentación, Unidad 1

**Estado:** `pending_human_review`  
**Handoff:** `ready_pending_external_review`  
**Estado editorial:** `pending`  
**Redacción completa autorizada:** no

## Propósito

Este bloque convierte la solicitud de revisión disciplinar en un flujo auditable. Define qué materiales recibe la persona revisora, cómo se congela el contenido examinado y qué condiciones deben cumplirse antes de iniciar una redacción completa controlada.

El flujo no sustituye a la persona revisora. Un manifiesto SHA-256, una ejecución de CI, un fixture sintético o una revisión interna no constituyen aprobación disciplinar.

## Artefactos centrales

- `data/review_handoffs/bioinstrumentacion-unit-01.json`: contrato del handoff;
- `data/review_templates/bioinstrumentacion/unit-01/disciplinary-review-decision-template.json`: plantilla vacía de decisión;
- `scripts/build_bioinstrumentation_u1_review_packet.py`: generador determinista del manifiesto;
- `scripts/evaluate_bioinstrumentation_u1_authorization.py`: evaluador de la decisión;
- `scripts/validate_bioinstrumentation_u1_review_handoff.py`: gate permanente;
- `docs/pilots/bioinstrumentacion/unit-01/DISCIPLINARY_REVIEW_REQUEST.md`: preguntas y escala disciplinar.

## 1. Congelar el paquete

La revisión debe realizarse sobre un commit concreto. Desde un checkout limpio del commit que se entregará al revisor:

```bash
python scripts/build_bioinstrumentation_u1_review_packet.py \
  --reviewed-commit <SHA_COMPLETO_DE_40_CARACTERES> \
  --output bioinstrumentacion-u1-review-packet.json
```

El manifiesto registra para cada artefacto:

- ruta;
- tamaño en bytes;
- SHA-256;
- digest global del paquete;
- commit que se declara revisado.

La generación es determinista: el mismo contenido y el mismo commit producen el mismo manifiesto.

## 2. Entregar el paquete

La persona revisora debe recibir:

1. el commit o un enlace permanente al commit;
2. el manifiesto generado;
3. todos los artefactos enumerados en `required_artifacts`;
4. la solicitud disciplinar;
5. una copia de la plantilla de decisión.

No debe recibir una versión mutable sin identificador de commit, porque una aprobación no puede trasladarse automáticamente a material modificado.

## 3. Completar la decisión

La decisión permite exactamente tres estados:

- `approve_for_controlled_drafting`;
- `approve_with_changes`;
- `do_not_approve`.

La persona revisora debe declarar al menos dos categorías de competencia, registrar el commit y el digest del paquete, puntuar las seis dimensiones, listar hallazgos y proporcionar una confirmación verificable.

No deben incluirse firmas manuscritas, teléfonos, direcciones, información clínica ni otros datos personales innecesarios. La confirmación puede referenciar una revisión de GitHub, un registro institucional, una atestación verificable o un documento firmado almacenado fuera del repositorio.

## 4. Evaluar la autorización

Cuando existan un manifiesto y una decisión reales:

```bash
python scripts/evaluate_bioinstrumentation_u1_authorization.py \
  --manifest <MANIFIESTO_REAL> \
  --decision <DECISION_REAL> \
  --output authorization-report.json
```

La autorización requiere simultáneamente:

- evidencia humana real;
- actor `human_reviewer`;
- decisión `approve_for_controlled_drafting`;
- al menos dos categorías de competencia válidas;
- commit y digest coincidentes con el manifiesto;
- puntuación mínima de 4/5 en cada dimensión;
- ningún hallazgo crítico;
- ninguna modificación obligatoria pendiente;
- confirmación verificable;
- solicitud explícita de autorización.

`approve_with_changes` nunca autoriza. Primero deben resolverse las modificaciones y realizarse una nueva decisión sobre el paquete actualizado.

## 5. Alcance de la autorización

Un resultado `authorized_for_controlled_drafting` permite únicamente comenzar una rama de redacción completa bajo control de fuentes y revisión.

La autorización:

- no desarrolla la unidad;
- no publica contenido;
- no valida prácticas con estudiantes;
- no demuestra utilidad clínica;
- no autoriza adquisición con personas;
- no promueve el curso a `developed` o `complete`;
- no sustituye la prueba cognitiva ni el acuerdo entre revisores.

## Controles negativos

CI incluye una reclamación sintética con puntuaciones máximas y decisión aprobatoria. Debe ser rechazada porque:

- `synthetic` es verdadero;
- `human_evidence` es falso;
- el actor es `ci_fixture`.

El gate también comprueba que `approve_with_changes` produzca `changes_required_no_authorization`.

## Estado actual

No existen todavía:

- `data/review_evidence/bioinstrumentacion-unit-01-disciplinary-review.json`;
- `data/review_evidence/bioinstrumentacion-unit-01-review-packet.json`.

Por tanto, el resultado actual debe permanecer `pending_human_review` y `controlled_full_theory_drafting_authorized: false`.
