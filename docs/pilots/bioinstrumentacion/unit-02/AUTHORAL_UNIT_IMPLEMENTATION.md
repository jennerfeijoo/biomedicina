# Implementación autoral — Bioinstrumentación, Unidad 2

**Estado:** `authored_internal_review_pending_external_verification`  
**Curso:** `pending`  
**Publicación:** bloqueada  
**Revisión profesional externa:** `pending_human_review`

## Alcance del bloque

Este bloque crea un borrador autoral interno completo de la Unidad 2, respaldado por la autorización provisional del propietario y por la auditoría previa de prácticas, evaluación y feedback. Este bloque no publica la unidad, no la declara `developed` y no representa validación profesional, institucional, clínica, regulatoria o de seguridad.

## Fuente modular

La autoría se mantiene en diecinueve fragmentos JSON dentro de:

```text
data/course_redevelopment/bioinstrumentacion/unit-02-source
```

El constructor determinista:

```text
scripts/build_bioinstrumentation_u2_authoral_unit.py
```

produce:

```text
data/course_redevelopment/bioinstrumentacion/units/unit-02.json
```

El artefacto canónico debe coincidir byte a byte con la composición de los fragmentos.

## Cobertura

El borrador contiene:

- seis secciones teóricas con al menos **2.200 palabras**;
- veinte términos de glosario;
- tres ejemplos razonados: `NTCLG100E2103JB`, `CEA-06-125UNA-350` y `S5821-03`;
- cinco actividades alineadas `U2-A1` a `U2-A5`;
- doce errores conceptuales;
- doce preguntas de autoevaluación;
- cinco conexiones biomédicas limitadas;
- tres prácticas ejecutables `U2-P1`, `U2-P2` y `U2-P3`;
- doce fuentes verificadas y localizadas.

## Reglas científicas incorporadas

1. Sensor, transductor, interfaz, acondicionamiento y sistema se distinguen por función y frontera.
2. Sensibilidad, selectividad, resolución, rango y exactitud no se tratan como sinónimos.
3. La linealidad requiere modelo de referencia, intervalo, dirección, condiciones y método.
4. Saturación, zona muerta, histéresis, deriva y ruido se diagnostican mediante patrones y pruebas diferentes.
5. La carga eléctrica sobre la tensión del puente permanece separada de la transferencia mecánica de deformación.
6. La relación `f_c = 1/(2πτ)` se limita al primer orden lineal y al criterio de −3 dB.
7. El rechazo dinámico se limita al modelo simple declarado y no excluye modelos compuestos.
8. Las especificaciones de componente conservan categoría y condición y no se transfieren a la cadena o a utilidad clínica.

## Integración con evaluación y prácticas

- `U2-A1` y `U2-A5` siguen requiriendo rúbrica humana.
- `U2-A2`, `U2-A3` y `U2-A4` emplean respuestas estructuradas.
- Las claves internas no se incorporan al contenido autoral dirigido al estudiante.
- El feedback conserva liberación progresiva y no revela respuestas completas.
- Las prácticas se ejecutan offline, con datos sintéticos o metadatos documentales compactos.
- No se conectan sensores a personas, no se emplean muestras y no se operan equipos clínicos.

## Gate permanente

```text
scripts/validate_bioinstrumentation_u2_authoral_unit.py
```

comprueba:

- inventario exacto de fragmentos;
- construcción canónica determinista;
- coherencia con resultados de aprendizaje;
- extensión y formalización teórica;
- cobertura conceptual y terminológica;
- alineación de ejemplos, actividades, prácticas y feedback;
- presencia de las seis correcciones de auditoría;
- trazabilidad de doce fuentes;
- ausencia de recomendaciones clínicas;
- curso en `pending`;
- publicación y promoción bloqueadas;
- evidencia humana y profesional todavía pendiente.

## Límites editoriales

Este borrador no constituye respaldo profesional externo. No autoriza publicación, cambio a `developed`, cambio a `complete`, validación clínica, afirmaciones de seguridad, conformidad normativa ni utilidad clínica.

La siguiente fase es una auditoría científica y editorial específica del borrador autoral completo. Después continuarán pendientes la prueba cognitiva con estudiantes, la revisión de usabilidad del feedback, la concordancia entre revisores y la revisión disciplinar externa.
