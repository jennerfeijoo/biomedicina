# Inventario de dependencias de numeración — Bioinstrumentación

## Objetivo

Identificar todas las superficies que dependen de la numeración actual de las unidades 4, 5 y 6 antes de ejecutar cualquier migración. Este inventario no modifica contenido académico.

## Resultado ejecutivo

La renumeración no puede limitarse a cambiar tres nombres de archivo. La numeración forma parte de:

- las fuentes académicas canónicas;
- las rutas HTML públicas;
- la navegación anterior/siguiente;
- prácticas y evaluaciones;
- autorizaciones y preparación;
- auditorías y paquetes de revisión;
- scripts y workflows específicos.

La migración debe ser atómica. El contenido digital de la Unidad 4 debe pasar a la Unidad 5; Sensores no eléctricos debe pasar de 5 a 6; Seguridad y EMC debe pasar de 6 a 7. La nueva Unidad 4 y las unidades 8–10 se incorporarán sin reescribir el contenido preservado.

## Matriz de dependencia

| Superficie | Dependencia actual | Riesgo | Política |
|---|---|---|---|
| Fuentes autorales | `unit-04.json`, `unit-05.json`, `unit-06.json` | Sobrescritura o pérdida de contenido | Crear destinos y actualizar referencias antes de retirar rutas antiguas |
| Página del curso | Lista y orden de unidades | Índice incoherente | Regenerar junto con las diez unidades |
| Índice de unidades | Rutas numéricas y títulos | Enlaces rotos o temas desordenados | Actualizar en el mismo PR |
| HTML de unidades | `unidad-04.html` a `unidad-06.html` | Cambio semántico de URLs públicas | Introducir URL canónica estable o aviso/alias de legado |
| Navegación | Botones anterior/siguiente | Saltos, ciclos o páginas inaccesibles | Validar secuencia 1–10 |
| Prácticas | Filenames e IDs U4–U6 | Evidencia vinculada al dominio equivocado | Conservar IDs estables y añadir cruce legacy/canonical |
| Evaluaciones | Filenames, criterios y feedback U4–U6 | Rúbricas aplicadas a otra unidad | Migrar por dominio, no por sustitución textual |
| Registros de fuentes | Referencias por número de unidad | Citas desconectadas | Clasificar contrato activo frente a historial |
| Auditorías y revisiones | Evidencia histórica numerada | Reescritura de la historia editorial | No renombrar; enlazar mediante crosswalk |
| Validadores | Paths y estados esperados U4–U6 | CI verde sin revisar archivos nuevos | Retirar o generalizar en la migración |
| Workflows | Filtros `paths` específicos | Omisión silenciosa de controles | Actualizar filtros o reemplazar por gate genérico |

## Dependencias activas identificadas

### Fuentes académicas

```text
data/course_redevelopment/bioinstrumentacion/units/unit-04.json
data/course_redevelopment/bioinstrumentacion/units/unit-05.json
data/course_redevelopment/bioinstrumentacion/units/unit-06.json
```

### Superficie pública

```text
ingenieria-biomedica/bioinstrumentacion/index.html
ingenieria-biomedica/bioinstrumentacion/unidades/index.html
ingenieria-biomedica/bioinstrumentacion/unidades/unidad-04.html
ingenieria-biomedica/bioinstrumentacion/unidades/unidad-05.html
ingenieria-biomedica/bioinstrumentacion/unidades/unidad-06.html
```

### Prácticas y evaluaciones

```text
data/practice_implementations/bioinstrumentacion-unit-04.json
data/practice_implementations/bioinstrumentacion-unit-05.json
data/practice_implementations/bioinstrumentacion-unit-06.json
data/assessment_implementations/bioinstrumentacion-unit-04.json
data/assessment_implementations/bioinstrumentacion-unit-05.json
data/assessment_implementations/bioinstrumentacion-unit-06.json
```

También existen artefactos relacionados bajo `unit_preparation`, `source_registry`, `assessment_authorizations`, `authoring_authorizations`, `editorial_audits`, `authoral_audits`, `final_authoral_audits`, `review_protocols`, `review_packets`, `review_handoffs` y `docs/pilots/bioinstrumentacion/`.

## Hallazgo crítico: colisión de URL pública

