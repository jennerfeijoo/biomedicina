/* Shared by the browser and the corpus audit. Banks retain exact source pointers. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.CitoAssessment = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const VERSION = '1.1';
  const marker = 'Concepto de la unidad que debe definirse mediante entidades observables';
  const norm = value => String(value || '').normalize('NFKC').toLocaleLowerCase('es').replace(/\s+/g, ' ').trim();
  const text = value => typeof value === 'string' ? value.trim() : '';
  const array = value => Array.isArray(value) ? value : value ? [value] : [];
  function buildBank(unit) {
    const items = [], seen = new Set();
    const blocked = JSON.stringify(unit).includes(marker);
    const source = `data/generated_units/${unit.subject_id}/unit-${String(unit.unit).padStart(2, '0')}.json`;
    function add(kind, i, prompt, answer, explanation, extra = {}) {
      if (!text(prompt) || !text(answer) || seen.has(norm(prompt))) return;
      seen.add(norm(prompt));
      items.push({id: `${unit.subject_id}:U${unit.unit}:${kind}:${i}`, unit: unit.unit,
        unitTitle: unit.title, kind, prompt, answer, explanation: explanation || '',
        source, pointer: `/${kind}/${i}`, review: 'pending', ...extra});
    }
    (unit.self_assessment || []).forEach((q, i) => add('self_assessment', i, q.question, q.answer,
      [q.reasoning, q.common_error && `Error frecuente: ${q.common_error}`].filter(Boolean).join('\n'),
      {objectiveIds: Array.isArray(q.objective_ids) ? q.objective_ids.filter(x => typeof x === 'string') : []}));
    (unit.common_errors || []).forEach((q, i) => add('common_errors', i,
      `Identifica y corrige el error de esta afirmación o actuación: «${q.error}»`, q.correction || q.recovery,
      'Justifica la corrección usando el mecanismo, supuesto o límite que estudiaste.'));
    (unit.worked_examples || []).forEach((q, i) => add('worked_examples', i,
      `${q.title}\n${q.scenario || q.problem || ""}\nResuelve o interpreta el caso y explicita sus limitaciones.`,
      [q.answer || q.result || q.solution || q.conclusion, q.interpretation].filter(Boolean).join('\n'), [...array(q.reasoning_steps || q.reasoning), ...array(q.limitations).map(x => `Límite: ${x}`)].join('\n')));
    const glossary = (unit.glossary || []).filter(q => text(q.term) && text(q.definition));
    (unit.glossary || []).forEach((q, i) => {
      if (!text(q.term) || !text(q.definition)) return;
      // Repeated definitions/terms cannot have an unambiguous matching key.
      const unique = glossary.filter(x => norm(x.definition) === norm(q.definition)).length === 1 &&
        glossary.filter(x => norm(x.term) === norm(q.term)).length === 1;
      const alternatives = glossary.filter(x => norm(x.term) !== norm(q.term) && norm(x.definition) !== norm(q.definition));
      add('glossary', i, `¿Qué término del glosario de esta unidad corresponde a esta definición?\n${q.definition}`,
        q.term, q.definition, {type: unique && alternatives.length >= 3 ? 'matching' : 'open',
          alternatives: unique ? [...new Set(alternatives.map(x => x.term))] : []});
    });
    const requiredObjectives = unit.assessment_blueprint?.enforce_objective_coverage === true ?
      (unit.assessment_blueprint.objectives || []).map(o => o.id) : [];
    return {version: VERSION, unit: unit.unit, title: unit.title, blocked, items, requiredObjectives};
  }
  function seeded(seed) {
    let h = 2166136261;
    for (const c of String(seed)) h = Math.imul(h ^ c.charCodeAt(0), 16777619);
    return function () { h += 0x6D2B79F5; let t = h; t = Math.imul(t ^ t >>> 15, t | 1);
      t ^= t + Math.imul(t ^ t >>> 7, t | 61); return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  }
  function shuffle(items, random) {
    const copy = [...items];
    for (let i = copy.length - 1; i > 0; i--) { const j = Math.floor(random() * (i + 1)); [copy[i], copy[j]] = [copy[j], copy[i]]; }
    return copy;
  }
  function select(banks, count, seed) {
    if (!banks.length || banks.some(b => b.blocked)) throw new Error('Hay unidades con contenido de plantilla: el examen está pendiente de reescritura.');
    if (!Number.isInteger(count) || count < banks.length) throw new Error('El tamaño no permite representar todas las unidades.');
    const random = seeded(seed), chosen = [], used = new Set(), prompts = new Set();
    const grouped = shuffle(banks, random).map(b => ({unit: b.unit, items: shuffle(b.items, random), requiredObjectives: b.requiredObjectives || []}));
    let glossaryCount = 0;
    function take(group, kind, objective) {
      if (chosen.length >= count) return false;
      const q = group.items.find(q => (!kind || q.kind === kind) && (!objective || q.objectiveIds?.includes(objective)) && !used.has(q.id) && !prompts.has(norm(q.prompt)) &&
        (q.kind !== 'glossary' || glossaryCount < Math.floor(count * .4)));
      if (!q) return false;
      chosen.push(q); used.add(q.id); prompts.add(norm(q.prompt)); if (q.kind === 'glossary') glossaryCount++;
      return true;
    }
    // Opt-in editorial blueprints reserve every mapped objective before random fill.
    // Mapping is editorial evidence, not psychometric validation or mastery.
    for (const group of grouped) {
      if (group.requiredObjectives.length) {
        for (const objective of group.requiredObjectives) {
          if (chosen.some(q => q.unit === group.unit && q.objectiveIds?.includes(objective))) continue;
          if (!take(group, 'self_assessment', objective)) throw new Error(`No se puede cubrir el objetivo ${objective} con el banco y tamaño elegidos.`);
        }
      } else if (!take(group, 'self_assessment') && !take(group)) throw new Error(`Banco insuficiente en unidad ${group.unit}.`);
    }
    for (const kind of ['common_errors', 'worked_examples']) {
      for (const group of grouped) if (chosen.length < count) take(group, kind);
    }
    while (chosen.length < count) {
      let progress = false;
      // Fill the least represented units first, without replacing exhausted units silently.
      const ordered = [...grouped].sort((a,b) => chosen.filter(q=>q.unit===a.unit).length - chosen.filter(q=>q.unit===b.unit).length);
      for (const group of ordered) { if (chosen.length === count) break; if (take(group)) progress = true; }
      if (!progress) throw new Error(`Solo hay ${chosen.length} preguntas distintas con la distribución exigida; se necesitan ${count}.`);
    }
    return shuffle(chosen, random).map(q => ({...q, options: q.type === 'matching' ?
      shuffle([q.answer, ...shuffle(q.alternatives, random).slice(0,3)], random) : undefined}));
  }
  return {VERSION, buildBank, select, seeded, norm};
});
