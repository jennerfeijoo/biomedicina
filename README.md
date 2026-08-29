# CitoNauta: Explorando la Biomedicina

CitoNauta es una plataforma educativa abierta para explorar ciencias básicas, biología, medicina, ingeniería biomédica y sus dimensiones éticas y sociales.

> Explorar la vida desde dentro, con los ojos del conocimiento.

## Estado del catálogo

- 94 asignaturas en cuatro áreas académicas.
- 94 con material lectivo y actividades disponibles.
- 21 conservan marcadores de plantilla en 119 unidades y requieren reconstrucción disciplinar.
- 73 no contienen esos marcadores conocidos; esto no equivale a validación científica.
- 0 con registro completo de afirmaciones y localizadores.
- 0 con revisión IA validada para un alcance científico.
- Ninguna asignatura tiene estado editorial `complete`.

Una página navegable o un workflow verde demuestra integridad técnica, no validez científica. Las asignaturas permanecen en `review` hasta que sus afirmaciones estén trazadas y el sistema revisor haya demostrado validez para el alcance correspondiente.

## Fuentes del sitio

El contenido se genera de forma reproducible a partir de:

- `data/courses/`, fuente académica canónica para las asignaturas migradas;
- `data/citonauta_curriculum.json`;
- `data/course_outlines.json`;
- `data/catalog_statuses.json`;
- `data/subjects/`;
- `data/generated_courses/`;
- `data/generated_units/`;
- paquetes especializados bajo `data/course_redevelopment/`.

Cuando existe `data/courses/<course_id>/course.json`, esa carpeta tiene prioridad
sobre los archivos heredados. El HTML público y `data/generated_*` son salidas o
espejos de compatibilidad y no deben mantenerse como fuentes académicas
independientes. Consulte [el modelo académico canónico](docs/academic-content-model.md).

## Modelo de aprendizaje

CitoNauta organiza prerrequisitos, conceptos, actividades, evidencias y criterios de dominio sin imponer una duración universal. Cada persona avanza según su base previa, profundidad requerida y resultados demostrados.

El material es educativo. No sustituye programas oficiales, supervisión competente, revisión profesional ni certificación.

## Generación y validación

```bash
python scripts/complete_catalog_content.py --close-existing-partials
python scripts/publish_courses.py --all
python scripts/validate_curriculum.py
python scripts/validate_course_plan_packages.py
python scripts/validate_pilot_foundations.py
python scripts/validate_academic_courses.py
python scripts/validate_generated_units.py
python scripts/audit_course_readiness.py --strict
python scripts/audit_curriculum_completeness.py
python scripts/audit_course_portfolio.py --strict
python scripts/audit_generic_content.py
python scripts/validate_scientific_traceability.py
python scripts/validate_reviewer_validations.py
python -m unittest discover -s tests
python scripts/generate_site.py --force --with-units
python scripts/check_generated_preview.py --limit 94
python scripts/audit_public_unit_alignment.py --strict
python scripts/validate_links.py --quiet
```

Los controles verifican estructura, trazabilidad, cobertura, bibliografía, diversidad textual, actividades, sincronización pública y enlaces. No promueven automáticamente una asignatura a `complete`.

## Estructura

| Área | Directorio |
|---|---|
| Ciencias Básicas | `/ciencias-basicas/` |
| Biológicas y Médicas | `/biologicas-medicas/` |
| Ingeniería Biomédica Aplicada | `/ingenieria-biomedica/` |
| Gestión, Ética y Comunicación | `/gestion-etica-comunicacion/` |
| Investigación y Divulgación | `/investigacion/` |

## Contribuciones

Las contribuciones deben:

- usar fuentes verificables y registrar su procedencia;
- distinguir observación, asociación, predicción, causalidad y utilidad;
- conservar datos, código, parámetros y versiones cuando corresponda;
- evitar texto genérico y referencias decorativas;
- mantener `review` hasta una revisión documentada por un sistema validado para el alcance.

## Tecnologías

- HTML5 y CSS propio;
- JavaScript progresivo;
- Python para generación y auditoría;
- GitHub Actions para controles reproducibles;
- GitHub Pages para publicación.

## Licencia

El contenido original del proyecto se distribuye bajo Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0). Los materiales de terceros conservan sus propias condiciones y no quedan relicenciados por su inclusión como referencia.
