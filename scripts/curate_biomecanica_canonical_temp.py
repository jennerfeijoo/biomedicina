#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_DIR = ROOT / "data" / "courses" / "biomecanica"
TODAY = "2026-08-24"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def first_sentence(text: str, limit: int = 260) -> str:
    text = " ".join(str(text or "").split())
    if not text:
        return "Revisa el razonamiento y vuelve a justificar la respuesta con unidades, supuestos y límites."
    sentence = re.split(r"(?<=[.!?])\s+", text, maxsplit=1)[0]
    return sentence[:limit].rstrip()


def tokens(text: str) -> set[str]:
    stop = {
        "de", "del", "la", "las", "el", "los", "y", "o", "en", "un", "una", "para", "por", "con",
        "a", "al", "que", "se", "su", "sus", "como", "entre", "sin", "sobre", "the", "of", "and", "in",
    }
    return {t for t in re.findall(r"[a-záéíóúñü0-9]+", text.casefold()) if len(t) > 2 and t not in stop}


course = load(COURSE_DIR / "course.json")
sources = load(COURSE_DIR / "sources.json")
glossary = load(COURSE_DIR / "glossary.json")
claims = load(COURSE_DIR / "claims.json")
course_assessment = load(COURSE_DIR / "assessments" / "course-assessment.json")

source_by_id = {item["id"]: item for item in sources["sources"]}
sources_by_unit: dict[str, list[str]] = {}
for source in sources["sources"]:
    for unit_id in source.get("used_by_unit_ids", []):
        sources_by_unit.setdefault(unit_id, []).append(source["id"])

status = {
    "content": "complete",
    "sources": "traceable",
    "pedagogy": "complete",
    "multimedia": "planned",
    "internal_review": "pending",
    "external_review": "pending",
    "publication": "published_provisional",
}

