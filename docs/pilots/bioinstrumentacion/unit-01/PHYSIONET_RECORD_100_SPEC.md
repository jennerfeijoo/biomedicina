# Especificación del registro PhysioNet — Bioinstrumentación, Unidad 1

**Estado:** registro fijado y comprobado documentalmente.  
**Uso:** auditoría de metadatos; no interpretación clínica.

## Dataset

- recurso: MIT-BIH Arrhythmia Database;
- versión: `1.0.0`;
- DOI: `10.13026/C2F305`;
- licencia declarada: Open Data Commons Attribution License v1.0;
- registro seleccionado: `100`.

## Archivos

La práctica requiere:

- `100.hea` — encabezado WFDB;
- `100.dat` — señales.

`100.atr` es opcional y no se utilizará para clasificar latidos ni entrenar modelos en esta unidad.

## Snapshot del encabezado

```text
100 2 360 650000
100.dat 212 200 11 1024 995 -22131 0 MLII
100.dat 212 200 11 1024 1011 20052 0 V5
# 69 M 1085 1629 x1
# Aldomet, Inderal
```

El archivo publicado por PhysioNet contiene la misma información en una secuencia de texto. El snapshot dividido por líneas se conserva para hacer explícita la estructura.

## Metadatos esperados

- identificador: `100`;
- número de señales: `2`;
- frecuencia de muestreo: `360 Hz`;
- número de muestras: `650000`;
- canales: `MLII` y `V5`;
- token de formato WFDB: `212`;
- archivo de datos: `100.dat`.

Las unidades físicas deben obtenerse del parser WFDB y registrarse como salida. No deben inferirse únicamente por la apariencia de los valores ni codificarse de forma silenciosa.

## Objetivo de la práctica

El estudiante deberá:

1. fijar versión y DOI;
2. descargar o leer los archivos declarados;
3. extraer metadatos con una biblioteca WFDB o parser equivalente;
4. comparar la extracción con el snapshot esperado;
5. documentar unidades, ganancias, baselines y etiquetas tal como las reporte el parser;
6. producir un diccionario de datos;
7. señalar qué información no puede inferirse del archivo.

## Pruebas automáticas previstas

- el registro es exactamente `100`;
- la versión es exactamente `1.0.0`;
- existen dos señales;
- la frecuencia es `360 Hz`;
- el número de muestras es `650000`;
- las etiquetas preservan el orden `MLII`, `V5`;
- el parser no sustituye etiquetas ausentes por nombres inventados;
- la salida registra licencia, DOI y fecha de acceso;
- la ejecución no requiere las anotaciones clínicas.

## Inferencias prohibidas

- diagnosticar arritmias;
- interpretar segmentos, ondas o intervalos;
- considerar MLII o V5 equivalentes a actividad intracardíaca directa;
- comparar sujetos o generalizar a una población;
- tratar anotaciones como verdad clínica universal;
- afirmar validez de un modelo médico.

## Justificación de la selección

El registro 100 es adecuado porque su encabezado es pequeño, estable y explícito: permite estudiar cómo versión, frecuencia, canales, formato y metadatos condicionan la interpretación de una señal digital sin introducir todavía procesamiento o clasificación.

## Fuente

PhysioNet, MIT-BIH Arrhythmia Database v1.0.0, página del recurso y archivo `100.hea`. Los localizadores están registrados en `data/source_registry/bioinstrumentacion-unit-01-blockers.json`.
