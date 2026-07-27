# Política bibliográfica — Biología del Desarrollo

**Fecha:** 2026-07-27  
**Estado:** norma editorial para la consolidación previa a producción

## 1. Objetivo

La bibliografía debe permitir rastrear qué evidencia respalda la arquitectura, cada mecanismo, los métodos, las conexiones biomédicas y los límites éticos. El número de referencias no es una medida de calidad. Se priorizan pertinencia, trazabilidad, diversidad de evidencia, actualización y correspondencia con la afirmación curricular.

## 2. Niveles de lectura

Cada unidad deberá terminar con tres niveles claramente separados:

1. **Lectura obligatoria:** una o dos fuentes que sostengan el núcleo conceptual de la unidad y puedan discutirse de forma completa.
2. **Lectura de profundización:** revisiones, artículos primarios o atlas que amplíen mecanismos, métodos o controversias.
3. **Recurso de consulta:** atlas, bases de datos, guías, protocolos, libros o recursos visuales para resolver preguntas específicas.

Una fuente puede aparecer en varias unidades, pero debe existir una sola entrada canónica en el registro central y múltiples usos curriculares explícitos.

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
- `protocol_or_reporting_standard`.

No se normalizará un tipo cuando la fuente no permita determinarlo con seguridad.

## 4. Estados de verificación

- `verified_directly`: se consultó la fuente o su página oficial suficiente para verificar el uso curricular descrito.
- `verified_metadata`: se verificaron metadatos e identidad, pero no se revisó el texto completo.
- `recommended_future_review`: fuente identificada pero no evaluada todavía.
- `superseded`: versión conservada por trazabilidad pero reemplazada por una fuente posterior.
- `unavailable`: referencia identificada cuyo contenido no pudo consultarse.

`verified_metadata` no autoriza atribuir conclusiones detalladas al texto completo.

## 5. Identificadores y deduplicación

Orden de preferencia para identidad bibliográfica:

1. DOI normalizado;
2. PMID;
3. identificador estable del repositorio o atlas;
4. URL canónica;
5. título normalizado más autores y año, únicamente como señal para revisión manual.

Las coincidencias de título no se fusionarán automáticamente. Versiones preprint, artículo final, corrección, actualización de guía o edición de libro deben conservar relaciones explícitas.

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
- `limitations`.

Campos recomendados:

- `edition` o `version`;
- `isbn` para libros;
- `units` que utilizan la fuente;
- `reading_level`: `required`, `advanced` o `reference`;
- `license_status`;
- `notes_on_species_or_stage`.

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

## 10. Criterio de cierre bibliográfico

La consolidación se considerará completa cuando:

- las 14 unidades estén inventariadas;
- DOI, PMID y URL estén normalizados;
- los duplicados exactos estén resueltos mediante una entrada canónica;
- posibles duplicados de título estén revisados manualmente;
- todas las entradas obligatorias tengan metadatos mínimos;
- cada unidad tenga lecturas obligatorias, avanzadas y de consulta;
- las licencias de cualquier figura prevista estén verificadas;
- un revisor disciplinar confirme suficiencia y equilibrio de fuentes.