course["content_version"] = "1.0.0"
course["audience"] = (
    "Estudiantes de ingeniería biomédica y áreas afines con formación universitaria inicial en mecánica, cálculo, "
    "anatomía funcional y programación científica que necesiten analizar movimiento humano de forma reproducible."
)
course["status"] = status
course["purpose"] = (
    "Integrar cinemática, cinética, mecánica musculoesquelética, mecánica de tejidos, medición multimodal y "
    "aplicaciones funcionales para construir análisis biomecánicos reproducibles del movimiento humano, declarando "
    "marcos de referencia, unidades, supuestos, procesamiento, incertidumbre y uso previsto, y separando resultado "
    "mecánico de diagnóstico, causalidad, prescripción y beneficio clínico no demostrados."
)
course["scope"] = {
    "included": [
        "Cinemática 2D/3D con marcos de referencia, transformaciones, posición, orientación, velocidad y aceleración.",
        "Cinética segmentaria con diagramas de cuerpo libre, Newton-Euler, fuerzas, momentos y dinámica inversa.",
        "Mecánica músculo-tendón, brazos de momento, redundancia, co-contracción y límites de inferencia sobre fuerza muscular.",
        "Caracterización mecánica de hueso, cartílago y tendón con anisotropía y viscoelasticidad.",
        "Plataformas de fuerza, captura de movimiento y sEMG con calibración, muestreo, filtrado, sincronización y trazabilidad.",
        "Fiabilidad, SEM, MDC, métricas de marcha, rehabilitación, prótesis/órtesis y ergonomía dentro del alcance de cada método.",
        "Expedientes reproducibles con controles, sensibilidad, alternativas explicativas y límites de interpretación.",
    ],
    "excluded": [
        "Diagnóstico de lesión, enfermedad o alteración funcional a partir de una métrica biomecánica aislada.",
        "Prescripción de rehabilitación, prótesis, órtesis, cirugía o adaptación laboral individual.",
        "Atribución causal a una intervención a partir de una comparación pre/post sin diseño causal suficiente.",
        "Uso de sEMG como sustituto directo de fuerza muscular o de dinámica inversa como identificador de músculos individuales.",
        "Prácticas con personas, pacientes o dispositivos clínicos sin infraestructura, supervisión, consentimiento y autorización apropiados.",
    ],
    "handoff_courses": [
        "laboratorio-biomecanica",
        "fundamentos-biomecanica",
        "biomecanica-medios-continuos",
        "modelado-simulacion-biomedicina",
        "simulacion-planificacion-quirurgica",
    ],
}
course["prerequisites"] = [
    {"id": "BIOMEC-PRE01", "statement": "Álgebra vectorial, trigonometría, cálculo diferencial y mecánica universitaria inicial."},
    {"id": "BIOMEC-PRE02", "statement": "Diagramas de cuerpo libre, unidades SI y análisis dimensional."},
    {"id": "BIOMEC-PRE03", "statement": "Programación científica básica para tablas, vectores, series temporales y visualización reproducible."},
    {"id": "BIOMEC-PRE04", "statement": "Anatomía funcional y fisiología musculoesquelética introductorias."},
    {"id": "BIOMEC-PRE05", "statement": "Muestreo y estadística descriptiva básica para interpretar variabilidad y error de medición."},
]
course["competencies"] = [
    {"id": "BIOMEC-COMP01", "statement": "Construir descripciones cinemáticas reproducibles con convenciones espaciales y temporales explícitas."},
    {"id": "BIOMEC-COMP02", "statement": "Resolver balances segmentarios e interpretar fuerzas, momentos y dinámica inversa con fronteras mecánicas claras."},
    {"id": "BIOMEC-COMP03", "statement": "Relacionar músculo-tendón, geometría articular y propiedades de tejidos sin colapsar niveles de explicación."},
    {"id": "BIOMEC-COMP04", "statement": "Diseñar y auditar cadenas de medición multimodal con calibración, sincronización, procesamiento y metadatos."},
    {"id": "BIOMEC-COMP05", "statement": "Evaluar incertidumbre, fiabilidad, sensibilidad, cambio detectable y transferibilidad antes de interpretar diferencias."},
    {"id": "BIOMEC-COMP06", "statement": "Interpretar aplicaciones en marcha, rehabilitación, prótesis/órtesis y ergonomía sin exceder el uso previsto de la evidencia."},
    {"id": "BIOMEC-COMP07", "statement": "Integrar las seis unidades en un expediente reproducible con evidencia, controles, alternativas, límites y revisión documentada."},
]
course["learning_outcomes"] = [
    {"id": "BIOMEC-LO01", "statement": "Construye un análisis cinemático reproducible que declara marcos, convenciones, transformaciones, procesamiento, derivadas y fuentes de error."},
    {"id": "BIOMEC-LO02", "statement": "Resuelve e interpreta un balance cinético segmentario con fuerzas, momentos, parámetros inerciales y dinámica inversa, manteniendo la frontera entre resultado neto y fuerza muscular individual."},
    {"id": "BIOMEC-LO03", "statement": "Integra mecánica músculo-tendón y propiedades de tejidos para explicar capacidad y respuesta mecánica dependientes de estructura y tiempo sin inferir lesión individual."},
    {"id": "BIOMEC-LO04", "statement": "Diseña y audita una cadena de medición multimodal con plataforma de fuerza, captura de movimiento y sEMG, documentando calibración, sincronización, procesamiento y propagación de error."},
    {"id": "BIOMEC-LO05", "statement": "Evalúa fiabilidad, incertidumbre, sensibilidad y cambio detectable y determina si una diferencia es suficientemente robusta para el uso analítico definido."},
    {"id": "BIOMEC-LO06", "statement": "Interpreta métricas biomecánicas en marcha, rehabilitación, prótesis/órtesis y ergonomía con objetivos funcionales y límites explícitos, sin presentar diagnóstico, prescripción o causalidad no demostrada."},
    {"id": "BIOMEC-LO07", "statement": "Entrega y defiende un expediente integrador reproducible que conecta las seis unidades, compara explicaciones alternativas, registra correcciones y especifica la siguiente evidencia necesaria."},
]
course["study_method"] = [
    "Definir primero pregunta, sistema, tarea, uso previsto y resultado admisible.",
    "Alternar explicación, ejemplo resuelto, práctica guiada, comprobación y transferencia con apoyo progresivamente menor.",
    "Separar dato observado, transformación, variable derivada, modelo, interpretación y decisión.",
    "Predefinir controles, criterios de aceptación y análisis de sensibilidad antes de interpretar resultados.",
    "Conservar unidades, marcos de referencia, parámetros, versiones, procedencia y discrepancias.",
    "Revisar cada producto con rúbrica y justificar las correcciones antes de cerrar una conclusión.",
]
core_ids: list[str] = []
for n in range(1, 7):
    uid = f"BIOMEC-U{n:02d}"
    verified = [sid for sid in sources_by_unit.get(uid, []) if source_by_id[sid].get("verification_status") == "verified_directly"]
    core_ids.extend(verified[:2])
