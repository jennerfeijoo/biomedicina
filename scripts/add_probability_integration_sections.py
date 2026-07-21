#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT_DIR = ROOT / "data" / "generated_units" / "probabilidad-estadistica"

SECTIONS = {
    1: {
        "heading": "Integración avanzada: probabilidad, conocimiento y mecanismos",
        "paragraphs": [
            "La misma cifra probabilística puede representar aleatoriedad física, variación entre unidades o incertidumbre sobre un parámetro. Separar estas fuentes evita interpretar una distribución de población como incertidumbre individual o tratar desconocimiento como variabilidad irreducible.",
            "Un modelo generativo describe cómo podrían producirse los datos: selección de unidades, estado latente, medición y pérdidas. Escribir ese proceso revela dependencias y denominadores que permanecen ocultos en una tabla final.",
            "La calibración probabilística compara predicciones con frecuencias observadas en grupos comparables. Una probabilidad bien calibrada no necesariamente discrimina bien y una clasificación precisa puede estar mal calibrada.",
            "La evaluación debe usar datos no empleados para construir el modelo. Reutilizar la misma muestra para elegir variables, ajustar probabilidades y comprobarlas produce optimismo y subestima la incertidumbre."
        ],
        "key_points": [
            "Probabilidad puede representar fuentes de incertidumbre diferentes.",
            "Los modelos generativos hacen visibles selección y dependencia.",
            "Calibración y discriminación son propiedades distintas.",
            "La evaluación independiente limita el optimismo."
        ]
    },
    2: {
        "heading": "Integración avanzada: dependencia diagnóstica y verificación",
        "paragraphs": [
            "Las pruebas pueden compartir mecanismos de error, muestras o condiciones preanalíticas. Condicionar por el estado de enfermedad no garantiza independencia si ambos ensayos responden al mismo interferente. Combinar razones de verosimilitud exige estudiar esta dependencia.",
            "El estándar de referencia puede ser imperfecto. Tratarlo como verdad absoluta transfiere sus errores a sensibilidad y especificidad. Los modelos de clase latente intentan estimar estados no observados, pero requieren supuestos de identificabilidad difíciles de verificar.",
            "La verificación parcial ocurre cuando solo algunos resultados reciben confirmación. Si la probabilidad de verificación depende de la prueba o del estado clínico, los conteos observados no representan la tabla completa.",
            "La validación diagnóstica debe describir flujo de participantes, resultados indeterminados, tiempos entre pruebas y cegamiento. Estas decisiones pueden cambiar el rendimiento tanto como la fórmula usada."
        ],
        "key_points": [
            "Las pruebas secuenciales pueden compartir errores.",
            "Un estándar imperfecto sesga métricas diagnósticas.",
            "La verificación selectiva altera denominadores.",
            "El flujo del estudio forma parte del rendimiento."
        ]
    },
    3: {
        "heading": "Integración avanzada: condicionamiento y descomposición de varianza",
        "paragraphs": [
            "La ley de esperanza total expresa E(X)=E[E(X|Z)]. Permite separar el promedio global en promedios de subgrupos ponderados y conecta modelos jerárquicos con agregación poblacional.",
            "La varianza total se descompone en variabilidad promedio dentro de grupos y variabilidad entre sus medias. Esta identidad explica por qué mezclar poblaciones heterogéneas aumenta dispersión y por qué ajustar por grupos puede cambiar la incertidumbre residual.",
            "Las distribuciones marginales pueden ocultar componentes multimodales. Una media global situada entre dos grupos puede describir mal a cualquiera. Visualizar la mezcla y conservar la variable de grupo evita resumir estructuras distintas como una sola población homogénea.",
            "En modelos jerárquicos, los parámetros de grupo se estiman con información compartida. La contracción reduce estimaciones extremas ruidosas, pero depende de un modelo de distribución entre grupos y no debe confundirse con borrar diferencias reales."
        ],
        "equations": [
            {"label": "Esperanza total", "latex": "E(X)=E[E(X|Z)]"},
            {"label": "Varianza total", "latex": "Var(X)=E[Var(X|Z)]+Var[E(X|Z)]"}
        ],
        "key_points": [
            "El promedio global pondera promedios condicionales.",
            "La varianza total separa componentes dentro y entre grupos.",
            "Las mezclas pueden ser multimodales.",
            "La contracción jerárquica intercambia ruido e información compartida."
        ]
    },
    4: {
        "heading": "Integración avanzada: distribuciones positivas y tiempos",
        "paragraphs": [
            "Muchas variables biomédicas son positivas y asimétricas. Las distribuciones lognormal y gamma ofrecen soportes adecuados para concentraciones, costes y duraciones, mientras la exponencial modela tiempos con tasa constante y propiedad sin memoria.",
            "La elección entre normal sobre escala original, normal sobre logaritmos y gamma cambia la interpretación de medias, efectos y varianza. Debe apoyarse en el mecanismo, los residuos y el objetivo, no en una prueba automática de normalidad.",
            "Los tiempos hasta evento incluyen censura cuando el evento no se observa durante seguimiento. Tratar censurados como tiempos completos o excluirlos sesga resultados. La supervivencia y el riesgo instantáneo describen aspectos distintos del proceso.",
            "La truncación también difiere de censura: ciertos valores nunca entran en la muestra. Un estudio de personas que ya sobrevivieron hasta reclutamiento puede mostrar sesgo de supervivencia si se ignora el mecanismo de entrada."
        ],
        "key_points": [
            "Variables positivas requieren soportes compatibles.",
            "Transformación y familia cambian el estimando.",
            "Censura conserva información parcial del tiempo.",
            "Truncación modifica quién puede aparecer en la muestra."
        ]
    },
    5: {
        "heading": "Integración avanzada: inferencia selectiva y fragilidad",
        "paragraphs": [
            "La inferencia clásica supone que la hipótesis y el análisis no fueron elegidos por el mismo resultado que se evalúa. Seleccionar el efecto más grande y después usar un intervalo convencional produce cobertura deficiente y estimaciones exageradas.",
            "El registro previo, los planes analíticos y la separación entre exploración y confirmación reducen esta selección. No eliminan decisiones legítimas durante el análisis, pero obligan a documentarlas y evaluar su impacto.",
            "La fragilidad puede cuantificarse observando cuánto cambian las conclusiones ante pequeñas modificaciones de datos, definiciones o modelos. Un resultado que cruza un umbral por una sola observación requiere una comunicación diferente a uno estable en múltiples análisis.",
            "Los intervalos de compatibilidad y las funciones de confianza muestran un continuo de valores en lugar de una etiqueta. Esta perspectiva favorece decisiones basadas en magnitud, incertidumbre y consecuencias."
        ],
        "key_points": [
            "Seleccionar resultados altera la inferencia posterior.",
            "La preespecificación mejora transparencia.",
            "La fragilidad evalúa estabilidad ante cambios plausibles.",
            "La evidencia es continua, no una etiqueta binaria."
        ]
    },
    6: {
        "heading": "Integración avanzada: validación predictiva y cambio de distribución",
        "paragraphs": [
            "Un modelo puede fallar porque cambia la relación entre predictores y desenlace, la distribución de predictores o la prevalencia. Estos cambios de distribución afectan calibración y error de manera diferente y requieren vigilancia después de implementación.",
            "La validación temporal evalúa si el modelo mantiene desempeño en períodos posteriores. La validación geográfica o institucional prueba transportabilidad entre centros. Ninguna reemplaza la evaluación prospectiva dentro del flujo donde se usará.",
            "La recalibración ajusta intercepto o pendiente predictiva sin reconstruir todo el modelo. Puede corregir cambios de prevalencia, pero no resuelve predictores obsoletos, nuevas prácticas o errores de medición.",
            "El desempeño por subgrupos debe analizarse con intervalos y tamaño suficiente. Diferencias aparentes pueden ser ruido, mientras un promedio global adecuado puede ocultar fallos sistemáticos en grupos relevantes."
        ],
        "key_points": [
            "El cambio de distribución puede afectar varias propiedades del modelo.",
            "La validación debe reflejar tiempo, lugar y flujo real.",
            "Recalibrar no corrige todos los mecanismos de deterioro.",
            "Los subgrupos requieren precisión y justificación."
        ]
    }
}


def main() -> int:
    for unit, section in SECTIONS.items():
        path = UNIT_DIR / f"unit-{unit:02d}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        headings = {item.get("heading") for item in data.get("theory_sections", [])}
        if section["heading"] not in headings:
            data["theory_sections"].append(section)
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"Ampliada: {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
