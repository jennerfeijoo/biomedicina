# Notas de validación de la auditoría interna · Bioinstrumentación U2

## Filtración de claves

El gate distingue entre **nombres de campos** y texto descriptivo. Una salida infringe la política cuando contiene como clave estructural alguno de los campos prohibidos, por ejemplo `expected_decision`, `tau_target_s` o `answer_key`.

Una cadena descriptiva como `diagnostic_and_recovery_without_answer_key` no contiene una clave de respuesta ni revela su valor. Por ello, el validador recorre recursivamente las claves de objetos y listas en lugar de buscar subcadenas dentro de todos los valores serializados.

## Regla de seguridad

La comprobación estructural no reduce el alcance de la política de distribución:

- los campos esperados permanecen solo en el contrato interno de evaluación;
- el resultado entregado al estudiante no puede contenerlos como claves;
- no está autorizado incluir el contrato con respuestas en un bundle público;
- cualquier futura publicación exige una revisión de despliegue separada.

## Límites

Esta nota documenta el comportamiento del gate. No constituye revisión profesional externa, evidencia con estudiantes, autorización de teoría completa ni autorización de publicación.
