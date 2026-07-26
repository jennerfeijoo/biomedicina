(() => {
  "use strict";

  const normalize = (value) =>
    String(value || "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLocaleLowerCase("es")
      .trim();

  const tokens = (value) => String(value || "").split(/\s+/).filter(Boolean);

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

  document.querySelectorAll("[data-catalog]").forEach(initCatalog);
})();
