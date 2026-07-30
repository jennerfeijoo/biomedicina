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
scientific_editorial_audit: passed_with_corrections_applied
unresolved_critical_findings: 0
unresolved_major_findings: 0
provisional_authoring_authorized: true
authoring_authorization_status: controlled_authoring_authorized
full_theory_drafting_authorized_provisionally: true
external_professional_review: pending_human_review
authoral_source_status: present
unit_authoral_file_current: present_internal_review
authoral_unit_status: authored_internal_review_pending_external_verification
authoral_theory_sections: 6
authoral_minimum_theory_words: 2200
authoral_glossary_terms: 20
authoral_worked_examples: 3
authoral_source_count: 12
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
- gates permanentes con fixtures de dominio y diagnóstico;
- auditoría científica-editorial interna con seis hallazgos resueltos;
- autorización provisional separada para autoría controlada de la Unidad 2.

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

## Auditoría científica y editorial interna

La auditoría conjunta de U2-P1 a U2-P3, U2-A1 a U2-A5 y las doce rutas de feedback fue aprobada con correcciones aplicadas. El registro estructurado es:

```text
data/course_audits/bioinstrumentacion/UNIT_02_PRACTICES_ASSESSMENT_SCIENTIFIC_EDITORIAL_AUDIT_2026-07-29.json
```

El gate permanente es:

```text
scripts/validate_bioinstrumentation_u2_scientific_editorial_audit.py
```

La auditoría resolvió la separación entre carga eléctrica y transferencia mecánica, precisó el alcance del rechazo del modelo simple de primer orden, corrigió una ruta diagnóstica no sustentada, añadió trazabilidad evaluación–evidencia y bloqueó la distribución pública de claves. No aporta evidencia humana ni autorización de teoría o publicación.

## Autorización provisional de autoría controlada

El propietario indicó continuar después de la auditoría interna y autorizó provisionalmente la producción de un borrador autoral controlado. El registro autoritativo es:

```text
data/authoring_authorizations/bioinstrumentacion-unit-02-provisional.json
```

La documentación y el gate permanente son:

```text
docs/pilots/bioinstrumentacion/unit-02/PROVISIONAL_AUTHORING_AUTHORIZATION.md
scripts/validate_bioinstrumentation_u2_provisional_authorization.py
```

La autorización permite crear el directorio fuente modular, redactar la teoría completa, integrar prácticas y evaluaciones existentes, construir `unit-02.json` como borrador interno y ejecutar validación determinista. Se limita al commit `a29fcedce078de03976970cdb8ce21a10b300245` y a las seis correcciones de auditoría.

Esta autorización es un `project_owner_continuation_override`: no constituye revisión profesional, evidencia humana, autorización de publicación ni cambio del estado externo `pending_human_review`.

## Borrador autoral completo

La fuente modular y el artefacto canónico interno son:

```text
data/course_redevelopment/bioinstrumentacion/unit-02-source
data/course_redevelopment/bioinstrumentacion/units/unit-02.json
```

El constructor, el validador y la documentación de implementación son:

```text
scripts/build_bioinstrumentation_u2_authoral_unit.py
scripts/validate_bioinstrumentation_u2_authoral_unit.py
docs/pilots/bioinstrumentacion/unit-02/AUTHORAL_UNIT_IMPLEMENTATION.md
```

El borrador contiene seis secciones teóricas con al menos 2.200 palabras, veinte términos de glosario, tres ejemplos razonados, cinco actividades alineadas, doce errores conceptuales, doce preguntas de autoevaluación, cinco conexiones biomédicas limitadas, tres prácticas ejecutables y doce fuentes localizadas. Integra las seis correcciones de la auditoría previa y mantiene las claves de evaluación fuera del contenido destinado al estudiante.

La evidencia humana continúa pendiente. El curso permanece `pending`, la publicación continúa bloqueada y el archivo no debe incorporarse a la generación pública mientras no existan revisión profesional, prueba cognitiva, revisión de usabilidad y concordancia documentadas.

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
- crear `data/course_redevelopment/bioinstrumentacion/unit-02-source`;
- crear `data/course_redevelopment/bioinstrumentacion/units/unit-02.json` como borrador interno;
- redactar la teoría completa con fuentes localizadas, supuestos y límites;
- integrar prácticas, evaluaciones, feedback y recuperación;
- crear un constructor determinista y un validador autoral específico;
- corregir el borrador mediante gates internos sin publicarlo ni promover el curso.

## Qué no está autorizado

- publicar una página nueva o exponer el borrador como contenido completado;
- promover el curso a `developed` o `complete`;
- usar datos de personas, muestras o conexión de sensores a sujetos;
- operar equipos clínicos;
- puntuar automáticamente razonamientos abiertos;
- distribuir claves de evaluación en recursos públicos;
- presentar especificaciones de fabricante como validación de una cadena;
- declarar utilidad clínica, conformidad normativa, seguridad o aprobación profesional;
- fabricar prueba cognitiva, revisión de usabilidad, concordancia o revisión profesional.

## Gate antes de autoría completa

El gate histórico exigía: **Preparar una autorización provisional separada** para la redacción controlada. Esa transición ya quedó materializada mediante el registro y el validador indicados arriba. El gate actual habilita únicamente la creación del borrador autoral interno y no satisface los gates de publicación, promoción, prueba cognitiva o revisión profesional.

## Gates posteriores a la autoría controlada

Antes de declarar la unidad desarrollada o publicarla todavía se requiere:

- mantener vigentes las correcciones y el gate de auditoría científica y editorial;
- auditar científicamente el borrador autoral completo;
- ejecutar una prueba cognitiva con estudiantes;
- revisar usabilidad del feedback y concordancia entre revisores;
- revisar continuidad pedagógica y suficiencia de fuentes;
- mantener bloqueadas publicación y promoción;
- completar revisión profesional externa mediante evidencia humana válida.

## Próximo bloque recomendado

Ejecutar una auditoría científica y editorial del borrador autoral completo, verificando teoría, ejemplos, glosario, continuidad pedagógica, trazabilidad y coherencia con las prácticas y evaluaciones. La auditoría seguirá siendo interna y no modificará `pending_human_review`, la publicación ni el estado del curso.