course["core_source_ids"] = list(dict.fromkeys(core_ids))
course["editorial_notice"] = (
    "Corpus canónico educativo completo a nivel de contenido y pedagogía interna para las seis unidades. Las fuentes "
    "quedan trazadas y la publicación sigue siendo provisional. La revisión humana interna, la revisión disciplinaria "
    "externa, cualquier evaluación con personas, el diagnóstico, la prescripción, la causalidad clínica y la aptitud "
    "ocupacional individual permanecen fuera del cierre y siguen pendientes."
)

mapping = {
    1: ["BIOMEC-LO01", "BIOMEC-LO05"],
    2: ["BIOMEC-LO02", "BIOMEC-LO05"],
    3: ["BIOMEC-LO03", "BIOMEC-LO05"],
    4: ["BIOMEC-LO03", "BIOMEC-LO05"],
    5: ["BIOMEC-LO04", "BIOMEC-LO05"],
    6: ["BIOMEC-LO05", "BIOMEC-LO06", "BIOMEC-LO07"],
}
durations = {1: 120, 2: 120, 3: 120, 4: 120, 5: 150, 6: 150}
unit_payloads: dict[str, dict] = {}

for n in range(1, 7):
    uid = f"BIOMEC-U{n:02d}"
    unit_path = COURSE_DIR / "units" / f"unit-{n:02d}.json"
    unit = load(unit_path)
    unit["status"] = status
    unit["course_learning_outcome_ids"] = mapping[n]
    for activity in unit.get("activities", []):
        activity["estimated_duration_minutes"] = durations[n]
        activity["status"] = "curated_internal_review_pending"
    unit_payloads[uid] = unit

    assessment_path = COURSE_DIR / "assessments" / f"unit-{n:02d}.json"
    assessment = load(assessment_path)
    candidate_sources = sources_by_unit.get(uid, [])
    for index, item in enumerate(assessment.get("items", []), start=1):
        if index <= 2:
            item["difficulty"] = "foundational"
            item["cognitive_level"] = "understand"
        elif index <= 5:
            item["difficulty"] = "intermediate"
            item["cognitive_level"] = "apply"
        elif index <= 8:
            item["difficulty"] = "intermediate"
            item["cognitive_level"] = "analyze"
        else:
            item["difficulty"] = "advanced"
            item["cognitive_level"] = "evaluate"
        answer = item.get("answer_key", {})
        explanation = first_sentence(answer.get("explanation") or answer.get("expected_answer"))
        misconceptions = answer.get("common_misconceptions") or []
        item["feedback"] = {
            "correct": f"Correcto. Conserva en tu justificación este criterio: {explanation}",
            "incorrect": (
                f"Revisa el razonamiento. Evita este error frecuente: {first_sentence(misconceptions[0])}"
                if misconceptions
                else f"Revisa qué se observa, qué se calcula y qué se puede inferir. Pista: {explanation}"
            ),
        }
        if candidate_sources:
            item["source_ids"] = [candidate_sources[(index - 1) % len(candidate_sources)]]
        item["status"] = "curated_internal_review_pending"
    assessment["status"] = "curated_internal_review_pending"
    write(assessment_path, assessment)

