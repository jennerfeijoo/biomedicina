# Modelo de dependencias curriculares de CitoNauta

## Propósito

CitoNauta distingue entre tres clases de relación que no deben confundirse:

1. **Prerrequisitos descriptivos de una asignatura**: conocimientos, habilidades o experiencias que facilitan abordar su contenido. Se expresan en lenguaje natural dentro de cada curso.
2. **Dependencias curriculares explícitas**: relaciones entre asignaturas identificadas y justificadas en `data/prerequisite_graph.json`.
3. **Rutas interdisciplinarias**: agrupaciones temáticas de `data/tracks.json` destinadas a descubrir conexiones. Compartir una ruta no implica dependencia.

La red explícita permite navegar el currículo, auditar relaciones, detectar ciclos y mostrar fundamentos o continuaciones posibles. No impone semestres, horas, plazos ni una secuencia única.

## Interpretación de una arista

Una relación `recommended_foundation` desde A hacia B significa:

> A contiene conceptos o métodos que facilitan abordar B, pero el estudiante puede demostrar ese dominio mediante otra asignatura, experiencia previa, estudio independiente o evaluación diagnóstica.

No significa:

- que A sea un requisito administrativo;
- que B deba iniciarse inmediatamente después de A;
- que completar A garantice dominio suficiente;
- que no existan otras bases útiles;
- que todas las personas necesiten el mismo recorrido.

## Criterios para incorporar relaciones

Una arista debe cumplir simultáneamente:

- **Dependencia conceptual identificable**: B utiliza de forma sustantiva conocimientos o métodos desarrollados en A.
- **Dirección justificable**: la relación no es solo una asociación temática simétrica.
- **Racional explícito**: cada arista explica por qué A facilita B.
- **Identificadores válidos**: origen y destino deben existir en `data/citonauta_curriculum.json`.
- **Ausencia de ciclos**: la red completa debe seguir siendo un grafo dirigido acíclico.
- **Prudencia editorial**: ante duda, se omite la arista hasta disponer de revisión suficiente.

## Cobertura deliberadamente incompleta

El mapa no intenta conectar artificialmente las 84 asignaturas. La ausencia de una relación significa que todavía no existe una dependencia curada con suficiente confianza. No debe interpretarse como evidencia de independencia.

Este criterio evita transformar similitud de vocabulario, proximidad profesional o pertenencia a una ruta en falsos prerrequisitos.

## Presentación pública

`mapa/index.html` permite seleccionar cualquier asignatura y visualizar:

- bases recomendadas directas;
- continuaciones directas;
- fundamentos acumulados por transitividad;
- desarrollos posteriores alcanzables;
- justificación de cada relación directa.

Las relaciones se muestran como orientación para aprendizaje basado en dominio. El mapa no sustituye requisitos institucionales de admisión, matrícula, homologación o certificación.

## Validación automática

`scripts/validate_prerequisite_graph.py` comprueba:

- existencia de todos los IDs;
- tipos de relación reconocidos;
- justificaciones mínimas;
- ausencia de duplicados y auto-dependencias;
- ausencia de ciclos;
- cobertura mínima de la red;
- presencia de relaciones entre áreas;
- existencia de la página y sus activos;
- ausencia de lenguaje temporal o de obligatoriedad no respaldada.

El validador se ejecuta en `CitoNauta Quality Gates`, junto con la comprobación sintáctica de `assets/js/prerequisite-map.js`.

## Revisión futura

Las nuevas relaciones deben añadirse de forma incremental y revisable. La prioridad es la validez de cada dependencia, no alcanzar un número máximo de aristas ni producir una apariencia de completitud.
