# Figuras de Electrónica

Seis SVG originales, uno por unidad, muestran rectificación ideal, pérdidas de conducción, ganancia y ancho de banda, circuito y magnitud de un paso bajo RC, márgenes lógicos y carga resistiva del instrumento. Cada figura se inserta en su tema canónico, con ampliación, texto alternativo, pie, referencias y licencia CC BY-NC 4.0.

Son modelos educativos, no mediciones de componentes reales. Los valores lógicos son hipotéticos. El MOSFET se representa con resistencia constante sin pérdidas de conmutación ni realimentación térmica. La aproximación de ganancia usa un polo, pequeña señal y realimentación de tensión; no se generaliza a todos los operacionales. El filtro presupone fuente ideal y salida sin carga. La carga del instrumento se limita al régimen DC resistivo.

Las fuentes corresponden al registro documental del curso. MT-033 de Analog Devices se consultó adicionalmente el 8 de octubre de 2026, especialmente las secciones de respuesta de un polo y producto ganancia-ancho de banda: https://www.analog.com/media/en/training-seminars/tutorials/MT-033.pdf . Las imágenes son construcciones propias, no reproducciones del documento.

`scripts/build_electronics_figures.py` reconstruye los SVG con NumPy y Matplotlib. `calculation-record.json` conserva parámetros y resultados para contrastar corte RC, ancho de banda, márgenes y divisor resistivo. No se añaden dependencias al sitio estático.

Se revisaron visualmente las seis figuras y se probaron sus cálculos e inserción pública. El estado multimedia completo se limita a los seis recursos planificados del curso; no modifica su revisión científica. El corpus canónico alcanza 20 figuras completadas y mantiene 108 recursos planificados.
