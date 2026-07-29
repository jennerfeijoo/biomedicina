# Readiness de autoría — Bioinstrumentación, Unidad 1

**Estado de preparación base:** `authoring_preparation_review`  
**Workstream de prácticas:** `practice_implementation_review`  
**Workstream de evaluación:** `assessment_implementation_review`  
**Workstream de revisión humana:** `human_review_protocol_ready`  
**Workstream de handoff disciplinar:** `disciplinary_review_handoff_ready`  
**Autorización provisional de autoría:** `controlled_authoring_authorized`  
**Borrador autoral completo:** `implemented_internal_review`  
**Estado editorial del curso:** `pending`  
**Unidad desarrollada:** no  
**Fecha:** 29 de julio de 2026

## Decisión

**bloqueos técnicos resueltos:** caso de presión, modelo térmico sintético y registro de PhysioNet.

La Unidad 1 dispone ahora de alcance, modelo conceptual, teoría completa, ejemplos, prácticas, evaluación, feedback, recuperación y fuentes localizadas. El contenido se mantiene en fragmentos auditables y se compila de forma determinista a `data/course_redevelopment/bioinstrumentacion/units/unit-01.json`.

Como estado histórico del handoff externo, la teoría completa todavía **no está autorizada** por una revisión disciplinar profesional. Posteriormente, el propietario del proyecto aceptó provisionalmente las revisiones internas de la IA y autorizó la redacción controlada. Esta autorización permitió producir el borrador autoral, mientras la revisión profesional externa sigue pendiente y el curso permanece `pending`.

La evidencia humana continúa pendiente: no se han ejecutado la revisión profesional externa, la prueba cognitiva ni la ronda real de acuerdo entre revisores.

La autorización y la existencia del borrador no equivalen a evidencia humana, aprobación profesional o validación institucional. La publicación continúa bloqueada. Tampoco se permite marcar la unidad como desarrollada, promover el curso o afirmar validación clínica o regulatoria.

## Artefactos principales

- `data/unit_preparation/bioinstrumentacion-unit-01.json`
- `data/unit_preparation/bioinstrumentacion-unit-01-blocker-resolution.json`
- `data/practice_implementations/bioinstrumentacion-unit-01.json`
- `data/assessment_implementations/bioinstrumentacion-unit-01.json`
- `data/assessment_implementations/bioinstrumentacion-unit-01-feedback.json`
- `data/review_protocols/bioinstrumentacion-unit-01-human-review.json`
- `data/review_handoffs/bioinstrumentacion-unit-01.json`
- `data/authoring_authorizations/bioinstrumentacion-unit-01-provisional.json`
- `data/course_redevelopment/bioinstrumentacion/unit-01-source/`
- `data/course_redevelopment/bioinstrumentacion/units/unit-01.json`
- `scripts/build_bioinstrumentation_u1_authoral_unit.py`
- `scripts/validate_bioinstrumentation_u1_authoral_unit.py`
- `docs/pilots/bioinstrumentacion/unit-01/AUTHORAL_UNIT_IMPLEMENTATION.md`
- `docs/pilots/bioinstrumentacion/unit-01/SOURCE_DOSSIER.md`
- `docs/pilots/bioinstrumentacion/unit-01/CONCEPT_AND_VISUAL_MODEL.md`
- `docs/pilots/bioinstrumentacion/unit-01/ASSESSMENT_AND_FEEDBACK_BLUEPRINT.md`
- `docs/pilots/bioinstrumentacion/unit-01/MISCONCEPTION_COMPLETION.md`
- `docs/pilots/bioinstrumentacion/unit-01/PRACTICE_AND_DATA_PLAN.md`
- `docs/pilots/bioinstrumentacion/unit-01/PRESSURE_CASE_RESOLUTION.md`
- `docs/pilots/bioinstrumentacion/unit-01/THERMAL_MODEL_RESOLUTION.md`
- `docs/pilots/bioinstrumentacion/unit-01/PHYSIONET_RECORD_100_SPEC.md`
- `docs/pilots/bioinstrumentacion/unit-01/PRACTICE_IMPLEMENTATION.md`
- `docs/pilots/bioinstrumentacion/unit-01/ASSESSMENT_IMPLEMENTATION.md`
- `docs/pilots/bioinstrumentacion/unit-01/COGNITIVE_TEST_PROTOCOL.md`
- `docs/pilots/bioinstrumentacion/unit-01/INTER_RATER_AGREEMENT_PROTOCOL.md`
- `docs/pilots/bioinstrumentacion/unit-01/DISCIPLINARY_REVIEW_REQUEST.md`
- `docs/pilots/bioinstrumentacion/unit-01/REVIEW_HANDOFF_AND_AUTHORIZATION.md`
- `docs/pilots/bioinstrumentacion/unit-01/PROVISIONAL_AUTHORING_AUTHORIZATION.md`

