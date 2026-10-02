# CitoNauta: Explorando la Biomedicina

CitoNauta es una plataforma educativa abierta para explorar ciencias básicas, biología, medicina, ingeniería biomédica y sus dimensiones éticas y sociales.

> Explorar la vida desde dentro, con los ojos del conocimiento.

## Estado del catálogo

- 94 asignaturas en cuatro áreas académicas.
- 94 con material lectivo y actividades disponibles.
- 17 conservan marcadores de plantilla en 101 unidades y requieren reconstrucción disciplinar.
- 77 no contienen esos marcadores conocidos; esto no equivale a validación científica.
- 0 con registro completo de afirmaciones y localizadores.
- 0 con revisión IA validada para un alcance científico.
- Ninguna asignatura tiene estado editorial `complete`.

Una página navegable o un workflow verde demuestra integridad técnica, no validez científica. Las asignaturas permanecen en `review` hasta que sus afirmaciones estén trazadas y exista una revisión documentada adecuada al alcance. La revisión documental y los controles reproducibles no requieren un modelo de lenguaje; tampoco acreditan una revisión humana que no se haya realizado.

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

## Instalación y desarrollo

Requiere Python 3.12 y Node.js 22 (para comprobar la sintaxis JavaScript). La generación utiliza la biblioteca estándar de Python; pytest es una dependencia exclusiva de pruebas.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m http.server 8000
```

Abra `http://localhost:8000`. En Windows active el entorno con `.venv\Scripts\Activate.ps1`.

## Generación y validación

Edite las fuentes canónicas, publique sus espejos y regenere las páginas:

```bash
python scripts/publish_courses.py --all
python scripts/sync_catalog_statuses.py
python scripts/generate_site.py --force --with-units
python scripts/run_quality.py
```

La suite ejecuta todos los validadores, unittest, pytest, auditorías, comprobaciones de JavaScript y dos generaciones consecutivas. Guarda logs y un resumen JSON; acepta `--report-dir` para elegir su ubicación. Comprueba enlaces, recursos y anclas, además de la coherencia de las salidas versionadas. No promueve automáticamente una asignatura a `complete`.

La auditoría científica adicional incluye los registros canónicos migrados y detalla los campos o localizadores que faltan:

```bash
python scripts/audit_scientific_traceability.py --strict
```

Esta comprobación de finalización científica todavía detecta brechas. El resultado técnico de CI no sustituye ese control ni acredita la corrección o cobertura de todas las afirmaciones. Los informes de contenido genérico y trazabilidad forman parte de los artefactos de CI.

## Publicación

El sitio es estático y se publica en [GitHub Pages](https://jennerfeijoo.github.io/biomedicina/). El HTML generado, el sitemap y los recursos se versionan junto con las fuentes. El workflow `CitoNauta Quality Gates` ejecuta la misma suite en pull requests y en `main`; integre únicamente cambios técnicos sin regresiones. No se requieren procesos residentes ni APIs privadas para servir las páginas.

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
- mantener `review` hasta una revisión documentada adecuada al alcance; no atribuir aprobación humana o clínica a pruebas automatizadas.

## Tecnologías

- HTML5 y CSS propio;
- JavaScript progresivo;
- Python para generación y auditoría;
- GitHub Actions para controles reproducibles;
- GitHub Pages para publicación.

## Licencia

El contenido original del proyecto se distribuye bajo Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0). Los materiales de terceros conservan sus propias condiciones y no quedan relicenciados por su inclusión como referencia.
