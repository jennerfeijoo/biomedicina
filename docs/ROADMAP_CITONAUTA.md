# Roadmap CitoNauta

## Estado de ejecución — 29 de julio de 2026

La fábrica editorial, los generadores, los validadores y el catálogo navegable están operativos. El inventario actual contiene **94 asignaturas centrales** distribuidas en cuatro áreas y **607 unidades esperadas**.

El desarrollo lectivo no está terminado:

- **40 asignaturas** tienen todas sus unidades desarrolladas mediante JSON avanzado;
- **54 asignaturas** todavía dependen de unidades generadas con contenido de respaldo;
- existen **283 unidades avanzadas** y **324 unidades fallback**;
- no existen páginas de unidad ausentes;
- `provisional_subjects.json` no contiene entradas;
- ninguna asignatura está en `complete`, porque todavía no existe revisión disciplinar documentada.

La ausencia de asignaturas provisionales significa que todos los identificadores pertenecen al currículo central. No significa que las 94 asignaturas tengan desarrollo lectivo completo.

Entre las 40 asignaturas desarrolladas, 20 matrices de cobertura están declaradas como `implemented` y 20 como `partial`. Los controles automáticos verifican estructura, sincronización, enlaces, densidad, cobertura declarada y consistencia editorial; no certifican corrección disciplinar, suficiencia bibliográfica ni utilidad educativa final.

## 1. Lectura estratégica del proyecto

CitoNauta no es únicamente una colección de páginas HTML sobre biomedicina. El repositorio construye una plataforma educativa abierta para organizar rutas progresivas de aprendizaje que conecten ciencias básicas, ciencias biológicas y médicas, ingeniería biomédica aplicada, computación, gestión, ética y comunicación científica.

La función principal del sitio es servir como atlas curricular y fábrica editorial: una estructura navegable capaz de convertir una malla amplia de asignaturas en cursos, unidades, prácticas, conexiones interdisciplinarias, recursos verificables y contenido reutilizable para formación y divulgación.

## 2. Modelo editorial vigente

El proyecto distingue cuatro conceptos que no deben confundirse:

- **catalogada**: la asignatura existe en `data/citonauta_curriculum.json` y tiene página pública;
- **pending**: la asignatura todavía depende total o parcialmente de unidades fallback;
- **developed**: todas las unidades esperadas son avanzadas o autorales, aunque la revisión académica siga pendiente;
- **complete**: existe revisión disciplinar documentada y una decisión editorial explícita.

Una página generada no demuestra desarrollo académico. Un workflow verde tampoco convierte `review` en `complete`.

## 3. Arquitectura técnica

La plataforma conserva HTML, CSS y JavaScript estáticos compatibles con GitHub Pages. La generación y validación se apoyan principalmente en:

```text
data/citonauta_curriculum.json
data/subjects/
data/generated_courses/
data/generated_units/
data/course_redevelopment/
data/catalog_statuses.json
templates/
scripts/
.github/workflows/
```

### Fuente curricular central

`data/citonauta_curriculum.json` mantiene áreas, asignaturas, rutas públicas, módulos y unidades esperadas. Los overlays de `data/subjects/` y los paquetes de `data/course_redevelopment/` amplían esa fuente sin convertir el HTML en origen manual de verdad.

### Estados del catálogo

`data/catalog_statuses.json` se genera desde las auditorías de desarrollo real. Debe contener una partición completa de las asignaturas centrales:

- `developed`;
- `pending`;
- `complete`, como subconjunto de `developed`.

El catálogo público puede calcular y filtrar estos estados, pero el manifiesto también debe conservarlos de forma explícita para auditoría y automatización.

### Unidades avanzadas y fallback

Una unidad avanzada existe en `data/generated_units/<subject_id>/unit-XX.json` y supera los contratos de estructura y densidad. Una unidad fallback mantiene navegación y continuidad visual, pero no cuenta como desarrollo lectivo terminado.

## 4. Estado de las fases

### Fase 1 — Motor editorial base

**Implementada.** Existen fuentes estructuradas, plantillas, generadores, validadores de enlaces y workflows de control.

### Fase 2 — Inventario curricular

**Implementada a nivel de catálogo.** Las 94 asignaturas centrales están registradas. El inventario debe mantenerse sincronizado con el manifiesto editorial y los índices públicos.

### Fase 3 — Generación controlada

**Implementada.** El sitio genera cursos, unidades, índices de área y catálogo de forma determinista.

### Fase 4 — Migración progresiva

**Parcial.** Cuarenta asignaturas ya fueron sustituidas por unidades avanzadas; cincuenta y cuatro conservan contenido de respaldo.

### Fase 5 — Enriquecimiento pedagógico

**Parcial.** Las 40 asignaturas desarrolladas tienen arquitectura válida, pero solo la mitad declara cobertura `implemented`; ninguna dispone todavía de revisión disciplinar completa.

### Fase 6 — Investigación y divulgación

**Pendiente de consolidación.** Debe conectarse con las asignaturas sin crear una segunda fuente curricular paralela.

## 5. Trabajo restante

### Desarrollo lectivo

Reemplazar las **324 unidades fallback** correspondientes a **54 asignaturas pendientes** mediante paquetes trazables, decisiones curriculares justificadas y fuentes verificadas.

La mayor concentración se encuentra en Ingeniería Biomédica Aplicada:

- Ingeniería Biomédica Aplicada: 32 asignaturas pendientes;
- Ciencias Básicas: 9;
- Gestión, Ética y Comunicación: 9;
- Biológicas y Médicas: 4.

### Cobertura curricular

Revisar las 20 matrices declaradas como `partial`. La promoción a `implemented` debe responder a cobertura real, no a una modificación nominal del estado.

### Bibliografía

Reducir advertencias por enlaces genéricos, concentración de dominios y repetición excesiva entre unidades. Las advertencias no bloqueantes deben tratarse como backlog editorial, no como evidencia de corrección bibliográfica.

### Revisión disciplinar

Definir revisores por dominio, registrar observaciones, corregir hallazgos críticos y conservar evidencia de la decisión antes de promover cualquier curso a `complete`.

## 6. Reglas de operación

- No modificar `main` directamente para cambios curriculares amplios.
- No rebajar validadores para hacer pasar contenido insuficiente.
- No equiparar cantidad de palabras con cobertura disciplinar.
- No promover estados editoriales sin evidencia humana documentada.
- Mantener separadas fuente canónica, material generado y páginas públicas.
- Validar enlaces, estados, prerrequisitos y sincronización antes de fusionar.
- Conservar GitHub Pages como objetivo de despliegue.
- Usar una rama y un pull request por bloque curricular o auditoría coherente.

## 7. Prioridad inmediata

1. Mantener explícita la partición de 94 asignaturas en `developed`, `pending` y `complete`.
2. Desarrollar las 54 asignaturas pendientes mediante bloques priorizados, comenzando por las dependencias más reutilizadas y por las áreas estratégicas de CitoNauta.
3. Resolver las 20 coberturas parciales sin declarar exhaustividad inexistente.
4. Reducir deuda bibliográfica y ampliar diversidad de fuentes primarias y oficiales.
5. Organizar revisión disciplinar documentada de las 40 asignaturas desarrolladas.

La pregunta guía continúa siendo:

> ¿Este cambio aumenta la coherencia curricular, reduce trabajo manual futuro y mejora la trazabilidad de la evidencia sin exagerar el estado académico del contenido?
