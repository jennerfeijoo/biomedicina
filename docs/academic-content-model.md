# Modelo de contenido académico canónico

## Propósito

El contenido académico debe poder revisarse, versionarse, transformar y servir
desde una aplicación dinámica sin depender de fragmentos HTML. Para las
asignaturas migradas, `data/courses/<course_id>/` es la única fuente de autoría.
La web estática consume una proyección de esos datos y continúa funcionando
durante la transición.

## Organización de una asignatura

```text
data/courses/<course_id>/
├── course.json
├── glossary.json
├── sources.json
├── claims.json
├── media.json
├── units/
│   ├── unit-01.json
│   └── ...
└── assessments/
    ├── unit-01.json
    ├── ...
    └── course-assessment.json
```

`course.json` contiene identidad, versión, nivel, audiencia, alcance y
exclusiones, prerrequisitos, competencias, resultados de aprendizaje y las
rutas de todos los componentes. No contiene HTML.

Cada unidad usa la jerarquía `asignatura → unidad → tema → subtema → bloque`.
Los bloques tienen tipo explícito; la versión 1.0 incorpora `paragraph` y
`equation` y puede ampliarse de forma compatible con `definition`, `table`,
`figure`, `dataset`, `case_study`, `warning`, `code` u otros tipos documentados.
Cada tema puede conservar además una lista `key_points` para separar la síntesis
conceptual de los títulos de subtema sin duplicar párrafos.

Las evaluaciones viven fuera de la unidad para que una aplicación futura pueda
enviar al estudiante solo el enunciado y reservar `answer_key`, explicación,
retroalimentación y rúbrica. Toda pregunta debe apuntar a uno o más resultados
de aprendizaje estables.

El glosario evita definiciones repetidas en HTML. Las fuentes tienen un
identificador único y las unidades solo guardan referencias a esos
identificadores. El registro de afirmaciones añade fuente, localizador, tipo de
apoyo, riesgo y estado de revisión. `media.json` permite planificar figuras,
datos, audio, video o recursos interactivos antes de producirlos.

## Identificadores

Los títulos pueden corregirse sin romper relaciones. Por eso, las relaciones
usan identificadores estables como:

- `BIOEST-U01`: unidad;
- `BIOEST-U01-T03`: tema;
- `BIOEST-U01-T03-ST02`: subtema;
- `BIOEST-U01-ACT01`: actividad;
- `BIOEST-U01-Q08`: pregunta;
- `BIOEST-GLO-014`: entrada de glosario.

No se deben reutilizar identificadores eliminados ni derivar relaciones a
partir de la posición visible o del texto de un título.

## Estados independientes

Una página publicada no equivale a contenido validado. Curso y unidad declaran
por separado:

- contenido;
- fuentes;
- diseño pedagógico;
- multimedia;
- revisión interna;
- revisión externa;
- publicación.

La migración inicial conserva estados provisionales. Solo una decisión
documentada puede promover una dimensión; publicar HTML no modifica ninguna.

## Validación

```bash
python scripts/validate_academic_courses.py
python scripts/validate_academic_courses.py --strict-content
python scripts/validate_academic_courses.py --strict-academic
```

El primer comando exige integridad estructural y referencial: archivos,
identidades, jerarquía, identificadores, mapeo de resultados, pesos, fuentes,
afirmaciones y ausencia de marcadores genéricos conocidos. El modo estricto
de contenido falla mientras existan brechas en teoría, fuentes, actividades o
evaluaciones, pero permite diferir multimedia. El modo académico completo exige
además producir y documentar los recursos multimedia planificados. Entre las
brechas explícitas se incluyen:

- una actividad sin producto o duración estimada;
- una pregunta sin dificultad, nivel cognitivo, explicación o feedback;
- una definición sin fuente exacta;
- una fuente no verificada o sin estado de verificación declarado;
- un curso sin afirmaciones centrales trazadas;
- un recurso multimedia todavía planificado.

Estas brechas no deben ocultarse para obtener un control verde. Son la lista de
trabajo académica que debe cerrarse antes de solicitar revisión externa.

## Migración de otra asignatura

```bash
python scripts/migrate_course_to_canonical.py \
  --subject <course_id> \
  --course-code <CODIGO>
```

La herramienta realiza un bootstrap mecánico desde las fuentes heredadas y se
niega a sobrescribir un curso canónico existente. Después del bootstrap, los
archivos nuevos se editan directamente, se validan y se revisan académicamente;
no se vuelve a ejecutar la migración para regenerar contenido ya corregido.

## Criterio para revisión externa

Una asignatura puede presentarse a especialistas de contenido cuando el modo
`--strict-content` no informa brechas. La publicación académica completa exige
además que `--strict-academic` pase sin brechas y que la revisión interna confirme:

1. alcance, nivel, audiencia y prerrequisitos coherentes;
2. cobertura completa y progresiva de todos los resultados;
3. temas y subtemas con profundidad suficiente y sin duplicación sustantiva;
4. actividades con instrucciones, recursos, producto y criterios observables;
5. evaluaciones alineadas, con claves, explicaciones, feedback y rúbricas;
6. glosario consistente y respaldado;
7. fuentes exactas verificadas y afirmaciones centrales con localizador;
8. ecuaciones con variables, unidades y supuestos cuando corresponda;
9. límites clínicos, regulatorios, éticos y de generalización declarados;
10. paquete de revisión generado desde el mismo corpus canónico.