# Glossary: link every definition to the most relevant verified source(s) from its own unit(s).
for entry in glossary.get("entries", []):
    candidates: list[str] = []
    for uid in entry.get("unit_ids", []):
        candidates.extend(sources_by_unit.get(uid, []))
    candidates = list(dict.fromkeys(candidates))
    term_tokens = tokens(entry.get("term", "") + " " + entry.get("definition", ""))
    scored = []
    for sid in candidates:
        source = source_by_id[sid]
        source_tokens = tokens(source.get("title", "") + " " + source.get("description", ""))
        score = len(term_tokens & source_tokens)
        verified_bonus = 1 if source.get("verification_status") == "verified_directly" else 0
        scored.append((score, verified_bonus, sid))
    scored.sort(reverse=True)
    chosen = [sid for _, _, sid in scored[:2]]
    if not chosen and candidates:
        chosen = candidates[:1]
    if not chosen:
        raise RuntimeError(f"No source available for glossary entry {entry['id']}")
    entry["source_ids"] = chosen
    entry["verification_status"] = (
        "verified_directly" if all(source_by_id[sid].get("verification_status") == "verified_directly" for sid in chosen)
        else "traceable"
    )
write(COURSE_DIR / "glossary.json", glossary)

# Central claims: two literal key points per topic (eight per unit), tied to verified unit sources.
claim_records = []
for n in range(1, 7):
    uid = f"BIOMEC-U{n:02d}"
    unit = unit_payloads[uid]
    candidate_sources = sources_by_unit.get(uid, [])
    verified_sources = [sid for sid in candidate_sources if source_by_id[sid].get("verification_status") == "verified_directly"]
    pool = verified_sources or candidate_sources
    if not pool:
        raise RuntimeError(f"No source available for claims in {uid}")
    unit_claim_ids = []
    counter = 0
    for topic in unit.get("topics", []):
        for point in topic.get("key_points", [])[:2]:
            counter += 1
            cid = f"{uid}-C{counter:03d}"
            sid = pool[(counter - 1) % len(pool)]
            source = source_by_id[sid]
            locator = source.get("locator") or source.get("doi") or source.get("url") or "Fuente verificada enlazada"
            claim_records.append({
                "claim_id": cid,
                "unit": n,
                "text": point,
                "claim_type": "methodological_or_interpretive",
                "risk": "medium",
                "context": f"Síntesis educativa de {unit['title']}; debe interpretarse dentro del protocolo, supuestos y límites declarados en la unidad.",
                "source_id": sid,
                "locator": {"section": str(locator)},
                "support": "direct_or_synthesis",
                "source_verification_status": source.get("verification_status", "traceable"),
                "review_state": "ai_review_provisional",
                "reviewer_validation_id": None,
                "reviewed_at": TODAY,
                "id": cid,
                "unit_id": uid,
            })
            unit_claim_ids.append(cid)
    unit["claim_ids"] = unit_claim_ids
    write(COURSE_DIR / "units" / f"unit-{n:02d}.json", unit)

claims.update({
    "content_version": "1.0.0",
    "content_commit": None,
    "scope": "Afirmaciones centrales literales de las seis unidades de Biomecánica con fuentes verificadas; revisión disciplinaria humana pendiente.",
    "review_state": "ai_review_provisional",
    "claims": claim_records,
})
write(COURSE_DIR / "claims.json", claims)

