# Roadmap CitoNauta

## Estado de ejecución — julio de 2026

La fábrica editorial y el inventario curricular ya están operativos. Las 84 asignaturas cuentan con un temario específico de seis o más unidades y se enriquecen automáticamente con objetivos, resultados evaluables, actividades, evaluación, conceptos, relaciones y recursos. Las páginas de asignatura y los cuatro índices de área se generan desde datos estructurados y pasan validación curricular, de plantilla y de enlaces.

Las fases 1 a 5 se consideran implementadas a nivel de plataforma y contenido base. La revisión experta continua, la ampliación de bibliografía específica, los ejercicios resueltos y la sección de investigación permanecen como trabajo editorial evolutivo; ya no bloquean que las asignaturas funcionen como guías abiertas completas.

## 1. Lectura estratégica del proyecto

CitoNauta no debe entenderse solo como una colección de páginas HTML sobre biomedicina. El objetivo real del repositorio es construir una plataforma educativa abierta para organizar una ruta progresiva de aprendizaje biomédico, conectando ciencias básicas, ciencias biológicas y médicas, ingeniería biomédica aplicada, gestión, ética, comunicación e investigación/divulgación.

La función principal del sitio es servir como atlas curricular y editorial: una estructura navegable que permita convertir una malla amplia de asignaturas en rutas de aprendizaje, páginas de referencia, recursos abiertos, prácticas, conexiones interdisciplinarias y contenido de divulgación científica.

## 2. Estado actual

El proyecto ya cuenta con una estructura estática basada en HTML/CSS/JS y compatible con GitHub Pages. La navegación se organiza en áreas académicas principales:

- `ciencias-basicas/`
- `biologicas-medicas/`
- `ingenieria-biomedica/`
- `gestion-etica-comunicacion/`

Cada área contiene múltiples páginas de asignaturas bajo rutas del tipo:

```text
area/asignatura/index.html
```

La estructura actual es útil como esqueleto inicial, pero muchas páginas comparten un patrón muy similar: título, descripción genérica, navegación, breadcrumbs, enlaces al índice del área y enlaces anterior/siguiente.

## 3. Problema principal

El riesgo central es intentar terminar el sitio editando manualmente cada página `index.html`. Ese enfoque no escala.

Mantener manualmente decenas de páginas implica alto riesgo de:

- inconsistencias en títulos;
- errores en rutas relativas;
- breadcrumbs desactualizados;
- navegación anterior/siguiente incorrecta;
- metadatos incompletos;
- estilos fragmentados;
- contenido repetitivo;
- dificultad para actualizar el diseño global;
- pérdida de coherencia pedagógica entre asignaturas.

El problema no es solo técnico. También es editorial y curricular: cada asignatura necesita una estructura pedagógica mínima común para que la plataforma sea útil.

## 4. Objetivo de la Fase 1

La Fase 1 debe convertir CitoNauta en una fábrica estática controlada, manteniendo HTML/CSS/JS y compatibilidad con GitHub Pages.

El objetivo no es migrar a React, Next, Astro, Hugo, Jekyll ni otro framework. El objetivo es crear un motor interno simple y transparente que permita generar páginas repetitivas a partir de datos estructurados.

## 5. Arquitectura propuesta

```text
data/citonauta_curriculum.json
templates/asignatura.html
scripts/generate_site.py
scripts/validate_links.py
docs/ROADMAP_CITONAUTA.md
```

### `data/citonauta_curriculum.json`

Fuente central de información curricular y editorial. Debe contener:

- datos generales del proyecto;
- áreas académicas;
- asignaturas;
- rutas;
- títulos;
- descripciones breves;
- objetivos de aprendizaje;
- módulos;
- conceptos clave;
- conexiones biomédicas;
- estado de desarrollo de cada página.

### `templates/asignatura.html`

Plantilla HTML común para páginas de asignatura. Debe controlar:

- estructura base;
- metadatos;
- breadcrumbs;
- navegación de área;
- título;
- descripción;
- objetivos;
- módulos;
- conceptos clave;
- conexión biomédica;
- enlaces anterior/siguiente;
- footer.

### `scripts/generate_site.py`

Script generador. Debe leer el JSON, aplicar la plantilla y escribir páginas HTML. En esta fase debe funcionar de forma conservadora:

- no borrar archivos existentes;
- no sobrescribir páginas sin confirmación explícita;
- permitir modo `--dry-run`;
- permitir modo `--force` solo cuando se decida migrar páginas;
- reportar páginas generadas, omitidas y pendientes.

### `scripts/validate_links.py`

Validador de enlaces internos. Debe recorrer HTML del repositorio y detectar enlaces locales rotos, ignorando enlaces externos, `mailto:`, anclas vacías y protocolos no locales.

## 6. Estructura pedagógica mínima por asignatura

Cada asignatura debería avanzar hacia una estructura mínima:

```text
Asignatura
├── Propósito
├── Objetivos de aprendizaje
├── Módulos o bloques temáticos
├── Conceptos clave
├── Conexión biomédica
├── Prácticas o actividades sugeridas
├── Recursos abiertos
└── Relaciones con otras asignaturas
```

Esta estructura evita que el sitio sea solo un índice de carpetas y lo convierte en un mapa de aprendizaje.

## 7. Fases recomendadas

### Fase 1 — Motor editorial base

- Crear `docs/ROADMAP_CITONAUTA.md`.
- Crear `data/citonauta_curriculum.json`.
- Crear `templates/asignatura.html`.
- Crear `scripts/generate_site.py`.
- Crear `scripts/validate_links.py`.
- No migrar todas las páginas todavía.

### Fase 2 — Inventario curricular completo

- Revisar todas las asignaturas existentes.
- Normalizar títulos con tildes.
- Añadir descripciones breves.
- Definir estado editorial: `placeholder`, `draft`, `review`, `complete`.

### Fase 3 — Generación controlada

- Probar generación en una o dos asignaturas.
- Comparar HTML generado con páginas existentes.
- Ajustar plantilla.
- Validar enlaces.

### Fase 4 — Migración progresiva

- Migrar por área, no todo el sitio a la vez.
- Priorizar páginas placeholder.
- Revisar resultados antes de sobrescribir contenido existente.

### Fase 5 — Enriquecimiento pedagógico

- Añadir objetivos de aprendizaje.
- Añadir módulos.
- Añadir conceptos clave.
- Añadir recursos.
- Añadir conexiones entre asignaturas.

### Fase 6 — Investigación y divulgación

- Crear o consolidar la sección `investigacion/`.
- Clasificar artículos, proyectos, notas de divulgación y avances biomédicos.
- Conectar contenidos de investigación con asignaturas relacionadas.

## 8. Reglas de seguridad

- No editar masivamente páginas HTML sin respaldo.
- No borrar páginas existentes sin confirmación explícita.
- No modificar `main` directamente para cambios grandes.
- Trabajar en ramas de fase.
- Revisar `git status` antes y después de cada bloque de cambios.
- Validar enlaces antes de abrir pull request.
- Mantener GitHub Pages como objetivo de despliegue.

## 9. Prioridad inmediata

La prioridad no es terminar todas las páginas. La prioridad es crear una base editorial que permita terminar el sitio de forma escalable.

La pregunta guía debe ser:

> ¿Este cambio reduce trabajo manual futuro y aumenta coherencia curricular?

Si la respuesta es sí, pertenece a la Fase 1.
