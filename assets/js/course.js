(() => {
  "use strict";

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

  function appendHeading(parent, level, text, id = "") {
    const heading = element(`h${level}`, "course-heading", text);
    if (id) heading.id = id;
    parent.appendChild(heading);
    return heading;
  }

  function currentSubjectId() {
    const parts = window.location.pathname.split("/").filter(Boolean);
    if (parts.at(-1)?.endsWith(".html")) parts.pop();
    return parts.at(-1) || "";
  }

  function addTocLink(targetId, label, beforeSelector = null) {
    const toc = document.querySelector(".course-toc");
    if (!toc || toc.querySelector(`a[href="#${targetId}"]`)) return;
    const link = element("a", "", label);
    link.href = `#${targetId}`;
    const before = beforeSelector ? toc.querySelector(beforeSelector) : null;
    if (before) toc.insertBefore(link, before);
    else toc.appendChild(link);
  }


function renderCourseHeader(course) {
  const meta = document.querySelector(".course-meta");
  if (!meta) return;
  const values = meta.querySelectorAll("dd");
  if (values[0] && course.academic_level) values[0].textContent = course.academic_level;
}

function renderPurpose(course) {
    const section = document.querySelector("#proposito");
    if (!section) return;

    const overview = element("div", "course-overview");
    appendHeading(overview, 3, "Alcance del curso");
    overview.appendChild(element("p", "", course.course_purpose));

    if (course.study_method?.length) {
      appendHeading(overview, 3, "Cómo estudiar esta asignatura");
      appendList(overview, course.study_method, "course-checklist");
    }
    section.appendChild(overview);
  }

  function renderPrerequisites(course) {
    const section = document.querySelector("#prerrequisitos");
    if (!section) return;

    if (course.prerequisites?.length) {
      const wrapper = element("div", "course-panel");
      appendHeading(wrapper, 3, "Conocimientos necesarios");
      appendList(wrapper, course.prerequisites);
      section.appendChild(wrapper);
    }

    const diagnostic = course.diagnostic_assessment;
    if (!diagnostic) return;

    const details = element("details", "course-details");
    const summary = element("summary", "", diagnostic.title || "Diagnóstico de prerrequisitos");
    details.appendChild(summary);
    if (diagnostic.purpose) details.appendChild(element("p", "", diagnostic.purpose));

    const questions = element("div", "course-diagnostic");
    (diagnostic.questions || []).forEach((item, index) => {
      const question = element("details", "course-question");
      question.appendChild(element("summary", "", `${index + 1}. ${item.question}`));
      question.appendChild(element("p", "", item.answer));
      questions.appendChild(question);
    });
    details.appendChild(questions);

    if (diagnostic.interpretation?.length) {
      appendHeading(details, 4, "Interpretación del resultado");
      appendList(details, diagnostic.interpretation);
    }
    section.appendChild(details);
  }

  function renderCompetencies(course) {
    const section = document.querySelector("#competencias");
    if (!section || !course.course_competencies?.length) return;
    const existing = section.querySelector("ul");
    if (existing) existing.remove();
    appendList(section, course.course_competencies, "course-outcomes");
  }

  function renderLearningOutcomes(course) {
    const section = document.querySelector("#resultados");
    if (!section || !course.learning_outcomes?.length) return;
    const existing = section.querySelector("ul");
    if (existing) existing.remove();
    appendList(section, course.learning_outcomes, "course-outcomes");
  }


  function renderAssessment(course) {
    const section = document.querySelector("#evaluacion");
    if (!section || !course.assessment_plan?.length) return;

    const wrapper = element("div", "course-assessment");
    appendHeading(wrapper, 3, "Plan de evaluación");
    const table = element("table", "course-table course-grading");
    const thead = element("thead");
    const headRow = element("tr");
    ["Componente", "Ponderación", "Evidencia evaluada"].forEach((label) => headRow.appendChild(element("th", "", label)));
    thead.appendChild(headRow);
    table.appendChild(thead);

    const tbody = element("tbody");
    let total = 0;
    for (const item of course.assessment_plan) {
      const tr = element("tr");
      tr.appendChild(element("td", "", item.component));
      tr.appendChild(element("td", "", `${item.weight_percent} %`));
      tr.appendChild(element("td", "", item.description));
      tbody.appendChild(tr);
      total += Number(item.weight_percent || 0);
    }
    const totalRow = element("tr", "course-total");
    totalRow.appendChild(element("th", "", "Total"));
    totalRow.appendChild(element("th", "", `${total} %`));
    totalRow.appendChild(element("td", "", ""));
    tbody.appendChild(totalRow);
    table.appendChild(tbody);
    wrapper.appendChild(table);

    if (course.assessment_principles?.length) {
      appendHeading(wrapper, 4, "Principios de corrección");
      appendList(wrapper, course.assessment_principles);
    }

    if (course.midterm_exam_blueprint?.length) {
      appendHeading(wrapper, 4, "Estructura del examen intermedio");
      const list = element("ul");
      course.midterm_exam_blueprint.forEach((item) => {
        list.appendChild(element("li", "", `${item.domain}: ${item.weight_percent} %`));
      });
      wrapper.appendChild(list);
    }
    section.appendChild(wrapper);
  }

  function renderFinalProject(course) {
    const section = document.querySelector("#practicas");
    const project = course.final_project;
    if (!section || !project) return;

    const wrapper = element("article", "course-project");
    appendHeading(wrapper, 3, `Proyecto integrador: ${project.title}`, "proyecto-integrador");
    wrapper.appendChild(element("p", "course-project-scenario", project.scenario));

    appendHeading(wrapper, 4, "Fases");
    const phases = element("ol");
    (project.phases || []).forEach((phase) => phases.appendChild(element("li", "", phase)));
    wrapper.appendChild(phases);

    appendHeading(wrapper, 4, "Entregables");
    appendList(wrapper, project.deliverables);

    if (project.rubric?.length) {
      appendHeading(wrapper, 4, "Rúbrica");
      const table = element("table", "course-table");
      const thead = element("thead");
      const headRow = element("tr");
      ["Criterio", "Peso", "Desempeño excelente"].forEach((label) => headRow.appendChild(element("th", "", label)));
      thead.appendChild(headRow);
      table.appendChild(thead);
      const tbody = element("tbody");
      project.rubric.forEach((item) => {
        const tr = element("tr");
        tr.appendChild(element("td", "", item.criterion));
        tr.appendChild(element("td", "", `${item.weight_percent} %`));
        tr.appendChild(element("td", "", item.excellent));
        tbody.appendChild(tr);
      });
      table.appendChild(tbody);
      wrapper.appendChild(table);
    }
    section.appendChild(wrapper);
    addTocLink("proyecto-integrador", "Proyecto", 'a[href="#evaluacion"]');
  }

  function renderResources(course) {
    const section = document.querySelector("#recursos");
    if (!section || !course.core_resources?.length) return;

    const wrapper = element("div", "course-resources");
    appendHeading(wrapper, 3, "Bibliografía central del curso");
    const list = element("ol");
    for (const resource of course.core_resources) {
      const item = element("li");
      const link = element("a", "", resource.title);
      link.href = resource.url;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      item.appendChild(link);
      item.appendChild(document.createTextNode(` — ${resource.organization}. ${resource.role}`));
      list.appendChild(item);
    }
    wrapper.appendChild(list);

    if (course.completion_criteria?.length) {
      appendHeading(wrapper, 3, "Criterios para completar la asignatura", "criterios-finalizacion");
      appendList(wrapper, course.completion_criteria, "course-checklist");
    }
    section.appendChild(wrapper);
  }

  async function loadCourse(rootUrl, subjectId) {
    const url = new URL(`data/generated_courses/${subjectId}.json`, rootUrl);
    const response = await fetch(url, { cache: "no-cache" });
    if (response.status === 404) return null;
    if (!response.ok) throw new Error(`No se pudo cargar ${url.pathname}: ${response.status}`);
    return response.json();
  }

  async function init() {
    const subjectId = currentSubjectId();
    if (!subjectId) return;
    const rootUrl = new URL("../../", window.location.href);
    const course = await loadCourse(rootUrl, subjectId).catch((error) => {
      console.error(error);
      return null;
    });
    if (!course) return;

    const css = element("link");
    css.rel = "stylesheet";
    css.href = new URL("assets/css/course.css", rootUrl).href;
    document.head.appendChild(css);

    renderCourseHeader(course);
    renderPurpose(course);
    renderPrerequisites(course);
    renderCompetencies(course);
    renderLearningOutcomes(course);
    renderFinalProject(course);
    renderAssessment(course);
    renderResources(course);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