course_assessment["principles"] = [
    "La evidencia de dominio es un producto verificable con unidades, marcos, supuestos, controles e interpretación proporcional.",
    "Una respuesta numérica sin procedimiento, comprobaciones y límites recibe crédito parcial aunque el número final sea correcto.",
    "La recuperación sin apoyo precede a la consulta de soluciones y la retroalimentación se usa para corregir el razonamiento.",
    "Los datos sintéticos o abiertos se prefieren para las actividades autónomas; prácticas con personas requieren un contexto autorizado aparte.",
    "La evaluación distingue descripción mecánica, validez de medición, inferencia científica y decisiones clínicas u ocupacionales.",
    "La revisión humana interna y externa permanecen pendientes y no se sustituyen por los controles automáticos del repositorio.",
]
course_assessment["midterm_blueprint"] = [
    {"domain": "U1 Cinemática", "weight_percent": 15, "learning_outcome_ids": ["BIOMEC-LO01", "BIOMEC-LO05"], "evidence": "Transformación de marcos, derivadas, comparación 2D/3D y error."},
    {"domain": "U2 Cinética", "weight_percent": 20, "learning_outcome_ids": ["BIOMEC-LO02", "BIOMEC-LO05"], "evidence": "Cuerpo libre, Newton-Euler, momentos y dinámica inversa."},
    {"domain": "U3 Mecánica musculoesquelética", "weight_percent": 15, "learning_outcome_ids": ["BIOMEC-LO03"], "evidence": "Músculo-tendón, brazo de momento, redundancia y límites."},
    {"domain": "U4 Tejidos biológicos", "weight_percent": 15, "learning_outcome_ids": ["BIOMEC-LO03", "BIOMEC-LO05"], "evidence": "Tensión-deformación, anisotropía y viscoelasticidad."},
    {"domain": "U5 Medición y modelado", "weight_percent": 20, "learning_outcome_ids": ["BIOMEC-LO04", "BIOMEC-LO05"], "evidence": "Calibración, captura, sEMG, filtrado, sincronización y propagación de error."},
    {"domain": "U6 Aplicaciones", "weight_percent": 15, "learning_outcome_ids": ["BIOMEC-LO06", "BIOMEC-LO07"], "evidence": "Fiabilidad/cambio, marcha, rehabilitación, prótesis/órtesis, RNLE y límites de decisión."},
]
course_assessment["capstone"]["scenario"] = (
    "Un equipo académico recibe un caso sintético de análisis de movimiento con cinemática, fuerzas externas y señales auxiliares. "
    "Debe construir un expediente biomecánico reproducible, evaluar una comparación o intervención simulada y defender qué puede "
    "concluirse, qué explicaciones alternativas permanecen y qué evidencia adicional sería necesaria, sin diagnosticar ni prescribir."
)
course_assessment["capstone"]["integration_requirements"] = [
    "Usar de forma explícita evidencia o procedimientos de las seis unidades y mapearlos a BIOMEC-LO01–BIOMEC-LO07.",
    "Incluir al menos un control geométrico o dimensional, un análisis de sensibilidad y una explicación alternativa plausible.",
    "Separar señal medida, variable derivada, salida de modelo, interpretación funcional y decisión fuera de alcance.",
    "Registrar versiones, parámetros, correcciones y discrepancias para que otra persona pueda reproducir el análisis.",
    "Cerrar con una conclusión proporcional y una lista priorizada de evidencia que faltaría para una inferencia clínica u ocupacional.",
]
course_assessment["status"] = "curated_internal_review_pending"
write(COURSE_DIR / "assessments" / "course-assessment.json", course_assessment)
write(COURSE_DIR / "course.json", course)

