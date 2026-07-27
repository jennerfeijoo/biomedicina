# Descriptores avanzados de asignaturas

Esta carpeta contiene los descriptores académicos generados que consumen los renderers y las auditorías de CitoNauta.

## Fuente y sincronización

- Los cursos reconstruidos se editan en `data/course_redevelopment/<subject_id>/course.json`.
- `scripts/publish_courses.py` promueve los campos públicos y académicos a esta carpeta.
- Las unidades lectivas se conservan por separado en `data/generated_units/<subject_id>/`.
- Los descriptores con estado `review` no implican revisión disciplinar externa ni acreditación.

## Regla editorial

No se deben editar manualmente campos que proceden de un paquete `course_redevelopment`. Después de modificar una fuente canónica, se debe ejecutar el publicador, regenerar las páginas afectadas y comprobar la alineación pública.
