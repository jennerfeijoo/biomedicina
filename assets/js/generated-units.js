(() => {
  "use strict";

  const UNIT_FILE_LIMIT = 12;

  function element(tag, className = "", text = null) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== null && text !== undefined) node.textContent = String(text);
    return node;
  }

  function listItemText(item) {
    if (item === null || item === undefined) return "";
    if (typeof item !== "object") return String(item).trim();

    const topic = String(item.topic || item.title || item.label || "").trim();
    const connection = String(
      item.connection || item.description || item.text || item.value || ""
    ).trim();
    if (topic && connection) return `${topic}: ${connection}`;
    return topic || connection;
  }

  function appendList(parent, items, className = "") {
    const list = element("ul", className);
    for (const item of items || []) {
      const text = listItemText(item);
      if (text) list.appendChild(element("li", "", text));
    }
    parent.appendChild(list);
    return list;
  }

  function appendHeading(parent, level, text) {
    const heading = element(`h${level}`, "generated-unit-heading", text);
    parent.appendChild(heading);
    return heading;
  }

  function asArray(source, singular, plural) {
    if (Array.isArray(source?.[plural])) return source[plural];
    const value = source?.[singular];
    return value && typeof value === "object" ? [value] : [];
  }

  function renderEquations(parent, equations) {
    if (!Array.isArray(equations) || equations.length === 0) return;
    const group = element("div", "generated-unit-equations");
    for (const rawEquation of equations) {
      const equation = typeof rawEquation === "string" ? { latex: rawEquation } : rawEquation;
      if (!equation || typeof equation.latex !== "string" || !equation.latex.trim()) continue;
      const block = element("div", "generated-unit-math");
      if (equation.label) block.appendChild(element("strong", "generated-unit-math-label", equation.label));
      block.appendChild(element("div", "generated-unit-math-expression", `\\[${equation.latex}\\]`));
      if (equation.interpretation) block.appendChild(element("p", "generated-unit-math-interpretation", equation.interpretation));
      group.appendChild(block);
    }
    if (group.childElementCount) parent.appendChild(group);
  }

  function renderUnitMetadata(parent, unit) {
    const values = [];
    if (unit.difficulty) values.push(unit.difficulty);
    if (values.length) parent.appendChild(element("p", "generated-unit-meta", values.join(" · ")));

    if (unit.prerequisite_knowledge?.length) {
      const details = element("details", "generated-unit-details");
      details.appendChild(element("summary", "", "Conocimientos previos de la unidad"));
      appendList(details, unit.prerequisite_knowledge);
      parent.appendChild(details);
    }

    if (unit.progression?.previous || unit.progression?.next) {
      const progression = element("div", "generated-unit-progression");
      if (unit.progression.previous) {
        const paragraph = element("p");
        paragraph.appendChild(element("strong", "", "Parte de: "));
        paragraph.appendChild(document.createTextNode(unit.progression.previous));
        progression.appendChild(paragraph);
      }
      if (unit.progression.next) {
        const paragraph = element("p");
        paragraph.appendChild(element("strong", "", "Prepara para: "));
        paragraph.appendChild(document.createTextNode(unit.progression.next));
        progression.appendChild(paragraph);
      }
      parent.appendChild(progression);
    }
  }

  function renderTheory(parent, sections) {
    if (!Array.isArray(sections) || sections.length === 0) return;
    appendHeading(parent, 4, "Desarrollo teórico");
    for (const section of sections) {
      const block = element("section", "generated-unit-theory");
      appendHeading(block, 5, section.heading || "Concepto");
      for (const paragraph of section.paragraphs || []) block.appendChild(element("p", "", paragraph));
      renderEquations(block, section.equations);
      if (section.key_points?.length) {
        const summary = element("div", "generated-unit-key-points");
        summary.appendChild(element("strong", "", "Ideas clave"));
        appendList(summary, section.key_points);
        block.appendChild(summary);
      }
      parent.appendChild(block);
    }
  }

  function renderGlossary(parent, glossary) {
    if (!Array.isArray(glossary) || glossary.length === 0) return;
    const details = element("details", "generated-unit-details");
    details.appendChild(element("summary", "", `Glosario (${glossary.length} términos)`));
    const dl = element("dl", "generated-unit-glossary");
    for (const item of glossary) {
      dl.appendChild(element("dt", "", item.term));
      dl.appendChild(element("dd", "", item.definition));
    }
    details.appendChild(dl);
    parent.appendChild(details);
  }

  function renderWorkedExample(parent, example, index, total) {
    if (!example || typeof example !== "object") return;
    const section = element("section", "generated-unit-panel generated-unit-example");
    const prefix = total > 1 ? `Ejemplo ${index + 1}` : "Ejemplo";
    appendHeading(section, 4, `${prefix}: ${example.title || "Aplicación"}`);
    if (example.scenario) section.appendChild(element("p", "generated-unit-scenario", example.scenario));
    renderEquations(section, example.equations);
    if (example.pseudocode?.length) {
      section.appendChild(element("strong", "", "Pseudocódigo"));
      appendList(section, example.pseudocode);
    }
    if (example.reasoning_steps?.length) {
      section.appendChild(element("strong", "", "Razonamiento paso a paso"));
      const ordered = element("ol", "generated-unit-steps");
      for (const step of example.reasoning_steps) ordered.appendChild(element("li", "", step));
      section.appendChild(ordered);
    }
    if (example.code) {
      const pre = element("pre", "generated-unit-code");
      pre.appendChild(element("code", "", example.code));
      section.appendChild(pre);
    }
    if (example.expected_output) {
      const output = element("p");
      output.appendChild(element("strong", "", "Salida esperada: "));
      output.appendChild(document.createTextNode(example.expected_output));
      section.appendChild(output);
    }
    if (example.interpretation) {
      const interpretation = element("p");
      interpretation.appendChild(element("strong", "", "Interpretación: "));
      interpretation.appendChild(document.createTextNode(example.interpretation));
      section.appendChild(interpretation);
    }
    if (example.verification?.length) {
      section.appendChild(element("strong", "", "Comprobación"));
      appendList(section, example.verification);
    }
    if (example.limitations?.length) {
      section.appendChild(element("strong", "", "Limitaciones"));
      appendList(section, example.limitations);
    }
    parent.appendChild(section);
  }

  function renderActivity(parent, activity, index, total) {
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

  function renderPracticeSets(parent, sets) {
    if (!Array.isArray(sets) || sets.length === 0) return;
    appendHeading(parent, 4, "Práctica graduada");
    for (const set of sets) {
      const wrapper = element("section", "generated-unit-practice-set");
      appendHeading(wrapper, 5, set.title || set.level || "Problemas");
      if (set.purpose) wrapper.appendChild(element("p", "", set.purpose));
      const list = element("ol", "generated-unit-practice-list");
      for (const problem of set.problems || []) {
        const item = element("li", "generated-unit-practice-item");
        if (typeof problem === "string") {
          item.appendChild(document.createTextNode(problem));
        } else {
          item.appendChild(element("p", "generated-unit-problem-prompt", problem.prompt || "Problema"));
          renderEquations(item, problem.equations);
          if (problem.hint || problem.solution || problem.answer) {
            const details = element("details", "generated-unit-solution");
            details.appendChild(element("summary", "", problem.solution ? "Ver orientación y solución" : "Ver orientación"));
            if (problem.hint) {
              const hint = element("p");
              hint.appendChild(element("strong", "", "Pista: "));
              hint.appendChild(document.createTextNode(problem.hint));
              details.appendChild(hint);
            }
            if (problem.solution) details.appendChild(element("p", "", problem.solution));
            if (problem.answer) {
              const answer = element("p");
              answer.appendChild(element("strong", "", "Respuesta: "));
              answer.appendChild(document.createTextNode(problem.answer));
              details.appendChild(answer);
            }
            item.appendChild(details);
          }
        }
        list.appendChild(item);
      }
      wrapper.appendChild(list);
      parent.appendChild(wrapper);
    }
  }

  function renderCommonErrors(parent, errors) {
    if (!Array.isArray(errors) || errors.length === 0) return;
    appendHeading(parent, 4, "Errores frecuentes");
    const list = element("div", "generated-unit-errors");
    for (const item of errors) {
      const card = element("div", "generated-unit-error");
      card.appendChild(element("strong", "", item.error));
      card.appendChild(element("p", "", item.correction));
      list.appendChild(card);
    }
    parent.appendChild(list);
  }

  function renderAssessment(parent, questions) {
    if (!Array.isArray(questions) || questions.length === 0) return;
    const details = element("details", "generated-unit-details");
    details.appendChild(element("summary", "", `Autoevaluación (${questions.length} preguntas)`));
    const wrapper = element("div", "generated-unit-assessment");
    questions.forEach((item, index) => {
      const question = element("details", "generated-unit-question");
      question.appendChild(element("summary", "", `${index + 1}. ${item.question}`));
      question.appendChild(element("p", "", item.answer));
      wrapper.appendChild(question);
    });
    details.appendChild(wrapper);
    parent.appendChild(details);
  }

  function renderSources(parent, sources) {
    if (!Array.isArray(sources) || sources.length === 0) return;
    appendHeading(parent, 4, "Fuentes de la unidad");
    const list = element("ul", "generated-unit-sources");
    for (const source of sources) {
      const item = element("li");
      const url = String(source.url || "");
      if (url.startsWith("https://") || url.startsWith("http://")) {
        const link = element("a", "", source.title || url);
        link.href = url;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        item.appendChild(link);
      } else {
        item.appendChild(element("span", "", source.title || "Fuente"));
      }
      const organization = [source.organization, source.type].filter(Boolean).join(" · ");
      if (organization) item.appendChild(document.createTextNode(` — ${organization}`));
      if (source.use) item.appendChild(document.createTextNode(`. ${source.use}`));
      list.appendChild(item);
    }
    parent.appendChild(list);
  }

  function renderUnit(article, unit) {
    article.classList.add("course-unit-developed");
    article.replaceChildren();
    article.appendChild(element("h3", "", `Unidad ${unit.unit}. ${unit.title}`));
    renderUnitMetadata(article, unit);
    if (unit.purpose) article.appendChild(element("p", "generated-unit-purpose", unit.purpose));
    if (unit.learning_objectives?.length) {
      appendHeading(article, 4, "Objetivos de aprendizaje");
      appendList(article, unit.learning_objectives);
    }

    renderTheory(article, unit.theory_sections);
    renderEquations(article, unit.equations);
    renderGlossary(article, unit.glossary);

    const examples = asArray(unit, "worked_example", "worked_examples");
    examples.forEach((example, index) => renderWorkedExample(article, example, index, examples.length));

    const activities = asArray(unit, "guided_activity", "guided_activities");
    activities.forEach((activity, index) => renderActivity(article, activity, index, activities.length));

    renderPracticeSets(article, unit.practice_sets);
    renderCommonErrors(article, unit.common_errors);
    renderAssessment(article, unit.self_assessment);

    if (unit.biomedical_connections?.length) {
      appendHeading(article, 4, "Conexiones biomédicas");
      appendList(article, unit.biomedical_connections);
    }
    renderSources(article, unit.sources);
  }

  function unitNumberFromArticle(article) {
    const heading = article.querySelector("h3");
    const match = heading?.textContent?.match(/Unidad\s+(\d+)/i);
    return match ? Number(match[1]) : null;
  }

  function unitTitleFromArticle(article) {
    const heading = article.querySelector("h3");
    return heading?.textContent?.replace(/^Unidad\s+\d+\.?\s*/i, "").trim() || "Unidad";
  }

  function scrollToTarget(targetId) {
    const target = document.getElementById(targetId);
    if (!target) return;
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    history.pushState(null, "", `#${targetId}`);
    target.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
  }

  function createUnitSelector(articles) {
    const unitsLink = document.querySelector('.course-toc a[href="#unidades"]');
    if (!unitsLink) return;

    const select = element("select", "course-unit-select");
    select.setAttribute("aria-label", "Ir a una unidad concreta");
    select.title = "Ir a una unidad concreta";

    const overview = element("option", "", "Unidades");
    overview.value = "unidades";
    select.appendChild(overview);

    for (const article of articles) {
      const number = unitNumberFromArticle(article);
      if (number === null) continue;
      const id = `unidad-${number}`;
      article.id = id;
      const option = element("option", "", `Unidad ${number} · ${unitTitleFromArticle(article)}`);
      option.value = id;
      select.appendChild(option);
    }

    const syncFromHash = () => {
      const hash = window.location.hash.slice(1);
      const exists = [...select.options].some((option) => option.value === hash);
      select.value = exists ? hash : "unidades";
    };

    select.addEventListener("change", () => scrollToTarget(select.value));
    window.addEventListener("hashchange", syncFromHash);
    unitsLink.replaceWith(select);
    syncFromHash();
  }

  async function typesetMath(root) {
    const mathJax = window.MathJax;
    if (!mathJax) return;
    try {
      if (mathJax.startup?.promise) await mathJax.startup.promise;
      if (typeof mathJax.typesetClear === "function") mathJax.typesetClear([root]);
      if (typeof mathJax.typesetPromise === "function") await mathJax.typesetPromise([root]);
    } catch (error) {
      console.error("No se pudo renderizar la notación matemática.", error);
    }
  }

  // pedagogy-guided-activities:v1
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

  async function fetchUnit(rootUrl, subjectId, unitNumber) {
    const file = `unit-${String(unitNumber).padStart(2, "0")}.json`;
    const url = new URL(`data/generated_units/${subjectId}/${file}`, rootUrl);
    const response = await fetch(url, { cache: "no-cache" });
    if (response.status === 404) return null;
    if (!response.ok) throw new Error(`No se pudo cargar ${url.pathname}: ${response.status}`);
    return response.json();
  }

  function currentSubjectId() {
    const explicit = document.querySelector("[data-subject-id]")?.dataset.subjectId;
    if (explicit) return explicit;
    const parts = window.location.pathname.split("/").filter(Boolean);
    if (parts.at(-1)?.endsWith(".html")) parts.pop();
    if (parts.at(-1) === "unidades") return parts.at(-2) || "";
    return parts.at(-1) || "";
  }

  function siteRootUrl() {
    const brandHref = document.querySelector(".brand")?.getAttribute("href");
    if (brandHref) return new URL("./", new URL(brandHref, window.location.href));
    return new URL("/", window.location.href);
  }

  function ensureGeneratedUnitStyles(rootUrl) {
    if (document.querySelector('link[data-generated-units="true"]')) return;
    const css = element("link");
    css.rel = "stylesheet";
    css.href = new URL("assets/css/generated-units.css", rootUrl).href;
    css.dataset.generatedUnits = "true";
    document.head.appendChild(css);
  }

  function createUnitPageSection(id, title, description = "") {
    const section = element("section", "section");
    section.id = id;
    const header = element("div", "section-header");
    header.appendChild(element("h2", "", title));
    if (description) header.appendChild(element("p", "", description));
    section.appendChild(header);
    return section;
  }

  function renderUnitPage(container, unit) {
    container.classList.add("course-unit-developed");
    container.replaceChildren();

    const results = createUnitPageSection("resultados", "Resultados y alcance");
    renderUnitMetadata(results, unit);
    if (unit.learning_objectives?.length) {
      appendHeading(results, 3, "Objetivos de aprendizaje");
      appendList(results, unit.learning_objectives);
    }
    if (unit.biomedical_connections?.length) {
      appendHeading(results, 3, "Conexiones biomédicas");
      appendList(results, unit.biomedical_connections);
    }
    container.appendChild(results);

    const theory = createUnitPageSection(
      "teoria",
      "Desarrollo teórico",
      "La teoría, las ecuaciones y el glosario se presentan dentro de la lección correspondiente."
    );
    renderTheory(theory, unit.theory_sections);
    renderEquations(theory, unit.equations);
    renderGlossary(theory, unit.glossary);
    container.appendChild(theory);

    const caseSection = createUnitPageSection("caso", "Casos y ejemplos resueltos");
    const examples = asArray(unit, "worked_example", "worked_examples");
    if (examples.length) {
      examples.forEach((example, index) => renderWorkedExample(caseSection, example, index, examples.length));
    } else {
      caseSection.appendChild(element("p", "muted", "Esta edición no incluye todavía un ejemplo resuelto específico."));
    }
    container.appendChild(caseSection);

    const practice = createUnitPageSection("practica", "Práctica guiada y problemas");
    const activities = asArray(unit, "guided_activity", "guided_activities");
    activities.forEach((activity, index) => renderActivity(practice, activity, index, activities.length));
    renderPracticeSets(practice, unit.practice_sets);
    renderCommonErrors(practice, unit.common_errors);
    if (!activities.length && !unit.practice_sets?.length) {
      practice.appendChild(element("p", "muted", "La práctica específica de esta edición permanece pendiente."));
    }
    container.appendChild(practice);

    const assessment = createUnitPageSection("autoevaluacion", "Autoevaluación");
    renderAssessment(assessment, unit.self_assessment);
    if (!unit.self_assessment?.length) {
      assessment.appendChild(element("p", "muted", "La autoevaluación específica de esta edición permanece pendiente."));
    }
    container.appendChild(assessment);

    const sources = createUnitPageSection("fuentes", "Fuentes de la unidad");
    renderSources(sources, unit.sources);
    if (!unit.sources?.length) {
      sources.appendChild(element("p", "muted", "Consulta los recursos generales de la asignatura."));
    }
    container.appendChild(sources);
  }

  function loadCourseEnhancer(rootUrl) {
    if (document.querySelector('script[data-course="true"]')) return;
    const script = element("script");
    script.src = new URL("assets/js/course.js", rootUrl).href;
    script.defer = true;
    script.dataset.course = "true";
    document.body.appendChild(script);
  }

  async function init() {
    const rootUrl = siteRootUrl();
    const unitPage = document.querySelector(".unit-lesson[data-unit-number]");
    if (unitPage) {
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

    const unitsSection = document.querySelector("#unidades .course-units");
    if (!unitsSection) return;
    const articles = [...unitsSection.querySelectorAll(".course-unit")];
    if (articles.length === 0) return;
    const subjectId = currentSubjectId();
    if (!subjectId) return;

    ensureGeneratedUnitStyles(rootUrl);
    createUnitSelector(articles);

    const total = Math.min(Math.max(articles.length, 1), UNIT_FILE_LIMIT);
    const results = await Promise.all(
      Array.from({ length: total }, (_, index) => fetchUnit(rootUrl, subjectId, index + 1).catch((error) => {
        console.error(error);
        return null;
      }))
    );

    const articleByUnit = new Map();
    for (const article of articles) {
      const number = unitNumberFromArticle(article);
      if (number !== null) articleByUnit.set(number, article);
    }
    for (const unit of results.filter(Boolean)) {
      const article = articleByUnit.get(Number(unit.unit));
      if (article) renderUnit(article, unit);
    }

    await typesetMath(unitsSection);
    loadCourseEnhancer(rootUrl);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
