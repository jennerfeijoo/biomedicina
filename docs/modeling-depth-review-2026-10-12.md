# Revisión de Modelado y Simulación en Biomedicina

Reescritura del 11 de octubre; comprobaciones y preparación de publicación del 12 de octubre de 2026. Estado: **review**. Esta es una revisión interna de una asignatura, no una validación científica independiente ni una declaración de dominio completo del proyecto.

## Problema corregido

Las seis unidades repetían una estructura genérica, definiciones sin contenido disciplinar y referencias a mecánica que no explicaban estimación o procesos estocásticos. Se sustituyeron sus desarrollos, objetivos, ejemplos, actividades, errores, preguntas, fuentes y presentación del curso. Se sincronizaron los originales de `course_redevelopment`, los archivos publicados y el catálogo para evitar que una regeneración restaurase el texto anterior.

## Contenido de las unidades

| Unidad | Desarrollo específico | Figura y comprobación destacada |
|---|---|---|
| 1. Formulación | Contexto de uso, estados y observables, fronteras, balances, dimensiones, volumen variable y escalas | Dilución con cantidad constante; regla del producto para A=VC |
| 2. Deterministas | Eliminación y entrada, dos compartimentos, equilibrio, estabilidad, positividad, Euler, rigidez y eventos | Euler estable en magnitud que produce cantidades negativas; comparación con solución analítica |
| 3. Estocásticos y agentes | Markov, tasas y probabilidades, esperas, eventos competidores, reglas de agentes, réplicas y MCSE | Diferencia entre λΔt y 1−exp(−λΔt); transición de Markov calculada |
| 4. Estimación | Residuos y ponderación, identificabilidad, sensibilidad local y global, dependencias e incertidumbre | Dos pares CL,V producen la misma curva normalizada; derivada contrastada por diferencias finitas |
| 5. Verificación y validación | Referencias, invariantes, refinamiento, orden observado, datos independientes, métricas y discrepancias | Convergencia de Euler, correlación sin acuerdo y criterios contextualizados |
| 6. Decisiones | Escenarios, pérdidas, umbrales, Pareto, robustez, arrepentimiento, información y seguimiento | Cruce de pérdidas esperadas en p=1/3 y valor de información perfecta |

Cada unidad contiene cuatro desarrollos teóricos, seis objetivos, diez casos resueltos, ocho tareas de transferencia, diez errores corregidos, 24 autoevaluaciones razonadas y 16 términos de glosario. Las seis figuras son originales, reproducibles desde ecuaciones y cuentan con texto alternativo, unidades, alcance sintético y preguntas de observación.

La teoría continua tiene entre 862 y 949 palabras por unidad, además de casos, preguntas y actividades. La auditoría conserva su alerta heurística de menos de 1000 palabras: no se cambió el umbral ni se añadió texto de relleno para ocultarla. La extensión no prueba suficiencia; queda pendiente examinar profundidad y carga de aprendizaje con revisión independiente.

## Bancos y selección

- **60 candidatos por unidad; 360 en total.** Se componen de 24 preguntas abiertas, 10 análisis de errores, 10 casos y 16 correspondencias de glosario. No son 360 preguntas de opción múltiple ni 360 ítems validados psicométricamente.
- **Test de unidad: 15 preguntas. Final: 50.** La selección no repite identificadores ni enunciados dentro del intento.
- Cada uno de los **36 objetivos** tiene cuatro preguntas abiertas alineadas manualmente. El motor reserva una pregunta por objetivo en cada unidad representada, antes de completar la selección aleatoria. En el final añade además un caso y un análisis de error de cada unidad.
- La reserva se activa únicamente en unidades con una matriz explícita. Si faltan ítems para un objetivo o el tamaño no permite cubrirlos, el motor falla de forma visible en vez de presentar una cobertura incompleta como completa.
- La representación de objetivos no garantiza cubrir todos sus subtemas ni medir ejecución práctica. La dificultad, discriminación, ambigüedad y utilidad del banco requieren pilotaje.
- Las respuestas abiertas siguen siendo **autoevaluadas** mediante solución y rúbrica. El texto no recibe corrección semántica automática. Los blancos ya no se contabilizan como respuestas autoevaluadas.

