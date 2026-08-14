# Protocolo de desarrollo de contenido académico

## Propósito

Este documento define el proceso obligatorio para diseñar, desarrollar, revisar y publicar asignaturas en CitoNauta. Su objetivo es asegurar que cada curso tenga una arquitectura curricular justificada, contenido científicamente trazable, progresión pedagógica coherente y estados editoriales honestos.

Las estructuras existentes deben tratarse como material de trabajo, no como decisiones curriculares definitivas. Ningún número de unidades, secuencia temática, actividad o evaluación se conserva únicamente porque ya exista en el repositorio.

## Principio rector

Cada asignatura debe analizarse de manera independiente antes de producir o reorganizar contenido. La arquitectura final debe derivarse del alcance real de la disciplina, su nivel académico, los prerrequisitos, los estándares pertinentes, programas universitarios oficiales, libros de referencia, revisiones científicas, guías técnicas y necesidades pedagógicas.

La uniformidad técnica del repositorio no debe imponerse sobre la lógica académica de una disciplina.

## Flujo obligatorio por asignatura

### 1. Delimitación disciplinar

Antes de decidir unidades o redactar lecciones, se debe definir:

- propósito del curso;
- nivel académico y público previsto;
- prerrequisitos y competencias de entrada;
- resultados de aprendizaje terminales;
- relación con asignaturas previas, paralelas y posteriores;
- límites temáticos para evitar solapamientos;
- aplicaciones biomédicas legítimas;
- contenidos que deben quedar fuera del curso.

El resultado debe incluir una declaración explícita de alcance y exclusiones.

### 2. Revisión de evidencia externa

La arquitectura del curso debe contrastarse con fuentes externas suficientes y diversas. Se priorizan:

1. programas y planes docentes oficiales de universidades;
2. currículos, consensos y recursos de sociedades científicas o profesionales;
3. libros de texto reconocidos;
4. revisiones científicas de alta calidad;
5. guías técnicas, clínicas, regulatorias o éticas;
6. artículos primarios que definan métodos, conceptos o avances esenciales;
7. documentación oficial de herramientas, bases de datos y estándares.

No debe construirse una asignatura a partir de una única fuente ni de una sola tradición curricular.

### 3. Registro de fuentes

Cada referencia debe registrar, cuando sea posible:

- título;
- autores u organización;
- año, edición o versión;
- DOI, ISBN, URL o identificador estable;
- tipo de fuente;
- función curricular;
- secciones o temas relevantes;
- fecha de consulta;
- estado de verificación.

Estados de verificación permitidos:

- `verified_directly`: contenido relevante consultado de forma directa;
- `verified_metadata`: existencia, identidad y pertinencia general verificadas, sin acceso completo al contenido;
- `recommended_future_review`: referencia pertinente identificada para revisión posterior;
- `superseded`: fuente reemplazada por una versión más reciente o adecuada;
- `excluded`: fuente evaluada y descartada, con justificación.

Una referencia no consultada directamente no puede utilizarse como evidencia detallada de una afirmación específica. Puede mantenerse como recurso identificado o bibliografía futura con el estado correspondiente.

### 4. Matriz de cobertura disciplinar

Antes de fijar el número de unidades, se debe construir una matriz con:

- dominios nucleares y subdominios;
- conceptos imprescindibles;
- mecanismos;
- métodos experimentales o computacionales;
- aplicaciones y limitaciones;
- cuestiones éticas o regulatorias;
- competencias cuantitativas;
- conexiones con otras asignaturas.

Cada dominio debe clasificarse como fundamental, intermedio, avanzado, transversal, opcional o fuera de alcance.

### 5. Decisión del número de unidades

El número de unidades debe justificarse después de revisar la matriz de cobertura. Se deben considerar:

- dependencias conceptuales;
- extensión y complejidad de cada dominio;
- carga cognitiva;
- separación entre fundamentos, mecanismos, métodos y aplicaciones;
- necesidad de prácticas o proyectos;
- continuidad temporal o causal;
- equilibrio entre profundidad y fragmentación;
- riesgo de comprimir múltiples sistemas o métodos en una sola unidad;
- riesgo de crear unidades demasiado breves o redundantes.

No existe un número predeterminado de unidades. Cada decisión debe registrar alternativas consideradas, estructura seleccionada, razones para aceptar o rechazar cada alternativa, temas fusionados, temas separados, temas trasladados y contenidos diferidos.

### 6. Arquitectura pedagógica

Cada unidad debe incluir, como mínimo:

- pregunta central;
- propósito;
- resultados de aprendizaje evaluables;
- conocimientos previos;
- conceptos y mecanismos;
- modelo mental o representación visual;
- métodos de estudio;
- evidencia experimental o computacional;
- actividad guiada;
- actividad reproducible o práctica;
- ejemplo biomédico;
- limitaciones y errores frecuentes;
- evaluación formativa;
- referencias específicas.

