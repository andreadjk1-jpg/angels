/* Nome di 42 lettere: tracciamento diretto e scelta esplicita del seme lunare. */
function createDivineNamesUI(orthography, spec) {
  'use strict';
  let trace = null;
  let lunarSeed = null;
  const entries = [spec.full, ...spec.groups];
  const escape = value => String(value).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
  function panelHTML(order) {
    return `<details data-divine42-panel="${order}" style="margin:12px 0; padding:10px; border:1px solid var(--gold); border-radius:8px; min-width:0;">
      <summary style="cursor:pointer; color:var(--gold-bright); font-weight:bold;">Nome divino di 42 lettere · sette gruppi di sei</summary>
      <p>Forma acrostica di Ana Bekoach. Tracciamento sulla tavola ${order}×${order}: convenzione del progetto.</p>
      ${entries.map(item=>`<div data-divine42-entry="${item.id}" style="padding:8px 0; border-top:1px solid var(--border-gold); overflow-wrap:anywhere;">
        <strong>${item.label}</strong> · ${item.letters} lettere · gematria ${item.gematria}<br/>
        <bdi dir="rtl" class="hebrew">${item.hebrew}</bdi><br/>
        <span style="font-size:0.82rem;">${escape(item.latin)}</span>
        <div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:6px;">
          <button type="button" data-divine42-action="trace" data-divine42-id="${item.id}">Traccia sulla tavola ${order}×${order}</button>
          <button type="button" data-divine42-action="lunar-seed" data-divine42-id="${item.id}">Usa per la derivazione lunare</button>
        </div>
      </div>`).join('')}
      <p>Il tracciamento diretto conserva le lettere del Nome. La derivazione lunare applica la sostituzione di Agrippa III.27 e il suffisso scelto nel pannello lunare.</p>
      <p><a href="#divineNames42">Acrostico, gematrie e fonte del Nome</a></p>
    </details>`;
  }
  document.addEventListener('click', event => {
    const button = event.target.closest('[data-divine42-action]');
    if (!button) return;
    const panel = button.closest('[data-divine42-panel]');
    const item = entries.find(entry => entry.id === button.dataset.divine42Id);
    if (!panel || !item) return;
    const order = Number(panel.dataset.divine42Panel);
    if (button.dataset.divine42Action === 'trace' && trace) {
      trace(order, `Nome divino · Ana Bekoach · ${item.label}`, item.label, item.hebrew, item.gematria);
    } else if (button.dataset.divine42Action === 'lunar-seed' && lunarSeed) {
      lunarSeed(order, item.hebrew);
    }
  });
  return {spec, panelHTML, setTraceHandler:handler=>{trace=handler;}, setLunarSeedHandler:handler=>{lunarSeed=handler;}};
}
