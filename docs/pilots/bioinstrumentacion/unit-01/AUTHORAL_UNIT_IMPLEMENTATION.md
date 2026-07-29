# Implementación autoral — Bioinstrumentación, Unidad 1

**Unidad:** Mensurando, sistema de medición y cadena de trazabilidad  
**Estado:** `authored_internal_review_pending_external_verification`  
**Curso:** `pending`  
**Publicación:** bloqueada  
**Fecha:** 29 de julio de 2026

## Resultado

Se implementó el borrador autoral completo de la Unidad 1 como una fuente modular y un artefacto canónico generado de forma determinista.

La implementación permite revisión interna, ejecución de prácticas y evaluación. No publica la unidad, no cambia Bioinstrumentación a `developed` y no sustituye `pending_human_review`.

## Arquitectura de autoría

La fuente se mantiene en:

```text
data/course_redevelopment/bioinstrumentacion/unit-01-source/
```

El compilador:

```text
scripts/build_bioinstrumentation_u1_authoral_unit.py
```

produce:

```text
data/course_redevelopment/bioinstrumentacion/units/unit-01.json
```

La compilación:

- usa únicamente la biblioteca estándar de Python;
- exige un inventario exacto de fragmentos;
- rechaza campos superiores duplicados;
- conserva Unicode;
- ordena las seis secciones teóricas por número;
- produce bytes deterministas;
- permite comprobar sincronización mediante `--check`.

## Cobertura teórica

El gate exige **2.200 palabras teóricas** como mínimo. La unidad se organiza en seis secciones:

1. especificación del mensurando;
2. fenómeno, señal, indicación, valor medido y resultado;
3. sistema, cadena, fronteras y metadatos;
4. modelo, cantidades de entrada, influencias y correcciones;
5. calibración y trazabilidad de resultados específicos;
6. separación entre trazabilidad y aptitud para el uso.

Cada sección contiene:

- cuatro párrafos sustantivos;
- cuatro puntos clave;
- al menos una formalización matemática o algorítmica;
- localizadores de las fuentes que sostienen sus afirmaciones.

## Modelo conceptual y accesibilidad

El modelo presenta diez capas funcionales desde el fenómeno hasta el juicio de aptitud. Puede leerse en dos direcciones:

- de izquierda a derecha para reconstruir transformaciones;
- de derecha a izquierda para auditar la evidencia que sostiene el resultado.

La representación visual no debe depender únicamente del color. Posición, forma y descripción textual deben diferenciar fenómeno, cadena, modelo, resultado, trazabilidad y aptitud.

## Ejemplos razonados

Se incluyen tres casos complementarios:

- cadena térmica sintética con `T_u`, `T_d`, `T_s` e indicación;
- auditoría del encabezado WFDB del registro ECG 100;
- comparación entre presión intraarterial, estimación auscultatoria y estimación oscilométrica.

Cada ejemplo contiene escenario, seis pasos de razonamiento, interpretación y al menos tres limitaciones. Ninguno autoriza diagnóstico, tratamiento o evaluación de dispositivos.

## Prácticas ejecutables

La unidad integra las dos prácticas previamente validadas:

### `thermal-synthetic`

```bash
python scripts/generate_bioinstrumentation_thermal_dataset.py \
  --output-dir build/bioinstrumentacion-u1/thermal
```

Permite estudiar perturbación, dinámica, offset, ruido, indicación y límites del modelo sin usar personas ni dispositivos reales.

### `physionet-header-audit`

```bash
python scripts/audit_wfdb_header.py \
  data/practice_fixtures/bioinstrumentacion/mitdb-100/100.hea \
  --expect-record-100
```

Audita metadatos del registro 100 sin descargar o interpretar `100.dat`.

## Evaluación y recuperación

Las cinco actividades se alinean con los contratos existentes:

- `U1-A1`: clasificación diagnóstica;
- `U1-A2`: especificación del mensurando;
- `U1-A3`: auditoría de la cadena;
- `U1-A4`: revisión de trazabilidad;
- `U1-A5`: transferencia a un caso no visto.

Los trece errores frecuentes corresponden exactamente a las trece misconceptions del banco ejecutable. El feedback conserva tres etapas y no revela categorías, decisiones esperadas o una clave completa.

## Fuentes

La unidad incluye ocho fuentes directamente verificadas y con localizadores:

- VIM3;
- JCGM GUM-6:2020;
- JCGM GUM-1:2023;
- NIST TN 2156;
- AHA sobre medición de presión arterial;
- MacRae et al. sobre perturbación térmica de contacto;
- Rudtsch et al. sobre dinámica de termómetros de contacto;
- PhysioNet MIT-BIH v1.0.0, registro 100.

Las fuentes clínicas delimitan diferencias entre métodos. No se usan para recomendaciones clínicas personales.

## Gate específico

```bash
python scripts/build_bioinstrumentation_u1_authoral_unit.py
python scripts/validate_bioinstrumentation_u1_authoral_unit.py
```

El validador comprueba:

- identidad y schema 2.0;
- seis secciones y densidad teórica;
- veinte términos únicos;
- tres ejemplos con límites;
- actividades `U1-A1` a `U1-A5`;
- correspondencia exacta con las trece misconceptions;
- dos prácticas offline y sin datos humanos;
- ocho fuentes localizadas;
- bloqueo de recomendaciones clínicas;
- autorización provisional vigente;
- curso `pending`;
- publicación y estado `developed` bloqueados;
- revisión profesional externa en `pending_human_review`.

## Estado pendiente

La implementación interna no completa los gates humanos. Siguen pendientes:

- revisión disciplinar profesional;
- prueba cognitiva con el perfil objetivo;
- ronda independiente entre revisores;
- evaluación empírica de usabilidad del feedback;
- autorización expresa de publicación.

El objetivo de este bloque es producir una base científicamente responsable y técnicamente auditable que requiera cambios mínimos durante la verificación posterior, sin afirmar que dicha verificación ya ocurrió.
