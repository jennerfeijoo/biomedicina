# CitoNauta: Explorando la Biomedicina

CitoNauta es una plataforma educativa abierta para explorar ciencias básicas, biología, medicina, ingeniería biomédica y sus dimensiones éticas y sociales.

> Explorar la vida desde dentro, con los ojos del conocimiento.

## Estado del catálogo

- 94 asignaturas en cuatro áreas académicas.
- 44 desarrolladas con contenido lectivo sustantivo.
- 50 pendientes que todavía dependen total o parcialmente de contenido de respaldo.
- 0 con revisión disciplinar completa.
- Ninguna asignatura tiene estado editorial `complete`.

Una página navegable o un workflow verde demuestra integridad técnica, no revisión académica externa. Las asignaturas desarrolladas permanecen en `review` hasta que exista revisión disciplinar documentada.

## Fuentes del sitio

El contenido se genera de forma reproducible a partir de:

- `data/citonauta_curriculum.json`;
- `data/course_outlines.json`;
- `data/catalog_statuses.json`;
- `data/subjects/`;
- `data/generated_courses/`;
- `data/generated_units/`;
- paquetes especializados bajo `data/course_redevelopment/`.

El HTML público es una salida generada y no debe mantenerse como una segunda fuente académica independiente.

## Modelo de aprendizaje

CitoNauta organiza prerrequisitos, conceptos, actividades, evidencias y criterios de dominio sin imponer una duración universal. Cada persona avanza según su base previa, profundidad requerida y resultados demostrados.

El material es educativo. No sustituye programas oficiales, supervisión competente, revisión profesional ni certificación.

## Generación y validación

```bash
python scripts/validate_curriculum.py
python scripts/validate_course_plan_packages.py
python scripts/validate_pilot_foundations.py
python scripts/validate_generated_units.py
python scripts/audit_curriculum_completeness.py
python scripts/generate_site.py --force --with-units
python scripts/check_generated_preview.py --limit 94
python scripts/audit_public_unit_alignment.py --strict
python scripts/validate_links.py --quiet
```

Los controles verifican estructura, trazabilidad, cobertura, bibliografía, sincronización pública y enlaces. No promueven automáticamente una asignatura a `complete`.

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
- mantener `review` hasta una revisión disciplinar real.

## Tecnologías

- HTML5 y CSS propio;
- JavaScript progresivo;
- Python para generación y auditoría;
- GitHub Actions para controles reproducibles;
- GitHub Pages para publicación.

## Licencia

El proyecto se distribuye bajo Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0).
