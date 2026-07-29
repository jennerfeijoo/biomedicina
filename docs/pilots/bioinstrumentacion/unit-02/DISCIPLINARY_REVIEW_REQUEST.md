# Solicitud de revisión disciplinar · Bioinstrumentación Unidad 2

Estado: `pending_human_review`

## Alcance de la revisión

Se solicita revisar la resolución técnica previa a la implementación de las prácticas de la Unidad 2: **Sensores, transductores y modelos estáticos y dinámicos**.

El paquete incluye:

- generadores sintéticos para función lineal, saturación, zona muerta e histéresis;
- modelo dinámico lineal de primer orden con controles positivos y negativos;
- relación limitada entre `τ`, tiempo de respuesta y frecuencia de corte;
- selección fijada de termistor, galga extensométrica y fotodiodo;
- cuatro casos seguros de carga térmica, mecánica, eléctrica y óptica;
- registro de fuentes y límites de transferencia.

## Competencia requerida

La persona revisora debe poder cubrir, individualmente o junto con otra persona:

1. instrumentación biomédica o ciencia de la medición;
2. sistemas dinámicos, control o señales;
3. sensores resistivos u ópticos y lectura crítica de hojas de datos.

## Preguntas de revisión

1. ¿Los generadores estáticos permiten discriminar patrón, mecanismo y evidencia sin sobregeneralizar?
2. ¿La relación entre `τ`, tiempo de respuesta y `f_c` está limitada correctamente al primer orden lineal?
3. ¿Los controles negativos rechazan retardo puro, segundo orden subamortiguado y ausencia de tiempo?
4. ¿Los modelos exactos y campos fijados conservan condición, unidad y categoría típico/máximo/tolerancia?
5. ¿Los casos de carga describen una ruta causal correcta y segura?
6. ¿Alguna afirmación invade las unidades 4, 6 u 8 o sugiere validación clínica?

## Errores críticos

La revisión debe marcar como crítico cualquiera de los siguientes:

- presentar `tiempo de respuesta = τ` como identidad universal;
- presentar `f_c = 1/(2πτ)` fuera del modelo declarado;
- aprobar un primer orden ante sobreimpulso o retardo no modelado;
- confundir sensibilidad con resolución, exactitud o selectividad;
- copiar una especificación típica como garantía;
- usar la frecuencia de corte del fotodiodo como ancho de banda de toda la cadena;
- inferir temperatura corporal, fuerza, presión, concentración u oximetría;
- declarar seguridad, conformidad normativa o utilidad clínica.

## Decisiones permitidas

- `approve_for_practice_implementation`: permite implementar U2-P1, U2-P2 y U2-P3 bajo los límites documentados.
- `approve_with_changes`: exige resolver cambios antes de implementar.
- `do_not_approve`: mantiene bloqueada la implementación.

Ninguna decisión de este bloque autoriza la teoría completa, publicación, promoción a `developed` o afirmaciones clínicas.

## Evidencia requerida

La decisión futura debe identificar a la persona revisora, competencia, versión o commit revisado, hallazgos, cambios obligatorios, decisión y confirmación verificable. Los datos personales no necesarios no deben almacenarse en el repositorio.

## Declaración de límite

Este documento **no es una revisión**. Su existencia, la selección de fuentes y un CI verde no equivalen a aprobación humana, respaldo profesional, validación institucional o conformidad regulatoria.
