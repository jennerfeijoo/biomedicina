# Estándar de navegación entre asignaturas y unidades

Cada asignatura de CitoNauta debe utilizar la misma arquitectura pública:

1. **Página de asignatura**: propósito, prerrequisitos, competencias, resultados, cronograma, evaluación, recursos y una vista breve de la secuencia de unidades.
2. **Índice de unidades** (`unidades/index.html`): tarjetas de todas las unidades con título, descripción y acceso directo.
3. **Página individual de unidad** (`unidades/unidad-XX.html`): desarrollo lectivo completo, práctica, autoevaluación, fuentes y navegación anterior/siguiente.

## Regla editorial

La página principal de la asignatura no debe reproducir teoría, actividades, autoevaluaciones ni fuentes de cada unidad. Estos contenidos pertenecen a la página individual correspondiente.

## Mejora progresiva

El contenido esencial debe permanecer disponible sin JavaScript. Cuando exista una unidad avanzada en `data/generated_units`, JavaScript puede sustituir el contenido genérico de su página individual por la edición avanzada, pero no debe expandir de nuevo todas las unidades dentro de la página principal de la asignatura.

## Criterios de aceptación

- todas las asignaturas enlazan a `unidades/index.html`;
- cada unidad tiene una URL propia;
- la página principal muestra únicamente resúmenes breves de unidades;
- los enlaces `#unidad-X` dejan de ser la navegación principal;
- las unidades avanzadas se muestran dentro de su página individual;
- las unidades sin suplemento avanzado conservan el contenido estático generado;
- la regeneración completa y los validadores del repositorio finalizan sin diferencias.
