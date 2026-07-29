# Autorización provisional de autoría — Bioinstrumentación, Unidad 1

**Estado:** `authorized_for_controlled_drafting_provisionally`  
**Fecha efectiva:** 29 de julio de 2026  
**Curso:** `pending`  
**Publicación:** bloqueada  
**Revisión profesional externa:** pendiente

## Decisión

El propietario del proyecto autoriza continuar la redacción controlada de la Unidad 1 y acepta provisionalmente las revisiones internas realizadas por la IA como base operativa suficiente para producir un borrador de alta calidad.

Esta decisión se registra como `project_owner_override`. No constituye revisión humana disciplinar, validación profesional, respaldo institucional ni aprobación externa.

## Qué queda autorizado

- crear `data/course_redevelopment/bioinstrumentacion/units/unit-01.json` como borrador autoral;
- redactar la teoría completa de la unidad;
- desarrollar y revisar ejemplos, actividades, evaluación, feedback y recuperación;
- abrir PRs de autoría y ejecutar todos los gates internos;
- corregir el contenido hasta alcanzar alta coherencia científica, pedagógica y técnica.

## Qué continúa bloqueado

- declarar la unidad `developed`;
- publicar la unidad como contenido completado;
- promover Bioinstrumentación fuera de `pending`;
- marcar el curso como `complete`;
- afirmar revisión humana, respaldo profesional o validación institucional;
- realizar afirmaciones de utilidad clínica o cumplimiento regulatorio no verificadas.

## Relación con la revisión externa

El issue `#154` permanece abierto. La revisión profesional posterior deberá evaluar el contenido producido y podrá:

1. confirmar la autorización;
2. exigir cambios;
3. rechazar partes del borrador;
4. sustituir esta autorización provisional mediante una decisión verificable.

La intención operativa es producir material con suficiente calidad para que esa revisión posterior requiera cambios mínimos o ninguno. Esto no elimina la posibilidad de correcciones sustantivas si el revisor identifica errores.

## Regla de trazabilidad

La autorización se basa en el estado fusionado hasta el commit:

`e702bf18af9f5bdce189ffd7ceda3aa378753945`

El registro estructurado se encuentra en:

`data/authoring_authorizations/bioinstrumentacion-unit-01-provisional.json`

## Estado editorial resultante

- curso: `pending`;
- unidad: `controlled_authoring_authorized`;
- publicación: `blocked_pending_external_verification`;
- revisión profesional: `pending_human_review`.

Esta separación permite avanzar en la producción sin representar la revisión interna de IA como evidencia profesional externa.
