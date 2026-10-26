"""Catalogo statico dei nomi presenti nel progetto, raggruppati per sfera.

Eseguire dopo la rigenerazione delle sorgenti: python -X utf8 build_complete_catalog.py
Il documento finale non richiede script, risorse esterne, effemeridi o server.
"""
import ast
from collections import Counter,defaultdict
import hashlib
from html import escape
import json
from pathlib import Path
import re
import unicodedata

from hebrew_orthography import HEBREW_ALPHABET,hebrew_gematria
from sphere_zodiac import audit_spheres,export_zodiac_audit

BASE=Path(__file__).resolve().parent
ALPHABET='אבגדהוזחטיכלמנסעפצקרשת'
FINALS=str.maketrans('ךםןףץ','כמנפצ')
KIND_LABELS={'angel':'מלאך','generated':'שם מחושב','spirit':'רוח','divine':'שם קודש',
             'choir':'מקהלה','attribute':'ספירה','archive':'שם מן הארכיון'}
FAMILY_LABELS={'structural':'שמות הטבלאות','lunar':'שמות מחושבים מן הלבנה',
               'shem42':'שמות מחושבים משם מ״ב','shem72':'שבעים ושניים השמות',
               'mansions':'מלאכי כ״ח המחנות','divine42':'שם מ״ב וקבוצותיו',
               'archive':'הארכיון','sphere':'שמות הספירות והטבלאות','elements':'שמות היסודות'}


def js_literal(source,name):
    """Legge dati JS letterali senza eseguire codice o richiedere un browser."""
    match=re.search(r'\bconst\s+'+re.escape(name)+r'\s*=\s*',source)
    if not match:raise ValueError('Dato assente: '+name)
    i=match.end();stack=[];tokens=[];started=False
    while i<len(source):
        ch=source[i]
        if ch.isspace():tokens.append(ch);i+=1;continue
        if source.startswith('//',i):
            end=source.find('\n',i);i=len(source) if end<0 else end;continue
        if source.startswith('/*',i):
            end=source.find('*/',i+2)
            if end<0:raise ValueError('Commento non chiuso.')
            i=end+2;continue
        if ch in "'\"":
            end=i+1
            while end<len(source):
                if source[end]=='\\':end+=2;continue
                if source[end]==ch:break
                end+=1
            tokens.append(repr(ast.literal_eval(source[i:end+1])));i=end+1;continue
        ident=re.match(r'[A-Za-z_$][A-Za-z0-9_$]*',source[i:])
        if ident:
            word=ident[0];i+=len(word)
            rest=source[i:].lstrip()
            if rest.startswith(':'):tokens.append(repr(word))
            elif word in {'true','false','null'}:tokens.append({'true':'True','false':'False','null':'None'}[word])
            else:raise ValueError('Espressione non letterale: '+word)
            continue
        if ch in '[{':stack.append(ch);started=True
        elif ch in ']}':
            if not stack or stack.pop()!=('[' if ch==']' else '{'):raise ValueError('Delimitatori non validi.')
        elif not (ch.isdigit() or ch in '-+.,:'):
            raise ValueError('Token non supportato nella dichiarazione '+name+': '+ch)
        tokens.append(ch);i+=1
        if started and not stack:return ast.literal_eval(''.join(tokens))
    raise ValueError('Dichiarazione incompleta: '+name)


def clean_hebrew(value):
    text=unicodedata.normalize('NFC',str(value))
    return ' '.join(''.join(ch for ch in word if ch in HEBREW_ALPHABET) for word in text.split()).strip()


def name_key(value):return ''.join(clean_hebrew(value).split())


def classify(role):
    text=role.casefold()
    if 'divin' in text:return 'divine'
    if 'sephir' in text or 'conoscenza' in text:return 'attribute'
    if 'coro' in text or 'choir' in text:return 'choir'
    if 'spirit' in text:return 'spirit'
    if any(word in text for word in ('angel','intelligenz','custod')):return 'angel'
    return 'archive'


