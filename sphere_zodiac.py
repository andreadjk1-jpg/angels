"""Verifica delle sfere e delle camere del progetto rispetto al riferimento astronomico.

Nessuna camera numerica è trattata come posizione osservata di un pianeta.
Le tredici costellazioni riportate riguardano il percorso del Sole sull'eclittica.
"""
from pathlib import Path
import json

SIGN_HEBREW=['טלה','שור','תאומים','סרטן','אריה','בתולה','מאזניים','עקרב','קשת','גדי','דלי','דגים']
SIGN_ITALIAN=['Ariete','Toro','Gemelli','Cancro','Leone','Vergine','Bilancia','Scorpione','Sagittario','Capricorno','Acquario','Pesci']
SPHERES=(
    (1,'הגלגל הראשון · כתר','Primum Mobile / Kether',[10],'non-observational','ללא שיוך למזל אסטרונומי'),
    (2,'גלגל הכוכבים והמזלות · חכמה','Stelle fisse e Zodiaco / Chokmah',[11],'whole-zodiac','גלגל המזלות כולו'),
    (3,'גלגל שבתאי · בינה','Saturno / Binah',[3,12],'moving-body','המיקום משתנה לפי התאריך והשעה'),
    (4,'גלגל צדק · חסד','Giove / Chesed',[4,13],'moving-body','המיקום משתנה לפי התאריך והשעה'),
    (5,'גלגל מאדים · גבורה','Marte / Geburah',[5,14],'moving-body','המיקום משתנה לפי התאריך והשעה'),
    (6,'גלגל השמש · תפארת','Sole / Tiphereth',[6,15],'moving-body','המיקום משתנה לפי התאריך והשעה'),
    (7,'גלגל נוגה · נצח','Venere / Netzach',[7,16],'moving-body','המיקום משתנה לפי התאריך והשעה'),
    (8,'גלגל כוכב · הוד','Mercurio / Hod',[8,17],'moving-body','המיקום משתנה לפי התאריך והשעה'),
    (9,'גלגל הלבנה · יסוד','Luna / Yesod',[9,18],'moving-body','המיקום משתנה לפי התאריך והשעה'),
    (10,'עולם היסודות · מלכות','Mondo degli elementi / Malkuth',[19],'non-observational','ללא שיוך למזל אסטרונומי'),
    (11,'הרחבה ראשונה · שער תו','Estensione I: Porta di Tav',[20],'symbolic-extension','הרחבה סמלית של הפרויקט'),
    (12,'הרחבה שנייה · אמת','Estensione II: Verità',[21],'symbolic-extension','הרחבה סמלית של הפרויקט'),
)
SOURCES={
    'agrippaSpheres':'https://www.esotericarchives.com/agrippa/agripp2b.htm#chap13',
    'iauZodiac':'https://www.iau.org/IAU/IAU/Astronomy-FAQs/FAQs.aspx',
    'iauBoundaries':'https://www.iau.org/IAU/Astronomy-FAQs/Constellations.aspx',
}


