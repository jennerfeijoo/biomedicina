# Readiness de autoría · Bioinstrumentación Unidad 2

## Estado

```text
preparation_status: authoring_preparation_review
technical_blockers_resolved: true
review_handoff: ready_pending_external_review
course_editorial_state: pending
unit_authoral_file: absent
practice_implementation_authorized: false
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
- doce errores conceptuales;
- cinco evaluaciones alineadas;
- tres prácticas planificadas sin datos humanos;
- registro de once fuentes directamente consultadas;
- especificación visual con errores prohibidos;
- cuatro generadores estáticos deterministas;
- modelo dinámico de primer orden con controles positivos y negativos;
- tres componentes exactos fijados para auditoría documental;
- cuatro casos de carga seguros;
- handoff disciplinar con manifiesto determinista y plantilla de decisión.

## Bloqueos técnicos resueltos

1. **Caracterización estática:** se fijaron generadores para control lineal, saturación, zona muerta e histéresis, con semilla, ecuaciones, parámetros y pruebas de aceptación.
2. **Dinámica:** se fijó el primer orden lineal, la actualización discreta exacta, las tolerancias y los controles de rechazo para retardo puro, segundo orden subamortiguado y ausencia de tiempo.
3. **Relación tiempo–frecuencia:** `f_c = 1/(2πτ)` quedó limitada al primer orden lineal y al criterio de −3 dB.
4. **Carga:** se formalizaron rutas térmica, mecánica, eléctrica y óptica sin adquisición humana.
5. **Componentes:** se fijaron `NTCLG100E2103JB`, `CEA-06-125UNA-350` y `S5821-03`, conservando condición y categoría de cada especificación.

La resolución técnica permite solicitar revisión; no constituye aprobación humana ni autoriza implementación.

## Handoff disciplinar

El contrato de entrega es:

```text
data/review_handoffs/bioinstrumentacion-unit-02.json
```

El paquete puede congelarse mediante:

```text
scripts/build_bioinstrumentation_u2_review_packet.py
```

La decisión futura debe usar:

```text
data/review_templates/bioinstrumentacion/unit-02/disciplinary-review-decision-template.json
```

La autorización será evaluada por:

```text
scripts/evaluate_bioinstrumentation_u2_practice_authorization.py
```

Hasta que existan un manifiesto y una decisión humana válidos, el estado permanece `pending_human_review`.

## Qué está autorizado

- revisar alcance, resultados, modelos, componentes y fuentes;
- construir un manifiesto del paquete para un commit específico;
- entregar el paquete a una persona revisora competente;
- completar la plantilla mediante revisión humana real;
- ejecutar gates documentales y controles sintéticos de rechazo.

## Qué no está autorizado

- crear `data/practice_implementations/bioinstrumentacion-unit-02.json`;
- implementar U2-P1, U2-P2 o U2-P3 antes de aprobación humana válida;
- crear `data/course_redevelopment/bioinstrumentacion/units/unit-02.json`;
- redactar la teoría completa;
- publicar una página nueva;
- promover el curso a `developed` o `complete`;
- usar datos de personas o conectar sensores a sujetos;
- presentar especificaciones de fabricante como validación del sistema;
- declarar utilidad clínica, conformidad normativa o seguridad.

## Gate antes de implementar prácticas

Se requiere una decisión `approve_for_practice_implementation` que cumpla simultáneamente:

- persona revisora identificada con competencia suficiente;
- commit revisado válido;
- digest del paquete coincidente;
- puntuación mínima 4/5 en todas las dimensiones;
- ausencia de hallazgos críticos;
- ausencia de cambios obligatorios;
- confirmación humana verificable;
- rechazo explícito de registros sintéticos, plantillas y actores de CI.

## Gate antes de autoría completa

Incluso después de autorizar e implementar prácticas, seguirá siendo necesario:

- validar las prácticas implementadas y sus salidas deterministas;
- implementar evaluación y retroalimentación ejecutables;
- revisar continuidad pedagógica y fuentes de la teoría;
- obtener autorización explícita y limitada para redacción controlada;
- mantener bloqueadas publicación y promoción del curso.

## Próximo bloque recomendado

Obtener revisión disciplinar humana real sobre un commit y un manifiesto congelados. Solo una decisión válida podrá autorizar la implementación de U2-P1, U2-P2 y U2-P3; la teoría completa continuará bloqueada.
