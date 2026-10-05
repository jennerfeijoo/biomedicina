# Laboratorio de Señales Biomédicas: reconstrucción de seis unidades

Fecha: 4 de octubre de 2026. Estado editorial: revisión experta pendiente.

Se reemplaza el contenido de plantilla del paquete de reconstrucción y sus copias publicadas. El curso aborda reloj y calibración, máscaras de calidad, filtros y remuestreo, eventos, características y reproducción del análisis. Contiene 12 ejemplos resueltos, 48 problemas de práctica distintos de las 48 preguntas de autoevaluación y 72 términos de glosario distribuidos entre unidades.

## Cálculos y límites

Las derivaciones propias muestran alias de dos cosenos, cuantización ideal, cobertura como unión de defectos, SNR, respuesta de media móvil, magnitud del filtrado bidireccional, conversión de anotaciones, métricas de eventos, identidad RMS-varianza y potencia de banda. Se conserva la distinción entre duración nominal e intervalo entre muestras extremas, entre potencia absoluta y relativa, y entre ventanas y sujetos independientes.

Las fuentes primarias incluyen documentación de WFDB, SciPy, NumPy, scikit-learn y Python, además de las bases MIT-BIH y Noise Stress Test de PhysioNet. Cada referencia identifica la operación o apartado utilizado. Los parámetros sintéticos y las derivaciones no se presentan como resultados clínicos de esas fuentes.

El script público `assets/labs/signal_laboratory.py` se ejecuta con Python 3.10 o superior, sin dependencias. Produce un caso verificable por unidad. Su emparejamiento usa programación dinámica: maximiza el número de parejas y minimiza después el error absoluto total. Los empates tienen una regla determinista, la tolerancia es inclusiva y los denominadores vacíos producen `None`. Su coste cuadrático lo limita a ejemplos pequeños; no se presenta como detector de eventos fisiológicos.

## Comprobaciones

Las pruebas contrastan escalas y alias, unión de defectos, cancelación espectral y bordes de la media móvil, duplicados, entradas inválidas y emparejamientos contra enumeración exhaustiva de asignaciones pequeñas. La validación del sitio comprueba las seis unidades y sus copias exactas.

La auditoría de contenido pasa de 17 a 16 cursos con patrones de plantilla detectados, de 101 a 95 unidades afectadas y de 512 a 486 coincidencias. Esto mide los patrones conocidos de la auditoría; no acredita revisión científica exhaustiva. La reconstrucción no añade un registro de afirmaciones validado ni una revisión humana.

La integración exige los 98 controles completos y dos generaciones consecutivas sin cambios; el README se actualiza junto al catálogo para conservar el mismo estado público.
