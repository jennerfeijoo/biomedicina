# Resolución de bloqueos técnicos — Bioinstrumentación Unidad 4

## Alcance

La Unidad 4 aborda conversión y procesamiento de señales biomédicas. Antes de implementar prácticas se fijan seis decisiones técnicas vinculantes para evitar confundir modelos educativos con desempeño real, seguridad o conformidad.

## Bloqueos resueltos

### U4-B01 · Muestreo y anti-alias

La banda objetivo, la banda analógica presente y la frecuencia de muestreo se documentarán por separado. El filtro anti-alias se sitúa antes del muestreador. El criterio de Nyquist no se presentará como garantía suficiente para una cadena real.

### U4-B02 · Rango, cuantización y saturación

El modelo distingue rango de entrada, códigos, LSB nominal, cuantización, ruido, offset, ganancia y clipping. El LSB no equivale a exactitud ni a cambio mínimo detectable real.

### U4-B03 · ENOB

ENOB se utilizará únicamente bajo condiciones de prueba declaradas. No se inferirá desde el número nominal de bits ni se interpretará como exactitud de continua.

### U4-B04 · Sincronización y tiempo

Se distinguen simultaneidad física, muestreo multiplexado, reloj compartido, marcas de tiempo y alineación posterior. Timestamps iguales no prueban muestreo simultáneo.

### U4-B05 · Integridad de datos

Las prácticas usarán contadores de secuencia e inyección reproducible de pérdida, duplicación y reordenamiento. La interpolación no se presentará como recuperación de muestras reales.

### U4-B06 · Aislamiento y seguridad documental

El aislamiento se tratará por función y frontera. No se diseñan conexiones con personas ni se conectan electrodos o equipos biomédicos. Ninguna simulación demuestra seguridad, conformidad o utilidad clínica.

## Autorización

```text
U4-P1: implementation_authorized
U4-P2: implementation_authorized
U4-P3: implementation_authorized

assessment_implementation_authorized: false
full_theory_drafting_authorized: false
public_release_authorized: false
human_or_professional_review: not_claimed
course_state: pending
```

La siguiente fase permitida es implementar las tres prácticas sintéticas y sus validadores reproducibles.
