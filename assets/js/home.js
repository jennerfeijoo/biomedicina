(() => {
  "use strict";

  const normalize = (value) =>
    String(value || "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLocaleLowerCase("es")
      .trim();

  const state = { courses: [], tracks: [], research: [] };
  const areaTitles = {
    "ciencias-basicas": "Ciencias Básicas",
    "biologicas-medicas": "Biológicas y Médicas",
    "ingenieria-biomedica": "Ingeniería Biomédica Aplicada",
    "gestion-etica-comunicacion": "Gestión, Ética y Comunicación",
  };

  function flattenCurriculum(payload) {
    return payload.areas.flatMap((area) =>
      area.subjects.map((subject) => ({ ...subject, area_id: area.id, area_title: area.title }))
    );
  }

  function courseSearchText(course) {
    return normalize([
      course.title,
      course.description,
      course.biomedical_connection,
      course.area_title,
      ...(course.track_titles || []),
      ...(course.key_concepts || []),
      ...(course.modules || []),
    ].join(" "));
  }

  function annotateTracks(courses, tracks) {
    const membership = new Map();
    tracks.forEach((track) => {
      track.subjects.forEach((subjectId) => {
        const list = membership.get(subjectId) || [];
        list.push({ id: track.id, title: track.title });
        membership.set(subjectId, list);
      });
    });

    return courses.map((course) => {
      const related = membership.get(course.id) || [];
      return {
        ...course,
        track_ids: related.map((item) => item.id),
        track_titles: related.map((item) => item.title),
      };
    });
  }

  function statusLabel(status) {
    const labels = {
      placeholder: "Contenido pendiente",
      draft: "Borrador inicial",
      review: "Revisión pendiente",
      generated: "Revisión experta pendiente",
      complete: "Revisado por especialista",
    };
    return labels[status] || "Estado editorial";
  }

  function createResultCard(course) {
    const card = document.createElement("a");
    card.className = "home-result-card";
    card.href = course.path;

    const meta = document.createElement("div");
    meta.className = "result-meta";

    const area = document.createElement("span");
    area.className = "result-chip";
    area.textContent = course.area_title;
    meta.append(area);

    if (course.status === "placeholder") {
      const pending = document.createElement("span");
      pending.className = "result-chip pending";
      pending.textContent = statusLabel(course.status);
      meta.append(pending);
    } else if (course.track_titles?.length) {
      const track = document.createElement("span");
      track.className = "result-chip";
      track.textContent = course.track_titles[0];
      meta.append(track);
    }

    const title = document.createElement("h3");
    title.textContent = course.title;

    const description = document.createElement("p");
    description.textContent = course.description;

    const action = document.createElement("span");
    action.className = "result-action";
    action.textContent = "Abrir asignatura →";

    card.append(meta, title, description, action);
    return card;
  }

  function updateCatalogLink(link, query, area, track) {
    const url = new URL("catalogo/index.html", window.location.href);
    if (query) url.searchParams.set("q", query);
    if (area) url.searchParams.set("area", area);
    if (track) url.searchParams.set("track", track);
    link.href = url;
  }

  function initExplorer() {
    const root = document.querySelector("[data-home-explorer]");
    if (!root) return;

    const search = root.querySelector("[data-home-search]");
    const area = root.querySelector("[data-home-area]");
    const track = root.querySelector("[data-home-track]");
    const reset = root.querySelector("[data-home-reset]");
    const results = root.querySelector("[data-home-results]");
    const status = root.querySelector("[data-home-status]");
    const fullCatalog = root.querySelector("[data-home-catalog-link]");

    state.tracks.forEach((item) => {
      const option = document.createElement("option");
      option.value = item.id;
      option.textContent = item.title;
      track.append(option);
    });

    const apply = () => {
      const rawQuery = search.value.trim();
      const queryTokens = normalize(rawQuery).split(/\s+/).filter(Boolean);
      const selectedArea = area.value;
      const selectedTrack = track.value;
      const hasFilters = Boolean(queryTokens.length || selectedArea || selectedTrack);

      updateCatalogLink(fullCatalog, rawQuery, selectedArea, selectedTrack);

      if (!hasFilters) {
        results.replaceChildren();
        status.textContent = "Introduce un término o selecciona un filtro.";
        return;
      }

      const matches = state.courses
        .filter((course) => {
          const text = courseSearchText(course);
          return (
            (!queryTokens.length || queryTokens.every((token) => text.includes(token))) &&
            (!selectedArea || course.area_id === selectedArea) &&
            (!selectedTrack || course.track_ids.includes(selectedTrack))
          );
        })
        .sort((left, right) => left.title.localeCompare(right.title, "es"));

      status.textContent = `${matches.length} asignaturas coinciden. Se muestran hasta 6 resultados.`;
      results.replaceChildren(...matches.slice(0, 6).map(createResultCard));

      if (!matches.length) {
        const empty = document.createElement("div");
        empty.className = "research-empty";
        empty.innerHTML = "<p>No hay una coincidencia directa. Prueba con un término más general o continúa en el catálogo completo.</p>";
        results.append(empty);
      }
    };

    search.addEventListener("input", apply);
    area.addEventListener("change", apply);
    track.addEventListener("change", apply);
    reset.addEventListener("click", () => {
      search.value = "";
      area.value = "";
      track.value = "";
      apply();
      search.focus();
    });

    apply();
  }

  function initRouteCounts() {
    state.tracks.forEach((track) => {
      document.querySelectorAll(`[data-track-count="${track.id}"]`).forEach((node) => {
        node.textContent = `${track.subjects.length} asignaturas`;
      });
    });
  }

  function createResearchItem(item) {
    const article = document.createElement("article");
    article.className = "research-item";

    const meta = document.createElement("div");
    meta.className = "result-meta";
    (item.subject_ids || []).slice(0, 2).forEach((subjectId) => {
      const course = state.courses.find((entry) => entry.id === subjectId);
      if (!course) return;
      const chip = document.createElement("span");
      chip.className = "result-chip";
      chip.textContent = course.title;
      meta.append(chip);
    });

    const title = document.createElement("h4");
    title.textContent = item.title;

    const summary = document.createElement("p");
    summary.textContent = item.summary;

    const details = document.createElement("p");
    details.textContent = [item.publication_date, item.study_design, item.evidence_type]
      .filter(Boolean)
      .join(" · ");

    article.append(meta, title, summary, details);
    return article;
  }

  function initResearch() {
    const container = document.querySelector("[data-research-items]");
    const empty = document.querySelector("[data-research-empty]");
    const count = document.querySelector("[data-research-count]");
    if (!container || !empty || !count) return;

    const items = [...state.research].sort((left, right) =>
      String(right.publication_date || "").localeCompare(String(left.publication_date || ""))
    );

    count.textContent = items.length ? `${items.length} artículos` : "Catálogo preparado";
    if (!items.length) {
      empty.hidden = false;
      return;
    }

    empty.hidden = true;
    container.replaceChildren(...items.slice(0, 3).map(createResearchItem));
  }

  function initNavigation() {
    const toggle = document.querySelector("[data-nav-toggle]");
    const menu = document.querySelector("[data-nav-menu]");
    if (!toggle || !menu) return;

    toggle.addEventListener("click", () => {
      const open = menu.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });

    menu.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        menu.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  function initReveals() {
    const items = document.querySelectorAll(".reveal");
    if (!("IntersectionObserver" in window)) {
      items.forEach((item) => item.classList.add("is-visible"));
      return;
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.1 });

    items.forEach((item) => observer.observe(item));
  }

  async function loadData() {
    const responses = await Promise.all([
      fetch("data/citonauta_curriculum.json", { cache: "no-store" }),
      fetch("data/provisional_subjects.json", { cache: "no-store" }),
      fetch("data/tracks.json", { cache: "no-store" }),
      fetch("data/research_catalog.json", { cache: "no-store" }),
    ]);

    for (const response of responses) {
      if (!response.ok) throw new Error(`No se pudo cargar ${response.url}: HTTP ${response.status}`);
    }

    const [curriculum, provisional, tracksPayload, researchPayload] = await Promise.all(
      responses.map((response) => response.json())
    );

    const coreCourses = flattenCurriculum(curriculum);
    const provisionalCourses = provisional.subjects.map((subject) => ({
      ...subject,
      area_title: subject.area_title || areaTitles[subject.area_id],
    }));

    state.tracks = tracksPayload.tracks;
    state.courses = annotateTracks([...coreCourses, ...provisionalCourses], state.tracks);
    state.research = researchPayload.items || [];
  }

  async function boot() {
    initNavigation();
    initReveals();

    try {
      await loadData();
      initExplorer();
      initRouteCounts();
      initResearch();
    } catch (error) {
      console.error("No se pudo iniciar la portada interactiva.", error);
      const status = document.querySelector("[data-home-status]");
      if (status) status.textContent = "La búsqueda interactiva no está disponible. El catálogo completo sigue accesible.";
    }
  }

  boot();
})();
