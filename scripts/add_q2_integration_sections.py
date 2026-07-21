#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT_DIR = ROOT / "data" / "generated_units" / "quimica-ii"

SECTIONS = {
    1: {
        "heading": "Integración avanzada: especiación numérica y sistemas acoplados",
        "paragraphs": [
            "Los equilibrios reales suelen compartir especies. Protonación, complejación, precipitación y unión pueden competir por el mismo componente, de modo que resolver cada reacción por separado viola balances globales. El modelo completo combina constantes, conservación de masa, electroneutralidad y restricciones de no negatividad.",
            "La resolución numérica requiere elegir variables, escalas y valores iniciales. Trabajar con logaritmos de concentraciones puede evitar soluciones negativas y mejorar estabilidad. La convergencia del algoritmo no garantiza una solución química válida: deben comprobarse residuos, balances y sensibilidad a condiciones iniciales.",
            "La identificabilidad química también importa. Dos conjuntos de constantes pueden describir datos limitados de manera parecida. Medir varias especies, cambiar concentración total o pH y usar datos independientes ayuda a distinguir modelos.",
            "En una aplicación biomédica, la especiación calculada es una hipótesis condicionada por temperatura, fuerza iónica y base de datos termodinámica. La predicción debe acompañarse de incertidumbre y, cuando sea posible, de validación experimental directa."
        ],
        "key_points": ["Los equilibrios acoplados comparten balances.", "La solución numérica debe auditarse químicamente.", "Convergencia no implica identificabilidad.", "La especiación requiere validación contextual."]
    },
    2: {
        "heading": "Integración avanzada: capacidad, actividad y nucleación",
        "paragraphs": [
            "La capacidad reguladora es una derivada: mide cuánto ácido o base debe añadirse para cambiar el pH. Dos buffers con el mismo pH pueden tener capacidades muy distintas. En formulación, el objetivo no es solo alcanzar un pH inicial, sino resistir perturbaciones durante almacenamiento, mezcla o uso.",
            "A fuerza iónica elevada, las actividades se separan de las concentraciones. Los pKa aparentes y productos de solubilidad dependen del medio. Modelos como Debye-Hückel o extensiones aportan correcciones limitadas; soluciones concentradas pueden requerir parámetros específicos.",
            "La sobresaturación es una condición termodinámica, pero la precipitación necesita nucleación. Una solución puede permanecer metaestable y precipitar después de agitación, contacto con una superficie o introducción de una semilla. Por ello Q>Ksp no predice el tiempo de aparición del sólido.",
            "El tamaño, la forma y el polimorfismo del precipitado afectan filtración, disolución y respuesta biológica. Una auditoría de solubilidad debe distinguir equilibrio, cinética de nucleación y transformación de fases."
        ],
        "key_points": ["pH y capacidad no son equivalentes.", "La actividad depende del medio.", "Sobresaturación no determina la velocidad.", "La fase sólida tiene propiedades propias."]
    },
    3: {
        "heading": "Integración avanzada: fuerzas impulsoras y sistemas abiertos",
        "paragraphs": [
            "En un sistema abierto, la dirección de un proceso depende de potenciales químicos y flujos. Mantener concentraciones mediante alimentación y retirada puede sostener una reacción lejos del equilibrio. El estado estacionario conserva variables macroscópicas mientras produce entropía y disipa energía.",
            "La afinidad química cuantifica la fuerza impulsora de una reacción y desaparece en equilibrio. Cerca del equilibrio, flujos y fuerzas pueden aproximarse linealmente; lejos de él aparecen acoplamientos y no linealidades. Esta perspectiva conecta termodinámica con transporte y metabolismo.",
            "La exergía representa capacidad de producir trabajo respecto a un entorno. Aunque la energía se conserve, la disipación reduce su disponibilidad. En procesos de separación, bombeo o síntesis, comparar energía suministrada con el límite reversible permite localizar pérdidas.",
            "Los balances biológicos deben definir fronteras, reservorios y tiempos. Afirmar que una vía es favorable usando solo ΔG° ignora composición, transporte y acoplamiento. La interpretación requiere ΔG real y el mecanismo que conecta procesos."
        ],
        "key_points": ["Estado estacionario no es equilibrio.", "La afinidad desaparece en equilibrio.", "La disipación reduce exergía.", "Los balances necesitan fronteras y composición real."]
    },
    4: {
        "heading": "Integración avanzada: diseño cinético e identificabilidad",
        "paragraphs": [
            "La información de un experimento cinético depende de cuándo y dónde se mide. Tomar muchos puntos en una región plana puede aportar menos información que pocos puntos alrededor de un cambio rápido. El diseño óptimo busca condiciones que separen predicciones de modelos competidores.",
            "La identificabilidad estructural pregunta si parámetros únicos pueden recuperarse con datos perfectos; la práctica incorpora ruido y rango limitado. Perfiles de verosimilitud, matrices de sensibilidad y simulaciones ayudan a detectar combinaciones de parámetros no distinguibles.",
            "Los modelos enzimáticos pueden confundir inhibición, desactivación y transporte. Variar enzima, agitación, tiempo de preincubación y geometría crea perturbaciones capaces de separar mecanismos. Ajustar una única curva de velocidad frente a sustrato rara vez resuelve todas las alternativas.",
            "La validación predictiva usa condiciones no empleadas para ajustar: otra temperatura, lote, concentración o matriz. Un modelo que interpola bien puede fallar al extrapolar, por lo que el dominio validado debe declararse."
        ],
        "key_points": ["El muestreo temporal determina información.", "Identificabilidad y ajuste son distintos.", "Las perturbaciones separan mecanismos.", "La validación debe cubrir condiciones nuevas."]
    },
    5: {
        "heading": "Integración avanzada: circuitos equivalentes y trazabilidad",
        "paragraphs": [
            "Los circuitos equivalentes representan procesos interfaciales mediante resistencias, capacitancias y elementos distribuidos. Son modelos, no componentes físicos literales. Diferentes circuitos pueden ajustar el mismo espectro, por lo que la selección necesita plausibilidad química y estabilidad de parámetros.",
            "La impedancia debe medirse dentro de un régimen aproximadamente lineal y estacionario. Una amplitud excesiva altera el sistema; una medición demasiado larga permite deriva. Comprobar causalidad, consistencia y repetición ayuda a detectar espectros inválidos.",
            "La trazabilidad de un sensor incluye referencia, temperatura, historial de acondicionamiento, área efectiva, lote, electrónica y algoritmo. Una calibración sin estos metadatos no puede reproducirse ni compararse entre laboratorios.",
            "La recalibración puede corregir deriva suave, pero no resuelve pérdida de selectividad o cambio de mecanismo. La vigilancia debe diferenciar desplazamiento del cero, cambio de sensibilidad, aumento de ruido y respuesta a interferentes."
        ],
        "key_points": ["Un circuito equivalente es una hipótesis.", "La impedancia exige linealidad y estabilidad.", "La trazabilidad incluye hardware y software.", "Recalibrar no corrige todo deterioro."]
    },
    6: {
        "heading": "Integración avanzada: información química y reproducibilidad",
        "paragraphs": [
            "Una estructura química digital debe conservar conectividad, carga, isótopos y estereoquímica. Identificadores como SMILES o InChI facilitan intercambio, pero pueden diferir en canonicalización, tautomería y protonación. El archivo fuente y las reglas de normalización deben documentarse.",
            "Las bases químicas integran datos con calidades distintas. Un valor de pKa, solubilidad o actividad puede depender de método, temperatura, forma sólida y matriz. Reutilizarlo exige recuperar condiciones y procedencia, no copiar una cifra aislada.",
            "Los análisis computacionales deben versionar estructuras, parámetros, software y semillas. La preparación molecular —protonación, conformeros, cargas— puede influir más que el algoritmo posterior. Una canalización reproducible registra cada transformación.",
            "El proyecto final debe separar conocimiento observado, inferido y predicho. Esta distinción permite revisar qué parte proviene de datos, qué parte de un modelo y qué evidencia adicional sería necesaria para una aplicación biomédica."
        ],
        "key_points": ["Los identificadores deben conservar química relevante.", "Los datos requieren procedencia y condiciones.", "La preparación molecular forma parte del método.", "Observación, inferencia y predicción deben separarse."]
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
        json.loads(path.read_text(encoding="utf-8"))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
