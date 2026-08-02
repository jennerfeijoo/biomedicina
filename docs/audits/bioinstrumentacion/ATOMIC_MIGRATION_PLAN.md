# Plan de migración atómica — Bioinstrumentación

## Alcance

Este plan define cómo pasar de seis unidades autorales numeradas a una arquitectura canónica de diez unidades sin perder contenido, romper la navegación pública ni reescribir evidencia histórica.

## Decisión de identidad

La posición curricular y la identidad del contenido deben separarse.

Cada unidad deberá disponer de:

```text
canonical_id
canonical_unit
legacy_unit (cuando exista)
slug
migration_id
```

La posición `canonical_unit` podrá cambiar en futuras revisiones sin alterar el identificador estable del dominio.

## Mapa de migración

| Origen | Destino | Acción |
|---|---:|---|
| Unidad 1 | 1 | Conservar |
| Unidad 2 | 2 | Conservar |
| Unidad 3 | 3 | Conservar |
| Nueva | 4 | Crear acondicionamiento analógico |
| Unidad 4 | 5 | Migrar adquisición digital sin reescritura sustantiva |
| Unidad 5 | 6 | Migrar sensores no eléctricos |
| Unidad 6 | 7 | Migrar seguridad eléctrica y EMC |
| Nueva | 8 | Crear caracterización, calibración e incertidumbre |
| Nueva | 9 | Crear verificación, validación y riesgo |
| Nueva | 10 | Crear integración y expediente reproducible |

## Estrategia de URL

Las rutas numéricas actuales no son suficientemente estables para una renumeración. La migración deberá introducir rutas canónicas basadas en slug para las unidades desplazadas y mantener páginas numéricas como capa de compatibilidad cuando el generador lo permita.

Objetivo conceptual:

```text
/unidades/adquisicion-digital.html
/unidades/sensores-no-electricos.html
/unidades/seguridad-electrica-emc.html
```

Las rutas numéricas se mantendrán únicamente como navegación curricular o alias controlado. No se debe cambiar silenciosamente el tema servido por una URL histórica sin aviso de migración.

## Fases dentro de un único PR de migración

### 1. Preparación estructural

- añadir soporte de `canonical_id`, `canonical_unit`, `legacy_unit` y `slug`;
- actualizar el generador para ordenar por `canonical_unit`;
- permitir rutas canónicas estables;
- preparar alias o páginas de transición;
- ampliar validación genérica para comprobar unicidad y continuidad 1–10.

### 2. Destinos antes que orígenes

- crear la nueva Unidad 4;
- crear destinos canónicos 5, 6 y 7 con el contenido preservado;
- verificar títulos, IDs, referencias y bibliografía;
- no retirar todavía las fuentes antiguas.

### 3. Contratos asociados

- migrar prácticas y evaluaciones por dominio;
- conservar IDs internos estables;
- añadir metadata `legacy_unit` cuando el filename o ID histórico no se cambie;
- mantener estados humanos pendientes;
- clasificar registros de fuentes y preparación como activos o históricos.

### 4. Nuevas unidades finales

- crear unidades 8, 9 y 10;
- añadir prácticas, evaluaciones, feedback, recuperación y bibliografía;
- mantener límites regulatorios, clínicos y de seguridad.

### 5. Publicación sincronizada

- regenerar página del curso;
- regenerar índice de unidades;
- generar diez páginas canónicas;
- actualizar navegación anterior/siguiente;
- actualizar mapa curricular y catálogo si consumen la secuencia;
- verificar enlaces internos y externos.

### 6. Automatización

- ejecutar validadores genéricos;
- revisar todos los `paths` de workflows;
- retirar o archivar validadores específicos que ya solo prueben fases históricas;
- no crear una nueva familia de validadores U7–U10.

### 7. Retirada controlada

Solo después de que los destinos y aliases sean válidos:

- retirar fuentes activas duplicadas;
- conservar auditorías y revisiones históricas;
- registrar la migración como ejecutada;
- regenerar informes de completitud y alineación pública.

## Condiciones de rollback

La migración debe revertirse completa si ocurre cualquiera de estos casos:

- falta una unidad canónica entre 1 y 10;
- una práctica o evaluación queda asociada al dominio equivocado;
- un enlace público de unidad queda roto;
- la navegación no es continua;
- un workflow deja de ejecutarse por un filtro de paths obsoleto;
- una auditoría histórica se sobrescribe;
- el curso se promueve a `complete` sin revisión disciplinar documentada.

## Gates de aceptación

```text
canonical_units == 10
canonical_ids_unique == true
canonical_sequence_contiguous == true
public_pages_synchronized == true
broken_internal_links == 0
legacy_crosswalk_complete == true
historical_audits_preserved == true
practice_domain_alignment == true
assessment_domain_alignment == true
human_review_executed == false
academic_status in [pending, review]
```

## Estado

```text
atomic_migration_plan: completed
migration_executed: false
academic_content_modified: false
next_action: implement_migration_in_single_integrated_pr
```
