# Política bibliográfica — Biología del Desarrollo

**Fecha:** 2026-07-27  
**Estado:** norma editorial y técnica previa a producción

## 1. Objetivo

La bibliografía debe permitir rastrear qué evidencia respalda la arquitectura, cada mecanismo, los métodos, las conexiones biomédicas y los límites éticos. El número de referencias no es una medida de calidad. Se priorizan pertinencia, trazabilidad, diversidad de evidencia, actualización y correspondencia con la afirmación curricular.

Toda fuente utilizada por una unidad debe existir en el registro canónico único:

`data/source_registry/biologia-desarrollo.json`

El CI rechaza usos locales sin entrada canónica, colisiones de identificadores, referencias ambiguas y metadatos obligatorios incompletos.

## 2. Niveles de lectura

Cada unidad deberá terminar con tres niveles claramente separados:

1. **Lectura obligatoria:** una o dos fuentes que sostengan el núcleo conceptual de la unidad y puedan discutirse de forma completa.
2. **Lectura de profundización:** revisiones, artículos primarios o atlas que amplíen mecanismos, métodos o controversias.
3. **Recurso de consulta:** atlas, bases de datos, guías, protocolos, libros o recursos visuales para resolver preguntas específicas.

Una fuente puede aparecer en varias unidades, pero debe existir una sola entrada canónica y múltiples usos curriculares explícitos.

## 3. Taxonomía normalizada

Los valores de `type` deberán converger en estas categorías:

- `official_university_syllabus`;
- `official_university_course_description`;
- `reference_textbook`;
- `open_reference_textbook`;
- `peer_reviewed_review`;
- `peer_reviewed_primary_research`;
- `primary_single_cell_atlas`;
- `primary_spatial_atlas`;
- `human_development_resource`;
- `scientific_society_education_resource`;
- `official_method_training`;
- `scientific_and_ethics_guideline`;
- `normative_guidance`;
- `database_or_atlas`;
- `protocol_or_reporting_standard`;
- `protocol_book`;
- `published_correction`.

No se normalizará un tipo cuando la fuente no permita determinarlo con seguridad. Los tipos históricos conservados en el registro deberán migrarse durante la curación editorial final, no mediante inferencia automática.

## 4. Estados de verificación

- `verified_directly`: se consultó la fuente o su página oficial suficiente para verificar el uso curricular descrito.
- `verified_metadata`: se verificaron metadatos e identidad, pero no se revisó el texto completo.
- `identified_for_future_full_review`: la referencia fue identificada y debe revisarse a texto completo.
- `consulted_uploaded_source`: el recurso suministrado fue consultado dentro del proyecto.
- `verified_with_correction`: el artículo se interpreta junto con una corrección publicada.
- `recommended_future_review`: fuente identificada pero no evaluada todavía.
- `superseded`: versión conservada por trazabilidad pero reemplazada por una fuente posterior.
- `unavailable`: referencia identificada cuyo contenido no pudo consultarse.

`verified_metadata` no autoriza atribuir conclusiones detalladas al texto completo. Los estados no se elevan automáticamente durante consolidación o promoción.

## 5. Identificadores y deduplicación

Orden de preferencia para identidad bibliográfica:

1. ID canónico o alias controlado;
2. DOI normalizado;
3. PMID;
4. identificador estable del repositorio o atlas;
5. URL canónica;
6. título normalizado más autores y año, únicamente como señal para revisión manual.

Las coincidencias de título no se fusionan automáticamente. Versiones preprint, artículo final, corrección, actualización de guía o edición de libro deben conservar relaciones explícitas.

La promoción de referencias locales agrupa únicamente componentes conectados por DOI, PMID o URL exactos y se detiene ante conflictos de título, autoría, año, tipo o estado de verificación.

## 6. Campos mínimos

Toda entrada central deberá contener:

- `id` estable y legible;
- `title`;
- `authors_or_organization`;
- `year` cuando exista;
- `type`;
- al menos un identificador estable (`doi`, `pmid`, identificador de recurso o `url`);
- `verification_status`;
- `consulted_on` cuando la fuente haya sido revisada;
- `curricular_role`;
- `limitations`;
- unidades o procedencia cuando corresponda.

Campos recomendados:

- `aliases`;
- `edition` o `version`;
- `isbn` para libros;
- `units` que utilizan la fuente;
- `reading_level`: `required`, `advanced` o `reference`;
- `license_status`;
- `notes_on_species_or_stage`;
- `source_provenance`.

## 7. Selección por unidad

Una unidad no debe depender solo de:

- un libro de texto;
- una revisión narrativa antigua;
- un atlas sin validación funcional;
- un modelo animal sin discutir especie y estadio;
- un artículo primario aislado para una afirmación general;
- una fuente clínica para establecer un mecanismo experimental.

La selección ideal combina, según corresponda:

- una fuente de síntesis;
- evidencia primaria representativa;
- un recurso metodológico o atlas;
- una guía ética o normativa cuando el tema lo requiera.

## 8. Actualización y obsolescencia

No se eliminarán automáticamente fuentes clásicas si su función es histórica o experimental. Deben marcarse sus límites y acompañarse de evidencia contemporánea cuando el mecanismo, método o nomenclatura haya cambiado.

Recursos dinámicos como Human Cell Atlas, HDBR, ISSCR y cursos metodológicos deberán registrar fecha de consulta y versión cuando exista.

Correcciones, retractaciones y actualizaciones editoriales deben vincularse con el registro afectado y revisarse antes de reutilizar datos o conclusiones.

## 9. Figuras y licencias

La inclusión de una referencia no autoriza reutilizar sus figuras.

Antes de incorporar una figura, esquema o captura se deberá registrar:

- licencia aplicable;
- atribución requerida;
- posibilidad de modificación;
- restricciones comerciales;
- versión consultada;
- alternativa de recreación original basada en datos.

Cuando la licencia no sea clara, la figura no se reutiliza. Puede citarse la fuente y crear una visualización original que no copie composición ni elementos protegidos.

## 10. Automatización obligatoria

### `scripts/audit_course_bibliography.py`

Resuelve usos locales contra el registro y distingue repeticiones canónicas de colisiones reales.

### `scripts/repair_course_redevelopment_json.py`

Valida los 14 JSON y protege las ecuaciones LaTeX frente a escapes y controles ocultos.

### `scripts/consolidate_course_source_registry.py`

Exige un registro central único y valida IDs y alias.

### `scripts/promote_unit_sources_to_registry.py`

Comprueba que todo uso bibliográfico de unidad tenga una fuente canónica.

### `Audit course bibliography`

El workflow falla ante:

- JSON inválido o LaTeX mal escapado;
- registro no consolidado;
- fuente local no registrada;
- duplicado exacto no resuelto;
- referencia ambigua;
- metadatos obligatorios incompletos.

## 11. Criterio de cierre bibliográfico

### Ingeniería registral

- [x] Las 14 unidades están inventariadas.
- [x] Existe un registro canónico único.
- [x] Los 117 usos locales se resuelven contra el registro.
- [x] DOI, PMID y URL están normalizados.
- [x] Los duplicados exactos están resueltos mediante entradas canónicas.
- [x] Posibles duplicados y ambigüedad están controlados.
- [x] Las entradas obligatorias tienen metadatos mínimos.

### Curación académica

- [ ] Revisar a texto completo fuentes con verificación limitada.
- [ ] Asignar lecturas obligatorias, avanzadas y de consulta.
- [ ] Normalizar completamente tipos históricos.
- [ ] Auditar licencias de figuras y materiales.
- [ ] Confirmar suficiencia y equilibrio mediante revisión disciplinar.
