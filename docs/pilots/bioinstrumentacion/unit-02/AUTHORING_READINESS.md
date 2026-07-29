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
external_professional_practice_authorization: false
full_theory_drafting_authorized: false
unit_developed: false
public_release_authorized: false
disciplinary_review: pending_human_review
```

## Material disponible

- contrato estructurado de preparación;
- cinco resultados de aprendizaje observables;
- modelo conceptual de 17 nodos y 12 relaciones;
- tres casos limitados: termistor, galga extensométrica y fotodiodo;
- doce errores conceptuales y cinco evaluaciones planificadas;
- registros de fuentes y especificación visual;
- bloqueos técnicos estáticos, dinámicos, documentales y de carga resueltos;
- handoff disciplinar con manifiesto determinista y plantilla de decisión;
- autorización provisional del propietario para prácticas internas;
- implementación ejecutable de U2-P1, U2-P2 y U2-P3;
- gate permanente con hashes dorados y controles negativos.

## Implementación de prácticas

El contrato autoritativo es:

```text
data/practice_implementations/bioinstrumentacion-unit-02.json
```

La documentación ejecutable se encuentra en:

```text
docs/pilots/bioinstrumentacion/unit-02/PRACTICE_IMPLEMENTATION.md
```

La validación permanente se ejecuta mediante:

```text
scripts/validate_bioinstrumentation_u2_practices.py
```

### U2-P1

Implementa cuatro familias sintéticas: control lineal, saturación, zona muerta e histéresis. El gate recupera `K`, `b` y `2*h`, verifica sensibilidad local decreciente y demuestra que un ajuste agrupado no elimina los residuos sistemáticos por rama.

### U2-P2

Implementa un primer orden lineal con actualización discreta exacta, estimación de `tau` y relación limitada con `f_c`. Rechaza retardo puro, segundo orden subamortiguado y curvas sin eje temporal.

### U2-P3

Audita metadatos compactos de `NTCLG100E2103JB`, `CEA-06-125UNA-350` y `S5821-03`. Conserva condiciones y categorías, mantiene no resuelto el factor de galga específico del lote y rechaza valores típicos convertidos en garantías.

## Handoff disciplinar

El contrato externo permanece en:

```text
data/review_handoffs/bioinstrumentacion-unit-02.json
```

La revisión profesional operativa continúa en el issue `#161`. La implementación interna no crea un manifiesto ni una decisión humana, no cambia `pending_human_review` y no debe presentarse como `approve_for_practice_implementation`.

## Qué está autorizado

- ejecutar y revisar U2-P1, U2-P2 y U2-P3;
- regenerar salidas en `build/` o directorios temporales;
- modificar generadores, fixture y gate dentro del alcance provisional;
- mejorar reproducibilidad, controles negativos y documentación;
- preparar el siguiente bloque de evaluación y retroalimentación.

## Qué no está autorizado

- crear `data/course_redevelopment/bioinstrumentacion/units/unit-02.json`;
- redactar la teoría completa;
- publicar una página nueva;
- promover el curso a `developed` o `complete`;
- usar datos de personas, muestras o conexión de sensores a sujetos;
- operar equipos clínicos;
- presentar especificaciones de fabricante como validación de una cadena;
- declarar utilidad clínica, conformidad normativa, seguridad o aprobación profesional.

## Gate antes de autoría completa

Aún se requiere:

- implementar evaluación y retroalimentación ejecutables;
- realizar auditoría científica y editorial de las prácticas y evaluaciones;
- revisar continuidad pedagógica y suficiencia de fuentes;
- obtener una autorización separada para redacción controlada;
- mantener bloqueadas publicación y promoción;
- completar revisión profesional externa mediante evidencia humana válida.

## Próximo bloque recomendado

Implementar el sistema de evaluación y retroalimentación de la Unidad 2, alineado con U2-P1, U2-P2 y U2-P3, sin crear todavía la unidad autoral. La teoría completa y la publicación continúan bloqueadas.
