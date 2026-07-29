# Readiness de autoría — Bioinstrumentación, Unidad 1

**Estado de preparación base:** `authoring_preparation_review`  
**Workstream de prácticas:** `practice_implementation_review`  
**Workstream de evaluación:** `assessment_implementation_review`  
**Estado editorial del curso:** `pending`  
**Unidad desarrollada:** no  
**Fecha:** 29 de julio de 2026

## Decisión

**bloqueos técnicos resueltos:** caso de presión, modelo térmico sintético y registro de PhysioNet.

La Unidad 1 dispone de alcance, modelo conceptual, evaluación, feedback y fuentes localizadas. Los tres bloqueos técnicos verificables están resueltos, dos prácticas cuentan con implementación reproducible y el sistema de evaluación cerrada dispone de diagnóstico y recuperación ejecutables.

La teoría completa todavía **no está autorizada**, porque falta revisión disciplinar humana documentada.

## Artefactos de preparación

- `data/unit_preparation/bioinstrumentacion-unit-01.json`
- `data/unit_preparation/bioinstrumentacion-unit-01-blocker-resolution.json`
- `data/practice_implementations/bioinstrumentacion-unit-01.json`
- `data/assessment_implementations/bioinstrumentacion-unit-01.json`
- `data/assessment_implementations/bioinstrumentacion-unit-01-feedback.json`
- `data/source_registry/bioinstrumentacion-unit-01-blockers.json`
- `docs/pilots/bioinstrumentacion/unit-01/SOURCE_DOSSIER.md`
- `docs/pilots/bioinstrumentacion/unit-01/CONCEPT_AND_VISUAL_MODEL.md`
- `docs/pilots/bioinstrumentacion/unit-01/ASSESSMENT_AND_FEEDBACK_BLUEPRINT.md`
- `docs/pilots/bioinstrumentacion/unit-01/MISCONCEPTION_COMPLETION.md`
- `docs/pilots/bioinstrumentacion/unit-01/PRACTICE_AND_DATA_PLAN.md`
- `docs/pilots/bioinstrumentacion/unit-01/PRESSURE_CASE_RESOLUTION.md`
- `docs/pilots/bioinstrumentacion/unit-01/THERMAL_MODEL_RESOLUTION.md`
- `docs/pilots/bioinstrumentacion/unit-01/PHYSIONET_RECORD_100_SPEC.md`
- `docs/pilots/bioinstrumentacion/unit-01/PRACTICE_IMPLEMENTATION.md`
- `docs/pilots/bioinstrumentacion/unit-01/ASSESSMENT_IMPLEMENTATION.md`
- `docs/pilots/bioinstrumentacion/unit-01/DISCIPLINARY_REVIEW_REQUEST.md`

## Aspectos resueltos

### Alcance y modelo conceptual

La unidad distingue fenómeno, cantidad, mensurando, método, ruta de señal, modelo de medición, indicación, valor medido, resultado, influencia, corrección, incertidumbre, trazabilidad y aptitud para el uso. No invade procesamiento avanzado, normativa, diseño clínico ni interpretación diagnóstica.

### Evaluación y feedback

Los cinco resultados tienen evidencia observable, criterio de dominio, errores críticos y recuperación. Trece misconceptions cuentan con diagnóstico, explicación, dos pistas graduadas, actividad de recuperación distinta y criterio objetivo para continuar.

La implementación ejecutable incorpora:

- 18 ítems de clasificación con diez categorías;
- cuatro afirmaciones de trazabilidad;
- 13 rutas de feedback estructuradas;
- liberación progresiva por intento;
- rechazo explícito de calificación semántica automática para respuestas abiertas;
- rúbricas humanas con criterios críticos para `U1-A2`, `U1-A3` y `U1-A5`.

CI comprueba que el feedback no revela `correct_category`, `expected_decision`, una clave de respuesta ni una solución completa. Esta validación resuelve el riesgo técnico de feedback limitado a mostrar respuestas, pero no sustituye una prueba de usabilidad con estudiantes.

### Caso de presión

**Resuelto internamente para autoría.** El caso diferencia:

1. presión intravascular en sitio y referencia especificados;
2. estimación auscultatoria braquial;
3. estimación oscilométrica dependiente del algoritmo.

No se permite equiparar presión del manguito, PPG, tiempo de tránsito o una salida numérica con presión arterial directa.

