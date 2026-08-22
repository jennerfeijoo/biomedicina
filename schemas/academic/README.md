# Esquema académico canónico

`data/courses/<course_id>/` es la fuente de autoría para las asignaturas migradas.
El HTML público y los archivos bajo `data/generated_*` son salidas o espejos de
compatibilidad y no deben editarse como una segunda fuente académica.

La versión 1.0 separa:

- identidad, alcance, competencias y resultados del curso (`course.json`);
- temas, subtemas y bloques tipados de cada unidad (`units/*.json`);
- instrumentos y claves de respuesta (`assessments/*.json`);
- glosario, fuentes, afirmaciones y medios (`*.json` en la raíz del curso).

Los identificadores son estables y no dependen del título visible. Los estados
son multidimensionales para no confundir publicación técnica con validación
académica. Ejecute `python scripts/validate_academic_courses.py` antes de publicar.

