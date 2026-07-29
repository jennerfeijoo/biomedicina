# Autorización provisional para implementar prácticas · Bioinstrumentación Unidad 2

**Estado:** `authorized_for_controlled_practice_implementation_provisionally`  
**Autoridad interna:** `project_owner_continuation_override`  
**Revisión profesional externa:** `pending_human_review`  
**Issue operativo:** `#161`  
**Estado editorial del curso:** `pending`

## Qué autoriza este registro

La instrucción del propietario de continuar el flujo se emitió inmediatamente después de identificar como siguiente bloque la autorización provisional y controlada para implementar las prácticas de la Unidad 2. Dentro de ese contexto, el registro permite únicamente:

- crear `data/practice_implementations/bioinstrumentacion-unit-02.json`;
- implementar U2-P1, U2-P2 y U2-P3;
- crear generadores sintéticos, fixtures documentales y controles negativos;
- añadir pruebas de reproducibilidad y gates internos;
- revisar la documentación técnica de las prácticas;
- abrir pull requests limitados a esta implementación.

La base técnica congelada es el commit:

```text
b8134a50a9fea89fe896b167d5791d17ee055e5c
```

El registro autoritativo es:

```text
data/authoring_authorizations/bioinstrumentacion-unit-02-practices-provisional.json
```

## Condiciones obligatorias

La implementación debe cumplir simultáneamente:

1. utilizar únicamente datos sintéticos o documentación de componentes;
2. evitar adquisición de datos de personas, muestras o dispositivos clínicos;
3. no conectar sensores a sujetos;
4. ejecutarse en CI sin depender de red;
5. fijar semillas, parámetros, unidades y tolerancias;
6. incluir controles positivos y negativos;
7. no versionar salidas generadas;
8. conservar condiciones, categorías y límites de cada especificación;
9. impedir inferencias clínicas, regulatorias o de seguridad.

Una práctica que incumpla cualquiera de estas condiciones queda fuera de la autorización.

## Qué permanece bloqueado

Esta autorización no permite:

- redactar la teoría completa;
- crear `data/course_redevelopment/bioinstrumentacion/units/unit-02.json`;
- publicar una página de la unidad;
- declarar la unidad `developed`;
- promover o completar Bioinstrumentación;
- atribuir aprobación humana, profesional o institucional;
- afirmar exactitud clínica, utilidad clínica, seguridad o conformidad normativa;
- usar datos reales de personas o conectar equipos a sujetos.

## Relación con el handoff disciplinar

El handoff externo permanece en:

```text
data/review_handoffs/bioinstrumentacion-unit-02.json
```

Su estado continúa `ready_pending_external_review`, y la revisión operativa se registra en el issue `#161`.

La autorización provisional no modifica el handoff ni simula su decisión. Una revisión humana futura puede confirmar, limitar, exigir cambios o revocar el alcance interno. El manifiesto, CI, fixtures sintéticos y esta autorización no equivalen a evidencia humana.

## Estado resultante

```text
practice_implementation_authorized_provisionally: true
external_professional_practice_authorization: false
full_theory_drafting_authorized: false
unit_authoral_file: absent
unit_developed: false
public_release_authorized: false
course_state: pending
```

## Próximo gate

Antes de fusionar una implementación de U2-P1, U2-P2 y U2-P3 deberán existir:

- contrato estructurado de prácticas;
- generadores reproducibles;
- pruebas de aceptación y rechazo;
- auditoría de unidades y condiciones;
- validación de ausencia de datos humanos;
- documentación de resultados esperados y límites;
- gate permanente que falle ante cualquier ampliación de alcance.
