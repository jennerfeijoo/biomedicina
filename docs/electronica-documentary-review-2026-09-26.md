# Electrónica: cotejo documental de afirmaciones centrales

Se revisaron los 24 registros centrales de las seis unidades contra documentación primaria de fabricantes, conservando el texto académico y el estado provisional del curso. Cada registro incorpora sección, contexto, riesgo y distinción entre apoyo directo e inferencia. Esto no acredita cobertura exhaustiva de las ecuaciones, cifras o recomendaciones restantes, ni revisión humana externa.

Se corrigieron referencias cruzadas que no respaldaban la afirmación: tensión Zener citada a un diodo de señal, umbral MOSFET citado a un BJT, offset citado a un tutorial de ruido, arranque de osciladores citado a filtros y flancos de PCB citados a la interfaz de comandos de KiCad. Las nuevas asociaciones se encuentran en `data/courses/electronica/claims.json`.

Las secuencias didácticas de diseño y bring-up conservan apoyo parcial y explican qué procede del autor del curso. La nota específica para AM62P ilustra puntos de prueba; no se presenta como norma universal de seguridad. Las ocho recomendaciones bibliográficas heredadas cuya etiqueta no documentaba verificación de contenido se clasifican como `recommended_future_review`, preservando la etiqueta anterior en una nota.

El enlace SNOA953A correspondía a **ADC32RF45: Amplifier to ADC Interface**, no a **Printed Circuit Board Layout**. Se corrigen título y alcance tanto en el registro canónico como en la fuente heredada y su espejo, sin inventar un documento sustituto.

Las incidencias de la auditoría ampliada bajan de 2001 a 1849; Electrónica pasa de 152 a cero incidencias entre sus registros existentes. Son incidencias del contrato de trazabilidad, no una medida del número de errores científicos del corpus.