## Borrador autoral completo

El borrador contiene seis secciones teóricas sustantivas, cada una con formalización, supuestos, límites y localizadores. Cubre:

1. especificación del mensurando;
2. separación entre fenómeno, señal, indicación, valor medido y resultado;
3. sistema, cadena, fronteras y metadatos;
4. modelo, entradas, influencias y correcciones;
5. calibración y trazabilidad de resultados específicos;
6. aptitud para el uso y límites de inferencia.

La implementación incluye veinte términos de glosario, tres ejemplos razonados, cinco actividades alineadas con `U1-A1` a `U1-A5`, trece errores correspondientes exactamente al banco de misconceptions, doce preguntas de autoevaluación, cinco conexiones biomédicas limitadas y ocho fuentes directamente verificadas.

El compilador exige el inventario exacto de fragmentos, rechaza campos duplicados y produce bytes deterministas. El validador impone un mínimo de 2.200 palabras teóricas, densidad por párrafo, unicidad, correspondencia con prácticas y evaluación, y bloqueo de efectos editoriales no autorizados.

## Aspectos resueltos

### Alcance y modelo conceptual

La unidad distingue fenómeno, cantidad, mensurando, método, ruta de señal, modelo de medición, indicación, valor medido, resultado, influencia, corrección, incertidumbre, trazabilidad y aptitud para el uso. No invade procesamiento avanzado, normativa, diseño clínico ni interpretación diagnóstica.

### Evaluación y feedback

Los cinco resultados tienen evidencia observable, criterio de dominio, errores críticos y recuperación. Trece misconceptions cuentan con diagnóstico, explicación, dos pistas graduadas, actividad de recuperación distinta y criterio objetivo para continuar.

La implementación ejecutable incorpora:

- 18 ítems de clasificación con diez categorías;
- cuatro afirmaciones de trazabilidad;
- 13 rutas de feedback estructuradas;
- liberación progresiva por intento;
- rechazo explícito de calificación semántica automática para respuestas abiertas;
- rúbricas humanas con criterios críticos para `U1-A2`, `U1-A3` y `U1-A5`.

CI comprueba que el feedback no revela `correct_category`, `expected_decision`, una clave de respuesta ni una solución completa. Esta validación no sustituye una prueba de usabilidad con estudiantes.

### Protocolos humanos

La prueba cognitiva está formalizada para estudiar comprensión de instrucciones, selección de respuesta, utilidad de pistas y transferencia. El acuerdo entre revisores incluye puntuación ordinal 0–2, acuerdo exacto, diferencia absoluta media, kappa ponderado lineal, análisis separado de flags críticos, matriz de confusión y controles sintéticos positivo y negativo.

Las plantillas vacías prohíben identificadores directos, datos clínicos y respuestas reales dentro del repositorio. Las sesiones y rondas reales no se han ejecutado.

### Handoff disciplinar

El handoff dispone de contrato de artefactos, manifiesto SHA-256, plantilla de decisión, evaluador de autorización y rechazo de aprobaciones sintéticas. Mantiene `pending_human_review`; no existe respaldo disciplinar externo en `data/review_evidence/`.

### Autorización provisional de autoría

El registro `data/authoring_authorizations/bioinstrumentacion-unit-01-provisional.json` documenta un `project_owner_override` que autoriza crear el borrador, revisar sus componentes y ejecutar gates internos.

No autoriza publicación, estado `developed`, promoción del curso, estado `complete`, afirmaciones de respaldo profesional o validación clínica o regulatoria.

### Caso de presión

**Resuelto internamente para autoría.** Diferencia presión intravascular en sitio y referencia especificados, estimación auscultatoria braquial y estimación oscilométrica dependiente del algoritmo. No equipara presión del manguito, PPG, tiempo de tránsito o una salida numérica con presión arterial directa.

### Modelo térmico

**Implementado y validado técnicamente.** Distingue `T_u`, `T_d`, `T_s` e indicación con offset y ruido. La aproximación de primer orden tiene pruebas de determinismo, convergencia, constante de tiempo, monotonía y ausencia de sobreimpulso ideal. No se presenta como modelo fisiológico validado.

