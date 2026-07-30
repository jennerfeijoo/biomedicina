# Kit de reclutamiento y ejecución humana · Bioinstrumentación Unidad 2

## Propósito

Convertir el paquete congelado de la Unidad 2 en una ejecución humana controlada sin introducir datos identificables, clínicos o sensibles en el repositorio público.

## Roles mínimos

### Participantes de prueba cognitiva

Se requieren al menos tres personas que cumplan la mayor parte de este perfil:

- formación actual o reciente en ingeniería biomédica, bioingeniería, electrónica, física aplicada o disciplina cuantitativa afín;
- conocimientos básicos de funciones, unidades, circuitos resistivos y sistemas de primer orden;
- no haber participado en la redacción de la Unidad 2;
- capacidad para explicar en voz alta cómo interpreta una consigna;
- ausencia de relación de evaluación académica directa con el moderador cuando pueda generar presión indebida.

### Revisores de usabilidad del feedback

Se requieren al menos dos personas con experiencia en docencia, diseño de evaluación, tutoría técnica o comunicación científica. Deben revisar las doce rutas diagnósticas sin utilizar claves de respuesta públicas.

### Revisores para concordancia

Se requieren exactamente dos revisores que puntúen de forma independiente `U2-A1` y `U2-A5`. Deben comprender bioinstrumentación básica y aplicar la escala ordinal `0–1–2` sin consensuar antes de la primera ronda.

### Revisor disciplinar profesional

La revisión profesional continúa separada en el issue #161. Debe ser realizada por una persona con competencia demostrable en bioinstrumentación, sensores, instrumentación biomédica o metrología aplicada.

## Mensaje de invitación para participantes

> Se está evaluando la claridad de una unidad didáctica sobre sensores y transductores, no el desempeño personal del participante. La sesión dura aproximadamente 45–60 minutos e incluye lectura, resolución de tareas breves y preguntas sobre cómo se interpretaron las instrucciones. No se solicitan datos clínicos ni información sensible. Las notas se registran con un identificador seudónimo y se almacenan fuera del repositorio público.

## Mensaje de invitación para revisores

> Se solicita una revisión independiente de una unidad didáctica de Bioinstrumentación. La tarea consiste en aplicar una rúbrica predefinida a actividades abiertas o revisar la utilidad de rutas de feedback. La revisión no implica respaldo institucional, certificación del curso, validación clínica ni aprobación regulatoria. Los resultados se registrarán de forma seudónima y fuera del repositorio público.

## Secuencia de ejecución

1. Verificar que el paquete congelado y su commit coinciden con el manifiesto vigente.
2. Asignar identificadores seudónimos fuera del repositorio.
3. Confirmar consentimiento para participar y, por separado, para cualquier audio o video.
4. Ejecutar las sesiones cognitivas sin enseñar respuestas modelo.
5. Ejecutar la revisión de usabilidad de las doce rutas de feedback.
6. Ejecutar la primera ronda independiente de puntuación de `U2-A1` y `U2-A5`.
7. Calcular acuerdo exacto, diferencia absoluta media y kappa ponderado.
8. Resolver únicamente las discrepancias críticas después de congelar la primera ronda.
9. Redactar un resumen no identificable con hallazgos, cambios obligatorios y decisión.
10. Regenerar el paquete si cambia cualquier artefacto congelado.

## Criterios de detención

La ejecución debe detenerse cuando:

- un participante revela información clínica o sensible no solicitada;
- no puede confirmarse el consentimiento;
- el moderador descubre que se está usando una versión distinta del paquete congelado;
- un revisor consultó claves de respuesta antes de completar la primera ronda;
- existe una relación de dependencia que impide una participación voluntaria;
- se intenta registrar nombres, correos, identificadores institucionales o grabaciones en el repositorio público.

## Evidencia que puede conservarse

Puede conservarse fuera del repositorio:

- consentimiento y fecha;
- identificador seudónimo;
- versión y commit revisados;
- notas de comprensión, dificultades y sugerencias;
- puntuaciones independientes;
- justificaciones y discrepancias;
- decisión final de cada bloque.

En el repositorio solo debe incorporarse un resumen agregado no identificable y la decisión de estado correspondiente. No deben subirse transcripciones, grabaciones, nombres, correos, firmas, datos académicos detallados ni información clínica.

## Resultado permitido

La ejecución puede producir una de estas decisiones:

- `proceed_without_changes`;
- `proceed_with_minor_corrections`;
- `revision_required_before_next_round`;
- `do_not_proceed`.

Ninguna de estas decisiones sustituye la revisión profesional del issue #161 ni autoriza publicación por sí sola.
