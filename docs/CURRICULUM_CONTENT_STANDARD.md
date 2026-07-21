# Estándar curricular universitario para CitoNauta

## 1. Principio rector

Una asignatura de CitoNauta no es una página de presentación ni una colección de resúmenes. Debe funcionar como un curso abierto de nivel preuniversitario avanzado o universitario, con profundidad suficiente para sostener un semestre completo de estudio autónomo, docencia guiada, práctica, evaluación y conexión con problemas biomédicos.

La existencia de seis archivos de unidad no basta para declarar una asignatura completa. El estado final depende de la cobertura conceptual, la profundidad explicativa, el volumen de práctica y la coherencia del curso entero.

## 2. Equivalencia académica esperada

Una asignatura completa debe representar, según su nivel:

- 12 a 16 semanas de trabajo;
- 6 a 10 horas semanales entre lectura, ejercicios, actividades y evaluación;
- 90 a 150 horas totales para una asignatura introductoria;
- 120 a 180 horas totales para una asignatura universitaria cuantitativa, experimental o profesional;
- progresión desde fundamentos hasta aplicación, integración y análisis crítico;
- cobertura comparable a un sílabo formal, aunque CitoNauta no otorgue créditos ni certificación.

## 3. Componentes obligatorios del curso

Cada asignatura debe incluir:

- propósito y alcance claramente delimitados;
- nivel académico y carga estimada;
- prerrequisitos verificables;
- competencias y resultados de aprendizaje evaluables;
- secuencia de 6 a 10 unidades coherentes;
- desarrollo teórico completo, no listas de temas;
- ejemplos resueltos con razonamiento, interpretación y limitaciones;
- ejercicios graduados desde comprensión hasta integración;
- actividades prácticas o computacionales;
- autoevaluaciones con respuestas razonadas;
- evaluación formativa y sumativa;
- proyecto, caso integrador o producto final;
- bibliografía primaria, libros abiertos y documentación oficial;
- aplicaciones biomédicas correctamente contextualizadas;
- conexiones explícitas con asignaturas previas y posteriores.

## 4. Profundidad mínima por unidad

Una unidad semestralmente válida debe contener, como referencia mínima:

- 5 a 8 objetivos específicos;
- 4 a 6 secciones teóricas sustantivas;
- 2 000 a 4 000 palabras de contenido académico, sin contar enlaces ni metadatos;
- definiciones, relaciones, supuestos, unidades y límites de aplicación;
- notación matemática renderizada cuando corresponda;
- 2 o más ejemplos resueltos;
- 1 o más actividades guiadas;
- 8 a 15 problemas o tareas graduadas;
- 8 a 12 preguntas de autoevaluación con respuestas;
- 5 o más errores frecuentes explicados;
- 12 o más términos de glosario cuando el campo lo requiera;
- 5 o más fuentes trazables, priorizando fuentes primarias u oficiales;
- conexiones biomédicas específicas, evitando analogías superficiales.

Los rangos pueden adaptarse a asignaturas predominantemente prácticas, clínicas, éticas o de diseño, pero la carga y profundidad total del curso deben mantenerse.

## 5. Progresión pedagógica

Las unidades no deben ser independientes ni repetitivas. El curso completo debe avanzar por estas fases:

1. fundamentos, vocabulario y representaciones;
2. métodos y procedimientos;
3. resolución de problemas;
4. interpretación de datos, modelos o evidencia;
5. aplicación biomédica;
6. integración, validación, incertidumbre y límites.

Cada unidad debe reutilizar conocimientos anteriores y preparar explícitamente los siguientes.

## 6. Matemáticas, ecuaciones y código

- Las expresiones matemáticas se escriben con LaTeX y se renderizan mediante MathJax.
- Matrices, fracciones, exponentes, integrales, derivadas, sistemas y símbolos no deben mostrarse como texto plano ambiguo.
- Toda ecuación debe definir variables, unidades, supuestos e interpretación.
- El código debe ser ejecutable o claramente pseudocódigo, con entradas, salidas, validación y explicación.
- Los resultados numéricos deben comprobarse dimensionalmente y discutirse, no solo calcularse.

Las reglas detalladas están en `docs/MATHEMATICAL_NOTATION.md`.

## 7. Práctica y evaluación

Un curso semestral debe disponer, en conjunto, de:

- al menos 40 ejercicios o tareas distribuidos entre las unidades;
- problemas conceptuales, cuantitativos, interpretativos y aplicados;
- actividades con datos, código, laboratorio virtual, lectura crítica o diseño cuando corresponda;
- una evaluación diagnóstica o de prerrequisitos;
- evaluaciones formativas por unidad;
- al menos una evaluación integradora intermedia;
- un proyecto, caso o examen final con rúbrica;
- ponderaciones que sumen 100 %;
- criterios de corrección y resultados esperados.

## 8. Bibliografía y trazabilidad

Las fuentes deben cumplir estas reglas:

- priorizar libros universitarios abiertos, documentación oficial, estándares y artículos de referencia;
- evitar enlaces genéricos cuando existe un capítulo o documento específico;
- verificar que la URL funciona y respalda el contenido citado;
- no inventar DOI, títulos, autores ni organizaciones;
- distinguir fuentes introductorias de evidencia especializada;
- actualizar las referencias cuando el campo sea cambiante.

## 9. Estados editoriales

- `placeholder`: existe únicamente la estructura mínima.
- `draft`: contiene material inicial, pero aún incompleto.
- `developed`: las unidades poseen contenido sustantivo, aunque no cumplen todavía toda la equivalencia semestral.
- `review`: cumple el estándar de carga y estructura y está pendiente de revisión académica final.
- `complete`: superó revisión conceptual, pedagógica, técnica, bibliográfica y visual.

No debe usarse `complete` solo porque existan todas las unidades.

## 10. Criterio de aceptación semestral

Una asignatura puede considerarse lista para `review` únicamente cuando:

- cubre todos los resultados del sílabo;
- tiene una secuencia completa de unidades;
- alcanza la carga académica declarada;
- desarrolla teoría y no solo describe qué debería estudiarse;
- contiene práctica suficiente y graduada;
- incorpora evaluación formativa y sumativa;
- incluye un producto integrador;
- presenta notación, código, tablas y figuras de forma legible;
- usa fuentes trazables y pertinentes;
- diferencia evidencia, inferencia, predicción y causalidad;
- declara supuestos, incertidumbre y límites;
- funciona en escritorio y móvil;
- ha sido revisada como un curso completo, no como archivos aislados.

## 11. Estrategia de migración

Las unidades existentes con esquema `1.0` se consideran contenido desarrollado de transición. Deben ampliarse y revisarse antes de declarar la asignatura semestralmente completa.

La migración seguirá este orden:

1. corregir navegación, notación y estructura común;
2. seleccionar una asignatura;
3. convertir todas sus unidades al estándar semestral;
4. incorporar práctica y evaluación de curso;
5. realizar auditoría académica y visual;
6. solo entonces marcarla como `review` o `complete`;
7. repetir el proceso asignatura por asignatura.

La regla operativa es:

> No aumentar el número de asignaturas nominalmente completas a costa de profundidad. Cada curso debe ser realmente estudiable durante un semestre.