Cuando corresponda, debe distinguirse explícitamente:

- causa, asociación, correlación y predicción;
- mecanismo biológico, métrica computacional y utilidad clínica;
- significancia estadística y relevancia clínica;
- validación técnica, validación externa y utilidad en flujo real;
- biomarcador, diagnóstico, pronóstico, predicción y monitorización;
- observación, perturbación, rescate y evidencia causal.

### 7. Producción del contenido

La escritura debe avanzar desde la arquitectura aprobada, no desde el texto previo. El contenido existente puede reutilizarse, editarse, dividirse, fusionarse, reemplazarse o retirarse según su calidad científica, especificidad, trazabilidad y función pedagógica.

Se debe evitar:

- relleno genérico;
- repetición de plantillas entre temas;
- párrafos intercambiables entre asignaturas;
- enumeraciones sin mecanismo;
- afirmaciones clínicas sin validación;
- referencias decorativas;
- analogías que distorsionen;
- sobrecarga terminológica sin integración.

### 8. Control de repetición y especificidad

Antes de publicar se debe comprobar:

- frases repetidas entre unidades;
- párrafos que podrían pertenecer a cualquier asignatura;
- correspondencia entre ejemplos, mecanismos y métodos;
- especificidad de actividades y evaluaciones;
- diversidad real de fuentes;
- coherencia entre teoría, práctica y resultados de aprendizaje.

Las advertencias transversales deben mantenerse, pero adaptadas al contexto concreto.

### 9. Evaluación y criterios de dominio

El plan de evaluación debe derivarse de los resultados de aprendizaje e incluir una combinación pertinente de recuperación conceptual, resolución de problemas, interpretación de datos, diseño experimental o computacional, evaluación de evidencia, comunicación científica, proyecto integrador, revisión por pares y defensa de decisiones.

Cada actividad debe indicar competencia evaluada, evidencia esperada, criterio de logro, errores críticos y limitaciones de la evaluación.

### 10. Revisión académica

La revisión debe comprobar cobertura disciplinar, precisión científica, actualidad de fuentes, progresión pedagógica, coherencia terminológica, trazabilidad de afirmaciones, calidad de prácticas, transparencia sobre incertidumbre y límites biomédicos, clínicos, éticos y regulatorios.

No se debe inferir madurez académica a partir de existencia de archivos, cumplimiento de un esquema JSON, número de palabras, número de unidades, renderizado correcto o ausencia de errores técnicos.

El sistema revisor puede ser IA y autorizar de forma autónoma cuando exista un registro `validated_for_scope` que coincida con su modelo, versión, prompt, rúbrica, disciplina, riesgo y acceso a fuentes. Hasta entonces su decisión es `ai_review_provisional`. Las personas expertas forman el comparador de la validación y se convocan después para vigilancia, incidentes, abstenciones o casos fuera de alcance.

### 11. Estados editoriales

- `placeholder`: asignatura catalogada sin programa desarrollado;
- `draft`: arquitectura o contenido inicial incompleto;
- `review`: programa estructurado con revisión provisional o pendiente;
- `generated`: unidades desarrolladas pendientes de trazabilidad o validación final;
- `complete`: contenido revisado por un sistema validado para el alcance y con criterios documentados.

Ningún proceso automático puede promover una asignatura a `complete` únicamente por superar validaciones técnicas.

### 12. Artefactos mínimos por asignatura

Cada asignatura desarrollada debe disponer de:

1. ficha curricular;
2. matriz de cobertura;
3. documento de decisión de arquitectura;
4. registro de fuentes;
5. programa de unidades;
6. unidades desarrolladas;
7. prácticas y evaluaciones;
8. criterios de dominio;
9. registro de revisión;
10. página pública sincronizada.

## Estructura recomendada de archivos

```text
data/
  subjects/<area>/<subject>.json
  curriculum_coverage/<area>.json
  curriculum_decisions/<subject>.json
  source_registry/<subject>.json
  generated_courses/<subject>.json
  generated_units/<subject>/unit-XX.json
```

## Criterio de cierre

Una asignatura está lista para revisión final cuando su alcance está delimitado, el número de unidades está justificado, los dominios nucleares están cubiertos, las referencias están registradas y clasificadas, las unidades son específicas y no repetitivas, las prácticas evalúan competencias reales, las limitaciones están declaradas, las páginas públicas son reproducibles, los controles técnicos pasan y la madurez académica ha sido evaluada separadamente de la integridad técnica.

## Regla de mantenimiento

Este protocolo debe revisarse cuando cambien estándares disciplinares, regulaciones, herramientas metodológicas, arquitectura del repositorio, criterios editoriales o procesos de validación. Las modificaciones deben conservar historial y justificación.
