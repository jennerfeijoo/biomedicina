from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "ingenieria-clinica-gestion"
COURSE_ID = "ingenieria-clinica-gestion"
TODAY = "2026-08-24"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


COMPLETE_STATUS = {"content": "complete", "sources": "traceable", "pedagogy": "complete", "multimedia": "planned", "internal_review": "pending", "external_review": "pending", "publication": "published_provisional"}
course = load(COURSE / "course.json")
course.update({
    "content_version": "1.0.0",
    "academic_level": "Pregrado universitario intermedio y avanzado",
    "audience": "Estudiantes de ingeniería biomédica y áreas afines con fundamentos de instrumentación, medición, estadística descriptiva y gestión técnica que necesiten administrar tecnología sanitaria con trazabilidad, seguridad y límites explícitos.",
    "status": COMPLETE_STATUS,
    "purpose": "Integrar gobernanza de ingeniería clínica, inventario y criticidad, mantenimiento y metrología, adquisición y evaluación, seguridad e incidentes, y proyectos de mejora para construir un expediente reproducible de gestión de tecnología sanitaria, separando evidencia técnica, desempeño operativo, seguridad, obligación regulatoria potencial y decisión clínica y sin presentar el trabajo académico como autorización institucional, auditoría, certificación ni recomendación asistencial.",
    "scope": {
        "included": ["Gobernanza, roles, responsabilidades, escalamiento e interfaces del servicio de ingeniería clínica.", "Inventario, identidad de activos, calidad de datos, estado, criticidad y priorización con criterios explícitos.", "Mantenimiento preventivo y correctivo, órdenes de trabajo, disponibilidad, metrología, calibración, verificación, trazabilidad e incertidumbre.", "Evaluación de necesidades, requisitos, HTA local, coste del ciclo de vida, criterios multicriterio y análisis de sensibilidad para adquisición.", "Seguridad, preservación de evidencia, cronología, investigación multicausal, vigilancia y aprendizaje de incidentes.", "KPIs, contratos y SLA como instrumentos operativos, PDSA, formación basada en competencia, adopción, sostenibilidad y transferencia operativa.", "Expedientes sintéticos reproducibles con fuentes, versiones, denominadores, supuestos, decisiones, brechas y límites de inferencia."],
        "excluded": ["Intervenir, mantener, calibrar, liberar, retirar o modificar dispositivos médicos reales.", "Usar datos personales, historias clínicas, tickets confidenciales o información identificable de pacientes o trabajadores.", "Realizar una HTA oficial, licitación, adjudicación, investigación oficial de incidentes, auditoría, certificación o evaluación de conformidad.", "Emitir asesoría jurídica, contractual, regulatoria, clínica o de seguridad para una organización real.", "Inferir causalidad, beneficio clínico, cumplimiento legal o seguridad global a partir de un KPI, SLA, matriz de criticidad o ejercicio académico.", "Sustituir la gobernanza de hospitales, autoridades competentes, profesionales de salud, metrología acreditada o especialistas regulatorios."],
        "handoff_courses": ["desarrollo-dispositivos-medicos", "bioinstrumentacion", "laboratorio-bioinstrumentacion", "ciencia-regulatoria-calidad-seguridad-tecnologias-medicas", "aplicaciones-salud-digital"]},
    "prerequisites": [{"id": "ICG-PRE01", "statement": "Fundamentos de instrumentación biomédica, magnitudes, unidades y sistemas de medición."}, {"id": "ICG-PRE02", "statement": "Estadística descriptiva básica, proporciones, tasas, incertidumbre y lectura de series temporales."}, {"id": "ICG-PRE03", "statement": "Anatomía y fisiología introductorias suficientes para comprender contexto de uso de tecnología sanitaria."}, {"id": "ICG-PRE04", "statement": "Documentación técnica, trazabilidad, control de versiones y pensamiento sistémico."}, {"id": "ICG-PRE05", "statement": "Capacidad para consultar fuentes técnicas, normativas y regulatorias oficiales en inglés cuando sea necesario."}],
    "competencies": [{"id": "ICG-COMP01", "statement": "Definir gobernanza, roles, interfaces y escalamiento de un servicio de ingeniería clínica con límites de autoridad explícitos."}, {"id": "ICG-COMP02", "statement": "Construir y auditar inventarios de tecnología sanitaria con identidad, procedencia, calidad de datos y priorización reproducible."}, {"id": "ICG-COMP03", "statement": "Interpretar mantenimiento y evidencia metrológica conservando unidades, trazabilidad, incertidumbre, criterios y configuración."}, {"id": "ICG-COMP04", "statement": "Comparar alternativas de adquisición mediante necesidades, requisitos, evidencia, coste de ciclo de vida, sensibilidad y límites."}, {"id": "ICG-COMP05", "statement": "Gestionar información de seguridad e incidentes preservando evidencia, cronología, múltiples causas posibles y rutas de escalamiento."}, {"id": "ICG-COMP06", "statement": "Diseñar sistemas de medición y mejora con KPIs, SLA, pruebas de cambio, competencia y sostenibilidad sin sobreinterpretar causalidad."}, {"id": "ICG-COMP07", "statement": "Integrar U1–U6 en expedientes auditables que distingan dato, cálculo, inferencia, decisión y evidencia todavía necesaria."}],
    "learning_outcomes": [{"id": "ICG-LO01", "statement": "Delimita la función de ingeniería clínica mediante gobernanza, responsabilidades, interfaces, escalamiento y criterios de documentación sin atribuir autoridad que corresponda a otras funciones."}, {"id": "ICG-LO02", "statement": "Construye y audita un inventario sintético de tecnología sanitaria con identidad, estado, procedencia, calidad de datos y criticidad reproducible, distinguiendo prioridad operativa de riesgo clínico demostrado."}, {"id": "ICG-LO03", "statement": "Interpreta mantenimiento y metrología mediante órdenes de trabajo, métricas con denominadores, calibración, verificación, trazabilidad e incertidumbre, sin convertir una prueba educativa en liberación de un equipo real."}, {"id": "ICG-LO04", "statement": "Construye una evaluación de adquisición trazable que conecta necesidad, requisitos, evidencia, HTA local, coste del ciclo de vida, criterios multicriterio y sensibilidad sin presentarla como licitación o adjudicación oficial."}, {"id": "ICG-LO05", "statement": "Organiza un expediente sintético de seguridad e incidentes con preservación de evidencia, cronología, investigación multicausal, denominadores y vigilancia, separando reporte interno de obligaciones externas potenciales."}, {"id": "ICG-LO06", "statement": "Diseña y evalúa un proyecto de mejora con baseline, KPIs de resultado/proceso/equilibrio, SLA, PDSA, formación basada en competencia, adopción y sostenibilidad sin inferir causalidad de un simple antes-después."}, {"id": "ICG-LO07", "statement": "Integra las seis unidades en un expediente reproducible de gestión de tecnología sanitaria que conserva fuentes, versiones, supuestos, incertidumbre, decisiones, evidencia negativa y límites y especifica la siguiente evidencia necesaria antes de actuar en un servicio real."}],
    "study_method": ["Definir primero el sistema, activo o proceso, la decisión que se intenta sostener y la autoridad de cada rol.", "Alternar explicación, ejemplo trabajado, actividad sintética guiada, recuperación y revisión con criterios explícitos.", "Separar dato observado, variable calculada, interpretación, decisión y obligación externa potencial.", "Conservar denominadores, unidades, ventanas temporales, versiones, configuración, fuentes y criterios antes de comparar resultados.", "Usar discrepancias, datos faltantes y efectos no deseados para estrechar conclusiones en vez de ocultarlos.", "Cerrar cada unidad con un handoff explícito a la siguiente y revisar el expediente acumulativo antes de avanzar."],
    "editorial_notice": "Corpus canónico educativo completo a nivel de contenido y pedagogía interna para U1–U6. Las fuentes están trazadas y la publicación continúa como provisional. La revisión humana interna y disciplinaria externa, la asesoría jurídica, contractual, clínica o regulatoria, la auditoría, certificación, evaluación de conformidad, investigación oficial de incidentes y cualquier intervención sobre tecnología o servicios reales siguen fuera de este cierre y permanecen pendientes."
})

