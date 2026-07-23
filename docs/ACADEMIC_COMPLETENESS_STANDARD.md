# Estándar de completitud académica de Citonauta

## Principio central

La completitud de una asignatura no se determina por el número de palabras, páginas, unidades o semanas. La extensión textual se conserva únicamente como métrica descriptiva y como señal de posibles truncamientos. No existe un máximo de palabras por unidad ni por asignatura.

Una asignatura se considera preparada para revisión académica cuando cubre el conocimiento disciplinar pertinente con profundidad, progresión, práctica, evidencia y evaluación. El estado interno debe permanecer en `review` hasta que una persona experta en la disciplina complete una revisión externa documentada.

## Capas obligatorias de aprendizaje

Cada concepto debe desarrollarse mediante las capas que correspondan:

1. **Definición y delimitación**: significado, alcance, unidades y diferencias respecto de conceptos próximos.
2. **Intuición estructurada**: modelo mental que no distorsione el mecanismo.
3. **Mecanismo**: actores, estados, direcciones, escalas espaciales y temporales.
4. **Formalización**: ecuaciones, algoritmos, estructuras de datos o modelos cuando sean pertinentes.
5. **Evidencia**: qué observaciones o experimentos sustentan el concepto y qué alternativas existen.
6. **Medición**: instrumentos, variables, resolución, calibración, controles, incertidumbre y sesgos.
7. **Aplicación**: problemas resueltos, casos, datos y decisiones justificadas.
8. **Limitaciones**: supuestos, excepciones, fallos, controversias y dominio de validez.
9. **Integración**: relación con otros conceptos, escalas y asignaturas.
10. **Transferencia**: capacidad de aplicar el conocimiento a un problema nuevo.

No todos los conceptos requieren la misma extensión. Ninguno puede considerarse cubierto por aparecer únicamente en una lista, glosario o frase introductoria.

## Componentes obligatorios por asignatura

### Cobertura disciplinar

- Matriz explícita de dominios y temas obligatorios.
- Nivel esperado para cada tema: introducción, aplicación, profundización o integración.
- Prerrequisitos trazables.
- Identificación de solapamientos y límites con otras asignaturas.
- Temas avanzados y optativos separados del núcleo obligatorio.

### Teoría

- Explicaciones mecanísticas y no solo descriptivas.
- Excepciones y variabilidad biológica o técnica.
- Comparación de modelos alternativos.
- Escalas, unidades y órdenes de magnitud.
- Separación entre observación, asociación, predicción, causalidad y utilidad.

### Práctica

- Problemas graduados y problemas de transferencia.
- Actividades con datos crudos o simulados.
- Soluciones razonadas y criterios de corrección.
- Casos adversariales, fronteras y resultados negativos.
- Retroalimentación sobre errores frecuentes.

### Experimentación o computación

Cuando la disciplina lo requiera:

- pregunta e hipótesis;
- diseño y unidad experimental;
- controles positivos, negativos y ortogonales;
- réplicas biológicas y técnicas;
- fase preanalítica;
- adquisición y control de calidad;
- análisis reproducible;
- interpretación y alternativas;
- troubleshooting;
- bioseguridad, ética y límites de uso.

Las actividades pueden emplear datos abiertos, simulaciones, laboratorios virtuales o materiales educativos cuando no sea viable o seguro ejecutar procedimientos físicos.

### Literatura científica

- Libros o tratados canónicos.
- Documentación técnica o estándares primarios.
- Artículos de investigación representativos.
- Actividades de lectura de figuras y métodos.
- Identificación de hipótesis, controles, resultados, inferencias y limitaciones.
- Diferenciación entre artículo primario, revisión, consenso, guía y recurso divulgativo.

### Visualización

- Diagramas de mecanismos y flujos.
- Figuras con escalas, unidades, leyendas y procedencia.
- Representaciones multiescala cuando sean necesarias.
- Lectura crítica de gráficos reales.
- Ausencia de elementos decorativos sin función explicativa.

### Evaluación de dominio

- Diagnóstico de prerrequisitos.
- Evaluación formativa por dominio.
- Evaluación acumulativa.
- Problemas nuevos no idénticos a los ejemplos.
- Proyecto integrador reproducible.
- Defensa o explicación oral cuando corresponda.
- Criterios de recuperación para dominios no dominados.

## Estados de cobertura

Cada tema de la matriz curricular debe usar uno de estos estados:

- `verified`: contenido, práctica y evaluación existen y fueron revisados.
- `implemented`: contenido y evidencia existen, pendientes de revisión externa.
- `partial`: existe cobertura, pero falta profundidad, práctica, fuente o evaluación.
- `missing`: no existe cobertura suficiente.
- `out_of_scope`: exclusión deliberada y justificada.

El estado global de una asignatura no puede ser superior al de sus dominios nucleares.

## Criterios que no demuestran completitud

Por sí solos, los siguientes indicadores no permiten declarar una asignatura completa:

- número de palabras;
- número de unidades;
- duración declarada;
- cantidad de referencias;
- presencia de ecuaciones;
- aprobación de sintaxis JSON;
- ausencia de párrafos duplicados;
- ejecución exitosa de CI;
- existencia de un proyecto final.

Estos controles son necesarios para integridad editorial y técnica, pero no sustituyen una auditoría disciplinar.

## Política de extensión

- No existe máximo de palabras por unidad o curso.
- No se expandirá contenido con repetición, paráfrasis redundante o relleno.
- Un tema complejo puede dividirse en capítulos, anexos o módulos suplementarios.
- La ruta de 16 semanas representa una secuencia docente, no un límite para el corpus.
- La claridad tiene prioridad sobre la brevedad y la exhaustividad tiene prioridad sobre una estructura uniforme.

## Revisión externa

La transición de `review` a `complete` requiere:

1. revisión por una persona experta;
2. matriz de cobertura sin dominios nucleares `missing` o `partial`;
3. verificación de fuentes y afirmaciones;
4. revisión de problemas, soluciones y evaluaciones;
5. comprobación de materiales prácticos;
6. registro de fecha, alcance, revisor y cambios solicitados.
