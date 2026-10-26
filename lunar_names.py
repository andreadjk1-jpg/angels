"""Derivazione lunare dalla tavola planetaria di Agrippa, III.27 (1651, p. 433)."""
import json
from pathlib import Path

from hebrew_orthography import hebrew_gematria, transliterate_hebrew

ALPHABET = 'אבגדהוזחטיכלמנסעפצקרשת'
# Colonna sotto la Luna, ingresso discendente dei nomi buoni, in ordine Aleph–Tav.
# Si conserva Peh nella riga Tsadi, come nella trascrizione del testo del 1651.
MOON_COLUMN = 'זנשומרהלקדכצגיפבטפאחסת'
FINAL_TO_NORMAL = str.maketrans('ךםןףץ', 'כמנפצ')
ORDERS = ['Angeli', 'Arcangeli', 'Principati', 'Virtù', 'Potestà',
          'Dominazioni', 'Troni', 'Cherubini', 'Serafini']
SOURCE = 'https://www.esotericarchives.com/agrippa/agripp3b.htm#chap27'
TRANSCRIPTION = 'https://magick.me/library/three-books-of-occult-philosophy/172'


def lunar_hierarchy(seed, suffix='אל', depth=9):
    if suffix not in ('אל', 'יה'):
        raise ValueError('Scegliere il suffisso אל oppure יה.')
    if not isinstance(depth, int) or isinstance(depth, bool) or not 1 <= depth <= 9:
        raise ValueError('I gradi della gerarchia devono essere da 1 a 9.')
    current = ''.join(ch for ch in seed.translate(FINAL_TO_NORMAL) if ch in ALPHABET)
    if not current:
        raise ValueError('Inserire un nome di partenza in lettere ebraiche.')
    substitution = dict(zip(ALPHABET, MOON_COLUMN))
    result = []
    for level in range(depth):
        root = ''.join(substitution[ch] for ch in current)
        name = root + suffix
        result.append({'level': level + 1, 'order': ORDERS[level], 'seed': current,
                       'root_heb': root, 'hebrew': name, 'latin': transliterate_hebrew(name),
                       'gematria': hebrew_gematria(name),
                       'steps': [{'from': ch, 'to': substitution[ch]} for ch in current]})
        # La variante adottata reinserisce il nome completo precedente, suffisso incluso.
        current = name
    return result


def lunar_spec(spheres):
    mansions = sorted(({'num': n, 'name': mansion, 'angel': angel, 'hebrew': hebrew,
                       'start': (n - 1) * 360 / 28, 'end': n * 360 / 28}
                      for s in spheres for n, mansion, angel, hebrew in s['mansions']),
                     key=lambda item: item['num'])
    if [item['num'] for item in mansions] != list(range(1, 29)):
        raise ValueError('Devono essere presenti esattamente le 28 mansioni.')
    return {'alphabet': ALPHABET, 'moonColumn': MOON_COLUMN, 'orders': ORDERS,
            'mansions': mansions, 'source': SOURCE, 'transcription': TRANSCRIPTION,
            'edition': '1651, p. 433; colonna lunare letta dall’ingresso discendente',
            'readingNote': 'La riga Tsadi conserva Peh, come nella trascrizione del 1651. '
                           'L’ingresso Ayin illeggibile è identificato dalla successione alfabetica delle righe.',
            'iterationRule': 'Ogni grado reinserisce il nome completo precedente, suffisso incluso.'}


def export_lunar_catalog(spheres, base_dir):
    spec = lunar_spec(spheres)
    catalog = {'method': spec['edition'], 'source': SOURCE, 'transcription': TRANSCRIPTION,
               'iterationRule': spec['iterationRule'], 'readingNote': spec['readingNote'],
               'projection': '9×9: tavola lunare classica; sulle altre tavole il tracciamento è una proiezione del progetto.',
               'mansions': [{**m, 'generated': lunar_hierarchy(m['hebrew'])} for m in spec['mansions']]}
    target = Path(base_dir)
    (target / 'lunar_angels_generated.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Nomi lunari derivati: 28 nomi di partenza × 9 gradi', '',
             'Metodo: tavola planetaria, colonna della Luna, Agrippa III.27, edizione 1651 p. 433.',
             f'Fonte: {SOURCE}', f'Trascrizione: {TRANSCRIPTION}', '',
             spec['readingNote'], spec['iterationRule'], catalog['projection'], '']
    for mansion in catalog['mansions']:
        lines.extend([f"## {mansion['num']}. {mansion['name']} — {mansion['angel']} ({mansion['hebrew']})", '',
                      '| Grado | Ordine | Nome ebraico derivato | Traslitterazione | Gematria |',
                      '|---|---|---|---|---|'])
        for item in mansion['generated']:
            lines.append(f"| {item['level']} | {item['order']} | {item['hebrew']} | {item['latin']} | {item['gematria']} |")
        lines.append('')
    (target / 'lunar_generated_angels.md').write_text('\n'.join(lines), encoding='utf-8')
    return spec
