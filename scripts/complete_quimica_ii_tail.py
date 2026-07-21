#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT_DIR = ROOT / "data" / "generated_units" / "quimica-ii"


def upgrade_unit_5(data: dict) -> dict:
    data.update({
        "schema_version": "2.0",
        "status": "review",
        "weeks": [10, 11, 12],
        "estimated_hours": 24,
        "slug": "electroquimica-interfaces-sensores",
        "title": "Electroquímica, interfaces y sensores",
        "purpose": "Relacionar transferencia electrónica, potencial químico y eléctrico, celdas, transporte iónico e interfaces con mediciones electroquímicas, corrosión, biosensores y bioelectricidad, separando equilibrio termodinámico, cinética interfacial y respuesta instrumental.",
    })
    data["learning_objectives"] = [
        "Balancear semirreacciones en medios ácido y básico conservando masa y carga.",
        "Distinguir oxidante, reductor, ánodo, cátodo y portadores de carga.",
        "Calcular potenciales de celda sin multiplicar potenciales intensivos.",
        "Relacionar potencial estándar, energía libre y constante de equilibrio.",
        "Aplicar la ecuación de Nernst con actividades y estequiometría correctas.",
        "Interpretar potenciales respecto a electrodos de referencia.",
        "Relacionar corriente, carga y transformación química mediante Faraday.",
        "Explicar doble capa, polarización, sobrepotencial y transporte de masa.",
        "Comparar potenciometría, amperometría, voltametría e impedancia.",
        "Evaluar calibración, interferencia, deriva y biofouling en sensores biomédicos.",
    ]
    for section in data.get("theory_sections", []):
        heading = section.get("heading", "")
        if heading.startswith("Reacciones redox"):
            section["equations"] = [
                {"label": "Conservación electrónica", "latex": "n_{e^-,oxidacion}=n_{e^-,reduccion}"},
                {"label": "Balance global", "latex": "\\sum_i \\nu_i A_i=0"},
            ]
        elif heading.startswith("Celdas"):
            section["equations"] = [
                {"label": "Potencial estándar", "latex": "E^\\circ_{celda}=E^\\circ_{catodo}-E^\\circ_{anodo}"},
                {"label": "Energía libre", "latex": "\\Delta G^\\circ=-nFE^\\circ"},
            ]
        elif heading.startswith("Nernst"):
            section["equations"] = [
                {"label": "Nernst", "latex": "E=E^\\circ-\\frac{RT}{nF}\\ln Q"},
                {"label": "Carga", "latex": "q=\\int I(t)\\,dt"},
            ]
    data["theory_sections"].extend([
        {
            "heading": "Interfaces, cinética y transporte de masa",
            "paragraphs": [
                "En la interfaz electrodo-solución se organiza una doble capa de carga que responde parcialmente como una capacitancia. Además pueden ocurrir transferencias electrónicas farádicas. Una señal de corriente puede incluir reacción del analito, carga interfacial, reacciones laterales y ruido; separar estas contribuciones es parte del diseño experimental.",
                "El sobrepotencial es la diferencia entre el potencial aplicado y el reversible necesario para sostener una corriente. La cinética de transferencia de carga puede describirse con Butler-Volmer y, en ciertos rangos, con aproximaciones de Tafel. El potencial de equilibrio por sí solo no determina la velocidad observada.",
                "Difusión, convección y migración controlan la llegada de especies al electrodo. Una corriente límite puede reflejar agotamiento cerca de la superficie y no saturación del reconocimiento. Agitación, viscosidad, geometría y tamaño del electrodo modifican la señal.",
                "La pasivación y el biofouling alteran área activa, capacitancia y transferencia electrónica. En matrices biológicas, proteínas y células pueden bloquear la superficie. La estabilidad debe estudiarse durante el tiempo de uso previsto y no solo en una solución patrón recién preparada.",
            ],
            "equations": [
                {"label": "Faraday", "latex": "n_{sustancia}=\\frac{q}{zF}"},
                {"label": "Butler-Volmer", "latex": "i=i_0[\\exp(\\alpha nF\\eta/RT)-\\exp(-(1-\\alpha)nF\\eta/RT)]"},
            ],
            "key_points": [
                "La corriente contiene componentes farádicos y capacitivos.",
                "El sobrepotencial refleja pérdidas cinéticas.",
                "El transporte puede controlar la respuesta.",
                "El biofouling cambia sensibilidad y estabilidad.",
            ],
        },
        {
            "heading": "Métodos electroanalíticos, biosensores y validación",
            "paragraphs": [
                "La potenciometría mide potencial con corriente mínima; la amperometría mide corriente a potencial controlado; la voltametría modifica el potencial para explorar procesos; la impedancia analiza magnitud y fase frente a frecuencia. Cada técnica responde a una propiedad distinta y requiere un modelo de medida coherente.",
                "Un biosensor integra reconocimiento, transducción y procesamiento. En un sensor enzimático, la señal puede depender de cinética, difusión, mediadores, oxígeno y transferencia electrónica. Una curva de calibración no basta sin blancos, interferentes, tiempo de respuesta, histéresis y deriva.",
                "Selectividad no significa ausencia absoluta de interferencia. Debe cuantificarse respuesta frente a especies coexistentes y cambios de matriz. La recuperación por adición y la comparación con un método de referencia ayudan a estimar sesgo, pero la validación debe usar muestras independientes.",
                "Para uso biomédico se evalúan precisión, exactitud, límite de detección, intervalo de medición, estabilidad, reproducibilidad entre lotes y seguridad. Si la salida alimenta una decisión, también importan calibración clínica, umbrales y consecuencias de falsos resultados.",
            ],
            "equations": [
                {"label": "Sensibilidad local", "latex": "S=\\frac{d\\,senal}{d\\,concentracion}"},
                {"label": "Impedancia", "latex": "Z(\\omega)=\\frac{V(\\omega)}{I(\\omega)}"},
            ],
            "key_points": [
                "Cada técnica mide una propiedad electroquímica distinta.",
                "La matriz real puede cambiar el desempeño.",
                "La validación debe separar calibración y evaluación.",
                "Una buena señal analítica no garantiza utilidad clínica.",
            ],
        },
    ])
    first_example = data.pop("worked_example")
    data["worked_examples"] = [first_example, {
        "title": "Carga necesaria para transformar un ion divalente",
        "scenario": "Se desea transformar 0,010 mol de M2+ con eficiencia farádica ideal.",
        "reasoning_steps": [
            "Escribir M2++2e-→M.",
            "Calcular 0,020 mol de electrones.",
            "Usar q=nF y obtener aproximadamente 1930 C.",
            "Para 0,50 A, calcular t=q/I≈3860 s.",
            "Comprobar unidades coulomb=ampere·segundo.",
            "Ajustar por eficiencia de corriente si existen reacciones laterales.",
        ],
        "interpretation": "La estequiometría electrónica conecta una corriente integrada con cantidad química, pero el rendimiento real depende de la interfaz y el transporte.",
        "limitations": ["Se supone eficiencia del 100 %.", "No se modela transporte.", "No se predice la morfología del producto."],
    }]
    first_activity = data.pop("guided_activity")
    data["guided_activities"] = [first_activity, {
        "title": "Plan de validación de un biosensor",
        "instructions": [
            "Define analito, matriz, intervalo y uso.",
            "Selecciona técnica y arquitectura de reconocimiento.",
            "Diseña calibración, blancos e interferentes.",
            "Evalúa precisión, sesgo, deriva y biofouling.",
            "Reserva muestras independientes para validación.",
        ],
        "problems": ["Compara buffer y plasma.", "Evalúa dos lotes.", "Analiza un cambio de pendiente.", "Define criterios de aceptación."],
        "checking_criteria": ["El mensurando está definido.", "Los controles separan matriz y señal.", "La validación no reutiliza toda la calibración.", "Las conclusiones respetan el uso estudiado."],
    }]
    data["practice_sets"] = [{
        "title": "Práctica graduada de electroquímica",
        "problems": [
            {"level": "básico", "question": "Identifica ánodo y cátodo.", "solution": "Ánodo es oxidación y cátodo reducción."},
            {"level": "básico", "question": "Balancea Fe2+→Fe3+.", "solution": "Fe2+→Fe3++e-."},
            {"level": "básico", "question": "Calcula E° con 0,80 y -0,20 V.", "solution": "1,00 V para la orientación favorable."},
            {"level": "intermedio", "question": "Calcula ΔG° para n=2 y E°=0,50 V.", "solution": "Aproximadamente -96,5 kJ/mol."},
            {"level": "intermedio", "question": "Explica por qué E no se duplica.", "solution": "E es intensivo; se duplica n y la energía."},
            {"level": "intermedio", "question": "Calcula moles de electrones para 9648,5 C.", "solution": "0,100 mol."},
            {"level": "avanzado", "question": "Predice un cambio nernstiano de diez veces.", "solution": "Cambia en (RT/nF)ln10 con signo según Q."},
            {"level": "avanzado", "question": "Distingue corriente farádica y capacitiva.", "solution": "La primera transforma especies; la segunda carga la interfaz."},
            {"level": "integrador", "question": "Audita una deriva en plasma.", "solution": "Evaluar referencia, unión, fouling, fuerza iónica e interferentes."},
            {"level": "integrador", "question": "Compara amperometría e impedancia.", "solution": "Definir perturbación, controles, métricas y validación independiente."},
        ],
    }]
    data["common_errors"].extend([
        {"error": "Confundir potencial y corriente.", "correction": "El potencial es fuerza impulsora; la corriente depende de cinética y transporte."},
        {"error": "Validar únicamente en buffer.", "correction": "Estudiar matriz, interferentes, recuperación y comparación externa."},
    ])
    data["self_assessment"].extend([
        {"question": "¿Qué produce corriente capacitiva?", "answer": "La carga y descarga de la doble capa."},
        {"question": "¿Qué es sobrepotencial?", "answer": "El exceso de potencial respecto al reversible para sostener corriente."},
        {"question": "¿Qué relaciona Faraday?", "answer": "Carga con moles de electrones y sustancia transformada."},
        {"question": "¿Por qué falla un sensor en matriz real?", "answer": "Por actividades, interferentes, fouling, referencia y transporte."},
    ])
    data["sources"].extend([
        {"title": "IUPAC Gold Book — Electrochemistry", "organization": "IUPAC", "url": "https://goldbook.iupac.org/", "type": "terminología oficial"},
        {"title": "Biosensors", "organization": "NIBIB", "url": "https://www.nibib.nih.gov/science-education/science-topics/biosensors", "type": "recurso institucional"},
    ])
    return data


