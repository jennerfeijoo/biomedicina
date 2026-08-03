# Implementación pública canónica — Bioinstrumentación

## Resultado

La capa pública de Bioinstrumentación queda estructurada en diez unidades canónicas y en estado editorial `review`.

La implementación corrige la discrepancia entre el plan curricular de diez unidades y la web previa de seis unidades sin reescribir la evidencia histórica.

## Secuencia pública

1. Mensurando, sistema de medición y cadena de trazabilidad.
2. Sensores, transductores y modelos estáticos y dinámicos.
3. Biopotenciales, electrodos e interfaz electrodo-tejido.
4. Acondicionamiento analógico, ruido y rechazo de interferencias.
5. Muestreo, conversión y adquisición digital.
6. Sensores mecánicos, térmicos, de flujo y ópticos.
7. Aislamiento, seguridad eléctrica y compatibilidad electromagnética.
8. Caracterización de desempeño, calibración e incertidumbre.
9. Verificación, validación, riesgo y aptitud para el uso.
10. Integración y expediente reproducible.

## Política de migración

- Las unidades autorales históricas 1–3 se preservan como procedencia de las unidades canónicas 1–3.
- La nueva unidad analógica ocupa la posición canónica 4.
- El contenido digital de la antigua unidad 4 se publica como unidad canónica 5.
- El contenido de sensores no eléctricos de la antigua unidad 5 se publica como unidad canónica 6.
- El contenido de seguridad eléctrica y EMC de la antigua unidad 6 se publica como unidad canónica 7.
- Las unidades 8–10 completan caracterización, verificación/riesgo e integración.
- Los documentos históricos, prácticas, evaluaciones y auditorías legacy permanecen sin reescritura retroactiva.

## Superficies sincronizadas

```text
data/subjects/ingenieria-biomedica/bioinstrumentacion.json
data/generated_courses/bioinstrumentacion.json
data/generated_units/bioinstrumentacion/unit-01.json ... unit-10.json
ingenieria-biomedica/bioinstrumentacion/index.html
ingenieria-biomedica/bioinstrumentacion/unidades/index.html
ingenieria-biomedica/bioinstrumentacion/unidades/unidad-01.html ... unidad-10.html
```

La navegación pública es continua de la unidad 1 a la 10. Las páginas se generan desde las fuentes estructuradas y no se mantienen como una segunda fuente académica independiente.

## Controles técnicos

La implementación se somete a:

- validación curricular global;
- validación del contrato avanzado de unidades;
- auditoría bibliográfica;
- auditoría de redundancia;
- validación de conexiones biomédicas estructuradas;
- alineación estricta entre fuentes y HTML público;
- validación de enlaces internos;
- auditoría de completitud;
- preflight de preservación legacy;
- gate canónico específico del curso.

## Frontera editorial

```text
public_status: review
human_review_executed: false
disciplinary_review_complete: false
professional_approval_claimed: false
clinical_validity_claimed: false
safety_conformity_claimed: false
emc_conformity_claimed: false
regulatory_conformity_claimed: false
accreditation_claimed: false
```

La publicación corresponde a contenido educativo estructurado y revisado internamente. No constituye formación práctica supervisada, revisión disciplinar externa, certificación, conformidad normativa ni autorización clínica.

## Gates externos pendientes

1. revisión humana real de evaluaciones abiertas;
2. revisión disciplinar por una persona competente en bioinstrumentación;
3. registro y resolución de los hallazgos de esa revisión;
4. decisión editorial separada antes de cualquier transición a `complete`.
