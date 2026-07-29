# Paquete de entrega y autorización · Bioinstrumentación Unidad 2

**Estado del handoff:** `ready_pending_external_review`  
**Decisión profesional actual:** `pending_human_review`  
**Implementación interna de prácticas:** `authorized_provisionally_by_project_owner`  
**Teoría completa autorizada:** no  
**Estado editorial del curso:** `pending`

## Propósito

Este bloque convierte la solicitud de revisión disciplinar en un proceso ejecutable y auditable. Una persona revisora competente podrá congelar un conjunto explícito de artefactos, revisar exactamente ese contenido y emitir una decisión limitada sobre la implementación de las prácticas U2-P1, U2-P2 y U2-P3.

El handoff no implementa prácticas, no redacta teoría, no publica contenido y no desarrolla la unidad. Una autorización provisional separada del propietario permite entretanto la implementación interna y controlada, sin alterar el estado profesional del handoff.

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
- la regla exacta de autorización profesional;
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

Autoriza profesionalmente y exclusivamente implementar las prácticas:

- U2-P1: banco sintético de características estáticas;
- U2-P2: respuesta dinámica de primer orden;
- U2-P3: auditoría comparativa de hojas de datos.

Solo autoriza si todas las dimensiones obtienen al menos 4 de 5, no existen hallazgos críticos, no quedan cambios obligatorios y la evidencia humana coincide con el commit y el digest del manifiesto.

### `approve_with_changes`

Mantiene bloqueada la autorización profesional hasta resolver y volver a revisar los cambios obligatorios.

### `do_not_approve`

Mantiene bloqueada la autorización profesional del bloque de prácticas.

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

La autorización profesional solo puede resultar verdadera cuando coinciden:

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

También verifica que `approve_with_changes` nunca produzca autorización profesional.

## Autorización provisional del propietario

El registro separado es:

```text
data/authoring_authorizations/bioinstrumentacion-unit-02-practices-provisional.json
```

Su estado es:

```text
authorized_for_controlled_practice_implementation_provisionally
```

Este override interno permite implementar y probar U2-P1, U2-P2 y U2-P3 con datos exclusivamente sintéticos o documentales. Se basa en la instrucción contextual del propietario de continuar el siguiente bloque previamente identificado.

No cambia el contenido de `data/review_handoffs/bioinstrumentacion-unit-02.json`, no crea una decisión humana y no debe registrarse como `approve_for_practice_implementation`. La revisión profesional continúa abierta en el issue `#161`.

## Límite de ambas rutas

Una decisión humana válida o la autorización provisional interna:

- pueden habilitar implementación reproducible dentro de su alcance declarado;
- no autorizan la teoría completa;
- no crean `unit-02.json`;
- no publican páginas;
- no promueven el curso a `developed` o `complete`;
- no demuestran exactitud de un dispositivo real;
- no validan seguridad, conformidad normativa o utilidad clínica;
- no autorizan adquisición con personas, muestras o equipos clínicos.

## Estado vigente

```text
external_professional_review: pending_human_review
external_professional_practice_authorization: false
provisional_internal_practice_authorization: true
full_theory_drafting_authorized: false
unit_developed: false
public_release_authorized: false
course_state: pending
```

La implementación interna puede continuar bajo el override provisional. Cualquier afirmación de aprobación profesional permanece bloqueada hasta que existan manifiesto y decisión humana válidos.
