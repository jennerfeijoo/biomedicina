# CitoNauta: Explorando la Biomedicina

CitoNauta es una plataforma educativa y de divulgación científica abierta que invita a estudiantes,
investigadores y curiosos a explorar el universo de la biomedicina moderna, desde los fundamentos de
las ciencias básicas hasta las aplicaciones tecnológicas y éticas más actuales.

> "Explorar la vida desde dentro, con los ojos del conocimiento."

## Estado actual

- 94 asignaturas distribuidas en cuatro áreas académicas.
- 43 desarrolladas con contenido lectivo sustantivo y 51 pendientes que todavía conservan contenido de respaldo.
- 0 con revisión disciplinar completa; ninguna asignatura tiene todavía estado editorial `complete`.
- Las asignaturas desarrolladas permanecen en `review` hasta que exista revisión experta documentada.
- Una página navegable o un workflow verde no demuestra que una asignatura esté desarrollada o revisada.
- Las páginas se generan de forma reproducible desde `data/citonauta_curriculum.json`, `data/course_outlines.json`, `data/catalog_statuses.json` y los contenidos especializados de `data/subjects/` y `data/course_redevelopment/`.
- Los cursos académicos avanzados y sus unidades estructuradas se almacenan en `data/generated_courses/` y `data/generated_units/`.
- El catálogo es completo como inventario curricular, no como promesa de que las 94 asignaturas estén terminadas.

## Estado de publicación

El repositorio conserva temporalmente dos capas de contenido:

1. HTML estático generado para cursos y páginas individuales de unidad.
2. Unidades académicas avanzadas en JSON que pueden enriquecer la página del curso en el navegador.

La presencia de una unidad avanzada no demuestra por sí sola que su página individual ya publique el mismo contenido. El comando siguiente audita esa alineación y produce un inventario reproducible de páginas ausentes, genéricas o desincronizadas:

```bash
python scripts/audit_public_unit_alignment.py
```

El modo estricto está reservado para cuando la migración a una fuente única de verdad haya finalizado:

```bash
python scripts/audit_public_unit_alignment.py --strict
```

GitHub Actions ejecuta la auditoría informativa y conserva el informe como artefacto. Mientras existan discrepancias, el estado académico debe permanecer en `review` o `generated`, nunca en `complete`.

## Modelo de aprendizaje autogestionado

CitoNauta organiza contenidos, prerrequisitos, actividades y criterios de dominio, pero no asigna duraciones, cargas horarias ni calendarios estándar. Cada persona avanza según sus conocimientos previos, profundidad requerida, práctica y necesidad de revisión. Completar una asignatura significa demostrar los resultados de aprendizaje y no cumplir una cantidad predeterminada de tiempo.

La existencia de autoevaluaciones con respuestas no equivale todavía a tutoría autónoma. La ruta piloto de excelencia incorporará feedback diagnóstico, recuperación de prerrequisitos y criterios verificables para continuar antes de presentar una ruta como autosuficiente.

## Generación y validación

```bash
python scripts/validate_curriculum.py
python scripts/validate_course_plan_packages.py
python scripts/validate_pilot_foundations.py
python scripts/generate_site.py --force --with-units
python scripts/check_generated_preview.py --limit 94
python scripts/validate_units.py
python scripts/audit_public_unit_alignment.py
python scripts/validate_links.py --quiet
```

El generador conserva el modo seguro por defecto. Las unidades redactadas manualmente no se sobrescriben ni siquiera con `--force`; solo se reemplazan si se solicita además `--force-authored-units`.

---

## Propósito

El objetivo de CitoNauta es crear una guía estructurada y libre para aprender biomedicina de forma
progresiva, interdisciplinaria y accesible. Cada área del conocimiento biomédico se convierte en una
ruta de exploración, compuesta por asignaturas, recursos abiertos, prácticas y reflexiones.

---

## Estructura del sitio

El sitio está dividido en cuatro rutas principales y una sección de investigación:

| Área | Contenido principal | Directorio |
|---|---|---|
| Ciencias Básicas | Matemáticas, física, química, programación y estadística. | `/ciencias-basicas/` |
| Biológicas y Médicas | Biología molecular, genética, fisiología, histología y bioquímica. | `/biologicas-medicas/` |
| Ingeniería Biomédica Aplicada | Biomecánica, bioinstrumentación, biomateriales, simulación e informática médica. | `/ingenieria-biomedica/` |
| Gestión, Ética y Comunicación | Ética científica, políticas públicas, historia, innovación y divulgación. | `/gestion-etica-comunicacion/` |
| Investigación y Divulgación | Resúmenes de artículos, proyectos y avances biomédicos clasificados por área. | `/investigacion/` |

---

## Cómo contribuir

1. Haz un fork del repositorio.
2. Crea una rama para tu aporte:

```bash
git checkout -b nombre-de-tu-rama
```

3. Agrega o mejora contenido dentro de la asignatura correspondiente.
4. Envía un Pull Request explicando tu cambio.

Toda contribución debe:

- citar fuentes confiables, preferentemente primarias u oficiales;
- registrar si la fuente fue consultada directamente o solo verificada por metadata;
- mantener un lenguaje claro, técnico y respetuoso;
- favorecer la comprensión interdisciplinaria;
- diferenciar observación, asociación, predicción, causalidad y utilidad;
- conservar el estado `review` hasta que exista revisión experta documentada;
- evitar texto genérico, referencias decorativas y promoción automática por métricas técnicas.

---

## Filosofía CitoNauta

CitoNauta nace del deseo de unir curiosidad, ciencia y empatía. No busca reemplazar la educación formal,
sino ampliar el acceso al conocimiento biomédico y crear puentes entre la ciencia y la sociedad.

> Cada célula es un mundo. Cada mente, un universo que aprende.

---

## Tecnologías utilizadas

- HTML5 y CSS propio — estructura, accesibilidad y diseño responsivo.
- JavaScript progresivo — navegación, renderizado de unidades estructuradas y notación matemática.
- Python — generación estática, auditorías y validación curricular.
- GitHub Actions — quality gates e informes reproducibles.
- Git y GitHub Pages — control de versiones y despliegue abierto.

---

## Contacto

Creado por **Jenner Feijoo**  
Email: jennerfeijoo@gmail.com  
GitHub: [github.com/jennerfeijoo](https://github.com/jennerfeijoo)

---

## Licencia

Este proyecto se distribuye bajo la Licencia **Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0)**.
Puedes usar, compartir y adaptar el contenido con fines educativos o no comerciales, citando la fuente original.

> CitoNauta — Aprender es una forma de explorar la vida.
