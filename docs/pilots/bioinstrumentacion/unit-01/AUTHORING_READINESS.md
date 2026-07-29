# Readiness de autoría — Bioinstrumentación, Unidad 1

**Estado del bloque:** `authoring_preparation_review` con bloqueos técnicos resueltos  
**Estado editorial del curso:** `pending`  
**Unidad desarrollada:** no  
**Fecha:** 29 de julio de 2026

## Decisión

La Unidad 1 dispone de alcance, modelo conceptual, evaluación, feedback y prácticas planificadas. Además, los tres bloqueos técnicos verificables quedaron resueltos: el caso de presión diferencia mensurandos y métodos, el modelo térmico se limita a una simulación didáctica de primer orden y PhysioNet se fija en MIT-BIH v1.0.0, registro 100.

La teoría completa todavía **no está autorizada**, porque falta revisión disciplinar humana documentada.

## Artefactos de preparación

- `data/unit_preparation/bioinstrumentacion-unit-01.json`
- `data/unit_preparation/bioinstrumentacion-unit-01-blocker-resolution.json`
- `data/source_registry/bioinstrumentacion-unit-01-blockers.json`
- `docs/pilots/bioinstrumentacion/unit-01/SOURCE_DOSSIER.md`
- `docs/pilots/bioinstrumentacion/unit-01/CONCEPT_AND_VISUAL_MODEL.md`
- `docs/pilots/bioinstrumentacion/unit-01/ASSESSMENT_AND_FEEDBACK_BLUEPRINT.md`
- `docs/pilots/bioinstrumentacion/unit-01/MISCONCEPTION_COMPLETION.md`
- `docs/pilots/bioinstrumentacion/unit-01/PRACTICE_AND_DATA_PLAN.md`
- `docs/pilots/bioinstrumentacion/unit-01/PRESSURE_CASE_RESOLUTION.md`
- `docs/pilots/bioinstrumentacion/unit-01/THERMAL_MODEL_RESOLUTION.md`
- `docs/pilots/bioinstrumentacion/unit-01/PHYSIONET_RECORD_100_SPEC.md`
- `docs/pilots/bioinstrumentacion/unit-01/DISCIPLINARY_REVIEW_REQUEST.md`

## Aspectos resueltos

### Alcance

La unidad se limita a especificación del mensurando, capas de la medición, sistema y cadena, modelo introductorio, influencias, resultado, trazabilidad y aptitud para el uso. No invade diseño detallado de transductores, incertidumbre cuantitativa completa, procesamiento avanzado, normativa ni interpretación clínica.

### Modelo conceptual

Se distinguen explícitamente fenómeno, cantidad, mensurando, método, ruta de señal, modelo de medición, indicación, valor medido, resultado, influencia, corrección, incertidumbre, trazabilidad y aptitud para el uso.

### Evaluación y feedback

Los cinco resultados tienen evidencia observable, criterio de dominio, errores críticos y recuperación. Trece misconceptions cuentan con diagnóstico, explicación, dos pistas graduadas, actividad de recuperación distinta y criterio objetivo para continuar.

### Bloque técnico 1 — Presión

**Resuelto internamente para autoría.** El caso diferencia:

1. presión intravascular en sitio y referencia especificados;
2. estimación auscultatoria braquial;
3. estimación oscilométrica dependiente del algoritmo.

No se permite equiparar presión del manguito, PPG, tiempo de tránsito o una salida numérica con presión arterial directa. El caso no incluye procedimientos ni interpretación clínica.

### Bloque técnico 2 — Modelo térmico

**Resuelto internamente para diseño del dataset.** La práctica separa:

- `T_u`: superficie no perturbada;
- `T_d`: superficie perturbada por contacto;
- `T_s`: temperatura del sensor;
- `y`: indicación simulada.

El modelo de primer orden está limitado explícitamente y dispone de pruebas de convergencia, constante de tiempo, ausencia de sobreimpulso ideal y separación entre perturbación, dinámica, offset y ruido.

### Bloque técnico 3 — PhysioNet

**Resuelto y fijado.** Se utilizará:

- MIT-BIH Arrhythmia Database;
- versión `1.0.0`;
- registro `100`;
- archivos `100.hea` y `100.dat`;
- dos canales `MLII` y `V5`;
- frecuencia `360 Hz`;
- `650000` muestras.

La práctica se limita a metadatos. No usa anotaciones para clasificación ni realiza interpretación diagnóstica.

### Fuentes

La base metrológica se apoya en VIM3, JCGM GUM-1:2023, JCGM GUM-6:2020 y NIST TN 2156. La resolución de bloqueos incorpora statements AHA de medición de presión, literatura sobre termometría de contacto y la documentación oficial de PhysioNet. Cada fuente tiene afirmaciones autorizadas y limitaciones explícitas.

## Riesgos abiertos

1. Falta revisión disciplinar humana por una persona competente en metrología e instrumentación biomédica.
2. Falta una prueba cognitiva con una persona del perfil objetivo.
3. La implementación futura del feedback debe demostrar que no se limita a revelar respuestas.
4. Las prácticas todavía no se han implementado ni ejecutado desde un entorno limpio.
5. La teoría completa todavía no ha sido redactada ni auditada.

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
- [ ] Revisión disciplinar humana inicial.

La redacción completa solo puede comenzar cuando el último punto esté documentado mediante `DISCIPLINARY_REVIEW_REQUEST.md`. Un workflow verde no sustituye esa revisión.

## Gate antes de considerar la unidad desarrollada

- teoría completa con fuentes y localizadores;
- al menos dos ejemplos razonados y un caso de transferencia no resuelto previamente;
- prácticas implementadas y ejecutadas desde un entorno limpio;
- rúbricas y feedback probados;
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
- no se creará `data/course_redevelopment/bioinstrumentacion/units/unit-01.json`;
- los tres bloqueos técnicos estarán cerrados;
- la revisión disciplinar seguirá abierta;
- el siguiente bloque será obtener y registrar esa revisión antes de la autoría completa.
