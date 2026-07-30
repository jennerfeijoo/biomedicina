# Implementación interna de prácticas · Bioinstrumentación Unidad 3

## Estado

`unit_03_practices_implemented_internal_review`

## U3-P1 · Fuentes distribuidas sintéticas

Genera cuatro potenciales superficiales sintéticos y dos derivaciones diferenciales a partir de dos fuentes temporales ponderadas por geometría. La práctica demuestra superposición, dependencia espacial y efecto de la elección de electrodos.

No representa potenciales transmembrana, localización de fuentes ni un modelo anatómico validado.

## U3-P2 · Impedancia de interfaz

Calcula un barrido de frecuencia para un modelo equivalente formado por una resistencia del medio en serie con una rama paralela de transferencia de carga y doble capa. Produce parte real, parte imaginaria, magnitud y fase.

Los parámetros son didácticos y dependientes de condiciones. El resultado no constituye evidencia de seguridad, biocompatibilidad ni conformidad.

## U3-P3 · Diagnóstico de artefactos

Aplica reglas reproducibles a cuatro fixtures sintéticos. Cada salida conserva patrón, mecanismo plausible y prueba discriminante. Los casos incluyen interferencia de red, movimiento/contacto, saturación y ráfagas ambiguas por cable o actividad biológica no objetivo.

La clasificación no sustituye revisión humana ni permite interpretación clínica.

## Reproducibilidad

Las tres prácticas:

- usan únicamente la biblioteca estándar de Python;
- no requieren red;
- no contienen aleatoriedad;
- generan sus resultados fuera del árbol fuente;
- pueden ejecutarse en CI;
- mantienen bloqueadas evaluación, teoría completa y publicación.

## Límites editoriales

Bioinstrumentación continúa en `pending`. No se crea `unit-03.json`, no se declara revisión profesional y no se autoriza adquisición con personas o conexión física de electrodos.
