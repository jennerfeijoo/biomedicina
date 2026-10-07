# Figuras docentes en las asignaturas

Primera entrega: seis figuras originales para Desarrollo de Dispositivos Médicos, una por unidad. SVG accesible, texto alternativo, pie explicativo, licencia CC BY-NC 4.0 y referencias documentales. Son síntesis docentes, no reproducciones de figuras institucionales ni evidencia experimental.

## Contenido

1. Observación, interpretación, actores, entorno y formulación de necesidades.
2. Trazabilidad entre necesidades, requisitos, arquitectura, verificación y validación.
3. Peligros, riesgo, prioridad de controles y riesgo residual.
4. Configuración, método, criterio y evidencia de verificación.
5. Diferencias entre verificación y validación y límites de los ensayos de banco.
6. Retroalimentación entre diseño, producción, información posmercado y cambios.

## Integración

El registro canónico `media.json` vincula cada figura completa a una unidad y un tema mediante `unit_id`, `topic_id` y `media_ids`. El renderizador inserta la figura junto al texto del tema, ofrece ampliación al SVG original, reserva su relación de aspecto y usa carga diferida. Los registros planificados no crean imágenes vacías.

Para nuevas figuras se requieren archivo local en `assets/figures/`, título, texto alternativo, pie, dimensiones, atribución, licencia y fuentes válidas. El validador comprueba estos datos y la correspondencia con unidad y tema. El generador reproducible es `scripts/build_device_development_figures.py`; no añade dependencias de ejecución al sitio.

El estado multimedia completo de este curso corresponde a sus seis recursos planificados. No cambia los estados de revisión científica. Los otros cursos mantienen su estado y quedan 122 recursos multimedia planificados en el corpus canónico.

## Comprobaciones

Inspección visual de las seis figuras renderizadas; pruebas de inserción en las seis páginas, accesibilidad básica y fuentes; exclusión de medios planificados y rutas de archivo no admitidas; control completo del repositorio y regeneración determinista.
