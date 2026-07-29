# Preparación para revisión — Análisis Estadístico Multivariado

## Estado

`review`

## Revisiones requeridas

1. **Estadística multivariada:** ecuaciones, supuestos, inferencia y terminología.
2. **Bioestadística:** diseño, faltantes, multiplicidad y tamaños de efecto.
3. **Alta dimensión:** regularización, estabilidad, leakage y validación.
4. **Biomedicina computacional:** batch effects, composicionalidad e integración de modalidades.
5. **Reproducibilidad:** código, versiones, semillas, particiones y documentación.

## Criterios antes de `complete`

- verificar directamente todas las fuentes;
- ejecutar y revisar ejemplos reproducibles;
- auditar cada ecuación y notación;
- comprobar que ninguna figura sugiera certeza inexistente;
- validar fronteras con cursos vecinos;
- documentar revisión humana y cambios derivados.

## Riesgos conocidos

- sobreinterpretación de PCA y clustering;
- selección inestable cuando p supera n;
- confusión entre análisis multivariado y machine learning;
- corrección de batch que elimina señal biológica;
- inferencia post-selección no controlada.
