# Revisión parcial de Tratamiento Digital de Imágenes

12 de octubre de 2026. Estado: **review**. Se reescriben las unidades 1 y 2. Las unidades 3–6 conservan contenido de plantilla y sus tests y el examen final siguen bloqueados. Esta entrega no equivale a reconstruir ni validar toda la asignatura.

## Contenido sustituido

| Unidad | Desarrollo | Evidencia de aprendizaje |
|---|---|---|
| 1. Imagen digital | Adquisición frente a matriz; muestreo y aliasing; resolución e interpolación; cuantización con convención explícita; geometría, área y volumen; histogramas; calibración, canales y exportación | 10 casos, 4 actividades con soluciones y criterios propios, 24 preguntas abiertas razonadas, 10 errores corregidos y 16 términos |
| 2. Transformaciones de intensidad | Operaciones afines; CNR; ventanas y recorte; diferencia con DICOM LINEAR; gamma y no linealidad; ecualización discreta; contraste local y CLAHE; comparaciones y separación de prueba | 10 casos, 4 actividades con soluciones y criterios propios, 24 preguntas abiertas razonadas, 10 errores corregidos y 16 términos |

La teoría continua tiene 1238 y 1333 palabras, respectivamente, además de casos, actividades y preguntas. La extensión se registra para auditar el cambio, no como prueba de suficiencia pedagógica. Los desarrollos utilizan escenarios sintéticos y declaran unidades, dominio, redondeo y condiciones.

La presentación de la asignatura reconoce la revisión parcial y deja de prometer un «curso completo». El diagnóstico de entrada se sustituye por diez preguntas de prerrequisitos con soluciones; se retiran cortes de interpretación no validados.

## Preguntas y actividades

- 60 candidatos por unidad, 120 en las dos unidades revisadas: 24 respuestas abiertas, 10 casos, 10 análisis de errores y 16 reconocimientos de glosario en cada una.
- No son 120 preguntas de opción múltiple ni 120 ítems validados. Las preguntas abiertas se autoevalúan con sus soluciones; no se corrige automáticamente su significado.
- Cada unidad declara seis objetivos, con cuatro preguntas abiertas alineadas manualmente por objetivo. El test de 15 reserva una por objetivo antes de completar la selección; la reserva no garantiza todos los subtemas ni ejecución práctica.
- Las ocho actividades incluyen solución orientativa, criterios específicos y una rúbrica formativa común. Su pertinencia, dificultad y claridad necesitan revisión y pilotaje.
- Los casos son autosuficientes: valores, convención y problema aparecen en el enunciado sin depender de «la tabla anterior».
- El final de 50 queda bloqueado hasta reconstruir las unidades restantes. No se rellena con repeticiones de las dos unidades revisadas.

## Figuras originales

Cuatro SVG reproducibles mediante `scripts/build_image_foundations_figures.py`:

1. Cosenos de 3 y 7 ciclos/mm con muestras idénticas cada 0,1 mm: aliasing.
2. Mitades y tablero con idéntico histograma: pérdida de información espacial.
3. Curvas gamma con convención y=x^γ, extremos y dos valores calculables.
4. Ventanas continuas 0–100 y 25–75: pendiente, mesetas y pérdida por recorte.

Incluyen texto alternativo, título, descripción, ejes, procedencia sintética, licencia y preguntas de observación con respuesta. Se inspeccionaron las cuatro representaciones. Son demostraciones matemáticas, no imágenes de pacientes ni resultados clínicos. Las preguntas junto a las figuras todavía no constituyen un banco visual independiente del test.

## Comprobaciones

`tests/test_image_foundations_revision.py` comprueba el contraejemplo de aliasing dentro y fuera de la malla, cuantización con empates, saturación, geometría, histogramas con vecindarios distintos, CNR afín, medias no lineales, ventanas y tablas discretas de ecualización. Comprueba también sincronización entre originales y derivados, matriz de objetivos y presencia de figuras y soluciones en HTML.

`tests/test_assessment_banks.cjs` añade 40 selecciones por unidad para comprobar reserva de objetivos, tamaño y ausencia de repetición; exige que las unidades 3–6 permanezcan bloqueadas y que no aparezca un final disponible. Se mantienen las comprobaciones del resto del corpus.

La prueba focalizada terminó con 8 tests y 96 subtests aprobados. La suite completa terminó con 100 comprobaciones sin fallos, incluidas dos regeneraciones sin cambios. Estos resultados comprueban cálculos y comportamiento del software; no equivalen a revisión científica independiente.

## Fuentes consultadas y límites

Las unidades enlazan los apartados concretos de DICOM PS3.3 sobre geometría y VOI LUT, la documentación de coordenadas de 3D Slicer y las guías oficiales de scikit-image sobre tipos, reducción de tamaño, exposición y ecualización. Se especifica cuándo una fórmula es una convención didáctica y cuándo una implementación depende del estándar o de la versión. No se afirma haber auditado íntegramente DICOM ni que los ejercicios formen un visor conforme.

Pendientes: unidades 3–6 (filtrado espacial, procesamiento frecuencial, morfología/segmentación y evaluación); prácticas con datos y código completos; ampliación de interpretación de figuras; revisión disciplinar y pedagógica independiente; pilotaje y análisis de respuestas. El corpus queda con **87 unidades de 15 asignaturas** con marcadores conocidos de plantilla, **530 tests de unidad** y **79 finales** utilizables para práctica. La ausencia de marcadores no implica validación.
