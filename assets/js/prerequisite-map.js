(() => {
  const curriculumUrl = "../data/citonauta_curriculum.json";
  const graphUrl = "../data/prerequisite_graph.json";

  const normalize = (value) => String(value || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();

  const elements = {
    search: document.querySelector("[data-subject-search]"),
    select: document.querySelector("[data-subject-select]"),
    status: document.querySelector("[data-map-status]"),
    flow: document.querySelector("[data-dependency-flow]"),
    foundations: document.querySelector("[data-foundations]"),
    selected: document.querySelector("[data-selected-course]"),
    next: document.querySelector("[data-next-courses]"),
    ancestors: document.querySelector("[data-ancestors]"),
    descendants: document.querySelector("[data-descendants]"),
    ancestorCount: document.querySelector("[data-ancestor-count]"),
    descendantCount: document.querySelector("[data-descendant-count]")
  };

  if (!elements.select || !elements.status) return;

  const state = {
    subjects: new Map(),
    orderedSubjects: [],
    incoming: new Map(),
    outgoing: new Map()
  };

  const flattenSubjects = (curriculum) => {
    const subjects = [];
    for (const area of curriculum.areas || []) {
      for (const subject of area.subjects || []) {
        subjects.push({
          ...subject,
          areaId: area.id,
          areaTitle: area.title,
          href: `../${subject.path}`
        });
      }
    }
    return subjects.sort((a, b) => a.title.localeCompare(b.title, "es"));
  };

  const addEdge = (map, key, edge) => {
    if (!map.has(key)) map.set(key, []);
    map.get(key).push(edge);
  };

  const optionFor = (subject) => {
    const option = document.createElement("option");
    option.value = subject.id;
    option.textContent = `${subject.title} — ${subject.areaTitle}`;
    option.dataset.search = normalize(`${subject.title} ${subject.description} ${subject.areaTitle}`);
    return option;
  };

  const populateSelect = (query = "") => {
    const current = elements.select.value;
    const normalizedQuery = normalize(query);
    const fragment = document.createDocumentFragment();
    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = "Selecciona una asignatura";
    fragment.appendChild(placeholder);

    for (const subject of state.orderedSubjects) {
      const haystack = normalize(`${subject.title} ${subject.description} ${subject.areaTitle}`);
      if (!normalizedQuery || haystack.includes(normalizedQuery)) {
        fragment.appendChild(optionFor(subject));
      }
    }
    elements.select.replaceChildren(fragment);
    if (current && state.subjects.has(current)) elements.select.value = current;
  };

  const createCourseCard = (subject, edge = null) => {
    const article = document.createElement("article");
    article.className = "dependency-card";

    const link = document.createElement("a");
    link.href = subject.href;
    link.textContent = subject.title;
    link.className = "dependency-card-title";

    const area = document.createElement("span");
    area.className = "catalog-chip";
    area.textContent = subject.areaTitle;

    article.append(link, area);
    if (edge?.rationale) {
      const rationale = document.createElement("p");
      rationale.textContent = edge.rationale;
      article.appendChild(rationale);
    }
    return article;
  };

  const renderList = (container, edges, direction) => {
    container.replaceChildren();
    if (!edges.length) {
      const empty = document.createElement("p");
      empty.className = "dependency-empty";
      empty.textContent = direction === "incoming"
        ? "No hay una base curricular directa curada para esta asignatura."
        : "No hay una continuación directa curada desde esta asignatura.";
      container.appendChild(empty);
      return;
    }
    for (const edge of edges) {
      const subjectId = direction === "incoming" ? edge.from : edge.to;
      const subject = state.subjects.get(subjectId);
      if (subject) container.appendChild(createCourseCard(subject, edge));
    }
  };

  const traverse = (startId, adjacency, nextKey) => {
    const visited = new Set();
    const queue = [startId];
    while (queue.length) {
      const current = queue.shift();
      for (const edge of adjacency.get(current) || []) {
        const next = edge[nextKey];
        if (!visited.has(next) && next !== startId) {
          visited.add(next);
          queue.push(next);
        }
      }
    }
    return [...visited]
      .map((id) => state.subjects.get(id))
      .filter(Boolean)
      .sort((a, b) => a.title.localeCompare(b.title, "es"));
  };

  const renderCompactList = (container, subjects) => {
    container.replaceChildren();
    if (!subjects.length) {
      const item = document.createElement("li");
      item.textContent = "Sin relaciones transitivas curadas.";
      container.appendChild(item);
      return;
    }
    for (const subject of subjects) {
      const item = document.createElement("li");
      const link = document.createElement("a");
      link.href = subject.href;
      link.textContent = subject.title;
      item.appendChild(link);
      container.appendChild(item);
    }
  };

  const updateUrl = (subjectId) => {
    const url = new URL(window.location.href);
    if (subjectId) url.searchParams.set("subject", subjectId);
    else url.searchParams.delete("subject");
    window.history.replaceState({}, "", url);
  };

  const renderSubject = (subjectId, updateHistory = true) => {
    const subject = state.subjects.get(subjectId);
    if (!subject) {
      elements.flow.hidden = true;
      elements.status.textContent = "Selecciona una asignatura para explorar sus dependencias.";
      elements.ancestorCount.textContent = "0";
      elements.descendantCount.textContent = "0";
      renderCompactList(elements.ancestors, []);
      renderCompactList(elements.descendants, []);
      if (updateHistory) updateUrl("");
      return;
    }

    const incoming = state.incoming.get(subjectId) || [];
    const outgoing = state.outgoing.get(subjectId) || [];
    const ancestors = traverse(subjectId, state.incoming, "from");
    const descendants = traverse(subjectId, state.outgoing, "to");

    elements.selected.replaceChildren(createCourseCard(subject));
    renderList(elements.foundations, incoming, "incoming");
    renderList(elements.next, outgoing, "outgoing");
    renderCompactList(elements.ancestors, ancestors);
    renderCompactList(elements.descendants, descendants);
    elements.ancestorCount.textContent = String(ancestors.length);
    elements.descendantCount.textContent = String(descendants.length);
    elements.flow.hidden = false;
    elements.status.textContent = `${subject.title}: ${incoming.length} bases directas y ${outgoing.length} continuaciones directas curadas.`;
    if (updateHistory) updateUrl(subjectId);
  };

  const initialize = async () => {
    try {
      const [curriculumResponse, graphResponse] = await Promise.all([
        fetch(curriculumUrl),
        fetch(graphUrl)
      ]);
      if (!curriculumResponse.ok || !graphResponse.ok) throw new Error("No se pudieron cargar los datos curriculares.");

      const [curriculum, graph] = await Promise.all([
        curriculumResponse.json(),
        graphResponse.json()
      ]);

      state.orderedSubjects = flattenSubjects(curriculum);
      state.subjects = new Map(state.orderedSubjects.map((subject) => [subject.id, subject]));
      for (const edge of graph.edges || []) {
        addEdge(state.outgoing, edge.from, edge);
        addEdge(state.incoming, edge.to, edge);
      }

      populateSelect();
      const requested = new URL(window.location.href).searchParams.get("subject") || "";
      if (requested && state.subjects.has(requested)) {
        elements.select.value = requested;
        renderSubject(requested, false);
      } else {
        renderSubject("", false);
      }

      elements.select.addEventListener("change", () => renderSubject(elements.select.value));
      elements.search?.addEventListener("input", () => populateSelect(elements.search.value));
    } catch (error) {
      elements.status.textContent = error instanceof Error ? error.message : "No se pudo cargar el mapa curricular.";
      elements.status.classList.add("dependency-error");
    }
  };

  initialize();
})();
