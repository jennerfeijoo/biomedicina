# Implementación de evaluación y feedback · Bioinstrumentación Unidad 2

**Estado:** `implemented_internal_review`  
**Evaluación automática:** únicamente respuestas estructuradas deterministas  
**Respuestas abiertas:** `human_rubric` sin puntuación semántica automática  
**Revisión disciplinar externa:** `pending_human_review`  
**Prueba cognitiva con estudiantes:** pendiente  
**Estado editorial del curso:** `pending`

## Propósito

Este bloque implementa evaluación diagnóstica y retroalimentación recuperativa para **Sensores, transductores y modelos estáticos y dinámicos**. Las tareas se conectan con los resultados `U2-LO1` a `U2-LO5` y con las evidencias reproducibles de `U2-P1`, `U2-P2` y `U2-P3`.

La implementación calcula dominio sobre respuestas estructuradas, valida rúbricas humanas y libera pistas graduadas **sin revelar la respuesta**. No redacta la teoría completa, no crea `unit-02.json`, no publica contenido y no convierte CI en revisión profesional.

La prueba cognitiva con estudiantes permanece pendiente; los fixtures verifican comportamiento técnico del motor, pero no aportan evidencia sobre comprensión, carga cognitiva o usabilidad real.

## Artefactos autoritativos

```text
data/assessment_implementations/bioinstrumentacion-unit-02.json
data/assessment_implementations/bioinstrumentacion-unit-02-feedback.json
scripts/bioinstrumentation_u2_assessment_core.py
scripts/evaluate_bioinstrumentation_u2_assessment.py
scripts/validate_bioinstrumentation_u2_assessment.py
```

Los fixtures de regresión se encuentran en:

```text
data/assessment_fixtures/bioinstrumentacion/unit-02/
```

## Matriz de evaluación

| Evaluación | Modalidad | Resultados | Evidencia vinculada | Criterio central |
|---|---|---|---|---|
| `U2-A1` | rúbrica humana | `U2-LO1` | clasificación funcional | declarar frontera, cantidades y funciones |
| `U2-A2` | estructurada automática | `U2-LO2`, `U2-LO3` | `U2-P1` | diagnosticar patrón, evidencia y prueba refutadora |
| `U2-A3` | estructurada automática | `U2-LO4` | `U2-P2` | aceptar o rechazar primer orden con límites y `τ` |
| `U2-A4` | estructurada automática | `U2-LO3`, `U2-LO5` | `U2-P3` y casos de carga | reconstruir ruta causal, perturbación y evidencia faltante |
| `U2-A5` | rúbrica humana | `U2-LO1`–`U2-LO5` | transferencia multicriterio | justificar selección y limitar conclusiones |

## U2-A2 · Auditoría de curvas estáticas

El motor recibe, para cada uno de cuatro casos:

```text
pattern
evidence[]
refutation_test
```

Los casos discriminan:

- región lineal local;
- saturación;
- zona muerta;
- histéresis.

Una clasificación solo cuenta como completa cuando coincide el patrón, incluye la evidencia mínima y selecciona una prueba capaz de desafiar la interpretación. La retroalimentación no devuelve el patrón esperado ni la lista correcta de evidencias.

## U2-A3 · Modelo dinámico de primer orden

La respuesta estructurada incluye:

```text
decision
reasons[]
tau_estimate_s
response_time_interpretation
bandwidth_interpretation
```

El control positivo exige:

- eje temporal;
- respuesta monótona sin sobreimpulso;
- cruce compatible con `1 − exp(−1)`;
- estimación de `τ = 2,0 s` dentro de `±0,1 s`;
- tiempo de respuesta dependiente del criterio;
- relación frecuencia–tiempo limitada al primer orden y a −3 dB.

Los controles negativos obligan a rechazar:

- retardo puro no modelado;
- segundo orden subamortiguado con sobreimpulso;
- curva estática sin eje temporal.

El motor no permite asignar `τ` cuando el modelo ha sido rechazado.

## U2-A4 · Revisión de mecanismos de carga

Cada respuesta identifica:

```text
decision
route
perturbed_quantity
missing_evidence
mitigation_status
```

Los cuatro casos cubren carga eléctrica, térmica, mecánica y óptica. Una mitigación siempre queda marcada como `proposed_not_guaranteed`; no puede presentarse como prueba de ausencia de carga, seguridad o desempeño del sistema.

## U2-A1 y U2-A5 · Rúbrica humana

Las respuestas abiertas requieren:

