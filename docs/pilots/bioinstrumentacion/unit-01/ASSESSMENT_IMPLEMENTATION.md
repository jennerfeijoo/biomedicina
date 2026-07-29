# Implementación de evaluación y feedback — Bioinstrumentación, Unidad 1

**Estado:** `implemented_internal_review`  
**Estado editorial:** `pending`  
**Revisión disciplinar:** `pending_human_review`  
**Prueba cognitiva pendiente:** sí

## Decisión

La Unidad 1 dispone ahora de una implementación ejecutable para evaluación cerrada, diagnóstico de misconceptions y recuperación graduada. Este bloque no publica actividades ni autoriza la teoría completa.

La implementación automatiza únicamente aquello que admite una clave inequívoca. Las respuestas abiertas de especificación, auditoría de cadenas y transferencia mantienen **rúbrica humana**; no se utiliza coincidencia de palabras, clasificación generativa ni una puntuación semántica automática.

## Artefactos

- `data/assessment_implementations/bioinstrumentacion-unit-01.json`
- `data/assessment_implementations/bioinstrumentacion-unit-01-feedback.json`
- `scripts/bioinstrumentation_assessment_core.py`
- `scripts/run_bioinstrumentation_u1_assessment.py`
- `scripts/validate_bioinstrumentation_u1_assessment.py`
- `data/assessment_fixtures/bioinstrumentacion/unit-01/mastery-concept-sort.json`
- `data/assessment_fixtures/bioinstrumentacion/unit-01/diagnostic-concept-sort.json`
- `data/assessment_fixtures/bioinstrumentacion/unit-01/diagnostic-traceability.json`

## Evaluaciones automatizadas

### U1-A1 — Clasificación diagnóstica

Contiene exactamente 18 ítems y diez categorías funcionales:

- fenómeno;
- cantidad;
- mensurando;
- señal;
- indicación;
- valor medido;
- resultado de medición;
- cantidad de entrada;
- magnitud de influencia;
- referencia.

La regla de dominio exige al menos 15 respuestas correctas y ausencia de errores en los distractores críticos. Una clasificación incorrecta se vincula con una o más misconceptions documentadas; no se deriva el diagnóstico de una etiqueta clínica ni de texto libre.

### U1-A4 — Revisión de afirmaciones de trazabilidad

Incluye cuatro afirmaciones. El estudiante selecciona una decisión limitada y los componentes documentales presentes o ausentes. El motor comprueba:

- sujeto de la afirmación;
- referencia;
- cadena de calibraciones;
- condiciones e intervalo;
- incertidumbre;
- separación entre trazabilidad y aptitud para el uso.

## Evaluaciones con rúbrica humana

Las siguientes tareas no se califican automáticamente:

- `U1-A2`: especificación de mensurandos;
- `U1-A3`: auditoría de sistema, cadena y modelo;
- `U1-A5`: transferencia a un caso no utilizado en ejemplos.

Cada una dispone de criterios de 0–2, criterios críticos y una regla de dominio. El motor rechaza cualquier intento de usar estas tareas como evaluación cerrada.

## Feedback por intento

El feedback se libera de forma progresiva:

1. **Primer intento:** diagnóstico, explicación del fallo, primera pista y localizador.
2. **Segundo intento:** diagnóstico, explicación, segunda pista y localizador.
3. **Tercer intento o posterior:** problema de recuperación diferente, criterio objetivo para continuar y localizador.

La salida funciona **sin revelar la respuesta**. No contiene:

- `correct_category`;
- `expected_decision`;
- `answer_key`;
- una respuesta completa para copiar.

El problema de recuperación cambia el contexto o la estructura inferencial; no se limita a modificar números.

## Banco de 13 misconceptions

El banco ejecutable conserva exactamente los 13 identificadores del contrato de preparación. Cada entrada incluye:

- misconception diagnosticada;
- explicación causal del fallo;
- dos pistas graduadas;
- sección o fuente que debe revisarse;
- problema de recuperación distinto;
- criterio objetivo de continuación.

Todos los distractores y afirmaciones automatizadas apuntan a identificadores existentes. Las tareas abiertas también declaran qué misconceptions debe considerar quien aplique la rúbrica.

## Validación

El gate prueba:

- fixture de dominio completo con 18/18;
- fixture diagnóstico con errores críticos;
- fixture de trazabilidad;
- liberación diferente en intentos 1, 2 y 3;
- ausencia de campos que revelen la clave;
- rechazo de evaluación automática de tareas abiertas;
- correspondencia exacta con el blueprint y sus 13 misconceptions;
- Bioinstrumentación en `pending`;
- ausencia de unidad autoral;
- revisión humana todavía abierta.

## Límites

CI demuestra coherencia estructural y comportamiento determinista. No demuestra que las instrucciones sean comprensibles para estudiantes, que las pistas tengan la dificultad adecuada ni que las rúbricas produzcan acuerdo entre revisores.

Por tanto:

- la revisión disciplinar permanece `pending_human_review`;
- la prueba cognitiva pendiente debe realizarse con una persona del perfil objetivo;
- la usabilidad del feedback permanece pendiente;
- la teoría completa no está autorizada;
- la unidad no está desarrollada ni publicada.
