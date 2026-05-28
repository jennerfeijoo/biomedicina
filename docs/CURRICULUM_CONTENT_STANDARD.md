# Estándar curricular universitario para CitoNauta

## 1. Principio rector

A partir de esta fase, una asignatura de CitoNauta no debe tratarse como una página breve de presentación. Cada asignatura debe aspirar a funcionar como una guía de curso universitario: suficientemente completa para orientar aprendizaje autónomo, diseño de clases, planificación de estudio, producción de material educativo y conexión con aplicaciones biomédicas reales.

La página web puede mostrar una versión navegable y resumida, pero el contenido fuente debe permitir expandir cada asignatura hasta nivel de curso.

## 2. Diferencia entre página mínima y curso completo

Una página mínima contiene:

- título;
- descripción;
- propósito;
- objetivos generales;
- módulos sugeridos;
- conceptos clave.

Un curso completo debe contener además:

- nivel académico;
- carga estimada;
- prerrequisitos;
- competencias;
- resultados de aprendizaje evaluables;
- unidades temáticas detalladas;
- actividades prácticas;
- sistema de evaluación;
- recursos y bibliografía;
- conexiones con otras asignaturas;
- aplicaciones biomédicas;
- productos esperados del estudiante.

## 3. Estructura recomendada por asignatura

Cada archivo en `data/subjects/<area_id>/<subject_id>.json` puede evolucionar hacia la siguiente estructura:

```json
{
  "id": "...",
  "area_id": "...",
  "status": "draft",
  "title": "...",
  "description": "...",
  "level": "pregrado universitario",
  "estimated_workload": "12-16 semanas; 90-150 horas de trabajo total",
  "prerequisites": [],
  "course_competencies": [],
  "learning_objectives": [],
  "learning_outcomes": [],
  "modules": [],
  "detailed_units": [
    {
      "unit": 1,
      "title": "...",
      "description": "...",
      "topics": [],
      "learning_outcomes": [],
      "activities": [],
      "biomedical_applications": []
    }
  ],
  "practical_activities": [],
  "assessment": [],
  "key_concepts": [],
  "biomedical_connection": "...",
  "related_subjects": [],
  "suggested_resources": []
}
```

## 4. Nivel de detalle esperado

Cada asignatura completa debe tener, como mínimo:

- 6 a 10 unidades temáticas;
- 4 a 8 objetivos generales;
- 6 a 12 resultados de aprendizaje evaluables;
- 10 a 25 conceptos clave;
- 4 a 8 actividades prácticas;
- 3 a 6 componentes de evaluación;
- 5 a 12 recursos sugeridos;
- conexiones explícitas con otras asignaturas.

## 5. Reglas editoriales

- El contenido debe ser claro, técnico y útil para aprendizaje universitario.
- No debe limitarse a listas genéricas.
- Cada módulo debe conectar conceptos con problemas biomédicos reales.
- Las actividades deben ser factibles para estudiantes con recursos abiertos.
- Las evaluaciones deben medir comprensión, análisis, aplicación y comunicación.
- Las páginas deben evitar prometer certificación formal; son guías educativas abiertas.
- Cuando se añadan referencias específicas, deben verificarse antes de publicarse.

## 6. Estados editoriales

- `placeholder`: página creada como marcador estructural.
- `draft`: contenido inicial útil, pero no completamente revisado.
- `review`: curso detallado pendiente de revisión final.
- `complete`: curso completo, revisado y coherente con el estándar.

## 7. Estrategia de migración

No se deben migrar decenas de asignaturas con contenido superficial. La prioridad debe ser:

1. consolidar el modelo de curso completo;
2. migrar pocas asignaturas con alto nivel de detalle;
3. revisar visualmente y pedagógicamente;
4. escalar por bloques pequeños.

La regla práctica es:

> Menos asignaturas, pero más completas y útiles.

## 8. Criterio de aceptación para una asignatura completa

Una asignatura puede considerarse lista para `review` cuando:

- tiene propósito formativo claro;
- contiene unidades temáticas detalladas;
- incluye actividades prácticas;
- define resultados de aprendizaje evaluables;
- conecta con aplicaciones biomédicas;
- contiene evaluación sugerida;
- incluye recursos o bibliografía orientativa;
- sus enlaces internos funcionan;
- su página es legible en móvil.
