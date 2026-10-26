"""Nome di 42 lettere nella forma acrostica di Ana Bekoach, sette gruppi di sei.

Testo e acrostici: Open Siddur, fonte liturgica distinta dalle tavole di Agrippa.
Le forme finali presenti nell'edizione sono conservate, con gematria ordinaria.
"""
from html import escape
import json
from pathlib import Path

from hebrew_orthography import HEBREW_ALPHABET, hebrew_gematria, transliterate_hebrew

SOURCE = 'https://opensiddur.org/prayers/life-cycle/death/dying/ana-bkhoah-a-42-letter-name-piyyut-translated-by-reb-zalman/'
GROUPS_42 = (
    ('אבגיתץ', 'אנא בכח גדלת ימינך תתיר צרורה'),
    ('קרעשטן', 'קבל רנת עמך שגבנו טהרנו נורא'),
    ('נגדיכש', 'נא גבור דורשי יחודך כבבת שמרם'),
    ('בטרצתג', 'ברכם טהרם רחמי צדקתך תמיד גמלם'),
    ('חקבטנע', 'חסין קדוש ברוב טובך נהל עדתך'),
    ('יגלפזק', 'יחיד גאה לעמך פנה זוכרי קדשתך'),
    ('שקוצית', 'שועתנו קבל ושמע צעקתנו יודע תעלומות'),
)
FINAL_TO_NORMAL = str.maketrans('ךםןףץ', 'כמנפצ')


def shem42_spec():
    groups = []
    for index, (hebrew, line) in enumerate(GROUPS_42, 1):
        words = line.split()
        if len(hebrew) != 6 or len(words) != 6 or ''.join(word[0] for word in words) != hebrew.translate(FINAL_TO_NORMAL):
            raise ValueError(f'Acrostico di sei lettere non valido: gruppo {index}.')
        groups.append({'id': f'group-{index}', 'label': f'Gruppo {index}', 'number': index,
                       'hebrew': hebrew, 'letters': 6, 'latin': transliterate_hebrew(hebrew),
                       'gematria': hebrew_gematria(hebrew), 'prayer': line})
    full = ' '.join(item['hebrew'] for item in groups)
    count = sum(ch in HEBREW_ALPHABET for ch in full)
    if count != 42:
        raise ValueError('Il Nome deve contenere esattamente 42 lettere.')
    return {'title': 'Nome divino di 42 lettere · Ana Bekoach', 'source': SOURCE,
            'form': 'Acrostico di Ana Bekoach: sette gruppi di sei lettere.',
            'orthographyNote': 'Le forme finali ץ e ן sono conservate alla fine dei gruppi; '
                               'per acrostico e sostituzioni valgono come צ e נ. Gematria ordinaria.',
            'projectionNote': 'Il tracciamento di questo Nome sulle tavole è una convenzione del progetto. '
                              'La successiva derivazione lunare usa separatamente la colonna della Luna di Agrippa III.27.',
            'full': {'id': 'full', 'label': 'Nome completo di 42 lettere', 'hebrew': full, 'letters': count,
                     'latin': transliterate_hebrew(full), 'gematria': hebrew_gematria(full)},
            'groups': groups}


def known_divine_names():
    """Alias espliciti del Nome; Ana Bekoach da solo indica invece la preghiera."""
    full = shem42_spec()['full']['hebrew']
    return {alias: full for alias in ('Shem 42', 'Shem Mem Bet', 'Nome di 42 lettere', 'Nome 42')}


def export_shem42(base_dir):
    spec = shem42_spec()
    target = Path(base_dir)
    (target / 'shem42_divine_names.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# ' + spec['title'], '', spec['form'], '',
             spec['full']['hebrew'], '', f"42 lettere · gematria ordinaria: {spec['full']['gematria']}.", '',
             '| Gruppo | Sei lettere | Traslitterazione consonantica | Gematria | Verso di sei parole |',
             '|---|---|---|---|---|']
    for item in spec['groups']:
        lines.append(f"| {item['number']} | {item['hebrew']} | {item['latin']} | {item['gematria']} | {item['prayer']} |")
    lines.extend(['', spec['orthographyNote'], '', spec['projectionNote'], '',
                  'Il Nome è riportato come sequenza divina; i nomi angelici eventualmente derivati sono risultati del metodo scelto.', '',
                  'Fonte degli acrostici e del testo ebraico tradizionale (qui senza segni vocalici): ' + SOURCE, '',
                  'La formula di chiusura «Baruch shem…» è esterna alle sette righe dell’acrostico.', ''])
    (target / 'shem42_letter_name.md').write_text('\n'.join(lines), encoding='utf-8')
    return spec


def shem42_overview(spec):
    rows = ''.join(f'<tr><td>{item["number"]}</td><td><bdi dir="rtl" class="hebrew">{item["hebrew"][:3]} {item["hebrew"][3:]}</bdi></td>'
                   f'<td style="overflow-wrap:anywhere;">{item["latin"]}</td><td>{item["gematria"]}</td>'
                   f'<td><bdi dir="rtl" class="hebrew">{escape(item["prayer"])}</bdi></td></tr>' for item in spec['groups'])
    return f'''<!-- divine42-overview:start -->
<section id="divineNames42" style="margin:18px 0; padding:16px; border:1px solid var(--gold); border-radius:10px; min-width:0;">
  <h2 style="color:var(--gold-bright); margin-top:0; font-size:1.2rem;">{spec['title']}</h2>
  <p>Sette gruppi di sei lettere: <strong>42 lettere complessive</strong> · gematria ordinaria totale <strong data-divine42-total>{spec['full']['gematria']}</strong>.</p>
  <p style="font-size:1.25rem; overflow-wrap:anywhere;"><bdi dir="rtl" class="hebrew" data-divine42-full>{spec['full']['hebrew']}</bdi></p>
  <p>In ogni tavola apri «Nome divino di 42 lettere» per tracciare il Nome completo o un gruppo, oppure usarlo come partenza della derivazione lunare.</p>
  <details><summary style="cursor:pointer;">Sette gruppi, gematria e acrostico delle iniziali</summary>
    <div style="overflow-x:auto;"><table style="width:100%;"><thead><tr><th>N.</th><th>Sei lettere</th><th>Traslitterazione consonantica</th><th>Gematria</th><th>Verso di sei parole</th></tr></thead><tbody>{rows}</tbody></table></div>
    <p>{spec['orthographyNote']}</p><p>{spec['projectionNote']}</p>
    <p>Questa è la forma acrostica di Ana Bekoach. La formula di chiusura «Baruch shem…» è esterna alle sette righe.</p>
    <p><a href="{spec['source']}" target="_blank" rel="noopener noreferrer">Fonte: testo e acrostici di Ana Bekoach, Open Siddur</a></p>
  </details>
  <p><a href="shem42_angel_generator.html">Genera nuovi nomi dal Nome di 42 lettere sulle tue 19 tavole →</a></p>
  <p><a href="complete_angel_catalog.html">Catalogo completo in ebraico, raggruppato per sfera →</a></p>
  <p style="margin-bottom:0;"><a href="shem42_letter_name.md">Catalogo leggibile</a> · <a href="shem42_divine_names.json">Dati JSON</a></p>
</section>
<!-- divine42-overview:end -->'''
