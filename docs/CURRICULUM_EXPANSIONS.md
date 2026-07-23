# Expansiones disciplinares auditables

## Propósito

Las matrices de cobertura definen qué debe dominar un curso. Una expansión disciplinar demuestra cómo se materializa esa cobertura en teoría adicional, práctica, literatura primaria, visualización y evaluación. No se usa el número de palabras como sustituto de calidad.

## Estados

- `implemented`: la especificación académica está completa y supera controles automáticos; conserva `academic_status: review`.
- `verified`: existe evidencia de revisión académica humana externa y se documenta en `external_review_evidence`.

## Contrato mínimo

Cada archivo de `data/curriculum_expansions/` debe:

1. corresponder a una asignatura de `data/curriculum_coverage/`;
2. cubrir todos los identificadores de dominio y todos sus temas obligatorios;
3. mapear cada dominio a unidades del curso;
4. definir evidencias de dominio, expansiones teóricas, tareas cuantitativas, taller de literatura y activos visuales;
5. incluir un programa práctico con mediciones, controles y entregables;
6. incluir lectura crítica de literatura primaria;
7. mantener separadas medición, asociación, predicción, mecanismo causal y utilidad clínica;
8. documentar límites, seguridad y requisitos de revisión externa.

## Biología Celular y Tisular

La primera implementación usa como base el sílabo de Yachay Tech de 2017, las diez unidades ya publicadas y la matriz `BC-01` a `BC-10`. Se incorporan explícitamente:

- ósmosis y tonicidad;
- proliferación celular;
- ELISA indirecto y calibración;
- transporte iónico y excitabilidad;
- RE, Golgi y tráfico;
- metabolismo mitocondrial y apoptosis;
- citoesqueleto y migración;
- matriz extracelular y mecanobiología;
- citometría de ciclo y muerte;
- arquitectura tisular y análisis espacial.

Las actividades pueden ejecutarse con datos educativos, simulaciones, imágenes públicas o demostraciones institucionales supervisadas. El repositorio no proporciona protocolos operativos de manipulación biológica.

## Validación

```bash
python scripts/audit_curriculum_expansions.py --strict
python scripts/audit_curriculum_expansions.py --subject biologia-celular-tisular --strict
```

La auditoría comprueba correspondencia exacta de dominios y temas, cobertura práctica, literatura, visuales, controles y evaluación de dominio. Superarla no equivale a acreditación ni a revisión docente externa.
