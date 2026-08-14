# Roadmap CitoNauta

## Estado de ejecución — 14 de agosto de 2026

CitoNauta dispone de una fábrica editorial, un catálogo navegable y controles técnicos reproducibles. El inventario actual contiene **94 asignaturas**, **617 unidades** y **9 rutas interdisciplinarias**.

La disponibilidad de archivos no se interpreta como validez científica:

- las 94 asignaturas tienen material lectivo disponible;
- 50 cursos conservan marcadores de plantilla en 298 unidades;
- 44 cursos no contienen esos marcadores conocidos, sin que esto demuestre validez;
- ninguna asignatura dispone todavía de un registro completo afirmación–fuente;
- ningún sistema revisor IA tiene aún estado `validated_for_scope`;
- ninguna asignatura puede presentarse como científicamente validada o `complete`.

## 1. Objetivo

Construir una plataforma abierta de estudio independiente en biomedicina que combine:

- lenguaje académico con explicaciones sencillas;
- rutas adaptables y prerrequisitos explícitos;
- práctica, evaluación, recuperación y transferencia;
- afirmaciones científicas trazables;
- revisión por IA con validez empíricamente demostrada;
- cuentas, progreso versionado y logros asociados a evidencia.

## 2. Modelo editorial multidimensional

El catálogo no reduce la madurez a una sola etiqueta. Informa por separado:

| Dimensión | Pregunta |
|---|---|
| Material | ¿Existe contenido utilizable? |
| Especificidad | ¿Conserva texto de plantilla conocido? |
| Fuentes | ¿Las afirmaciones tienen fuente y localizador? |
| Revisión | ¿La decisión es provisional o validada? |
| Validez del revisor | ¿La configuración fue validada para este alcance? |
| Evidencia educativa | ¿Se estudió aprendizaje, transferencia y retención? |

`complete` solo puede utilizarse cuando coinciden contenido trazable, revisión `ai_review_validated`, registro `validated_for_scope` vigente y ausencia de hallazgos bloqueantes.

## 3. Gate 0 — Veracidad y control científico

### Implementado en la transición actual

- inventario público corregido a 94 asignaturas y 617 unidades;
- detección reproducible de plantillas conocidas;
- estados multidimensionales en el catálogo;
- protocolo de equivalencia o no inferioridad IA–humano;
- manifiesto versionado de validez del revisor;
- estado provisional para el revisor actual;
- bloqueo del `auto_merge` sin revisor validado;
- registro estructurado de afirmaciones y localizadores;
- migración conceptual de los gates humanos del piloto.

### Trabajo pendiente del Gate 0

1. Normalizar el vocabulario de las fuentes existentes.
2. Construir registros de afirmaciones para los cursos piloto.
3. Recuperar texto completo autorizado y localizadores.
4. Congelar corpus, modelo, prompt, rúbrica y análisis.
5. Ejecutar el estudio ciego IA–humano.
6. Publicar resultados e incertidumbre.
7. Activar `validated_for_scope` únicamente si se supera el criterio predefinido.

## 4. Gate 1 — Producto de estudio independiente

El MVP debe incluir:

- registro, inicio de sesión, recuperación y modo invitado;
- progreso sincronizado por resultado de aprendizaje;
- intentos, respuestas, pistas, feedback y reintentos;
- estados `not_started`, `exploring`, `practiced`, `mastered` y `needs_review`;
- logros vinculados a criterio, evidencia y versión;
- exportación y borrado de datos;
- aislamiento por usuario y pruebas de privacidad;
- recorrido crítico conforme con WCAG 2.2 AA.

No se marcará dominio por desplazamiento, tiempo de pantalla o simple visita.

## 5. Gate 2 — Pilotos científicos

Orden recomendado:

1. Bioestadística;
2. Fundamentos de Programación;
3. Bioinformática;
4. Aprendizaje Automático Biomédico y Validación Clínica;
5. Descubrimiento Computacional de Fármacos.

Cada piloto requiere:

- matriz competencia–unidad–evaluación;
- afirmaciones localizadas;
- ejercicios ejecutables y tests;
- datos abiertos o sintéticos con licencia;
- revisión ciega paralela IA–humano;
- comparación IA–humano, humano–humano e IA–IA;
- prueba de claridad del lenguaje;
- medición de aprendizaje, transferencia y retención;
- publicación de resultados negativos y limitaciones.

## 6. Gate 3 — Escalamiento

Después de validar un curso completo:

- reconstruir los 50 cursos con plantilla detectada;
- curar las conexiones curriculares faltantes;
- consolidar workflows repetidos;
- revalidar fuentes según fecha y riesgo;
- mantener un registro de cambios científicos;
- ampliar la validez del revisor por disciplina y riesgo;
- emitir logros interoperables solo cuando sus criterios estén validados.

## 7. Indicadores

### Científicos

- cobertura de localizadores por riesgo;
- sensibilidad y falsos negativos para errores críticos;
- no inferioridad con intervalo de confianza;
- acuerdo humano–humano, IA–humano e IA–IA;
- estabilidad, abstención y detección fuera de alcance;
- tiempo de corrección de fuentes retiradas o actualizadas.

### Educativos

- desempeño diagnóstico, inmediato y diferido;
- transferencia a problemas nuevos;
- errores antes y después del feedback;
- abandono y motivo declarado;
- diferencias por base inicial y necesidades de accesibilidad.

### Producto

- éxito al encontrar, retomar y practicar;
- errores de sincronización;
- incidentes de aislamiento de datos;
- accesibilidad de tareas críticas;
- logros con evidencia verificable y versión vigente.

## 8. Regla operativa

El siguiente hito no es añadir más volumen. Es completar un curso piloto capaz de responder de forma auditable:

1. qué debe aprender la persona;
2. qué evidencia respalda cada afirmación importante;
3. qué actividad demuestra dominio;
4. qué sistema autorizó la versión y para qué alcance estaba validado.
