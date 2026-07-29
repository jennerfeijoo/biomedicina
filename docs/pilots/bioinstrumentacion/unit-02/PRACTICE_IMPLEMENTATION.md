# Implementación reproducible · Bioinstrumentación Unidad 2

**Estado:** `implemented_internal_review`  
**Autorización interna:** `authorized_for_controlled_practice_implementation_provisionally`  
**Revisión profesional externa:** `pending_human_review`  
**Teoría completa:** bloqueada  
**Curso:** `pending`

## Alcance

Este bloque implementa U2-P1, U2-P2 y U2-P3 como actividades offline y reproducibles. No adquiere datos de personas, no conecta sensores a sujetos, no opera equipos clínicos y no convierte resultados sintéticos o documentales en validación física, clínica, regulatoria o de seguridad.

Las salidas se generan dentro de `build/` o directorios temporales y no se versionan.

## U2-P1 · Banco sintético de características estáticas

```bash
python scripts/generate_bioinstrumentation_u2_static_dataset.py \
  --output-dir build/bioinstrumentacion-u2/static
```

Produce:

- `static_characteristics.csv`;
- `static_characteristics_manifest.json`.

El CSV distingue `linear-local`, `saturation`, `dead-zone` e `hysteresis`. Cada fila conserva modelo, rama, dirección, entrada, salida ideal, ruido y salida observada. Las unidades son deliberadamente didácticas para impedir que las curvas se presenten como datos de tejido, persona o dispositivo.

### Controles positivos

- recuperación de `K` y `b` en el control lineal;
- sensibilidad local decreciente en saturación;
- salida ideal constante dentro de la zona muerta;
- diferencia media entre ramas igual a `2*h` en histéresis.

### Control negativo de histéresis

Un ajuste lineal agrupado que ignora la dirección deja residuos medios opuestos en las ramas ascendente y descendente. Por tanto, un ajuste global aceptable no elimina la dependencia de trayectoria.

## U2-P2 · Respuesta dinámica de primer orden

```bash
python scripts/generate_bioinstrumentation_u2_dynamic_dataset.py \
  --output-dir build/bioinstrumentacion-u2/dynamic
```

Produce:

- `first_order_response.csv`;
- `dynamic_negative_controls.csv`;
- `dynamic_response_manifest.json`.

El modelo implementado es:

```text
tau*dy/dt + y = K*x(t) + b
```

La entrada permanece constante durante cada intervalo y se usa la actualización discreta exacta. El gate comprueba la fracción `1-exp(-1)` a una constante de tiempo, la estimación de `tau`, la ausencia de sobreimpulso y la magnitud `1/sqrt(2)` en `f_c = 1/(2*pi*tau)`.

### Controles negativos

- **pure-delay:** se rechaza si existe un intervalo plano posterior al escalón mayor que `5*dt`;
- **underdamped-second-order:** se rechaza si el sobreimpulso supera 1 % del cambio final;
- **static-only:** se rechaza cualquier estimación de `tau` cuando falta el eje temporal.

La relación entre `tau` y `f_c` se limita al primer orden lineal y al criterio de −3 dB. No se generaliza a retardos, resonancia, polos múltiples o cadenas completas.

## U2-P3 · Auditoría documental de componentes

```bash
python scripts/audit_bioinstrumentation_u2_datasheets.py \
  data/practice_fixtures/bioinstrumentacion/unit-02/component-datasheet-records.json \
  --output build/bioinstrumentacion-u2/datasheet-audit.json
```

El fixture contiene metadatos compactos para:

- Vishay `NTCLG100E2103JB`;
- Micro-Measurements `CEA-06-125UNA-350`;
- Hamamatsu `S5821-03`.

No reproduce hojas de datos completas. La auditoría conserva unidades, condiciones, categorías nominal/típico/máximo y campos no resueltos. El factor de galga específico del lote permanece sin valor porque la página genérica no lo sustenta.

Los controles negativos rechazan una condición eliminada y cualquier intento de marcar un valor típico como garantía.

## Reproducibilidad

El gate permanente ejecuta las tres prácticas en directorios temporales, compara hashes dorados y verifica que cambiar una semilla altera el ruido sin modificar el contrato. No requiere red ni dependencias externas.

## Límites editoriales

La implementación:

- no crea `data/course_redevelopment/bioinstrumentacion/units/unit-02.json`;
- no autoriza teoría completa;
- no publica una página;
- no promueve el curso a `developed` o `complete`;
- no simula revisión humana;
- no demuestra exactitud de componentes o cadenas reales;
- no valida seguridad, conformidad normativa o utilidad clínica.

La revisión disciplinar profesional continúa en el issue `#161`.
