# Notas de validación del borrador autoral — Bioinstrumentación Unidad 2

## Artefacto validado

El borrador autoral canónico se genera desde diecinueve fragmentos mediante:

```text
scripts/build_bioinstrumentation_u2_authoral_unit.py
```

y se valida con:

```text
scripts/validate_bioinstrumentation_u2_authoral_unit.py
```

El artefacto resultante es:

```text
data/course_redevelopment/bioinstrumentacion/units/unit-02.json
```

## Estado de integración

La sincronización determinista actualizó el paquete central, `AUTHORING_READINESS.md` y el archivo canónico. El workflow excluye las Unidades 1 y 2 de la generación pública antes de reconstruir sus borradores internos, por lo que la presencia de `unit-02.json` no implica publicación.

## Límites

- curso: `pending`;
- unidad: `authored_internal_review_pending_external_verification`;
- publicación: bloqueada;
- revisión profesional externa: `pending_human_review`;
- prueba cognitiva: `pending_human_execution`;
- revisión de usabilidad: `pending_human_execution`;
- concordancia entre revisores: `pending_human_execution`.

Estas notas no constituyen revisión humana, aprobación profesional, validación clínica, afirmación de seguridad, conformidad regulatoria ni utilidad clínica. El siguiente gate es una auditoría científica y editorial específica del borrador completo.
