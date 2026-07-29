# Readiness de autoría — Bioinstrumentación, Unidad 1

**Estado del bloque:** `authoring_preparation_review`  
**Estado editorial del curso:** `pending`  
**Unidad desarrollada:** no  
**Fecha:** 29 de julio de 2026

## Decisión

La Unidad 1 dispone ahora de una base suficiente para revisión interna de autoría, pero no debe publicarse como lección desarrollada. El bloque define qué debe enseñarse, qué evidencia debe producir el estudiante, cómo se diagnostican errores y qué fuentes sostienen las afirmaciones centrales.

## Artefactos del bloque

- `data/unit_preparation/bioinstrumentacion-unit-01.json`
- `docs/pilots/bioinstrumentacion/unit-01/SOURCE_DOSSIER.md`
- `docs/pilots/bioinstrumentacion/unit-01/CONCEPT_AND_VISUAL_MODEL.md`
- `docs/pilots/bioinstrumentacion/unit-01/ASSESSMENT_AND_FEEDBACK_BLUEPRINT.md`
- `docs/pilots/bioinstrumentacion/unit-01/MISCONCEPTION_COMPLETION.md`
- `docs/pilots/bioinstrumentacion/unit-01/PRACTICE_AND_DATA_PLAN.md`

## Aspectos resueltos

### Alcance

La unidad se limita a especificación del mensurando, capas de la medición, sistema y cadena, modelo introductorio, influencias, resultado, trazabilidad y aptitud para el uso. No invade diseño detallado de transductores, incertidumbre cuantitativa completa, procesamiento avanzado, normativa ni interpretación clínica.

### Modelo conceptual

Se distinguen explícitamente:

- fenómeno y cantidad;
- mensurando y método;
- ruta de señal y modelo de medición;
- indicación, valor medido y resultado;
- influencia, corrección e incertidumbre;
- trazabilidad y aptitud para el uso.

### Evaluación

Los cinco resultados tienen evidencia observable, criterio de dominio, errores críticos y recuperación. La evaluación incluye clasificación diagnóstica, especificación, auditoría de cadena, modelo, trazabilidad y transferencia.

### Feedback

Trece misconceptions cuentan con:

- diagnóstico;
- explicación del fallo;
- dos pistas graduadas;
- actividad de recuperación distinta;
- criterio objetivo para continuar.

El primer ciclo de CI detectó cinco errores evaluados que todavía no tenían ficha propia. El banco y la documentación se completaron sin eliminar las pruebas que los discriminaban.

### Práctica

Se han definido tres prácticas seguras:

1. cadena térmica sintética;
2. auditoría de metadatos ECG abiertos;
3. auditoría documental de trazabilidad.

Ninguna requiere adquisición con personas, conexión a equipos clínicos ni interpretación diagnóstica.

### Fuentes

Las afirmaciones centrales se apoyan en VIM3, JCGM GUM-1:2023, JCGM GUM-6:2020 y NIST TN 2156. PhysioNet se usa solo como fuente de datos y metadatos para una práctica.

## Riesgos abiertos

1. La especificación del caso de presión arterial requiere revisión para evitar simplificar métodos invasivos y no invasivos como equivalentes.
2. El caso térmico necesita revisión del modelo sintético antes de generar datos.
3. Debe fijarse el registro exacto de MIT-BIH y comprobarse el diccionario de metadatos utilizado por el código.
4. Falta una prueba cognitiva con una persona del perfil objetivo.
5. Falta revisión disciplinar por una persona con competencia en metrología e instrumentación biomédica.
6. La implementación del feedback debe demostrar que no se limita a revelar respuestas.

## Gate antes de redactar teoría completa

- [x] Alcance y exclusiones definidos.
- [x] Resultados y evidencias alineados.
- [x] Modelo conceptual y visual especificado.
- [x] Trece misconceptions y feedback diseñados.
- [x] Prácticas seguras y reproducibles planificadas.
- [x] Afirmaciones centrales vinculadas a fuentes directas.
- [ ] Revisión interna del caso de presión arterial.
- [ ] Revisión interna del modelo térmico.
- [ ] Registro de PhysioNet fijado y comprobado.
- [ ] Revisión disciplinar inicial.

La redacción puede comenzar de forma controlada después de resolver los cuatro puntos pendientes. Ningún borrador deberá cambiar el estado del curso.

## Gate antes de considerar la unidad desarrollada

- teoría completa con fuentes y localizadores;
- al menos dos ejemplos razonados y un caso de transferencia no resuelto previamente;
- prácticas implementadas y ejecutadas desde un entorno limpio;
- rúbricas y feedback probados;
- revisión de exactitud científica y de terminología;
- accesibilidad textual y visual;
- ausencia de saltos hacia interpretación clínica o requisitos normativos no consultados;
- validación automática del paquete;
- revisión humana documentada del bloque.

## Gate antes de `complete`

Este bloque no modifica el criterio general. `complete` exige revisión disciplinar externa documentada del curso, resolución de observaciones, auditoría de continuidad entre unidades y evidencia de que las actividades permiten autonomía real. Un workflow verde no satisface este requisito.

## Resultado editorial

Después de fusionar este bloque:

- Bioinstrumentación seguirá en `pending`;
- las seis unidades fallback públicas seguirán identificadas como contenido de respaldo;
- no se creará todavía `data/course_redevelopment/bioinstrumentacion/units/unit-01.json`;
- el siguiente bloque será la resolución de brechas y revisión inicial, o la autoría controlada cuando esas condiciones estén documentadas.