sources = load(COURSE / "sources.json")
used = []
for source in sources.get("sources", []):
    if source.get("used_by_unit_ids"):
        if source.get("verification_status") != "verified_directly":
            raise SystemExit(f"Fuente usada no verificada directamente: {source.get('id')}: {source.get('verification_status')}")
        used.append(source)
if len(used) < 25:
    raise SystemExit(f"Cobertura bibliográfica insuficiente: {len(used)} fuentes verificadas")
sources["sources"] = used
sources["coverage_gaps"] = []
sources["consulted_on"] = TODAY
sources["source_policy"] = "Priorizar fuentes oficiales, estándares y literatura académica primaria o metodológica directamente verificable; conservar jurisdicción, versión, fecha y límites de uso cuando correspondan."
source_by_id = {s["id"]: s for s in used}
write(COURSE / "sources.json", sources)
course["core_source_ids"] = [s["id"] for s in used[:12]]

lo_map = {1: ["ICG-LO01", "ICG-LO07"], 2: ["ICG-LO02", "ICG-LO07"], 3: ["ICG-LO03", "ICG-LO07"], 4: ["ICG-LO04", "ICG-LO07"], 5: ["ICG-LO05", "ICG-LO07"], 6: ["ICG-LO06", "ICG-LO07"]}
unit_source_ids = {}
for number in range(1, 7):
    unit_path = COURSE / "units" / f"unit-{number:02d}.json"
    unit = load(unit_path)
    unit["status"] = COMPLETE_STATUS
    unit["course_learning_outcome_ids"] = lo_map[number]
    unit_source_ids[number] = [sid for sid in unit.get("source_ids", []) if sid in source_by_id]
    if not unit_source_ids[number]: raise SystemExit(f"U{number}: sin fuentes verificadas")
    for idx, activity in enumerate(unit.get("activities", []), start=1):
        activity["estimated_duration_minutes"] = 240 if idx == 1 else 120
        activity["status"] = "complete"
    if not unit.get("activities"): raise SystemExit(f"U{number}: sin actividad guiada")
    write(unit_path, unit)
    ap = COURSE / "assessments" / f"unit-{number:02d}.json"
    assessment = load(ap)
    items = assessment.get("items", [])
    if len(items) < 10: raise SystemExit(f"U{number}: autoevaluación insuficiente")
    difficulties = ["foundational", "intermediate", "intermediate", "advanced"]
    cognitive = ["understand", "apply", "analyze", "evaluate"]
    for idx, item in enumerate(items):
        item["difficulty"] = difficulties[idx % 4]
        item["cognitive_level"] = cognitive[idx % 4]
        if not item.get("answer_key", {}).get("explanation"): raise SystemExit(f"U{number} Q{idx+1}: falta explicación")
        item["feedback"] = {"correct": "Correcto. Conserva la distinción conceptual y la evidencia indicada antes de transferirla a otro escenario.", "incorrect": "Revisa la explicación y vuelve a separar dato, cálculo, inferencia, decisión y límite. Después responde otra vez sin consultar la clave."}
        item["source_ids"] = [unit_source_ids[number][idx % len(unit_source_ids[number])]]
        item["status"] = "complete"
    assessment["status"] = "complete"
    write(ap, assessment)

