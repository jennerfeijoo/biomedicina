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
  const tracksDataUrl = new URL("data/tracks.json", siteRoot);
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

  function trackMembership(tracks) {
    const membership = new Map();
    tracks.forEach((track) => {
      track.subjects.forEach((subjectId) => {
        const list = membership.get(subjectId) || [];
        list.push(track.id);
        membership.set(subjectId, list);
      });
    });
    return membership;
  }

  function buildCourseCard(subject, membership) {
    const card = document.createElement("a");
    card.className = "link-card course-card";
    card.href = new URL(subject.path, siteRoot).href;
    card.dataset.courseCard = "";
    card.dataset.subject = subject.id;
    card.dataset.area = subject.area_id;
    card.dataset.tracks = (membership.get(subject.id) || []).join(" ");
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

  function assignTrackMembership(grid, membership) {
    grid.querySelectorAll("[data-course-card]").forEach((card) => {
      card.dataset.tracks = (membership.get(card.dataset.subject) || []).join(" ");
    });
  }

  function populateTrackSelect(root, tracks) {
    const select = root.querySelector("[data-track-filter]");
    if (!select) return;

    const selected = new URLSearchParams(window.location.search).get("track") || "";
    select.replaceChildren(new Option("Todas las rutas", ""));

    tracks.forEach((track) => {
      select.append(new Option(track.title, track.id));
    });

    if (selected && tracks.some((track) => track.id === selected)) {
      select.value = selected;
    }
  }

  function renderTrackGrid(tracks) {
    const grid = document.querySelector(".track-grid");
    if (!grid || !window.location.pathname.split("/").includes("catalogo")) return;

    const cards = tracks.map((track) => {
      const card = document.createElement("a");
      card.className = "track-card";
      card.href = `?track=${encodeURIComponent(track.id)}#asignaturas`;

      const title = document.createElement("strong");
      title.textContent = track.title;

      const description = document.createElement("p");
      description.textContent = track.description;

      const count = document.createElement("span");
      count.textContent = `${track.subjects.length} asignaturas relacionadas →`;

      card.append(title, description, count);
      return card;
    });

    grid.replaceChildren(...cards);
  }

  function findMetaField(label) {
    const rows = Array.from(document.querySelectorAll(".course-meta > div"));
    const row = rows.find((item) => normalize(item.querySelector("dt")?.textContent) === label);
    return row?.querySelector("dd") || null;
  }

  function updatePublicCounts(grid, tracks) {
    const count = grid.querySelectorAll("[data-course-card]").length;
    const countField = findMetaField("asignaturas");
    const routeCountField = findMetaField("rutas");
    if (countField) countField.textContent = String(count);
    if (routeCountField) routeCountField.textContent = String(tracks.length);

    if (!window.location.pathname.split("/").includes("catalogo")) return;

    const intro = document.querySelector(".page-intro");
    const introDescription = intro
      ? Array.from(intro.children).find(
          (element) => element.tagName === "P" && !element.classList.contains("eyebrow")
        )
      : null;

    if (introDescription) {
      introDescription.textContent = `Explora las ${count} asignaturas mediante búsqueda, áreas y rutas interdisciplinarias. Las rutas conectan problemas y métodos; no prescriben una duración ni un orden único.`;
    }

    const metaDescription = document.querySelector('meta[name="description"]');
    if (metaDescription) {
      metaDescription.content = `Busca y explora las ${count} asignaturas abiertas de CitoNauta por área y ruta interdisciplinaria.`;
    }
  }

  async function prepareCatalog(tracks, provisionalSubjects) {
    const grid = document.querySelector("[data-course-grid]");
    if (!grid) return;

    const membership = trackMembership(tracks);
    const area = currentArea();
    const existing = new Set(
      Array.from(grid.querySelectorAll("[data-course-card]"), (card) => card.dataset.subject)
    );

    provisionalSubjects
      .filter((subject) => !area || subject.area_id === area)
      .filter((subject) => !existing.has(subject.id))
      .sort((left, right) => left.title.localeCompare(right.title, "es"))
      .forEach((subject) => grid.append(buildCourseCard(subject, membership)));

    assignTrackMembership(grid, membership);

    const cards = Array.from(grid.querySelectorAll("[data-course-card]"));
    cards
      .sort((left, right) =>
        left.querySelector("strong").textContent.localeCompare(
          right.querySelector("strong").textContent,
          "es"
        )
      )
      .forEach((card) => grid.append(card));

    document.querySelectorAll("[data-catalog]").forEach((root) => populateTrackSelect(root, tracks));
    renderTrackGrid(tracks);
    updatePublicCounts(grid, tracks);
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
      const queryTokens = normalize(search.value).split(/\s+/).filter(Boolean);
      const selectedArea = area ? area.value : "";
      const selectedTrack = track.value;
      let visible = 0;

      cards.forEach((card) => {
        const searchable = normalize(card.dataset.search);
        const matchesSearch =
          !queryTokens.length || queryTokens.every((token) => searchable.includes(token));
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
    try {
      const [provisionalResponse, tracksResponse] = await Promise.all([
        fetch(provisionalDataUrl, { cache: "no-store" }),
        fetch(tracksDataUrl, { cache: "no-store" }),
      ]);

      if (!provisionalResponse.ok || !tracksResponse.ok) {
        throw new Error("No se pudieron cargar los datos del catálogo.");
      }

      const [provisionalPayload, tracksPayload] = await Promise.all([
        provisionalResponse.json(),
        tracksResponse.json(),
      ]);

      await prepareCatalog(tracksPayload.tracks, provisionalPayload.subjects);
      document.querySelectorAll("[data-catalog]").forEach(initCatalog);
    } catch (error) {
      console.error("No se pudo iniciar el catálogo.", error);
      document.querySelectorAll("[data-catalog]").forEach(initCatalog);
    }
  }

  boot();
})();
