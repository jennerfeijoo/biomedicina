# CitoNauta: Explorando la Biomedicina
CitoNauta es una plataforma educativa y de divulgacion cientifica abierta que invita a estudiantes,
investigadores y curiosos a explorar el universo de la biomedicina moderna, desde los fundamentos de
las ciencias basicas hasta las aplicaciones tecnologicas y eticas mas actuales.
> "Explorar la vida desde dentro, con los ojos del conocimiento."

## Estado actual

- 84 asignaturas distribuidas en cuatro áreas académicas.
- 508 unidades navegables: 497 generadas con el estándar lectivo común y 11 unidades editoriales extensas conservadas.
- Cada unidad incluye resultados, desarrollo conceptual, caso de integración, práctica segura, autoevaluación con respuestas, glosario y cinco o más recursos abiertos.
- Todas las asignaturas incluyen prerrequisitos, competencias, objetivos, evaluación, conceptos clave y conexiones curriculares.
- Las páginas se generan de forma reproducible desde `data/citonauta_curriculum.json`, `data/course_outlines.json` y los contenidos especializados de `data/subjects/`.
- Los índices de área y las páginas de curso se mantienen sincronizados con las plantillas de `templates/`.
- Estado editorial: contenido lectivo disponible y pendiente de revisión experta; no equivale a acreditación ni a consejo clínico.

## Generación y validación

```bash
python scripts/validate_curriculum.py
python scripts/generate_site.py --force --with-units
python scripts/check_generated_preview.py --limit 84
python scripts/validate_units.py
python scripts/validate_links.py --quiet
```

El generador conserva el modo seguro por defecto. Las unidades redactadas manualmente no se sobrescriben ni siquiera con `--force`; solo se reemplazan si se solicita además `--force-authored-units`.

---
## Proposito
El objetivo de CitoNauta es crear una guia estructurada y libre para aprender biomedicina de forma
progresiva, interdisciplinaria y accesible.
Cada area del conocimiento biomedico se convierte en una ruta de exploracion, compuesta por
asignaturas, recursos abiertos, practicas y reflexiones.
---
## Estructura del sitio
El sitio esta dividido en cuatro rutas principales y una seccion de investigacion:
| Area | Contenido principal | Directorio |
|------|---------------------|-------------|
| Ciencias Basicas | Matematicas, fisica, quimica, programacion y estadistica. | /ciencias-basicas/ |
| Biologicas y Medicas | Biologia molecular, genetica, fisiologia, histologia y bioquimica. | /biologicas-medicas/ |
| Ingenieria Biomedica Aplicada | Biomecanica, bioinstrumentacion, biomateriales, simulacion e informatica medica. | /ingenieria-biomedica/ |
| Gestion, Etica y Comunicacion | Etica cientifica, politicas publicas, historia, innovacion y divulgacion. | /gestion-etica-comunicacion/ |
| Investigacion y Divulgacion | Resumenes de articulos, proyectos y avances biomedicos clasificados por area. | /investigacion/ |

---
## Como contribuir
1. Haz un fork del repositorio.
2. Crea una rama para tu aporte:
```
git checkout -b nombre-de-tu-rama
```
3. Agrega o mejora contenido dentro de la asignatura correspondiente.
4. Envia un Pull Request explicando tu cambio.
Toda contribucion debe:
- Citar fuentes confiables (papers, libros, recursos abiertos).
- Mantener un lenguaje claro y respetuoso.
- Favorecer la comprension interdisciplinaria.
---
## Filosofia CitoNauta
CitoNauta nace del deseo de unir curiosidad, ciencia y empatia.
No busca reemplazar la educacion formal, sino ampliar el acceso al conocimiento biomedico y crear
puentes entre la ciencia y la sociedad.
> Cada celula es un mundo. Cada mente, un universo que aprende.
---
## Tecnologias utilizadas
- HTML5 + TailwindCSS — estructura y estilo ligero
- JavaScript (minimo) — animaciones y navegacion basica
- Git & GitHub Pages — control de versiones y despliegue abierto
---
## Contacto
Creado por **Jenner Feijoo**
Email: jennerfeijoo@gmail.com
GitHub: [github.com/jennerfeijoo](https://github.com/jennerfeijoo)
---
## Licencia
Este proyecto se distribuye bajo la Licencia **Creative Commons Attribution-NonCommercial 4.0 (CC
BY-NC 4.0)**.
Puedes usar, compartir y adaptar el contenido con fines educativos o no comerciales, citando la fuente
original.
---
> CitoNauta — Aprender es una forma de explorar la vida.