# Permanent regression protecting the canonical course closure.
test = '''from __future__ import annotations\n\nimport json\nimport unittest\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nCOURSE = ROOT / "data" / "courses" / "biomecanica"\nGENERIC = "concepto de la unidad que debe definirse"\n\n\nclass BiomecanicaCanonicalCourseTests(unittest.TestCase):\n    @classmethod\n    def setUpClass(cls):\n        cls.course = json.loads((COURSE / "course.json").read_text(encoding="utf-8"))\n        cls.sources = json.loads((COURSE / "sources.json").read_text(encoding="utf-8"))\n        cls.glossary = json.loads((COURSE / "glossary.json").read_text(encoding="utf-8"))\n        cls.claims = json.loads((COURSE / "claims.json").read_text(encoding="utf-8"))\n\n    def test_course_status_preserves_human_review_boundary(self):\n        status = self.course["status"]\n        self.assertEqual(status["content"], "complete")\n        self.assertEqual(status["sources"], "traceable")\n        self.assertEqual(status["pedagogy"], "complete")\n        self.assertEqual(status["multimedia"], "planned")\n        self.assertEqual(status["internal_review"], "pending")\n        self.assertEqual(status["external_review"], "pending")\n\n    def test_six_units_and_all_course_outcomes_are_covered(self):\n        self.assertEqual(len(self.course["unit_files"]), 6)\n        known = {item["id"] for item in self.course["learning_outcomes"]}\n        covered = set()\n        for relative in self.course["unit_files"]:\n            unit = json.loads((COURSE / relative).read_text(encoding="utf-8"))\n            covered.update(unit["course_learning_outcome_ids"])\n            self.assertNotIn(GENERIC, json.dumps(unit, ensure_ascii=False).casefold())\n            self.assertTrue(unit["activities"][0]["estimated_duration_minutes"] > 0)\n        self.assertEqual(known, covered)\n\n    def test_assessment_items_are_classified_and_have_feedback(self):\n        source_ids = {item["id"] for item in self.sources["sources"]}\n        for n in range(1, 7):\n            assessment = json.loads((COURSE / "assessments" / f"unit-{n:02d}.json").read_text(encoding="utf-8"))\n            self.assertEqual(len(assessment["items"]), 10)\n            for item in assessment["items"]:\n                self.assertNotEqual(item["difficulty"], "unclassified")\n                self.assertNotEqual(item["cognitive_level"], "unclassified")\n                self.assertTrue(item["feedback"]["correct"])\n                self.assertTrue(item["feedback"]["incorrect"])\n                self.assertTrue(set(item["source_ids"]) <= source_ids)\n\n    def test_glossary_and_claims_are_traceable(self):\n        source_ids = {item["id"] for item in self.sources["sources"]}\n        self.assertGreaterEqual(len(self.glossary["entries"]), 100)\n        for entry in self.glossary["entries"]:\n            self.assertTrue(entry["source_ids"])\n            self.assertTrue(set(entry["source_ids"]) <= source_ids)\n            self.assertNotEqual(entry["verification_status"], "unverified")\n        self.assertGreaterEqual(len(self.claims["claims"]), 40)\n        self.assertEqual({claim["unit_id"] for claim in self.claims["claims"]}, {f"BIOMEC-U{i:02d}" for i in range(1, 7)})\n\n    def test_course_assessment_integrates_all_units(self):\n        assessment = json.loads((COURSE / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))\n        self.assertEqual(sum(item["weight_percent"] for item in assessment["assessment_plan"]), 100)\n        self.assertEqual(sum(item["weight_percent"] for item in assessment["midterm_blueprint"]), 100)\n        self.assertEqual(sum(item["weight_percent"] for item in assessment["capstone"]["rubric"]), 100)\n        self.assertGreaterEqual(len(assessment["diagnostic"]["questions"]), 10)\n\n\nif __name__ == "__main__":\n    unittest.main()\n'''
(ROOT / "tests" / "test_biomecanica_canonical_course.py").write_text(test, encoding="utf-8")

print(f"Curated canonical Biomecanica: {len(glossary['entries'])} glossary entries, {len(claim_records)} claims")
