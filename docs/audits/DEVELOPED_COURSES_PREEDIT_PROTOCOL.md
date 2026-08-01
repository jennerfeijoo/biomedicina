# Protocolo de evaluación previa de asignaturas desarrolladas

## Regla vinculante

Ninguna asignatura clasificada como `developed`, ni ninguna asignatura `pending` que ya contenga unidades autorales o avanzadas, se editará antes de completar una evaluación de contenido de solo lectura.

## Objetivo

Evitar que una edición posterior:

- degrade contenido ya sólido;
- duplique explicaciones existentes;
- elimine trazabilidad o bibliografía útil;
- sustituya contenido autoral por texto genérico;
- cambie el nivel académico sin justificación;
- confunda una carencia editorial con una carencia científica.

## Dimensiones obligatorias

Cada curso será evaluado en las siguientes dimensiones:

1. **Cobertura curricular**: correspondencia entre objetivos, unidades y conceptos esperados.
2. **Progresión**: orden lógico, prerrequisitos y dificultad creciente.
3. **Rigor científico**: definiciones, modelos, ecuaciones, supuestos y límites de inferencia.
4. **Profundidad**: suficiencia de las explicaciones frente al nivel declarado.
5. **Redundancia**: repeticiones dentro del curso y solapamientos evitables con otros cursos.
6. **Ejemplos y casos**: pertinencia, corrección y conexión biomédica.
7. **Prácticas**: reproducibilidad, seguridad, entregables y alineación con objetivos.
8. **Evaluación**: cobertura de resultados de aprendizaje, feedback y recuperación.
9. **Bibliografía**: relevancia, verificabilidad, actualidad y relación con afirmaciones.
10. **Publicación**: sincronización entre fuente estructurada y HTML público.
11. **Accesibilidad editorial**: claridad, terminología, notación y navegabilidad.
12. **Estado real**: decisión entre conservar, corregir, ampliar, reestructurar o no editar.

## Resultado por asignatura

Cada evaluación producirá una ficha con:

- `subject_id`;
- estado previo;
- evidencia inspeccionada;
- fortalezas;
- defectos críticos;
- defectos mayores;
- defectos menores;
- redundancias;
- vacíos;
- riesgo de editar;
- decisión editorial;
- lista cerrada de cambios autorizados;
- cambios explícitamente prohibidos;
- estado posterior esperado.

## Decisiones permitidas

- `preserve`: el contenido se conserva; solo se corrigen errores verificables.
- `minor_revision`: ajustes locales sin reestructuración.
- `major_revision`: requiere reordenamiento o ampliación sustantiva.
- `complete_missing_units`: el contenido existente se preserva y solo se completan vacíos.
- `public_sync_only`: el contenido está bien; solo falta sincronización pública.
- `hold_for_expert_review`: no editar hasta revisión disciplinar.

## Secuencia de trabajo

1. Ejecutar inventarios técnicos existentes.
2. Leer fuente estructurada, páginas públicas, prácticas, evaluaciones y bibliografía.
3. Redactar ficha de auditoría sin modificar contenido académico.
4. Registrar decisión y cambios autorizados.
5. Solo entonces abrir el PR de edición de la asignatura.

## Primera ronda

La primera ronda evaluará, antes de cualquier edición:

1. `bioinstrumentacion`;
2. `biomateriales`;
3. `biomecanica`;
4. `imagenes-biomedicas`;
5. `senales-biomedicas`;
6. `laboratorio-bioinstrumentacion`.

Bioinstrumentación se evaluará transversalmente como curso completo; no se reabrirá el flujo de micro-PR por unidad.