### PhysioNet

**Implementado y fijado offline.** La práctica usa un fixture atribuido de `100.hea`, MIT-BIH v1.0.0, registro 100. Valida dos canales, `360 Hz`, `650000` muestras, formato `212`, etiquetas `MLII` y `V5`, sin descargar `100.dat` ni interpretar señales.

### Reproducibilidad

Las prácticas, evaluadores, calculador de acuerdo, generadores de manifiestos y compilador autoral usan la biblioteca estándar de Python. CI trabaja sin red, genera resultados temporales y rechaza contratos inconsistentes.

### Fuentes

La base se apoya en VIM3, JCGM GUM-1:2023, JCGM GUM-6:2020, NIST TN 2156, AHA para delimitar métodos de presión, literatura sobre termometría de contacto y documentación oficial de PhysioNet. Cada fuente del borrador tiene localizadores y una función declarada.

## Riesgos abiertos

1. Falta revisión disciplinar humana por una persona competente en metrología e instrumentación biomédica.
2. Falta ejecutar la prueba cognitiva con una persona del perfil objetivo.
3. Falta revisar empíricamente la usabilidad y dificultad de las pistas y problemas de recuperación.
4. Falta ejecutar una ronda independiente con dos revisores y resolver sus desacuerdos.
5. Las prácticas están validadas técnicamente, pero aún no han sido probadas por estudiantes ni revisadas externamente.
6. El borrador autoral debe someterse a verificación profesional antes de publicación o promoción editorial.

## Gate antes de redactar teoría completa

- [x] Alcance y exclusiones definidos.
- [x] Resultados y evidencias alineados.
- [x] Modelo conceptual y visual especificado.
- [x] Trece misconceptions y feedback diseñados.
- [x] Prácticas seguras y reproducibles planificadas.
- [x] Afirmaciones centrales vinculadas a fuentes directas.
- [x] Revisión interna del caso de presión arterial.
- [x] Revisión interna del modelo térmico.
- [x] Registro de PhysioNet fijado y comprobado documentalmente.
- [x] Dos prácticas implementadas y ejecutadas en un entorno limpio de CI.
- [x] Evaluación cerrada y feedback recuperativo implementados y probados en CI.
- [x] Protocolo de prueba cognitiva formalizado.
- [x] Protocolo de acuerdo entre revisores formalizado.
- [x] Handoff disciplinar y gate de autorización formalizados.
- [x] Override provisional del propietario registrado para autoría controlada.
- [x] Borrador autoral completo generado y auditado internamente.
- [ ] Ejecución de prueba cognitiva con participante humano.
- [ ] Ejecución de ronda independiente con dos revisores.
- [ ] Revisión disciplinar humana inicial.

## Gate antes de considerar la unidad desarrollada

- [x] teoría completa con fuentes y localizadores;
- [x] al menos dos ejemplos razonados y un caso de transferencia no resuelto previamente;
- [x] prácticas implementadas y ejecutadas técnicamente;
- [x] validación automática del paquete autoral;
- [ ] prácticas revisadas pedagógicamente con usuarios;
- [ ] rúbricas y feedback probados con usuarios y revisores;
- [ ] revisión profesional de exactitud científica y terminología;
- [ ] verificación de accesibilidad con perfil objetivo;
- [ ] revisión humana documentada del bloque.

La ausencia de los cinco últimos elementos impide declarar la unidad `developed` o publicarla.

## Gate antes de `complete`

`complete` exige revisión disciplinar externa documentada del curso, resolución de observaciones, auditoría de continuidad entre unidades y evidencia de autonomía real. No se alcanza mediante conteos, generación automática, override provisional o CI.

## Resultado editorial

Después de fusionar este bloque:

- Bioinstrumentación seguirá en `pending`;
- existirá un borrador autoral canónico en estado `review`;
- la publicación continuará bloqueada;
- las unidades fallback públicas no serán sustituidas automáticamente;
- dos prácticas seguirán ejecutables y auditables offline;
- la evaluación cerrada y el feedback seguirán ejecutables;
- las respuestas abiertas seguirán bajo rúbrica humana;
- la revisión disciplinar, la prueba cognitiva y el acuerdo real seguirán abiertos;
- el borrador no podrá presentarse como desarrollado, publicado o profesionalmente validado.