Se corrigieron referencias dependientes de otros ejercicios, como «la misma matriz» o «la misma tabla», para que los casos seleccionados sean comprensibles por separado. El diagnóstico de entrada tiene doce preguntas específicas con sus soluciones; se retiraron puntos de corte sin validación.

## Correcciones de publicación

El generador omitía el campo de respuesta explícita de algunos casos aunque mostraba razonamiento e interpretación. Ahora presenta también «Solución». La corrección beneficia a las páginas que utilizan ese campo; no implica una revisión científica nueva de esas otras asignaturas.

La presentación del curso deja de llamarlo «curso completo» y declara fundamentos seleccionados, estado de revisión y evidencia pendiente. El proyecto integrador exige formulación, componentes determinista y estocástico pertinentes, estimación, verificación, contraste y decisiones condicionadas.

## Comprobaciones reproducibles

- `tests/test_modeling_revision.py`: cálculos de cantidad y volumen, soluciones analíticas, convergencia y positividad de Euler, Markov, error Monte Carlo, sensibilidad, identificabilidad, pérdidas y valor de información; presencia de figuras y soluciones en las páginas.
- `tests/test_assessment_banks.cjs`: conserva las comprobaciones de todo el corpus y añade 40 selecciones por unidad y 100 finales para verificar los 36 objetivos, casos, errores, tamaño y ausencia de repetición. Comprueba también rechazo de bancos sin un objetivo y tamaños insuficientes.
- `scripts/build_modeling_figures.py`: reproduce las seis figuras. Inspección visual de ejes, leyendas, alcance y legibilidad.
- `scripts/publish_courses.py`, `scripts/sync_catalog_statuses.py` y `scripts/generate_site.py`: sincronizan originales, derivados, catálogo y páginas. Las dos regeneraciones de la última suite no modificaron archivos.

Estas pruebas comprueban propiedades y cálculos específicos. No prueban ausencia de todo error conceptual ni validan los supuestos en sistemas reales.

## Fuentes y alcance

Las unidades identifican fuentes y documentación según su función: [NIBIB](https://www.nibib.nih.gov/science-education/science-topics/computational-modeling), [página de la guía FDA](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/assessing-credibility-computational-modeling-and-simulation-medical-device-submissions), [solve_ivp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html), [curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html), [ODD 2020](https://www.jasss.org/23/2/7.html), [SALib](https://salib.readthedocs.io/en/latest/user_guide/basics.html) y [registro de STRESS](https://www.equator-network.org/reporting-guidelines/strengthening-the-reporting-of-empirical-simulation-studies-introducing-the-stress-guidelines/). El [texto de Preston y colaboradores](https://arxiv.org/abs/2508.18853) se identifica expresamente como preprint y lectura complementaria.

Las soluciones y figuras son ejercicios sintéticos desarrollados para este curso; no son datos clínicos ni recomendaciones asistenciales. La consulta de la página de una guía no se presenta como revisión completa de sus documentos asociados ni como cumplimiento regulatorio.

## Pendientes

1. Revisión disciplinar y pedagógica independiente de explicaciones, fuentes, enunciados y claves.
2. Soluciones detalladas y rúbricas específicas para todas las tareas abiertas de transferencia; la rúbrica actual es común y formativa.
3. Pilotaje con alumnado y análisis de errores, dificultad, discriminación y carga de trabajo.
4. Ampliación de preguntas basadas directamente en figuras y conjuntos de datos; las preguntas de observación actuales están junto a las figuras y no forman un banco visual del examen.
5. Profundizaciones diferenciadas en modelos espaciales, EDP, elementos finitos, multiescala y otros dominios que estas seis unidades no cubren exhaustivamente.
6. Continuar la reconstrucción del resto del proyecto: **89 unidades de 15 asignaturas** conservan marcadores conocidos de plantilla. Su ausencia en otras unidades tampoco implica validación.
