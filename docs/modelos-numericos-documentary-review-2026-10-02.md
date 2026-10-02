# Reconstrucción documental: Modelos Numéricos en Biomedicina

Fecha: 2026-10-02. Alcance: ficha de asignatura y sus seis unidades.

La versión anterior repetía definiciones y actividades genéricas. La reconstrucción incorpora balances y cálculos propios con condiciones explícitas, fuentes técnicas consultadas y localizadores en cada bibliografía. Los números de los ejercicios son sintéticos; no se presentan como parámetros medidos de tejidos o dispositivos.

## Contenido y comprobaciones

| Unidad | Trabajo realizado | Comprobación representativa |
| --- | --- | --- |
| 1. De problema biomédico a modelo | Estados, parámetros, observación, balance de cámara y escalas | Equilibrio de masa, solución exponencial y tiempo al 90% |
| 2. Geometría y discretización | Geometría, diferencias centrales, ensamblaje y normas | Poisson resuelto en tres mallas; error nodal de orden dos y error entre nodos |
| 3. Modelos de transporte | Flujos, volúmenes finitos, advección, difusión y reacción | Conservación con pérdida de positividad; restricción combinada; transferencia entre especies |
| 4. Mecánica computacional | Elasticidad, barras, apoyos, singularidades y extensiones | Sistema de dos barras, reacciones, energía y efecto de restricción lateral |
| 5. Calibración e incertidumbre | Residuos, pesos, identificabilidad, sensibilidades y covarianza | Mínimos cuadrados exactos, simetría paramétrica y propagación correlacionada |
| 6. Validación y comunicación | Solución fabricada, errores numéricos y comparación experimental | Derivación de fuente, Richardson y escala de una discrepancia sintética |

Se incluyen 16 ejemplos resueltos, 48 problemas con criterios de respuesta, 48 preguntas de autoevaluación y 30 entradas de fuentes en las unidades. La ficha enlaza una selección de diez recursos técnicos, establece prerrequisitos específicos y un proyecto de cámara y soporte sintéticos con módulos diferenciados.

`tests/test_modelos_numericos_examples.py` contiene 13 pruebas que recalculan resultados mediante eliminación racional, balances, integración temporal algebraica y diferenciación finita independiente. Vinculan valores representativos con el texto canónico para detectar discrepancias editoriales. No son validación experimental ni revisión humana.

## Fuentes y alcance

- FEniCSx: Poisson, ecuación del calor, elasticidad, hiperelasticidad y normas de error.
- NIST FiPy: discretización por volúmenes finitos y ejemplos de difusión; Clawpack: advección.
- Gmsh: geometría, mallas y entidades físicas.
- A. F. Bower: formulación por elementos y bloqueo volumétrico; COMSOL: singularidades de tensión.
- NIST/SEMATECH y SciPy: mínimos cuadrados, ponderación, jacobiano y covarianza aproximada.
- JCGM 100:2008, sección 5: propagación de incertidumbre con correlación.
- NASA/NPARC: verificación, validación y convergencia de malla.
- FDA: guía final de credibilidad de modelos mecanísticos, portada fechada 17 de noviembre de 2023, secciones IV y VI. Se conserva su carácter de recomendaciones no vinculantes.

Los localizadores y URL se incluyen en las fuentes canónicas. Las derivaciones sintéticas se distinguen de resultados de las referencias. El estado `review` se conserva: no se atribuye aprobación disciplinar humana, validación clínica ni certificación regulatoria.

## Efecto sobre el catálogo

El detector de marcadores conocidos pasa de 18 asignaturas, 107 unidades y 544 coincidencias a 17 asignaturas, 101 unidades y 512 coincidencias. Desaparecen las 32 coincidencias de esta asignatura. La ausencia de ese marcador no equivale a completitud científica de todo el catálogo. Esta reconstrucción no altera los registros de afirmaciones de otras asignaturas ni oculta sus brechas.

## Validación técnica

La suite `scripts/run_quality.py` completó 98 comprobaciones sin fallos, incluidas dos regeneraciones completas sin diferencias. Se corrigió durante la validación la estructura de `suggested_resources` para conservar objetos bibliográficos compatibles con el generador. La auditoría científica global sigue informando 1821 incidencias en sus registros; este bloque no las presenta como resueltas.