```text
rubric_scores
reviewer_notes
diagnosed_misconceptions
human_reviewer_confirmed: true
```

El motor solo:

1. verifica que estén todos los criterios;
2. valida rangos enteros;
3. suma puntos;
4. detecta criterios críticos en cero;
5. libera feedback para las rutas seleccionadas por la persona revisora.

No realiza comparación semántica, no inventa puntuaciones y no acepta una rúbrica sin confirmación humana. Esta modalidad es **rúbrica humana**, no evaluación automática de texto libre.

## Política de feedback

Cada error se conecta con uno o más de los doce misconceptions del contrato de preparación. El banco contiene:

- diagnóstico del error;
- explicación causal;
- primera pista;
- segunda pista;
- sección o fuente para revisar;
- problema de recuperación diferente;
- criterio objetivo para continuar.

La liberación es gradual:

- intento 1: diagnóstico, explicación y primera pista;
- intento 2: diagnóstico, explicación y segunda pista;
- intento 3 o posterior: problema diferente y criterio objetivo de recuperación.

Nunca se devuelven `expected_pattern`, `expected_decision`, rutas esperadas, `tau_target_s`, claves completas ni respuestas modelo.

## Ejecución

```bash
python scripts/evaluate_bioinstrumentation_u2_assessment.py \
  data/assessment_fixtures/bioinstrumentacion/unit-02/mastery-static.json
```

La salida es JSON y puede escribirse a un archivo temporal mediante `--output`. No se versionan resultados generados.

El gate completo se ejecuta con:

```bash
python scripts/validate_bioinstrumentation_u2_assessment.py
```

## Fixtures de regresión

Se incluyen pares de dominio y diagnóstico para:

- curvas estáticas;
- dinámica y controles negativos;
- carga e inferencia documental;
- rúbricas humanas.

Los fixtures de diagnóstico deben fallar dominio y activar rutas conceptuales específicas. Los fixtures de dominio no reciben remediación.

## Límites

Esta implementación:

- usa datos sintéticos o documentación compacta;
- no solicita datos de personas o muestras;
- no conecta sensores a sujetos;
- no interpreta resultados clínicos;
- no valida dispositivos reales;
- no demuestra seguridad o conformidad normativa;
- no equivale a revisión disciplinar humana;
- mantiene la publicación y la teoría completa bloqueadas.

## Estado posterior al bloque

```text
assessment_implementation: implemented_internal_review
machine_scored_assessments: U2-A2, U2-A3, U2-A4
human_scored_assessments: U2-A1, U2-A5
automatic_semantic_grading: false
answer_key_exposed_in_feedback: false
student_cognitive_test: pending
feedback_usability_review: pending
external_professional_review: pending_human_review
full_theory_drafting_authorized: false
unit_developed: false
public_release_authorized: false
course_state: pending
```

## Próximo gate

Antes de autorizar la teoría completa deben revisarse la usabilidad del feedback, la claridad de las rúbricas, el comportamiento de estudiantes reales y la concordancia entre revisores. Este bloque no aporta todavía esa evidencia humana.

## Correcciones de auditoría científica y editorial interna

La auditoría interna conjunta de prácticas, evaluaciones y feedback quedó en `passed_with_corrections_applied`.

1. **Carga eléctrica:** `LG01` ahora identifica como cantidad perturbada la **tensión de salida del puente**. La transferencia de deformación pertenece al caso mecánico y no se combina con la carga por impedancia de entrada.
2. **Alcance del rechazo dinámico:** `reject_declared_simple_first_order` significa que el modelo simple declarado no explica la evidencia. No afirma que ningún modelo compuesto pueda contener un subsistema de primer orden.
3. **Alineación diagnóstica:** `SC01` remedia linealidad global indebida; la ruta «mayor sensibilidad es mejor» permanece en los casos donde existe una decisión de sensibilidad o selección.
4. **Trazabilidad:** cada evaluación `U2-A1` a `U2-A5` posee un `evidence_crosswalk` con resultados, prácticas, afirmaciones fuente y artefactos localizados.
5. **Protección de claves:** los campos esperados se conservan solo para evaluación interna. El payload del estudiante y cualquier futuro cliente público deben excluirlos.

Los identificadores de máquina permanecen en inglés para mantener compatibilidad y reproducibilidad; las instrucciones y explicaciones dirigidas al estudiante usan terminología española. Esta auditoría no sustituye revisión profesional externa, prueba cognitiva ni revisión de usabilidad del feedback.
