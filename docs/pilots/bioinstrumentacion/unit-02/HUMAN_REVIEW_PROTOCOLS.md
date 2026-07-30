# Protocolos de revisión humana · Bioinstrumentación Unidad 2

## Estado

```text
protocol_status: protocol_ready_pending_human_execution
cognitive_test: pending_human_execution
feedback_usability_review: pending_human_execution
inter_rater_review: pending_human_execution
external_professional_review: pending_human_review
course_state: pending
public_release_authorized: false
unit_developed: false
```

Este bloque prepara la ejecución humana del borrador autoral de la Unidad 2. **No constituye evidencia humana**, revisión profesional, aprobación institucional, validación clínica, conformidad regulatoria ni autorización de publicación.

El contrato estructurado es:

```text
data/review_protocols/bioinstrumentacion-unit-02-human-review.json
```

## Prueba cognitiva

La prueba utiliza muestreo intencional para detección de problemas —`purposive_problem_detection_not_population_estimation`— y no para estimar prevalencias en una población. El gate piloto requiere al menos tres sesiones completadas fuera del repositorio público.

Las tareas seleccionadas son:

- `U2-A1`: clasificación funcional y justificación de fronteras;
- `U2-A2`: diagnóstico de propiedades estáticas;
- `U2-A3`: alcance del rechazo `reject_declared_simple_first_order`;
- `U2-A5`: selección multicriterio y límites de las afirmaciones.

La sesión debe incluir think-aloud, probes retrospectivos de comprensión, recuperación, juicio y respuesta, observación de uso del feedback y clasificación de problemas por severidad. Los criterios verifican, entre otros puntos, que la persona:

- distinga sensor, transductor, interfaz y sistema;
- exprese sensibilidad con unidades y dominio;
- no confunda constante de tiempo con cualquier definición de tiempo de respuesta;
- no interprete el rechazo del modelo simple como rechazo de todos los modelos dinámicos;
- no transfiera una especificación de componente a utilidad clínica.

La plantilla vacía se encuentra en:

```text
data/review_templates/bioinstrumentacion/unit-02/cognitive-session-template.json
```

No deben almacenarse identificadores directos, datos clínicos, audio, video ni transcripciones completas en el repositorio público. Cualquier grabación requiere consentimiento separado y almacenamiento gobernado fuera del repositorio.

## Revisión de usabilidad del feedback

Dos personas deben revisar las doce rutas diagnósticas. Para cada ruta se evalúa:

1. correspondencia entre error y diagnóstico;
2. explicación causal sin revelar la respuesta;
3. progresión entre primera y segunda pista;
4. localización de la fuente o sección de recuperación;
5. problema de transferencia diferente;
6. criterio objetivo para continuar.

Una ruta con un problema crítico no puede conservarse sin corrección y nueva revisión.

## Concordancia entre revisores

Las tareas abiertas `U2-A1` y `U2-A5` requieren dos revisores independientes. La escala ordinal es `0, 1, 2`. La ronda final debe incluir al menos doce elementos doblemente puntuados.

El cálculo reporta:

- acuerdo exacto;
- acuerdo ponderado lineal;
- **weighted kappa** lineal.

Umbrales del piloto:

```text
minimum_exact_agreement: 0.75
minimum_weighted_agreement: 0.85
minimum_weighted_kappa: 0.60
minimum_double_rated_items: 12
```

La plantilla y el calculador son:

```text
data/review_templates/bioinstrumentacion/unit-02/inter-rater-round-template.json
scripts/calculate_bioinstrumentation_u2_agreement.py
```

Los coeficientes describen consistencia bajo la muestra, escala y distribución de categorías observadas. No demuestran validez de contenido, competencia clínica ni generalización a otros evaluadores.

## Controles sintéticos

CI ejecuta dos fixtures explícitamente sintéticos:

- `high-agreement-synthetic.json` debe superar los umbrales;
- `low-agreement-synthetic.json` debe fallar al menos un umbral.

Los fixtures prueban el cálculo y el gate. No representan revisores reales ni pueden emplearse como evidencia de concordancia humana.

## Gate permanente

```text
scripts/validate_bioinstrumentation_u2_human_review.py
```

El gate verifica contrato, plantillas vacías, gobernanza, controles sintéticos, unidad autoral, auditoría interna aprobada, ausencia de evidencia externa fabricada y permanencia del curso en `pending`.

## Ejecución válida futura

Para registrar una ejecución humana real se requiere, fuera de este bloque:

- commit exacto de la unidad y versión de rúbrica;
- consentimiento y gobernanza documentados;
- perfiles de participantes o revisores verificados sin publicar identificadores;
- sesiones o puntuaciones independientes efectivamente realizadas;
- análisis de problemas y correcciones trazables;
- nueva revisión después de cambios críticos;
- decisión profesional separada en el issue `#161`.

Hasta entonces permanecen `pending_human_execution` y `pending_human_review`.