def audit_spheres(metadata):
    if len(metadata)!=12 or sorted(item['sphereNum'] for item in metadata)!=list(range(1,13)):
        raise ValueError('Sono necessarie dieci sfere e due estensioni distinte.')
    by_number={item['sphereNum']:item for item in metadata}
    groups=[]
    for number,hebrew,italian,orders,status,note in SPHERES:
        meta=by_number[number]
        actual=sorted([meta['higherOrder']]+([meta['classicOrder']] if meta['classicOrder'] else []))
        if actual!=orders:raise ValueError(f'Tavole non coerenti con la sfera {number}: {actual}.')
        chamber=(meta['higherOrder']-1)%12+1
        if (meta['chamber12']!=chamber or int(meta['sign'].split('.')[0])!=chamber
                or SIGN_ITALIAN[chamber-1].casefold() not in meta['sign'].casefold()):
            raise ValueError(f'Camera numerica non coerente nella scheda {number}.')
        if bool(meta.get('isExtension'))!=(number>10):
            raise ValueError(f'Sfera ed estensione non distinte nella scheda {number}.')
        groups.append({'id':('sphere-' if number<=10 else 'extension-')+str(number if number<=10 else number-10),
                       'number':number,'kind':'sphere' if number<=10 else 'extension',
                       'nameHebrew':hebrew,'nameItalian':italian,'tableOrders':orders,
                       'astronomicalStatus':status,'astronomicalNoteHebrew':note,
                       'fixedAstronomicalSign':None,
                       'tableChambers':[{'order':order,'chamber':(order-1)%12+1,
                                         'signHebrew':SIGN_HEBREW[(order-1)%12],
                                         'signItalian':SIGN_ITALIAN[(order-1)%12]} for order in orders]})
    order_to_group={order:group['id'] for group in groups for order in group['tableOrders']}
    if set(order_to_group)!=set(range(3,22)) or sum(len(g['tableOrders']) for g in groups)!=19:
        raise ValueError('Le diciannove tavole devono appartenere ciascuna a un solo gruppo.')
    return {'traditionalSphereCount':10,'symbolicExtensionCount':2,
            'traditionalTableAssignmentVerified':True,'projectChamberFormulaVerified':True,
            'fixedSphereToAstronomicalSignCorrespondence':False,'planetaryPositionsComputed':False,
            'chamberFormula':'((N - 1) mod 12) + 1',
            'conclusion':'Le camere delle tavole sono associazioni numeriche del progetto. '
                         'La sfera delle stelle fisse comprende lo Zodiaco nel suo insieme. '
                         'Per i sette astri occorre un istante per calcolare la posizione geocentrica.',
            'tropicalZodiac':{'sectorCount':12,'sectorWidthDegrees':30,
                             'note':'I settori astrologici di 30° si distinguono dalle aree delle costellazioni.'},
            'solarEclipticConstellations':['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra',
                                           'Scorpius','Ophiuchus','Sagittarius','Capricornus','Aquarius','Pisces'],
            'constellationNote':'Il percorso solare attraversa tredici costellazioni di ampiezza diversa; include Ofiuco.',
            'sources':SOURCES,'groups':groups}


def export_zodiac_audit(audit,base_dir):
    target=Path(base_dir)
    (target/'verify_spheres_zodiac.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Verifica delle sfere e dello Zodiaco','',
           'Esito: le associazioni delle camere numeriche non rappresentano uno zodiaco astronomico fisso.',
           '',audit['conclusion'],'',
           'L’ordine delle dieci sfere segue il modello storico di Agrippa, II.13. Le due schede finali restano estensioni simboliche.',
           'Le posizioni planetarie non sono calcolate in questo catalogo statico: una posizione richiede data e ora.',
           'I dodici segni astrologici sono settori di 30°. Le costellazioni astronomiche hanno confini e ampiezze differenti; il percorso solare comprende anche Ofiuco.',
           '', '| Gruppo | Tavole | Camere numeriche del progetto | Riferimento astronomico |',
           '|---|---|---|---|']
    for group in audit['groups']:
        kind='Sfera' if group['kind']=='sphere' else 'Estensione'
        number=group['number'] if kind=='Sfera' else group['number']-10
        chambers='; '.join(f"{item['order']}×{item['order']} → camera {item['chamber']}, {item['signItalian']}" for item in group['tableChambers'])
        status={'non-observational':'Nessun segno astronomico assegnabile',
                'whole-zodiac':'Intero Zodiaco nel modello storico',
                'moving-body':'Posizione variabile, da calcolare per un istante',
                'symbolic-extension':'Nessuna corrispondenza astronomica'}[group['astronomicalStatus']]
        lines.append(f"| {kind} {number}: {group['nameItalian']} | {', '.join(str(n)+'×'+str(n) for n in group['tableOrders'])} | {chambers} | {status} |")
    lines.extend(['','Le camere sono mantenute come convenzioni del progetto; non sono riassegnate a costellazioni senza una data.', '',
                  'Fonti:', '- Agrippa II.13: '+SOURCES['agrippaSpheres'],
                  '- IAU, Zodiaco e Ofiuco: '+SOURCES['iauZodiac'],
                  '- IAU, confini delle costellazioni: '+SOURCES['iauBoundaries'],''])
    (target/'verify_spheres_zodiac.md').write_text('\n'.join(lines),encoding='utf-8')
