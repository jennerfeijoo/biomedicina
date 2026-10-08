# Figuras de Bioestadística

Ocho gráficos originales se integran en los temas pertinentes de las ocho unidades: medidas repetidas, influencia de extremos, distribución de medias muestrales, cobertura de intervalos, pares, regresión logística, multiplicidad y lectura de intervalos.

Todos representan datos sintéticos, modelos analíticos o intervalos hipotéticos. No contienen información de pacientes ni resultados de investigaciones reales. Cada figura incluye unidades o escala, supuestos, límites, texto alternativo, atribución, licencia y referencias del corpus canónico. La figura de cobertura explicita que la desviación poblacional es conocida; no aplica sin más el intervalo normal a cualquier diseño. Las medias proceden de 30 muestras normales independientes de tamaño 25 con semilla 20261008. No se seleccionaron simulaciones para obtener exactamente 95 % de cobertura.

El generador `scripts/build_biostatistics_figures.py` requiere NumPy y Matplotlib solo para reconstruir los SVG. El sitio y las pruebas ordinarias no incorporan estas dependencias. El registro `assets/figures/bioestadistica/calculation-record.json` conserva las cantidades usadas para comprobar los cálculos. Las figuras tienen texto vectorial y se pueden ampliar desde la unidad.

La explicación frecuentista se contrastó también con NIST, sección 1.3.5.2, el 8 de octubre de 2026: https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm . Las demás referencias corresponden a las fuentes ya registradas en la asignatura. Son visualizaciones originales, no copias de ilustraciones ajenas.

El estado multimedia completo cubre estos ocho recursos planificados. La revisión científica permanece pendiente. Con las seis figuras de Desarrollo de Dispositivos Médicos, hay 14 recursos completados y 114 planificados en el corpus canónico.
