/* Interfaccia del generatore: nessuna effemeride o colonna planetaria. */
const Shem42Generator=(()=>{
  'use strict';
  const $=id=>document.getElementById(id),escape=value=>String(value).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
  const allSeeds=[SHEM42_DATA.divine.full,...SHEM42_DATA.divine.groups],allOrders=SHEM42_DATA.tables.tables.map(table=>table.order);
  let records=[],visible=[],matched=[],selected=null;
  function config() {
    const seedChoice=$('s42Seed').value,tableChoice=$('s42Table').value,suffixChoice=$('s42Suffix').value;
    const seeds=seedChoice==='groups'?SHEM42_DATA.divine.groups:seedChoice==='all'?allSeeds:allSeeds.filter(seed=>seed.id===seedChoice);
    const orders=tableChoice==='all'?allOrders:tableChoice==='classic'?allOrders.filter(n=>n<=9):tableChoice==='higher'?allOrders.filter(n=>n>=10):[Number(tableChoice)];
    if(!seeds.length) throw new Error('Scegli un nome di partenza.');
    return {seeds,orders,suffixes:suffixChoice==='both'?['אל','יה']:[suffixChoice],depth:Number($('s42Depth').value)};
  }
  function render() {
    const query=$('s42Search').value.trim();
    const normalized=Table42Engine.normalize(query);
    matched=records.filter(item=>!query||(normalized&&item.hebrew.includes(normalized))||String(item.gematria)===query);
    const byName=new Map();
    for(const item of matched) {if(!byName.has(item.hebrew)) byName.set(item.hebrew,[]); byName.get(item.hebrew).push(item);}
    visible=$('s42Unique').checked?[...byName.values()].map(items=>items[0]):matched;
    $('s42ResultsPanel').classList.toggle('pure',$('s42HebrewOnly').checked);
    $('s42Paths').textContent=matched.length.toLocaleString('it-IT');
    $('s42Distinct').textContent=byName.size.toLocaleString('it-IT');
    $('s42Visible').textContent=visible.length.toLocaleString('it-IT');
    $('s42Rows').innerHTML=visible.map(item=>`<tr data-record-id="${item.id}"><td><button type="button" class="name hebrew" lang="he" dir="rtl" data-open-record="${item.id}" aria-label="Mostra le celle di ${item.hebrew}">${item.hebrew}</button><span class="meta">${escape(item.latin)}</span></td><td class="meta">${item.gematria}</td><td class="meta">${escape(item.seed_label)}</td><td class="meta">${item.table_order}×${item.table_order}</td><td class="meta">${item.level}</td><td class="meta hebrew">${item.suffix}</td></tr>`).join('');
    $('s42Empty').hidden=visible.length>0;
    document.querySelectorAll('[data-selection-export]').forEach(button=>{button.disabled=!visible.length;});
    if(selected&&!visible.some(item=>item.id===selected.id)) {$('s42Details').hidden=true; selected=null;}
  }
  function generate() {
    try {
      const options=config();
      records=Table42Engine.generate(options.seeds,options.orders,options.suffixes,options.depth);
      $('s42Error').hidden=true;
    } catch(error) {
      records=[]; $('s42Error').textContent=error.message||String(error); $('s42Error').hidden=false;
    }
    selected=null; $('s42Details').hidden=true; render();
  }
  function showRecord(id) {
    selected=records.find(item=>item.id===id);
    if(!selected) return;
    const item=selected,n=item.table_order,table=Table42Engine.getTable(n),active=new Set(item.steps.map(step=>step.cell));
    $('s42RecordHeading').innerHTML=`<p class="detail-name hebrew" dir="rtl">${item.hebrew}</p><p class="small">${escape(item.seed_label)} · tavola ${n}×${n} · grado ${item.level} · gematria ${item.gematria}</p><p>Ingresso: <bdi class="hebrew">${item.seed}</bdi> → radice letta: <bdi class="hebrew">${item.root_heb}</bdi> + <bdi class="hebrew">${item.suffix}</bdi></p>`;
    const points=item.steps.map(step=>({x:(step.col+.5)*100/n,y:(step.row+.5)*100/n}));
    const first=points[0],last=points[points.length-1];
    $('s42MatrixStage').innerHTML=`<div class="matrix" style="grid-template-columns:repeat(${n},minmax(0,1fr));--cell-font:${n>16?10:n>10?12:16}px">${table.matrix.flat().map(cell=>`<span class="cell hebrew ${active.has(cell)?'active':''}" data-cell="${cell}" title="${cell}">${Orthography.numberToHebrew(cell)}</span>`).join('')}</div><svg class="path" viewBox="0 0 100 100" role="img" aria-label="Percorso di lettura delle celle"><polyline points="${points.map(p=>`${p.x},${p.y}`).join(' ')}" stroke="#7dd7ce" stroke-width=".7" stroke-linejoin="round" fill="none"/><circle cx="${first.x}" cy="${first.y}" r="1.2" fill="none" stroke="#e2c881" stroke-width=".7"/><path d="M${last.x-1.2} ${last.y-1.2} L${last.x+1.2} ${last.y+1.2}" stroke="#e2c881" stroke-width=".7"/></svg>`;
    $('s42Steps').innerHTML=item.steps.map((step,i)=>`<p>${i+1}. <bdi class="hebrew">${step.letter}</bdi> = ${step.value} → cella ${step.cell} (riga ${step.row+1}, colonna ${step.col+1}) → <bdi class="hebrew">${step.numeral}</bdi></p>`).join('')+`<p>Somma delle celle: ${item.root_value} + suffisso ${Orthography.gematria(item.suffix)} = ${item.gematria}.</p>`;
    $('s42Details').hidden=false; $('s42Details').scrollIntoView({behavior:'smooth',block:'start'});
  }
  function selectionPayload() {
    return {...SHEM42_DATA.catalogMeta,counts:{derivations:matched.length,distinctSpellings:new Set(matched.map(item=>item.hebrew)).size},
      selection:{search:$('s42Search').value,oneRowPerSpelling:$('s42Unique').checked,depth:Number($('s42Depth').value)},
      visibleRecordIds:visible.map(item=>item.id),records:matched};
  }
  function completePayload() {
    return {...SHEM42_DATA.catalogMeta,seeds:allSeeds,records:Table42Engine.generate(allSeeds,allOrders,['אל','יה'],9)};
  }
  function plainHtml() {
    return '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>שמות</title><style>body{max-width:960px;margin:40px auto;padding:0 20px;font:26px/1.8 "Times New Roman",serif;color:#151515;background:#fff}li{padding:12px 0;overflow-wrap:anywhere;break-inside:avoid}ol{list-style:none;padding:0}</style></head><body><ol>'+visible.map(item=>'<li>'+escape(item.hebrew)+'</li>').join('')+'</ol></'+'body></html>';
  }
  function download(name,type,text) {
    const url=URL.createObjectURL(new Blob([text],{type}));
    const link=document.createElement('a'); link.href=url; link.download=name; link.click(); setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  $('s42Seed').innerHTML='<option value="groups">I sette gruppi di sei lettere</option><option value="full">Il Nome completo di 42 lettere</option><option value="all">Nome completo e sette gruppi</option>'+SHEM42_DATA.divine.groups.map(seed=>`<option value="${seed.id}">${seed.label} · ${seed.hebrew}</option>`).join('');
  $('s42Table').insertAdjacentHTML('beforeend',allOrders.map(n=>`<option value="${n}">${n}×${n}</option>`).join(''));
  for(const id of ['s42Seed','s42Table','s42Suffix','s42Depth']) $(id).addEventListener('change',generate);
  $('s42Generate').addEventListener('click',generate);
  $('s42Search').addEventListener('input',render);
  for(const id of ['s42Unique','s42HebrewOnly']) $(id).addEventListener('change',render);
  $('s42Rows').addEventListener('click',event=>{const button=event.target.closest('[data-open-record]'); if(button) showRecord(button.dataset.openRecord);});
  $('s42CloseDetails').addEventListener('click',()=>{$('s42Details').hidden=true;selected=null;});
  $('s42ExportJson').addEventListener('click',()=>download('nomi_42_tavole_selezione.json','application/json',JSON.stringify(selectionPayload(),null,2)));
  $('s42ExportTxt').addEventListener('click',()=>download('nomi_42_ebraico.txt','text/plain;charset=utf-8',visible.map(item=>item.hebrew).join('\n')+'\n'));
  $('s42ExportHtml').addEventListener('click',()=>download('nomi_42_ebraico.html','text/html;charset=utf-8',plainHtml()));
  $('s42ExportAll').addEventListener('click',()=>download('shem42_generated_angels.json','application/json',JSON.stringify(completePayload(),null,2)));
  $('s42Rule').textContent=SHEM42_DATA.tables.rule; $('s42Iteration').textContent=SHEM42_DATA.tables.iterationRule;
  $('s42Scope').textContent=SHEM42_DATA.tables.scopeNote;
  $('s42DivineSource').href=SHEM42_DATA.divine.source;
  $('s42CorpusCount').textContent=`${SHEM42_DATA.catalogMeta.counts.derivations.toLocaleString('it-IT')} derivazioni, ${SHEM42_DATA.catalogMeta.counts.distinctSpellings.toLocaleString('it-IT')} grafie distinte`;
  generate();
  return {generate,render,showRecord,selectionPayload,completePayload,plainHtml,getRecords:()=>records,getVisible:()=>visible};
})();
