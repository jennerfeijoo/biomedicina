#!/usr/bin/env python3
"""Strengthen the disciplinary alignment of computational drug discovery.

This migration replaces generic data-science practice with domain-specific,
auditable self-study tasks and adds primary or official drug-discovery sources.
It deliberately preserves ``review``: technical improvement is not external
disciplinary certification.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT_ROOTS = (
    ROOT / "data/course_redevelopment/descubrimiento-computacional-farmacos/units",
    ROOT / "data/generated_units/descubrimiento-computacional-farmacos",
)


SOURCES = {
    "chembl": {
        "title": "ChEMBL: a drug discovery platform spanning multiple bioactivity data types and time periods",
        "organization": "EMBL-EBI",
        "url": "https://doi.org/10.1093/nar/gkad1004",
        "role": "Fundamenta procedencia, estructura y uso de datos químicos y bioactivos.",
        "type": "artículo de recurso",
        "verification_status": "verified_directly",
    },
    "pubchem": {
        "title": "PubChem PUG REST Tutorial",
        "organization": "National Center for Biotechnology Information",
        "url": "https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest-tutorial",
        "role": "Documenta recuperación reproducible de identidad, propiedades y anotaciones químicas.",
        "type": "documentación oficial",
        "verification_status": "verified_directly",
    },
    "rdkit": {
        "title": "RDKit Book",
        "organization": "RDKit Project",
        "url": "https://www.rdkit.org/docs/RDKit_Book.html",
        "role": "Documenta representaciones, descriptores, fingerprints y operaciones quimioinformáticas.",
        "type": "documentación oficial",
        "verification_status": "verified_directly",
    },
    "pdb": {
        "title": "RCSB PDB Web APIs Overview",
        "organization": "RCSB Protein Data Bank",
        "url": "https://www.rcsb.org/docs/programmatic-access/web-apis-overview",
        "role": "Documenta acceso, metadatos, ensamblajes y evidencia estructural del PDB.",
        "type": "documentación oficial",
        "verification_status": "verified_directly",
    },
    "vina": {
        "title": "AutoDock Vina documentation: basic docking",
        "organization": "Forli Lab, Scripps Research",
        "url": "https://autodock-vina.readthedocs.io/en/latest/docking_basic.html",
        "role": "Sustenta preparación, búsqueda conformacional, puntuación y controles de docking.",
        "type": "documentación oficial",
        "verification_status": "verified_directly",
    },
    "qsar": {
        "title": "OECD principles for the validation of (Q)SAR models",
        "organization": "Organisation for Economic Co-operation and Development",
        "url": "https://www.oecd.org/chemicalsafety/risk-assessment/validationofqsarmodels.htm",
        "role": "Define endpoint, algoritmo, aplicabilidad, desempeño y, cuando sea posible, interpretación.",
        "type": "principios de validación",
        "verification_status": "verified_directly",
    },
    "teachopen": {
        "title": "TeachOpenCADD: a teaching platform for computer-aided drug design",
        "organization": "Volkamer Lab",
        "url": "https://doi.org/10.1186/s13321-022-00637-2",
        "role": "Proporciona flujos reproducibles y actividades de diseño de fármacos asistido por computadora.",
        "type": "artículo metodológico",
        "verification_status": "verified_directly",
    },
    "hpc": {
        "title": "High Performance Computing for Drug Discovery and Biomedicine",
        "organization": "Methods in Molecular Biology",
        "url": "https://doi.org/10.1007/978-1-0716-3449-3",
        "role": "Integra reproducibilidad, escalamiento y métodos computacionales de descubrimiento de fármacos.",
        "type": "libro de métodos",
        "verification_status": "verified_from_supplied_source",
    },
}


ACTIVITIES = {
    1: {
        "title": "De la necesidad terapéutica al perfil de producto objetivo",
        "instructions": [
            "Selecciona una necesidad terapéutica ficticia y define población, intervención actual, limitación y resultado clínicamente significativo.",
            "Formula una hipótesis de diana sin confundir asociación con causalidad y construye una cadena evidencia-mecanismo-intervención.",
            "Define un perfil mínimo de producto objetivo con criterios medibles de eficacia, exposición, selectividad y seguridad.",
            "Preespecifica tres criterios de abandono y señala qué experimento resolvería la incertidumbre dominante.",
        ],
        "problems": [
            "Distingue necesidad médica, diana, mecanismo, modalidad y candidato.",
            "Reescribe dos afirmaciones causales que solo están respaldadas por asociación.",
            "Ordena evidencia genética, bioquímica, celular, animal y clínica por la inferencia concreta que permite.",
            "Construye un diagrama de decisión con al menos dos rutas alternativas.",
            "Identifica un posible conflicto entre potencia y seguridad.",
            "Propón un control negativo y uno positivo para la hipótesis de mecanismo.",
            "Explica qué resultado obligaría a revisar la diana y cuál solo obligaría a revisar el ensayo.",
            "Redacta un memorando de continuidad de 250 palabras con incertidumbres explícitas.",
        ],
        "checking_criteria": [
            "Cada afirmación está vinculada a un tipo de evidencia.",
            "Los criterios de continuidad y abandono son observables y previos al resultado.",
            "La incertidumbre de mecanismo se separa de la incertidumbre de medición.",
            "La recomendación no excede el nivel de evidencia disponible.",
        ],
    },
    2: {
        "title": "Curación reproducible de una tabla de bioactividad",
        "instructions": [
            "Diseña un esquema para diez registros sintéticos con identificador de compuesto, estructura, diana, organismo, tipo de ensayo, relación, valor, unidad y procedencia.",
            "Normaliza unidades sin mezclar IC50, Ki, Kd y porcentaje de inhibición.",
            "Define reglas explícitas para sales, mezclas, estereoquímica, duplicados y mediciones censuradas.",
            "Conserva una tabla de decisiones que permita reconstruir cada exclusión o transformación.",
        ],
        "problems": [
            "Detecta cuándo dos filas representan el mismo compuesto y cuándo no puede decidirse.",
            "Separa identidad química, registro de sustancia y resultado experimental.",
            "Convierte valores molares a una escala coherente conservando desigualdades.",
            "Explica por qué no deben agregarse endpoints heterogéneos por promedio directo.",
            "Propón una regla para réplicas concordantes y otra para resultados conflictivos.",
            "Identifica leakage derivado de duplicados o análogos próximos.",
            "Construye un diccionario de datos con restricciones de tipo y dominio.",
            "Entrega un informe de procedencia, pérdidas y población final analizable.",
        ],
        "checking_criteria": [
            "La unidad de observación y el endpoint son inequívocos.",
            "Las transformaciones son reversibles o quedan auditadas.",
            "No se fusionan mediciones biológicamente no comparables.",
            "Los conflictos se conservan como información, no se borran silenciosamente.",
        ],
    },
    3: {
        "title": "Auditoría de representaciones y similitud molecular",
        "instructions": [
            "Construye un conjunto sintético de moléculas descritas por tres rasgos binarios y dos continuos.",
            "Compara similitud de Tanimoto para rasgos binarios con distancia estandarizada para descriptores continuos.",
            "Prueba una transformación irrelevante de representación y una modificación que sí altere identidad o propiedades.",
            "Define un dominio de aplicabilidad basado en vecinos y no solo en mínimos y máximos.",
        ],
        "problems": [
            "Calcula manualmente dos similitudes de Tanimoto.",
            "Demuestra cómo la escala domina una distancia euclídea sin estandarización.",
            "Compara dos representaciones manteniendo fija la partición y el modelo.",
            "Identifica una colisión de fingerprint conceptual.",
            "Explica por qué una proyección 2D no conserva todas las distancias.",
            "Diseña un control para estereoquímica y otro para tautomería.",
            "Marca tres consultas como interpolación, extrapolación o indeterminadas.",
            "Redacta la ficha de versión y parámetros de la representación elegida.",
        ],
        "checking_criteria": [
            "La métrica corresponde al tipo de representación.",
            "Las comparaciones controlan partición y preprocesamiento.",
            "La similitud no se interpreta como mecanismo o actividad.",
            "El dominio de aplicabilidad tiene una regla reproducible.",
        ],
    },
    4: {
        "title": "Crítica de un experimento de docking",
        "instructions": [
            "Selecciona una estructura pública y documenta método experimental, resolución, ensamblaje, ligandos, residuos ausentes y estado de protonación incierto.",
            "Define preparación de receptor y ligando, centro y tamaño de caja, semillas y exhaustividad.",
            "Incluye redocking de un ligando conocido, inspección de pose y un señuelo como controles.",
            "Compara la afirmación permitida por la pose con las afirmaciones que requerirían evidencia bioquímica o celular.",
        ],
        "problems": [
            "Distingue unidad asimétrica y ensamblaje biológico.",
            "Identifica cuatro decisiones de preparación que pueden cambiar el resultado.",
            "Explica por qué el score no es una afinidad experimental.",
            "Define un criterio geométrico para validar redocking.",
            "Analiza el efecto potencial de agua estructural y cofactor.",
            "Compara búsqueda de pose y ranking de ligandos como tareas diferentes.",
            "Propón una prueba de sensibilidad a la caja y a la semilla.",
            "Redacta una conclusión limitada con controles fallidos y exitosos.",
        ],
        "checking_criteria": [
            "La estructura y su contexto experimental están identificados.",
            "Los parámetros permiten repetir la ejecución.",
            "Existen controles de pose y de ranking.",
            "El score no se presenta como evidencia suficiente de unión o eficacia.",
        ],
    },
    5: {
        "title": "Validación temporal y por familias químicas",
        "instructions": [
            "Crea un conjunto sintético con fecha, familia química, endpoint y predicción.",
            "Compara partición aleatoria, temporal y por agrupaciones estructurales.",
            "Calcula discriminación o error, calibración y cobertura del dominio de aplicabilidad.",
            "Documenta qué escenario representa mejor el uso prospectivo y por qué.",
        ],
        "problems": [
            "Detecta leakage por réplicas, sales y análogos cercanos.",
            "Define un baseline acorde al endpoint.",
            "Separa validación interna, externa y prospectiva.",
            "Calcula un intervalo por remuestreo sobre un ejemplo pequeño.",
            "Compara error global y error fuera del dominio.",
            "Evalúa estabilidad ante tres semillas.",
            "Propón una prueba de permutación del endpoint.",
            "Completa una tarjeta de modelo con uso previsto y exclusiones.",
        ],
        "checking_criteria": [
            "La partición refleja la pregunta de generalización.",
            "El preprocesamiento se ajusta solo con entrenamiento.",
            "Se informa incertidumbre y no solo una métrica puntual.",
            "La aplicabilidad acompaña cada predicción o recomendación.",
        ],
    },
    6: {
        "title": "Decisión multiobjetivo con incertidumbre",
        "instructions": [
            "Construye una matriz sintética de cinco candidatos con potencia, selectividad, solubilidad, exposición e incertidumbre.",
            "Normaliza direcciones y escalas sin ocultar qué variables son proxies.",
            "Identifica soluciones dominadas y construye un frente de Pareto.",
            "Realiza sensibilidad a pesos y redacta una recomendación condicional.",
        ],
        "problems": [
            "Distingue endpoint medido, proxy y predicción.",
            "Propaga un intervalo simple en una razón beneficio-riesgo.",
            "Identifica dos compensaciones que un promedio oculta.",
            "Compara ranking ponderado y regla de veto.",
            "Evalúa qué candidato cambia de posición al variar pesos.",
            "Define un umbral de abandono independiente del ranking.",
            "Selecciona la siguiente medición por valor esperado de información cualitativo.",
            "Redacta una tabla decisión-evidencia-incertidumbre-acción.",
        ],
        "checking_criteria": [
            "Las preferencias están separadas de los datos.",
            "Las escalas y direcciones se justifican.",
            "La sensibilidad muestra si el ranking es robusto.",
            "La recomendación explicita qué nueva evidencia podría cambiarla.",
        ],
    },
    7: {
        "title": "Auditoría cerrada de propuestas generativas",
        "instructions": [
            "Trabaja solo con diez candidatos sintéticos ya proporcionados; no generes instrucciones de síntesis ni nuevas sustancias.",
            "Define validez, unicidad, diversidad, proximidad al dominio y filtros de alerta antes de observar rankings.",
            "Compara el objetivo optimizado con dos propiedades no incluidas para buscar reward hacking.",
            "Diseña un ciclo de aprendizaje activo conceptual con presupuesto, regla de selección y criterio de parada.",
        ],
        "problems": [
            "Distingue novedad de utilidad.",
            "Detecta duplicados y variantes triviales.",
            "Compara diversidad interna y distancia al entrenamiento.",
            "Identifica una función objetivo susceptible de explotación.",
            "Diseña un control negativo para el oráculo.",
            "Compara incertidumbre, diversidad y explotación como reglas de selección.",
            "Define trazabilidad de modelo, semilla, filtros y exclusiones.",
            "Concluye qué propuestas merecen evaluación adicional sin afirmar descubrimiento.",
        ],
        "checking_criteria": [
            "La actividad permanece educativa, sintética y no operativa.",
            "Los criterios se fijan antes de revisar resultados.",
            "Se auditan propiedades fuera de la función objetivo.",
            "La salida se comunica como propuesta sujeta a validación.",
        ],
    },
    8: {
        "title": "Paquete de validación conceptual y reporte",
        "instructions": [
            "Elige una predicción ficticia y conviértela en hipótesis refutable con unidad experimental y resultado primario.",
            "Diseña controles positivo, negativo, de vehículo y ortogonal cuando sean pertinentes.",
            "Preespecifica exclusiones, réplicas, análisis y criterio de decisión sin describir procedimientos experimentales peligrosos.",
            "Integra resultados sintéticos concordantes y discordantes en una actualización de evidencia.",
        ],
        "problems": [
            "Distingue réplica técnica, biológica e independiente.",
            "Define qué sesgo controla cada comparador.",
            "Explica cómo una lectura ortogonal reduce ambigüedad.",
            "Analiza un resultado computacional positivo y experimental nulo.",
            "Analiza un resultado aparente que falla al repetir.",
            "Separa ausencia de evidencia y evidencia de ausencia.",
            "Completa un checklist de datos, código, versiones y desviaciones.",
            "Redacta una conclusión final proporcional al conjunto completo de evidencia.",
        ],
        "checking_criteria": [
            "La hipótesis y el resultado primario son refutables.",
            "Cada control responde a una amenaza identificada.",
            "Las discrepancias se investigan y no se seleccionan resultados favorables.",
            "El reporte permite auditar decisiones y límites de inferencia.",
        ],
    },
}


UNIT_SOURCES = {
    1: ("chembl", "teachopen", "hpc"),
    2: ("chembl", "pubchem", "teachopen"),
    3: ("rdkit", "pubchem", "teachopen"),
    4: ("pdb", "vina", "teachopen"),
    5: ("chembl", "qsar", "teachopen"),
    6: ("chembl", "qsar", "hpc"),
    7: ("chembl", "rdkit", "hpc"),
    8: ("pdb", "chembl", "teachopen"),
}


def main() -> int:
    canonical_root, generated_root = UNIT_ROOTS
    for path in sorted(canonical_root.glob("unit-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        unit = int(data["unit"])
        data["guided_activities"] = [ACTIVITIES[unit]]
        data.pop("guided_activity", None)

        existing = data.get("sources", [])
        generic_titles = {
            "FAIR Guiding Principles for scientific data management and stewardship",
            "Datasheets for Datasets",
            "Model Cards for Model Reporting",
            "Artificial Intelligence Risk Management Framework 1.0",
            "A framework for understanding unintended consequences of machine learning",
            "Specification gaming: the flip side of AI ingenuity",
        }
        retained = [source for source in existing if source.get("title") not in generic_titles]
        additions = [SOURCES[key] for key in UNIT_SOURCES[unit]]
        merged = []
        seen = set()
        for source in [*additions, *retained]:
            key = source.get("url") or source.get("doi") or source.get("title")
            if key in seen:
                continue
            seen.add(key)
            merged.append(source)
        for source in SOURCES.values():
            key = source.get("url") or source.get("title")
            if len(merged) >= 5:
                break
            if key not in seen:
                seen.add(key)
                merged.append(source)
        data["sources"] = merged
        serialized = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        path.write_text(serialized, encoding="utf-8")
        (generated_root / path.name).write_text(serialized, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
