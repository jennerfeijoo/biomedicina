# Auditoría léxica de redundancia — Biología del Desarrollo

**Fecha:** 2026-07-27  
**Estado:** cribado automatizado completado; revisión disciplinar de progresión pendiente  
**Rama:** `agent/biologia-desarrollo-evidence-based`  
**PR:** #113

## 1. Objetivo

Evaluar si las 14 unidades contienen bloques de texto idénticos, párrafos casi equivalentes o frases metodológicas repetidas que indiquen duplicación editorial. El análisis complementa, pero no sustituye, la auditoría conceptual registrada en `PROGRESSION_AND_REDUNDANCY_AUDIT.md`.

## 2. Alcance técnico

El auditor extrajo contenido pedagógico de:

- propósito y objetivos;
- párrafos y puntos clave;
- definiciones de glosario;
- ejemplos trabajados;
- actividades, problemas y criterios;
- errores frecuentes;
- autoevaluación;
- conexiones biomédicas.

Se excluyeron bibliografía, metadatos, títulos y avisos editoriales. Solo se compararon bloques pertenecientes a unidades distintas.

## 3. Resultados

| Métrica | Resultado |
|---|---:|
| Unidades analizadas | 14 |
| Bloques de texto analizados | 1.838 |
| Grupos exactos entre unidades | 0 |
| Pares casi duplicados sobre umbral | 0 |
| Frases recurrentes reportadas | 2 |

Umbrales utilizados:

- mínimo general: 8 tokens;
- comparación cercana: 16 tokens;
- similitud de secuencia: 0,82;
- Jaccard de tokens: 0,68;
- frase recurrente: 6 tokens presentes en al menos 3 unidades.

## 4. Único patrón recurrente

Las dos frases detectadas son ventanas solapadas del mismo patrón:

- `trazado de linaje y una perturbación`;
- `un trazado de linaje y una`.

Aparecen en instrucciones de actividades de las unidades 4, 8 y 11:

- Unidad 4: diseñar trazado de linaje y perturbación de polaridad o señalización;
- Unidad 8: añadir trazado de linaje y perturbación de señalización;
- Unidad 11: añadir trazado de linaje y perturbación con rescate.

### Evaluación editorial

No se considera duplicación problemática. Las tres instrucciones aplican una competencia transversal a sistemas distintos y añaden una exigencia contextual propia. La recurrencia refuerza el diseño causal del curso y no repite una explicación teórica.

No se modifica el contenido por este hallazgo.

## 5. Relación con la auditoría conceptual

El cribado léxico no contradice los solapamientos conceptuales ya documentados:

- Unidad 1 frente al resto: jerarquía de evidencia;
- Unidades 2 y 11: línea germinal frente a organogénesis gonadal;
- Unidades 4 y 13: implantación temprana frente a placenta posterior;
- Unidades 6 y 9: oscilador general frente a somitogénesis anatómica;
- Unidad 7 frente a 8–11: principios mecánicos frente a implementación por órgano;
- Unidad 12 frente a menciones de organoides en otras unidades;
- Unidades 13 y 14: DOHaD frente a plasticidad y evolución.

Estos solapamientos no producen párrafos duplicados según los umbrales utilizados. Su revisión restante es conceptual: comprobar que cada reaparición aumenta el nivel de integración, evidencia o aplicación.

## 6. Automatización

### `scripts/audit_course_redundancy.py`

- normaliza texto y acentos;
- identifica duplicación exacta entre unidades;
- calcula similitud de secuencia y Jaccard para pares comparables;
- detecta frases recurrentes entre tres o más unidades;
- limita la comparación cercana a categorías pedagógicas equivalentes;
- produce JSON y Markdown;
- no modifica contenido ni clasifica automáticamente una repetición como error.

### `.github/workflows/audit-course-redundancy.yml`

El workflow ejecuta el cribado y conserva los informes como artefactos. Su función actual es informativa: un número de coincidencias no debe bloquear el curso sin revisión humana.

## 7. Limitaciones

- La similitud léxica no detecta toda redundancia semántica expresada con palabras diferentes.
- Los umbrales pueden omitir paráfrasis parciales o detectar terminología técnica legítima.
- El análisis no evalúa por sí solo progresión cognitiva, densidad, claridad ni suficiencia.
- No se utilizaron embeddings ni modelos externos; el resultado es reproducible con biblioteca estándar.
- La ausencia de duplicación textual no demuestra ausencia de solapamiento conceptual.

## 8. Criterios de cierre

- [x] Inventario automatizado de bloques pedagógicos.
- [x] Detección de duplicados exactos entre unidades.
- [x] Detección de pares casi duplicados.
- [x] Detección de frases recurrentes.
- [x] Revisión manual de los candidatos encontrados.
- [x] Solapamientos conceptuales principales asignados a unidades canónicas.
- [ ] Revisar progresión y densidad mediante lectura disciplinar completa.
- [ ] Incorporar referencias cruzadas en la futura versión pública.
- [ ] Confirmar que la reducción de advertencias no elimine contexto necesario.

## 9. Veredicto

No existe evidencia de duplicación textual sustancial entre las 14 unidades. La repetición detectada corresponde a una práctica experimental transversal y se conserva. La auditoría de redundancia queda cerrada a nivel estructural y léxico; permanece pendiente la revisión disciplinar de progresión, densidad y secuenciación pedagógica.