def collect_catalog(base_dir=BASE):
    base=Path(base_dir);source=(base/'index.html').read_text(encoding='utf-8')
    metadata=js_literal(source,'ORTHOGRAPHY_SPHERES')
    spheres=js_literal(source,'SPHERES_DATA')
    zodiac=js_literal(source,'ZODIAC_12_DATA')
    shem=js_literal(source,'SHEM_72_ANGELS')
    mansions=js_literal(source,'MANSIONS_28_LUNA')
    elements=js_literal(source,'ELEMENTS_4_DATA')
    latin=js_literal(source,'LATIN_NAMES_BY_SPHERE')
    orth_match=re.search(r'const\s+Orthography\s*=\s*createOrthography\(',source)
    known=json.JSONDecoder().raw_decode(source[orth_match.end():])[0]['knownNames']
    entries={};occurrence_counts=Counter();source_files={'index.html'}

    def add(raw,family,path,kind='archive',orders=(),label='',record_id=None):
        hebrew=clean_hebrew(raw);key=name_key(hebrew)
        if not key:return
        if any(not 3<=order<=21 for order in orders):raise ValueError('Tavola fuori intervallo.')
        if key not in entries:
            entries[key]={'id':'name-'+hashlib.sha256(key.encode('utf-8')).hexdigest()[:14],
                          'hebrew':hebrew,'key':key,'spellings':set(),'kinds':set(),'families':set(),
                          'tableOrders':set(),'occurrences':[]}
        entry=entries[key]
        entry['spellings'].add(hebrew);entry['kinds'].add(kind);entry['families'].add(family)
        entry['tableOrders'].update(orders)
        occurrence={'family':family,'path':path,'kind':kind,'tableOrders':sorted(set(orders))}
        if label:occurrence['label']=label
        if record_id:occurrence['recordId']=record_id
        entry['occurrences'].append(occurrence);occurrence_counts[family]+=1

    def labeled(raw,family,path,kind,orders):
        for index,hebrew in enumerate(re.findall(r'([א-ת][א-ת\u0591-\u05c7 ]*)',str(raw))):
            if name_key(hebrew):add(hebrew,family,path+f'/hebrew-{index}',kind,orders)

    shem_orders=defaultdict(set);mansion_orders=defaultdict(lambda:{9,18});sphere_orders={}
    for index,meta in enumerate(metadata):
        orders=[meta['higherOrder']]+([meta['classicOrder']] if meta['classicOrder'] else [])
        sphere_orders[meta['sphereNum']]=orders
        prefix=f'index.html/ORTHOGRAPHY_SPHERES/{index}'
        for field,kind in [('divineHeb','divine'),('permYHVH','divine'),('intHeb','generated'),('spirHeb','generated'),('signAngelHeb','angel')]:
            add(meta[field],'sphere',prefix+'/'+field,kind,orders)
        for field,kind in [('archangel','angel'),('choir','choir'),('divineName','divine'),('sephirah','attribute')]:
            labeled(meta[field],'sphere',prefix+'/'+field,kind,orders)
        for number,_,_,_ in meta['mansions']:mansion_orders[number].update(orders)
        start,end=meta['shemRange']
        for number in range(start,end+1):shem_orders[number].update(orders)

    for index,sphere in enumerate(spheres):
        orders=sphere_orders[sphere['sphereNum']];prefix=f'index.html/SPHERES_DATA/{index}'
        for field,kind in [('divineHebrew','divine'),('archangelHebrew','angel'),('intelligenceHebrew','angel'),('spiritHebrew','spirit')]:
            if sphere.get(field):add(sphere[field],'archive',prefix+'/'+field,kind,orders)
        for field,kind in [('archangel','angel'),('angelicChoir','choir'),('sephirah','attribute'),('divineName','divine')]:
            labeled(sphere.get(field,''),'archive',prefix+'/'+field,kind,orders)
        for number,entity in enumerate(sphere.get('entities',[])):
            add(entity['hebrew'],'archive',prefix+f'/entities/{number}',classify(entity.get('role','')),orders,entity.get('name',''))
        for field,value in latin.get(sphere['id'],{}).items():
            if field.endswith('Heb'):
                chosen=[sphere['order']] if field.startswith('classic') and sphere.get('order') else [max(orders)]
                add(value,'archive',f'index.html/LATIN_NAMES_BY_SPHERE/{sphere["id"]}/{field}','archive',chosen)

    # Le cinque schede senza kamea classica costruiscono le entità all'avvio.
    # Si leggono anche questi elenchi letterali, senza eseguire la pagina.
    by_id={sphere['id']:sphere for sphere in spheres}
    for match in re.finditer(r"(?:if|else if)\s*\(s\.id\s*===\s*'([^']+)'\)\s*\{\s*s\.entities\s*=\s*",source):
        sphere_id=match[1]
        entities=js_literal('const CATALOG_ENTITIES = '+source[match.end():],'CATALOG_ENTITIES')
        orders=sphere_orders[by_id[sphere_id]['sphereNum']]
        for index,entity in enumerate(entities):
            add(entity['hebrew'],'archive',f'index.html/runtimeEntities/{sphere_id}/{index}',
                classify(entity.get('role','')),orders,entity.get('name',''))

    for index,item in enumerate(zodiac):
        orders=[meta['higherOrder'] for meta in metadata if meta['chamber12']==index+1]
        add(item['angelHeb'],'archive',f'index.html/ZODIAC_12_DATA/{index}/angelHeb','angel',orders)
        labeled(item['permYHVH'],'archive',f'index.html/ZODIAC_12_DATA/{index}/permYHVH','divine',orders)
    for index,item in enumerate(shem):
        label,hebrew=(item[0],item[1]) if isinstance(item,list) else (item['name'],item['heb'])
        add(hebrew,'shem72',f'index.html/SHEM_72_ANGELS/{index}','angel',shem_orders[index+1],label)
    for index,item in enumerate(mansions):
        add(item['heb'],'mansions',f'index.html/MANSIONS_28_LUNA/{index}','angel',mansion_orders[item['num']],item['angel'])
    for index,item in enumerate(elements):
        for field in ('archangel','ruler'):labeled(item[field],'elements',f'index.html/ELEMENTS_4_DATA/{index}/{field}','angel',[19])
    for label,hebrew in known.items():
        existing=entries.get(name_key(hebrew))
        orders=sorted(existing['tableOrders']) if existing else [9]
        add(hebrew,'archive','index.html/Orthography/knownNames/'+label,'archive',orders,label)

    def walk(value,path):
        if isinstance(value,dict):
            if all(key in value for key in ('latin','hebrew','gematria')):yield value,path
            for key,child in value.items():yield from walk(child,path+'/'+key)
        elif isinstance(value,list):
            for index,child in enumerate(value):yield from walk(child,path+'/'+str(index))
    filename='table_angels_generated.json';source_files.add(filename)
    for table_id,table in json.loads((base/filename).read_text(encoding='utf-8')).items():
        for record,path in walk(table,filename+'/'+table_id):add(record['hebrew'],'structural',path,'generated',[table['order']],record['latin'])
    filename='lunar_angels_generated.json';source_files.add(filename)
    for mansion in json.loads((base/filename).read_text(encoding='utf-8'))['mansions']:
        for index,record in enumerate(mansion['generated']):add(record['hebrew'],'lunar',filename+f'/mansions/{mansion["num"]}/generated/{index}','generated',[9,18],record['latin'])
    filename='shem42_generated_angels.json';source_files.add(filename)
    for record in json.loads((base/filename).read_text(encoding='utf-8'))['records']:
        add(record['hebrew'],'shem42',filename+'/'+record['id'],'generated',[record['table_order']],record['latin'],record['id'])
    filename='shem42_divine_names.json';source_files.add(filename)
    divine=json.loads((base/filename).read_text(encoding='utf-8'))
    for record in [divine['full'],*divine['groups']]:add(record['hebrew'],'divine42',filename+'/'+record['id'],'divine',range(3,22))

    result=[]
    for entry in entries.values():
        for field in ('spellings','kinds','families','tableOrders'):entry[field]=sorted(entry[field])
        if not entry['tableOrders']:raise ValueError('Nome senza tavola: '+entry['hebrew'])
        if 'generated' in entry['kinds']:
            entry['kinds']=[kind for kind in entry['kinds'] if kind!='archive']
        if len(entry['kinds'])>1 and 'archive' in entry['kinds']:entry['kinds'].remove('archive')
        entry['gematria']=hebrew_gematria(entry['hebrew'])
        result.append(entry)
    rank={letter:index for index,letter in enumerate(ALPHABET)}
    result.sort(key=lambda entry:(tuple(rank[ch] for ch in entry['key'].translate(FINALS)),entry['key']))
    audit=audit_spheres(metadata)
    groups=audit['groups']
    order_to_group={order:group['id'] for group in groups for order in group['tableOrders']}
    for entry in result:
        memberships={order_to_group[order] for order in entry['tableOrders']}
        entry['groupIds']=[group['id'] for group in groups if group['id'] in memberships]
    for group in groups:
        group['entryIds']=[entry['id'] for entry in result if group['id'] in entry['groupIds']]
        group['nameCount']=len(group['entryIds'])
    return {'schemaVersion':2,'scope':'Tutti i nomi già presenti nelle sorgenti del progetto, raggruppati nelle dieci sfere e nelle due estensioni.',
            'deduplication':'Si uniscono solo varianti di spaziatura. Lettere finali e grafie diverse restano distinte.',
            'presentation':'Solo testo ebraico, senza sigilli. Ogni nome compare una volta in ciascun gruppo associato alle sue tavole.',
            'counts':{'entries':len(result),'occurrences':sum(occurrence_counts.values()),'families':dict(sorted(occurrence_counts.items())),
                      'tableAssociations':sum(len(entry['tableOrders']) for entry in result),
                      'groupMemberships':sum(len(entry['groupIds']) for entry in result)},
            'sources':{name:hashlib.sha256((base/name).read_bytes()).hexdigest() for name in sorted(source_files)},
            'zodiacAudit':audit,'sphereGroups':groups,'entries':result}


