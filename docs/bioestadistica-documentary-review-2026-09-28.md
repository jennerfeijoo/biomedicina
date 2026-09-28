# Revisión documental de Bioestadística — 2026-09-28

Se revisaron las 28 incidencias detectadas en el registro canónico de 112 afirmaciones. Se corrigieron textos, fuentes y localizadores; dos incidencias eran tipos de afirmación no admitidos (`interpretation` → `inference`). No se modificaron los niveles de riesgo para eludir requisitos ni se atribuyó aprobación humana.

## Correcciones científicas y didácticas

- La dependencia entre visitas no produce siempre intervalos demasiado estrechos. Para medias conjuntas y diferencias pareadas puede actuar en sentidos opuestos. Se corrigieron ambas apariciones de la generalización y se añadió una derivación numérica sintética.
- La interpretación de pendientes ahora especifica un modelo aditivo sin interacciones ni transformaciones del predictor.
- La prevención de fuga distingue transformaciones aprendidas en entrenamiento de conversiones fijas de unidades.
- Discriminación, calibración y utilidad se distinguen con apoyo del artículo de Van Calster y colaboradores (2019).
- Se precisaron valor p, equivalencia, incertidumbre, sensibilidad, permutaciones, Wilcoxon–Mann–Whitney, confusión residual y reproducibilidad computacional.
- La asignación equilibrada se justifica mediante la varianza de dos medias independientes con igual varianza y tamaño total fijo; se incluye su derivación.
- Se corrigió la expresión «intervalos pequeños» en el apartado sobre normalidad: la limitación relevante mencionada es el tamaño muestral.

## Fuentes consultadas

Los registros canónicos contienen las URL y los apartados concretos: ASA (principios 2 y 5); Cochrane (10.14 y 23.2.5–23.2.7); NIST (intervalos, prueba t, diagnósticos, simulación); documentación oficial de R y SciPy; scikit-learn (12.2); Fay y Proschan (2010, pp. 10–11 y tabla 1); STROBE Explanation and Elaboration (2007); National Academies (2019, recomendación 4-1 y nota 3, pp. 58–59); Anand Avati, Stanford CS229 (sección 2, p. 2); FDA (2016, II y III.F).

Las fuentes nuevas se consultaron directamente. No se generaron huellas de documentos que no se descargaron. La copia académica del artículo de Fay y Proschan sustituye la URL de metadatos en el mismo registro, conservando DOI y autoría sin duplicar la obra.

## Alcance y verificación

La auditoría del contrato de trazabilidad pasa de 28 a 0 incidencias para Bioestadística y de 1849 a 1821 para el conjunto de registros. Esto no mide todos los errores científicos del catálogo ni demuestra cobertura exhaustiva. Se conservan los estados editoriales y la revisión humana pendiente. Las afirmaciones de riesgo menor con apoyo parcial no se reclasifican automáticamente.

Se regenera el HTML desde las fuentes canónicas. La suite completa comprueba consistencia, enlaces, tests y reproducibilidad de dos generaciones; el test de regresión del curso protege la correspondencia afirmación–fuente–texto y el matiz sobre dependencia. Sus resultados técnicos no sustituyen la revisión documental.

Resultado local: 98 comprobaciones, 0 fallos; dos generaciones consecutivas sin cambios. La publicación y los checks remotos se comprueban por separado tras la integración.
