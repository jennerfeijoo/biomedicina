# Auditoría curricular de Biología del Desarrollo

**Fecha:** 2026-07-26  
**Estado:** reconstrucción completa en espacio de trabajo; no migrada a producción  
**Rama:** `agent/biologia-desarrollo-evidence-based`  
**PR:** #113

## 1. Veredicto

La arquitectura prevista de **14 unidades** está implementada en `data/course_redevelopment/biologia-desarrollo/units/`. La secuencia cubre fundamentos experimentales, desarrollo temprano, patronamiento, morfogénesis, organogénesis, células madre, desarrollo humano, teratología y evo-devo.

El curso es **técnicamente íntegro y curricularmente coherente como borrador avanzado**, pero todavía no debe presentarse como contenido público terminado. Antes de la migración se requieren revisión disciplinar externa, consolidación bibliográfica, auditoría de repetición y validación explícita de algunas coberturas transversales.

## 2. Inventario técnico

- `course.json`: presente y alineado con 14 unidades.
- `unit-01.json` a `unit-14.json`: presentes.
- `data/curriculum_decisions/biologia-desarrollo.json`: presente.
- `data/source_registry/biologia-desarrollo.json`: presente.
- Archivos públicos de la asignatura: sin cambios en este PR.
- Estado de producción: aislado del trabajo parcial.

El commit `790e2f9c7c65d68d5ddc9bb0f3f92c28e86a0675` superó:

1. `Validar CitoNauta`;
2. `Audit course completion`;
3. `Public Content Alignment`;
4. `CitoNauta Quality Gates`.

Estas comprobaciones demuestran integridad técnica y ausencia de desalineación pública. No sustituyen revisión académica especializada.

## 3. Cobertura por bloques

| Bloque | Unidades | Cobertura principal |
|---|---:|---|
| Lógica del campo | 1 | estados celulares, linaje, causalidad, modelos y métodos contemporáneos |
| Reproducción y desarrollo temprano | 2–5 | línea germinal, gametogénesis, fecundación, MZT, segmentación, implantación, gastrulación y ejes |
| Sistemas de patrón y forma | 6–7 | redes reguladoras, morfógenos, osciladores, mecánica y comportamientos celulares |
| Neurodesarrollo y organogénesis | 8–11 | sistema nervioso, cresta neural, somitas, músculo, esqueleto, corazón, sangre, vasos, riñón, órganos endodérmicos y gónadas |
| Células madre y modelos | 12 | nichos, regeneración, reprogramación, organoides, assembloids y SCBEM |
| Desarrollo humano aplicado | 13 | estadificación, placenta, interfaz materno-fetal, anomalías congénitas y teratología |
| Síntesis evolutiva | 14 | homología, redes, heterocronía, sesgo del desarrollo, plasticidad, ambiente y comparación ómica |

## 4. Solapamientos controlados

### Unidad 2 y Unidad 11

- Unidad 2: especificación de línea germinal, determinación sexual, meiosis y gametogénesis.
- Unidad 11: organogénesis gonadal, arquitectura del nicho y conductos reproductivos.

La división es funcional y evita repetir meiosis dentro de organogénesis visceral.

### Unidad 4 y Unidad 13

- Unidad 4: trofectodermo, implantación y tejidos extraembrionarios tempranos.
- Unidad 13: diferenciación placentaria posterior, vellosidades, decidua, perfusión e interfaz materno-fetal.

El solapamiento se mantiene como continuidad temporal, no como duplicación literal.

### Unidad 6 y Unidad 9

- Unidad 6: teoría de osciladores, gradientes y redes de segmentación.
- Unidad 9: implementación del reloj y frente en somitogénesis, polaridad y derivados somíticos.

La primera establece el modelo general; la segunda lo aplica a un sistema anatómico.

### Unidad 7 y unidades de organogénesis

- Unidad 7: principios transversales de fuerza, adhesión, matriz, migración y ramificación.
- Unidades 8–11: uso específico de esos principios en órganos.

Debe conservarse la referencia cruzada y reducirse cualquier repetición definicional durante la edición final.

### Unidad 12 y unidades 4–5

- Unidades 4–5: los modelos embrionarios sirven para comprender procesos concretos.
- Unidad 12: benchmarking, reproducibilidad, nomenclatura, supervisión y límites traslacionales.

Esta separación es adecuada: mecanismo primero, evaluación del modelo después.

## 5. Fortalezas verificadas

1. **Secuencia cognitiva:** pasa de evidencia y estados celulares a procesos tempranos, patrones, forma, órganos y síntesis.
2. **Causalidad explícita:** necesidad, suficiencia, rescate y función aparecen de forma transversal.
3. **Métodos modernos integrados:** single-cell, spatial, imagen viva, trazado, organoides y modelado no están aislados en una unidad metodológica decorativa.
4. **Jerarquía estadística:** se advierte repetidamente sobre células, organoides, embriones, camadas y lotes anidados.
5. **Separación biomédica:** mecanismo experimental, asociación humana, riesgo poblacional y decisión clínica se mantienen diferenciados.
6. **Comparación responsable:** especies y modelos se comparan por estadio, anatomía y validez, no por equivalencia automática.
7. **Ética distribuida:** material humano, SCBEM, reproducción, teratología y variación humana incluyen límites explícitos.

