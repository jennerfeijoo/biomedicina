# Evaluaciones implementadas · Bioinstrumentación · Unidad 5

## Estado

```text
assessment_implementation_status: internal_review
course_state: pending
public_release_authorized: false
professional_review_claimed: false
```

Se implementan cinco evaluaciones con datos exclusivamente sintéticos. `U5-A1` a `U5-A4` admiten puntuación determinista. `U5-A5` exige revisión humana real y no admite aprobación automática.

## U5-A1 · Referencias y tipos de presión

Evalúa la distinción entre presión absoluta, manométrica y diferencial. La respuesta debe declarar referencia, signo, unidad y rango. Las conversiones solo son válidas cuando la presión de referencia está disponible y es compatible.

Feedback obligatorio:

- error conceptual: confusión entre magnitud y referencia;
- error numérico: signo, unidades, redondeo o referencia incorrecta;
- error interpretativo: extrapolación fuera de rango o atribución clínica no sustentada.

## U5-A2 · Respuesta térmica de primer orden

Evalúa la separación entre temperatura del objeto, sensor y ambiente, la estimación reproducible de la constante de tiempo y el reconocimiento de equilibrio aproximado y autocalentamiento.

## U5-A3 · Magnitudes de flujo

Evalúa velocidad local, flujo volumétrico y flujo másico. Toda conversión debe declarar área efectiva, densidad, perfil de velocidad, régimen y unidades.

## U5-A4 · Modalidades y geometría óptica

Evalúa transmitancia, absorbancia, reflectancia y dispersión, incluyendo longitud de onda, trayectoria óptica, referencia, geometría fuente-muestra-detector y luz parásita.

## U5-A5 · Caso integrador multimodal

```text
automatic_approval_allowed: false
required_review: real_human_review
review_status: prepared_not_executed
```

La persona revisora debe examinar coherencia entre modalidades, trazabilidad de unidades y supuestos, incertidumbre, separación entre observación e inferencia y ausencia de afirmaciones clínicas o de seguridad no sustentadas.

## Recuperación

- Error conceptual: redefinir magnitud, referencia y mecanismo.
- Error numérico: repetir análisis dimensional y cálculo guiado.
- Error interpretativo: separar observación, inferencia y afirmación no demostrada.
- U5-A5 no aprobada: corregir según revisión humana y volver a someter; nunca aprobar automáticamente.

## Límites

```text
synthetic_only: true
human_participants: false
physical_sensor_acquisition: false
biomedical_hardware_connection: false
clinical_validity_claimed: false
electrical_safety_claimed: false
regulatory_conformity_claimed: false
professional_review_claimed: false
public_release_authorized: false
course_completion_authorized: false
course_state: pending
```

No se crea `data/course_redevelopment/bioinstrumentacion/units/unit-05.json` en esta etapa.
