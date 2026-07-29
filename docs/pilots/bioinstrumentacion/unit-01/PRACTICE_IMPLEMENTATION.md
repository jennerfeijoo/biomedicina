# Implementación reproducible — Bioinstrumentación, Unidad 1

**Estado:** `implemented_internal_review`  
**Estado editorial:** `pending`  
**Revisión disciplinar:** pendiente  
**Teoría completa autorizada:** no

## Objetivo

Este bloque convierte dos prácticas planificadas en software ejecutable y verificable. No crea una lección pública, no adquiere datos de personas y no sustituye la revisión disciplinar.

## 1. Cadena térmica sintética

El generador `scripts/generate_bioinstrumentation_thermal_dataset.py` produce un CSV y un manifiesto JSON mediante biblioteca estándar de Python.

La implementación conserva cuatro niveles separados:

- `T_u_C`: temperatura superficial no perturbada prescrita;
- `T_d_C`: temperatura superficial perturbada por un sesgo de contacto declarado;
- `T_s_C`: estado dinámico interno del sensor;
- `indication_C`: indicación después de offset y ruido sintético.

La evolución de `T_s` se calcula con la solución discreta exacta de un sistema lineal de primer orden para entradas constantes por tramo. El modelo verifica convergencia, respuesta a una y cinco constantes de tiempo, monotonía y ausencia de sobreimpulso ideal.

**No es un modelo fisiológico validado.** Los parámetros predeterminados son didácticos y no representan una población, piel real, temperatura corporal central ni un dispositivo comercial.

### Ejecución

```bash
python scripts/generate_bioinstrumentation_thermal_dataset.py \
  --output-dir build/bioinstrumentacion-u1/thermal
```

Los resultados generados no se versionan. El manifiesto registra parámetros, semilla, columnas, limitaciones y `sha256` del CSV.

## 2. Auditoría del encabezado WFDB

El parser `scripts/audit_wfdb_header.py` lee una copia mínima y atribuida del encabezado `100.hea` del MIT-BIH Arrhythmia Database v1.0.0.

Comprueba:

- registro `100`;
- dos señales;
- frecuencia de `360 Hz`;
- `650000` muestras;
- formato `212` en ambos canales;
- etiquetas `MLII` y `V5`;
- referencia a `100.dat`.

### Ejecución

```bash
python scripts/audit_wfdb_header.py \
  data/practice_fixtures/bioinstrumentacion/mitdb-100/100.hea \
  --expect-record-100
```

La actividad se limita a metadatos y procedencia. No incluye `100.dat`, interpretación de ECG, clasificación de arritmias ni inferencia clínica.

## Sin descarga en CI

Todas las validaciones se ejecutan offline. CI no descarga PhysioNet, no depende de `wfdb` y no genera artefactos persistentes en el repositorio. El generador trabaja en un directorio temporal y el parser utiliza el fixture local atribuido.

## Validación

```bash
python scripts/validate_bioinstrumentation_u1_practices.py
```

El gate verifica determinismo, dinámica ideal, manifiesto, hash esperado, parser WFDB, rechazo de encabezados inconsistentes, atribución, sincronización con el paquete piloto y permanencia del curso en `pending`.

## Límites editoriales

- No se crea `data/course_redevelopment/bioinstrumentacion/units/unit-01.json`.
- No se publica teoría ni evaluación para estudiantes.
- No se promueve el curso a `developed` o `complete`.
- La revisión disciplinar pendiente continúa siendo un gate humano obligatorio.
- Un workflow verde demuestra reproducibilidad técnica, no validez científica externa ni utilidad clínica.
