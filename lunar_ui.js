/* Componenti condivisi: stato lunare e generazione/tracciamento nelle tavole. */
function createLunarUI(engine, orthography) {
  'use strict';
  let state = null;
  let trace = null;
  const generated = new WeakMap();
  const escape = text => String(text).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
  const degree = value => Number(value).toFixed(4) + '°';
  function position(value) {
    const signs = ['Ariete','Toro','Gemelli','Cancro','Leone','Vergine','Bilancia','Scorpione','Sagittario','Capricorno','Acquario','Pesci'];
    return degree(value % 30) + ' ' + signs[Math.floor(value / 30) % 12];
  }
  function stateHTML(value) {
    const phase = value.phaseAngle * Math.PI / 180;
    const x = 70 + 42 * Math.sin(phase), y = 70 - 42 * Math.cos(phase);
    return `<div class="lunar-state" style="margin:14px 0; padding:14px; border:1px solid var(--cyan); border-radius:10px;">
      <h3 style="color:var(--cyan); margin-top:0;">Luna: posizione, fase e mansione</h3>
      <p><strong>Istante UTC:</strong> <time data-lunar-utc>${escape(value.utc)}</time> · <strong>Riferimento:</strong> ${escape(value.frame)}</p>
      <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:12px;">
        <div><strong data-lunar-phase>${escape(value.phaseName)}</strong><br/>
          Illuminazione: <span data-lunar-illumination>${(value.illumination * 100).toFixed(2)}%</span><br/>
          Angolo Luna–Sole: <span data-lunar-angle>${degree(value.phaseAngle)}</span>
          <svg viewBox="0 0 140 140" width="120" height="120" role="img" aria-label="Angolo della Luna rispetto al Sole">
            <circle cx="70" cy="70" r="42" fill="none" stroke="#9aa5b1"/>
            <circle cx="70" cy="28" r="6" fill="#f5d76e"/>
            <line x1="70" y1="70" x2="${x}" y2="${y}" stroke="#48c9b0"/>
            <circle cx="${x}" cy="${y}" r="5" fill="#eceff4"/>
            <text x="70" y="16" text-anchor="middle" fill="#f5d76e" font-size="10">0° · Sole</text>
            <text x="70" y="132" text-anchor="middle" fill="#eceff4" font-size="10">180° · Luna piena</text>
          </svg>
        </div>
        <div><strong>Posizioni geocentriche</strong><br/>
          Luna: <span data-lunar-longitude>${degree(value.moonLongitude)}</span> · ${position(value.moonLongitude)}<br/>
          Sole: ${degree(value.sunLongitude)} · ${position(value.sunLongitude)}<br/>
          Latitudine lunare: ${degree(value.moonLatitude)}<br/>Distanza: ${Math.round(value.distanceKm).toLocaleString('it-IT')} km
        </div>
        <div><strong data-lunar-mansion>Mansione ${value.mansion.num}: ${escape(value.mansion.name)}</strong><br/>
          Intervallo: ${degree(value.mansion.start)} ≤ λ &lt; ${degree(value.mansion.end)}<br/>
          Angelo dell’archivio: <strong>${escape(value.mansion.angel)}</strong> (<span class="hebrew">${value.mansion.hebrew}</span>)<br/>
          Gematria: ${orthography.gematria(value.mansion.hebrew)}<br/>
          <small>360° divisi in 28 settori; la fase usa il rapporto Luna–Sole.</small>
        </div>
      </div>
      <p style="font-size:0.8rem; margin-bottom:0;">Le etichette «prossimità» indicano una distanza inferiore a 0,5° dalla fase principale.
        Calcolo UTC, calendario gregoriano prolettico. Astronomy Engine 2.1.19, incorporato nella pagina.
        <a href="https://aa.usno.navy.mil/faq/moon_phases" target="_blank" rel="noopener noreferrer">Definizione delle fasi</a>.</p>
    </div>`;
  }
  function selectedMansion(panel) {
    const choice = panel.querySelector('[data-lunar-mansion-choice]').value;
    return choice === 'auto' ? (state ? state.mansion : null) : engine.spec.mansions[Number(choice) - 1];
  }
  function panelHTML(order) {
    const options = engine.spec.mansions.map(m => `<option value="${m.num}">${m.num}. ${escape(m.angel)} · ${escape(m.name)}</option>`).join('');
    return `<details data-lunar-panel="${order}" style="margin:12px 0; padding:10px; border:1px solid var(--cyan); border-radius:8px; min-width:0;">
      <summary style="cursor:pointer; color:var(--cyan); font-weight:bold;">☽ Genera e traccia i nomi lunari sulla tavola ${order}×${order}</summary>
      <p>${order === 9 ? 'Tavola lunare classica 9×9.' : 'Tracciamento su questa tavola: proiezione del progetto; la tavola lunare classica è 9×9.'}
        Derivazione dei nomi dalla colonna della Luna, Agrippa III.27.</p>
      <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:8px;">
        <label>Mansione e nome di partenza<br/><select data-lunar-mansion-choice style="max-width:100%; width:100%;">
          <option value="auto">Mansione dell’istante selezionato</option>${options}</select></label>
        <label>Nome divino o angelico alternativo<br/><input data-lunar-seed placeholder="Vuoto: angelo della mansione" style="max-width:100%; width:100%;"/></label>
        <label>Suffisso<br/><select data-lunar-suffix><option value="auto">Come nel calcolatore</option><option value="אל">El · אל</option><option value="יה">Yah · יה</option></select></label>
      </div>
      <div style="display:flex; gap:6px; flex-wrap:wrap; margin-top:8px;">
        <button type="button" data-lunar-action="generate">Genera i nove gradi</button>
        <button type="button" data-lunar-action="traditional">Traccia l’angelo della mansione</button>
        <button type="button" data-lunar-action="elim">Usa il nome divino Elim · אלים</button>
        <button type="button" data-lunar-action="export">Esporta i nomi JSON</button>
      </div>
      <p data-lunar-seed-note></p><div data-lunar-names></div>
      <details style="margin-top:8px;"><summary>Regola, lettere e fonti</summary>
        <p>Ingresso discendente della tavola planetaria, colonna della Luna: ciascuna lettera del nome è sostituita con la lettera della stessa riga sotto la Luna.
          Si aggiunge il suffisso scelto; per il grado successivo si reinserisce il nome completo precedente. Le forme finali del nome di partenza sono ricondotte alle lettere ordinarie.</p>
        <p>${escape(engine.spec.readingNote)} I nomi delle 28 mansioni restano distinti dai nomi così derivati.</p>
        <div style="overflow-x:auto;"><table style="width:100%;"><thead><tr><th>Ingresso</th><th>Colonna della Luna</th></tr></thead><tbody>
          ${Array.from(engine.spec.alphabet).map((ch,i)=>`<tr><td class="hebrew">${ch}</td><td class="hebrew">${engine.spec.moonColumn[i]}</td></tr>`).join('')}
        </tbody></table></div>
        <p><a href="${engine.spec.source}" target="_blank" rel="noopener noreferrer">Agrippa III.27</a> · <a href="${engine.spec.transcription}" target="_blank" rel="noopener noreferrer">Tavola del 1651, p. 433, trascritta riga per riga</a></p>
      </details>
    </details>`;
  }
  function refreshPanel(panel) {
    const mansion = selectedMansion(panel);
    const custom = panel.querySelector('[data-lunar-seed]').value.trim();
    const converted = custom ? orthography.convertName(custom) : null;
    const seed = custom ? converted.hebrew : mansion ? mansion.hebrew : '';
    const suffixValue = panel.querySelector('[data-lunar-suffix]').value;
    const suffix = suffixValue === 'auto' ? (state ? state.suffix : 'אל') : suffixValue;
    const note = panel.querySelector('[data-lunar-seed-note]');
    const target = panel.querySelector('[data-lunar-names]');
    panel.querySelector('[data-lunar-action="traditional"]').disabled = !mansion;
    const autoOption = panel.querySelector('[data-lunar-mansion-choice] option[value="auto"]');
    autoOption.textContent = state ? `Attuale: ${state.mansion.num}. ${state.mansion.angel}` : 'Definisci un istante valido oppure scegli una mansione';
    if (!seed) {
      generated.delete(panel);
      note.textContent = 'Scegli una mansione o inserisci la grafia ebraica del nome di partenza.';
      target.replaceChildren(); return [];
    }
    const names = engine.hierarchy(seed, suffix);
    generated.set(panel, names);
    const provenance = custom ? 'Nome specificato' : panel.querySelector('[data-lunar-mansion-choice]').value === 'auto' ? 'Angelo della mansione attuale' : 'Mansione scelta manualmente';
    note.textContent = `${provenance}: ${seed} · gematria ${orthography.gematria(seed)} · suffisso ${suffix}.` + (custom && converted.kind === 'conventional' ? ' Conversione latina convenzionale: verifica la grafia.' : '');
    target.innerHTML = `<div style="display:flex; flex-wrap:wrap; gap:6px;">${names.map((name,i)=>`<button type="button" data-lunar-action="trace" data-lunar-index="${i}" style="max-width:100%; overflow-wrap:anywhere;">
      ${name.level}. ${name.order}: <strong>${escape(name.latin)}</strong> (<span class="hebrew">${name.hebrew}</span> = ${name.gematria})</button>`).join('')}</div>
      <details style="margin-top:8px;"><summary>Passaggi della derivazione</summary>${names.map(name=>`<p><strong>${name.level}. ${name.order}</strong>: ${name.steps.map(step=>`${step.from}→${step.to}`).join(' · ')} + ${suffix} = <span class="hebrew">${name.hebrew}</span> (${name.gematria})</p>`).join('')}</details>`;
    return names;
  }
  function refreshPanels() { document.querySelectorAll('[data-lunar-panel]').forEach(refreshPanel); }
  function setState(value) {
    state = value;
    const host = document.getElementById('lunarStatePanel');
    if (host) host.innerHTML = value ? stateHTML(value) : '';
    refreshPanels();
  }
  function showError(message) {
    setState(null);
    const host = document.getElementById('lunarStatePanel');
    if (host) host.textContent = message;
  }
  document.addEventListener('change', event => {
    const panel = event.target.closest('[data-lunar-panel]');
    if (panel) refreshPanel(panel);
  });
  document.addEventListener('click', event => {
    const button = event.target.closest('[data-lunar-action]');
    if (!button) return;
    const panel = button.closest('[data-lunar-panel]');
    const order = Number(panel.dataset.lunarPanel);
    const action = button.dataset.lunarAction;
    if (action === 'elim') panel.querySelector('[data-lunar-seed]').value = 'אלים';
    const names = refreshPanel(panel);
    if (action === 'trace' && trace) {
      const name = names[Number(button.dataset.lunarIndex)];
      if (name) trace(order, `Nome lunare derivato · ${name.order} · Agrippa III.27`, name.latin, name.hebrew, name.gematria);
    }
    if (action === 'traditional' && trace) {
      const mansion = selectedMansion(panel);
      if (mansion) trace(order, `Angelo della mansione ${mansion.num} · ${mansion.name}`, mansion.angel, mansion.hebrew, orthography.gematria(mansion.hebrew));
    }
    if (action === 'export' && names.length) {
      const blob = new Blob([JSON.stringify({tableOrder:order, utc:state ? state.utc : null, method:engine.spec.edition, source:engine.spec.source, names}, null, 2)], {type:'application/json'});
      const url = URL.createObjectURL(blob); const link = document.createElement('a'); link.href=url;
      link.download=`angeli_lunari_tavola_${order}.json`; link.click(); setTimeout(()=>URL.revokeObjectURL(url),1000);
    }
  });
  return {setState, showError, refreshPanels, panelHTML, getState:()=>state, setTraceHandler:handler=>{trace=handler;}};
}
