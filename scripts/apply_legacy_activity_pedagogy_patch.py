#!/usr/bin/env python3
from pathlib import Path

path = Path("assets/js/generated-units.js")
text = path.read_text(encoding="utf-8")
old = '''  function renderActivity(parent, activity, index, total) {
    if (!activity || typeof activity !== "object") return;
    const section = element("section", "generated-unit-panel generated-unit-activity");
    const prefix = total > 1 ? `Actividad guiada ${index + 1}` : "Actividad guiada";
    appendHeading(section, 4, `${prefix}: ${activity.title || "Práctica"}`);
    if (activity.purpose) section.appendChild(element("p", "generated-unit-scenario", activity.purpose));
    if (activity.instructions?.length) {
      section.appendChild(element("strong", "", "Instrucciones"));
      appendList(section, activity.instructions);
    }
    renderEquations(section, activity.equations);
    if (activity.problems?.length) {
      section.appendChild(element("strong", "", "Problemas o tareas"));
      appendList(section, activity.problems);
    }
    if (activity.starter_code) {
      const pre = element("pre", "generated-unit-code");
      pre.appendChild(element("code", "", activity.starter_code));
      section.appendChild(pre);
    }
    if (activity.checking_criteria?.length) {
      section.appendChild(element("strong", "", "Criterios de comprobación"));
      appendList(section, activity.checking_criteria);
    }
    parent.appendChild(section);
  }
'''
new = '''  function renderActivity(parent, activity, index, total) {
    if (!activity || typeof activity !== "object") return;
    const section = element("section", "generated-unit-panel generated-unit-activity");
    const prefix = total > 1 ? `Actividad guiada ${index + 1}` : "Actividad guiada";
    appendHeading(section, 4, `${prefix}: ${activity.title || "Práctica"}`);

    const tasks = activity.tasks || activity.problems || activity.exercises || [];
    const deliverables = activity.deliverables || [];
    const brief = element("div", "activity-learning-brief");
    brief.appendChild(element("strong", "", "Qué vas a conseguir"));
    brief.appendChild(element(
      "p",
      "",
      activity.purpose || "Aplicar los conceptos de esta unidad en una tarea concreta y comprobar que puedes justificar el procedimiento y el resultado."
    ));
    const meta = element("div", "activity-meta-row");
    if (activity.estimated_duration_minutes) {
      meta.appendChild(element("span", "activity-meta-chip", `${activity.estimated_duration_minutes} min aprox.`));
    }
    if (tasks.length) meta.appendChild(element("span", "activity-meta-chip", `${tasks.length} tareas`));
    if (deliverables.length) meta.appendChild(element("span", "activity-meta-chip", `${deliverables.length} entregables`));
    if (meta.childElementCount) brief.appendChild(meta);
    const help = element("button", "pedagogy-help-button", "¿Cómo trabajo esta actividad?");
    help.type = "button";
    help.addEventListener("click", () => showActivityGuide(section, activity));
    brief.appendChild(help);
    section.appendChild(brief);

    if (activity.instructions?.length) {
      section.appendChild(element("strong", "", "Ruta de trabajo paso a paso"));
      const ordered = element("ol", "pedagogy-step-list");
      for (const step of activity.instructions) {
        const stepText = listItemText(step);
        if (stepText) ordered.appendChild(element("li", "", stepText));
      }
      section.appendChild(ordered);
    }

    renderEquations(section, activity.equations);

    if (tasks.length) {
      section.appendChild(element("strong", "", "Tareas: demuestra que comprendiste"));
      const taskList = appendList(section, tasks, "pedagogy-task-list");
      addTaskGuidance(taskList);
    }

    if (activity.starter_code) {
      const codeLabel = element("strong", "", "Punto de partida de código");
      section.appendChild(codeLabel);
      const pre = element("pre", "generated-unit-code");
      pre.appendChild(element("code", "", activity.starter_code));
      section.appendChild(pre);
    }

    if (deliverables.length) {
      section.appendChild(element("strong", "", "Qué debes entregar"));
      appendList(section, deliverables, "activity-deliverables");
    }

    if (activity.checking_criteria?.length) {
      section.appendChild(element("strong", "", "Auto-comprobación antes de terminar"));
      appendList(section, activity.checking_criteria, "activity-self-check");
    }
    parent.appendChild(section);
  }
'''
if old not in text:
    raise SystemExit("No se encontró el renderActivity esperado")
text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")
print("renderActivity heredado actualizado con andamiaje pedagógico")
