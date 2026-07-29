# Readiness de autoría · Bioinstrumentación Unidad 2

## Estado

```text
preparation_status: authoring_preparation_review
technical_blockers_resolved: true
review_handoff: ready_pending_external_review
course_editorial_state: pending
unit_authoral_file: absent
practice_implementation_authorized_provisionally: true
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
- doce errores conceptuales;
- cinco evaluaciones alineadas;
- tres prácticas planificadas sin datos humanos;
- registro de once fuentes directamente consultadas;
- especificación visual con errores prohibidos;
- cuatro generadores estáticos deterministas;
- modelo dinámico de primer orden con controles positivos y negativos;
- tres componentes exactos fijados para auditoría documental;
- cuatro casos de carga seguros;
- handoff disciplinar con manifiesto determinista y plantilla de decisión;
- autorización provisional del propietario para la implementación interna de U2-P1, U2-P2 y U2-P3.

## Bloqueos técnicos resueltos

1. **Caracterización estática:** se fijaron generadores para control lineal, saturación, zona muerta e histéresis, con semilla, ecuaciones, parámetros y pruebas de aceptación.
2. **Dinámica:** se fijó el primer orden lineal, la actualización discreta exacta, las tolerancias y los controles de rechazo para retardo puro, segundo orden subamortiguado y ausencia de tiempo.
3. **Relación tiempo–frecuencia:** `f_c = 1/(2πτ)` quedó limitada al primer orden lineal y al criterio de −3 dB.
4. **Carga:** se formalizaron rutas térmica, mecánica, eléctrica y óptica sin adquisición humana.
5. **Componentes:** se fijaron `NTCLG100E2103JB`, `CEA-06-125UNA-350` y `S5821-03`, conservando condición y categoría de cada especificación.

La resolución técnica permite implementar internamente las prácticas bajo la autorización provisional; no constituye aprobación humana ni autoriza teoría, publicación o promoción.

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

La autorización profesional será evaluada por:

```text
scripts/evaluate_bioinstrumentation_u2_practice_authorization.py
```

La revisión humana operativa permanece abierta en el issue `#161`. Hasta que existan un manifiesto y una decisión humana válidos, el estado profesional continúa `pending_human_review`.

## Autorización provisional de prácticas

El registro interno es:

```text
data/authoring_authorizations/bioinstrumentacion-unit-02-practices-provisional.json
```

Este registro interpreta la instrucción contextual del propietario de continuar como autorización limitada al siguiente bloque ya identificado: implementar y auditar internamente U2-P1, U2-P2 y U2-P3. No reemplaza el handoff profesional ni altera su estado.

## Qué está autorizado

- crear `data/practice_implementations/bioinstrumentacion-unit-02.json`;
- implementar U2-P1: banco sintético de características estáticas;
- implementar U2-P2: respuesta dinámica de primer orden;
- implementar U2-P3: auditoría comparativa de hojas de datos;
- crear generadores sintéticos y fixtures documentales;
- añadir controles positivos, negativos y pruebas de reproducibilidad;
- revisar documentación y gates internos;
- usar exclusivamente datos sintéticos o documentación de componentes.

## Qué no está autorizado

- crear `data/course_redevelopment/bioinstrumentacion/units/unit-02.json`;
- redactar la teoría completa;
- publicar una página nueva;
- promover el curso a `developed` o `complete`;
- usar datos de personas o conectar sensores a sujetos;
- operar equipos clínicos;
- presentar especificaciones de fabricante como validación del sistema;
- declarar utilidad clínica, conformidad normativa, seguridad o aprobación profesional.

## Gate antes de fusionar prácticas

La implementación deberá demostrar simultáneamente:

- datos exclusivamente sintéticos o documentales;
- semilla, parámetros, unidades y tolerancias versionados;
- ejecución sin red en CI;
- resultados deterministas;
- controles de aceptación y rechazo;
- separación entre patrón sintético y mecanismo físico;
- conservación de condiciones y categorías de especificación;
- salidas generadas no versionadas;
- ausencia de inferencias clínicas, regulatorias o de seguridad.

## Gate antes de autoría completa

Incluso después de implementar prácticas, seguirá siendo necesario:

- validar las prácticas implementadas y sus salidas deterministas;
- implementar evaluación y retroalimentación ejecutables;
- revisar continuidad pedagógica y fuentes de la teoría;
- obtener una autorización separada y explícita para redacción controlada;
- mantener bloqueadas publicación y promoción del curso;
- conservar pendiente la revisión profesional externa hasta que exista evidencia humana válida.

## Próximo bloque recomendado

Implementar U2-P1, U2-P2 y U2-P3 bajo la autorización provisional, con un contrato estructurado, scripts reproducibles y un gate permanente. La teoría completa y la publicación continúan bloqueadas.
