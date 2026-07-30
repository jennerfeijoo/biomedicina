# Bioinstrumentación — Unidad 4

## Estado

- `authoral_draft_internal_review`
- `course_state: pending`
- `public_release_authorized: false`
- `professional_review_claimed: false`
- `U4-A5: pending_real_human_review`

## Alcance del borrador

El borrador integra la cadena analógica-digital, aliasing, filtrado anti-alias, ADC ideal, cuantización, saturación, SINAD, ENOB, sincronización, timestamps, integridad temporal y una frontera conceptual de aislamiento.

## Hallazgos de auditoría resueltos

### U4-F01

Se incorporó un ejemplo numérico con SINAD de 61.96 dB:

`ENOB = (61.96 - 1.76) / 6.02 = 10.0 bits`.

El ejemplo declara que el resultado depende de frecuencia, amplitud y configuración de prueba, y que no representa exactitud en continua.

### U4-F02

Se incorporó la frontera conceptual:

`dominio de adquisición → frontera de aislamiento → dominio digital o de comunicación`.

La representación no demuestra seguridad electromédica, conformidad regulatoria ni aptitud para conectar personas, electrodos o equipos biomédicos.

## Límites

El contenido utiliza datos y escenarios sintéticos. No contiene adquisición humana o de dispositivos, validación clínica, diseño de seguridad, aprobación profesional ni autorización de publicación.