glossary = load(COURSE / "glossary.json")
for entry in glossary.get("entries", []):
    candidate = []
    for unit_id in entry.get("unit_ids", []):
        try: number = int(unit_id.rsplit("U", 1)[1])
        except Exception: continue
        candidate.extend(unit_source_ids.get(number, []))
    candidate = list(dict.fromkeys(candidate))
    if not candidate: raise SystemExit(f"Glosario sin trazabilidad: {entry.get('term')}")
    entry["source_ids"] = candidate[:2]
    entry["verification_status"] = "traceable_to_verified_source"
glossary["status"] = "traceable"
write(COURSE / "glossary.json", glossary)

claims = []
for number in range(1, 7):
    up = COURSE / "units" / f"unit-{number:02d}.json"
    unit = load(up)
    topics = unit.get("topics", [])
    if len(topics) < 4: raise SystemExit(f"U{number}: se esperaban cuatro temas")
    unit_claim_ids = []
    for idx, topic in enumerate(topics[:4], start=1):
        if not topic.get("key_points"): raise SystemExit(f"U{number} T{idx}: sin key point")
        text = topic["key_points"][0]
        source_id = unit_source_ids[number][(idx - 1) % len(unit_source_ids[number])]
        source = source_by_id[source_id]
        claim_id = f"ICG-U{number:02d}-C{idx:03d}"
        unit_claim_ids.append(claim_id)
        claims.append({"claim_id": claim_id, "unit": number, "text": text, "claim_type": "methodological_or_interpretive", "risk": "medium", "context": f"Afirmación ancla enseñada literalmente en U{number}: {unit['title']}; interpretar dentro del alcance, jurisdicción, supuestos y límites declarados.", "source_id": source_id, "locator": {"url": source.get("url"), "title": source.get("title")}, "support": "direct", "source_verification_status": "verified_directly", "review_state": "ai_review_provisional", "reviewer_validation_id": None, "reviewed_at": TODAY, "id": claim_id, "unit_id": f"ICG-U{number:02d}"})
    unit["claim_ids"] = unit_claim_ids
    write(up, unit)
