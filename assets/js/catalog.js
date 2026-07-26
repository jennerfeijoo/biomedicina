(() => {
  "use strict";

  const normalize = (value) =>
    String(value || "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLocaleLowerCase("es")
      .trim();

  const tokens = (value) => String(value || "").split(/\s+/).filter(Boolean);

  const scriptUrl = document.currentScript?.src || new URL("assets/js/catalog.js", window.location.href).href;
  const siteRoot = new URL("../../", scriptUrl);
  const provisionalDataUrl = new URL("data/provisional_subjects.json", siteRoot);
  const areaIds = [
    "ciencias-basicas",
    "biologicas-medicas",
    "ingenieria-biomedica",
    "gestion-etica-comunicacion",
  ];

  function currentArea() {
    const segments = window.location.pathname.split("/").filter(Boolean);
    return areaIds.find((areaId) => segments.includes(areaId)) || "";
  }

  function buildCourseCard(subject) {
    const card = document.createElement("a");
    card.className = "link-card course-card";
    card.href = new URL(subject.path, siteRoot).href;
    card.dataset.courseCard = "";
    card.dataset.subject = subject.id;
    card.dataset.area = subject.area_id;
    card.dataset.tracks = "";
    card.dataset.search = [
      subject.title,
      subject.description,
      subject.biomedical_connection,
      subject.area_title,
      "Contenido pendiente",
    ].join(" ");

    const title = document.createElement("strong");
    title.textContent = subject.title;

    const description = document.createElement("p");
    description.textContent = subject.description;

    const meta = document.createElement("span");
    meta.className = "course-card-meta";

    const areaChip = document.createElement("span");
    areaChip.className = "catalog-chip";
    areaChip.textContent = subject.area_title;

    const statusChip = document.createElement("span");
    statusChip.className = "catalog-chip";
    statusChip.textContent = "Contenido pendiente";

    meta.append(areaChip, statusChip);
    card.append(title, description, meta);
    return card;
  }

  function findSubjectCountField() {
    const metaRows = Array.from(document.querySelectorAll(".course-meta > div"));
    const subjectRow = metaRows.find(
      (row) => normalize(row.querySelector("dt")?.textContent) === "asignaturas"
    );
    return subjectRow?.querySelector("dd") || null;
  }

  function updatePublicCounts(grid) {
    const count = grid.querySelectorAll("[data-course-card]").length;
    const countField = findSubjectCountField();
    if (countField) countField.textContent = String(count);

    const isCatalog = window.location.pathname.split("/").includes("catalogo");
    if (!isCatalog) return;

    const intro = document.querySelector(".page-intro");
    const introDescription = intro
      ? Array.from(intro.children).find(
          (element) => element.tagName === "P" && !element.classList.contains("eyebrow")
        )
      : null;
    if (introDescription) {
      introDescription.textContent = `Explora las ${count} asignaturas mediante búsqueda, áreas y rutas interdisciplinarias. Ninguna ruta fija plazos ni obliga a completar las asignaturas en un orden único.`;
    }

    const metaDescription = document.querySelector('meta[name="description"]');
    if (metaDescription) {
      metaDescription.content = `Busca y explora las ${count} asignaturas abiertas de CitoNauta por área y ruta interdisciplinaria.`;
    }
  }

  async function injectProvisionalSubjects() {
    const grid = document.querySelector("[data-course-grid]");
    if (!grid) return;

    try {
      const response = await fetch(provisionalDataUrl, { cache: "no-store" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const payload = await response.json();
      const area = currentArea();
      const existing = new Set(
        Array.from(grid.querySelectorAll("[data-course-card]"), (card) => card.dataset.subject)
      );

      payload.subjects
        .filter((subject) => !area || subject.area_id === area)
        .filter((subject) => !existing.has(subject.id))
        .sort((left, right) => left.title.localeCompare(right.title, "es"))
        .forEach((subject) => grid.append(buildCourseCard(subject)));

      const cards = Array.from(grid.querySelectorAll("[data-course-card]"));
      cards
        .sort((left, right) =>
          left.querySelector("strong").textContent.localeCompare(
            right.querySelector("strong").textContent,
            "es"
          )
        )
        .forEach((card) => grid.append(card));

      updatePublicCounts(grid);
    } catch (error) {
      console.error("No se pudieron cargar las asignaturas provisionales.", error);
    }
  }

  function initCatalog(root) {
    const cards = Array.from(document.querySelectorAll("[data-course-card]"));
    const search = root.querySelector("[data-course-search]");
    const area = root.querySelector("[data-area-filter]");
    const track = root.querySelector("[data-track-filter]");
    const reset = root.querySelector("[data-catalog-reset]");
    const count = root.querySelector("[data-result-count]");
    const empty = document.querySelector("[data-empty-state]");

    if (!cards.length || !search || !track || !count) return;

    const params = new URLSearchParams(window.location.search);
    if (params.has("q")) search.value = params.get("q") || "";
    if (area && params.has("area")) area.value = params.get("area") || "";
    if (params.has("track")) track.value = params.get("track") || "";

    const apply = () => {
      const query = normalize(search.value);
      const selectedArea = area ? area.value : "";
      const selectedTrack = track.value;
      let visible = 0;

      cards.forEach((card) => {
        const matchesSearch = !query || normalize(card.dataset.search).includes(query);
        const matchesArea = !selectedArea || card.dataset.area === selectedArea;
        const matchesTrack = !selectedTrack || tokens(card.dataset.tracks).includes(selectedTrack);
        const show = matchesSearch && matchesArea && matchesTrack;
        card.hidden = !show;
        if (show) visible += 1;
      });

      count.textContent = String(visible);
      if (empty) empty.hidden = visible !== 0;

      const next = new URL(window.location.href);
      const values = { q: search.value.trim(), area: selectedArea, track: selectedTrack };
      Object.entries(values).forEach(([key, value]) => {
        if (value) next.searchParams.set(key, value);
        else next.searchParams.delete(key);
      });
      window.history.replaceState({}, "", next);
    };

    search.addEventListener("input", apply);
    if (area) area.addEventListener("change", apply);
    track.addEventListener("change", apply);
    reset?.addEventListener("click", () => {
      search.value = "";
      if (area) area.value = "";
      track.value = "";
      apply();
      search.focus();
    });

    apply();
  }

  async function boot() {
    await injectProvisionalSubjects();
    document.querySelectorAll("[data-catalog]").forEach(initCatalog);
  }

  boot();
})();
