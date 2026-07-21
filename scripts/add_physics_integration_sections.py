#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT_DIR = ROOT / "data" / "generated_units" / "fisica-i"

SECTIONS = {
    1: {
        "heading": "Integración avanzada: del mensurando al modelo",
        "paragraphs": [
            "Una cadena de medición completa comienza con una definición operacional del mensurando y termina con una conclusión limitada por la incertidumbre. Entre ambos extremos aparecen sensor, acondicionamiento, muestreo, calibración, procesamiento y modelo. Cada etapa puede introducir sesgo, ruido, retraso o pérdida de información; por ello la trazabilidad debe incluir también decisiones computacionales.",
            "La sensibilidad de una variable derivada puede estudiarse perturbando entradas dentro de sus incertidumbres. Si pequeñas variaciones cambian mucho el resultado, conviene reformular el método, mejorar la medición o reportar un intervalo más amplio. Una cifra estable frente a redondeo no garantiza estabilidad frente a errores sistemáticos.",
            "La reproducibilidad exige conservar datos originales, metadatos, código, versiones y parámetros. Un gráfico final sin la cadena de transformación impide distinguir señal física de artefacto. El análisis debe permitir reconstruir cómo cada muestra produjo cada resultado.",
            "En biomedicina, la variabilidad entre personas no debe mezclarse automáticamente con incertidumbre instrumental. Ambas afectan los datos, pero responden a preguntas distintas. Diseñar un estudio requiere decidir qué variabilidad se desea describir y qué error se intenta reducir."
        ],
        "key_points": [
            "La cadena de medición incluye etapas físicas y computacionales.",
            "La sensibilidad revela fragilidad del resultado frente a entradas.",
            "Reproducibilidad exige datos, metadatos, código y parámetros.",
            "Variabilidad biológica e incertidumbre instrumental deben separarse."
        ]
    },
    2: {
        "heading": "Integración avanzada: identificabilidad dinámica",
        "paragraphs": [
            "Observar movimiento y fuerzas externas no siempre permite identificar de manera única todas las fuerzas internas. Dos conjuntos de parámetros o acciones musculares pueden producir aceleraciones similares. Esta falta de identificabilidad debe reconocerse antes de interpretar una solución como mecanismo único.",
            "El escalado también modifica la dinámica. En sistemas geométricamente semejantes, masa, área y volumen no crecen con la misma potencia de la longitud. Por ello una relación válida para un dispositivo pequeño no se extrapola linealmente a otro tamaño sin revisar fuerzas, rigidez y disipación.",
            "Los modelos dinámicos deben someterse a pruebas de conservación, equilibrio y respuesta a perturbaciones. Un resultado numérico plausible puede ocultar un signo incorrecto o una fuerza duplicada. Los casos límite, como fricción cero o masa muy grande, ayudan a detectar estas incoherencias.",
            "La validación externa compara predicciones con mediciones que no se usaron para ajustar parámetros. Ajustar y evaluar con los mismos datos tiende a sobrestimar la calidad del modelo, especialmente cuando existen muchos parámetros."
        ],
        "key_points": [
            "La dinámica inversa puede tener soluciones internas no únicas.",
            "El cambio de escala altera relaciones entre masa, área y volumen.",
            "Casos límite y conservación detectan errores de implementación.",
            "La validación debe usar información independiente cuando sea posible."
        ]
    },
    3: {
        "heading": "Integración avanzada: exergía y disponibilidad mecánica",
        "paragraphs": [
            "Aunque la energía total se conserva, no toda energía posee la misma capacidad de producir trabajo útil. La disipación reduce la disponibilidad mecánica al distribuir energía en grados de libertad internos. Esta distinción explica por qué recuperar toda la energía térmica generada por fricción no es viable en un dispositivo real.",
            "En ciclos, el trabajo neto es el área cerrada en diagramas apropiados, como fuerza-desplazamiento o presión-volumen. La orientación del ciclo determina el signo. Estas representaciones permiten comparar almacenamiento, retorno y disipación sin depender únicamente de picos.",
            "Los balances experimentales rara vez cierran exactamente. La discrepancia puede provenir de energía omitida, sincronización, deformación no medida o calibración. Debe reportarse como residuo del balance y analizarse frente a la incertidumbre, no forzarse a cero mediante ajustes arbitrarios.",
            "En sistemas activos, energía química o eléctrica entra continuamente. La conservación mecánica simple deja de ser adecuada, pero un balance ampliado sigue siendo válido. Definir puertos de entrada y salida permite comparar actuadores, prótesis y procesos biológicos sin confundir formas de energía."
        ],
        "key_points": [
            "Conservación de energía no implica disponibilidad completa para trabajo.",
            "El área de un ciclo cuantifica trabajo neto o disipación.",
            "Los residuos de balance deben compararse con incertidumbre.",
            "Los sistemas activos requieren contabilizar entradas no mecánicas."
        ]
    },
    4: {
        "heading": "Integración avanzada: modelos tridimensionales",
        "paragraphs": [
            "En tres dimensiones, torque y momento angular no tienen por qué ser paralelos a velocidad angular. La relación L=Iω utiliza un tensor de inercia y depende de los ejes principales. Reducir un movimiento tridimensional a un plano puede ocultar componentes y acoplamientos relevantes.",
            "Los ejes articulares funcionales pueden desplazarse durante el movimiento. Elegir un centro fijo simplifica el cálculo, pero introduce error en brazos de momento y potencias. Los sistemas de coordenadas anatómicos y las convenciones de rotación deben documentarse para comparar estudios.",
            "La estimación de parámetros inerciales segmentarios suele usar tablas poblacionales. Estas aproximaciones pueden ser suficientes para docencia o análisis general, pero introducen incertidumbre individual. Un análisis de sensibilidad permite saber si esa incertidumbre modifica las conclusiones.",
            "Los balances angulares ofrecen una comprobación independiente de la dinámica inversa. Comparar el cambio de momento angular total con el impulso angular externo ayuda a detectar errores de sincronización, signos o marcos de referencia."
        ],
        "key_points": [
            "La rotación tridimensional requiere tensor de inercia y convenciones.",
            "Los ejes articulares no siempre son fijos.",
            "Los parámetros antropométricos añaden incertidumbre individual.",
            "El balance angular puede validar un análisis segmentario."
        ]
    },
    5: {
        "heading": "Integración avanzada: escalas y números adimensionales",
        "paragraphs": [
            "Los números adimensionales permiten comparar sistemas de distinto tamaño sin depender de una unidad concreta. Reynolds compara inercia y viscosidad, mientras Womersley compara pulsatilidad e influencia viscosa en conductos oscilatorios. La similitud dinámica requiere igualar los números relevantes, no solo la geometría.",
            "En modelos físicos de circulación, usar agua en un tubo ampliado no reproduce automáticamente el comportamiento sanguíneo. Densidad, viscosidad, frecuencia, compliance y rugosidad deben escalarse. Un modelo puede conservar una relación y distorsionar otra; la prioridad depende de la pregunta experimental.",
            "La interacción fluido-estructura aparece cuando la presión deforma la pared y esa deformación cambia el flujo. Tratar por separado fluido y pared puede fallar en tubos blandos, válvulas o cámaras. Incluso un modelo reducido debe declarar qué acoplamiento ignora.",
            "Los parámetros agregados como resistencia y compliance son útiles para interpretar redes, pero pueden no ser identificables de manera única con una sola señal. Combinar presión y caudal, aplicar perturbaciones y usar varios regímenes mejora la capacidad de estimación."
        ],
        "key_points": [
            "La similitud dinámica depende de números adimensionales.",
            "Escalar geometría no basta para reproducir un flujo.",
            "La deformación de paredes puede acoplarse con el fluido.",
            "Múltiples mediciones mejoran identificabilidad de parámetros."
        ]
    },
    6: {
        "heading": "Integración avanzada: sistemas lineales y respuesta impulsional",
        "paragraphs": [
            "Un sistema lineal e invariante en el tiempo puede caracterizarse mediante su respuesta impulsional o su función de transferencia. La salida es la convolución de la entrada con esa respuesta. Esta perspectiva conecta osciladores, filtros, transductores y propagación de pulsos dentro de un mismo marco.",
            "La función de transferencia describe amplitud y fase frente a frecuencia. Un sensor puede medir correctamente señales lentas y distorsionar señales cercanas a su resonancia. Calibrar solo con valores constantes no revela ese comportamiento, por lo que la caracterización dinámica es necesaria.",
            "La deconvolución intenta recuperar una entrada a partir de salida y respuesta del sistema, pero amplifica ruido donde la respuesta tiene baja ganancia. La regularización intercambia resolución y estabilidad. Este problema muestra que invertir un sistema matemáticamente no garantiza una reconstrucción fiable.",
            "Los tejidos y dispositivos pueden ser no lineales o variar con el tiempo. Armónicos, dependencia de amplitud y cambios de parámetros son señales de que el modelo lineal falla. La validación debe explorar varios niveles de excitación y condiciones, no una única curva."
        ],
        "key_points": [
            "La respuesta impulsional caracteriza sistemas lineales invariantes.",
            "La respuesta en frecuencia incluye magnitud y fase.",
            "La inversión puede amplificar ruido y requerir regularización.",
            "La dependencia de amplitud revela posibles no linealidades."
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