La URL numérica `unidad-04.html` identifica actualmente el contenido digital que deberá ocupar la posición canónica 5. Si la misma URL se reutiliza directamente para la nueva unidad analógica, un enlace o marcador previo apuntará a otro tema sin indicar la migración.

La solución recomendada es separar:

- **identidad canónica estable**, mediante slug o identificador persistente;
- **posición curricular**, mediante el campo `unit` o `sequence`;
- **referencia histórica**, mediante `legacy_unit`.

Ejemplo conceptual:

```text
canonical_id: bioinstrumentacion-adquisicion-digital
canonical_unit: 5
legacy_unit: 4
```

No se ejecutará esta modificación hasta que el generador, los enlaces y los gates estén preparados.

## Política para artefactos históricos

Los documentos de auditoría, autorizaciones, handoffs y paquetes de revisión registran decisiones tomadas cuando el contenido tenía otra numeración. No deben renombrarse masivamente ni editarse para aparentar que siempre pertenecieron a la nueva secuencia.

Se conservarán como evidencia histórica y se conectarán con:

```text
legacy_unit: 4
canonical_unit: 5
migration_id: bioinstrumentacion-numbering-v1
```

La misma regla aplica a 5→6 y 6→7.

## Política para prácticas y evaluaciones

La migración se realizará según el dominio evaluado, no mediante búsqueda y reemplazo de números.

- Las prácticas de muestreo, ADC, cuantización y sincronización pasan al dominio canónico 5.
- Las prácticas de presión, temperatura, flujo y óptica pasan al dominio canónico 6.
- Las prácticas de seguridad eléctrica y EMC pasan al dominio canónico 7.
- Los IDs internos se conservarán cuando sean estables y no ambiguos.
- Cuando el ID contenga el número antiguo, se añadirá metadata de legado antes de decidir si se renombra.
- Las evaluaciones humanas pendientes seguirán pendientes; la migración no equivale a revisión ejecutada.

## Política para automatización

La búsqueda del repositorio confirma la presencia de múltiples validadores específicos, por ejemplo:

```text
scripts/validate_bioinstrumentation_u4_*.py
scripts/validate_bioinstrumentation_u5_*.py
scripts/validate_bioinstrumentation_u6_*.py
```

No se crearán copias U7, U8, U9 y U10 de ese patrón. Durante la migración se deberá:

1. identificar qué invariantes siguen siendo útiles;
2. trasladarlas a validación genérica por esquema o curso;
3. retirar gates históricos que solo verifican una fase ya completada;
4. mantener la trazabilidad en Git y en el manifiesto de migración;
5. comprobar que los filtros de workflows incluyan las nuevas rutas.

## Secuencia de migración propuesta

1. Introducir IDs canónicos persistentes y metadata `legacy_unit` para las unidades 4–6 actuales.
2. Preparar el generador para diez unidades y rutas canónicas estables.
3. Crear la nueva Unidad 4 analógica.
4. Mover el contenido digital 4→5 sin reescritura sustantiva.
5. Mover Sensores no eléctricos 5→6.
6. Mover Seguridad y EMC 6→7.
7. Migrar prácticas y evaluaciones por dominio.
8. Crear unidades 8, 9 y 10.
9. Regenerar índice, navegación y HTML.
10. Actualizar o sustituir validadores y filtros de CI.
11. Ejecutar auditorías globales de currículo, unidades, bibliografía, redundancia, alineación pública y enlaces.
12. Mantener el curso en `review` o `pending` hasta revisión disciplinar humana documentada.

## Gates previos completados

- [x] inventariar enlaces internos y rutas públicas afectadas;
- [x] comprobar dependencias de navegación;
- [x] identificar referencias en prácticas y evaluaciones;
- [x] clasificar auditorías y revisiones como evidencia histórica;
- [x] identificar validadores y workflows sensibles a numeración;
- [x] registrar un crosswalk legible por máquina;
- [ ] diseñar el cambio del generador y la estrategia de URL canónica;
- [ ] ejecutar la migración atómica;

## Estado

```text
numbering_dependency_inventory: completed
academic_content_modified: false
migration_manifest: data/course_migrations/bioinstrumentacion-numbering-v1.json
migration_status: planned_not_executed
next_action: design_atomic_migration_plan
human_review_executed: false
disciplinary_review_complete: false
public_release_authorized: false
```
