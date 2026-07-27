# Auditoría bibliográfica — Biología del Desarrollo

**Fecha:** 2026-07-27  
**Estado:** consolidación e integridad registral completadas; curación académica final pendiente  
**Rama:** `agent/biologia-desarrollo-evidence-based`  
**PR:** #113

## 1. Veredicto

La bibliografía del espacio de reconstrucción está consolidada en un único registro canónico:

`data/source_registry/biologia-desarrollo.json`

Las 14 unidades contienen 117 usos bibliográficos. Todos se resuelven contra una fuente canónica mediante ID, alias, DOI, PMID o URL normalizada. No quedan registros suplementarios, colisiones exactas sin resolver, referencias ambiguas ni campos obligatorios ausentes después de la resolución canónica.

Este resultado demuestra **integridad registral y trazabilidad técnica**. No demuestra que todas las fuentes hayan sido revisadas a texto completo, que la selección de lecturas sea pedagógicamente óptima ni que exista permiso para reutilizar sus figuras.

## 2. Resultados cuantitativos

| Métrica | Resultado |
|---|---:|
| Fuentes canónicas | 109 |
| Usos bibliográficos en unidades | 117 |
| Usos resueltos contra el registro | 117 |
| Usos sin registro canónico | 0 |
| Unidades con fuentes | 14 de 14 |
| Registros centrales activos | 1 |
| Identificadores exactos únicos | 166 |
| Grupos de uso repetido resueltos | 159 |
| Grupos duplicados exactos no resueltos | 0 |
| Posibles duplicados por título | 0 |
| Referencias ambiguas | 0 |
| Ocurrencias incompletas tras resolución | 0 |

Los 159 grupos resueltos no representan 159 fuentes duplicadas. El auditor agrupa por identificador, por lo que una misma fuente puede formar grupos separados por DOI, PMID y URL. Estos grupos representan usos locales correctamente vinculados con su entrada canónica.

## 3. Distribución de usos por unidad

| Unidad | Usos bibliográficos |
|---:|---:|
| 1 | 8 |
| 2 | 6 |
| 3 | 7 |
| 4 | 8 |
| 5 | 7 |
| 6 | 9 |
| 7 | 7 |
| 8 | 10 |
| 9 | 9 |
| 10 | 10 |
| 11 | 8 |
| 12 | 8 |
| 13 | 11 |
| 14 | 9 |

El número de fuentes no se interpreta como medida de calidad o dificultad. La suficiencia depende de la relación entre afirmación, tipo de evidencia, actualidad, sistema experimental y función curricular.

## 4. Consolidación realizada

### 4.1 Registro único

Se fusionaron los antiguos registros suplementarios de alcance y de fuentes de unidades dentro de `biologia-desarrollo.json`. La consolidación valida:

- unicidad de IDs canónicos;
- ausencia de colisiones entre IDs y alias;
- recuento declarado de fuentes;
- eliminación de registros suplementarios;
- preservación de estados de verificación y limitaciones.

### 4.2 Promoción de referencias locales

Las referencias que solo existían dentro de una unidad se promovieron al registro canónico mediante agrupación conectada por DOI, PMID y URL. La promoción rechaza automáticamente conflictos de:

- título normalizado;
- autoría u organización;
- año;
- tipo de fuente;
- estado de verificación.

Las unidades no se reescribieron. Mantienen sus citas locales y el auditor las resuelve contra el registro canónico.

### 4.3 Alias controlados

Cuando una misma fuente tenía IDs locales distintos, se conservó un ID canónico y se registraron alias. Por ejemplo, las dos referencias locales al modelo organizador de Martyn de 2018 se resuelven contra una sola entrada.

## 5. Reparación técnica detectada durante la auditoría

El primer inventario reveló que las unidades 1–7 y 14 contenían JSON inválido o ecuaciones LaTeX dañadas por barras invertidas no escapadas. Los validadores anteriores no analizaban todos los JSON del espacio de reconstrucción.

Se corrigieron:

- escapes JSON inválidos en campos `latex`;
- secuencias JSON válidas pero semánticamente incorrectas como `\frac`, `\nabla` o `\tau` interpretadas como controles;
- objetos finales sin llave de cierre en algunas listas;
- validación de los 14 archivos mediante `json.loads`;
- rechazo de caracteres de control dentro de ecuaciones decodificadas.

El workflow bibliográfico exige desde entonces que el reparador no detecte cambios pendientes.

## 6. Automatización incorporada

### `scripts/audit_course_bibliography.py`

- normaliza DOI, PMID y URL;
- resuelve referencias mediante ID, alias e identificadores;
- distingue usos repetidos resueltos de colisiones no resueltas;
- detecta coincidencias de título, ambigüedad y metadatos incompletos;
- produce informes JSON y Markdown.

### `scripts/repair_course_redevelopment_json.py`

- valida la sintaxis de las 14 unidades;
- normaliza escapes LaTeX;
- detecta controles ocultos;
- funciona en modo de reparación explícita o comprobación de solo lectura.

### `scripts/consolidate_course_source_registry.py`

- valida IDs y alias;
- consolida suplementos de forma determinista;
- comprueba que solo exista un registro central.

### `scripts/promote_unit_sources_to_registry.py`

- agrupa fuentes locales por identificadores conectados;
- rechaza metadatos incompatibles;
- exige que todo uso de unidad tenga una entrada canónica.

### `.github/workflows/audit-course-bibliography.yml`

El workflow falla cuando existe cualquiera de estas condiciones:

- JSON de unidad inválido o LaTeX mal escapado;
- registro no consolidado;
- uso bibliográfico de unidad sin fuente canónica;
- duplicado exacto no resuelto;
- referencia ambigua;
- metadatos obligatorios incompletos.

## 7. Trabajo bibliográfico todavía pendiente

La consolidación técnica no cierra la curación académica. Aún se requiere:

- revisar a texto completo las fuentes marcadas como `verified_metadata`, `identified_for_future_full_review` o equivalentes;
- normalizar de forma completa la taxonomía histórica de tipos de fuente;
- asignar a cada unidad lecturas obligatorias, avanzadas y de consulta;
- comprobar equilibrio entre revisiones, estudios primarios, atlas, métodos y guías;
- revisar actualidad de recursos dinámicos y registrar versiones;
- auditar licencias antes de reutilizar figuras, tablas o capturas;
- confirmar suficiencia bibliográfica mediante revisión disciplinar externa.

## 8. Criterio de salida bibliográfico

- [x] Las 14 unidades están inventariadas.
- [x] Existe un registro canónico único.
- [x] Todos los usos locales se resuelven contra el registro.
- [x] DOI, PMID y URL se normalizan automáticamente.
- [x] No existen colisiones exactas sin resolver.
- [x] No existen referencias ambiguas.
- [x] No existen metadatos obligatorios ausentes después de resolución.
- [ ] Todas las fuentes prioritarias están revisadas a texto completo.
- [ ] Cada unidad tiene lecturas obligatorias, avanzadas y de consulta aprobadas.
- [ ] Las licencias de materiales visuales previstos están verificadas.
- [ ] La suficiencia y el equilibrio reciben revisión disciplinar externa.

## 9. Recomendación

Considerar cerrada la **ingeniería de registro bibliográfico**, pero no la revisión académica de fuentes. El siguiente bloque editorial debe combinar selección de lecturas, auditoría de repetición y revisión disciplinar, manteniendo el PR como borrador y la producción sin cambios.
