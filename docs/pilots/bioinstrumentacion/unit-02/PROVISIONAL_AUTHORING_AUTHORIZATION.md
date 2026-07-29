# Autorización provisional de autoría — Bioinstrumentación, Unidad 2

**Estado:** `authorized_for_controlled_drafting_provisionally`  
**Fecha efectiva:** 30 de julio de 2026  
**Commit base:** `a29fcedce078de03976970cdb8ce21a10b300245`  
**Curso:** `pending`  
**Publicación:** bloqueada  
**Revisión profesional externa:** `pending_human_review`

## Decisión

Después de completar las prácticas U2-P1 a U2-P3, las evaluaciones U2-A1 a U2-A5 y la auditoría científica-editorial conjunta, el propietario del proyecto indicó continuar. Esta instrucción autoriza producir un borrador autoral controlado de la Unidad 2 y acepta provisionalmente la revisión interna como base operativa para la redacción.

La decisión se registra como `project_owner_continuation_override`. No constituye revisión humana disciplinar, validación profesional, respaldo institucional, aprobación regulatoria ni autorización de publicación.

## Base técnica

La autorización se limita al estado fusionado en el commit:

```text
a29fcedce078de03976970cdb8ce21a10b300245
```

Ese estado contiene una auditoría interna `passed_with_corrections_applied`, seis hallazgos resueltos y cero hallazgos críticos o mayores pendientes. La auditoría revisó prácticas, evaluación y feedback; no ejecutó pruebas cognitivas con estudiantes, revisión de usabilidad real, concordancia entre revisores ni revisión profesional externa.

## Qué queda autorizado

- crear `data/course_redevelopment/bioinstrumentacion/unit-02-source`;
- crear `data/course_redevelopment/bioinstrumentacion/units/unit-02.json` como borrador autoral interno;
- redactar la teoría completa de sensores, transductores y modelos estáticos y dinámicos;
- integrar U2-P1, U2-P2, U2-P3 y U2-A1 a U2-A5;
- revisar ejemplos, glosario, actividades de recuperación y conexiones biomédicas;
- crear un constructor determinista y un validador específico de la unidad;
- abrir PRs de autoría controlada y ejecutar gates internos;
- corregir el borrador hasta alcanzar coherencia científica, pedagógica, editorial y técnica.

## Restricciones obligatorias de autoría

1. **Fronteras funcionales.** Sensor, transductor, interfaz, acondicionamiento y sistema deben distinguirse mediante cantidades de entrada y salida, interacción y frontera declarada.
2. **Propiedades estáticas.** Sensibilidad, linealidad, saturación, zona muerta e histéresis deben formularse con modelo, dominio, referencia, dirección y condiciones.
3. **Dinámica.** El rechazo de controles negativos se limita al modelo simple de primer orden declarado; no equivale a negar que un sistema compuesto pueda contener subsistemas de primer orden.
4. **Carga.** Las rutas eléctrica, térmica, mecánica y óptica deben conservar variables perturbadas y mecanismos separados.
5. **Hojas de datos.** Una propiedad de componente no se transfiere automáticamente a la cadena, al dispositivo o a una aplicación clínica.
6. **Claves de evaluación.** Los campos esperados permanecen internos y no se incorporan al payload del estudiante ni a recursos públicos.
7. **Alcance experimental.** Solo se permiten datos sintéticos o metadatos documentales compactos; no se autorizan personas, muestras, equipos clínicos ni hardware conectado a sujetos.
8. **Límites de inferencia.** El borrador no puede declarar utilidad clínica, seguridad, conformidad regulatoria, validación de dispositivo ni respaldo profesional.

## Qué continúa bloqueado

- declarar la unidad `developed`;
- publicar la unidad como contenido completado;
- promover Bioinstrumentación fuera de `pending`;
- marcar el curso como `complete`;
- afirmar revisión humana, respaldo profesional o validación institucional;
- fabricar evidencia de prueba cognitiva, usabilidad o acuerdo entre revisores;
- modificar el estado externo `pending_human_review`;
- incluir claves de respuesta en recursos públicos;
- realizar afirmaciones clínicas, regulatorias o de seguridad no verificadas.

## Relación con la revisión externa

El issue `#161` permanece abierto. Una revisión profesional válida podrá confirmar el contenido, exigir cambios, rechazar partes del borrador o sustituir esta autorización provisional mediante una decisión verificable.

La autoría interna no satisface `approve_for_practice_implementation`, no crea una decisión humana y no convierte la auditoría interna en evidencia profesional.

## Estado editorial resultante

```text
controlled_authoring_authorized: true
authoral_unit_present_in_authorization_block: false
full_theory_drafting_authorized_provisionally: true
public_release_authorized: false
unit_developed: false
course_state: pending
external_professional_review: pending_human_review
student_cognitive_test: pending_human_execution
feedback_usability_review: pending_human_execution
inter_rater_round: pending_human_execution
```

## Próximo gate

El siguiente bloque debe crear de forma modular y reproducible:

```text
data/course_redevelopment/bioinstrumentacion/unit-02-source/
data/course_redevelopment/bioinstrumentacion/units/unit-02.json
scripts/build_bioinstrumentation_u2_authoral_unit.py
scripts/validate_bioinstrumentation_u2_authoral_unit.py
```

Antes de cualquier publicación o cambio de estado se requerirá una auditoría científica-editorial del borrador autoral, además de la evidencia humana y profesional todavía pendiente.

El registro estructurado de esta decisión se encuentra en:

```text
data/authoring_authorizations/bioinstrumentacion-unit-02-provisional.json
```
