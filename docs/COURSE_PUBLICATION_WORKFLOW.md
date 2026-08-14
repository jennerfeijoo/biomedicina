# Flujo reutilizable de publicación de asignaturas

## Propósito

Este documento define la transición técnica desde un paquete académico reconstruido hasta una asignatura pública. La publicación comprueba integridad y sincronización; no sustituye una revisión científicamente validada ni promueve automáticamente un curso a `complete`.

## Paquete fuente

Cada asignatura publicable debe tener esta estructura:

```text
data/course_redevelopment/<subject>/
  course.json
  units/
    unit-01.json
    unit-02.json
    ...
```

`course.json` declara `id` o `subject_id`, `area_id`, estado editorial, arquitectura, resultados, evaluación y secuencia de unidades. Los archivos de unidad son la fuente canónica del título y del contenido lectivo renderizado.

## Publicador

El comando general es:

```bash
python scripts/publish_courses.py --subject <subject>
```

Para promover todos los paquetes reconstruidos:

```bash
python scripts/publish_courses.py --all
```

Modos de comprobación:

```bash
python scripts/publish_courses.py --subject <subject> --check
python scripts/publish_courses.py --subject <subject> --check-public
```

El publicador calcula dinámicamente el área, el número de unidades y las rutas de destino. Sincroniza:

```text
data/subjects/<area>/<subject>.json
data/generated_courses/<subject>.json
data/generated_units/<subject>/unit-XX.json
<area>/<subject>/index.html
<area>/<subject>/unidades/index.html
<area>/<subject>/unidades/unidad-XX.html
```

La generación HTML se realiza con `scripts/generate_site.py` después de la promoción JSON.

## Workflow

`.github/workflows/publish-redeveloped-courses.yml` ejecuta el flujo completo en pull requests y antes de registrar cambios en `main`:

1. descubre una asignatura solicitada o todos los paquetes;
2. valida identidad, secuencia, estados y evaluación;
3. promueve overlay, descriptor avanzado y unidades;
4. valida todas las unidades avanzadas;
5. genera la página del curso, el índice y las lecciones;
6. audita alineación pública y enlaces internos;
7. comprueba el contrato público por asignatura;
8. audita cursos desarrollados y paquetes reconstruidos;
9. registra únicamente las rutas publicadas cuando el evento ocurre en `main`.

## Auditoría

El inventario se genera con:

```bash
python scripts/audit_developed_courses.py \
  --json-output developed-courses.json \
  --markdown-output developed-courses.md
```

La auditoría distingue:

- paquete fuente válido;
- promoción JSON sincronizada;
- páginas HTML sincronizadas;
- unidades avanzadas, autorales, fallback o ausentes;
- publicación técnica;
- revisión validada para el alcance.

Un curso publicado con estado `review` conserva una revisión provisional. CI solo puede convertirlo a `complete` cuando encuentra un manifiesto `validated_for_scope` vigente y exactamente coincidente.
