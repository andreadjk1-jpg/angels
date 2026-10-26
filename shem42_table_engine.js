/* Lettura delle celle delle diciannove tavole: regola numerica del progetto. */
function createShem42TableEngine(orthography,spec) {
  'use strict';
  const finals={'ך':'כ','ם':'מ','ן':'נ','ף':'פ','ץ':'צ'};
  const tables=new Map(spec.tables.map(table=>[table.order,{...table,
    coords:new Map(table.matrix.flatMap((row,r)=>row.map((cell,c)=>[cell,{row:r,col:c}])))}]));
  const normalize=seed=>[...String(seed)].map(ch=>finals[ch]||ch).filter(ch=>orthography.letters[ch]).join('');
  function reduceToCell(value,maxCell) {
    if(!Number.isSafeInteger(value)||value<1||!Number.isSafeInteger(maxCell)||maxCell<1) throw new Error('Valore della lettera o capacità della tavola non valido.');
    while(value>maxCell) {
      if(value%10===0) value=Math.floor(value/10);
      else {const root=Math.floor(value/10); value=root>0&&root<=maxCell?root:((value-1)%maxCell)+1;}
    }
    return value;
  }
  function hierarchy(seed,order=9,suffix='אל',depth=1) {
    const table=tables.get(order);
    if(!Number.isInteger(order)||!table) throw new Error('Scegli una tavola da 3×3 a 21×21.');
    if(!['אל','יה'].includes(suffix)||!Number.isInteger(depth)||depth<1||depth>9) throw new Error('Suffisso o numero di gradi non valido.');
    let current=normalize(seed);
    if(!current) throw new Error('Il nome di partenza deve contenere lettere ebraiche.');
    const result=[];
    for(let level=1;level<=depth;level++) {
      const steps=[...current].map(letter=>{
        const value=orthography.letters[letter].val,cell=reduceToCell(value,table.cells);
        return {letter,value,cell,...table.coords.get(cell),numeral:orthography.numberToHebrew(cell)};
      });
      const root=steps.map(step=>step.numeral).join(''),hebrew=root+suffix;
      result.push({level,seed:current,root_heb:root,hebrew,latin:orthography.transliterateHebrew(hebrew),
        gematria:orthography.gematria(hebrew),root_value:steps.reduce((sum,step)=>sum+step.cell,0),steps});
      current=hebrew;
    }
    return result;
  }
  function generate(seeds,orders,suffixes,depth=1) {
    const result=[];
    for(const seed of seeds) for(const order of orders) for(const suffix of suffixes) {
      const suffixId=suffix==='אל'?'el':'yah';
      for(const name of hierarchy(seed.hebrew,order,suffix,depth)) result.push({
        id:`s42-${seed.id}-table-${order}-${suffixId}-${name.level}`,seed_id:seed.id,seed_label:seed.label,
        source_hebrew:seed.hebrew,table_order:order,suffix,...name});
    }
    return result;
  }
  return {spec,normalize,reduceToCell,hierarchy,generate,getTable:order=>tables.get(order)};
}
