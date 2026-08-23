#!/usr/bin/env python3
from pathlib import Path

JS_PATH = Path("assets/js/generated-units.js")
CSS_PATH = Path("assets/css/generated-units.css")

js = JS_PATH.read_text(encoding="utf-8")
css = CSS_PATH.read_text(encoding="utf-8")

if "pedagogy-guided-activities:v1" in js:
    raise SystemExit("El parche pedagógico ya está aplicado.")

anchor = '''  async function fetchUnit(rootUrl, subjectId, unitNumber) {
'''
helpers = r'''  // pedagogy-guided-activities:v1
  function normalizedTaskVerb(task) {
    return String(task || "")
      .trim()
      .toLocaleLowerCase("es")
      .split(/\s+/)[0]
      .replace(/[^a-záéíóúüñ]/g, "");
  }

  function taskScaffold(task) {
    const verb = normalizedTaskVerb(task);
    const guides = {
      elegir: [
        "Enumera primero las opciones plausibles y define con qué criterio las compararás antes de escoger.",
        "La respuesta debe nombrar la elección y justificar por qué es adecuada frente a al menos una alternativa."
      ],
      seleccionar: [
        "Define criterios de selección antes de mirar el resultado que te gustaría obtener.",
        "La respuesta debe dejar visible qué criterio se usó, qué opción se descartó y por qué."
      ],
      identificar: [
        "Recorre el proceso en orden y señala cada elemento que cumple la condición pedida; evita limitarte a una lista sin justificarla.",
        "La respuesta debe mostrar qué identificaste y la razón concreta por la que pertenece a esa categoría."
      ],
      detectar: [
        "Busca señales observables del problema y vincula cada una con el mecanismo que la produciría.",
        "La respuesta debe distinguir evidencia del problema de una simple sospecha."
      ],
      comparar: [
        "Construye una comparación por dimensiones: supuesto, ventaja, limitación, coste o complejidad y situación de uso.",
        "La respuesta debe terminar con una conclusión condicionada: qué opción preferirías y bajo qué circunstancias."
      ],
      diferenciar: [
        "Define primero el criterio que separa los conceptos y después aplica ese criterio a cada uno.",
        "La respuesta debe incluir al menos una diferencia que cambie una decisión práctica."
      ],
      explicar: [
        "Organiza la explicación como una cadena: condición inicial → mecanismo → consecuencia → límite o excepción.",
        "La respuesta debe explicar el porqué, no solo repetir una definición."
      ],
      interpretar: [
        "Describe primero qué muestra el resultado, después qué significa en contexto y finalmente qué no permite concluir.",
        "La respuesta debe separar observación, interpretación y limitación."
      ],
      justificar: [
        "Formula la decisión, explicita el criterio y aporta la evidencia o razonamiento que conecta ambos.",
        "La respuesta debe permitir que otra persona audite la decisión."
      ],
      diseñar: [
        "Especifica objetivo, entradas, secuencia de decisiones, salida esperada y controles antes de añadir detalles opcionales.",
        "La respuesta debe ser suficientemente concreta para que otra persona pueda ejecutar el diseño."
      ],
      planificar: [
        "Ordena las acciones, dependencias, criterios de avance y puntos de comprobación.",
        "La respuesta debe indicar qué ocurre primero, qué depende de qué y cómo se sabrá si el plan funciona."
      ],
      proponer: [
        "Define el problema que resuelve la propuesta, los supuestos que necesita y la evidencia que permitiría aceptarla o rechazarla.",
        "La respuesta debe incluir al menos una limitación o condición de uso."
      ],
      corregir: [
        "Señala el error, explica qué sesgo o fallo introduce, reordena el procedimiento y añade una comprobación final.",
        "La respuesta debe mostrar tanto el procedimiento corregido como la razón de la corrección."
      ],
      revisar: [
        "Contrasta el trabajo con criterios explícitos uno por uno y registra cualquier incumplimiento antes de proponer cambios.",
        "La respuesta debe distinguir hallazgos, consecuencias y acciones correctivas."
      ],
      auditar: [
        "Usa una lista de criterios predefinidos, conserva evidencia para cada hallazgo y separa ausencia de evidencia de evidencia de ausencia.",
        "La respuesta debe ser trazable: criterio, evidencia, conclusión y acción."
      ],
      redactar: [
        "Convierte la idea en una regla explícita con condición, decisión y excepción; evita frases que dependan de interpretación implícita.",
        "La respuesta debe poder aplicarse de la misma forma por dos personas distintas."
      ],
      formular: [
        "Expresa con precisión población u objeto, variable o mecanismo relevante, condición y resultado esperado.",
        "La respuesta debe ser específica, comprobable y sin términos ambiguos innecesarios."
      ],
      crear: [
        "Empieza por una estructura mínima con campos obligatorios y completa cada campo con información verificable.",
        "El producto final debe ser reutilizable por otra persona sin depender de explicaciones verbales adicionales."
      ],
      construir: [
        "Divide el producto en componentes, define la función de cada uno y comprueba las interfaces entre componentes.",
        "La respuesta debe incluir el producto y una forma concreta de verificar que cumple su función."
      ],
      calcular: [
        "Escribe datos, fórmula o algoritmo, sustitución, unidades y resultado; después interpreta el valor obtenido.",
        "La respuesta debe permitir comprobar el cálculo y detectar errores de unidades o supuestos."
      ],
      estimar: [
        "Declara el estimando, los datos utilizados, el método, la incertidumbre y los supuestos que sostienen la estimación.",
        "La respuesta debe incluir una interpretación compatible con la incertidumbre, no solo un valor puntual."
      ]
    };
    return guides[verb] || [
      "Divide la tarea en decisión, justificación, evidencia y comprobación. Responde primero lo esencial y añade detalle solo donde cambie la conclusión.",
      "La respuesta debe permitir que otra persona entienda qué hiciste, por qué lo hiciste y cómo comprobarlo."
    ];
  }

  function activityHeadingList(activity, fragment) {
    const headings = [...activity.querySelectorAll(":scope > h4")];
    const heading = headings.find((item) => item.textContent.toLocaleLowerCase("es").includes(fragment));
    const list = heading?.nextElementSibling;
    return { heading, list: list?.matches("ul, ol") ? list : null };
  }

  function addTaskGuidance(list) {
    if (!list) return;
    list.classList.add("pedagogy-task-list");
    [...list.children].forEach((item) => {
      if (item.querySelector(":scope > .activity-task-help")) return;
      const task = [...item.childNodes]
        .filter((node) => node.nodeType === Node.TEXT_NODE)
        .map((node) => node.textContent)
        .join(" ")
        .trim() || item.firstChild?.textContent?.trim() || item.textContent.trim();
      const [method, evidence] = taskScaffold(task);
      const details = element("details", "activity-task-help");
      details.appendChild(element("summary", "", "Cómo abordar esta tarea"));
      const methodParagraph = element("p");
      methodParagraph.appendChild(element("strong", "", "Método: "));
      methodParagraph.appendChild(document.createTextNode(method));
      details.appendChild(methodParagraph);
      const evidenceParagraph = element("p");
      evidenceParagraph.appendChild(element("strong", "", "Tu respuesta está lista cuando: "));
      evidenceParagraph.appendChild(document.createTextNode(evidence));
      details.appendChild(evidenceParagraph);
      item.appendChild(details);
    });
  }

  function showActivityGuide(activity, activityData) {
    const existing = document.querySelector("#activity-pedagogy-dialog");
    if (existing) existing.remove();
    const dialog = element("dialog", "pedagogy-dialog");
    dialog.id = "activity-pedagogy-dialog";
    const card = element("div", "pedagogy-dialog-card");
    const title = activity.querySelector(":scope > h3")?.textContent || activityData?.title || "Actividad guiada";
    card.appendChild(element("p", "eyebrow", "Guía de trabajo"));
    card.appendChild(element("h3", "", title));
    if (activityData?.purpose) card.appendChild(element("p", "pedagogy-dialog-purpose", activityData.purpose));
    const ordered = element("ol", "pedagogy-dialog-steps");
    [
      "Lee el propósito y define qué producto final demostraría que lo alcanzaste.",
      "Sigue el procedimiento en orden; registra decisiones y supuestos en lugar de confiar en la memoria.",
      "Resuelve cada tarea justificando tus decisiones. Usa «Cómo abordar esta tarea» si no sabes cómo empezar.",
      "Construye los entregables como evidencia del trabajo, no como una lista de respuestas aisladas.",
      "Antes de terminar, revisa uno por uno los criterios de comprobación y corrige cualquier punto que no puedas demostrar."
    ].forEach((step) => ordered.appendChild(element("li", "", step)));
    card.appendChild(ordered);
    if (activityData?.estimated_duration_minutes) {
      card.appendChild(element("p", "pedagogy-dialog-time", `Tiempo orientativo: ${activityData.estimated_duration_minutes} min. Puedes dividirlo en varias sesiones.`));
    }
    const close = element("button", "pedagogy-dialog-close", "Cerrar");
    close.type = "button";
    close.addEventListener("click", () => dialog.close());
    card.appendChild(close);
    dialog.appendChild(card);
    dialog.addEventListener("click", (event) => {
      if (event.target === dialog) dialog.close();
    });
    document.body.appendChild(dialog);
    if (typeof dialog.showModal === "function") dialog.showModal();
    else dialog.setAttribute("open", "");
  }

  function enhanceAdvancedActivities(root, canonicalUnit = null) {
    const activities = [...root.querySelectorAll(".advanced-guided-activity")];
    const records = Array.isArray(canonicalUnit?.activities) ? canonicalUnit.activities : [];
    activities.forEach((activity, index) => {
      if (activity.dataset.pedagogyEnhanced === "true") return;
      activity.dataset.pedagogyEnhanced = "true";
      const data = records[index] || null;
      const title = activity.querySelector(":scope > h3");

      const brief = element("div", "activity-learning-brief");
      brief.appendChild(element("strong", "", "Qué vas a conseguir"));
      brief.appendChild(element(
        "p",
        "",
        data?.purpose || "Aplicar los conceptos de la unidad en un producto verificable, explicando las decisiones y comprobando el resultado."
      ));
      const meta = element("div", "activity-meta-row");
      if (data?.estimated_duration_minutes) meta.appendChild(element("span", "activity-meta-chip", `${data.estimated_duration_minutes} min aprox.`));
      const taskCount = Array.isArray(data?.tasks) ? data.tasks.length : activityHeadingList(activity, "problemas").list?.children.length;
      const deliverableCount = Array.isArray(data?.deliverables) ? data.deliverables.length : activityHeadingList(activity, "entregables").list?.children.length;
      if (taskCount) meta.appendChild(element("span", "activity-meta-chip", `${taskCount} tareas`));
      if (deliverableCount) meta.appendChild(element("span", "activity-meta-chip", `${deliverableCount} entregables`));
      if (meta.childElementCount) brief.appendChild(meta);
      const help = element("button", "pedagogy-help-button", "¿Cómo trabajo esta actividad?");
      help.type = "button";
      help.addEventListener("click", () => showActivityGuide(activity, data));
      brief.appendChild(help);
      if (title) title.insertAdjacentElement("afterend", brief);
      else activity.prepend(brief);

      const procedure = activityHeadingList(activity, "procedimiento");
      if (procedure.heading) procedure.heading.textContent = "Ruta de trabajo paso a paso";
      if (procedure.list) procedure.list.classList.add("pedagogy-step-list");

      const tasks = activityHeadingList(activity, "problemas");
      if (tasks.heading) tasks.heading.textContent = "Tareas: demuestra que comprendiste";
      addTaskGuidance(tasks.list);

      const deliverables = activityHeadingList(activity, "entregables");
      if (deliverables.heading) deliverables.heading.textContent = "Qué debes entregar";
      if (deliverables.list) deliverables.list.classList.add("activity-deliverables");

      const criteria = activityHeadingList(activity, "criterios");
      if (criteria.heading) criteria.heading.textContent = "Auto-comprobación antes de terminar";
      if (criteria.list) criteria.list.classList.add("activity-self-check");
    });
  }

  async function fetchCanonicalUnit(rootUrl, subjectId, unitNumber) {
    const file = `unit-${String(unitNumber).padStart(2, "0")}.json`;
    const url = new URL(`data/courses/${subjectId}/units/${file}`, rootUrl);
    const response = await fetch(url, { cache: "no-cache" });
    if (response.status === 404) return null;
    if (!response.ok) throw new Error(`No se pudo cargar ${url.pathname}: ${response.status}`);
    return response.json();
  }

'''
if anchor not in js:
    raise SystemExit("No se encontró el ancla fetchUnit en generated-units.js")
