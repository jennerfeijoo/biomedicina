# Catálogo editorial de investigación biomédica

`data/research_catalog.json` almacena publicaciones científicas que pueden mostrarse en la portada de CitoNauta y, más adelante, en una biblioteca de investigación independiente.

## Principio editorial

Una publicación no se incorpora solo por ser reciente. Debe poder verificarse, clasificarse y conectarse con el currículo sin confundir novedad, calidad metodológica, significancia estadística, mecanismo biológico o utilidad clínica.

## Campos obligatorios por artículo

- `id`: identificador estable y legible.
- `title`: título de la publicación.
- `summary`: síntesis editorial original.
- `publication_date`: fecha de publicación en formato ISO.
- `source_url`: DOI, página de la revista o repositorio primario.
- `evidence_type`: categoría general de evidencia.
- `study_design`: diseño del estudio.
- `topic_tags`: temas biomédicos y computacionales.
- `subject_ids`: asignaturas necesarias o directamente relacionadas.
- `track_ids`: rutas interdisciplinarias relacionadas.
- `methods`: técnicas experimentales, clínicas o computacionales.
- `key_findings`: hallazgos principales, expresados sin exageración.
- `limitations`: límites declarados o detectados durante la revisión.
- `review_status`: estado editorial dentro de CitoNauta.
- `verified_at`: fecha de la última verificación.

## Campos recomendados

- `journal`
- `authors`
- `doi`
- `population`
- `sample_size`
- `comparators`
- `outcomes`
- `clinical_relevance`
- `data_code_availability`
- `conflicts_of_interest`
- `editorial_notes`

## Estados editoriales

- `candidate`: publicación identificada, todavía sin revisión.
- `screened`: metadatos y pertinencia revisados.
- `verified`: fuente, diseño, hallazgos y limitaciones comprobados.
- `updated`: registro revisado después de nueva evidencia, corrección o seguimiento.
- `archived`: se conserva por valor histórico, pero ya no representa el estado actual de la evidencia.

## Relación con asignaturas

`subject_ids` debe utilizar los identificadores del currículo principal o de `data/provisional_subjects.json`. La relación debe responder al menos a una de estas funciones:

1. aporta fundamentos para comprender el artículo;
2. explica el mecanismo biológico estudiado;
3. aporta el método experimental o computacional;
4. permite evaluar el diseño y la inferencia;
5. contextualiza la aplicación, regulación o impacto.

## Relación con rutas

`track_ids` debe utilizar los identificadores de `data/tracks.json`. Una publicación puede pertenecer a varias rutas cuando integra escalas, métodos o aplicaciones diferentes.

## Reglas de calidad

- Priorizar fuentes primarias y documentación oficial.
- Separar claramente hallazgo, interpretación e inferencia.
- No presentar asociación como causalidad.
- No equiparar desempeño técnico con utilidad clínica.
- Registrar validación externa, subgrupos, calibración, sesgo y seguridad cuando se trate de IA clínica.
- Registrar muestra, fase preanalítica, validación analítica, validación clínica y utilidad cuando se trate de biomarcadores.
- Mantener fecha de verificación y archivar registros desactualizados.