### Modelo térmico

**Implementado y validado técnicamente.** El generador distingue:

- `T_u`: superficie no perturbada prescrita;
- `T_d`: superficie perturbada por contacto;
- `T_s`: estado dinámico del sensor;
- `y`: indicación con offset y ruido sintético.

El modelo de primer orden dispone de pruebas automáticas de determinismo, convergencia, respuesta a una y cinco constantes de tiempo, monotonía, ausencia de sobreimpulso ideal, hash de salida y límites de uso. No se presenta como modelo fisiológico validado.

### PhysioNet

**Implementado y fijado offline.** La práctica utiliza un fixture atribuido del encabezado `100.hea` de MIT-BIH v1.0.0, registro `100`. El parser valida dos canales, `360 Hz`, `650000` muestras, formato `212`, etiquetas `MLII` y `V5`, sin descargar `100.dat` ni interpretar señales.

### Reproducibilidad

Las prácticas y el sistema de evaluación utilizan únicamente la biblioteca estándar de Python. CI trabaja sin red, genera resultados en directorios temporales y rechaza fixtures o submissions inconsistentes. Los resultados de estudiantes y datasets generados no se versionan.

### Fuentes

La base metrológica se apoya en VIM3, JCGM GUM-1:2023, JCGM GUM-6:2020 y NIST TN 2156. La resolución de bloqueos incorpora statements AHA, literatura sobre termometría de contacto y documentación oficial de PhysioNet. El fixture conserva DOI, versión y licencia.

## Riesgos abiertos

1. Falta revisión disciplinar humana por una persona competente en metrología e instrumentación biomédica.
2. Falta una prueba cognitiva con una persona del perfil objetivo.
3. Falta revisar la usabilidad y dificultad de las pistas y problemas de recuperación.
4. Falta comprobar acuerdo entre revisores al aplicar las rúbricas humanas.
5. Las prácticas están validadas técnicamente, pero aún no han sido probadas por estudiantes ni revisadas externamente.
6. La teoría completa todavía no ha sido redactada ni auditada.

## Gate antes de redactar teoría completa

- [x] Alcance y exclusiones definidos.
- [x] Resultados y evidencias alineados.
- [x] Modelo conceptual y visual especificado.
- [x] Trece misconceptions y feedback diseñados.
- [x] Prácticas seguras y reproducibles planificadas.
- [x] Afirmaciones centrales vinculadas a fuentes directas.
- [x] Revisión interna del caso de presión arterial.
- [x] Revisión interna del modelo térmico.
- [x] Registro de PhysioNet fijado y comprobado documentalmente.
- [x] Dos prácticas implementadas y ejecutadas en un entorno limpio de CI.
- [x] Evaluación cerrada y feedback recuperativo implementados y probados en CI.
- [ ] Revisión disciplinar humana inicial.

La redacción completa solo puede comenzar cuando el último punto esté documentado mediante el paquete de revisión. Un workflow verde no sustituye esa revisión.

## Gate antes de considerar la unidad desarrollada

- teoría completa con fuentes y localizadores;
- al menos dos ejemplos razonados y un caso de transferencia no resuelto previamente;
- prácticas implementadas, ejecutadas y revisadas pedagógicamente;
- rúbricas y feedback probados con usuarios y revisores;
- revisión de exactitud científica y terminología;
- accesibilidad textual y visual;
- ausencia de saltos hacia interpretación clínica o requisitos normativos no consultados;
- validación automática del paquete;
- revisión humana documentada del bloque.

## Gate antes de `complete`

`complete` exige revisión disciplinar externa documentada del curso, resolución de observaciones, auditoría de continuidad entre unidades y evidencia de autonomía real. No se alcanza mediante conteos, generación automática o CI.

## Resultado editorial

Después de fusionar este bloque:

- Bioinstrumentación seguirá en `pending`;
- las unidades fallback públicas seguirán identificadas como contenido de respaldo;
- no existirá `data/course_redevelopment/bioinstrumentacion/units/unit-01.json`;
- dos prácticas serán ejecutables y auditables offline;
- la evaluación cerrada y el feedback serán ejecutables;
- las respuestas abiertas seguirán bajo rúbrica humana;
- la revisión disciplinar y la prueba cognitiva seguirán abiertas;
- la teoría completa continuará bloqueada.