js = js.replace(anchor, helpers + anchor, 1)

old_unit_page = r'''    if (unitPage) {
      const subjectId = currentSubjectId();
      const unitNumber = Number(unitPage.dataset.unitNumber);
      if (!subjectId || !Number.isInteger(unitNumber) || unitNumber < 1) return;
      const unit = await fetchUnit(rootUrl, subjectId, unitNumber).catch((error) => {
        console.error(error);
        return null;
      });
      if (!unit) return;
      ensureGeneratedUnitStyles(rootUrl);
      renderUnitPage(unitPage, unit);
      await typesetMath(unitPage);
      return;
    }
'''
new_unit_page = r'''    if (unitPage) {
      const subjectId = currentSubjectId();
      const unitNumber = Number(unitPage.dataset.unitNumber);
      if (!subjectId || !Number.isInteger(unitNumber) || unitNumber < 1) return;
      ensureGeneratedUnitStyles(rootUrl);

      // Las páginas canónicas ya contienen la versión académica más reciente.
      // No deben ser reemplazadas por data/generated_units, que existe solo como compatibilidad.
      const hasCanonicalMarkup = Boolean(
        unitPage.querySelector(".advanced-theory-section, .advanced-guided-activity")
      );
      if (hasCanonicalMarkup) {
        const canonicalUnit = await fetchCanonicalUnit(rootUrl, subjectId, unitNumber).catch((error) => {
          console.error(error);
          return null;
        });
        enhanceAdvancedActivities(unitPage, canonicalUnit);
        return;
      }

      const unit = await fetchUnit(rootUrl, subjectId, unitNumber).catch((error) => {
        console.error(error);
        return null;
      });
      if (!unit) return;
      renderUnitPage(unitPage, unit);
      await typesetMath(unitPage);
      return;
    }
'''
if old_unit_page not in js:
    raise SystemExit("No se encontró el bloque unitPage esperado en generated-units.js")
