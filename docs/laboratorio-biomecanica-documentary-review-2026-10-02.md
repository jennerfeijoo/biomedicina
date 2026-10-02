# Laboratorio de Biomecánica: revisión documental de 24 afirmaciones

Fecha: 2 de octubre de 2026. Alcance: las 24 afirmaciones ancla registradas en las seis unidades. No representa cobertura exhaustiva del curso ni revisión disciplinar humana.

Se sustituyen las categorías no admitidas por tipos específicos y se añaden localizadores de secciones, notas y ecuaciones. La auditoría del registro pasa de 48 errores de contrato a cero; el conjunto del repositorio pasa de 1821 a 1773. Estos recuentos describen el contrato documental, no certifican validez científica completa.

## Correcciones docentes

- Unidad 1: se limita la necesidad de declarar origen a las coordenadas de posición. La precisión de marcadores y la validez del marco anatómico siguen diferenciadas; la inferencia conserva soporte parcial porque el resumen de Cappozzo et al. no cuantifica esa validez.
- Unidad 3: una traslación del origen con ejes fijos conserva las componentes de la fuerza y modifica el momento. Se incorpora un ejemplo calculable de transporte de momentos y la derivación del centro de presiones con origen en la superficie, fuerza normal no nula y momento libre normal.
- Unidad 4: la selección y colocación de electrodos pertenecen al procedimiento de adquisición. Se elimina su identificación imprecisa con el mensurando. La respuesta Butterworth ilustra cómo un filtro modifica amplitudes, distinguiendo una pasada de la aplicación hacia delante y atrás.

## Evidencia y límites

Los registros contienen los enlaces y localizadores exactos. Las nuevas referencias incluyen VIM 2.26, 2.33 y 2.34; OpenStax, sección 10.6, ecuación 10.22; Andersen et al. (2010), introducción sobre artefacto de tejido blando; y la documentación de `scipy.signal.butter`, parámetro Wn. La documentación de OpenSim sustenta marcos, entradas y resultados de dinámica inversa. Los resúmenes de artículos se identifican como tales: no se atribuye lectura íntegra cuando solo se ha comprobado el resumen.

La afirmación LABBIO-U01-C002 conserva `support: partial`. Las derivaciones propias se identifican como inferencias; no se atribuyen literalmente a un artículo. La referencia sobre ICC se utiliza para elección de modelo, tipo y definición, sin reproducir la tabla de fórmulas objeto de corrección editorial. FAIR no se equipara con acceso público irrestricto: se conserva la posibilidad de autenticación.

El estado permanece `ai_review_provisional`, sin identificador de validación humana. La fecha documental nueva se registra separadamente de los campos históricos de revisión.

## Verificación

Las pruebas de regresión comprueban el contrato documental, la conservación del soporte parcial y las correcciones de momento, CoP y respuesta del filtro. La integración exige además el conjunto de controles del repositorio y dos generaciones consecutivas sin cambios pendientes.
