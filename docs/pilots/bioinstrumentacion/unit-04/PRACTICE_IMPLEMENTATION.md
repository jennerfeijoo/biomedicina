# Implementación de prácticas — Bioinstrumentación Unidad 4

## Estado

- Prácticas `U4-P1`, `U4-P2` y `U4-P3`: implementadas para revisión interna.
- Datos: exclusivamente sintéticos y deterministas.
- Red: no requerida.
- Paquetes externos: no requeridos.
- `unit-04.json`: ausente.
- Evaluaciones, teoría completa y publicación: no autorizadas.

## U4-P1 — Aliasing y filtro anti-alias

Genera una señal compuesta a alta resolución temporal, aplica un filtro pasa-bajos causal simplificado y compara el muestreo con y sin filtrado previo. El resultado expone una componente de 170 Hz muestreada a 200 Hz, cuya frecuencia alias es 30 Hz.

La práctica no presenta el criterio de Nyquist como garantía suficiente para una cadena real y no afirma que un filtro digital posterior pueda reconstruir información ya plegada.

## U4-P2 — Rango, cuantización y saturación

Modela un ADC bipolar ideal de 10 bits entre −1 V y 1 V. Registra entrada, recorte, código, reconstrucción, error de cuantización, saturación y LSB nominal.

El LSB no se interpreta como exactitud, resolución efectiva ni ENOB. La práctica no valida un dispositivo real.

## U4-P3 — Integridad temporal multicanal

Procesa una secuencia sintética con pérdida, duplicación y reordenamiento de muestras. Usa contadores por canal para clasificar discontinuidades reproducibles.

Las marcas de tiempo no se consideran prueba de simultaneidad física. Cualquier interpolación futura deberá declararse como estimación y no como recuperación de datos observados.

## Límites

No se conectan personas, electrodos ni equipos biomédicos. Ningún resultado demuestra seguridad, conformidad, desempeño clínico o validez diagnóstica.