## 6. Brechas y tareas antes de producción

### 6.1 DOHaD

`course.json` incluye DOHaD en la Unidad 13. La cobertura existe de forma distribuida mediante placenta, crecimiento, exposiciones, teratología y plasticidad ambiental entre las unidades 13 y 14, pero **no existe todavía una sección explícita y autónoma sobre Developmental Origins of Health and Disease**.

Acción requerida: incorporar una sección breve que distinga programación del desarrollo, asociación de curso de vida, mediación placentaria, causalidad epidemiológica y determinismo. Debe evitar atribución causal automática a marcas epigenéticas y culpabilización materna.

### 6.2 Epidermis y anexos

La Unidad 8 incluye borde neural, placodas y sistemas sensoriales, pero epidermis, folículos, glándulas y anexos cutáneos tienen cobertura menor que la sugerida por el `course.json`.

Acción requerida: decidir si se añade una subsección compacta en la Unidad 8 o si se elimina `epidermis` de sus temas declarados.

### 6.3 Desarrollo inmunitario

Hematopoyesis, macrófagos fetales e inmunidad placentaria están cubiertos, pero la organogénesis tímica, la colonización linfoide y la maduración del sistema inmunitario no forman un bloque específico.

Acción requerida: decidir si el alcance biomédico del curso exige una subsección dentro de la Unidad 10 o si se declara como contenido de una asignatura posterior de inmunología.

### 6.4 Desarrollo vegetal e invertebrados

La arquitectura está deliberadamente centrada en vertebrados y desarrollo humano. Invertebrados aparecen como sistemas comparativos, pero el desarrollo vegetal no se desarrolla.

Acción requerida: explicitar esta delimitación en `course.json` para no presentar el curso como cobertura universal de toda la biología del desarrollo.

### 6.5 Bibliografía

Las fuentes por unidad están incorporadas, pero el registro central contiene principalmente fuentes de arquitectura curricular.

Acción requerida:

- deduplicar DOI, PMID y URL;
- normalizar autores y años;
- separar artículos primarios, revisiones, guías y recursos;
- revisar enlaces antiguos o metadatos incompletos;
- seleccionar lecturas obligatorias y complementarias;
- verificar licencias antes de reutilizar figuras.

### 6.6 Evaluación y carga de trabajo

La ficha define actividades y porcentajes, pero aún no se ha calculado carga semanal ni se ha demostrado correspondencia completa entre cada resultado, actividad y evaluación.

Acción requerida: construir una matriz `resultado → evidencia → actividad → evaluación → criterio` y estimar horas presenciales y autónomas.

## 7. Riesgos editoriales transversales

- Repetición de advertencias como “marcador no equivale a función”. Es conceptualmente correcta, pero debe expresarse con variación y solo donde cambie la inferencia.
- Densidad alta de conceptos por unidad. La versión pública necesitará jerarquía visual y rutas de lectura básica, intermedia y avanzada.
- Algunos ejemplos cuantitativos son deliberadamente idealizados. Deben mantener rótulos claros de modelo y limitaciones.
- Las conexiones clínicas deben seguir siendo contextos de interpretación, no recomendaciones ni herramientas diagnósticas.
- Los nombres de señales y factores deben revisarse para uniformar mayúsculas, cursivas de genes y nomenclatura por especie.

## 8. Criterios de salida del espacio de reconstrucción

El curso solo podrá migrarse a producción cuando se cumplan todos los criterios siguientes:

- [x] Arquitectura curricular justificada.
- [x] Catorce unidades redactadas.
- [x] Producción aislada durante el desarrollo.
- [x] Validaciones técnicas superadas.
- [ ] Brechas DOHaD, epidermis e inmunidad resueltas o delimitadas formalmente.
- [ ] Bibliografía consolidada y verificada.
- [ ] Auditoría de repetición y progresión completada.
- [ ] Matriz de evaluación y carga de trabajo completada.
- [ ] Revisión disciplinar externa completada.
- [ ] Correcciones de revisión incorporadas.
- [ ] Plan de migración, generación y reversión documentado.

## 9. Recomendación

Mantener el PR #113 como **borrador**. La siguiente fase no debe añadir unidades nuevas, sino realizar una revisión transversal en este orden:

1. resolver brechas de alcance;
2. consolidar bibliografía;
3. reducir repetición y mejorar progresión;
4. mapear resultados y evaluación;
5. obtener revisión disciplinar;
6. migrar de forma coordinada a producción y regenerar páginas e índices.
