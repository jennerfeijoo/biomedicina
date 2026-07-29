# Plan de práctica y datos — Bioinstrumentación, Unidad 1

**Estado:** preparación de autoría.  
**Modalidad:** simulación, auditoría de metadatos y datos fisiológicos abiertos.  
**Límite de seguridad:** no se adquieren datos de personas ni se conectan sensores, electrodos o equipos clínicos.

## Objetivo pedagógico

Las prácticas deben demostrar que un archivo o una lectura solo puede interpretarse cuando se conocen el mensurando, la cadena, las unidades, las transformaciones, el tiempo, las condiciones y el modelo. La programación es un medio de auditoría, no el tema central de la unidad.

## Práctica 1 — Cadena térmica sintética

### Pregunta

¿Por qué la temperatura indicada por un sensor en contacto puede diferir de la temperatura que se pretende atribuir al objeto?

### Dataset sintético

Archivo propuesto: `temperature_chain.csv`.

| Variable | Unidad | Función |
|---|---|---|
| `time_s` | s | eje temporal |
| `object_temperature_C` | °C | cantidad del objeto en la simulación |
| `ambient_temperature_C` | °C | magnitud de influencia |
| `sensor_temperature_C` | °C | estado térmico del sensor |
| `contact_state` | 0/1 | condición de interacción |
| `offset_C` | °C | efecto sistemático simulado |
| `adc_code` | código | indicación digital cruda |
| `reported_temperature_C` | °C | valor calculado mediante el modelo seleccionado |

### Generación

- semilla fija;
- ecuación y parámetros documentados;
- al menos tres escenarios de ambiente y contacto;
- cuantización visible;
- un escenario con offset no corregido;
- un escenario donde el tiempo de contacto es insuficiente.

### Tareas

1. Especificar dos mensurandos posibles y explicar por qué no son equivalentes.
2. Dibujar la cadena de señal.
3. Identificar indicación, cantidades de entrada y magnitudes de influencia.
4. Proponer un modelo introductorio y declarar sus supuestos.
5. Comparar la indicación con el resultado calculado.
6. Explicar por qué repetibilidad del código no demuestra ausencia de sesgo.
7. Redactar una afirmación limitada sobre trazabilidad y declarar la evidencia faltante.

### Producto reproducible

- script de generación;
- CSV generado;
- diccionario de datos;
- figura con objeto, sensor, ambiente e indicación;
- diagrama de cadena;
- modelo comentado;
- respuesta de auditoría.

### Criterio

La práctica se aprueba cuando el estudiante puede reconstruir qué valores son simulados, observados o inferidos y no presenta `reported_temperature_C` como verdad sin condiciones.

## Práctica 2 — Auditoría de metadatos ECG abiertos

### Fuente prevista

MIT-BIH Arrhythmia Database, PhysioNet, versión 1.0.0. Antes de escribir la unidad deberá fijarse un registro concreto y conservar:

- identificador;
- versión;
- licencia;
- canales;
- frecuencia de muestreo;
- unidades;
- ganancia y baseline documentados;
- archivos utilizados;
- hash o referencia de versión.

### Uso permitido

La señal se utiliza únicamente para estudiar cómo valores almacenados adquieren significado físico mediante metadatos y una cadena documentada.

No se utiliza para:

- diagnosticar arritmias;
- evaluar salud cardíaca;
- comparar pacientes;
- entrenar clasificadores;
- recomendar decisiones clínicas.

### Tareas

1. Leer el encabezado y un segmento corto mediante una biblioteca reproducible.
2. Identificar valores digitales, unidades físicas, canales y tiempo.
3. Explicar qué transformaciones convierten el almacenamiento en una señal representada.
4. Separar la señal registrada del fenómeno bioeléctrico y del mensurando especificado.
5. Enumerar qué partes de la adquisición no pueden reconstruirse solo desde el archivo.
6. Identificar al menos cinco metadatos necesarios para comparar resultados.
7. Construir una afirmación correcta sobre el alcance del registro.

### Producto reproducible

- script mínimo de lectura;
- tabla de metadatos;
- segmento visualizado sin anotación diagnóstica;
- cadena de procedencia del archivo;
- lista de inferencias permitidas y prohibidas;
- registro de entorno y dependencias.

### Criterio

La práctica se aprueba cuando el estudiante explica por qué una forma de onda, incluso visualmente plausible, no demuestra por sí sola procedencia fisiológica, mensurando ni validez clínica.

## Práctica 3 — Auditoría de trazabilidad documental

### Material sintético

Se prepararán cuatro expedientes breves:

- certificado de calibración con intervalo adecuado y medición dentro de condiciones;
- certificado correcto pero medición fuera del intervalo;
- instrumento recién calibrado sin modelo ni incertidumbre de uso;
- resultado con cadena documentada pero incertidumbre insuficiente para la necesidad.

### Tareas

Para cada expediente:

1. identificar el resultado al que se aplica la afirmación;
2. localizar la referencia especificada;
3. reconstruir los enlaces de calibración disponibles;
4. identificar contribuciones de incertidumbre omitidas;
5. evaluar si la afirmación de trazabilidad está respaldada;
6. evaluar por separado la aptitud para el uso;
7. redactar una conclusión limitada.

### Criterio

No se acepta la frase “instrumento trazable” como conclusión suficiente. El estudiante debe formular la propiedad para un resultado específico y justificar el alcance temporal y operativo.

## Estructura de repositorio futura

```text
practices/bioinstrumentacion/unit-01/
├── README.md
├── environment.yml
├── src/
│   ├── generate_temperature_chain.py
│   └── audit_ecg_metadata.py
├── data/
│   ├── synthetic/
│   └── external-manifest.json
├── notebooks/
├── tests/
└── outputs/
```

Los datos externos no deben duplicarse sin necesidad. `external-manifest.json` registrará la fuente, versión, licencia, archivos y comprobaciones de integridad.

## Pruebas automáticas previstas

- las columnas del dataset sintético coinciden con el diccionario;
- las unidades están presentes;
- la semilla reproduce el mismo archivo;
- el script no descarga datos distintos de la versión fijada;
- el segmento ECG conserva longitud y frecuencia esperadas;
- las figuras no contienen lenguaje diagnóstico;
- el notebook puede ejecutarse desde un entorno limpio;
- no existen rutas locales absolutas ni credenciales.

## Accesibilidad

- tablas además de figuras;
- texto alternativo para cada visualización;
- patrones o tipos de línea además del color;
- variables con nombres descriptivos y unidades;
- instrucciones ejecutables sin depender de una interfaz gráfica;
- versión tabular de los diagramas de cadena.

## Gate antes de implementar código

1. Confirmar el registro de PhysioNet y la licencia.
2. Revisar el modelo térmico y sus supuestos.
3. Definir hashes o identificadores de versión.
4. Aprobar el diccionario de datos.
5. Verificar que ninguna tarea requiere datos humanos nuevos.
6. Verificar que ninguna salida se presenta como interpretación clínica.
7. Alinear cada paso con un resultado de aprendizaje y una misconception.
