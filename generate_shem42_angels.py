"""Generatore offline dal Nome di 42 lettere sulle diciannove tavole del progetto.

Eseguire: python -X utf8 generate_shem42_angels.py
Otto ingressi × diciannove tavole × due suffissi × nove gradi = 2736 derivazioni.
"""
from html import escape
import json
from pathlib import Path

from divine_names import shem42_spec
from hebrew_orthography import browser_spec
from shem42_table_names import generate_records,table_spec

BASE=Path(__file__).resolve().parent


def build_shem42_generator(base_dir=BASE):
    target=Path(base_dir)
    divine,tables=shem42_spec(),table_spec()
    records=generate_records()
    catalog={'schemaVersion':1,'title':'Nomi derivati dal Nome di 42 lettere sulle diciannove tavole',
             'rule':tables['rule'],'iterationRule':tables['iterationRule'],
             'methodStatus':tables['methodStatus'],'scopeNote':tables['scopeNote'],
             'sources':tables['sources'],'divineSource':divine['source'],
             'scope':'Nome completo e sette gruppi, tavole da 3×3 a 21×21, due suffissi, fino a nove gradi.',
             'counts':{'derivations':len(records),'distinctSpellings':len({item['hebrew'] for item in records})},
             'seeds':[divine['full'],*divine['groups']],'records':records}
    (target/'shem42_generated_angels.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Nomi dal Nome di 42 lettere sulle diciannove tavole','',catalog['scope'],tables['methodStatus'],'',
           f"{len(records)} derivazioni; {catalog['counts']['distinctSpellings']} grafie ebraiche distinte.",'',
           tables['rule'],tables['iterationRule'],tables['scopeNote'],'',
           'Fonte del Nome di 42 lettere: '+divine['source'],'',
           '| ID | Ingresso | Tavola | Suffisso | Grado | Nome ebraico derivato | Gematria |',
           '|---|---|---|---|---|---|---|']
    for item in records:
        lines.append(f"| {item['id']} | {item['source_hebrew']} | {item['table_order']}×{item['table_order']} | {item['suffix']} | {item['level']} | {item['hebrew']} | {item['gematria']} |")
    (target/'shem42_generated_angels.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    template=(BASE/'shem42_generator_template.html').read_text(encoding='utf-8')
    payload={'divine':divine,'tables':tables,'catalogMeta':{key:value for key,value in catalog.items() if key not in ('records','seeds')}}
    scripts='\n'.join((BASE/name).read_text(encoding='utf-8') for name in ('orthography.js','shem42_table_engine.js'))
    scripts+='\nconst Orthography=createOrthography('+json.dumps(browser_spec({}),ensure_ascii=False)+');\n'
    scripts+='const SHEM42_DATA='+json.dumps(payload,ensure_ascii=False).replace('<','\\u003c')+';\n'
    scripts+='const Table42Engine=createShem42TableEngine(Orthography,SHEM42_DATA.tables);\n'
    scripts+=(BASE/'shem42_generator_ui.js').read_text(encoding='utf-8')
    page=template.replace('<!-- GENERATOR_ENGINE -->','<script>\n'+scripts+'\n</script>')
    page=page.replace('<!-- FULL_NAME -->',escape(divine['full']['hebrew']))
    (target/'shem42_angel_generator.html').write_text(page,encoding='utf-8')
    print(f"Creato shem42_angel_generator.html: {len(records)} derivazioni, {catalog['counts']['distinctSpellings']} grafie distinte.")
    return catalog


if __name__=='__main__':
    build_shem42_generator()
