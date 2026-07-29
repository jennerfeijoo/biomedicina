# Paquete de entrega y autorización · Bioinstrumentación Unidad 2

**Estado:** `ready_pending_external_review`  
**Decisión actual:** `pending_human_review`  
**Implementación de prácticas autorizada:** no  
**Teoría completa autorizada:** no  
**Estado editorial del curso:** `pending`

## Propósito

Este bloque convierte la solicitud de revisión disciplinar en un proceso ejecutable y auditable. Una persona revisora competente podrá congelar un conjunto explícito de artefactos, revisar exactamente ese contenido y emitir una decisión limitada sobre la implementación de las prácticas U2-P1, U2-P2 y U2-P3.

El handoff no implementa prácticas, no redacta teoría, no publica contenido y no desarrolla la unidad.

## Contrato autoritativo

El contrato se encuentra en:

```text
data/review_handoffs/bioinstrumentacion-unit-02.json
```

Define:

- los artefactos que forman el paquete;
- las categorías de competencia aceptadas;
- las dimensiones de puntuación;
- las decisiones posibles;
- la regla exacta de autorización;
- los límites editoriales que permanecen bloqueados.

## Congelación del paquete

El constructor:

```text
scripts/build_bioinstrumentation_u2_review_packet.py
```

recibe un commit de 40 caracteres y genera un manifiesto determinista con:

- ruta de cada artefacto;
- tamaño en bytes;
- hash SHA-256 individual;
- commit revisado;
- digest SHA-256 del paquete completo.

Ejemplo de ejecución futura:

```bash
python scripts/build_bioinstrumentation_u2_review_packet.py \
  --reviewed-commit <COMMIT_SHA> \
  --output data/review_evidence/bioinstrumentacion-unit-02-review-packet.json
```

El manifiesto SHA-256 congela el contenido sometido a revisión. No contiene evidencia humana y no puede aprobar nada por sí mismo.

## Registro de decisión

La plantilla se encuentra en:

```text
data/review_templates/bioinstrumentacion/unit-02/disciplinary-review-decision-template.json
```

La persona revisora debe completar una copia futura en:

```text
data/review_evidence/bioinstrumentacion-unit-02-disciplinary-review.json
```

La decisión debe identificar:

- nombre y contexto profesional suficiente;
- al menos dos categorías de competencia permitidas;
- nota de competencia;
- fecha;
- commit revisado;
- digest exacto del paquete;
- puntuaciones de 1 a 5;
- hallazgos críticos;
- cambios obligatorios;
- sugerencias no bloqueantes;
- confirmación verificable de que actuó una persona revisora.

No deben almacenarse datos personales innecesarios.

## Decisiones permitidas

### `approve_for_practice_implementation`

Autoriza exclusivamente implementar las prácticas:

- U2-P1: banco sintético de características estáticas;
- U2-P2: respuesta dinámica de primer orden;
- U2-P3: auditoría comparativa de hojas de datos.

Solo autoriza si todas las dimensiones obtienen al menos 4 de 5, no existen hallazgos críticos, no quedan cambios obligatorios y la evidencia humana coincide con el commit y el digest del manifiesto.

### `approve_with_changes`

Mantiene bloqueada la implementación hasta resolver y volver a revisar los cambios obligatorios.

### `do_not_approve`

Mantiene bloqueado el bloque de prácticas.

## Evaluador

El evaluador es:

```text
scripts/evaluate_bioinstrumentation_u2_practice_authorization.py
```

Ejemplo futuro:

```bash
python scripts/evaluate_bioinstrumentation_u2_practice_authorization.py \
  --manifest data/review_evidence/bioinstrumentacion-unit-02-review-packet.json \
  --decision data/review_evidence/bioinstrumentacion-unit-02-disciplinary-review.json \
  --require-authorization
```

La autorización solo puede resultar verdadera cuando coinciden:

1. handoff;
2. commit;
3. digest;
4. competencia;
5. puntuaciones;
6. decisión;
7. confirmación humana.

## Controles contra aprobación simulada

El repositorio incluye un fixture sintético que reclama aprobación con puntuaciones máximas. El gate exige que sea rechazado porque:

- `synthetic` es verdadero;
- `human_evidence` es falso;
- el actor es `ci_fixture`, no `human_reviewer`.

También verifica que `approve_with_changes` nunca autorice prácticas.

## Límite de autorización

Una decisión válida de este handoff:

- puede autorizar implementación reproducible de las tres prácticas;
- no autoriza la teoría completa;
- no crea `unit-02.json`;
- no publica páginas;
- no promueve el curso a `developed` o `complete`;
- no demuestra exactitud de un dispositivo real;
- no valida seguridad, conformidad normativa o utilidad clínica;
- no autoriza adquisición con personas, muestras o equipos clínicos.

Hasta que existan el manifiesto y la decisión humana válidos, el estado debe seguir siendo `pending_human_review` y `practice_implementation_authorized: false`.
