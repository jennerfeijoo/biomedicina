#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
COURSE_ROOT = ROOT / "data" / "course_redevelopment"

PATCHES: dict[str, dict[str, Any]] = {
    "biologia-desarrollo": {
        "study_method": [
            "Comenzar por especie, estadio, tejido, escala y pregunta causal.",
            "Separar observación, marcador, destino, linaje y función.",
            "Comparar perturbación, rescate, trazado de linaje e imagen temporal.",
            "Conservar lote, unidad experimental, metadatos y límites de extrapolación.",
            "Integrar evidencia molecular, celular, mecánica, espacial y comparativa."
        ],
        "diagnostic_assessment": {
            "title": "Diagnóstico de prerrequisitos para Biología del Desarrollo",
            "purpose": "Identificar brechas conceptuales y metodológicas antes de iniciar; no se utiliza como calificación.",
            "questions": [
                {"question": "¿En qué se diferencian especificación y determinación?", "answer": "La especificación expresa un destino en un ambiente neutral y todavía puede ser reversible; la determinación mantiene el destino incluso tras cambiar el contexto."},
                {"question": "¿Qué diferencia existe entre un fate map y un trazado de linaje?", "answer": "El fate map relaciona posición inicial con destinos probables; el trazado de linaje sigue descendencia celular mediante una marca heredable o registro temporal."},
                {"question": "¿Por qué necesidad y suficiencia requieren diseños distintos?", "answer": "La pérdida de función evalúa necesidad y la ganancia o exposición ectópica evalúa suficiencia; ninguna prueba sustituye automáticamente a la otra."},
                {"question": "¿Un marcador celular demuestra identidad o función?", "answer": "No. Un marcador informa asociación con un estado; identidad y función requieren evidencia adicional, contexto y, cuando corresponde, perturbación o desempeño funcional."},
                {"question": "¿Qué es pseudorreplicación en un experimento del desarrollo?", "answer": "Es tratar células, imágenes o secciones dependientes de un mismo embrión, organoide o lote como réplicas biológicas independientes."},
                {"question": "¿Una trayectoria de single-cell demuestra linaje causal?", "answer": "No. Ordena estados compatibles con un modelo; el linaje causal necesita información temporal, clonabilidad, marcas heredables o perturbaciones apropiadas."},
                {"question": "¿Por qué deben compararse estadios equivalentes entre especies o condiciones?", "answer": "La edad cronológica no garantiza equivalencia del desarrollo; comparar estadios distintos puede convertir heterocronía en una falsa diferencia mecanística."},
                {"question": "¿Qué evidencia sostiene un modelo de morfógeno?", "answer": "Distribución espacial y temporal, respuesta dependiente de concentración o duración, receptores y transducción pertinentes, perturbación, rescate y predicción de fronteras o destinos."},
                {"question": "¿Cómo se evalúa la validez de un organoide?", "answer": "Mediante origen celular, composición, arquitectura, madurez, función, reproducibilidad, estabilidad y benchmarking predefinido contra el tejido o proceso que pretende modelar."},
                {"question": "¿Una asociación prenatal permite atribuir causalidad individual?", "answer": "No. Requiere temporalidad, medición de exposición, control de confusión, plausibilidad, dosis, replicación y evidencia convergente; aun así puede no predecir un caso individual."}
            ],
            "interpretation": [
                "8–10 respuestas correctas: preparación suficiente para iniciar el curso.",
                "5–7: nivelación paralela en biología celular, genética, estadística y diseño experimental.",
                "0–4: reforzar prerrequisitos antes de abordar causalidad y métodos del desarrollo."
            ]
        },
        "assessment_principles": [
            "La evaluación prioriza relaciones causales, espacio-temporales y evidencia experimental.",
            "Marcadores, clusters y trayectorias no se presentan como función o linaje demostrado.",
            "Toda comparación declara especie, estadio, tejido, unidad experimental y referencia.",
            "Las conexiones humanas distinguen mecanismo, asociación, riesgo y uso clínico.",
            "Los modelos embrionarios y células madre se analizan bajo supervisión y límites éticos explícitos."
        ],
        "final_project": {
            "title": "Atlas causal y espacio-temporal de un proceso del desarrollo",
            "scenario": "Analizar una pregunta del desarrollo mediante literatura primaria, datos abiertos, imágenes o simulación, integrando estado celular, posición, tiempo, perturbación, incertidumbre y límites éticos.",
            "phases": [
                "Delimitar proceso, especie, estadio, tejido, escala y pregunta causal.",
                "Construir un modelo causal con actores, señales, fuerzas, estados y predicciones.",
                "Seleccionar evidencia, datos y controles con metadatos y unidad experimental explícitos.",
                "Analizar patrones, perturbaciones, alternativas y sensibilidad del resultado.",
                "Integrar conclusiones, límites de extrapolación, reproducibilidad y defensa crítica."
            ],
            "deliverables": [
                "Diagrama causal y mapa espacio-temporal del proceso.",
                "Matriz de evidencia que separa observación, marcador, perturbación, rescate y función.",
                "Cuaderno o informe reproducible con figuras, metadatos y análisis.",
                "Registro de alternativas, resultados negativos e incertidumbre.",
                "Síntesis crítica y presentación para revisión por pares."
            ],
            "integration_requirements": [
                "estado y linaje celular",
                "señalización y redes reguladoras",
                "morfogénesis y mecánica",
                "evidencia experimental o computacional",
                "traslación y límites éticos"
            ],
            "rubric": [
                {"criterion": "Pregunta y modelo causal", "weight_percent": 20, "excellent": "Delimita escala, estadio, actores, relaciones y predicciones falsables."},
                {"criterion": "Evidencia y diseño", "weight_percent": 25, "excellent": "Usa controles, unidad experimental y evidencia convergente apropiados."},
                {"criterion": "Análisis espacio-temporal", "weight_percent": 20, "excellent": "Integra posición, tiempo, linaje, dinámica y variabilidad de forma reproducible."},
                {"criterion": "Trazabilidad y reproducibilidad", "weight_percent": 20, "excellent": "Fuentes, datos, metadatos, decisiones y artefactos pueden auditarse."},
                {"criterion": "Comunicación, incertidumbre y ética", "weight_percent": 15, "excellent": "Distingue mecanismo, asociación, extrapolación y límites de uso responsable."}
            ]
        },
        "core_resources": [
            {"title": "Developmental Biology 13e", "organization": "Oxford University Press", "url": "https://www.oup.com.au/books/higher-education/biology/9780197574591", "type": "libro de referencia", "verification_status": "verified_directly"},
            {"title": "SDB Collaborative Resources", "organization": "Society for Developmental Biology", "url": "https://www.sdbonline.org/sdb_core", "type": "sociedad científica", "verification_status": "verified_directly"},
            {"title": "MIT OpenCourseWare Developmental Biology", "organization": "MIT OpenCourseWare", "url": "https://ocw.mit.edu/courses/7-22-developmental-biology-fall-2005/", "type": "curso universitario abierto", "verification_status": "verified_directly"},
            {"title": "Human Developmental Biology Resource", "organization": "HDBR", "url": "https://www.hdbr.org/", "type": "atlas humano", "verification_status": "verified_directly"},
            {"title": "ISSCR Guidelines", "organization": "International Society for Stem Cell Research", "url": "https://www.isscr.org/guidelines", "type": "guía científica y ética", "verification_status": "verified_directly"},
            {"title": "EMBL-EBI Single-cell Training", "organization": "EMBL-EBI", "url": "https://www.ebi.ac.uk/training/online/courses/single-cell-rna-seq-analysis/", "type": "formación metodológica", "verification_status": "verified_directly"},
            {"title": "Human Cell Atlas Data Portal", "organization": "Human Cell Atlas", "url": "https://data.humancellatlas.org/", "type": "datos celulares humanos", "verification_status": "verified_directly"},
            {"title": "CELLxGENE Discover", "organization": "Chan Zuckerberg Initiative", "url": "https://cellxgene.cziscience.com/", "type": "atlas y exploración single-cell", "verification_status": "verified_directly"}
        ]
    },
    "ecuaciones-diferenciales": {
        "study_method": [
            "Formular balances y unidades antes de resolver o simular.",
            "Comparar análisis exacto, cualitativo y numérico según la pregunta.",
            "Comprobar positividad, invariantes, escalas y casos límite.",
            "Separar error numérico, incertidumbre de datos y discrepancia estructural.",
            "Tratar ajuste, validación, predicción y utilidad como etapas distintas."
        ],
        "diagnostic_assessment": {
            "title": "Diagnóstico de prerrequisitos para Ecuaciones Diferenciales",
            "purpose": "Identificar brechas matemáticas y computacionales antes de iniciar; no se utiliza como calificación.",
            "questions": [
                {"question": "¿En qué se diferencia un estado de un parámetro?", "answer": "El estado evoluciona con el tiempo o espacio según el modelo; el parámetro caracteriza una relación y se trata como constante dentro del escenario declarado."},
                {"question": "¿Qué elementos definen un problema de valor inicial?", "answer": "La ecuación o sistema, dominio, parámetros, condición inicial y supuestos que garantizan significado y, cuando corresponde, existencia y unicidad."},
                {"question": "¿Por qué una ecuación debe ser dimensionalmente coherente?", "answer": "Cada término sumado debe compartir dimensiones; una inconsistencia revela una formulación, conversión o interpretación incorrecta."},
                {"question": "¿Qué diferencia existe entre equilibrio y estabilidad?", "answer": "Un equilibrio anula la derivada; la estabilidad describe qué ocurre con soluciones cercanas después de una perturbación."},
                {"question": "¿Qué informan los autovalores de un sistema lineal?", "answer": "Informan tasas y modos de crecimiento, decaimiento u oscilación, y permiten clasificar estabilidad bajo las condiciones del modelo."},
                {"question": "¿Qué representa una nulclina?", "answer": "El conjunto donde la derivada de una variable es cero; sus intersecciones ayudan a localizar equilibrios, pero no describen por sí solas todo el flujo."},
                {"question": "¿Para qué sirve refinar el paso de integración?", "answer": "Permite evaluar convergencia y separar comportamiento del modelo de artefactos de discretización, aunque no corrige un modelo estructuralmente inadecuado."},
                {"question": "¿Qué caracteriza a un problema rígido?", "answer": "Contiene escalas temporales muy separadas que restringen la estabilidad de métodos explícitos y pueden exigir integradores apropiados."},
                {"question": "¿Qué es identificabilidad paramétrica?", "answer": "La posibilidad de determinar parámetros de manera única o suficientemente precisa a partir del modelo, observables, diseño y datos disponibles."},
                {"question": "¿Por qué calibración y validación no son equivalentes?", "answer": "La calibración ajusta parámetros con ciertos datos; la validación evalúa predicciones o propiedades predefinidas en evidencia independiente o condiciones no usadas para ajustar."}
            ],
            "interpretation": [
                "8–10 respuestas correctas: preparación suficiente para iniciar el curso.",
                "5–7: nivelación paralela en cálculo, álgebra lineal y programación científica.",
                "0–4: reforzar prerrequisitos antes de abordar sistemas dinámicos y simulación."
            ]
        },
        "assessment_principles": [
            "Toda solución debe comprobar ecuación, condición, unidades y dominio.",
            "El análisis cualitativo precede a la interpretación de simulaciones complejas.",
            "La precisión computacional se separa de la adecuación estructural del modelo.",
            "Los parámetros ajustados se comunican con sensibilidad, identificabilidad e incertidumbre.",
            "Una trayectoria ajustada no demuestra mecanismo ni utilidad clínica."
        ],
        "final_project": {
            "title": "Modelo dinámico biomédico auditable",
            "scenario": "Formular, analizar, simular y evaluar un sistema dinámico educativo usando datos sintéticos o abiertos, con unidades, sensibilidad, validación y límites de inferencia.",
            "phases": [
                "Delimitar pregunta, estados, parámetros, entradas, observables y escalas.",
                "Derivar el modelo desde balances y auditar unidades, condiciones e invariantes.",
                "Realizar análisis analítico o cualitativo y establecer predicciones previas a la simulación.",
                "Implementar, verificar y comparar simulaciones con análisis de error y sensibilidad.",
                "Evaluar parámetros, incertidumbre, validación, alternativas y límites de extrapolación."
            ],
            "deliverables": [
                "Diagrama del sistema, tabla de variables y derivación del modelo.",
                "Análisis de equilibrios, estabilidad, escalas o geometría dinámica.",
                "Notebook ejecutable con pruebas, refinamiento y gráficos reproducibles.",
                "Informe de sensibilidad, identificabilidad, validación y discrepancia.",
                "Síntesis crítica y defensa ante revisión por pares."
            ],
            "integration_requirements": [
                "formulación y unidades",
                "análisis cualitativo",
                "simulación y verificación",
                "sensibilidad e identificabilidad",
                "validación y comunicación"
            ],
            "rubric": [
                {"criterion": "Formulación y coherencia", "weight_percent": 20, "excellent": "Estados, balances, unidades, condiciones y supuestos son explícitos y coherentes."},
                {"criterion": "Análisis matemático", "weight_percent": 20, "excellent": "Equilibrios, estabilidad, escalas y comportamiento se analizan correctamente."},
                {"criterion": "Verificación computacional", "weight_percent": 20, "excellent": "Código, integradores, tolerancias, refinamiento y pruebas son reproducibles."},
                {"criterion": "Inferencia y validación", "weight_percent": 25, "excellent": "Sensibilidad, identificabilidad, incertidumbre y evidencia independiente sostienen conclusiones proporcionales."},
                {"criterion": "Comunicación y límites", "weight_percent": 15, "excellent": "Distingue ajuste, predicción, mecanismo y utilidad, y documenta limitaciones."}
            ]
        },
        "core_resources": [
            {"title": "Introduction to Mathematics for Computational Biology", "organization": "Springer", "url": "https://doi.org/10.1007/978-3-031-36566-9", "type": "libro de referencia", "verification_status": "metadata_verified"},
            {"title": "Modeling in Computational Biology and Biomedicine", "organization": "Springer", "url": "https://doi.org/10.1007/978-3-642-31208-3", "type": "libro interdisciplinario", "verification_status": "metadata_verified"},
            {"title": "MIT OpenCourseWare Differential Equations", "organization": "MIT OpenCourseWare", "url": "https://ocw.mit.edu/courses/18-03sc-differential-equations-fall-2011/", "type": "curso universitario abierto", "verification_status": "verified_directly"},
            {"title": "SciPy solve_ivp", "organization": "SciPy", "url": "https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html", "type": "documentación de integración numérica", "verification_status": "verified_directly"},
            {"title": "DifferentialEquations.jl", "organization": "SciML", "url": "https://docs.sciml.ai/DiffEqDocs/stable/", "type": "documentación de sistemas dinámicos", "verification_status": "verified_directly"},
            {"title": "SymPy ODE Solvers", "organization": "SymPy", "url": "https://docs.sympy.org/latest/modules/solvers/ode.html", "type": "documentación de métodos simbólicos", "verification_status": "verified_directly"},
            {"title": "NumPy Testing", "organization": "NumPy", "url": "https://numpy.org/doc/stable/reference/testing.html", "type": "documentación de verificación computacional", "verification_status": "verified_directly"},
            {"title": "Jupyter Book", "organization": "Project Jupyter", "url": "https://jupyterbook.org/en/stable/", "type": "documentación reproducible", "verification_status": "verified_directly"}
        ]
    }
}


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: la raíz debe ser un objeto")
    return data


def main() -> int:
    for subject_id, patch in PATCHES.items():
        path = COURSE_ROOT / subject_id / "course.json"
        course = load_json(path)
        course.update(patch)
        path.write_text(json.dumps(course, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"[ok] {subject_id}: arquitectura formal completada")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