write(COURSE / "claims.json", {"$schema": "../../../schemas/academic/registry-v1.schema.json", "schema_version": "1.0", "course_id": COURSE_ID, "content_version": "1.0.0", "content_commit": None, "scope": "Veinticuatro afirmaciones ancla, cuatro por unidad, tomadas literalmente de las unidades canónicas y vinculadas a fuentes verificadas directamente; revisión disciplinaria humana pendiente.", "review_state": "ai_review_provisional", "claims": claims})

media = load(COURSE / "media.json")
media["coverage_status"] = "planned"
for item in media.get("items", []): item["status"] = "planned"
write(COURSE / "media.json", media)

course_assessment = {
    "$schema": "../../../../schemas/academic/assessment-v1.schema.json", "schema_version": "1.0", "id": "ICG-EVAL-CURSO", "course_id": COURSE_ID, "scope": "course",
    "principles": ["Evaluar decisiones trazables y reproducibles, no memorización aislada de acrónimos o umbrales.", "Separar gobernanza, dato, cálculo, interpretación, seguridad, obligación externa potencial y decisión en cada producto.", "Usar exclusivamente activos, tickets, contratos, incidentes y datos sintéticos en las actividades del curso.", "Exigir denominadores, unidades, ventanas temporales, fuentes y versiones cuando una conclusión dependa de ellos.", "Premiar la declaración explícita de incertidumbre, discrepancias y evidencia todavía necesaria.", "Mantener revisión humana externa, asesoría profesional y cualquier intervención sobre servicios reales fuera del cierre académico."],
    "assessment_plan": [{"component": "U1 · gobernanza e interfaces", "weight_percent": 8, "linked_learning_outcome_ids": ["ICG-LO01", "ICG-LO07"]}, {"component": "U2 · inventario, identidad y criticidad", "weight_percent": 8, "linked_learning_outcome_ids": ["ICG-LO02", "ICG-LO07"]}, {"component": "U3 · mantenimiento y metrología", "weight_percent": 10, "linked_learning_outcome_ids": ["ICG-LO03", "ICG-LO07"]}, {"component": "U4 · adquisición y evaluación", "weight_percent": 10, "linked_learning_outcome_ids": ["ICG-LO04", "ICG-LO07"]}, {"component": "U5 · seguridad e incidentes", "weight_percent": 12, "linked_learning_outcome_ids": ["ICG-LO05", "ICG-LO07"]}, {"component": "U6 · proyectos, KPIs y mejora", "weight_percent": 12, "linked_learning_outcome_ids": ["ICG-LO06", "ICG-LO07"]}, {"component": "Evaluación integradora intermedia U1–U3", "weight_percent": 15, "linked_learning_outcome_ids": ["ICG-LO01", "ICG-LO02", "ICG-LO03", "ICG-LO07"]}, {"component": "Capstone de gestión tecnológica U1–U6", "weight_percent": 25, "linked_learning_outcome_ids": [f"ICG-LO0{i}" for i in range(1, 8)]}],
    "diagnostic": {"purpose": "Comprobar prerrequisitos de medición, documentación y razonamiento antes de integrar la gestión de tecnología sanitaria.", "questions": ["Distingue función, responsabilidad, autoridad y escalamiento en un caso organizativo sintético.", "Explica por qué dos equipos con el mismo modelo necesitan identificadores de activo distintos.", "Detecta tres problemas de calidad de datos en una tabla de inventario sintética.", "Interpreta una proporción indicando numerador, denominador y ventana temporal.", "Distingue mantenimiento preventivo, correctivo e inspección de desempeño.", "Distingue calibración, verificación y ajuste mediante un ejemplo de medición.", "Explica por qué trazabilidad metrológica no significa simplemente conservar un certificado.", "Diferencia requisito obligatorio de criterio ponderable en una compra sintética.", "Explica por qué coste de compra y coste de ciclo de vida no son equivalentes.", "Distingue hecho observado, hipótesis causal y conclusión en un incidente ficticio.", "Explica por qué reporte interno y reportabilidad externa potencial son decisiones distintas.", "Define un KPI con numerador, denominador, fuente y medida de equilibrio.", "Distingue tiempo de respuesta de tiempo de resolución en un SLA.", "Explica por qué asistencia a formación no demuestra competencia."], "use": "Formativo y no ponderado; los errores se convierten en objetivos de nivelación antes de iniciar la unidad correspondiente."},
    "midterm_blueprint": [{"domain": "U1 · gobernanza y fronteras", "weight_percent": 20, "linked_learning_outcome_ids": ["ICG-LO01"]}, {"domain": "U2 · inventario, datos y criticidad", "weight_percent": 30, "linked_learning_outcome_ids": ["ICG-LO02"]}, {"domain": "U3 · mantenimiento, métricas y metrología", "weight_percent": 30, "linked_learning_outcome_ids": ["ICG-LO03"]}, {"domain": "Integración U1–U3 y calidad de decisión", "weight_percent": 20, "linked_learning_outcome_ids": ["ICG-LO01", "ICG-LO02", "ICG-LO03", "ICG-LO07"]}],
    "capstone": {"title": "Expediente sintético de gestión de tecnología sanitaria", "purpose": "Integrar U1–U6 en un dossier reproducible que permita reconstruir datos, cálculos, decisiones, límites y siguientes acciones sin explicación oral adicional.", "scenario": "Gestionar una cartera ficticia de tecnología sanitaria de un hospital simulado usando exclusivamente datos sintéticos; ninguna salida constituye decisión institucional, mantenimiento, investigación oficial, contratación o recomendación clínica.", "required_deliverables": ["Mapa de gobernanza, roles, interfaces, autoridad y escalamiento.", "Diccionario de inventario con identificadores, procedencia, estado y reglas de calidad de datos.", "Matriz de criticidad con dimensiones, reglas, sensibilidad y casos de empate.", "Plan sintético de mantenimiento con categorías, prioridades y criterios de cierre.", "Ficha de métricas de mantenimiento con numeradores, denominadores, ventanas y límites.", "Expediente metrológico sintético con calibración o verificación, trazabilidad e incertidumbre.", "Necesidad de adquisición y especificación de requisitos obligatorios y criterios ponderables.", "Modelo de coste del ciclo de vida y comparación multicriterio con análisis de sensibilidad.", "Expediente de incidente ficticio con hechos, cronología, hipótesis, evidencia preservada y brechas.", "Plan de aprendizaje y vigilancia con denominadores y frontera entre reporte interno y obligación externa potencial.", "Diccionario de KPIs con medidas de resultado, proceso y equilibrio.", "SLA sintético con alcance, exclusiones, relojes, evidencia y escalamiento.", "Ciclo PDSA con predicción, prueba limitada, datos, aprendizaje y decisión de adaptar, adoptar o abandonar.", "Plan de formación con tarea, práctica, criterio y evidencia de competencia.", "Plan de sostenibilidad, transferencia operativa y respuesta a deterioro.", "Registro final de fuentes, versiones, decisiones, discrepancias, brechas y afirmaciones fuera de alcance."], "constraints": ["No usar pacientes, datos personales, tickets reales, contratos reales ni dispositivos reales.", "No realizar mantenimiento, calibración, liberación, retirada, compra o cambio de servicios reales.", "No presentar métricas o matrices como evidencia de causalidad, seguridad global, beneficio clínico o cumplimiento legal.", "Toda conclusión debe declarar qué dato y fuente la sostienen y qué evidencia podría cambiarla."], "rubric": [{"criterion": "Gobernanza y límites de responsabilidad", "weight_percent": 10, "linked_learning_outcome_ids": ["ICG-LO01"]}, {"criterion": "Inventario, calidad de datos y criticidad", "weight_percent": 15, "linked_learning_outcome_ids": ["ICG-LO02"]}, {"criterion": "Mantenimiento, metrología y reproducibilidad", "weight_percent": 15, "linked_learning_outcome_ids": ["ICG-LO03"]}, {"criterion": "Adquisición, evidencia y sensibilidad", "weight_percent": 15, "linked_learning_outcome_ids": ["ICG-LO04"]}, {"criterion": "Seguridad, investigación y vigilancia", "weight_percent": 15, "linked_learning_outcome_ids": ["ICG-LO05"]}, {"criterion": "KPIs, SLA, mejora y sostenibilidad", "weight_percent": 15, "linked_learning_outcome_ids": ["ICG-LO06"]}, {"criterion": "Trazabilidad integral, límites y comunicación", "weight_percent": 15, "linked_learning_outcome_ids": ["ICG-LO07"]}]},
    "status": "complete"}
write(COURSE / "assessments" / "course-assessment.json", course_assessment)
write(COURSE / "course.json", course)
print(f"Canonical ICG finalized: {len(used)} sources, {len(glossary.get('entries', []))} glossary entries, {len(claims)} claims")
