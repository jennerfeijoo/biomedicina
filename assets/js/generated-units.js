(() => {
  "use strict";

  const UNIT_FILE_LIMIT = 12;

  function element(tag, className = "", text = null) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== null && text !== undefined) node.textContent = String(text);
    return node;
  }

  function appendList(parent, items, className = "") {
    const list = element("ul", className);
    for (const item of items || []) list.appendChild(element("li", "", item));
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
    if (unit.estimated_hours) values.push(`${unit.estimated_hours} horas estimadas`);
    if (unit.weeks?.length) values.push(`Semanas ${unit.weeks.join("–")}`);
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

  async function fetchUnit(rootUrl, subjectId, unitNumber) {
    const file = `unit-${String(unitNumber).padStart(2, "0")}.json`;
    const url = new URL(`data/generated_units/${subjectId}/${file}`, rootUrl);
    const response = await fetch(url, { cache: "no-cache" });
    if (response.status === 404) return null;
    if (!response.ok) throw new Error(`No se pudo cargar ${url.pathname}: ${response.status}`);
    return response.json();
  }

  function currentSubjectId() {
    const parts = window.location.pathname.split("/").filter(Boolean);
    if (parts.at(-1)?.endsWith(".html")) parts.pop();
    return parts.at(-1) || "";
  }

  function loadSemesterCourseEnhancer(rootUrl) {
    if (document.querySelector('script[data-semester-course="true"]')) return;
    const script = element("script");
    script.src = new URL("assets/js/semester-course.js", rootUrl).href;
    script.defer = true;
    script.dataset.semesterCourse = "true";
    document.body.appendChild(script);
  }

  async function init() {
    const unitsSection = document.querySelector("#unidades .course-units");
    if (!unitsSection) return;

    const articles = [...unitsSection.querySelectorAll(".course-unit")];
    if (articles.length === 0) return;

    const subjectId = currentSubjectId();
    if (!subjectId) return;

    const rootUrl = new URL("../../", window.location.href);
    const css = element("link");
    css.rel = "stylesheet";
    css.href = new URL("assets/css/generated-units.css", rootUrl).href;
    document.head.appendChild(css);

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
    loadSemesterCourseEnhancer(rootUrl);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