def upgrade_unit_6(data: dict) -> dict:
    data.update({
        "schema_version": "2.0",
        "status": "review",
        "weeks": [13, 14, 15, 16],
        "estimated_hours": 30,
        "slug": "quimica-organica-biomolecular",
        "title": "Química orgánica y biomolecular",
        "purpose": "Integrar estructura, estereoquímica, grupos funcionales, mecanismos, acidez, reactividad y macromoléculas para explicar propiedades de biomoléculas, fármacos y materiales, y cerrar el curso mediante un análisis químico reproducible.",
    })
    data["learning_objectives"] = [
        "Representar conectividad, geometría, hibridación y conformación.",
        "Reconocer grupos funcionales y anticipar propiedades electrónicas.",
        "Distinguir isomería constitucional, conformacional y configuracional.",
        "Interpretar quiralidad y configuración con relevancia biomolecular.",
        "Usar pKa, resonancia, efectos inductivos y solvente para comparar acidez.",
        "Identificar nucleófilos, electrófilos y grupos salientes.",
        "Seguir mecanismos de sustitución, adición, eliminación y transferencia acilo.",
        "Relacionar estructura con solubilidad, partición, permeabilidad y estabilidad.",
        "Explicar arquitectura de carbohidratos, lípidos, proteínas y ácidos nucleicos.",
        "Integrar equilibrio, termodinámica, cinética y electroquímica en un caso biomolecular.",
    ]
    for section in data.get("theory_sections", []):
        heading = section.get("heading", "")
        if heading.startswith("Estructura"):
            section["equations"] = [{"label": "Carga formal", "latex": "CF=V-N-B/2"}]
        elif heading.startswith("Isomería"):
            section["paragraphs"].append("La composición estereoquímica debe medirse mediante cromatografía quiral, polarimetría u otras técnicas adecuadas. La configuración de un producto no se deduce solo del rendimiento ni del signo de rotación óptica.")
        elif heading.startswith("Biomoléculas"):
            section["paragraphs"].append("El autoensamblaje surge de interacciones reversibles y del solvente. Concentración crítica, cooperatividad, nucleación y estados metastables determinan estructuras observadas; describirlo solo como atracción entre piezas omite la termodinámica del medio.")
    data["theory_sections"].extend([
        {
            "heading": "Acidez, basicidad, especiación y propiedades",
            "paragraphs": [
                "La acidez aumenta cuando la base conjugada se estabiliza por electronegatividad, resonancia, efecto inductivo o solvatación. La basicidad depende de la disponibilidad del par electrónico. Una amida es menos básica que una amina porque el par del nitrógeno está deslocalizado hacia el carbonilo.",
                "El pKa permite estimar protonación. En moléculas polifuncionales, los sitios interactúan y aparecen microestados. Una carga neta no describe por completo la distribución local ni las conformaciones accesibles.",
                "La ionización modifica solubilidad, partición y permeación. La forma neutra suele atravesar mejor una fase hidrofóbica, pero transporte, unión, tamaño y gradientes también importan. La regla pH-partición es un modelo inicial, no una predicción farmacocinética completa.",
                "La forma sólida, el polimorfismo y la energía de red también afectan solubilidad. Aumentar ionización puede favorecer hidratación, pero una sal puede precipitar o cambiar de fase. La propiedad observada resulta de la molécula y de su estado material.",
            ],
            "equations": [
                {"label": "Henderson-Hasselbalch", "latex": "pH=pKa+\\log([A^-]/[HA])"},
                {"label": "Fracción desprotonada", "latex": "f_{A^-}=1/(1+10^{pKa-pH})"},
            ],
            "key_points": ["La estabilidad de la base conjugada gobierna acidez.", "Las moléculas polifuncionales tienen microestados.", "Ionización influye, pero no determina sola la permeación.", "La forma sólida modifica solubilidad."],
        },
        {
            "heading": "Mecanismos orgánicos y control de productos",
            "paragraphs": [
                "Los mecanismos siguen el movimiento de pares electrónicos mediante flechas curvas que parten de un par o enlace. Los nucleófilos donan densidad y los electrófilos la aceptan. La reactividad depende de estructura, concentración, solvente, temperatura y accesibilidad.",
                "SN2 ocurre en un paso con inversión y es sensible al impedimento estérico; SN1 pasa por un carbocatión y puede producir reordenamientos. Estas categorías son modelos extremos y algunos sistemas presentan comportamiento mixto.",
                "E2 requiere una geometría adecuada y compite con SN2; E1 comparte carbocatión con SN1. Temperatura, basicidad y volumen de la base modifican la selección. Las reglas de Záitsev y Hofmann son tendencias condicionadas.",
                "Los carbonilos son electrófilos. Aldehídos y cetonas sufren adición nucleofílica; derivados de ácidos carboxílicos suelen sufrir sustitución acílica. La reactividad depende de resonancia y calidad del grupo saliente.",
                "Un mecanismo propuesto debe conservar carga, masa y electrones y explicar cinética y selectividad. Los productos observados restringen posibilidades, pero pueden ser compatibles con más de una ruta.",
            ],
            "key_points": ["Las flechas comienzan en electrones.", "SN1/SN2 y E1/E2 son modelos mecanísticos.", "Los carbonilos presentan reactividad modulada.", "El mecanismo es una hipótesis contrastable."],
        },
        {
            "heading": "Propiedad molecular, materiales e integración",
            "paragraphs": [
                "La relación estructura-propiedad conecta tamaño, carga, polaridad, flexibilidad y aromaticidad con solubilidad, partición, unión y estabilidad. Estas relaciones son multivariadas y presentan compromisos; mejorar una propiedad puede empeorar otra.",
                "La estabilidad incluye hidrólisis, oxidación, fotólisis, racemización y agregación. La velocidad depende de pH, temperatura, oxígeno, luz y matriz. Un ensayo acelerado debe demostrar que conserva el mecanismo de degradación.",
                "Los biomateriales orgánicos se diseñan mediante monómeros, enlaces cruzados, cristalinidad y grupos superficiales. La composición no determina sola biocompatibilidad: degradación, extractables, topografía, mecánica y respuesta biológica forman un sistema.",
                "El proyecto integrador debe combinar especiación, energía libre, cinética y medición. Una molécula puede ser estable pero degradarse por una ruta catalizada; un sensor puede reconocerla y fallar por fouling; un fármaco puede unirse y no alcanzar el compartimento.",
                "La química biomolecular produce mapas de posibilidades, no decisiones clínicas automáticas. La evidencia debe progresar desde estructura y ensayo hacia validación, seguridad y utilidad.",
            ],
            "key_points": ["Las propiedades presentan compromisos.", "La estabilidad depende de mecanismo y condiciones.", "Biocompatibilidad integra química, física y biología.", "La aplicación exige una cadena de validación."],
        },
    ])
    first_example = data.pop("worked_example")
    data["worked_examples"] = [first_example, {
        "title": "Competencia entre sustitución y eliminación",
        "scenario": "Un haluro secundario reacciona con una base fuerte a temperatura elevada.",
        "reasoning_steps": [
            "Identificar un sustrato secundario con competencia.",
            "La base fuerte favorece abstracción de protón y E2.",
            "La temperatura aumenta la contribución de eliminación.",
            "Revisar geometría antiperiplanar.",
            "Considerar SN2 como ruta competidora.",
            "Predecir mezcla dependiente de estructura y solvente.",
        ],
        "interpretation": "El modelo anticipa predominio de eliminación, pero la selectividad necesita datos de productos y cinética.",
        "limitations": ["No se especifica la base.", "No se cuantifican velocidades.", "No se incluyen efectos de fase."],
    }]
    first_activity = data.pop("guided_activity")
    data["guided_activities"] = [first_activity, {
        "title": "Proyecto integrador de Química II",
        "instructions": [
            "Selecciona una molécula, material o sensor biomédico.",
            "Integra equilibrio, termodinámica, cinética y estructura.",
            "Diseña una estrategia experimental y computacional.",
            "Define controles, incertidumbre y criterios de validación.",
            "Comunica resultados y límites en un informe reproducible.",
        ],
        "problems": ["Construye un diagrama de especies.", "Analiza una ruta de degradación.", "Propón una medición.", "Evalúa transportabilidad a matriz real."],
        "checking_criteria": ["Los dominios están conectados.", "Las ecuaciones tienen unidades y supuestos.", "El plan incluye controles.", "La utilidad no se afirma sin validación."],
    }]
    data["practice_sets"] = [{
        "title": "Práctica graduada de química orgánica y biomolecular",
        "problems": [
            {"level": "básico", "question": "Asigna hibridación a un carbonilo.", "solution": "El carbono es aproximadamente sp2."},
            {"level": "básico", "question": "Distingue conformación y configuración.", "solution": "La primera cambia por rotación; la segunda requiere ruptura."},
            {"level": "básico", "question": "Identifica nucleófilo y electrófilo.", "solution": "El nucleófilo dona al centro electrófilo."},
            {"level": "intermedio", "question": "Compara amina y amida.", "solution": "La amida es menos básica por resonancia."},
            {"level": "intermedio", "question": "Estima fracción ionizada a pH=pKa+1.", "solution": "Aproximadamente 91 % para la forma desprotonada de un ácido."},
            {"level": "intermedio", "question": "Clasifica dos estructuras R/S.", "solution": "Comparar todos los centros para decidir relación."},
            {"level": "avanzado", "question": "Predice SN2 frente a E2.", "solution": "Evaluar sustrato, base, solvente, temperatura y geometría."},
            {"level": "avanzado", "question": "Compara amida y éster.", "solution": "La amida está más estabilizada por resonancia."},
            {"level": "integrador", "question": "Audita permeabilidad basada solo en logP.", "solution": "Incluir pKa, sólido, tamaño, transportadores y unión."},
            {"level": "integrador", "question": "Diseña estabilidad de un compuesto quiral.", "solution": "Controlar pH, temperatura, luz, oxígeno y composición enantiomérica."},
        ],
    }]
    data["common_errors"].extend([
        {"error": "Confundir resonancia con equilibrio entre estructuras.", "correction": "Las formas son representaciones del mismo estado electrónico."},
        {"error": "Inferir función biológica desde estructura aislada.", "correction": "Validar unión, exposición, transporte, seguridad y contexto."},
    ])
    data["self_assessment"].extend([
        {"question": "¿Qué diferencia resonancia y conformación?", "answer": "Resonancia redistribuye electrones; conformación mueve núcleos por rotación."},
        {"question": "¿Qué describe R/S?", "answer": "Configuración absoluta según prioridades."},
        {"question": "¿Qué caracteriza SN2?", "answer": "Un paso concertado, dependencia bimolecular e inversión."},
        {"question": "¿Por qué estructura no basta para utilidad clínica?", "answer": "Faltan exposición, mecanismo, validación, seguridad y contexto."},
    ])
    data["sources"].extend([
        {"title": "IUPAC Gold Book", "organization": "IUPAC", "url": "https://goldbook.iupac.org/", "type": "terminología oficial"},
        {"title": "ChEBI", "organization": "EMBL-EBI", "url": "https://www.ebi.ac.uk/chebi/", "type": "ontología química"},
    ])
    return data


def main() -> int:
    for unit, upgrader in ((5, upgrade_unit_5), (6, upgrade_unit_6)):
        path = UNIT_DIR / f"unit-{unit:02d}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data = upgrader(data)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        json.loads(path.read_text(encoding="utf-8"))
        print(f"Completada: {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
