# Evaluación previa de contenido — Bioinstrumentación

## Alcance

Evaluación de solo lectura previa a cualquier modificación del curso. Se inspeccionan unidades autorales, paquetes de prácticas y evaluaciones, auditorías existentes, fuentes y representación pública. Esta ficha no autoriza cambios todavía.

## Estado observado

- El curso dispone de desarrollo autoral sustantivo en sus unidades.
- Las unidades 1 a 6 contienen objetivos, teoría, modelos, ejemplos, prácticas, evaluaciones y límites de inferencia.
- El curso mantiene estado editorial pendiente porque la revisión disciplinar externa no se ha ejecutado.
- Existen numerosas capas de preparación, autorización, implementación y auditoría que aportan trazabilidad, pero también redundancia documental.

## Fortalezas

1. **Rigor conceptual**: diferencia fenómeno, cantidad, señal, indicación, resultado y uso previsto.
2. **Metrología explícita**: mensurando, trazabilidad, incertidumbre, calibración y límites de aptitud para el uso.
3. **Separación de inferencias**: evita presentar simulaciones como evidencia clínica, regulatoria o de seguridad.
4. **Progresión técnica**: avanza desde fundamentos de medición hacia electrodos, conversión, sensores, seguridad eléctrica y EMC.
5. **Prácticas reproducibles**: prioriza datos sintéticos, ejecución offline y resultados auditables.
6. **Evaluaciones diferenciadas**: separa corrección determinista de revisión humana obligatoria.
7. **Bibliografía y trazabilidad**: las unidades enlazan afirmaciones con registros de fuentes y paquetes editoriales.

## Hallazgos críticos

No se identifica, en esta evaluación inicial, un defecto que justifique reescribir el curso completo o sustituir sus unidades autorales.

## Hallazgos mayores

1. **Estado global incoherente con el desarrollo real**: el curso sigue `pending` pese a contener material autoral amplio.
2. **Arquitectura editorial sobredimensionada**: demasiados contratos, validadores y documentos por unidad.
3. **Falta de auditoría transversal única**: las auditorías existentes son principalmente unitarias; falta comprobar continuidad, repeticiones y dependencias entre las seis unidades.
4. **Revisión humana no ejecutada**: varias evaluaciones abiertas siguen preparadas pero no revisadas.
5. **Revisión disciplinar externa pendiente**: impide promover el curso a `complete`, pero no debería impedir publicarlo como `review`.
6. **Posible desalineación pública**: debe verificarse que las páginas HTML representen la versión autoral más reciente de todas las unidades.

## Hallazgos menores

1. La densidad terminológica puede ser alta para lectores sin base previa.
2. Algunos límites y advertencias se repiten en varias capas documentales.
3. La notación conceptual debe comprobarse transversalmente para evitar variantes innecesarias.
4. Debe revisarse que cada unidad incluya una ruta visible hacia prerrequisitos y recuperación.

## Riesgo de editar

**Alto** para reescrituras generales. El curso contiene material especializado y estructurado; una edición amplia sin mapa previo podría degradar precisión, eliminar límites o duplicar contenido.

## Decisión editorial provisional

`preserve_and_consolidate`

El contenido académico existente se preservará. La siguiente fase no será una reescritura, sino una auditoría transversal y una consolidación controlada.

## Cambios autorizables después de la auditoría transversal

- corregir errores científicos o terminológicos verificables;
- eliminar redundancias reales entre unidades;
- reforzar transiciones y prerrequisitos;
- completar vacíos identificados;
- sincronizar fuente estructurada y HTML público;
- consolidar documentación y validadores repetitivos;
- actualizar el estado del curso a `review` cuando todas las páginas estén sincronizadas.

## Cambios prohibidos por ahora

- reemplazar unidades autorales por contenido generado genérico;
- simplificar afirmaciones técnicas sin conservar supuestos y límites;
- declarar revisión profesional no ejecutada;
- marcar el curso como `complete`;
- modificar contenido antes de cerrar la matriz transversal de cobertura y redundancia.

## Próxima acción

Construir una matriz única de seis unidades con:

- resultados de aprendizaje;
- conceptos centrales;
- prerrequisitos;
- prácticas;
- evaluaciones;
- bibliografía;
- solapamientos;
- vacíos;
- estado de publicación.

Solo después se abrirá el PR integral de cierre de Bioinstrumentación.
