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
  const statusesDataUrl = new URL("data/catalog_statuses.json", siteRoot);
  const areaIds = [
    "ciencias-basicas",
    "biologicas-medicas",
    "ingenieria-biomedica",
    "gestion-etica-comunicacion",
  ];
  const statusOptions = [
    ["", "Todos los estados"],
    ["review_pending", "Material en revisión"],
    ["reconstruction", "Requiere reconstrucción"],
    ["validated", "Revisión IA validada"],
    ["content_pending", "Material pendiente"],
  ];
  const statusLabels = {
    review_pending: "Material disponible · revisión científica pendiente",
    reconstruction: "Material disponible · plantilla detectada",
    validated: "Revisión IA validada para su alcance",
    content_pending: "Material lectivo pendiente",
  };

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

  function statusMembership(payload) {
    const dimensions = payload?.dimensions || {};
    return {
      materialAvailable: new Set(dimensions.material?.available || payload?.developed || []),
      templateDetected: new Set(dimensions.specificity?.template_detected || []),
      aiValidated: new Set(dimensions.review?.ai_review_validated || payload?.complete || []),
    };
  }

  function statusForSubject(subjectId, membership) {
    if (!membership.materialAvailable.has(subjectId)) return "content_pending";
    if (membership.aiValidated.has(subjectId)) return "validated";
    if (membership.templateDetected.has(subjectId)) return "reconstruction";
    return "review_pending";
  }

  function applyStatus(card, membership) {
    const status = statusForSubject(card.dataset.subject, membership);
    const label = statusLabels[status];
    card.dataset.status = status;
    card.dataset.search = `${card.dataset.search || ""} ${label}`.trim();

    const meta = card.querySelector(".course-card-meta");
    if (!meta) return;
    let chip = meta.querySelector("[data-status-chip]");
    if (!chip) {
      chip = document.createElement("span");
      chip.className = "catalog-chip";
      chip.dataset.statusChip = "";
      meta.append(chip);
    }
    chip.textContent = label;
  }

  function buildCourseCard(subject, tracksBySubject, statuses) {
    const card = document.createElement("a");
    card.className = "link-card course-card";
    card.href = new URL(subject.path, siteRoot).href;
    card.dataset.courseCard = "";
    card.dataset.subject = subject.id;
    card.dataset.area = subject.area_id;
    card.dataset.tracks = (tracksBySubject.get(subject.id) || []).join(" ");
    card.dataset.search = [
      subject.title,
      subject.description,
      subject.biomedical_connection,
      subject.area_title,
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
    meta.append(areaChip);
    card.append(title, description, meta);
    applyStatus(card, statuses);
    return card;
  }

  function populateTrackSelect(root, tracks) {
    const select = root.querySelector("[data-track-filter]");
    if (!select) return;
    const selected = new URLSearchParams(window.location.search).get("track") || "";
    select.replaceChildren(new Option("Todas las rutas", ""));
    tracks.forEach((track) => select.append(new Option(track.title, track.id)));
    if (selected && tracks.some((track) => track.id === selected)) select.value = selected;
  }

  function ensureStatusSelect(root) {
    let select = root.querySelector("[data-status-filter]");
    if (select) return select;
    const controls = root.querySelector(".catalog-controls");
    const reset = root.querySelector("[data-catalog-reset]");
    if (!controls) return null;

    const field = document.createElement("label");
    field.className = "catalog-field";
    const label = document.createElement("span");
    label.textContent = "Estado editorial";
    select = document.createElement("select");
    select.dataset.statusFilter = "";
    statusOptions.forEach(([value, text]) => select.append(new Option(text, value)));
    field.append(label, select);
    controls.insertBefore(field, reset || null);
    return select;
  }

  function ensureStatusSummary(root) {
    const summary = root.querySelector(".catalog-summary");
    if (!summary) return null;
    let detail = summary.querySelector("[data-status-summary]");
    if (!detail) {
      detail = document.createElement("span");
      detail.dataset.statusSummary = "";
      summary.append(document.createTextNode(" "), detail);
    }
    return detail;
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
  }

  async function prepareCatalog(tracks, provisionalSubjects, statuses) {
    const grid = document.querySelector("[data-course-grid]");
    if (!grid) return;
    const tracksBySubject = trackMembership(tracks);
    const area = currentArea();
    const existing = new Set(
      Array.from(grid.querySelectorAll("[data-course-card]"), (card) => card.dataset.subject)
    );

    provisionalSubjects
      .filter((subject) => !area || subject.area_id === area)
      .filter((subject) => !existing.has(subject.id))
      .sort((left, right) => left.title.localeCompare(right.title, "es"))
      .forEach((subject) => grid.append(buildCourseCard(subject, tracksBySubject, statuses)));

    grid.querySelectorAll("[data-course-card]").forEach((card) => {
      card.dataset.tracks = (tracksBySubject.get(card.dataset.subject) || []).join(" ");
      applyStatus(card, statuses);
    });

    Array.from(grid.querySelectorAll("[data-course-card]"))
      .sort((left, right) =>
        left.querySelector("strong").textContent.localeCompare(
          right.querySelector("strong").textContent,
          "es"
        )
      )
      .forEach((card) => grid.append(card));

    document.querySelectorAll("[data-catalog]").forEach((root) => {
      populateTrackSelect(root, tracks);
      ensureStatusSelect(root);
      ensureStatusSummary(root);
    });
    renderTrackGrid(tracks);
    updatePublicCounts(grid, tracks);
  }

  function initCatalog(root) {
    const cards = Array.from(document.querySelectorAll("[data-course-card]"));
    const search = root.querySelector("[data-course-search]");
    const area = root.querySelector("[data-area-filter]");
    const track = root.querySelector("[data-track-filter]");
    const status = ensureStatusSelect(root);
    const reset = root.querySelector("[data-catalog-reset]");
    const count = root.querySelector("[data-result-count]");
    const statusSummary = ensureStatusSummary(root);
    const empty = document.querySelector("[data-empty-state]");
    if (!cards.length || !search || !track || !status || !count) return;

    const params = new URLSearchParams(window.location.search);
    if (params.has("q")) search.value = params.get("q") || "";
    if (area && params.has("area")) area.value = params.get("area") || "";
    if (params.has("track")) track.value = params.get("track") || "";
    if (params.has("status")) status.value = params.get("status") || "";

    const apply = () => {
      const queryTokens = normalize(search.value).split(/\s+/).filter(Boolean);
      const selectedArea = area ? area.value : "";
      const selectedTrack = track.value;
      const selectedStatus = status.value;
      let visible = 0;
      let reconstructionVisible = 0;
      let validatedVisible = 0;

      cards.forEach((card) => {
        const searchable = normalize(card.dataset.search);
        const matchesSearch =
          !queryTokens.length || queryTokens.every((token) => searchable.includes(token));
        const matchesArea = !selectedArea || card.dataset.area === selectedArea;
        const matchesTrack = !selectedTrack || tokens(card.dataset.tracks).includes(selectedTrack);
        const matchesStatus = !selectedStatus || card.dataset.status === selectedStatus;
        const show = matchesSearch && matchesArea && matchesTrack && matchesStatus;
        card.hidden = !show;
        if (show) {
          visible += 1;
          if (card.dataset.status === "reconstruction") reconstructionVisible += 1;
          if (card.dataset.status === "validated") validatedVisible += 1;
        }
      });

      count.textContent = String(visible);
      if (statusSummary) {
        statusSummary.textContent =
          `(${reconstructionVisible} requieren reconstrucción; ${validatedVisible} con revisión IA validada).`;
      }
      if (empty) empty.hidden = visible !== 0;

      const next = new URL(window.location.href);
      const values = {
        q: search.value.trim(),
        area: selectedArea,
        track: selectedTrack,
        status: selectedStatus,
      };
      Object.entries(values).forEach(([key, value]) => {
        if (value) next.searchParams.set(key, value);
        else next.searchParams.delete(key);
      });
      window.history.replaceState({}, "", next);
    };

    search.addEventListener("input", apply);
    if (area) area.addEventListener("change", apply);
    track.addEventListener("change", apply);
    status.addEventListener("change", apply);
    reset?.addEventListener("click", () => {
      search.value = "";
      if (area) area.value = "";
      track.value = "";
      status.value = "";
      apply();
      search.focus();
    });
    apply();
  }

  async function boot() {
    try {
      const [provisionalResponse, tracksResponse, statusesResponse] = await Promise.all([
        fetch(provisionalDataUrl, { cache: "no-store" }),
        fetch(tracksDataUrl, { cache: "no-store" }),
        fetch(statusesDataUrl, { cache: "no-store" }),
      ]);
      if (!provisionalResponse.ok || !tracksResponse.ok || !statusesResponse.ok) {
        throw new Error("No se pudieron cargar los datos del catálogo.");
      }
      const [provisionalPayload, tracksPayload, statusesPayload] = await Promise.all([
        provisionalResponse.json(),
        tracksResponse.json(),
        statusesResponse.json(),
      ]);
      await prepareCatalog(
        tracksPayload.tracks,
        provisionalPayload.subjects,
        statusMembership(statusesPayload)
      );
      document.querySelectorAll("[data-catalog]").forEach(initCatalog);
    } catch (error) {
      console.error("No se pudo iniciar el catálogo.", error);
      document.querySelectorAll("[data-catalog]").forEach((root) => {
        ensureStatusSelect(root);
        ensureStatusSummary(root);
        initCatalog(root);
      });
    }
  }

  boot();
})();
