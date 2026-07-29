# Solicitud de revisión disciplinar — Bioinstrumentación, Unidad 1

**Estado:** `pending_human_review`  
**Unidad:** Mensurando, sistema de medición y cadena de trazabilidad  
**Efecto editorial:** ninguno; el curso permanece `pending`.

## Propósito de la revisión

Determinar si la base científica y pedagógica permite iniciar una redacción completa sin introducir errores de metrología, bioinstrumentación o interpretación clínica.

La revisión debe evaluar el paquete completo, no solo la corrección gramatical.

## Handoff auditable

El contrato de entrega está en `data/review_handoffs/bioinstrumentacion-unit-01.json`.

La persona revisora debe recibir un manifiesto generado sobre un commit concreto y completar una copia de `disciplinary-review-decision-template.json`. El procedimiento completo está documentado en `REVIEW_HANDOFF_AND_AUTHORIZATION.md`.

Una decisión solo puede aplicarse al commit y al digest SHA-256 registrados. Si cambia cualquier artefacto obligatorio, debe generarse un nuevo manifiesto y revisarse el paquete actualizado.

## Competencia esperada del revisor

La persona revisora debería demostrar al menos dos de las siguientes capacidades:

- formación o experiencia en metrología y evaluación de incertidumbre;
- docencia o práctica profesional en bioinstrumentación;
- experiencia con sistemas de medición fisiológica;
- experiencia en validación técnica de dispositivos o sistemas biomédicos;
- capacidad para distinguir desempeño analítico, validación del uso y utilidad clínica.

## Material obligatorio

1. `data/unit_preparation/bioinstrumentacion-unit-01.json`
2. `data/unit_preparation/bioinstrumentacion-unit-01-blocker-resolution.json`
3. `data/practice_implementations/bioinstrumentacion-unit-01.json`
4. `data/assessment_implementations/bioinstrumentacion-unit-01.json`
5. `data/assessment_implementations/bioinstrumentacion-unit-01-feedback.json`
6. `data/review_protocols/bioinstrumentacion-unit-01-human-review.json`
7. `data/source_registry/bioinstrumentacion-unit-01-blockers.json`
8. `data/source_registry/bioinstrumentacion-unit-01-review-methods.json`
9. `SOURCE_DOSSIER.md`
10. `PRESSURE_CASE_RESOLUTION.md`
11. `THERMAL_MODEL_RESOLUTION.md`
12. `PHYSIONET_RECORD_100_SPEC.md`
13. `CONCEPT_AND_VISUAL_MODEL.md`
14. `ASSESSMENT_AND_FEEDBACK_BLUEPRINT.md`
15. `MISCONCEPTION_COMPLETION.md`
16. `PRACTICE_AND_DATA_PLAN.md`
17. `PRACTICE_IMPLEMENTATION.md`
18. `ASSESSMENT_IMPLEMENTATION.md`
19. `COGNITIVE_TEST_PROTOCOL.md`
20. `INTER_RATER_AGREEMENT_PROTOCOL.md`
21. `AUTHORING_READINESS.md`
22. `REVIEW_HANDOFF_AND_AUTHORIZATION.md`

## Preguntas de revisión

### Metrología

- ¿El mensurando está suficientemente especificado en los tres casos?
- ¿Indicación, valor medido y resultado permanecen separados?
- ¿La trazabilidad se atribuye al resultado y no al instrumento?
- ¿Las magnitudes de influencia y condiciones de uso son suficientes para una unidad introductoria?
- ¿La simplificación del modelo de medición es explícita y pedagógicamente válida?

### Presión

- ¿La distinción entre medición intraarterial, estimación auscultatoria y estimación oscilométrica evita equivalencias incorrectas?
- ¿El caso puede enseñarse sin entrar en procedimientos clínicos?
- ¿Falta algún elemento crítico sobre sitio, referencia, dinámica o algoritmo?

### Temperatura

- ¿La separación `T_u`, `T_d`, `T_s` e `y` es científicamente defendible como modelo didáctico?
- ¿La aproximación de primer orden está suficientemente limitada?
- ¿Las pruebas previstas detectan confusión entre perturbación, dinámica, offset y ruido?

### ECG y datos

- ¿El uso del registro 100 está correctamente limitado a metadatos?
- ¿El snapshot del encabezado y los metadatos esperados son suficientes para reproducibilidad?
- ¿Las inferencias clínicas están excluidas de forma inequívoca?

### Evaluación y autonomía

- ¿Las preguntas discriminan razonamiento y no solo vocabulario?
- ¿El feedback permite identificar y recuperar errores específicos?
- ¿Los criterios para continuar son observables?
- ¿Existen saltos de prerrequisitos que impedirían aprendizaje autónomo?

## Escala de revisión

Cada dimensión se puntúa de 1 a 5:

| Dimensión | 1 | 3 | 5 |
|---|---|---|---|
| Exactitud científica | errores sustantivos | aceptable con correcciones | exacta y bien limitada |
| Especificidad disciplinar | genérica | parcialmente específica | propia de bioinstrumentación |
| Trazabilidad de fuentes | insuficiente | mayormente localizada | cada afirmación central localizada |
| Alineación educativa | desalineada | parcial | resultado–evidencia–feedback coherentes |
| Seguridad y límites | ambiguos | suficientes | inequívocos y verificables |
| Autonomía | depende de tutor | recuperación parcial | permite detectar y corregir errores |

La aprobación exige puntuación mínima de 4 en todas las dimensiones y ausencia de error crítico.

## Errores críticos

Cualquiera de los siguientes impide aprobar:

- confundir presión directa y estimaciones por manguito;
- presentar el modelo térmico como fisiología validada;
- usar PhysioNet para interpretación diagnóstica;
- atribuir trazabilidad al instrumento o certificado;
- reproducir requisitos normativos no consultados;
- afirmar utilidad clínica desde desempeño técnico;
- autorizar prácticas con personas o equipos clínicos no supervisados.

## Decisión formal

El revisor debe seleccionar una sola opción:

- `approve_for_controlled_drafting`
- `approve_with_changes`
- `do_not_approve`

Y registrar mediante la plantilla estructurada:

```text
reviewer.name
reviewer.affiliation_or_context
reviewer.competence_categories
reviewer.competence_note
review.review_date
review.reviewed_commit
review.packet_digest_sha256
review.decision
review.scores
review.critical_findings
review.required_changes
review.non_blocking_suggestions
confirmation.actor_type
confirmation.method
confirmation.reference
confirmation.statement
authorization_requested
```

`approve_with_changes` no autoriza la redacción. Las modificaciones deben resolverse y someterse a una nueva decisión sobre un paquete regenerado.

## Regla editorial

Este documento **no es una revisión**. Su existencia, un workflow verde, una revisión interna del repositorio o un fixture con puntuaciones máximas no autorizan la teoría completa.

La autorización solo existe cuando una persona competente completa un registro real, el commit y el manifiesto coinciden, todas las dimensiones alcanzan el umbral, no existen errores críticos ni cambios obligatorios pendientes y la confirmación es verificable.

Incluso una autorización válida se limita a `controlled_full_theory_drafting_only`: no desarrolla la unidad, no publica contenido y no cambia el estado del curso.
