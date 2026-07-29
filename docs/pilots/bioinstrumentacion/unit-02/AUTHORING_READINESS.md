# Readiness de autoría · Bioinstrumentación Unidad 2

## Estado

```text
preparation_status: authoring_preparation_review
technical_blockers_resolved: true
review_handoff: ready_pending_external_review
course_editorial_state: pending
unit_authoral_file: absent
practice_implementation_authorized_provisionally: true
u2_practices_implemented: true
practice_implementation_status: implemented_internal_review
assessment_implementation_status: implemented_internal_review
machine_scored_assessments: U2-A2, U2-A3, U2-A4
human_scored_assessments: U2-A1, U2-A5
automatic_semantic_grading: false
external_professional_practice_authorization: false
full_theory_drafting_authorized: false
unit_developed: false
public_release_authorized: false
disciplinary_review: pending_human_review
student_cognitive_test: pending
feedback_usability_review: pending
```

## Material disponible

- contrato estructurado de preparación;
- cinco resultados de aprendizaje observables;
- modelo conceptual de 17 nodos y 12 relaciones;
- tres casos limitados: termistor, galga extensométrica y fotodiodo;
- doce errores conceptuales con feedback recuperativo completo;
- cinco evaluaciones implementadas;
- registros de fuentes y especificación visual;
- bloqueos técnicos estáticos, dinámicos, documentales y de carga resueltos;
- handoff disciplinar con manifiesto determinista y plantilla de decisión;
- autorización provisional del propietario para prácticas internas;
- implementación ejecutable de U2-P1, U2-P2 y U2-P3;
- evaluación estructurada de curvas, dinámica y mecanismos de carga;
- rúbricas humanas para clasificación funcional y transferencia multicriterio;
- gates permanentes con fixtures de dominio y diagnóstico.

## Implementación de prácticas

El contrato autoritativo es:

```text
data/practice_implementations/bioinstrumentacion-unit-02.json
```

La documentación se encuentra en:

```text
docs/pilots/bioinstrumentacion/unit-02/PRACTICE_IMPLEMENTATION.md
```

La validación permanente se ejecuta mediante:

```text
scripts/validate_bioinstrumentation_u2_practices.py
```

### U2-P1

Implementa cuatro familias sintéticas: control lineal, saturación, zona muerta e histéresis. El gate recupera `K`, `b` y `2*h`, verifica sensibilidad local decreciente y demuestra que un ajuste agrupado no elimina residuos sistemáticos por rama.

### U2-P2

Implementa un primer orden lineal con actualización discreta exacta, estimación de `tau` y relación limitada con `f_c`. Rechaza retardo puro, segundo orden subamortiguado y curvas sin eje temporal.

### U2-P3

Audita metadatos compactos de `NTCLG100E2103JB`, `CEA-06-125UNA-350` y `S5821-03`. Conserva condiciones y categorías, mantiene no resuelto el factor de galga específico del lote y rechaza valores típicos convertidos en garantías.

## Implementación de evaluación y feedback

El contrato es:

```text
data/assessment_implementations/bioinstrumentacion-unit-02.json
```

El banco de doce rutas diagnósticas es:

```text
data/assessment_implementations/bioinstrumentacion-unit-02-feedback.json
```

La documentación y el gate son:

```text
docs/pilots/bioinstrumentacion/unit-02/ASSESSMENT_IMPLEMENTATION.md
scripts/validate_bioinstrumentation_u2_assessment.py
```

Las evaluaciones automáticas solo aceptan campos estructurados y deterministas. `U2-A1` y `U2-A5` requieren puntuación por rúbrica humana; el motor suma puntos y libera feedback, pero no realiza puntuación semántica automática.

La retroalimentación se libera por intentos y no expone patrones, decisiones, rutas causales, valores objetivo, claves completas ni respuestas modelo.

## Handoff disciplinar

El contrato externo permanece en:

```text
data/review_handoffs/bioinstrumentacion-unit-02.json
```

La revisión profesional operativa continúa en el issue `#161`. Las prácticas y evaluaciones internas no crean un manifiesto ni una decisión humana, no cambian `pending_human_review` y no deben presentarse como `approve_for_practice_implementation`.

## Qué está autorizado

- ejecutar y revisar U2-P1, U2-P2 y U2-P3;
- ejecutar U2-A2, U2-A3 y U2-A4 sobre respuestas estructuradas;
- aplicar rúbricas humanas de U2-A1 y U2-A5;
- regenerar salidas en `build/` o directorios temporales;
- mejorar reproducibilidad, controles negativos, feedback y documentación;
- preparar una auditoría científica y editorial conjunta de prácticas y evaluaciones.

## Qué no está autorizado

- crear `data/course_redevelopment/bioinstrumentacion/units/unit-02.json`;
- redactar la teoría completa;
- publicar una página nueva;
- promover el curso a `developed` o `complete`;
- usar datos de personas, muestras o conexión de sensores a sujetos;
- operar equipos clínicos;
- puntuar automáticamente razonamientos abiertos;
- presentar especificaciones de fabricante como validación de una cadena;
- declarar utilidad clínica, conformidad normativa, seguridad o aprobación profesional.

## Gate antes de autoría completa

Aún se requiere:

- realizar auditoría científica y editorial de prácticas, evaluaciones y feedback;
- ejecutar una prueba cognitiva con estudiantes;
- revisar usabilidad del feedback y concordancia entre revisores;
- revisar continuidad pedagógica y suficiencia de fuentes;
- obtener una autorización separada para redacción controlada;
- mantener bloqueadas publicación y promoción;
- completar revisión profesional externa mediante evidencia humana válida.

## Próximo bloque recomendado

Auditar científicamente y editorialmente la implementación conjunta de U2-P1 a U2-P3 y U2-A1 a U2-A5. La auditoría debe verificar exactitud, trazabilidad, alineación, ausencia de filtración de respuestas y suficiencia de los límites antes de considerar una autorización de autoría. La teoría completa y la publicación continúan bloqueadas.