js = js.replace(old_unit_page, new_unit_page, 1)

css_append = r'''

/* pedagogy-guided-activities:v1 */
.activity-learning-brief {
  display: grid;
  gap: 0.55rem;
  margin: 0.75rem 0 1.25rem;
  padding: 1rem 1.05rem;
  border: 1px solid rgba(8, 145, 178, 0.2);
  border-radius: 0.8rem;
  background: linear-gradient(135deg, rgba(8, 145, 178, 0.08), rgba(37, 99, 235, 0.045));
}

.activity-learning-brief > strong {
  color: var(--color-dark, #0d264c);
  font-size: 1rem;
}

.activity-learning-brief > p {
  margin: 0;
  max-width: 900px;
  line-height: 1.65;
}

.activity-meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  margin-top: 0.1rem;
}

.activity-meta-chip {
  display: inline-flex;
  align-items: center;
  padding: 0.28rem 0.6rem;
  border-radius: 999px;
  background: rgba(8, 145, 178, 0.1);
  color: #0e7490;
  font-size: 0.82rem;
  font-weight: 700;
}

.pedagogy-help-button,
.pedagogy-dialog-close {
  justify-self: start;
  margin-top: 0.25rem;
  padding: 0.55rem 0.8rem;
  border: 1px solid rgba(30, 136, 229, 0.24);
  border-radius: 0.6rem;
  background: #fff;
  color: var(--color-primary, #0b3d91);
  font: inherit;
  font-weight: 700;
  cursor: pointer;
}

.pedagogy-help-button:hover,
.pedagogy-dialog-close:hover {
  border-color: var(--color-secondary, #00b8d9);
  background: rgba(30, 136, 229, 0.04);
}

.pedagogy-help-button:focus-visible,
.pedagogy-dialog-close:focus-visible,
.activity-task-help summary:focus-visible {
  outline: 3px solid rgba(30, 136, 229, 0.22);
  outline-offset: 2px;
}

.pedagogy-step-list {
  counter-reset: activity-step;
  list-style: none;
  padding-left: 0 !important;
}

.pedagogy-step-list > li {
  position: relative;
  min-height: 2.5rem;
  padding: 0.7rem 0.8rem 0.7rem 3rem !important;
  border-left: 2px solid rgba(8, 145, 178, 0.22);
}

.pedagogy-step-list > li::before {
  counter-increment: activity-step;
  content: counter(activity-step);
  position: absolute;
  left: 0.45rem;
  top: 0.55rem;
  display: grid;
  width: 1.8rem;
  height: 1.8rem;
  place-items: center;
  border-radius: 50%;
  background: #0e7490;
  color: #fff;
  font-size: 0.82rem;
  font-weight: 800;
}

.pedagogy-task-list {
  list-style: none;
  padding-left: 0 !important;
}

.pedagogy-task-list > li {
  padding: 0.9rem 1rem !important;
  border: 1px solid rgba(30, 136, 229, 0.14);
  border-radius: 0.7rem;
  background: rgba(30, 136, 229, 0.025);
  line-height: 1.55;
}

.activity-task-help {
  margin-top: 0.65rem;
  border-top: 1px solid rgba(30, 136, 229, 0.12);
}

.activity-task-help summary {
  cursor: pointer;
  padding-top: 0.65rem;
  color: var(--color-primary, #0b3d91);
  font-weight: 700;
}

.activity-task-help p {
  margin: 0.6rem 0 0;
  color: var(--color-muted, #526a8b);
  line-height: 1.6;
}

.activity-deliverables,
.activity-self-check {
  list-style: none;
  padding-left: 0 !important;
}

.activity-deliverables > li,
.activity-self-check > li {
  position: relative;
  padding: 0.7rem 0.75rem 0.7rem 2.35rem !important;
  border-radius: 0.55rem;
  background: rgba(16, 185, 129, 0.045);
}

.activity-deliverables > li::before,
.activity-self-check > li::before {
  content: "";
  position: absolute;
  left: 0.75rem;
  top: 0.86rem;
  width: 0.9rem;
  height: 0.9rem;
  border: 2px solid #059669;
  border-radius: 0.2rem;
  background: #fff;
}

.pedagogy-dialog {
  width: min(720px, calc(100vw - 2rem));
  max-height: min(82vh, 760px);
  padding: 0;
  border: 0;
  border-radius: 1rem;
  box-shadow: 0 28px 80px rgba(13, 38, 76, 0.28);
}

.pedagogy-dialog::backdrop {
  background: rgba(8, 20, 40, 0.56);
  backdrop-filter: blur(3px);
}

.pedagogy-dialog-card {
  display: grid;
  gap: 0.8rem;
  padding: 1.4rem;
  background: #fff;
}

.pedagogy-dialog-card h3,
.pedagogy-dialog-card p {
  margin: 0;
}

.pedagogy-dialog-purpose,
.pedagogy-dialog-time {
  color: var(--color-muted, #526a8b);
  line-height: 1.65;
}

.pedagogy-dialog-steps {
  display: grid;
  gap: 0.7rem;
  margin: 0.25rem 0;
  padding-left: 1.35rem;
}

@media (max-width: 700px) {
  .activity-learning-brief {
    padding: 0.85rem;
  }

  .pedagogy-step-list > li {
    padding-right: 0.25rem !important;
  }

  .pedagogy-dialog-card {
    padding: 1rem;
  }
}
'''
if "pedagogy-guided-activities:v1" in css:
    raise SystemExit("El CSS pedagógico ya está aplicado.")
css = css.rstrip() + css_append + "\n"

JS_PATH.write_text(js, encoding="utf-8")
CSS_PATH.write_text(css, encoding="utf-8")
print("Parche pedagógico aplicado a generated-units.js y generated-units.css")
