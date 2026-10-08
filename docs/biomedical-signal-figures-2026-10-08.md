# Figuras de Señales Biomédicas

Seis SVG originales se incorporan a los temas de muestreo, fase y distorsión de filtros, emparejamiento de eventos, fuga espectral, partición por grupos y calibración. Se usan exclusivamente señales matemáticas, matrices ilustrativas y recuentos ficticios; no son registros clínicos ni resultados de un modelo validado.

Cada figura incluye texto alternativo, explicación, límites, fuentes del corpus y licencia CC BY-NC 4.0. El generador `scripts/build_biomedical_signal_figures.py` usa NumPy y Matplotlib y comparte el formato gráfico de Electrónica. El sitio estático no necesita esas dependencias. `calculation-record.json` conserva parámetros y resultados comprobables.

Detalles de interpretación:

- Los cosenos de 3 y 7 Hz coinciden exactamente, salvo redondeo numérico, al muestrearse a 10 Hz. La figura muestra ambigüedad, no reconstrucción de señales clínicas.
- La media móvil es causal de cinco muestras a 100 Hz; el pulso utilizado desplaza su máximo 20 ms. No se propone como filtro apropiado para toda modalidad.
- El emparejamiento mostrado es uno a uno y usa tolerancia de 50 ms: 2 verdaderos positivos, 2 falsos positivos y 1 referencia omitida. La detección duplicada se desplaza ligeramente en vertical para distinguir sus marcas, sin cambiar su tiempo.
- La DFT usa 100 muestras, 100 Hz, ventana rectangular y amplitud unilateral corregida en DC y Nyquist. No representa PSD.
- La partición por participante ilustra un objetivo de generalización a personas nuevas; cuatro participantes ficticios no constituyen una evaluación suficiente.
- La calibración usa cinco grupos hipotéticos de 100 casos y omite intervalos de incertidumbre. No demuestra utilidad clínica ni discriminación.

La teoría de aliasing se contrastó adicionalmente con el tutorial MT-002 de Analog Devices. Las fuentes de apoyo de cada imagen están en `media.json`; todas son ilustraciones propias, no copias de figuras ajenas.

El estado multimedia completo corresponde a seis recursos. La revisión científica sigue pendiente. Se alcanzan 26 figuras completadas en cuatro asignaturas; quedan 102 recursos multimedia planificados en el corpus canónico.
