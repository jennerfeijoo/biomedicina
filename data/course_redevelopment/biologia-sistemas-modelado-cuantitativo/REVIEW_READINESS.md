# Preparación para revisión disciplinar

## Estado

El curso permanece en `review`. Los validadores automáticos comprueban estructura, densidad, bibliografía, enlaces y sincronización, pero no certifican corrección matemática, biológica ni traslacional.

## Perfiles de revisión recomendados

1. Especialista en modelado dinámico de sistemas bioquímicos.
2. Bioestadístico o matemático con experiencia en identificabilidad y estimación.
3. Biólogo de sistemas o fisiólogo con experiencia experimental.
4. Especialista en metabolismo constraint-based.
5. Responsable de estándares interoperables SBML, CellML o COMBINE.

## Preguntas de revisión

- ¿La frontera del sistema y las escalas son coherentes con la pregunta?
- ¿Las ecuaciones conservan masa, carga o cantidades relevantes cuando corresponde?
- ¿Las unidades y signos son correctos en todas las tasas?
- ¿Los métodos numéricos son adecuados para rigidez, eventos y tolerancias?
- ¿La estabilidad local se distingue de robustez global y validez biológica?
- ¿Los modelos estocásticos usan propensiones y estados discretos coherentes?
- ¿Las métricas de red se interpretan con modelos nulos apropiados?
- ¿FBA declara restricciones, intercambio, función objetivo y soluciones alternativas?
- ¿El ajuste separa identificabilidad estructural, práctica y predictibilidad?
- ¿Los estándares exportados reproducen las simulaciones y unidades documentadas?

## Validación técnica materializada

El paquete fuente y sus ocho unidades fueron promovidos y publicados en la rama de revisión. La ronda automatizada comprobó esquema 2.0, densidad teórica, bibliografía, redundancia, conexiones biomédicas, currículo, temario canónico, JSON y HTML derivados, enlaces internos y contrato de publicación.

Durante la validación integral también se corrigieron dependencias editoriales heredadas: el inventario global se actualizó a 87 asignaturas, se completaron los recursos centrales de Machine Learning Biomédico y Ómicas, y la regeneración determinista del sitio quedó sincronizada con las páginas versionadas.

Esta evidencia acredita coherencia técnica y sincronización del artefacto. No constituye revisión disciplinar de ecuaciones y supuestos, validación experimental, certificación de interoperabilidad en herramientas independientes ni autorización para utilizar el modelo en decisiones clínicas o regulatorias.

## Evidencia mínima para promover a `complete`

- revisión documentada por al menos un perfil matemático y uno biológico;
- comprobación independiente de ecuaciones y unidades;
- ejecución de todos los casos y ejercicios;
- verificación de archivos SBML o CellML en una segunda herramienta;
- corrección de observaciones críticas;
- registro explícito de la decisión editorial final.
