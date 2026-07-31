# Resolución de bloqueos · Bioinstrumentación Unidad 6

## Estado

Los bloqueos técnicos `U6-B01` a `U6-B04` quedan resueltos internamente para permitir únicamente la implementación de prácticas sintéticas.

## U6-B01 · Frontera normativa

La unidad separará cuatro niveles:

1. principio físico o de seguridad;
2. vocabulario normativo;
3. requisito verificable;
4. evidencia formal de conformidad.

Los materiales internos no equivalen a certificación, conformidad con una edición normativa concreta, ensayo acreditado ni autorización de uso clínico. Toda referencia normativa futura deberá indicar edición, jurisdicción, alcance y necesidad de interpretación profesional.

## U6-B02 · Ejemplos de corriente

Se fijan dos casos sintéticos de baja energía:

- 5 V rms sobre 10 MΩ: 0.5 µA;
- acoplamiento capacitivo ideal de 100 pF, 50 Hz y 230 V rms: aproximadamente 7.23 µA.

Los valores sirven para aplicar relaciones físicas y comparar rutas de corriente. No son límites regulatorios ni resultados de ensayo de un dispositivo médico.

## U6-B03 · Modelo EMC reproducible

Cada ejercicio declarará fuente, víctima, trayectoria, frecuencia, amplitud, parámetros y limitaciones.

- Conducido: `V_error = I_interference × Z_common`.
- Capacitivo: `I_c = 2πfC_mutualV_source`.
- Inductivo: `V_induced = 2πfMI_source`.
- Radiado: modelo abstracto de ganancia de acoplamiento.

Estos modelos permiten comparar mecanismos, no demostrar inmunidad o cumplimiento EMC.

## U6-B04 · Revisión humana

La revisión disciplinaria queda preparada pero no ejecutada. No se atribuye aprobación profesional. La resolución habilita prácticas sintéticas internas; las evaluaciones y la teoría completa siguen sin autorización.

## Decisión

```text
synthetic_practice_implementation_authorized: true
assessment_implementation_authorized: false
full_theory_drafting_authorized: false
public_release_authorized: false
```

Se prohíben personas, equipos médicos energizados y afirmaciones de seguridad o conformidad.
