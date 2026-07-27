# Biología Sintética — fuente canónica

Este directorio contiene la reconstrucción académica canónica de **Biología Sintética**.

## Arquitectura

El curso se organiza en ocho unidades acumulativas:

1. diseño de sistemas biológicos y ciclo DBTL;
2. partes, expresión y contexto celular;
3. circuitos, dinámica y comportamiento poblacional;
4. modelado, identificabilidad y control;
5. construcción conceptual, edición y verificación;
6. ingeniería metabólica y bioproducción;
7. aplicaciones biomédicas y validación traslacional;
8. biocontención, bioseguridad y gobernanza responsable.

## Contrato editorial

- `course.json` define arquitectura, evaluación, proyecto y recursos centrales.
- `units/unit-XX.json` constituye la fuente lectiva.
- `scripts/publish_courses.py` sincroniza descriptor, unidades públicas y overlay editorial.
- El estado permanece en `review` hasta documentar revisión disciplinar externa.

## Límite de seguridad

Las actividades son analíticas, computacionales o conceptuales. El curso no incluye secuencias, protocolos operativos, condiciones de cultivo o transformación, optimización de liberación, evasión de salvaguardas ni recomendaciones clínicas.

## Cambios futuros

Toda modificación debe conservar trazabilidad bibliográfica, ausencia de párrafos duplicados, evaluación alineada con resultados, límites de inferencia y sincronización entre fuente, JSON generado y páginas públicas.
