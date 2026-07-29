# Solicitud de revisión disciplinar — Bioinstrumentación, Unidad 1

**Estado:** `pending_human_review`  
**Unidad:** Mensurando, sistema de medición y cadena de trazabilidad  
**Efecto editorial:** ninguno; el curso permanece `pending`.

## Propósito de la revisión

Determinar si la base científica y pedagógica permite iniciar una redacción completa sin introducir errores de metrología, bioinstrumentación o interpretación clínica.

La revisión debe evaluar el paquete completo, no solo la corrección gramatical.

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
3. `data/source_registry/bioinstrumentacion-unit-01-blockers.json`
4. `PRESSURE_CASE_RESOLUTION.md`
5. `THERMAL_MODEL_RESOLUTION.md`
6. `PHYSIONET_RECORD_100_SPEC.md`
7. `CONCEPT_AND_VISUAL_MODEL.md`
8. `ASSESSMENT_AND_FEEDBACK_BLUEPRINT.md`
9. `PRACTICE_AND_DATA_PLAN.md`
10. `AUTHORING_READINESS.md`

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

Y registrar:

```text
reviewer_name:
reviewer_affiliation_or_context:
relevant_competence:
review_date:
reviewed_commit:
decision:
critical_findings:
required_changes:
non_blocking_suggestions:
scores:
signature_or_verifiable_confirmation:
```

## Regla editorial

Este documento **no es una revisión**. Su existencia, un workflow verde o una revisión interna del repositorio no autorizan la teoría completa. La autorización solo existe cuando una persona competente completa el registro anterior y las observaciones críticas quedan resueltas.