def render_catalog(manifest):
    entries=manifest['entries'];groups=manifest['sphereGroups'];by_group={group['id']:group for group in groups}
    nav=''.join(f'<a href="#{group["id"]}">{escape(group["nameHebrew"])} <span>{group["nameCount"]}</span></a>' for group in groups)
    sections=[]
    for group in groups:
        group_orders=set(group['tableOrders'])
        cards=[]
        for entry in entries:
            if group['id'] not in entry['groupIds']:continue
            occurrences=[item for item in entry['occurrences'] if group_orders.intersection(item['tableOrders'])]
            kinds=' · '.join(KIND_LABELS[kind] for kind in entry['kinds'])
            families=' · '.join(FAMILY_LABELS[family] for family in sorted({item['family'] for item in occurrences}))
            orders=sorted(group_orders.intersection(entry['tableOrders']))
            table_text=' · '.join(f'<bdi dir="ltr">{order}×{order}</bdi>' for order in orders)
            related=[other for other in entry['groupIds'] if other!=group['id']]
            related_links=''
            if related:
                related_links='<p class="related">קבוצות נוספות: '+' · '.join(f'<a href="#{entry["id"]}--{other}">{escape(by_group[other]["nameHebrew"])}</a>' for other in related)+'</p>'
            spellings=''
            if len(entry['spellings'])>1:spellings='<p class="spellings">'+' · '.join(escape(name) for name in entry['spellings'])+'</p>'
            cards.append(f'''<article class="entry" id="{entry['id']}--{group['id']}" data-name="{escape(entry['key'])}" data-group="{group['id']}">
<div class="entry-head"><h3>{escape(entry['hebrew'])}</h3><span class="gematria">{entry['gematria']}</span></div>
<p class="kind">{kinds}</p><p class="tables">טבלאות: {table_text}</p>
<details class="provenance"><summary>מקורות והקשרים · {len(occurrences)}</summary><p>{families}</p>{spellings}{related_links}</details></article>''')
        number=group['number'] if group['kind']=='sphere' else group['number']-10
        kind='גלגל' if group['kind']=='sphere' else 'הרחבה'
        tables=' · '.join(f'<bdi dir="ltr">{n}×{n}</bdi>' for n in group['tableOrders'])
        chambers=' · '.join(f'{item["order"]}×{item["order"]}: חדר {item["chamber"]}, {item["signHebrew"]}' for item in group['tableChambers'])
        sections.append(f'''<section class="sphere-section" id="{group['id']}" data-kind="{group['kind']}">
<h2><span>{kind} {number} · {escape(group['nameHebrew'])}</span><a href="#top" aria-label="חזרה לראש הדף">↑</a></h2>
<p class="group-meta">{group['nameCount']} שמות · טבלאות {tables}</p>
<p class="astronomy-note">{group['astronomicalNoteHebrew']}</p>
<details class="chambers"><summary>החדרים המספריים של הטבלאות</summary><p>{chambers}</p><p>אלה זיקות מספריות של הפרויקט.</p></details>
<div class="entries">{''.join(cards)}</div></section>''')
    template=(BASE/'complete_catalog_template.html').read_text(encoding='utf-8')
    return template.replace('<!-- ENTRY_COUNT -->',str(len(entries))).replace('<!-- MEMBERSHIP_COUNT -->',str(manifest['counts']['groupMemberships'])).replace('<!-- SPHERE_NAV -->',nav).replace('<!-- CATALOG_ENTRIES -->','\n'.join(sections))


def build_complete_catalog(base_dir=BASE):
    base=Path(base_dir);manifest=collect_catalog(base)
    export_zodiac_audit(manifest['zodiacAudit'],base)
    (base/'complete_angel_catalog.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (base/'complete_angel_catalog.html').write_text(render_catalog(manifest),encoding='utf-8')
    print(f"Creato complete_angel_catalog.html: {manifest['counts']['entries']} grafie, {manifest['counts']['groupMemberships']} presenze nelle dieci sfere e nelle due estensioni; nessun sigillo.")
    return manifest


if __name__=='__main__':build_complete_catalog()
