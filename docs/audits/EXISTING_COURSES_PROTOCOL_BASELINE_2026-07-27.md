# Línea base de auditoría de asignaturas existentes

**Fecha:** 2026-07-27  
**Rama:** `audit/validate-existing-courses-2026-07`  
**PR:** #114  
**Protocolo:** `docs/ACADEMIC_CONTENT_DEVELOPMENT_PROTOCOL.md`

## 1. Propósito

Esta línea base determina qué evidencia curricular, técnica y editorial existe para las 84 asignaturas del repositorio. No certifica validez académica automática. Distingue:

- presencia en catálogo;
- desarrollo real de unidades;
- arquitectura pedagógica observable;
- artefactos mínimos del protocolo;
- registro de revisión;
- sincronización entre reconstrucción y publicación;
- especificidad del contenido entre asignaturas.

## 2. Resultado global

- Asignaturas inventariadas: **84**.
- Asignaturas con todas sus unidades desarrolladas o autorales: **27**.
- Asignaturas con desarrollo parcial: **2**.
- Asignaturas equivalentes a catálogo, placeholder o contenido de respaldo: **55**.
- Asignaturas con los diez artefactos mínimos y publicación sincronizada: **0**.
- Asignaturas con errores técnicos de lectura JSON: **0**.
- Asignaturas con discrepancias entre estado declarado y evidencia observable: **57**.

### Bandas actuales

| Banda | Cantidad | Interpretación |
|---|---:|---|
| `content_present_protocol_incomplete` | 27 | Existe contenido sustantivo, pero faltan artefactos, revisión o sincronización |
| `partial_development` | 2 | Solo una parte de las unidades está realmente desarrollada |
| `catalog_or_placeholder` | 55 | El curso está catalogado o renderizado con contenido de respaldo |

Ninguna banda equivale a validación disciplinar.

## 3. Artefactos ausentes

| Artefacto del protocolo | Asignaturas sin evidencia identificada |
|---|---:|
| Registro de revisión | 83 antes del primer dictamen; Biología I ya dispone de registro interno con cambios requeridos |
| Decisión de arquitectura | 82 después de documentar Biología I y Biología del Desarrollo |
| Registro de fuentes | 82 después de documentar Biología I y Biología del Desarrollo |
| Prácticas y evaluaciones identificables | 58 |
| Unidades completas | 57 |
| Ficha curricular sustantiva | 56 |
| Criterios de dominio | 56 |
| Matriz de cobertura | 55 |
| Sincronización pública de reconstrucciones | 1 |

Los recuentos cambian conforme se incorporan artefactos en el PR #114. El workflow genera la cifra vigente en cada commit.

## 4. Asignaturas desarrolladas pero incompletas según protocolo

### Biología del Desarrollo

- Reconstrucción: 14 unidades.
- Catálogo y publicación: 6 unidades.
- Estado: contenido reconstruido y auditado, **migración pública pendiente**.
- Brechas observables: sincronización pública y representación integrada de prácticas/evaluaciones en la ficha canónica.

### Biología I

- Seis unidades desarrolladas.
- Registro de fuentes y decisión curricular añadidos durante esta auditoría.
- Dictamen interno: **no validada; cambios requeridos**.
- Bloqueantes: Unidad 7 inexistente en la expansión, solapamiento con Biología II y texto excesivamente plantillado.

### Otras 25 asignaturas completas en unidades

Presentan unidades desarrolladas, pero carecen como mínimo de decisión curricular, registro canónico de fuentes y revisión documentada. Incluyen:

- Biología Celular y Tisular;
- Biología II;
- Biología Molecular;
- Biología Molecular y Celular Aplicada;
- Biología Sintética;
- Bioquímica;
- Fisiología Humana II;
- Fisiopatología Humana;
- Genética;
- Bioestadística;
- Biofísica;
- Álgebra;
- Cálculo;
- Ampliación de Cálculo;
- Ecuaciones Diferenciales;
- Física I y II;
- Química I y II;
- Probabilidad y Estadística;
- Métodos Numéricos;
- Fundamentos de Programación;
- Algoritmos y Estructuras de Datos;
- Arquitectura de Computadores;
- Bases de Datos.

La presencia de seis o más JSON avanzados no demuestra que el alcance, el número de unidades o las fuentes sean adecuados.

## 5. Desarrollo parcial

### Fisiología Humana I

- Dos de seis unidades desarrolladas.
- Cuatro unidades de respaldo.
- Estado declarado `generated`, incompatible con el desarrollo real.
- Requiere delimitar alcance, justificar arquitectura y reconstruir las cuatro unidades faltantes.

### Bioinformática

- Una de seis unidades desarrollada.
- Cinco unidades de respaldo.
- Carece de matriz de cobertura, decisión, fuentes, criterios de dominio y revisión.
- Su importancia para el proyecto Citonauta exige auditoría temprana.

## 6. Sincronización reconstrucción–publicación

El auditor separa el paquete académico de la publicación. Actualmente existe un paquete formal de reconstrucción:

| Asignatura | Reconstrucción | Catálogo | JSON públicos | Páginas públicas | Estado |
|---|---:|---:|---:|---:|---|
| Biología del Desarrollo | 14 | 6 | 6 | 6 | `migration_pending` |

La igualdad de recuentos sería necesaria, pero no suficiente: después de migrar deberá comprobarse equivalencia semántica, navegación, referencias y reversión.

## 7. Especificidad entre asignaturas

La auditoría examinó:

- **28 asignaturas** con unidades JSON;
- **7.325 bloques pedagógicos**.

Resultados:

- 0 grupos exactos compartidos entre asignaturas;
- 1 par casi duplicado: ejercicio de acoplamiento de energía libre en Biología I y Química II;
- 1 frase recurrente en cuatro asignaturas: “no identifica por sí sola el mecanismo”.

No se concluye plagio ni duplicación masiva. El principal riesgo editorial es la repetición de plantillas dentro de una misma asignatura, observada claramente en Biología I.

## 8. Límites del resultado

La línea base puede demostrar:

- existencia y legibilidad de archivos;
- proporción de unidades desarrolladas;
- presencia de componentes pedagógicos;
- disponibilidad de fuentes y decisiones;
- discrepancias de estado;
- candidatos de redundancia;
- desfases de publicación.

No puede demostrar:

- suficiencia disciplinar;
- actualidad real de cada fuente;
- claridad para estudiantes;
- viabilidad de carga;
- calidad de rúbricas;
- validez clínica;
- autorización de uso de figuras;
- preparación para acreditación.

## 9. Veredicto de línea base

El repositorio tiene una infraestructura técnica extensa, pero la mayoría de las asignaturas no fue construida conforme al protocolo académico vigente. Las 27 asignaturas con contenido desarrollado deben considerarse **material de revisión**, no cursos validados.

La estrategia correcta es auditar por lotes, comenzando por cursos fundacionales, biomédicos centrales y asignaturas parcialmente desarrolladas. Las 55 asignaturas de catálogo no deben completarse mediante expansión automática antes de delimitar cada disciplina.