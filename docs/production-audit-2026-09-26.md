# Auditoría técnica y científica — 26 de septiembre de 2026

Este registro describe una integración intermedia. No declara terminado el catálogo ni sustituye la revisión científica de sus 94 asignaturas y 617 unidades.

## Evidencia técnica

La suite anterior de unittest omitía las pruebas escritas como funciones de pytest. Al ejecutarlas aparecieron ocho fallos: siete dependían de formulaciones equivalentes del texto y uno prohibía mencionar SNR/CNR incluso al explicar por qué no usarlos. Se corrigieron las aserciones conservando la comprobación de límites y ecuaciones. Los validadores históricos del piloto confundían las condiciones anteriores a la migración con la publicación provisional actual. Ahora admiten únicamente la migración registrada, diez unidades en revisión y ausencia explícita de aprobación clínica, humana o regulatoria.

La suite unificada ejecuta 98 comprobaciones, incluidos todos los validadores, 1849 pruebas unittest, 1998 pruebas pytest y 270 subtests. La revisión de 814 documentos HTML no encuentra enlaces internos, recursos o anclas rotos. Dos generaciones completas consecutivas no modifican sus salidas. Los resultados científicos se registran como informes y no como aprobación de contenido.

Se retiraron el runtime de modelos locales, su configuración, dependencias y pruebas exclusivas. La validación de manifiestos de revisión conserva su función independiente. También se eliminó el generador inicial de plantillas que podía sobrescribir unidades curadas. Los 47 workflows previos se consolidaron en una suite reproducible; los scripts y controles específicos siguen ejecutándose.

## Contenido e integración

Se incorporaron las fuentes y pruebas de U1 de Laboratorio de Globalización y Emprendimiento (#518) y U5 de Laboratorio de Imágenes Biomédicas (#529), regenerando sus espejos y páginas. U1 de Electrofísica y Electromecánica (#437) y U3 de Laboratorio de Imágenes (#526) ya tienen versiones curadas independientes en main; reemplazarlas con las propuestas antiguas perdería trabajo posterior.

La auditoría inicial recalculada encontró 20 asignaturas, 115 unidades y 584 apariciones de marcadores conocidos. Después de estas dos incorporaciones: 19 asignaturas, 113 unidades y 572 apariciones. La ausencia de estos marcadores en las otras asignaturas no certifica su profundidad o corrección.

## Trazabilidad pendiente de resolución

El validador previo examinaba solamente el registro heredado de afirmaciones. La nueva auditoría incluye los veinte registros canónicos: 894 afirmaciones y 2001 incidencias de esquema, correspondencia literal, verificación o localización. La cifra cuenta incidencias, no afirmaciones científicamente falsas. Una afirmación puede generar varias incidencias. No se han inventado localizadores ni revisiones para reducirla.

Además de los campos incompletos, se observan referencias temáticamente incorrectas: por ejemplo, una afirmación sobre VGS(th) de MOSFET cita una ficha BC817 de BJT. El registro debe corregirse mediante consulta documental, no mediante una normalización mecánica de identificadores.

`python scripts/audit_scientific_traceability.py --strict` exige resolver esas incidencias. Incluso sin incidencias, su alcance queda limitado a las afirmaciones registradas; no certifica que todas las afirmaciones importantes del corpus estén cubiertas. Ningún curso se promueve a `complete` por esta integración.

## Interfaz y límites de comprobación

Se corrigen el solapamiento del identificador visual de la portada, el contenido invisible si JavaScript no ejecuta animaciones, el 404 con redirección automática y la afirmación incorrecta de que todo el catálogo tiene desarrollo completo. Se añaden metadatos deterministas, favicon, canonical, Open Graph, sitemap y robots.

La revisión visual de producción precede a la integración. El navegador remoto no puede abrir el servidor local de esta sesión; la comprobación visual de estos cambios se realizará contra la publicación. No se atribuye cobertura móvil o postdeployment a la comprobación estática de enlaces.
